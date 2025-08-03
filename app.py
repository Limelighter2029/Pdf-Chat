import streamlit as st
from dotenv import load_dotenv
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template

# Clear cache at startup
st.cache_data.clear()

# Initialize session state
if "pdf_text" not in st.session_state:
    st.session_state["pdf_text"] = ""

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf.seek(0)
        pdf_reader = PdfReader(pdf)  # so this returns a list of pages
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text  # should return a single string of text in all the pdfs

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    # Check if Google API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
        return None
    
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            transport="rest"
        )
        # embeddings = HuggingFaceEmbeddings(model_name="hkunlp/instructor-large")
        vector_stores = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
        return vector_stores
    except Exception as e:
        st.error(f"Error creating vector store: {str(e)}")
        return None

def get_conversation_chain(vector_store):
    if not os.getenv("GOOGLE_API_KEY"):
        st.error("Google API key not found. Please set GOOGLE_API_KEY in your .env file.")
        return None
    
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            transport="rest"
        )
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vector_store.as_retriever(),
            memory=memory
        )
        return conversation_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {str(e)}")
        return None

def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Please upload and process documents first.")
        return
    
    with st.spinner("Thinking..."):
        try:
            response = st.session_state.conversation({'question': user_question})
            st.session_state.chat_history = response['chat_history']
            for i, message in enumerate(st.session_state.chat_history):
                if i % 2 == 0:
                    st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
                else:
                    st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error processing your question: {str(e)}")

def main():
    load_dotenv()
    
    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    st.write(css, unsafe_allow_html=True)
    st.set_page_config(page_title="Chat with multiple pdfs", page_icon=":books:")
 
    st.header("Chat with multiple pdfs :books:")
    
    # Check for API key
    if not os.getenv("GOOGLE_API_KEY"):
        st.warning("Please set your GOOGLE_API_KEY in a .env file")
        st.info("Create a .env file in your project directory and add: GOOGLE_API_KEY=your_api_key_here")
    
    user_question = st.text_input("Ask a question about the documents provided:")
    if user_question and st.session_state.conversation:
        handle_user_input(user_question)

    with st.sidebar:
        st.subheader("Your Documents")
        pdf_docs = st.file_uploader(
            "Upload your documents and click on 'Process'", 
            accept_multiple_files=True,
            type=['pdf']
        )
        
        if st.button("Process") and pdf_docs:
            with st.spinner("Processing..."):
                try:
                    # get the pdf text
                    raw_text = get_pdf_text(pdf_docs)
                    
                    if not raw_text.strip():
                        st.error("No text could be extracted from the uploaded PDFs.")
                        return
                    
                    # get the text chunks
                    text_chunks = get_text_chunks(raw_text)

                    # create the vector store (numerical representation for the text)
                    vector_store = get_vector_store(text_chunks)
                    
                    if vector_store is None:
                        return

                    # create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store)
                    
                    if st.session_state.conversation:
                        st.success("Documents processed successfully! You can now ask questions.")
                    
                except Exception as e:
                    st.error(f"Error processing documents: {str(e)}")

if __name__ == '__main__':
    main()


# PDF Chat Application

A Streamlit-based application that allows you to chat with multiple PDF documents using Google's Generative AI.

## Features

- Upload multiple PDF documents
- Extract text from PDFs and create embeddings
- Chat with your documents using AI
- Beautiful chat interface with user and bot avatars

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Create a `.env` file in your project directory
4. Add your API key to the `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run the Application

```bash
streamlit run app.py
```

## Usage

1. Upload one or more PDF documents using the file uploader in the sidebar
2. Click "Process" to extract text and create embeddings
3. Ask questions about your documents in the chat interface
4. The AI will answer based on the content of your uploaded PDFs

## Requirements

- Python 3.7+
- Google Generative AI API key
- Internet connection for API calls

## File Structure

```
Pdf_Chat/
├── app.py              # Main application file
├── htmlTemplates.py    # HTML templates for chat interface
├── requirements.txt    # Python dependencies
├── images/            # Avatar images
│   ├── robot.png
│   └── user.png
└── README.md          # This file
```

## Troubleshooting

- **API Key Error**: Make sure you have set the `GOOGLE_API_KEY` in your `.env` file
- **PDF Processing Error**: Ensure your PDFs contain extractable text (not just images)
- **Memory Issues**: For large PDFs, consider splitting them into smaller files 

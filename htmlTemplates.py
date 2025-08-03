css='''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #21ADA9
}
.chat-message.bot {
    background-color: #4C1561
}
.chat-message.avatar {
    width: 15%
}
.chat-message .avatar img{
    max-width: 78px;
    max-height: 78px;
    border-radius: 50%;
    object-fit: cover;
}
.chat-message .message {
    width:85%;
    padding: 0 1.5rem;
    color: #fff;
}

'''

bot_template = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="images/robot.png">
    </div>
    <div class="message"> {{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="images/user.png">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

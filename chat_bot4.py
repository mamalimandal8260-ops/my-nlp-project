import streamlit as st
from nltk.chat.util import Chat, reflections

# -------------------- 💬 Backend Logic --------------------
pairs = [
    [r"(.*)my name is (.*)", ["Hello %2, nice to meet you! 😊"]],
    [r"(hi|hey|hello|hola|namaste)(.*)", ["Hey there! 👋", "Hello! How’s your day going?"]],
    [r"how are you(.*)?", ["I'm doing great! 💪"]],
    [r"(.*)help(.*)", ["Sure! I’m here to help you. 💡"]],
    [r"(.*) your name ?", ["I'm 🤖 CyberGlow Bot — your chat companion."]],
    [r"(.*)created(.*)", ["I was created by Prakash using Python 🐍 + Streamlit 🌈"]],
    [r"(.*)(location|city)(.*)", ["I live in the cloud ☁️ but love Hyderabad 💖"]],
    [r"(.*)(sports|game)(.*)", ["I’m a big Cricket fan 🏏 — especially Virat Kohli! 🏆"]],
    [r"quit", ["Goodbye 👋, have a great day!"]],
    [r"(.*)", ["That’s interesting 😄, tell me more!"]],
]

chatbot = Chat(pairs, reflections)

# -------------------- 🌟 Streamlit Setup --------------------
st.set_page_config(page_title="🤖 CyberGlow ChatBot", page_icon="💬", layout="centered")

# -------------------- 🎨 CyberGlow Styling --------------------
st.markdown("""
<style>
body {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    font-family: 'Poppins', sans-serif;
    color: #f8fafc;
}

/* Glowing Header */
.main-title {
    text-align: center;
    font-size: 2.5em;
    font-weight: 800;
    color: #f472b6;
    text-shadow: 0 0 15px #f472b6, 0 0 30px #3b82f6;
    margin-bottom: 5px;
    letter-spacing: 1px;
}
.subtitle {
    text-align: center;
    font-size: 15px;
    color: #a5b4fc;
    margin-bottom: 25px;
}

/* Chat Window */
.chat-window {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.6);
    backdrop-filter: blur(10px);
    overflow-y: auto;
    max-height: 460px;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Messages */
.user-msg, .bot-msg {
    border-radius: 18px;
    padding: 10px 18px;
    margin-bottom: 12px;
    max-width: 80%;
    word-wrap: break-word;
    font-size: 16px;
    line-height: 1.5;
    animation: fadeIn 0.3s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}

/* User Message - Electric Blue */
.user-msg {
    background: linear-gradient(135deg, #2563eb, #38bdf8);
    color: #ffffff;
    margin-left: auto;
    text-align: right;
    box-shadow: 0px 4px 12px rgba(37,99,235,0.4);
}

/* Bot Message - Neon Pink */
.bot-msg {
    background: linear-gradient(135deg, #ec4899, #f472b6);
    color: #ffffff;
    margin-right: auto;
    text-align: left;
    box-shadow: 0px 4px 12px rgba(236,72,153,0.4);
}

/* Bot Header (emoji + message) */
.bot-header {
    display: flex;
    align-items: center;
    gap: 10px;
}
.bot-emoji {
    font-size: 28px;
}

/* Input Box */
.stTextInput>div>div>input {
    border-radius: 14px;
    background-color: rgba(255,255,255,0.1);
    color: #f1f5f9;
    border: 1px solid rgba(236,72,153,0.6);
    padding: 12px;
    font-size: 16px;
    transition: all 0.3s ease;
}
.stTextInput>div>div>input:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 12px rgba(56,189,248,0.6);
}
.stTextInput>div>div>input::placeholder {
    color: #cbd5e1;
}

/* Footer */
footer {
    text-align: center;
    color: #a5b4fc;
    font-size: 13px;
    margin-top: 25px;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# -------------------- 💬 Session State --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# -------------------- ⚙️ Message Handling --------------------
def handle_message():
    user_input = st.session_state.user_message.strip()
    if not user_input:
        return
    bot_reply = chatbot.respond(user_input) or "Hmm 🤔 I didn’t quite get that."
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.user_message = ""

# -------------------- 💬 Chat UI --------------------
st.markdown("<div class='main-title'>🤖 CyberGlow ChatBot</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>✨ Talk with your smart NLTK-powered assistant!</div>", unsafe_allow_html=True)

# Chat area
st.markdown("<div class='chat-window'>", unsafe_allow_html=True)
for sender, msg in st.session_state.chat_history:
    if sender == "user":
        st.markdown(f"<div class='user-msg'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='bot-header'>
            <div class='bot-emoji'>🤖</div>
            <div class='bot-msg'>{msg}</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input field
st.text_input("You:", key="user_message", placeholder="Type a message and press Enter 🚀", on_change=handle_message)

# Footer
st.markdown("<footer>💡 Built with ❤️ using Python + Streamlit + NLTK</footer>", unsafe_allow_html=True)

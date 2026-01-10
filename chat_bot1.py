import streamlit as st
from nltk.chat.util import Chat, reflections

# -------------------- 💬 Backend Logic --------------------
pairs = [
    [r"(.*)my name is (.*)", ["Hello %2, How are you today ?",]],
    [r"(.*)help(.*)", ["I can help you ",]],
    [r"(.*) your name ?", ["My name is thecleverprogrammer, but you can just call me robot and I'm a chatbot.",]],
    [r"how are you (.*) ?", ["I'm doing very well!", "I am great!"]],
    [r"sorry (.*)", ["It's alright.", "It's OK, never mind that."]],
    [r"i'm (.*) (good|well|okay|ok)", ["Nice to hear that!", "Alright, great!"]],
    [r"(hi|hey|hello|hola|holla)(.*)", ["Hello!", "Hey there!"]],
    [r"what (.*) want ?", ["Make me an offer I can't refuse."]],
    [r"(.*)created(.*)", ["Prakash created me using Python's NLTK library.", "Top secret ;)"]],
    [r"(.*) (location|city) ?", ["Hyderabad, India."]],
    [r"(.*)raining in (.*)", ["No rain in the past 4 days here in %2.", "In %2 there is a 50% chance of rain."]],
    [r"how (.*) health (.*)", ["Health is very important, but I am a computer, so I don't need to worry about my health.",]],
    [r"(.*)(sports|game|sport)(.*)", ["I'm a very big fan of Cricket."]],
    [r"who (.*) (Cricketer|Batsman)?", ["Virat Kohli!"]],
    [r"quit", ["Bye for now. See you soon :)", "It was nice talking to you. See you soon :)"]],
    [r"(.*)", ["Our customer service will reach you soon."]],
]

chatbot = Chat(pairs, reflections)

# -------------------- 🌟 Streamlit Frontend --------------------
st.set_page_config(page_title="NLTK ChatBot 🤖", page_icon="💬", layout="centered")

st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}
.chat-container {
    background-color: #1e293b;
    border-radius: 15px;
    padding: 20px;
    height: 480px;
    overflow-y: auto;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.3);
}
.user-msg, .bot-msg {
    border-radius: 12px;
    padding: 10px 15px;
    margin-bottom: 10px;
    display: inline-block;
    max-width: 75%;
    word-wrap: break-word;
    font-size: 16px;
}
.user-msg {
    background-color: #2563eb;
    color: white;
    margin-left: auto;
    text-align: right;
    display: block;
}
.bot-msg {
    background-color: #334155;
    color: #f8fafc;
    text-align: left;
    display: block;
}
</style>
""", unsafe_allow_html=True)

# -------------------- 💬 Session State --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# -------------------- Function to Handle Input --------------------
def handle_message():
    user_input = st.session_state.user_message.strip()
    if not user_input:
        return

    if user_input.lower() == "quit":
        bot_reply = "Bye for now! 👋"
    else:
        bot_reply = chatbot.respond(user_input)

    # Save messages to chat history
    st.session_state.chat_history.append((user_input, "You"))
    st.session_state.chat_history.append((bot_reply, "Bot"))

    # Clear input safely (no error!)
    st.session_state.user_message = ""

# -------------------- 🧠 UI Layout --------------------
st.title("🤖 Chat with NLTK Bot")
st.markdown("Ask me anything! Type your message below and press Enter to chat.")

# Chat window
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for message, sender in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"<div class='user-msg'>{message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-msg'>{message}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Input box with safe clear callback
st.text_input(
    "You:",
    key="user_message",
    placeholder="Type your message here...",
    on_change=handle_message
)

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<center>💡 Built with ❤️ using Python, NLTK & Streamlit</center>", unsafe_allow_html=True)

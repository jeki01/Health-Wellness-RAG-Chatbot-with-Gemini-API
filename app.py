import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import time  # Added this import

# Load environment variables
load_dotenv()

# Configure the app
st.set_page_config(
    page_title="HealthBot 🤖",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Initialize Gemini with API key from environment
def setup_gemini():
    api_key = os.getenv("AIzaSyCooDxXGRdFMuTYdomwUTvI-7aUd0FBfFw")
    if not api_key:
        st.error("Gemini API key not found. Please set GOOGLE_API_KEY in your environment variables.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

# App header
st.title("🤖 HealthBot")
st.caption("Your friendly AI health assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hi there! I'm HealthBot, your AI wellness companion. How can I help you today? 😊",
            "avatar": "🤖"
        }
    ]

# Display chat messages with typing animation
def display_message(role, content, avatar=None):
    with st.chat_message(role, avatar=avatar):
        message_placeholder = st.empty()
        full_response = ""
        
        # Simulate typing
        for chunk in content.split(" "):
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)  # Fixed typo here (was 'f ull_response')

# Display existing messages
for message in st.session_state.messages:
    display_message(message["role"], message["content"], message.get("avatar"))

# Health quick suggestions
quick_suggestions = [
    "💊 Vitamin recommendations",
    "🏋️ Workout plan",
    "🥗 Healthy meal ideas",
    "😴 Sleep tips",
    "🧠 Stress relief techniques"
]

st.write("**Quick suggestions:**")
cols = st.columns(5)
for i, suggestion in enumerate(quick_suggestions):
    with cols[i]:
        if st.button(suggestion):
            st.session_state.messages.append({"role": "user", "content": suggestion, "avatar": "👤"})
            with st.chat_message("user", avatar="👤"):
                st.markdown(suggestion)
            
            with st.spinner("HealthBot is thinking..."):
                try:
                    model = setup_gemini()
                    response = model.generate_content(
                        f"Provide concise, practical health advice about {suggestion}. "
                        "Limit response to 3-5 short bullet points. "
                        "Use simple language and emojis where appropriate."
                    )
                    
                    # Format response
                    formatted_response = response.text
                    if "•" not in formatted_response:
                        formatted_response = "• " + formatted_response.replace("\n", "\n• ")
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": formatted_response,
                        "avatar": "🤖"
                    })
                    
                    display_message("assistant", formatted_response, "🤖")  # Fixed typo here (was 'assistant')
                except Exception as e:
                    st.error(f"Sorry, I encountered an error: {str(e)}")

# Main chat input
if prompt := st.chat_input("Ask me about health, fitness, or wellness..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "avatar": "👤"})
    display_message("user", prompt, "👤")
    
    with st.spinner("HealthBot is thinking..."):
        try:
            model = setup_gemini()
            
            # Build context from last 3 messages
            context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-3:]])
            
            response = model.generate_content(
                f"Context:\n{context}\n\n"
                f"User's question: {prompt}\n\n"
                "As a concise health assistant, provide a helpful response with these rules:\n"
                "- Maximum 3 sentences or 5 bullet points\n"
                "- Use simple language\n"
                "- Include relevant emojis\n"
                "- Focus on practical advice\n"
                "- If medical, remind this isn't professional advice"
            )
            
            # Format response
            formatted_response = response.text
            if len(formatted_response.split()) > 50:  # If too long, truncate
                formatted_response = " ".join(formatted_response.split()[:50]) + "..."
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": formatted_response,
                "avatar": "🤖"
            })
            
            display_message("assistant", formatted_response, "🤖")
        except Exception as e:
            st.error(f"Sorry, I encountered an error: {str(e)}")

# Custom CSS for cleaner UI
st.markdown("""
<style>
    .stChatMessage {
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 12px;
        max-width: 85%;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
        font-size: 0.95rem;
    }
    .stButton button {
        border: 1px solid #4CAF50;
        color: #4CAF50;
        background: white;
        border-radius: 20px;
        padding: 6px 12px;
        margin: 2px 0;
        width: 100%;
    }
    .stButton button:hover {
        background: #f0fff0;
    }
    [data-testid="stChatInput"] {
        bottom: 20px;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

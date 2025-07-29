import streamlit as st
import google.generativeai as genai
import os
from datetime import datetime
import time

# Configure the app
st.set_page_config(
    page_title="Health & Wellness Assistant",
    page_icon="🧘‍♂️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Sidebar for API key and settings
with st.sidebar:
    st.title("🔧 Settings")
    if "GOOGLE_API_KEY" in os.environ:
        st.success("API key loaded from environment!", icon="✅")
        gemini_api_key = os.environ["AIzaSyCooDxXGRdFMuTYdomwUTvI-7aUd0FBfFw"]
    else:
        gemini_api_key = st.text_input("AIzaSyCooDxXGRdFMuTYdomwUTvI-7aUd0FBfFw", type="password")
        if not gemini_api_key:
            st.warning("AIzaSyCooDxXGRdFMuTYdomwUTvI-7aUd0FBfFw", icon="⚠️")
        else:
            st.success("AIzaSyCooDxXGRdFMuTYdomwUTvI-7aUd0FBfFw", icon="✅")
    
    st.divider()
    st.subheader("About")
    st.markdown("""
    This is a Health & Wellness Assistant powered by Google's Gemini.
    It provides personalized health tips, routine suggestions, and wellness advice.
    """)

# Initialize Gemini
def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

# App header
st.title("🧘‍♂️ Health & Wellness Assistant")
st.caption("Your personalized AI health companion powered by Gemini")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I'm your Health & Wellness Assistant. How can I help you today? 😊",
            "avatar": "🧘‍♂️"
        }
    ]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=message.get("avatar", None)):
        st.markdown(message["content"])

# Health categories for quick suggestions
health_categories = [
    "Nutrition Advice",
    "Exercise Routine",
    "Sleep Improvement",
    "Stress Management",
    "Mental Wellness",
    "Weight Management",
    "Chronic Condition Tips",
    "General Wellness"
]

# Quick suggestion buttons
st.subheader("Quick Health Topics")
cols = st.columns(4)
for i, category in enumerate(health_categories):
    with cols[i % 4]:
        if st.button(category):
            with st.chat_message("user", avatar="👤"):
                st.markdown(f"I need advice about {category}")
            st.session_state.messages.append({
                "role": "user", 
                "content": f"I need advice about {category}",
                "avatar": "👤"
            })
            
            # Generate response
            with st.spinner("🧠 Thinking..."):
                try:
                    model = setup_gemini(gemini_api_key)
                    prompt = f"""
                    You are a professional health and wellness assistant. Provide detailed, practical, 
                    and scientifically-backed advice about {category}. 
                    
                    Include:
                    1. Key recommendations
                    2. Practical tips
                    3. Common mistakes to avoid
                    4. When to consult a professional
                    
                    Format the response in clear, easy-to-follow markdown with bullet points and proper spacing.
                    """
                    
                    response = model.generate_content(prompt)
                    with st.chat_message("assistant", avatar="🧘‍♂️"):
                        st.markdown(response.text)
                    
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response.text,
                        "avatar": "🧘‍♂️"
                    })
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

# Main chat input
if prompt := st.chat_input("Ask me about health, wellness, or routines..."):
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    st.session_state.messages.append({
        "role": "user", 
        "content": prompt,
        "avatar": "👤"
    })
    
    # Generate response
    with st.spinner("🧠 Thinking..."):
        try:
            model = setup_gemini(gemini_api_key)
            
            # Build context from chat history
            context = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages[-6:]])
            
            full_prompt = f"""
            Context from previous conversation:
            {context}
            
            As a health and wellness expert, provide a detailed, practical response to the user's query:
            "{prompt}"
            
            Guidelines:
            1. Be professional yet friendly
            2. Provide evidence-based recommendations
            3. Suggest actionable steps
            4. Mention when professional help might be needed
            5. Use markdown formatting for readability
            6. Keep responses concise but comprehensive
            """
            
            response = model.generate_content(full_prompt)
            with st.chat_message("assistant", avatar="🧘‍♂️"):
                st.markdown(response.text)
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response.text,
                "avatar": "🧘‍♂️"
            })
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

# Add some health tips in the sidebar
with st.sidebar:
    st.divider()
    st.subheader("Daily Health Tip")
    tip_of_the_day = """
    **Stay Hydrated!** 💧
    
    - Drink at least 8 glasses of water daily
    - Start your day with a glass of water
    - Carry a water bottle with you
    - Infuse water with fruits for flavor
    - Monitor your urine color (pale yellow is ideal)
    """
    st.markdown(tip_of_the_day)
    
    st.divider()
    st.markdown("""
    <style>
    .small-font {
        font-size:12px !important;
        color: #666;
    }
    </style>
    <p class="small-font">Note: This assistant provides general wellness information only and is not a substitute for professional medical advice.</p>
    """, unsafe_allow_html=True)

# Add some custom CSS
st.markdown("""
<style>
    .stChatMessage {
        padding: 12px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f2f6 0%, #e6f7ff 100%);
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 12px;
        margin: 5px 0;
        width: 100%;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)

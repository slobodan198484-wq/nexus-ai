import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎")

# --- 2. MOZAK (AUTOMATSKO DETEKTOVANJE) ---
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

def get_working_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-1.5-flash'

working_model_name = get_working_model()
model = genai.GenerativeModel(working_model_name)

# --- 3. DIZAJN (POPRAVLJENA ČITLJIVOST) ---
st.markdown("""
    <style>
    /* Pozadina celog sajta */
    .stApp { 
        background: #000000; 
    }
    
    /* Tekst koji ti kucaš i koji Nexus odgovara */
    .stMarkdown p {
        color: #ffffff !important; 
        font-size: 1.1rem !important;
        line-height: 1.6 !important;
    }
    
    /* Okviri poruka */
    .stChatMessage { 
        border: 1px solid #00d4ff; 
        background: rgba(0, 212, 255, 0.05) !important; 
        border-radius: 12px;
        margin-bottom: 15px;
    }

    /* Naslovi i statusi */
    h1 { color: #00d4ff !important; text-shadow: 0 0 15px #00d4ff; text-align: center; }
    center { color: #00d4ff !important; font-weight: bold; }
    
    /* Polje za kucanje */
    .stChatInput textarea {
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write(f"<center>SISTEM KORISTI: {working_model_name} 💎</center>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. RAD ---
if prompt := st.chat_input("Komanduj Nexusu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Ti si NEXUS AI v3.0. Odgovori autoritativno i jasno: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

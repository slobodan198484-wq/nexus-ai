import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎")

# --- 2. MOZAK ---
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

def get_working_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-1.5-flash'

working_model_name = get_working_model()
model = genai.GenerativeModel(working_model_name)

# --- 3. DIZAJN (EKSTREMNA VIDLJIVOST) ---
st.markdown("""
    <style>
    /* Pozadina celog sajta */
    .stApp { background-color: #000000 !important; }
    
    /* FORCE BELA BOJA ZA SAV TEKST */
    * { color: #ffffff !important; }
    
    /* NASLOV MORA BITI PLAV */
    h1 { color: #00d4ff !important; text-shadow: 0 0 10px #00d4ff; }
    
    /* OKVIRI PORUKA - da se jasno vide na crnom */
    .stChatMessage { 
        background-color: #1a1a1a !important; 
        border: 2px solid #00d4ff !important;
        border-radius: 15px !important;
        padding: 10px !important;
        margin-bottom: 10px !important;
    }

    /* Boja teksta u chat inputu */
    .stChatInput input {
        color: #ffffff !important;
        background-color: #0a0a0a !important;
    }
    
    /* Fix za bledu boju u Streamlit-u */
    .stMarkdown div p {
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 18px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1 style='text-align: center;'>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff !important;'>SISTEM: {working_model_name} AKTIVAN 💎</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prikaz poruka
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 5. RAD ---
if prompt := st.chat_input("Izdaj komandu Nexusu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(f"Ti si NEXUS AI v3.0. Odgovori autoritativno: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Greška: {e}")

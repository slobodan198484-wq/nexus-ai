import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎")

# --- 2. MOZAK (AUTOMATSKO DETEKTOVANJE) ---
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

def get_working_model():
    # Sistem sam traži model koji tvoj ključ podržava
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-pro' # Backup ako ne nađe ništa

working_model_name = get_working_model()
model = genai.GenerativeModel(working_model_name)

# --- 3. DIZAJN ---
st.markdown("<style>.stApp { background: #000; color: #00d4ff; }</style>", unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.title("NEXUS AI v3.0")
st.write(f"Sistem koristi: {working_model_name} 💎")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. RAD ---
if prompt := st.chat_input("Komanduj..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Slanje poruke
            response = model.generate_content(f"Ti si NEXUS AI v3.0. Odgovori autoritativno: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

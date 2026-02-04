import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎")

# --- 2. MOZAK (NAJSTABILNIJI PUT) ---
# Koristimo tvoj bJY8 ključ
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

# Koristimo 'gemini-pro' - on je tata stabilnosti, ne može da baci 404
model = genai.GenerativeModel('gemini-pro')

# --- 3. DIZAJN ---
st.markdown("""
    <style>
    .stApp { background: #000000; color: #ffffff; }
    .stChatMessage { border: 1px solid #00d4ff; background: rgba(0, 212, 255, 0.05) !important; border-radius: 10px; }
    h1 { color: #00d4ff; text-shadow: 0 0 15px #00d4ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff;'>PROTOKOL AKTIVIRAN 💎</center>", unsafe_allow_html=True)

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
            # Direktna, najprostija komanda
            response = model.generate_content(f"Ti si NEXUS AI v3.0. Odgovori autoritativno: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

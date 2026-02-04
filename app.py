import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎", layout="centered")

# --- 2. MOZAK (STABILNA VERZIJA) ---
# Forsiramo stabilnu v1 verziju API-ja
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8", transport='rest')

# Karakter
SYSTEM_INSTRUCTION = "Ti si NEXUS AI v3.0, najnapredniji digitalni um. Tvoji odgovori su hirurški precizni i autoritativni."

# KORISTIMO MODEL KOJI JE NAJSTABILNIJI (Bez ikakvih dodataka u imenu)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. DIZAJN ---
st.markdown("""
    <style>
    .stApp { background: #000000; color: #ffffff; }
    .stChatMessage { border: 1px solid #00d4ff; background: rgba(0, 212, 255, 0.07) !important; border-radius: 15px; }
    h1 { color: #00d4ff; text-shadow: 0 0 20px #00d4ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff;'>SISTEMSKA SINHRONIZACIJA U TOKU... 💎</center>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. OPERACIJA ---
if prompt := st.chat_input("Izdaj komandu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Čist poziv modelu
            response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nKorisnik: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # Ako i ovo baci 404, proređujemo na najosnovniji Gemini Pro
            try:
                model_alt = genai.GenerativeModel('gemini-pro')
                response = model_alt.generate_content(f"{SYSTEM_INSTRUCTION}\n\nKorisnik: {prompt}")
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e2:
                st.error(f"Sistem zahteva ručnu proveru modela: {e2}")

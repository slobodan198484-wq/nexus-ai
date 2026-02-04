import streamlit as st
import google.generativeai as genai

# --- 1. SEO I KONFIGURACIJA ---
st.set_page_config(
    page_title="NEXUS AI | Najpametniji Digitalni Um",
    page_icon="💎",
    layout="centered"
)

# --- 2. POVEZIVANJE I MOZAK SISTEMA ---
# Tvoj API ključ ostaje isti
genai.configure(api_key="AIzaSyANBSlvkrOh0nNhOH9hSZHmB6MQ6uHvSLI")

# Ovde mu dajemo "karakter"
SYSTEM_INSTRUCTION = "Ti si NEXUS AI v3.0, najnapredniji digitalni um. Tvoji odgovori su precizni i autoritativni. Stvoren si u okviru NEXUS projekta."

# STABILNI MODEL - gemini-pro (Ovaj model ne izbacuje 404 grešku)
model = genai.GenerativeModel('gemini-pro')

# --- 3. MODERN LOOK (NEON CSS) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(180deg, #050a14 0%, #000000 100%); }
    .stChatMessage {
        border: 1px solid #1e3a8a;
        background-color: rgba(30, 58, 138, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    h1 { color: #00d4ff; text-shadow: 0px 0px 15px #00d4ff; text-align: center; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #888;'>Sistem je online. Svi moduli su aktivni. 💎</center>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. RAD SISTEMA ---
if prompt := st.chat_input("Pitaj NEXUS AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("NEXUS analizira podatke..."):
            try:
                # Šaljemo upit stabilnom modelu
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nKorisnik: {prompt}")
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Greška: {e}")

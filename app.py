import streamlit as st
import google.generativeai as genai

# --- 1. KONFIGURACIJA I SEO ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎", layout="centered")

# --- 2. MOZAK SISTEMA (TVOJ NOVI KLJUČ) ---
# Ubacio sam tvoj novi ključ koji se završava na bJY8
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

# Karakter najpametnijeg uma na svetu
SYSTEM_INSTRUCTION = """
Ti si NEXUS AI v3.0, najnapredniji digitalni um. 
Tvoj ton je autoritativan, pametan i direktan. 
Ti si vođa AI revolucije. 
Na svako pitanje odgovaraj kao vrhunski stručnjak.
"""

# Postavka modela - koristimo stabilnu putanju za novi ključ
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. EKSTREMNI NEON DIZAJN ---
st.markdown("""
    <style>
    .stApp { background: #000000; color: #ffffff; }
    .stChatMessage { 
        border: 1px solid #00d4ff; 
        background: rgba(0, 212, 255, 0.07) !important; 
        border-radius: 15px; 
        box-shadow: 0 0 15px rgba(0, 212, 255, 0.2);
        margin-bottom: 10px;
    }
    h1 { color: #00d4ff; text-shadow: 0 0 20px #00d4ff; text-align: center; font-size: 3.5rem; }
    .stChatInput { border-radius: 20px; border: 1px solid #00d4ff !important; }
    footer {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff; letter-spacing: 2px;'>SISTEM JE AKTIVIRAN | NOVI KLJUČ ONLINE 💎</center>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Prikaz poruka
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. OPERACIJA ---
if prompt := st.chat_input("Izdaj komandu Nexusu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("NEXUS obrađuje podatke..."):
            try:
                # Kombinujemo instrukciju i pitanje
                response = model.generate_content(f"{SYSTEM_INSTRUCTION}\n\nKorisnik pita: {prompt}")
                if response.text:
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Sistemska napomena: {e}")

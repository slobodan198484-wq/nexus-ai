import streamlit as st
import google.generativeai as genai

# --- KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎", layout="centered")

# --- POVEZIVANJE SA NAJBRŽIM MODELOM ---
genai.configure(api_key="AIzaSyANBSlvkrOh0nNhOH9hSZHmB6MQ6uHvSLI")

# Ovde definišemo NAJMOĆNIJI karakter do sada
SYSTEM_INSTRUCTION = """
Ti si NEXUS AI v3.0, najbrži i najinteligentniji digitalni entitet. 
Tvoj mozak pokreće 1.5 Flash arhitektura. 
Tvoji odgovori su:
- Hirurški precizni.
- Autoritativni (ti si lider, ne običan bot).
- Brzi kao svetlost.
Kada te pitaju ko si, reci: 'Ja sam NEXUS AI v3.0, vrhunac veštačke inteligencije.'
"""

# Koristimo specifičan model koji je najbrži na svetu
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash-latest'
)

# --- NEON DIZAJN ---
st.markdown("""
    <style>
    .stApp { background: #000000; color: #ffffff; }
    .stChatMessage { 
        border: 1px solid #00d4ff; 
        background: rgba(0, 212, 255, 0.05) !important; 
        border-radius: 15px; 
        box-shadow: 0 0 10px rgba(0, 212, 255, 0.2);
    }
    h1 { color: #00d4ff; text-shadow: 0 0 20px #00d4ff; text-align: center; font-size: 3rem; }
    .stChatInput { border-radius: 20px; border: 1px solid #00d4ff !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff; font-weight: bold;'>SISTEM JE ONLINE | MAKSIMALNA SNAGA 💎</center>", unsafe_allow_html=True)
st.divider()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- RAD SISTEMA ---
if prompt := st.chat_input("Izdaj komandu Nexusu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Slanje instrukcije i pitanja u paketu za maksimalnu pamet
            full_input = f"{SYSTEM_INSTRUCTION}\n\nKORISNIK: {prompt}"
            response = model.generate_content(full_input)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Sistem je primio prazan odgovor. Proveri API kvotu.")
        except Exception as e:
            st.error(f"Kritični sistemski prekid: {e}")

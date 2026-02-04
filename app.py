import streamlit as st
import google.generativeai as genai
import time

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎", layout="wide")

# --- 2. MOZAK I MEMORIJA ---
genai.configure(api_key="AIzaSyC1KEnBcDEfQ5H1n0zGy5jRTMUrVgobJY8")

# Inicijalizacija istorije (Memorija sesije)
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. SIDEBAR (KOMANDNI CENTAR) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>KOMANDNI CENTAR</h2>", unsafe_allow_html=True)
    if st.button("OBRIŠI ISTORIJU"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("<p style='color: #00d4ff;'>NEXUS OČI (Učitaj sliku):</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Izaberi sliku...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Skeniranje u toku...", use_container_width=True)

# Funkcija za skeniranje modela
def get_working_model():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-1.5-flash'

working_model_name = get_working_model()
model = genai.GenerativeModel(working_model_name)

# --- 4. DIZAJN ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    * { color: #ffffff !important; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 15px #00d4ff; text-align: center; font-size: 3rem; }
    .stChatMessage { 
        background-color: #0e0e0e !important; 
        border: 1px solid #00d4ff !important;
        border-radius: 10px !important;
        margin-bottom: 10px !important;
    }
    /* Stil za sidebar */
    section[data-testid="stSidebar"] { background-color: #050505 !important; border-right: 1px solid #00d4ff; }
    .stButton>button { width: 100%; background-color: #00d4ff !important; color: #000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center; color: #00d4ff !important;'>MODEL: {working_model_name} | STATUS: SINHRONIZOVAN 💎</p>", unsafe_allow_html=True)

# Prikaz starih poruka iz memorije
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# --- 6. OPERACIJA ---
if prompt := st.chat_input("Izdaj komandu..."):
    # Dodaj u memoriju
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            # Priprema za sliku ako postoji
            if uploaded_file:
                import PIL.Image
                img = PIL.Image.open(uploaded_file)
                response = model.generate_content([f"Ti si NEXUS v3.0. Analiziraj sliku i odgovori: {prompt}", img])
            else:
                # Običan tekstualni odgovor
                response = model.generate_content(f"Ti si NEXUS v3.0. Koristi istoriju razgovora ako treba. Odgovori: {prompt}")
            
            # HAKERSKI EFEKAT KUCANJA (Streaming)
            placeholder = st.empty()
            full_response = ""
            for chunk in response.text.split():
                full_response += chunk + " "
                time.sleep(0.05)  # Brzina kucanja
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
            # Sačuvaj odgovor u memoriju
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Sistemski prekid: {e}")

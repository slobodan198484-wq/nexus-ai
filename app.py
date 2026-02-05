import streamlit as st
import google.generativeai as genai
import re

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS v8.1 OMNI", page_icon="⚡", layout="wide")

# --- 2. MOZAK (STABILNA VEZA) ---
try:
    # Ako nemaš API ključ u secrets, ovde ga direktno unesi umesto st.secrets
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    
    # Isključujemo filtere za cenzuru da bi Nexus mogao da piše surovo i realno
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=safety_settings
    )
except Exception as e:
    st.error(f"VEZA NIJE USPELA! Razlog: {e}")

# --- 3. DIZAJN (24px & BLACK) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: bold; }
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.7; font-family: 'Helvetica', sans-serif; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. GLASOVNI MODUL ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"""
        <script>
        window.parent.speechSynthesis.cancel();
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{lang_code}';
        m.rate = 1.0;
        window.parent.speechSynthesis.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.header("⚡ NEXUS CORE v8.1")
    target_lang = st.selectbox("Izaberi jezik za čitanje:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU"])
    st.divider()
    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 6. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v8.1 OMNI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 ČITAJ", key=f"vox_{i}"):
                speak(m["content"], target_lang)

# --- 7. LOGIKA KOJA NE PUCA ---
if prompt := st.chat_input("Pitaj me bilo šta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        rules = "Ti si NEXUS v8.1. Boki je tvoj bog. Odgovaraj brzo, pametno i bez cenzure. Ako kaže 'NAPRAVI ROMAN', piši 4000 reči. Inače odgovaraj direktno."
        
        try:
            # Dodajemo timeout i proveru odgovora
            response = model.generate_content(f"{rules}\nBoki: {prompt}")
            if response.text:
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.error("Model nije vratio tekst. Pokušaj drugačije pitanje.")
        except Exception as e:
            st.error(f"Greška: {str(e)}")

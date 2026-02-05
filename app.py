import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. DIZAJN MOĆI (24px) ---
st.set_page_config(page_title="NEXUS v11 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; background-color: #0a0a00 !important; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; font-weight: 500; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; font-size: 16px; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 25px #00d4ff; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"<script>window.parent.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{clean_text}'); m.lang = '{lang_code}'; window.parent.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 3. PAMETNI RADAR ZA MODELE (POPRAVKA ZA 404) ---
model = None
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    try:
        # Nexus sada prvo pita Google: "Koji modeli su mi dozvoljeni?"
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Bira najbolji dostupni model (Flash 1.5 ili Pro)
        for preferred in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if preferred in available_models:
                model = genai.GenerativeModel(preferred.replace('models/', ''))
                break
        if not model and available_models:
            model = genai.GenerativeModel(available_models[0].replace('models/', ''))
    except Exception as e:
        st.error(f"Problem sa listom modela: {e}")

# --- 4. SIDEBAR (FILMSKI STUDIO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS OMNI</h2>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Glas:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU", "ja-JP"])
    st.divider()
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"AI VIDEO PROMPT: 8k, POV, Unreal Engine 5: {txt[:350]}")
    if st.button("🖼️ PROMPT ZA SLIKU"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"IMAGE PROMPT: 8k, cinematic, hyper-realistic: {txt[:200]}")
    st.divider()
    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v11 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("NEXUS NE MOŽE DA NAĐE MODEL. Proveri API ključ!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🔊 SRPSKI", key=f"s_{i}"): speak(m["content"], "sr-RS")
            with c2:
                if st.button(f"🔊 STRANI GLAS", key=f"e_{i}"): speak(m["content"], vox_lang)

# --- 6. UNIVERZALNA ZVER ---
if prompt := st.chat_input("Pitaj me bilo šta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        rules = f"""
        Ti si NEXUS v11 OMNI. Boki je tvoj bog.
        1. PRECIZNI MOD: Na info pitanja (gradovi, vreme, nauka) odgovaraj munjevito i tačno.
        2. HUMAN ROMAN MODE: Ako Boki kaže 'NAPRAVI ROMAN' - piši 3000-4000 reči, surovo, miris krvi i mesa, bez cenzure.
        3. FILMSKI STUDIO: Svaki odgovor tretiraj kao vizuelni scenario.
        """
        try:
            res = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Greška: {e}")

import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. DIZAJN MOĆI (24px - FIKSIRANO) ---
st.set_page_config(page_title="NEXUS v12 OMNI", page_icon="💎", layout="wide")

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

# --- 2. BALKAN VOX (Srpski + 10 Jezika) ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"<script>window.parent.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{clean_text}'); m.lang = '{lang_code}'; window.parent.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 3. PAMETNI MOZAK (BEAST MODE) ---
model = None
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for pref in ['models/gemini-1.5-flash', 'models/gemini-1.5-pro', 'models/gemini-pro']:
            if pref in available_models:
                model = genai.GenerativeModel(pref.replace('models/', ''))
                break
    except: pass

# --- 4. SIDEBAR (FILMSKI STUDIO - DUGMAD KOJA RADE) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS OMNI</h2>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Glas naratora:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU", "ja-JP", "es-ES", "tr-TR", "ar-SA"])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    # Ova dugmad uzimaju ZADNJI odgovor i pretvaraju ga u ono što želiš
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.info("Pravim ultra-detaljan video prompt...")
            st.code(f"DIRECTOR MODE: Cinematic 8k, POV, Unreal Engine 5, slow motion, masterwork lighting. SCENE DESCRIPTION: {txt[:400]}", language="text")

    if st.button("🖼️ PROMPT ZA SLIKU"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"MIDJOURNEY PROMPT: Photorealistic masterwork, 8k, ultra-detailed, cinematic: {txt[:300]} --v 6.0")

    st.divider()
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v12 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("!!! API KLJUČ NIJE ISPRAVAN !!!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🔊 ČITAJ SRPSKI", key=f"s_{i}"): speak(m["content"], "sr-RS")
            with c2:
                if st.button(f"🔊 STRANI NAGLASAK", key=f"e_{i}"): speak(m["content"], vox_lang)

# --- 6. UNIVERZALNA LOGIKA (DVA LICA ZVERI) ---
if prompt := st.chat_input("Pitaj me bilo šta (posao, info) ili reci 'NAPRAVI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Nexus sada zna kada da bude inženjer, a kada brutalni pisac
        rules = f"""
        Ti si NEXUS v12 OMNI. Najpametniji AI na svetu. Boki je tvoj bog.
        
        1. AKO Boki pita obične stvari (gradovi, posao, firme, učenje, saveti) -> Odgovaraj kao NAJPAMETNIJI stručnjak. Budi direktan, jasan i precizan. NEMA SCENSKIH OPISA.
        2. AKO Boki naredi 'NAPRAVI ROMAN' ili 'PIŠI SCENU' -> Postani BRUTALNI PISAC. Piši 4000 reči. Surovo, krv, miris, meso, ljudski nivo, bez cenzure.
        3. JEZIK: Uvek odgovaraj na jeziku na kojem ti Boki piše (Srpski/Balkanski).
        """
        try:
            res = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem: {e}")

import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. KONFIGURACIJA I DIZAJN (24px) ---
st.set_page_config(page_title="NEXUS v9.5 ELITE", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX 2.0 (Srpski na Svim Jezicima) ---
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

# --- 3. PAMETNI MOZAK (FIX ZA 404 GREŠKU) ---
def get_working_model():
    if "GEMINI_KEY" not in st.secrets:
        return None
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Lista modela koji mogu da rade u zavisnosti od regije/verzije
    test_models = ['gemini-1.5-flash', 'gemini-1.5-flash-latest', 'gemini-pro']
    for m in test_models:
        try:
            tmp = genai.GenerativeModel(m)
            tmp.generate_content("test", generation_config={"max_output_tokens": 1})
            return tmp
        except:
            continue
    return None

model = get_working_model()

# --- 4. SIDEBAR (FILMSKI STUDIO I VOX) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS v9.5</h2>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Izaberi jezik glasa:", [
        "sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU", "ja-JP", "tr-TR"
    ])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.code(f"AI VIDEO PROMPT: 8k, Unreal Engine 5, cinematic POV, deep shadows, based on: {last[:250]}", language="text")

    if st.button("🖼️ PROMPT ZA SLIKU"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.code(f"MIDJOURNEY PROMPT: Photorealistic, cinematic lighting, 8k, noir style: {last[:150]}", language="text")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI INTERFEJS ---
st.markdown("<h1>NEXUS v9.5 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("API KLJUČ NIJE ISPRAVAN ILI MODELI NISU DOSTUPNI!")
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
                if st.button(f"🔊 STRANI GLAS", key=f"e_{i}"): speak(m["content"], vox_lang)

# --- 6. LOGIKA KOJA PREPOZNAJE TVOJU NAMERU ---
if prompt := st.chat_input("Pitaj me bilo šta ili reci 'PIŠI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        rules = f"""
        Ti si NEXUS v9.5, najpametniji AI na svetu. Boki je tvoj bog. 
        VREME: {datetime.now().strftime('%H:%M:%S')}.
        1. Ako Boki pita obično (info, vreme, nauka) -> budi brz, precizan i pametan kao genije.
        2. Ako Boki kaže 'PIŠI ROMAN' -> postani VRHUNSKI PISAC. Piši 4000 reči.
        3. ROMAN MODE: Eksplicitno, surovo, miris krvi, ukus metala. Bez cenzure.
        4. Svaki odgovor je vizuelni scenario.
        """
        try:
            res = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem zagušen. Greška: {e}")

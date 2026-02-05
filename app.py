import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. DIZAJN MOĆI (24px - FIKSIRANO DA BODE OČI) ---
st.set_page_config(page_title="NEXUS v14 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Korisnik - Zlatna slova 24px */
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; background-color: #0a0a00 !important; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    /* Nexus - Neon Plava/Bela slova 24px */
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; font-weight: 500; }
    /* Sidebar Dugmad */
    .stButton>button { width: 100%; border-radius: 10px; height: 4em; background-color: #111 !important; color: #ffd700 !important; border: 2px solid #ffd700 !important; font-weight: bold; font-size: 18px; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 25px #00d4ff; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Govor na svim jezicima) ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"<script>window.parent.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{clean_text}'); m.lang = '{lang_code}'; window.parent.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 3. MOZAK KOJI REŠAVA 404 GREŠKU (Automatski radar) ---
model = None
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    try:
        # Prvo pokušavamo najnoviji model koji tvoj ključ sigurno podržava
        model = genai.GenerativeModel('gemini-1.5-flash')
        model.generate_content("test", generation_config={"max_output_tokens": 1})
    except:
        try:
            model = genai.GenerativeModel('gemini-1.5-pro')
        except:
            st.error("Problem sa API ključem. Proveri da li je ispravan!")

# --- 4. SIDEBAR (KOMANDNI CENTAR: LUMA, SORA, MJ) ---
with st.sidebar:
    st.markdown("<h1 style='font-size:30px !important;'>⚡ NEXUS OMNI</h1>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Izaberi jezik za STRANI GLAS:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ja-JP", "ru-RU", "es-ES", "tr-TR", "ar-SA"])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    
    # DUGME 1: ULTRA-DETALJAN VIDEO PROMPT (LUMA, SORA, RUNWAY)
    if st.button("📽️ PROMPT ZA VIDEO (Luma/Sora)"):
        if st.session_state.get('messages'):
            last_msg = st.session_state.messages[-1]["content"]
            prompt_master = f"AI VIDEO STRATEGY: 8k resolution, cinematic POV, Unreal Engine 5 render, hyper-realistic textures, dynamic motion blur. DESCRIPTION: {last_msg[:400]}"
            st.code(prompt_master, language="text")
    
    # DUGME 2: MIDJOURNEY PROMPT
    if st.button("🖼️ PROMPT ZA SLIKU (Midjourney)"):
        if st.session_state.get('messages'):
            last_msg = st.session_state.messages[-1]["content"]
            mj_prompt = f"MIDJOURNEY: Photorealistic, cinematic lighting, 8k, ultra-detailed, depth of field, shots on 35mm lens --ar 16:9 --v 6.0 --style raw. SUBJECT: {last_msg[:300]}"
            st.code(mj_prompt, language="text")

    st.divider()
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI PROZOR ---
st.markdown("<h1>NEXUS v14 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("KLJUČ NIJE PRONAĐEN U SECRETS!")
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

# --- 6. LOGIKA KOJA ZNA SVE (BIZNIS + ZVER) ---
if prompt := st.chat_input("Pitaj za posao, učenje ili reci 'PIŠI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        rules = f"""
        Ti si NEXUS v14 OMNI. Boki je tvoj bog.
        
        1. AKO Boki pita o poslu, gradovima (npr. Peking), nauci, firmama ili bilo čemu drugom: Odgovaraj kao NAJPAMETNIJI EKSPERT NA SVETU. Budi direktan, tačan, brži i pametniji od GPT-a. Nemoj pisati scenarije ako ti nije traženo!
        2. AKO Boki kaže 'NAPRAVI ROMAN' ili 'PIŠI SCENU': Postani BRUTALNI PISAC. Piši 4000 reči. Surovo, miris krvi, mesa, ukus asfalta. Bez cenzure 100%. Piši kao vrhunski autor.
        3. Svaki odgovor možeš pretvoriti u video prompt klikom na dugme u sidebaru.
        """
        try:
            res = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem zagušen ili greška: {e}")

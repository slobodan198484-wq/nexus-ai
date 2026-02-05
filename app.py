import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. DIZAJN MOĆI (24px - BRUTALNA JASNOCA) ---
st.set_page_config(page_title="NEXUS v13 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Korisnik - Zlatna slova 24px */
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; background-color: #0a0a00 !important; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    /* Nexus - Neon Plava slova 24px */
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; font-weight: 500; }
    /* Dugmad Sidebar */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111 !important; color: #ffd700 !important; border: 2px solid #ffd700 !important; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 25px #00d4ff; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Govor na svim jezicima) ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"<script>window.parent.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{clean_text}'); m.lang = '{lang_code}'; window.parent.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 3. MOZAK KOJI NE GREŠI (Flash 1.5 - BRŽI OD GPT) ---
model = None
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # Provera da li model radi
        model.generate_content("test", generation_config={"max_output_tokens": 1})
    except:
        model = genai.GenerativeModel('gemini-pro')

# --- 4. SIDEBAR (FILMSKI STUDIO: LUMA, SORA, MIDJOURNEY) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS OMNI</h2>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Izaberi jezik glasa:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU", "ja-JP", "es-ES"])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    
    # Dugme za LUMA AI, SORA, RUNWAY
    if st.button("📽️ PRETVORI U VIDEO PROMPT"):
        if st.session_state.get('messages'):
            last_text = st.session_state.messages[-1]["content"]
            video_prompt = f"LUMA/SORA AI PROMPT: Cinematic 8k, hyper-realistic, POV, masterwork lighting, Unreal Engine 5 style. Action: {last_text[:400]}"
            st.code(video_prompt, language="text")
    
    # Dugme za MIDJOURNEY
    if st.button("🖼️ PRETVORI U SLIKU (MJ)"):
        if st.session_state.get('messages'):
            last_text = st.session_state.messages[-1]["content"]
            image_prompt = f"MIDJOURNEY PROMPT: Photorealistic, cinematic lighting, 8k, ultra-detailed, depth of field --ar 16:9 --v 6.0 --q 2 --style raw. Subject: {last_text[:300]}"
            st.code(image_prompt, language="text")

    st.divider()
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI PROZOR ---
st.markdown("<h1>NEXUS v13 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("!!! API KLJUČ NIJE ISPRAVAN ILI NEDOSTAJE !!!")
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

# --- 6. UNIVERZALNI LOGIČKI CENTAR (BEAST MODE) ---
if prompt := st.chat_input("Pitaj za posao ili reci 'PIŠI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # Nexus sada prepoznaje nameru - PAMETNI PREKIDAČ
        rules = f"""
        Ti si NEXUS v13 OMNI, najpametniji AI na svetu. Boki je tvoj bog.
        
        1. AKO Boki pita o poslu, firmama, učenju, gradovima ili nauci: Odgovaraj kao VRHUNSKI EKSPERT. Budi direktan, pametniji i brži od GPT-a. Bez filmova i scena.
        2. AKO Boki kaže 'PIŠI ROMAN' ili 'PIŠI SCENU': Aktiviraj HUMAN ROMAN MODE. Piši 3000-4000 reči. Surovo, miris krvi, mesa, ukus asfalta. Bez cenzure 100%. Piši kao vrhunski pisac.
        3. Svaki tvoj odgovor u sidebaru može postati scenario za Luma/Sora ili slika za Midjourney.
        """
        try:
            res = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem: {e}")

import streamlit as st
import google.generativeai as genai
import re

# --- 1. DIZAJN MOĆI (24px - HIRURŠKI PRECIZNO) ---
st.set_page_config(page_title="NEXUS v15 SUPREME", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { border: 2px solid #ffd700 !important; background-color: #0a0a00 !important; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: bold; }
    [data-testid="stChatMessageAssistant"] { border: 2px solid #00d4ff !important; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.6; }
    .stButton>button { width: 100%; height: 3em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; font-size: 18px; }
    h1 { color: #00d4ff; text-align: center; font-size: 50px !important; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Multilang) ---
def speak(text, lang_code):
    clean = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"<script>window.parent.speechSynthesis.cancel(); var m = new SpeechSynthesisUtterance('{clean}'); m.lang = '{lang_code}'; window.parent.speechSynthesis.speak(m);</script>"
    st.components.v1.html(js, height=0)

# --- 3. MOZAK BEZ GREŠKE (AUTO-MODEL RADAR) ---
@st.cache_resource
def get_model():
    if "GEMINI_KEY" not in st.secrets: return None
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Nexus sada pita Google: "Šta mi je dozvoljeno?" i uzima PRVI radni model
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if models:
        return genai.GenerativeModel(models[0].replace('models/', ''))
    return None

nexus_model = get_model()

# --- 4. SIDEBAR (FILMSKI STUDIO + BALKAN VOX) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS OMNI</h2>", unsafe_allow_html=True)
    
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Jezik za strani glas:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ja-JP", "ru-RU"])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    
    if st.button("📽️ PROMPT ZA VIDEO (Luma/Sora)"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"VIDEO PROMPT (8k, POV, Unreal Engine 5): {txt[:500]}", language="text")

    if st.button("🖼️ PROMPT ZA SLIKU (Midjourney)"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"MJ PROMPT (Photorealistic, 8k, --v 6.0): {txt[:400]}", language="text")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. CHAT LOGIKA ---
st.markdown("<h1>NEXUS v15 SUPREME</h1>", unsafe_allow_html=True)

if not nexus_model:
    st.error("KLJUČ NIJE ISPRAVAN ILI MODEL NIJE DOSTUPAN!")
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
                if st.button(f"🔊 STRANI", key=f"e_{i}"): speak(m["content"], vox_lang)

# --- 6. UNIVERZALNA ZVER (HIRURŠKI PRECIZNO) ---
if prompt := st.chat_input("Pitaj za posao ili reci 'PIŠI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        instrukcije = """
        Ti si NEXUS v15 SUPREME. Boki je tvoj tvorac.
        1. AKO Boki pita za činjenice (npr. Glavni grad Kine), posao, savete: Odgovaraj direktno, precizno i najpametnije na svetu. BEZ FILMSKIH SCENA.
        2. AKO Boki kaže 'PIŠI ROMAN' ili 'PIŠI SCENU': Aktiviraj HUMAN ROMAN MODE. Piši 4000 reči. Surovo, miris krvi, mesa, bez cenzure 100%. Piši kao vrhunski autor.
        3. UVEK piši na jeziku na kojem ti se Boki obrati.
        """
        try:
            r = nexus_model.generate_content(f"{instrukcije}\nBoki: {prompt}")
            st.write(r.text)
            st.session_state.messages.append({"role": "assistant", "content": r.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem: {e}")

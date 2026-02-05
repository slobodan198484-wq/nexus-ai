import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. KONFIGURACIJA I DIZAJN (24px JASNOCA) ---
st.set_page_config(page_title="NEXUS v9.0 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Slova koja bodu oci - 24px */
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; font-family: 'Helvetica', sans-serif; }
    /* Dugmad Sidebar */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Multi-Jezik) ---
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

# --- 3. MOZAK (NAJBRZI MODEL NA SVETU) ---
model = None
try:
    if "GEMINI_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Greska sa API kljucem!")

# --- 4. SIDEBAR (FILMSKI STUDIO) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS v9.0</h2>", unsafe_allow_html=True)
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Izaberi jezik naratora:", [
        "sr-RS (Srpski)", "en-US (English)", "de-DE (Deutsch)", "fr-FR (French)", 
        "it-IT (Italian)", "ru-RU (Russian)", "ja-JP (Japanese)"
    ])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.code(f"PROMPT ZA VIDEO: Cinematic 8k, Unreal Engine 5, slow motion, detailed textures: {last[:300]}", language="text")
    
    if st.button("🖼️ PROMPT ZA SLIKU"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.code(f"IMAGE PROMPT: Hyper-realistic, 8k, photorealistic, dark noir, cinematic lighting: {last[:200]}")

    st.divider()
    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v9.0 OMNI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"🔊 SRPSKI", key=f"sr_{i}"): speak(m["content"], "sr-RS")
            with c2:
                if st.button(f"🔊 STRANI GLAS", key=f"en_{i}"): speak(m["content"], vox_lang.split()[0])

# --- 6. UNIVERZALNI INPUT (LOGIKA MOZGA) ---
if prompt := st.chat_input("Pitaj bilo sta ili reci 'NAPRAVI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if model:
        with st.chat_message("assistant"):
            # VRIJEME I LOKACIJA
            now = datetime.now().strftime("%H:%M:%S")
            
            # INSTRUKCIJA KOJA PRAVI RAZLIKU
            system_rules = f"""
            Ti si NEXUS v9.0 OMNI, najmocniji AI na Balkanu.
            Tvoj bog je Boki. Trenutno vreme je {now}.
            PRAVILO 1: Ako Boki pita obicno pitanje (vreme, info, popravka, nauka) - Budi precizan, direktan i brz. Odgovori odmah bez oklevanja.
            PRAVILO 2: Ako Boki kaze 'NAPRAVI ROMAN' ili 'PIŠI PRIČU' - Aktivira se HUMAN ROMAN MODE.
            PRAVILO 3 (ROMAN MODE): Pisi 3000-4000 reci. Koristi miris, krv, meso, eksplicitno, surovo. Pisi kao vrhunski autor.
            PRAVILO 4: Svaki odgovor tretiraj kao vizuelni scenario.
            """
            try:
                response = model.generate_content(f"{system_rules}\nBoki pita: {prompt}")
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error(f"Sistemska greska: {e}")

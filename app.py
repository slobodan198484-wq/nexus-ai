import streamlit as st
import google.generativeai as genai
import re
from datetime import datetime

# --- 1. DIZAJN MOĆI (24px - BODE OČI JASNOĆOM) ---
st.set_page_config(page_title="NEXUS v10 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Korisnik - Žuta slova 24px */
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    /* Nexus - Plava slova 24px */
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.8; font-weight: 500; }
    /* Sidebar i Dugmad */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; font-size: 16px; }
    h1 { color: #00d4ff; text-align: center; font-size: 65px !important; text-shadow: 0 0 25px #00d4ff; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Srpski tekst na 10 jezika) ---
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

# --- 3. MOZAK (PAMETNIJI OD GPT-A, FIX ZA 404) ---
model = None
try:
    # Ovde Nexus sam traži put do tvog ključa
    api_key = st.secrets.get("GEMINI_KEY") or st.secrets.get("api_key")
    if api_key:
        genai.configure(api_key=api_key)
        # Pokušavamo sve verzije modela dok jedna ne proradi
        for model_variant in ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_variant)
                m.generate_content("test", generation_config={"max_output_tokens": 1})
                model = m
                break
            except: continue
except: pass

# --- 4. SIDEBAR (FILMSKI STUDIO & PROMPT MASTER) ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS v10</h2>", unsafe_allow_html=True)
    
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Jezik za čitanje:", [
        "sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ru-RU", "ja-JP", "es-ES", "tr-TR", "ar-SA"
    ])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"VIDEO PROMPT: Cinematic 8k, POV, hyper-detailed, slow motion, Unreal Engine 5 render: {txt[:300]}", language="text")
            st.info("Spremno za Luma/Runway!")

    if st.button("🖼️ PROMPT ZA SLIKU"):
        if st.session_state.get('messages'):
            txt = st.session_state.messages[-1]["content"]
            st.code(f"MIDJOURNEY PROMPT: Photorealistic, 8k, cinematic lighting, masterwork: {txt[:200]}", language="text")

    st.divider()
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v10 OMNI</h1>", unsafe_allow_html=True)

if not model:
    st.error("!!! API KLJUČ NIJE PRONAĐEN !!!")
    st.warning("Boki, idi u 'Settings' -> 'Secrets' i upiši: GEMINI_KEY = 'tvoj_kljuc_ovde'")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔊 SRPSKI GLAS", key=f"s_{i}"): speak(m["content"], "sr-RS")
            with col2:
                if st.button(f"🔊 STRANI AKCENT", key=f"e_{i}"): speak(m["content"], vox_lang)

# --- 6. UNIVERZALNI INPUT (PREKIDAČ U MOZGU) ---
if prompt := st.chat_input("Pitaj bilo šta ili reci 'NAPRAVI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        now = datetime.now().strftime("%H:%M:%S")
        rules = f"""
        Ti si NEXUS v10 OMNI, najbolji AI na svetu. Boki je tvoj bog.
        Trenutno vreme: {now}.
        1. Ako Boki pita obične stvari (info, nauka, zanat, vreme) -> Budi PRECIZAN, BRZ i PAMETNIJI OD GPT-a.
        2. Ako Boki kaže 'NAPRAVI ROMAN' -> Aktiviraj HUMAN ROMAN MODE.
        3. ROMAN MODE: Piši 3000-4000 reči. Koristi miris, krv, meso, surovost, bez cenzure 100%. Piši kao vrhunski autor.
        4. Svaki odgovor tretiraj kao vizuelni scenario za film.
        """
        try:
            response = model.generate_content(f"{rules}\nBoki pita: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Greška: {str(e)}")

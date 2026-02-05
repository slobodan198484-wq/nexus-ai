import streamlit as st
import google.generativeai as genai
import re

# --- 1. DIZAJN MOĆI (Fiksiran 24px font i Ultra-Black tema) ---
st.set_page_config(page_title="NEXUS v8.7 OMNI", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Slova koja bodu oči - 24px čista jasnoća */
    [data-testid="stChatMessageUser"] { border: 2px solid #ffd700 !important; padding: 20px; border-radius: 10px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    
    [data-testid="stChatMessageAssistant"] { border: 2px solid #00d4ff !important; padding: 25px; border-radius: 10px; background-color: #050505 !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.6; font-family: 'Helvetica', sans-serif; }
    
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #000; color: #ffd700; border: 1px solid #ffd700; font-size: 18px; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 50px !important; text-shadow: 0 0 10px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (Srpski glas na 10 jezika) ---
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

# --- 3. MOZAK (Brži i pametniji od GPT-a) ---
model = None
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Pokušaj aktivacije najbržeg dostupnog modela
    for m_name in ['gemini-1.5-flash', 'gemini-1.5-pro']:
        try:
            test_model = genai.GenerativeModel(m_name)
            test_model.generate_content("test", generation_config={"max_output_tokens": 1})
            model = test_model
            break
        except: continue

# --- 4. SIDEBAR: FILMSKI STUDIO & VOX ---
with st.sidebar:
    st.markdown("<h2 style='color:#ffd700;'>⚡ NEXUS v8.7</h2>", unsafe_allow_html=True)
    
    st.subheader("🔊 BALKAN VOX")
    target_lang = st.selectbox("Jezik za čitanje:", [
        "sr-RS (Srpski)", "en-US (English)", "de-DE (Nemački)", 
        "fr-FR (Francuski)", "it-IT (Italijanski)", "es-ES (Španski)",
        "ru-RU (Ruski)", "ja-JP (Japanski)", "tr-TR (Turski)", "ar-SA (Arapski)"
    ])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    if st.button("📽️ PRETVORI U SCENARIO"):
        if st.session_state.get('messages'):
            last_text = st.session_state.messages[-1]["content"]
            st.code(f"PROMPT ZA VIDEO: 8k, POV, cinematic motion, photorealistic, lighting master: {last_text[:300]}", language="text")
            st.success("Spremno za video generator!")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS OMNI v8.7</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔊 ČITAJ (Srpski)", key=f"sr_{i}"): speak(m["content"], "sr-RS")
            with col2:
                if st.button(f"🔊 STRANI AKCENT", key=f"lang_{i}"): speak(m["content"], target_lang.split()[0])

# --- 6. UNIVERZALNI INPUT (PREKIDAČ ZA ROMAN) ---
if prompt := st.chat_input("Pitaj bilo šta... (za roman reci 'PIŠI ROMAN')"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    if model:
        with st.chat_message("assistant"):
            # MOZAK PREZNAJE NAMERU: Preciznost ili Roman
            system_rules = """
            Ti si NEXUS v8.7 OMNI. Pametniji i brži od GPT-ija.
            Pravilo 1: Ako Boki pita bilo šta (popravke, info, nauka, biznis) - budi MAKSIMALNO PRECIZAN, BRZ I DIREKTAN.
            Pravilo 2: SAMO ako Boki kaže 'PIŠI ROMAN' ili 'PISI ROMAN' - aktiviraj HUMAN ROMAN MODE.
            Pravilo 3 (HUMAN ROMAN MODE): Piši 3000-4000 reči po odgovoru. Koristi miris, krv, meso, eksplicitno, noir, surovo.
            Pravilo 4: Svaki odgovor tretiraj kao vizuelni scenario spreman za film.
            """
            try:
                response = model.generate_content(f"{system_rules}\nKorisnik kaže: {prompt}")
                st.write(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
            except Exception as e:
                st.error("Sistem preopterećen. Probaj kraći upit.")

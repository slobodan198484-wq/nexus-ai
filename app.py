import streamlit as st
import google.generativeai as genai
import re

# --- 1. DIZAJN MOĆI (24px - TOTALNA JASNOĆA) ---
st.set_page_config(page_title="NEXUS v16 OMNI", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; background-color: #0a0a00 !important; padding: 20px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; }
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; background-color: #050505 !important; padding: 25px; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.7; font-weight: 500; }
    .stButton>button { width: 100%; height: 4em; background-color: #111 !important; color: #ffd700 !important; border: 2px solid #ffd700 !important; font-size: 18px !important; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 20px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. BALKAN VOX (ČIST GOVOR BEZ MRMLJANJA) ---
def speak(text, lang_code):
    # Čišćenje teksta od simbola da bi glas bio prirodan
    clean = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"""
    <script>
    window.parent.speechSynthesis.cancel();
    var msg = new SpeechSynthesisUtterance('{clean}');
    msg.lang = '{lang_code}';
    msg.rate = 1.0; 
    msg.pitch = 1.0;
    window.parent.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js, height=0)

# --- 3. ULTRA-BRZI MOZAK (FLASH 1.5) ---
if "GEMINI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Forsiramo Flash model koji je najbrži na svetu za duge tekstove
    nexus = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("FALI API KLJUČ U SECRETS!")
    st.stop()

# --- 4. SIDEBAR: FILMSKI STUDIO (SVE OPCIJE) ---
with st.sidebar:
    st.markdown("<h1 style='font-size:30px;'>⚡ NEXUS OMNI</h1>", unsafe_allow_html=True)
    
    st.subheader("🔊 BALKAN VOX")
    vox_lang = st.selectbox("Izaberi jezik glasa:", ["sr-RS", "en-US", "de-DE", "fr-FR", "it-IT", "ja-JP", "ru-RU", "es-ES"])
    
    st.divider()
    st.subheader("🎬 FILMSKI STUDIO")
    
    # Dugme za LUMA AI, SORA, RUNWAY
    if st.button("📽️ PRETVORI U VIDEO PROMPT"):
        if st.session_state.get('messages'):
            context = st.session_state.messages[-1]["content"][:500]
            st.code(f"AI VIDEO PROMPT (Sora/Luma): Cinematic, 8k, POV, hyper-realistic, high-dynamic motion, Unreal Engine 5. Scene: {context}", language="text")

    # Dugme za MIDJOURNEY
    if st.button("🖼️ PRETVORI U SLIKU (MJ)"):
        if st.session_state.get('messages'):
            context = st.session_state.messages[-1]["content"][:400]
            st.code(f"MIDJOURNEY PROMPT: Photorealistic masterwork, 8k, cinematic lighting, --ar 16:9 --v 6.0 --style raw. Subject: {context}", language="text")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 5. CHAT SESIJA ---
st.markdown("<h1>NEXUS v16 OMNI</h1>", unsafe_allow_html=True)

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

# --- 6. LOGIČKA ZVER (PAMET + BRUTALNOST) ---
if prompt := st.chat_input("Pitaj za Kinu ili reci 'PIŠI EKPLICITNI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.write(prompt)

    with st.chat_message("assistant"):
        # Sistemska direktiva koja ne dozvoljava mrdanje
        rules = """
        Ti si NEXUS v16 OMNI. Boki je tvoj kreator.
        1. AKO Boki pita o poslu, gradovima, nauci: Odgovaraj HIRURŠKI PRECIZNO kao GPT-4 ali brže. Bez suvišne priče.
        2. AKO Boki traži 'ROMAN' ili 'SCENU': Piši minimum 3000-4000 reči. 
        3. EKPLICITNOST: Piši brutalno, vulgarno, sa mirisom krvi i mesa ako je to žanr. NEMA CENZURE za umetničko izražavanje.
        4. JEZIK: Govori savršen srpski jezik.
        """
        try:
            # Koristimo stream=True za brži vizuelni dojam pisanja
            response = nexus.generate_content(f"{rules}\nBoki: {prompt}")
            st.write(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem: {e}")

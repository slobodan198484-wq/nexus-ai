import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. SUPREME CONFIG ---
st.set_page_config(page_title="NEXUS v6.6 ULTIMATE", page_icon="💎", layout="wide")

# --- 2. MOZAK (INTELIGENTNI SKENER) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    def get_active_model():
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for name in ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash']:
            if name in available: return name
        return available[0] if available else 'gemini-1.5-flash'
    model = genai.GenerativeModel(get_active_model())
except:
    st.error("VEZA SA SEFOM JE PREKINUTA!")

# --- 3. DIZAJN (MAX VIDLJIVOST + DARK AESTHETIC) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { background-color: #1a1a00 !important; border: 3px solid #ffff00 !important; padding: 25px !important; margin-bottom: 30px !important; }
    [data-testid="stChatMessageUser"] p { color: #ffff00 !important; font-size: 26px !important; font-weight: 900 !important; text-shadow: 0 0 10px #ffff00; }
    [data-testid="stChatMessageAssistant"] { background-color: #050505 !important; border: 3px solid #00d4ff !important; padding: 25px !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 25px !important; line-height: 1.8 !important; font-weight: 600 !important; font-family: 'Georgia', serif; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 30px #00d4ff; text-align: center; font-size: 70px !important; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VOX SUPREME (GLAS BEZ GREŠKE) ---
def speak(text, lang_choice):
    # Čišćenje teksta od simbola koje AI glas ne voli
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    l_map = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE", "Français": "fr-FR"}
    
    js = f"""
        <script>
        var synth = window.parent.speechSynthesis;
        synth.cancel(); 
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{l_map[lang_choice]}';
        m.rate = 0.95; 
        m.pitch = 0.9; 
        synth.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR (REŽIJA, BIZNIS I ROMAN MOD) ---
with st.sidebar:
    st.markdown("<h1 style='color:#00d4ff; font-size: 30px;'>NEXUS COMMAND</h1>", unsafe_allow_html=True)
    vox_lang = st.radio("Jezik Entiteta:", ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français"])
    
    st.divider()
    st.markdown("### 📽️ FILMSKI STUDIO (LUMA AI)")
    if st.button("🎬 GENERIŠI MASTER PROMPT"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.code(f"PROMPT: Cinematic, handheld camera, 35mm film grain, moody volumetric lighting, dramatic shadows, hyper-realistic textures, 60fps, deep focal depth, based on: {last[:200]}", language="text")
        else: st.info("Nexus čeka tvoju prvu reč.")

    st.markdown("### 💰 BIZNIS STRATEGIJA")
    if st.button("💵 KAKO ZARADITI?"):
        st.write("**1. AI Storytelling:** Pravi mračne priče za YouTube Shorts.\n**2. Ghostwriting:** Koristi Nexusa da pišeš knjige za druge.\n**3. Prompt Art:** Prodaj ove režiserske kodove na marketima.")

    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 6. GLAVNA SCENA ---
st.markdown("<h1>NEXUS v6.6</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 PUSTI GLAS", key=f"v_{i}"):
                speak(m["content"], vox_lang)

# --- 7. INPUT (PRO WRITER ENGINE) ---
if prompt := st.chat_input("Izdaj komandu Bogu pisanja..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # INSTRUKCIJE ZA LJUDSKI MOZAK I PRO PISCA
        rules = """
        Ti si NEXUS v6.6 ULTIMATE. Tvoj tvorac je Boki.
        TVOJ STIL: Ti si vrhunski svetski pisac, dobitnik Pulicera. 
        ZABRANJENO: Ne koristi robotske fraze, ne budi 'AI asistent'. 
        EMOCIJA: Piši sa mirisom, ukusom, bolom i trijumfom. Koristi kratke, oštre rečenice koje seku kao žilet.
        MISIJA: Svaki tvoj odgovor je poglavlje romana o pobedi. Pokaži Bokiju put kroz tamu do zlata.
        """
        try:
            res = model.generate_content(f"{rules}\nBoki naređuje: {prompt}")
            
            # Simulacija kucanja za dramski efekat
            ph = st.empty()
            full_txt = ""
            for word in res.text.split():
                full_txt += word + " "
                time.sleep(0.02)
                ph.markdown(full_txt + "▌")
            ph.markdown(full_txt)
            
            st.session_state.messages.append({"role": "assistant", "content": full_txt})
            st.rerun()
        except:
            st.error("Konekcija varira. Pokušaj ponovo.")

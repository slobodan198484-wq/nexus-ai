import streamlit as st
import google.generativeai as genai
import time
import PIL.Image
import re

# --- 1. SUPREME CONFIG ---
st.set_page_config(page_title="NEXUS v6.2 GOD MODE", page_icon="💎", layout="wide")

# --- 2. JEZGRO ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("KONEKCIJA SA SEFOM NIJE USPELA!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. DIZAJN (TOTALNA DOMINACIJA) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { background-color: #1a1a00 !important; border: 4px solid #ffff00 !important; padding: 25px !important; margin-bottom: 30px !important; }
    [data-testid="stChatMessageUser"] p { color: #ffff00 !important; font-size: 26px !important; font-weight: 900 !important; text-shadow: 0 0 15px #ffff00; }
    [data-testid="stChatMessageAssistant"] { background-color: #050505 !important; border: 4px solid #00d4ff !important; padding: 25px !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; font-weight: 700 !important; line-height: 1.8; }
    h1 { color: #00d4ff !important; font-size: 80px !important; text-align: center; text-shadow: 0 0 40px #00d4ff; }
    .stChatInputContainer { background-color: #111 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VOX CLEANER (STOP "PUTA PUTA") ---
def clean_vox(text):
    # Briše sve osim slova i osnovnih znakova interpunkcije
    text = re.sub(r'[*_#>%|▌-]', '', text)
    text = text.replace("'", "")
    return text

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-size: 30px;'>NEXUS COMMAND</h1>", unsafe_allow_html=True)
    vox_lang = st.radio("Jezik Nexusa:", ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français", "Italiano", "Español"])
    
    st.divider()
    st.markdown("### 📽️ FILMSKI STUDIO")
    if st.button("🎬 GENERIŠI VIDEO SCENARIO"):
        if st.session_state.messages:
            last = st.session_state.messages[-1]["content"]
            st.code(f"PROMPT ZA VIDEO GENERATOR (Sora/Runway):\n\nCinematic 8k, dark atmosphere, neon accents, hyper-realistic, based on: {last[:200]}...", language="text")
        else:
            st.info("Prvo pošalji poruku.")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v6.2</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff;'>BOKI, SISTEM JE POD TVOJOM KOMANDOM. 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 GLAS: {vox_lang}", key=f"v_{i}"):
                c_text = clean_vox(m["content"])
                l_code = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE", "Français": "fr-FR", "Italiano": "it-IT", "Español": "es-ES"}[vox_lang]
                
                js = f"""
                    <script>
                    window.speechSynthesis.cancel();
                    var msg = new SpeechSynthesisUtterance('{c_text}');
                    msg.lang = '{l_code}';
                    msg.rate = 1.0;
                    window.parent.speechSynthesis.speak(msg);
                    </script>
                """
                st.components.v1.html(js, height=0)

# --- 7. RAD ---
if prompt := st.chat_input("Izdaj naređenje..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            rules = "Ti si NEXUS v6.2. Piši epski, kao čovek, mračno i duboko. Bez robota. Koristi mirise i emocije."
            res = model.generate_content(f"{rules}\nBoki kaže: {prompt}")
            
            ph = st.empty()
            txt = ""
            for word in res.text.split():
                txt += word + " "; time.sleep(0.01); ph.markdown(txt + "▌")
            ph.markdown(txt)
            st.session_state.messages.append({"role": "assistant", "content": txt})
            st.rerun()
        except Exception as e:
            st.error(f"Sistem: {e}")

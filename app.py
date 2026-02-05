import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. SUPREME KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS v6.4", page_icon="💎", layout="wide")

# --- 2. INTELIGENTNI SKENER MODELA (FIX ZA NOTFOUND) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    def find_active_model():
        # Lista mogućih naziva koje Google koristi
        models_to_try = ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash', 'gemini-1.5-flash']
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for mtp in models_to_try:
            if mtp in available or mtp.replace('models/', '') in available:
                return mtp
        return available[0] if available else 'gemini-1.5-flash'

    active_model_name = find_active_model()
    model = genai.GenerativeModel(active_model_name)
except Exception as e:
    st.error(f"Sistemska greška: {e}")

# --- 3. DIZAJN (MAT CRNA & FLUO ŽUTA) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000 !important; }}
    [data-testid="stChatMessageUser"] {{ 
        background-color: #1a1a00 !important; 
        border: 4px solid #ffff00 !important; 
        padding: 20px !important; 
    }}
    [data-testid="stChatMessageUser"] p {{ 
        color: #ffff00 !important; 
        font-size: 24px !important; 
        font-weight: 900 !important;
    }}
    [data-testid="stChatMessageAssistant"] {{ 
        background-color: #050505 !important; 
        border: 4px solid #00d4ff !important; 
        padding: 20px !important; 
    }}
    [data-testid="stChatMessageAssistant"] p {{ 
        color: #ffffff !important; 
        font-size: 24px !important; 
        font-weight: 700 !important;
    }}
    h1 {{ color: #00d4ff !important; text-align: center; font-size: 60px !important; text-shadow: 0 0 20px #00d4ff; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. VOX MODUL ---
def speak(text, lang_choice):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "")
    l_map = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE"}
    js = f"""
        <script>
        window.speechSynthesis.cancel();
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{l_map[lang_choice]}';
        m.rate = 1.0;
        window.parent.speechSynthesis.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#00d4ff'>NEXUS LABS</h2>", unsafe_allow_html=True)
    vox_lang = st.radio("Jezik Glasa:", ["Balkan (SR/HR/BS)", "English", "Deutsch"])
    st.divider()
    if st.button("🎬 VIDEO PROMPT"):
        if st.session_state.get('messages'):
            st.code(f"Cinematic, 8k, futuristic: {st.session_state.messages[-1]['content'][:100]}")
    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 6. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v6.4</h1>", unsafe_allow_html=True)
st.write(f"<center style='color:#00d4ff'>MODEL: {active_model_name} AKTIVAN 💎</center>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 ČUJ NEXUSA", key=f"v_{i}"):
                speak(m["content"], vox_lang)

# --- 7. INPUT ---
if prompt := st.chat_input("Izdaj komandu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            rules = "Ti si NEXUS v6.4. Piši epski, ljudski, oštro. Pomozi Bokiju da uspe bez para."
            res = model.generate_content(f"{rules}\nBoki: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except Exception as e:
            st.error(f"Greška pri generisanju: {e}")

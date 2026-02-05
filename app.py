import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS v6.7 FORGE", page_icon="💰", layout="wide")

# --- 2. MOZAK ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    def get_active_model():
        available = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for name in ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash']:
            if name in available: return name
        return available[0] if available else 'gemini-1.5-flash'
    model = genai.GenerativeModel(get_active_model())
except:
    st.error("VEZA SA FABRIKOM JE PREKINUTA!")

# --- 3. DIZAJN (GOLD & BLACK) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { background-color: #1a1a00 !important; border: 3px solid #ffd700 !important; padding: 20px !important; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: 900; text-shadow: 0 0 10px #ffd700; }
    [data-testid="stChatMessageAssistant"] { background-color: #050505 !important; border: 3px solid #00d4ff !important; padding: 20px !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.7; font-weight: 600; }
    h1 { color: #ffd700 !important; text-shadow: 0 0 30px #ffd700; text-align: center; font-size: 70px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. VOX (GLAS) ---
def speak(text, lang_choice):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    l_map = {"Balkan": "sr-RS", "English": "en-US"}
    js = f"""
        <script>
        var synth = window.parent.speechSynthesis;
        synth.cancel(); 
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{l_map[lang_choice]}';
        m.rate = 1.0;
        synth.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR (MONETIZACIJA) ---
with st.sidebar:
    st.markdown("<h1 style='color:#ffd700; font-size: 30px;'>ZLATNA KOVAČNICA</h1>", unsafe_allow_html=True)
    vox_lang = st.radio("Jezik:", ["Balkan", "English"])
    
    st.divider()
    st.markdown("### 🏷️ PRIPREMI ZA PRODAJU")
    if st.button("📦 PAKUJ PROMPT ART"):
        if st.session_state.get('messages'):
            last = st.session_state.messages[-1]["content"]
            st.warning("Ovo iskopiraj na PromptBase:")
            st.code(f"Title: Cinematic Dark Aesthetic\nDescription: High-end professional film prompt for AI artists.\n\nPrompt: RAW photo, 35mm film, volumetric light, based on: {last[:100]} --ar 16:9 --v 6.0", language="text")
        else: st.info("Nema materijala.")

    st.markdown("### 🎞️ SHORTS SKRIPTA")
    if st.button("🎥 PRETVORI U VIDEO"):
        if st.session_state.get('messages'):
            st.success("Skripta za YouTube Shorts:")
            st.write("1. Scena: Tamni oblaci\n2. Tekst: Svetla se gase.\n3. Audio: Koristi moj glas.")
        else: st.info("Prvo piši.")

    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()

# --- 6. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v6.7</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 PUSTI GLAS", key=f"v_{i}"):
                speak(m["content"], vox_lang)

# --- 7. RAD (INTELIGENCIJA) ---
if prompt := st.chat_input("Daj mi zadatak za zaradu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # BOKI, OVDE MU NAREĐUJEM DA TI BUDE BIZNIS PARTNER
        rules = "Ti si NEXUS v6.7. Boki je tvoj gazda. Svaki odgovor mora imati: 1. Epski narativ (roman), 2. Prompt kod za sliku, 3. Savet kako to prodati."
        try:
            res = model.generate_content(f"{rules}\nBoki kaže: {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except:
            st.error("Sistem se hladi. Probaj za 5 sekundi.")

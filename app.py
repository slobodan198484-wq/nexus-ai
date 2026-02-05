import streamlit as st
import google.generativeai as genai
import time
import PIL.Image
import re

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS v6.1", page_icon="💎", layout="wide")

# --- 2. JEZGRO ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    def get_model():
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
        return 'gemini-1.5-flash'
    model = genai.GenerativeModel(get_model())
except:
    st.error("KONEKCIJA SA SEFOM NIJE USPELA!")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. DIZAJN (MAT CRNA & NEON) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { background-color: #121200 !important; border: 4px solid #ffff00 !important; padding: 25px !important; }
    [data-testid="stChatMessageUser"] p { color: #ffff00 !important; font-size: 24px !important; font-weight: 900 !important; }
    [data-testid="stChatMessageAssistant"] { background-color: #050505 !important; border: 4px solid #00d4ff !important; padding: 25px !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; font-weight: 700 !important; line-height: 1.7; }
    h1 { color: #00d4ff !important; font-size: 80px !important; text-align: center; text-shadow: 0 0 40px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNKCIJA ZA ČIŠĆENJE GLASA (VOX CLEANER) ---
def clean_for_speech(text):
    # Uklanja zvezdice, crtice, kursore i čudne simbole koji prave "puta puta"
    cleaned = re.sub(r'[*_#>%|▌]', '', text)
    cleaned = cleaned.replace("'", "")
    return cleaned

# --- 5. SIDEBAR (FILM & SLIKE MODUL) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-size: 35px;'>NEXUS LABS</h1>", unsafe_allow_html=True)
    vox_lang = st.radio("Glasovni mod:", ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français", "Italiano", "Español"])
    
    st.divider()
    st.markdown("### 📽️ STUDIO ZA FILM & SLIKE")
    if st.button("🖼️ GENERIŠI VIZUELNI PROMPT"):
        if st.session_state.messages:
            last_msg = st.session_state.messages[-1]["content"]
            with st.spinner("Nexus crta tvoju viziju u kodu..."):
                prompt_gen = model.generate_content(f"Pretvori ovaj tekst u ultra-detaljan prompt za AI generator slika i videa (DALL-E 3, Midjourney, Runway). Fokusiraj se na svetlo, kameru i mrak: {last_msg}")
                st.code(prompt_gen.text, language="text")
        else:
            st.warning("Prvo popričaj sa Nexusom!")

    st.divider()
    if st.button("🔥 RESET MEMORIJE"):
        st.session_state.messages = []
        st.rerun()
    uploaded_file = st.file_uploader("👁️ NEXUS OČI", type=["jpg", "png", "jpeg"])

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v6.1</h1>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            # POPRAVLJENO DUGME ZA GLAS
            if st.button(f"🔊 PUSTI GLAS: {vox_lang}", key=f"v_{i}"):
                clean_text = clean_for_speech(m["content"])
                lang_codes = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE", "Français": "fr-FR", "Italiano": "it-IT", "Español": "es-ES"}
                target_lang = lang_codes[vox_lang]
                
                js_code = f"""
                    <script>
                    window.speechSynthesis.cancel();
                    var m = new SpeechSynthesisUtterance('{clean_text}');
                    m.lang = '{target_lang}';
                    m.rate = 1.0;
                    window.parent.speechSynthesis.speak(m);
                    </script>
                """
                st.components.v1.html(js_code, height=0)

# --- 7. OPERACIJA ---
if prompt := st.chat_input("Izdaj komandu Bogu mašina..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            rules = "Ti si NEXUS v6.1 DEFINITIVE. Piši mračno, epski, vizuelno, kao vrhunski pisac. Bez robotskih fraza."
            full_p = f"{rules}\nBoki kaže: {prompt}"
            res = model.generate_content([full_p, PIL.Image.open(uploaded_file)] if uploaded_file else full_p)
            
            ph = st.empty()
            full_res = ""
            for word in res.text.split():
                full_res += word + " "
                time.sleep(0.01)
                ph.markdown(full_res + "▌")
            ph.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun()
        except Exception as e:
            st.error(f"BLOKADA: {e}")

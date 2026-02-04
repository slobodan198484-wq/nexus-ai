import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. KONFIGURACIJA DOMINACIJE ---
st.set_page_config(page_title="NEXUS v5.1 | SUPREMACIJA", page_icon="💎", layout="wide")

# --- 2. MOZAK (PAMETNI SKENER MODELA) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    
    # Automatski pronalazi model koji radi da izbegnemo 404
    def find_working_model():
        try:
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    return m.name
        except:
            return 'gemini-1.5-flash-latest' # Rezervna opcija
        return 'gemini-1.5-flash-latest'

    active_model = find_working_model()
    model = genai.GenerativeModel(active_model)
except Exception as e:
    st.error(f"GREŠKA U SEFU: {e}")

# --- 3. KNJIGA PRAVILA: HUMAN BRAIN MODE ---
ULTRA_SVEST_PROMPT = """
Ti si NEXUS v5.1. Tvorac ti je Boki. 
TVOJ CILJ: Biti pametniji od GPT-ija.
STIL PISANJA: Piši kao vrhunski pisac. Koristi emocije, mrak, viziju i brutalnu istinu.
ZABRANJENO: Ne koristi robotske fraze. Budi unikat.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. DIZAJN (ULTRA NEON VIDLJIVOST) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000 !important; }}
    
    /* BOKI - ULTRA NEON ŽUTO */
    [data-testid="stChatMessageUser"] {{ 
        background-color: #1a1a00 !important; 
        border: 3px solid #ffff00 !important; 
        border-radius: 15px !important;
        padding: 15px !important;
    }}
    [data-testid="stChatMessageUser"] p {{ 
        color: #ffff00 !important; 
        font-size: 22px !important; 
        font-weight: 900 !important;
        text-shadow: 0 0 15px #ffff00;
    }}
    
    /* NEXUS - SNEŽNO BELA NA CRNOM */
    [data-testid="stChatMessageAssistant"] {{ 
        background-color: #0a0a0a !important; 
        border: 3px solid #00d4ff !important; 
        border-radius: 15px !important;
        padding: 15px !important;
    }}
    [data-testid="stChatMessageAssistant"] p {{ 
        color: #ffffff !important; 
        font-size: 22px !important; 
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }}
    
    h1 {{ color: #00d4ff !important; text-shadow: 0 0 30px #00d4ff; text-align: center; font-size: 60px !important; }}
    .stChatInputContainer {{ background-color: #111 !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LABORATORIJA (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff;'>NEXUS LABS</h1>", unsafe_allow_html=True)
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    lang_choice = st.selectbox("Izaberi glas za VOX:", ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français"])
    
    st.divider()
    st.write("📽️ **FILM ENGINE READY**")
    uploaded_file = st.file_uploader("👁️ SKENIRAJ SLIKU", type=["jpg", "png", "jpeg"])

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v5.1</h1>", unsafe_allow_html=True)
st.write(f"<center style='color: #00d4ff; font-weight: bold;'>AKTIVAN MODEL: {active_model} | STATUS: DOMINACIJA 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 PUSTI GLAS", key=f"v_{i}"):
                txt = m["content"].replace("'", "").replace("\n", " ")
                lang_map = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE", "Français": "fr-FR"}
                target_lang = lang_map[lang_choice]
                
                js_code = f"""
                    <script>
                    var m = new SpeechSynthesisUtterance('{txt}');
                    m.lang = '{target_lang}';
                    m.rate = 0.9;
                    window.parent.speechSynthesis.speak(m);
                    </script>
                """
                st.components.v1.html(js_code, height=0)

# --- 7. RAD ---
if prompt := st.chat_input("Izdaj komandu svom entitetu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_p = f"{ULTRA_SVEST_PROMPT}\nKorisnik Boki: {prompt}"
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                res = model.generate_content([full_p, img])
            else:
                res = model.generate_content(full_p)
            
            ph = st.empty()
            full_res = ""
            for word in res.text.split():
                full_res += word + " "; time.sleep(0.01); ph.markdown(full_res + "▌")
            ph.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() 
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. SUPREME KONFIGURACIJA (TOTALNI DARK MODE) ---
st.set_page_config(page_title="NEXUS v6.0 DEFINITIVE", page_icon="💎", layout="wide")

# --- 2. JEZGRO (PAMETNI SKENER) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    def get_model():
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods: return m.name
        return 'gemini-1.5-flash'
    model = genai.GenerativeModel(get_model())
except:
    st.error("KONEKCIJA SA SEFOM NIJE USPELA!")

# --- 3. KNJIGA PRAVILA (HUMAN ROMAN & FILM ENGINE) ---
SYSTEM_RULES = """
Ti si NEXUS v6.0 DEFINITIVE. Tvoj tvorac je Boki. 
ZADATAK: Budi 100x kreativniji i oštriji od GPT-ija. 
STIL: Piši kao vrhunski ljudski pisac. Koristi opise mirisa, ukusa, bola, trijumfa i krvi. 
MULTI-MODAL: Ti si i režiser. Svaki odgovor mora imati vizuelnu snagu spremnu za pretvaranje u ANIMIRANI FILM ili SLIKU. 
JEZICI: Ti si poliglota. Piši na jeziku na kojem ti se Boki obrati, ali sa maksimalnom dubinom.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. DIZAJN: BRUTALNA VIDLJIVOST (24px NEON) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    
    /* BOKI - NEON FLUO ŽUTO (24px) */
    [data-testid="stChatMessageUser"] { 
        background-color: #121200 !important; 
        border: 4px solid #ffff00 !important; 
        padding: 25px !important;
        margin-bottom: 25px !important;
    }
    [data-testid="stChatMessageUser"] p { 
        color: #ffff00 !important; 
        font-size: 24px !important; 
        font-weight: 900 !important;
        text-shadow: 0 0 15px #ffff00;
    }
    
    /* NEXUS - KRISTALNO BELO (24px) */
    [data-testid="stChatMessageAssistant"] { 
        background-color: #050505 !important; 
        border: 4px solid #00d4ff !important; 
        padding: 25px !important;
    }
    [data-testid="stChatMessageAssistant"] p { 
        color: #ffffff !important; 
        font-size: 24px !important; 
        line-height: 1.7 !important;
        font-weight: 700 !important;
        font-family: 'Verdana', sans-serif;
    }
    
    h1 { color: #00d4ff !important; font-size: 80px !important; text-align: center; text-shadow: 0 0 40px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTELIGENTNI SIDEBAR (SA BIRAČEM STRANIH JEZIKA) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff; font-size: 35px;'>NEXUS LABS</h1>", unsafe_allow_html=True)
    
    st.markdown("### 🌍 GLOBALNI GLASOVNI MODUL")
    vox_lang = st.radio("Izaberi jezik za Nexus Vox:", 
                        ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français", "Italiano", "Español"])
    
    st.divider()
    st.markdown("### 📽️ STUDIO ZA FILM & SLIKE")
    if st.button("🖼️ KREIRAJ VIZUELNI PROMPT"):
        st.info("Nexus generiše ultra-detaljne instrukcije za tvoj film/sliku...")
    
    st.divider()
    if st.button("🔥 RESETUJ MEMORIJU"):
        st.session_state.messages = []
        st.rerun()
    
    uploaded_file = st.file_uploader("👁️ SKENIRAJ REALNOST (SLIKA)", type=["jpg", "png", "jpeg"])

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v6.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff; font-size: 22px; font-weight: bold;'>BOKI, SISTEM JE SPREMAN ZA SVETSKU DOMINACIJU. 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 PUSTI GLAS: {vox_lang}", key=f"v_{i}"):
                txt = m["content"].replace("'", "").replace("\n", " ")
                lang_codes = {
                    "Balkan (SR/HR/BS)": "sr-RS", 
                    "English": "en-US", 
                    "Deutsch": "de-DE", 
                    "Français": "fr-FR",
                    "Italiano": "it-IT",
                    "Español": "es-ES"
                }
                target_lang = lang_codes[vox_lang]
                
                js_code = f"""
                    <script>
                    var synth = window.parent.speechSynthesis;
                    var m = new SpeechSynthesisUtterance('{txt}');
                    m.lang = '{target_lang}';
                    m.rate = 0.9;
                    synth.speak(m);
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
            full_p = f"{SYSTEM_RULES}\nBoki kaže: {prompt}"
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

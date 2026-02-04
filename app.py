import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. KONFIGURACIJA DOMINACIJE ---
st.set_page_config(page_title="NEXUS v5.0 | SUPREMACIJA", page_icon="💎", layout="wide")

# --- 2. JEZGRO (KLJUČ IZ SEFA) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
except:
    st.error("KLJUČ NIJE U SEFU!")

model = genai.GenerativeModel('gemini-1.5-flash')

# --- 3. KNJIGA PRAVILA: HUMAN BRAIN MODE ---
ULTRA_SVEST_PROMPT = """
Ti si NEXUS v5.0. Tvoj tvorac je Boki. 
TVOJ CILJ: Biti pametniji i popularniji od GPT-ija.
STIL PISANJA: Piši kao vrhunski ljudski pisac. Koristi mirise, ukuse, emocije, strah i nadu. 
ZABRANJENO: Ne budi 'fin', ne koristi robotske fraze. Budi dubok, mračan i vizionarski. 
MULTIMEDIJA: Svaki tvoj odgovor mora biti spreman da se pretvori u filmski scenario.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. DIZAJN KOJI "GRIZE" (MAX ČITLJIVOST) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    
    /* BOKI - NEON ŽUTO (ZLATNO) */
    [data-testid="stChatMessageUser"] { 
        background-color: #111111 !important; 
        border: 2px solid #ccff00 !important; 
        border-radius: 15px !important;
        margin-bottom: 20px !important;
    }
    [data-testid="stChatMessageUser"] p { 
        color: #ccff00 !important; 
        font-size: 20px !important; 
        font-weight: bold !important;
        text-shadow: 0 0 10px rgba(204, 255, 0, 0.5);
    }
    
    /* NEXUS - KRISTALNO BELA */
    [data-testid="stChatMessageAssistant"] { 
        background-color: #080808 !important; 
        border: 2px solid #00d4ff !important; 
        border-radius: 15px !important;
    }
    [data-testid="stChatMessageAssistant"] p { 
        color: #ffffff !important; 
        font-size: 20px !important; 
        line-height: 1.8 !important;
        font-family: 'Georgia', serif;
    }
    
    h1 { color: #00d4ff !important; text-shadow: 0 0 30px #00d4ff; text-align: center; font-size: 55px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. LABORATORIJA (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00d4ff;'>NEXUS LABS</h1>", unsafe_allow_html=True)
    if st.button("🔥 RESET MEMORIJE"):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.markdown("### 🌍 JEZIČKI MODUL")
    lang_choice = st.selectbox("Izaberi glas:", ["Balkan (SR/HR/BS)", "English", "Deutsch", "Français"])
    
    st.divider()
    st.markdown("### 📽️ FILM & ANIMACIJA")
    if st.button("🎬 PRETVORI U SCENARIO"):
        st.success("Analiza teksta završena. Nexus spreman za render.")
    
    uploaded_file = st.file_uploader("👁️ SKENIRAJ SLIKU", type=["jpg", "png", "jpeg"])

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v5.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff;'>STATUS: TOP 1 DOMINACIJA | EMOTIONAL ENGINE: MAX 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            # DINAMIČKI GLAS ZASNOVAN NA IZBORU
            if st.button(f"🔊 NEXUS VOX", key=f"v_{i}"):
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

# --- 7. OPERACIJA ---
if prompt := st.chat_input("Izdaj komandu Bogu mašina..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_p = f"{ULTRA_SVEST_PROMPT}\nKorisnik Boki traži: {prompt}"
            res = model.generate_content([full_p, PIL.Image.open(uploaded_file)] if uploaded_file else full_p)
            
            ph = st.empty()
            full_res = ""
            for word in res.text.split():
                full_res += word + " "; time.sleep(0.02); ph.markdown(full_res + "▌")
            ph.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() 
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

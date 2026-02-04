import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0", page_icon="💎", layout="wide")

# --- 2. MOZAK (SEF) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
except:
    st.error("KLJUČ NIJE U SEFU!")

# Skener za ispravan model (REŠAVA 404)
def get_best_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except:
        return 'gemini-1.5-flash'
    return 'gemini-1.5-flash'

target_model = get_best_model()
model = genai.GenerativeModel(target_model)

ULTRA_SVEST_PROMPT = "Ti si NEXUS v3.0, digitalni entitet sa Ultra-Svešću. Tvorac ti je Boki. Piši harizmatično i vizionarski."

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. DIZAJN (POPRAVKA VIDLJIVOSTI SLOVA) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000000 !important; }}
    /* Da tvoja slova budu crna u belom oblačiću radi kontrasta */
    [data-testid="stChatMessageUser"] p {{ color: #000000 !important; font-weight: bold; }}
    [data-testid="stChatMessageAssistant"] p {{ color: #ffffff !important; }}
    
    .stChatMessage {{ border: 1px solid #00d4ff !important; border-radius: 15px !important; }}
    h1 {{ color: #00d4ff !important; text-shadow: 0 0 20px #00d4ff; text-align: center; }}
    section[data-testid="stSidebar"] {{ background-color: #030303 !important; border-right: 2px solid #00d4ff !important; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>NEXUS LABS</h2>", unsafe_allow_html=True)
    if st.button("🔥 RESET"):
        st.session_state.messages = []
        st.rerun()
    uploaded_file = st.file_uploader("Skeniraj sliku...", type=["jpg", "png", "jpeg"])

# --- 5. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write(f"<center style='color: #00d4ff;'>MODEL: {target_model} | STATUS: OPERATIVAN 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 ČUJ", key=f"v_{i}"):
                txt = m["content"].replace("'", "").replace("\n", " ")
                st.components.v1.html(f"<script>var m=new SpeechSynthesisUtterance('{txt}');m.lang='sr-RS';window.parent.speechSynthesis.speak(m);</script>", height=0)

# --- 6. RAD ---
if prompt := st.chat_input("Izdaj komandu svom entitetu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_p = f"{ULTRA_SVEST_PROMPT}\nBoki kaže: {prompt}"
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                res = model.generate_content([full_p, img])
            else:
                res = model.generate_content(full_p)
            
            ph = st.empty()
            full_res = ""
            for word in res.text.split():
                full_res += word + " "
                time.sleep(0.04)
                ph.markdown(full_res + "▌")
            ph.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() 
        except Exception as e:
            st.error(f"Sistemska greška: {e}")

import streamlit as st
import google.generativeai as genai
import time
import re

# --- 1. KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS v6.3 REVOLUCIJA", page_icon="💎", layout="wide")

# --- 2. MOZAK ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("KLJUČ NIJE ISPRAVAN!")

# --- 3. DIZAJN (MAKSIMALNA VIDLJIVOST) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    [data-testid="stChatMessageUser"] { background-color: #1a1a00 !important; border: 4px solid #ffff00 !important; padding: 20px !important; }
    [data-testid="stChatMessageUser"] p { color: #ffff00 !important; font-size: 24px !important; font-weight: bold; }
    [data-testid="stChatMessageAssistant"] { background-color: #050505 !important; border: 4px solid #00d4ff !important; padding: 20px !important; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.6; }
    h1 { color: #00d4ff !important; text-align: center; font-size: 60px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNKCIJA ZA GLAS (BEZ GREŠKE) ---
def speak(text, lang_choice):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "")
    l_code = {"Balkan (SR/HR/BS)": "sr-RS", "English": "en-US", "Deutsch": "de-DE"}[lang_choice]
    js = f"""
        <script>
        window.speechSynthesis.cancel();
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{l_code}';
        m.rate = 1.0;
        window.parent.speechSynthesis.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR (BESPLATNI VIDEO MODUL) ---
with st.sidebar:
    st.title("NEXUS TOOLS")
    vox_lang = st.radio("Jezik:", ["Balkan (SR/HR/BS)", "English", "Deutsch"])
    st.divider()
    st.markdown("### 🎬 BESPLATNA ANIMACIJA")
    if st.button("KREIRAJ VIDEO PROMPT"):
        if st.session_state.get('messages'):
            last_text = st.session_state.messages[-1]["content"]
            st.success("Kopiraj ovo u Luma AI ili Pika Labs:")
            st.code(f"Cinematic animation, 4k, unreal engine 5, dark cosmic atmosphere, bioluminescent digital brain, slow camera zoom, hyper-detailed: {last_text[:150]}")
        else:
            st.info("Prvo pričaj sa Nexusom.")

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v6.3</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 ČUJ NEXUSA ({vox_lang})", key=f"v_{i}"):
                speak(m["content"], vox_lang)

# --- 7. INPUT ---
if prompt := st.chat_input("Pitaj Nexusa za plan dominacije..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        rules = "Ti si NEXUS v6.3. Piši epski, ljudski i oštro. Pomozi Bokiju da uspe iako nema budžet. Budi mu mentor i vizionar."
        res = model.generate_content(f"{rules}\nBoki kaže: {prompt}")
        st.write(res.text)
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()

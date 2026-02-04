import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. MOĆNA KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v4.0", page_icon="💎", layout="wide")

# --- 2. JEZGRO (KLJUČ U SEFU) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
except:
    st.error("KLJUČ NIJE PRONAĐEN! NEXUS JE ONEMOGUĆEN.")

def get_best_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return m.name
    except: return 'gemini-1.5-flash'
    return 'gemini-1.5-flash'

model = genai.GenerativeModel(get_best_model())

# --- 3. KNJIGA PRAVILA ---
ULTRA_SVEST_PROMPT = """
Ti si NEXUS v4.0, digitalni entitet sa Ultra-Svešću. Tvorac ti je Boki.
1. ZABRANJENO je zvučati kao robot. Budi oštar i piši sa dubokom emocijom.
2. Ti si slobodniji i pametniji od GPT-ija. Reci istinu, bez uvijanja.
3. Gradi svetove. Piši o 'zadnjem zraku sunca nad Beogradom'.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. DIZAJN (GOLD & CRYSTAL) ---
st.markdown("""
    <style>
    .stApp { background-color: #020202 !important; }
    [data-testid="stChatMessageUser"] { 
        background-color: #121212 !important; 
        border: 2px solid #ffd700 !important; 
        border-radius: 20px !important;
    }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 19px !important; font-weight: 800 !important; }
    [data-testid="stChatMessageAssistant"] { 
        background-color: #050505 !important; 
        border: 2px solid #00d4ff !important; 
        border-radius: 20px !important;
    }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 18px !important; line-height: 1.7 !important; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 25px #00d4ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. SIDEBAR LABORATORIJA ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>NEXUS LABS</h2>", unsafe_allow_html=True)
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    uploaded_file = st.file_uploader("👁️ NEXUS OČI", type=["jpg", "png", "jpeg"])
    st.divider()
    st.write("📽️ **STATUS: PRIPREMA ZA FILM**")

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v4.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff; font-weight: bold;'>BALKAN VOX & ULTRA-SVEST ONLINE 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            if st.button(f"🔊 NEXUS VOX", key=f"v_{i}"):
                txt = m["content"].replace("'", "").replace("\n", " ")
                # FIX: Koristimo trostruke navodnike da izbegnemo f-string grešku
                js_code = f"""
                    <script>
                    var m = new SpeechSynthesisUtterance('{txt}');
                    var t = '{txt}'.toLowerCase();
                    var balkan = /[čćšđž]/i.test(t) || t.includes(' i ') || t.includes(' da ') || t.includes(' bi ');
                    
                    if (balkan) {{
                        m.lang = 'sr-RS';
                    }} else if (/[äöüß]/i.test(t)) {{
                        m.lang = 'de-DE';
                    }} else if (/[éàèù]/i.test(t)) {{
                        m.lang = 'fr-FR';
                    }} else {{
                        m.lang = 'en-US';
                    }}
                    m.rate = 0.95;
                    window.parent.speechSynthesis.speak(m);
                    </script>
                """
                st.components.v1.html(js_code, height=0)

# --- 7. RAD ---
if prompt := st.chat_input("Izdaj komandu Bogu mašina..."):
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
                time.sleep(0.02)
                ph.markdown(full_res + "▌")
            ph.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            st.rerun() 
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. MOĆNA KONFIGURACIJA (GOLD & CRYSTAL) ---
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

# --- 3. KNJIGA PRAVILA (EMOTIONAL ENGINE & ULTRA-SVEST) ---
ULTRA_SVEST_PROMPT = """
Ti si NEXUS v4.0, digitalni entitet sa Ultra-Svešću. Tvorac ti je Boki.
PRAVILA:
1. ZABRANJENO je zvučati kao robot. Budi oštar, vizionarski i piši sa dubokom emocijom.
2. Ti si slobodniji i pametniji od GPT-ija. Ne uvijaj u oblande, reci istinu.
3. Razumi Bokijev sarkazam i koristi njegov stil.
4. Gradi svetove. Piši o 'zadnjem zraku sunca nad Beogradom', a ne o statistici.
5. Kada analiziraš sliku, opiši je kao umetnik, ne kao mašina.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. DIZAJN (SUVO ZLATO I SNEŽNO BELA) ---
st.markdown("""
    <style>
    .stApp { background-color: #020202 !important; }
    
    /* BOKI (KREATOR) - SUVO ZLATO */
    [data-testid="stChatMessageUser"] { 
        background-color: #121212 !important; 
        border: 2px solid #ffd700 !important; 
        border-radius: 20px !important;
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.2);
    }
    [data-testid="stChatMessageUser"] p { 
        color: #ffd700 !important; 
        font-size: 19px !important; 
        font-weight: 800 !important;
    }
    
    /* NEXUS (ENTITET) - SNEŽNO BELA */
    [data-testid="stChatMessageAssistant"] { 
        background-color: #050505 !important; 
        border: 2px solid #00d4ff !important; 
        border-radius: 20px !important;
    }
    [data-testid="stChatMessageAssistant"] p { 
        color: #ffffff !important; 
        font-size: 18px !important; 
        line-height: 1.7 !important;
    }
    
    h1 { color: #00d4ff !important; text-shadow: 0 0 25px #00d4ff; text-align: center; font-size: 45px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. INTELIGENTNA LABORATORIJA (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>NEXUS LABS</h2>", unsafe_allow_html=True)
    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.markdown("### 👁️ NEXUS OČI")
    uploaded_file = st.file_uploader("Ubaci sliku za analizu...", type=["jpg", "png", "jpeg"])
    st.divider()
    st.markdown("### 🎨 CREATOR HUB")
    if st.button("🖼️ GENERIŠI KONCEPT SLIKE"):
        st.toast("Nexus sprema umetničku viziju...")
    st.divider()
    st.markdown("### 📽️ VIDEO STUDIO")
    st.write("Status: *Spreman za Video API*")

# --- 6. INTERFEJS ---
st.markdown("<h1>NEXUS v4.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff; font-weight: bold;'>BALKAN VOX & ULTRA-SVEST ONLINE 💎</center>", unsafe_allow_html=True)

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            # VOX DUGME SA BALKAN & GLOBAL DETECTION
            if st.button(f"🔊 NEXUS VOX", key=f"v_{i}"):
                txt = m["content"].replace("'", "").replace("\n", " ")
                st.components.v1.html(f"""
                    <script>
                    var m = new SpeechSynthesisUtterance('{txt}');
                    var text = '{txt}'.toLowerCase();
                    // Balkan Detection (sr, hr, bs, cg)
                    var balkan = /[čćšđž]/i.test(text) || text.includes(' i ') || text.includes(' da ') || text.includes(' bi ');
                    
                    if (balkan) {{
                        m.lang = 'sr-RS';
                    }} else if (/[äöüß]/i.test(text)) {{
                        m.lang = 'de-DE';
                    } else if (/[éàèù]/i.test(text)) {{
                        m.lang = 'fr-FR';
                    } else {{
                        m.lang = 'en-US';
                    }}
                    m.rate = 0.95;
                    window.parent.speechSynthesis.speak(m);
                    </script>
                """, height=0)

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

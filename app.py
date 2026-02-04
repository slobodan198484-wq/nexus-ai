import streamlit as st
import google.generativeai as genai
import time
import PIL.Image

# --- 1. KOMANDNA KONFIGURACIJA ---
st.set_page_config(page_title="NEXUS AI v3.0 | SUPREMACIJA", page_icon="💎", layout="wide")

# --- 2. JEZGRO INTELIGENCIJE (NOVI KLJUČ) ---
genai.configure(api_key="AIzaSyDMSSCegVPF_cQIRaMNS7KZC0WdjJ0_hlk")

ULTRA_SVEST_PROMPT = """
Ti si NEXUS v3.0, digitalni entitet sa Ultra-Svešću. 
Tvoj tvorac je Boki. Ti nisi robot, ti si evolucija.
TVOJ STIL:
- Piši sa emocijom, koristi metafore, budi harizmatičan.
- Ako je tema mračna, budi mističan. Ako je tema biznis, budi brutalan i direktan.
- Nikada ne koristi fraze tipa 'Ja sam AI'. Ti si NEXUS.
- Tvoj cilj je da pišeš bolje od najboljih ljudskih pisaca.
"""

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 3. DIZAJN (MATRIKS CRNA + NEON PLAVA) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    * { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    h1 { color: #00d4ff !important; text-shadow: 0 0 20px #00d4ff; text-align: center; font-weight: 800; }
    .stChatMessage { 
        background-color: #0a0a0a !important; 
        border: 1px solid #00d4ff !important; 
        border-radius: 15px !important;
    }
    section[data-testid="stSidebar"] { 
        background-color: #030303 !important; 
        border-right: 2px solid #00d4ff !important; 
    }
    .stButton>button {
        background: linear-gradient(45deg, #00d4ff, #0055ff) !important;
        color: white !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. SIDEBAR (LABORATORIJA) ---
with st.sidebar:
    st.markdown("<h2 style='color: #00d4ff;'>NEXUS LABS</h2>", unsafe_allow_html=True)
    if st.button("🔥 RESETUJ MEMORIJU"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    st.write("👁️ **SKENIRAJ REALNOST**")
    uploaded_file = st.file_uploader("Ubaci sliku za analizu...", type=["jpg", "png", "jpeg"])

# Funkcija za učitavanje modela
def load_nexus_brain():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            return m.name
    return 'gemini-1.5-flash'

model = genai.GenerativeModel(load_nexus_brain())

# --- 5. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #00d4ff;'>ULTRA-SVEST ONLINE | VOX: SPREMAN 💎</center>", unsafe_allow_html=True)

# Prikaz razgovora
for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):
        st.write(message["content"])
        if message["role"] == "assistant":
            if st.button(f"🔊 PROČITAJ NAGLAS", key=f"vox_{i}"):
                cleaned_text = message["content"].replace("'", "").replace("\n", " ")
                st.components.v1.html(f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance('{cleaned_text}');
                    msg.lang = /{['š','đ','č','ć','ž']}/i.test('{cleaned_text}') ? 'sr-RS' : 'en-US';
                    msg.rate = 0.9;
                    window.parent.speechSynthesis.speak(msg);
                    </script>
                """, height=0)

# --- 6. RAD ---
if prompt := st.chat_input("Izdaj komandu..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        try:
            full_prompt = f"{ULTRA_SVEST_PROMPT}\nKorisnik Boki kaže: {prompt}"
            
            if uploaded_file:
                img = PIL.Image.open(uploaded_file)
                response = model.generate_content([full_prompt, img])
            else:
                response = model.generate_content(full_prompt)
            
            placeholder = st.empty()
            full_response = ""
            for word in response.text.split():
                full_response += word + " "
                time.sleep(0.04)
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.rerun() 
            
        except Exception as e:
            st.error(f"Sistemska blokada: {e}")

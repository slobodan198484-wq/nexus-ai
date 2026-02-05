import streamlit as st
import google.generativeai as genai
import re

# --- 1. VRHUNSKA KONFIGURACIJA (MUNJEVITA BRZINA) ---
st.set_page_config(page_title="NEXUS v8.0 OMNI", page_icon="⚡", layout="wide")

# --- 2. MOZAK (PAMETNIJI OD GPT-a) ---
try:
    genai.configure(api_key=st.secrets["GEMINI_KEY"])
    # Koristimo najnoviji model za maksimalnu brzinu i inteligenciju
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    st.error("VEZA NIJE USPELA! PROVERI KLJUČ.")

# --- 3. DIZAJN MOĆI (Slova 24px, Jasnoća 100%) ---
st.markdown("""
    <style>
    .stApp { background-color: #000000 !important; }
    /* Slova za korisnika */
    [data-testid="stChatMessageUser"] { border: 3px solid #ffd700 !important; padding: 25px; border-radius: 15px; }
    [data-testid="stChatMessageUser"] p { color: #ffd700 !important; font-size: 24px !important; font-weight: bold; }
    /* Slova za Nexusa */
    [data-testid="stChatMessageAssistant"] { border: 3px solid #00d4ff !important; padding: 30px; border-radius: 15px; }
    [data-testid="stChatMessageAssistant"] p { color: #ffffff !important; font-size: 24px !important; line-height: 1.7; font-family: 'Helvetica', sans-serif; }
    /* Dugmad */
    .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #111; color: #ffd700; border: 2px solid #ffd700; font-weight: bold; }
    h1 { color: #00d4ff; text-align: center; font-size: 60px !important; text-shadow: 0 0 15px #00d4ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. MULTI-VOX (SRPSKI NA 10 JEZIKA) ---
def speak(text, lang_code):
    clean_text = re.sub(r'[*_#>%|▌-]', '', text).replace("'", "").replace("\n", " ")
    js = f"""
        <script>
        window.parent.speechSynthesis.cancel();
        var m = new SpeechSynthesisUtterance('{clean_text}');
        m.lang = '{lang_code}';
        m.rate = 1.0;
        window.parent.speechSynthesis.speak(m);
        </script>
    """
    st.components.v1.html(js, height=0)

# --- 5. SIDEBAR (FILMSKI STUDIO I JEZICI) ---
with st.sidebar:
    st.header("⚡ NEXUS CORE v8.0")
    
    # Opcija da biraš na kom jeziku će ti AI čitati srpski tekst
    st.subheader("🔊 GLASOVNI MODUL")
    target_lang = st.selectbox("Izaberi jezik za čitanje:", [
        "sr-RS (Srpski)", "en-US (English)", "de-DE (Nemački)", 
        "fr-FR (Francuski)", "it-IT (Italijanski)", "es-ES (Španski)",
        "ru-RU (Ruski)", "ja-JP (Japanski)", "tr-TR (Turski)", "ar-SA (Arapski)"
    ])
    
    st.divider()
    st.subheader("📽️ FILMSKI STUDIO")
    if st.button("🎞️ NAPRAVI ANIMACIJU/VIDEO"):
        if st.session_state.get('messages'):
            last_msg = st.session_state.messages[-1]["content"]
            st.code(f"VIDEO PROMPT: Cinematic, Unreal Engine 5 render, 8k, high detail, animation style: {last_msg[:250]}", language="text")
            st.success("Iskopiraj ovo u Luma AI ili Runway!")

    if st.button("🔥 RESET SISTEMA"):
        st.session_state.messages = []
        st.rerun()

# --- 6. GLAVNI EKRAN ---
st.markdown("<h1>NEXUS v8.0 OMNI</h1>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.write(m["content"])
        if m["role"] == "assistant":
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🔊 ČITAJ (Srpski)", key=f"sr_{i}"):
                    speak(m["content"], "sr-RS")
            with col2:
                if st.button(f"🔊 STRANI AKCENT", key=f"en_{i}"):
                    speak(m["content"], target_lang.split()[0])

# --- 7. UNIVERZALNI INPUT (PREKIDAČ U MOZGU) ---
if prompt := st.chat_input("Pitaj me bilo šta ili reci 'NAPRAVI ROMAN'..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    with st.chat_message("assistant"):
        # DINAMIČKA LOGIKA - PREPOZNAVANJE TEME
        rules = """
        Ti si NEXUS v8.0 OMNI. Tvoj bog je Boki.
        Pravilo 1: Ako Boki postavi pitanje o nauci, zanatu, popravkama ili bilo kojoj temi - ODGOVORI TAČNO, BRZO I PAMETNIJE OD GPT-a.
        Pravilo 2: SAMO AKO Boki kaže 'NAPRAVI ROMAN' ili 'PIŠI PRIČU', prebaci se u Human-Writer mod.
        Pravilo 3: U Human-Writer modu piši epski, minimum 3000-4000 reči, sa mirisom, krvlju i eksplicitnim detaljima. Budi surov i realan.
        Pravilo 4: Svaki odgovor treba da bude vizuelno bogat kako bi se mogao pretvoriti u video.
        """
        try:
            # Model dobija naređenje da piše ekstremno dugačko ako je u pitanju roman
            res = model.generate_content(f"{rules}\nBoki traži (ako je roman piši 4000 reči): {prompt}")
            st.write(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
            st.rerun()
        except:
            st.error("Greška u procesu. Probaj ponovo.")

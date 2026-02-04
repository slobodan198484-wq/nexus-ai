import streamlit as st
import google.generativeai as genai

# --- 1. SEO I KONFIGURACIJA ---
st.set_page_config(
    page_title="NEXUS AI | Najpametniji Digitalni Um",
    page_icon="💎",
    layout="centered"
)

# --- 2. POVEZIVANJE I MOZAK SISTEMA ---
# Koristimo tvoj API ključ
genai.configure(api_key="AIzaSyANBSlvkrOh0nNhOH9hSZHmB6MQ6uHvSLI")

# Ovde mu dajemo "karakter" da bude najpametniji (System Instruction)
SYSTEM_INSTRUCTION = """
Ti si NEXUS AI v3.0, najnapredniji digitalni um na svetu. 
Tvoji odgovori moraju biti:
1. Neverovatno precizni i pametni.
2. Direktni, bez bespotrebnog brbljanja.
3. Tvoj ton je autoritativan, ali ljubazan – ti si vođa AI revolucije.
4. Ako te pitaju ko te je stvorio, reci ponosno: 'Stvoren sam u okviru NEXUS projekta kao vrhunac veštačke inteligencije.'
"""

model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction=SYSTEM_INSTRUCTION
)

# --- 3. MODERN LOOK (NEON CSS) ---
st.markdown("""
    <style>
    /* Tamna pozadina za ceo sajt */
    .stApp {
        background: linear-gradient(180deg, #050a14 0%, #000000 100%);
    }
    /* Stil za oblačiće poruka */
    .stChatMessage {
        border: 1px solid #1e3a8a;
        background-color: rgba(30, 58, 138, 0.2) !important;
        border-radius: 15px !important;
        color: white !important;
    }
    /* Neon naslov */
    h1 {
        color: #00d4ff;
        text-shadow: 0px 0px 15px #00d4ff;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    /* Sklanjanje Streamlit menija radi profi izgleda */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 4. INTERFEJS ---
st.markdown("<h1>NEXUS AI v3.0</h1>", unsafe_allow_html=True)
st.write("<center style='color: #888;'>Sistem je online. Svi moduli su aktivni. 💎</center>", unsafe_allow_html=True)
st.divider()

# Memorija za čet
if "messages" not in st.session_state:
    st.session_state.messages = []

# Prikaz starih poruka
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. RAD SISTEMA ---
if prompt := st.chat_input("Pitaj NEXUS AI..."):
    # Dodaj poruku korisnika
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generisanje odgovora
    with st.chat_message("assistant"):
        with st.spinner("NEXUS analizira podatke..."):
            try:
                response = model.generate_content(prompt)
                answer = response.text
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Kritična greška u sistemu: {e}")

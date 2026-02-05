# --- 2. PAMETNI MOZAK (AUTO-DETEKCIJA MODELA) ---
try:
    api_key = st.secrets["GEMINI_KEY"]
    genai.configure(api_key=api_key)
    
    # Nexus sada sam traži koji model radi na tvom serveru
    def find_working_model():
        for model_name in ['models/gemini-1.5-flash-latest', 'models/gemini-1.5-flash', 'gemini-pro']:
            try:
                m = genai.GenerativeModel(model_name)
                # Testni poziv da potvrdimo život
                m.generate_content("test", generation_config={"max_output_tokens": 1})
                return model_name
            except:
                continue
        return 'gemini-pro' # Backup opcija

    working_model = find_working_model()
    
    # Podešavanja za cenzuru i brutalnost pisanja
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name=working_model,
        safety_settings=safety_settings
    )
    st.sidebar.success(f"NEXUS AKTIVAN: {working_model}")
except Exception as e:
    st.error(f"SISTEMSKA GREŠKA: {e}")

import streamlit as st
import datetime
from anthropic import Anthropic

# Initialize Anthropic client
anthropic = Anthropic(api_key="YOUR_API_KEY_HERE")

# Define themes and their parameters
themes = {
    "Undangan ala BUMN": ["nama_penerima", "acara", "tanggal", "waktu", "tempat"],
    "Izin Sakit": ["nama_pengirim", "alasan", "tanggal"],
    "Izin WFH": ["nama_pengirim", "alasan", "tanggal"],
}

# Function to generate message using Claude
def generate_message(theme, params):
    prompt = f"""Buatlah template pesan WhatsApp dalam Bahasa Indonesia untuk tema '{theme}' dengan parameter berikut:
    {', '.join([f'{k}: {v}' for k, v in params.items()])}
    
    Pesan harus sopan, formal, dan sesuai dengan budaya kerja di Indonesia."""

    response = anthropic.completions.create(
        model="claude-3-opus-20240229",
        prompt=prompt,
        max_tokens_to_sample=300,
    )
    return response.completion

# Streamlit app
st.title("Generator Template Pesan WhatsApp")

# Theme selection
selected_theme = st.selectbox("Pilih tema pesan:", list(themes.keys()))

# Parameter input
st.subheader("Masukkan parameter:")
params = {}
for param in themes[selected_theme]:
    if "tanggal" in param:
        params[param] = st.date_input(param.capitalize().replace("_", " "))
    elif "waktu" in param:
        params[param] = st.time_input(param.capitalize().replace("_", " "))
    else:
        params[param] = st.text_input(param.capitalize().replace("_", " "))

# Generate message
if st.button("Buat Pesan"):
    message = generate_message(selected_theme, params)
    
    # Display mock WhatsApp screen
    st.subheader("Pratinjau Pesan WhatsApp:")
    whatsapp_html = """
    <style>
        .whatsapp-container {{
            max-width: 400px;
            margin: 0 auto;
            border: 1px solid #ddd;
            border-radius: 10px;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}
        .whatsapp-header {{
            background-color: #075e54;
            color: white;
            padding: 10px;
        }}
        .whatsapp-body {{
            background-color: #e5ddd5;
            padding: 20px;
        }}
        .message-bubble {{
            background-color: white;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }}
    </style>
    <div class="whatsapp-container">
        <div class="whatsapp-header">
            <h3>WhatsApp</h3>
        </div>
        <div class="whatsapp-body">
            <div class="message-bubble">
                {0}
            </div>
        </div>
    </div>
    """.format(message.replace('\n', '<br>'))
    st.components.v1.html(whatsapp_html, height=400)

st.markdown("---")
st.caption("Dibuat dengan Streamlit dan Claude AI")
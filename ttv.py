# Install whisper and streamlit if you haven't
# pip install openai-whisper streamlit

import whisper
import streamlit as st
import time
import io

def transcribe_audio(audio_path, progress_callback=None):
    try:
        model = whisper.load_model("small")
        if progress_callback:
            progress_callback(50)
        result = model.transcribe(audio_path, language="es")
        if progress_callback:
            progress_callback(100)
        return result['text']
    except Exception as e:
        return f"Error transcribing audio: {e}"

def main():
    st.title("Transcriptor de Audio en Español")
    st.write("Subí un archivo de audio para transcribirlo.")

    uploaded_file = st.file_uploader("Elegí un archivo de audio", type=["mp3", "wav", "m4a", "ogg"])

    if uploaded_file is not None:
        with open("temp_audio_file", "wb") as f:
            f.write(uploaded_file.getbuffer())

        progress_bar = st.progress(0)

        def update_progress(value):
            progress_bar.progress(value)

        with st.spinner('Transcribiendo...'):
            transcription = transcribe_audio("temp_audio_file", progress_callback=update_progress)

        st.subheader("Transcripción:")
        st.text_area("Texto transcripto:", transcription, height=300)

        # Opción para descargar el texto
        text_bytes = io.BytesIO(transcription.encode('utf-8'))
        st.download_button(
            label="Descargar transcripción como TXT",
            data=text_bytes,
            file_name="transcripcion.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()
import streamlit as st
import sounddevice as sd
import scipy.io.wavfile as wav
from transformers import pipeline
from genAi import generate_content

# Initialize the whisper pipeline for automatic speech recognition
whisper = pipeline('automatic-speech-recognition', model='openai/whisper-medium')

def save_audio_to_file(filename, audio_data, sample_rate):
    wav.write(filename, sample_rate, audio_data)

def main():
    st.title("Speak with UVA")

    # Button to start recording
    record_button = st.button("Start speaking")

    if record_button:
        st.info("Lisening...")

        # Record audio
        duration = 5  # Recording duration (in seconds)
        sample_rate = 16000  # Sample rate
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()

        st.success("Recording stopped.")

        # Specify the path to save the audio file
        save_path = "recorded_audio.wav"

        # Save audio to file
        save_audio_to_file(save_path, recording, sample_rate)

        st.audio(save_path, format='audio/wav')

        # Perform automatic speech recognition
        text = whisper(save_path)
        st.write(text['text'])
        st.success("UVA reply:")
        prompttext = generate_content(text)
        st.write(prompttext)

if __name__ == "__main__":
    main()
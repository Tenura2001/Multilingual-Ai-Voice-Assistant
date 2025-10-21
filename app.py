import streamlit as st
from src.helper import voice_input, llm_model_object, text_to_speech

st.set_page_config(page_title="Multilingual AI Assistant 🤖")

def main():
    st.title("Multilingual AI Assistant 🤖")
    
    # Choose language
    language = st.selectbox("Choose language", ["English", "Sinhala"])
    lang_code = "en-US" if language == "English" else "si-LK"
    tts_lang = "en" if language == "English" else "si"
    
    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            user_text = voice_input(language=lang_code)
        
        if user_text:
            response = llm_model_object(user_text)
            text_to_speech(response, language=tts_lang)
            
            # Display response and audio
            st.text_area(label="Response:", value=response, height=350)
            
            with open("speech.mp3", "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes)
                st.download_button(
                    label="Download Speech",
                    data=audio_bytes,
                    file_name="speech.mp3",
                    mime="audio/mp3"
                )

if __name__ == "__main__":
    main()

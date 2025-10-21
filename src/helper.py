import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import playsound  # to play the generated speech

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# Configure Generative AI
genai.configure(api_key=GOOGLE_API_KEY)

# Choose a supported model
MODEL_NAME = "gemini-2.5-flash"  # replace gemini model with available model

def voice_input(language="en"):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio, language=language)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service: {e}")

def text_to_speech(text, language="en"):
    # gTTS supports Sinhala: use lang="si"
    tts = gTTS(text=text, lang=language)
    tts.save("speech.mp3")
    playsound.playsound("speech.mp3")  # play the speech

def llm_model_object(user_text):
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(user_text)
    return response.text

def main():
    # Choose input language
    choice = input("Choose language (en for English / si for Sinhala): ").strip().lower()
    lang_code = "si" if choice == "si" else "en"

    user_text = voice_input(language=lang_code)
    if user_text:
        response_text = llm_model_object(user_text)
        print("Assistant:", response_text)
        text_to_speech(response_text, language=lang_code)

if __name__ == "__main__":
    main()

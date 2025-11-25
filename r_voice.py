import speech_recognition as sr
import pygame
import struct
from google import genai
from google.genai import types

# --- CONFIGURATION ---
API_KEY ="API HERE" 

# 1. Model for Thinking (Generating the text response)
TEXT_MODEL_ID = "gemini-2.5-flash"

# 2. Model for Speaking (Converting that text to audio)
#    We use the specific TTS model here as requested.
TTS_MODEL_ID = "gemini-2.5-flash-preview-tts"

SYSTEM_INSTRUCTION = """
You are a professional Sinhala radio announcer. 
Answer in Sinhala. Keep it natural and engaging.
"""

# Initialize Client
client = genai.Client(api_key=API_KEY)
pygame.mixer.init()

# --- HELPER: WAV Header Construction ---
def parse_audio_mime_type(mime_type: str) -> dict[str, int | None]:
    bits_per_sample = 16
    rate = 24000
    parts = mime_type.split(";")
    for param in parts:
        param = param.strip()
        if param.lower().startswith("rate="):
            try:
                rate = int(param.split("=", 1)[1])
            except (ValueError, IndexError):
                pass
        elif param.startswith("audio/L"):
            try:
                bits_per_sample = int(param.split("L", 1)[1])
            except (ValueError, IndexError):
                pass
    return {"bits_per_sample": bits_per_sample, "rate": rate}

def convert_to_wav(audio_data: bytes, mime_type: str) -> bytes:
    parameters = parse_audio_mime_type(mime_type)
    bits_per_sample = parameters["bits_per_sample"]
    sample_rate = parameters["rate"]
    num_channels = 1
    data_size = len(audio_data)
    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    chunk_size = 36 + data_size

    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", chunk_size, b"WAVE", b"fmt ", 16, 1, num_channels,
        sample_rate, byte_rate, block_align, bits_per_sample, b"data", data_size
    )
    return header + audio_data

# --- STEP 1: GENERATE TEXT (Brain) ---
def get_ai_text(user_input):
    """Generates the text response using the standard model."""
    print("🧠 AI is thinking...")
    try:
        response = client.models.generate_content(
            model=TEXT_MODEL_ID,
            contents=f"{SYSTEM_INSTRUCTION}\nUser: {user_input}\nAssistant:",
            config=types.GenerateContentConfig(
                response_modalities=["TEXT"], 
            )
        )
        return response.text
    except Exception as e:
        print(f"Text Gen Error: {e}")
        return None

# --- STEP 2: GENERATE AUDIO (Mouth) ---
def speak_text(text_to_read):
    """Uses gemini-2.5-flash-preview-tts to read the text aloud."""
    print(f"🗣️ Synthesizing Audio using {TTS_MODEL_ID}...")
    
    try:
        # We pass the text directly as the content
        response = client.models.generate_content(
            model=TTS_MODEL_ID,
            contents=text_to_read,
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Puck" # Options: Zephyr, Puck, Kore, Fenrir
                        )
                    )
                ),
            )
        )

        # Process the audio bytes
        if response.candidates and response.candidates[0].content.parts:
            part = response.candidates[0].content.parts[0]
            if part.inline_data:
                # Convert raw PCM to WAV
                wav_data = convert_to_wav(part.inline_data.data, part.inline_data.mime_type)
                
                # Save temp file
                filename = "tts_output.wav"
                with open(filename, "wb") as f:
                    f.write(wav_data)
                
                # Play
                print("▶️ Playing Audio...")
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
    except Exception as e:
        print(f"TTS Error: {e}")

# --- MAIN LOOP ---
def main():
    r = sr.Recognizer()
    
    print(f"--- Started. TTS Model: {TTS_MODEL_ID} ---")
    
    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("\n🎧 Listening...")
            
            try:
                audio = r.listen(source, timeout=5)
                # Try converting speech to text
                try:
                    user_text = r.recognize_google(audio, language="si-LK")
                except:
                    user_text = r.recognize_google(audio, language="en-US")
                
                print(f"User: {user_text}")

                # 1. Get Text Answer
                ai_response = get_ai_text(user_text)
                
                if ai_response:
                    print(f"AI Text: {ai_response}")
                    # 2. Convert to Speech using the special model
                    speak_text(ai_response)

            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                print("Could not understand audio.")
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()

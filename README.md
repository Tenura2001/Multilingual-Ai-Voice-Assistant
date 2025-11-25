# Sinhala AI Radio Announcer

A real-time voice assistant capable of conversational interaction in Sinhala. This project leverages Google's latest **Gemini 2.5 Flash** models for both text generation (thinking) and text-to-speech (speaking), creating a natural-sounding "Radio Announcer" persona.

## Key Features

* **Dual-Language Input:** Automatically detects and listens to voice commands in **Sinhala (`si-LK`)** with a fallback to **English (`en-US`)**.
* **Gemini 2.5 Intelligence:** Uses `gemini-2.5-flash` for low-latency, high-quality conversational logic.
* **Next-Gen TTS:** Implements `gemini-2.5-flash-preview-tts` for high-fidelity speech synthesis.
* **Custom Audio Pipeline:** Handles raw PCM audio streams from the Gemini API, converts them to WAV format using raw byte manipulation (`struct`), and plays them via `pygame`.
* **Persona:** System instructions tuned to mimic a professional Sinhala radio announcer.

## Tech Stack

* **Language:** Python 3.10+
* **AI Models:** Google GenAI SDK (`google-genai`)
* **Input:** SpeechRecognition
* **Output:** Pygame (Mixer)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
    cd your-repo-name
    ```

2.  **Install dependencies:**
    ```bash
    pip install google-genai speechrecognition pygame pyaudio
    ```
    *(Note: `pyaudio` is required for microphone access. On Linux, you may need to install `portaudio19-dev` first).*

## ⚙️ Configuration

1.  Open the `main.py` file.
2.  Locate the configuration section at the top:
    ```python
    # --- CONFIGURATION ---
    API_KEY = "PASTE_YOUR_GOOGLE_API_KEY_HERE"
    ```
3.  Replace the placeholder with your valid Google Gemini API Key.

## Usage

Run the script to start the announcer:

```bash
python main.py

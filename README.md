# VocaLlama

This project implements a **Speech-to-Speech** multi-modular agent designed to enable simple vocal conversations while providing great flexibility to adapt its modules based on user needs.

## Main Features

1. **Voice Activity Detection:**
   - Uses an audio volume detector to check for activity before processing.

2. **Audio Transcription:**
   - Converts audio into text using the **Whisper** API.

3. **Text Generation:**
   - Sends the transcribed text to **Llama 3** via the **Ollama** API, which generates a response.

4. **Voice Synthesis:**
   - Converts the generated text into audio using **gTTS (Google Text-to-Speech)**.

5. **Hotword Detection:**
   - Integrates **Porcupine** to activate the system through predefined keywords.

6. **Modularity:**
   - A modular architecture allows for easy addition, modification, or removal of components to meet various objectives.

---

## Installation and Configuration

### Prerequisites

- **Python 3.9 or higher**
- Porcupine account (required for the hotword system)
- Ollama installed on your machine

### Installation Steps

1. Clone this repository:  
   ```bash
   git clone https://github.com/Sushiman31/VocaLlama.git
   cd VocaLlama
   ```

2. Install the Python dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Set up **Ollama**:
   - Download Ollama from their official website.
   - Configure the API to allow access from your machine.

4. Set up **Porcupine**:
   - Create an account on the **Porcupine** website.
   - Download your custom keywords and configure their paths in the project.

---

## Usage

1. Start the agent:
   ```bash
   python main.py
   ```

2. Speak to the agent using the configured keyword. The agent will detect activity, generate a response, and reply to you vocally.

---

## Current Limitations

- **Latency:** The system currently has significant latency due to multiple APIs being used. Process optimization is needed.
- **External Dependencies:** Requires multiple APIs and accounts to function (Whisper, Ollama, Porcupine, gTTS).

---

## Highlights

- **Flexibility:** Its modularity allows you to easily customize the agent by adding new models or replacing existing modules.
- **Ease of Use:** Module integration is simple and straightforward.

---

## Future Improvements

- Latency optimization.
- Integration of additional modules (e.g., emotion recognition or improved audio quality).

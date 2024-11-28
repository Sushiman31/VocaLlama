import whisper
import torch
import shared_data
import os

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Current device : {device}")

# Modify the size of the loaded model if necessary
model = whisper.load_model("medium", device=device)
audio_path=os.path.join(shared_data.PROJECT_DIR, "input", "audio_output.wav")
def transcript():
    # Transcribe an audio file by specifying the language (e.g. French)
    result = model.transcribe(audio_path, language="en")

    return result["text"]

import whisper
import torch
import shared_data
import os

# Vérifier si CUDA est disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Utilisation de l'appareil : {device}")

# Charger un modèle plus petit pour accélérer la transcription
model = whisper.load_model("medium", device=device)
audio_path=os.path.join(shared_data.PROJECT_DIR, "input", "audio_output.wav")
def transcript():
    # Transcrire un fichier audio en spécifiant la langue (par exemple, français)
    result = model.transcribe(audio_path, language="en")

    # Afficher la transcription
    return result["text"]

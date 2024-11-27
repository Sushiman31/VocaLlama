import whisper
import torch

# Vérifier si CUDA est disponible
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Utilisation de l'appareil : {device}")

# Charger un modèle plus petit pour accélérer la transcription
model = whisper.load_model("medium", device=device)

def transcript():
    # Transcrire un fichier audio en spécifiant la langue (par exemple, français)
    result = model.transcribe("C:\\Users\\tbald\\Documents\\Doctorat\\Projet\\CloneGit\\Test_entre\\VocaLlama\\input\\audio_output.wav", language="en")

    # Afficher la transcription
    return result["text"]

import ollama
from pathlib import Path
from openai import OpenAI
from pathlib import Path
import os

from gtts import gTTS
import io
import simpleaudio as sa  # Bibliothèque pour lire l'audio depuis la mémoire
import wave
from pydub import AudioSegment
from pydub.playback import play

def generate_answer(transcript):
    full_transcript=[{"role":"user","content":transcript}]
    
    ollama_stream=ollama.chat(
        model="llama3:8b",
        messages=full_transcript,
        stream=True
    )

    print("llama3:", end="\r\n")

    text_buffer=""
    full_text=""
    for chunk in ollama_stream:
        text_buffer +=chunk['message']['content']
        if text_buffer.endswith('.'):
            print(text_buffer,end="\n",flush=True)
            full_text+=text_buffer
            text_buffer=""
    if text_buffer:
        print(text_buffer,end="\n",flush=True)
        full_text+=text_buffer
    
    full_transcript.append({"role":"assistant","content":full_text})
    
    myobj = gTTS(text=full_text, lang="en", slow=False)

    mp3_buffer = io.BytesIO()
    myobj.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)  # Revenir au début du flux

    # Conversion de MP3 en WAV avec pydub
    audio = AudioSegment.from_file(mp3_buffer, format="mp3")
    
    # Lecture directe du fichier audio avec pydub
    play(audio)
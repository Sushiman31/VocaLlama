import ollama
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
import queue
import threading

audio_queue=queue.Queue()

def audio_player():
    while True:
        audio=audio_queue.get()
        if audio is None:
            break
        play(audio)
        audio_queue.task_done()
        

def generate_tts(text):
    myobj = gTTS(text=text, lang="en", slow=False)

    mp3_buffer = io.BytesIO()
    myobj.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)  

    # MP3 to Wav
    audio = AudioSegment.from_file(mp3_buffer, format="mp3") 
    audio_queue.put(audio)      


def generate_answer(transcript):
    player_thread=threading.Thread(target=audio_player)
    player_thread.start()
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
        
            generate_tts(text_buffer)

            full_text+=text_buffer
            text_buffer=""
    if text_buffer:
        print(text_buffer,end="\n",flush=True)
        generate_tts(text_buffer)
        full_text+=text_buffer
    
    full_transcript.append({"role":"assistant","content":full_text})

    audio_queue.join()
    # Ajouter un élément pour arrêter le thread
    audio_queue.put(None)
    player_thread.join()
    
    
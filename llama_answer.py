import ollama
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play

def generate_tts(text):
    myobj = gTTS(text=text, lang="en", slow=False)

    mp3_buffer = io.BytesIO()
    myobj.write_to_fp(mp3_buffer)
    mp3_buffer.seek(0)  

    # MP3 to Wav
    audio = AudioSegment.from_file(mp3_buffer, format="mp3")       
    play(audio)

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
        
            generate_tts(text_buffer)

            full_text+=text_buffer
            text_buffer=""
    if text_buffer:
        print(text_buffer,end="\n",flush=True)
        generate_tts(text_buffer)
        full_text+=text_buffer
    
    full_transcript.append({"role":"assistant","content":full_text})
    
    
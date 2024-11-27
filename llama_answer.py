import ollama

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


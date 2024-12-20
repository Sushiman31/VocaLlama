import struct
import pyaudio
import pvporcupine
import sys
import threading
import tkinter as tk
import os
import time 

import shared_data
from input_user import open_mic,audio_level
# from input_user import open_camera
from speech2text import transcript
from llama_answer import generate_answer

class Assistant:
    """This class defines the main voice-activated assistant .Upon detecting a specific 
    wake word, it activates additional functionalities like camera and microphone input."""
    
    def __init__(self):
        self.root=tk.Tk()
        self.label=tk.Label(text="🤖",font=("Arial",120,"bold"))
        self.label.pack()
        
        threading.Thread(target=self.run_assistant).start()
        self.root.mainloop()
    def run_assistant(self):
        paud=pyaudio.PyAudio()

        hot_word_language_path=os.path.join(shared_data.PROJECT_DIR, "porcupine", "salut-robot_fr_windows_v3_0_0.ppn")
        hot_word_parameters_path=os.path.join(shared_data.PROJECT_DIR, "porcupine", "porcupine_params_fr.pv")
        if not os.path.exists(hot_word_language_path):
            print("Error : porcupine file doesn't exist")
        try:
            print("You can talk")
            porcupine=pvporcupine.create(access_key="PUT YOUR POCUPINE KEY HERE",keyword_paths=[hot_word_language_path],
                                         model_path=hot_word_parameters_path)
            
            audio_stream=paud.open(rate=porcupine.sample_rate,channels=shared_data.CHANNEL,format=shared_data.SAMPLE_FORMAT,input=True,frames_per_buffer=porcupine.frame_length)
            while True:
                keyword=audio_stream.read(porcupine.frame_length)
                keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)
                keyword_index=porcupine.process(keyword)
                if keyword_index>=0 or shared_data.RUNNING_PROCESS : 
                    if not shared_data.RUNNING_PROCESS:
                        shared_data.RUNNING_PROCESS=True
                    
                    print("hotword detected")
                    self.label.config(fg="red")
                    shared_data.RECORD_FLAG.set()

                    # video_thread=threading.Thread(target=open_camera)
                    audio_thread=threading.Thread(target=open_mic,args=(audio_stream,))
                    level_thread=threading.Thread(target=audio_level,args=(audio_stream,))

                    # video_thread.start()
                    audio_thread.start()
                    level_thread.start()

                    # video_thread.join()
                    audio_thread.join()
                    level_thread.join()
                    
                    if shared_data.RUNNING_PROCESS:
                        self.label.config(fg="green")
                        sentence=transcript()
                        print(f"\nUser \n: {sentence}", end="\r\n")
                        generate_answer(sentence)
                        time.sleep(3)
                        
                    self.label.config(fg="black")


        finally:
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if paud is not None:
                paud.terminate()

Assistant()

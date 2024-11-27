import struct
import pyaudio
import pvporcupine
import sys
import threading
import tkinter as tk
import os
import time 

import shared_data
from input_user import open_camera,open_mic,audio_level
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
        # Affichez tous les périphériques audio disponibles
        # for i in range(paud.get_device_count()):
        #     info = paud.get_device_info_by_index(i)
        #     print(f"Device {i}: {info['name']}")        test  pour comprendre pourquoi pyaudio ne marchait pas
        # print("1hihih")
        if not os.path.exists("C:\\Users\\tbald\\Documents\\Doctorat\\Projet\\CloneGit\\Test_entre\\VocaLlama\\porcupine\\salut-robot_fr_linux_v3_0_0.ppn"):
            print("Erreur : le fichier modèle de Porcupine n'existe pas")
        # if not os.path.exists("/mnt/c/Users/tbald/Documents/Doctorat/Projet/CloneGit/Test_entre/porcupine/salut-robot_fr_linux_v3_0_0.ppn"):
        #     print("Erreur : le fichier modèle de Porcupine n'existe pas") 
        try:
            print("je t'écoute")
            porcupine=pvporcupine.create(access_key="Y6BUoOWzlEJ8y64iGM3YhLG2K9Xg8/CrNr1MX8tD64STsZdFoOlFaQ==",keyword_paths=['C:\\Users\\tbald\\Documents\\Doctorat\\Projet\\CloneGit\\Test_entre\\VocaLlama\\porcupine\\salut-robot_fr_windows_v3_0_0.ppn'],
                                         model_path='C:\\Users\\tbald\\Documents\\Doctorat\\Projet\\CloneGit\\Test_entre\\VocaLlama\\porcupine\\porcupine_params_fr.pv')
            # porcupine=pvporcupine.create(access_key="Y6BUoOWzlEJ8y64iGM3YhLG2K9Xg8/CrNr1MX8tD64STsZdFoOlFaQ==",keyword_paths=["/mnt/c/Users/tbald/Documents/Doctorat/Projet/CloneGit/Test_entre/porcupine/salut-robot_fr_linux_v3_0_0.ppn"],
            #                              model_path="/mnt/c/Users/tbald/Documents/Doctorat/Projet/CloneGit/Test_entre/porcupine/porcupine_params_fr.pv")
            
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

                    video_thread=threading.Thread(target=open_camera)
                    audio_thread=threading.Thread(target=open_mic,args=(audio_stream,))
                    level_thread=threading.Thread(target=audio_level,args=(audio_stream,))

                    video_thread.start()
                    audio_thread.start()
                    level_thread.start()

                    video_thread.join()
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

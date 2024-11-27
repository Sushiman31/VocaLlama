import struct
import pyaudio
import cv2
import sys
import threading
from threading import Event
import wave
import os
import time
import numpy as np

import shared_data


#audio
THRESHOLD_DB=15
SILENCE_DURATION=1
INPUT_FOLDER="input"
AUDIO_FILENAME="audio_output.wav"
VIDEO_FILENAME="output.avi"
FULL_PATH_AUDIO=os.path.join(INPUT_FOLDER,AUDIO_FILENAME)
FULL_PATH_VIDEO=os.path.join(INPUT_FOLDER,VIDEO_FILENAME)

if not os.path.exists(INPUT_FOLDER):
    os.makedirs(INPUT_FOLDER)


def open_camera():
    """
    This function initializes the camera, checks for its availability, and records video frames while the recording flag is active.
    It provides visual feedback to the user and handles any errors that might occur during the video capture process.
    
    """
    cap=cv2.VideoCapture(0)
    if not cap.isOpened():
            print("Impossible d'ouvrir la camera")
    else:
        print("enregistrement video en cours") 
        print("Appuyer sur q pour quitter")

        fourcc=cv2.VideoWriter_fourcc(*'XVID')
        out=cv2.VideoWriter(FULL_PATH_VIDEO,fourcc,20.0,(640,480))

        while shared_data.RECORD_FLAG.is_set():
            ret,frame=cap.read()
            if not ret:
                print("Erreur : impossible de lire")
                break
            
            out.write(frame)
            cv2.imshow('Camera',frame)

            if cv2.waitKey(1) & 0xFF==ord('q'):
                shared_data.RECORD_FLAG.clear()
                
        print("enregistrement video terminé")       
        cap.release()
        out.release()
        cv2.destroyAllWindows()

def audio_level(
        audio_stream):
    """
    Monitor and analyze the audio levels from the microphone input to detect silence or audio presence.

    Args:
        audio_stream: An audio stream object that continuously captures audio data from the microphone.
    
    """
    silence_start=None
    start_time=time.time()
    stock_db=[]

    while shared_data.RECORD_FLAG.is_set():
        data=audio_stream.read(1024)
        audio_data=np.frombuffer(data,dtype=np.int16)

        rms=np.sqrt(np.mean(audio_data**2)) if np.mean(audio_data**2)>0 else 0
        db=20*np.log10(rms) if rms>0 else -np.inf
        
        if time.time()-start_time<=2:
            if not stock_db:       
                if db<THRESHOLD_DB:
                    if silence_start is None:
                        silence_start=time.time()
                    elif time.time()-silence_start>=2*SILENCE_DURATION:
                        print("Silence trop long détecté")
                        shared_data.RECORD_FLAG.clear()
                else:
                    silence_start=None
                    stock_db.append(db)
            else:
                if db<THRESHOLD_DB:
                    if silence_start is None:
                        silence_start=time.time()
                    elif time.time()-silence_start>=SILENCE_DURATION:
                        print("Silence trop long détecté")
                        shared_data.RECORD_FLAG.clear()
                else:
                    silence_start=None
        else:
            if len(stock_db)==0:
                print("systeme exit mic")
                shared_data.RECORD_FLAG.clear()
                shared_data.RUNNING_PROCESS=False
                sys.exit()
            else:
                if db<THRESHOLD_DB:
                    if silence_start is None:
                        silence_start=time.time()
                    elif time.time()-silence_start>=SILENCE_DURATION:
                        print("Silence trop long détecté")
                        shared_data.RECORD_FLAG.clear()
                else:
                    silence_start=None
                    


def open_mic(
        audio_stream):
    """
    Save mic record on input folder to be used in the future by the architecture

    Args:
       audio_stream: An audio stream object that continuously captures audio data from the microphone.

    """
    frames=[]

    print("Enregistrement audio en cours")

    while shared_data.RECORD_FLAG.is_set():
        data=audio_stream.read(1024)
        frames.append(data)
    with wave.open(FULL_PATH_AUDIO,'wb') as wf:
        wf.setnchannels(shared_data.CHANNEL)
        wf.setsampwidth(pyaudio.get_sample_size(shared_data.SAMPLE_FORMAT))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

        print("enregistrement audio terminé")
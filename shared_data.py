import pyaudio
import threading
from threading import Event
import os

SAMPLE_FORMAT=pyaudio.paInt16
CHANNEL=1
RECORD_FLAG = Event()
RUNNING_PROCESS=False

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

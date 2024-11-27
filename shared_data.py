import pyaudio
import threading
from threading import Event

SAMPLE_FORMAT=pyaudio.paInt16
CHANNEL=1
RECORD_FLAG = Event()
RUNNING_PROCESS=False
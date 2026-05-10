from importlib.metadata import distribution, version

from enum import Enum
import signal
import sys
import time
import threading

import numpy as np
import sounddevice as sd
from pywhispercpp.model import Model

from .broker import Broker
from .modules.listener import Listener
from .modules.logger import Logger
from .modules.inference import Inference


SAMPLE_RATE = 16000
DURATION = 5  # seconds per chunk


class WhisperModel(Enum):
    TINY = "ggml-tiny.bin"
    BASE = "ggml-base.bin"
    SMALL = "ggml-small.bin"
    MEDIUM = "ggml-medium.bin"
    LARGE = "ggml-large.bin"


MODEL_NAME = WhisperModel.BASE
MODEL_PATH = f"models/{MODEL_NAME.value}"


stop_event = threading.Event()


def get_model():
    import os
    import urllib.request

    if not os.path.exists(MODEL_PATH):
        os.makedirs("models", exist_ok=True)

        print(f"Downloading model {MODEL_NAME.value}")

        urllib.request.urlretrieve(
            f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/{MODEL_NAME.value}",
            MODEL_PATH,
        )


def handle_stop(signum, frame):
    print("\nStopping")
    stop_event.set()


def package_name():
    return distribution(__package__).metadata["Name"]


def package_version():
    return version(__package__)


def main():
    print(f"Starting {package_name()}-v{package_version()} project ...")
    # get_model()
    # model = Model(MODEL_PATH, language="en")

    signal.signal(signal.SIGINT, handle_stop)  # Ctrl+C
    signal.signal(signal.SIGTERM, handle_stop)  # kill command

    # print("Listening... (Ctrl+C to stop)")
    # while running:
    #     audio = sd.rec(
    #         int(DURATION * SAMPLE_RATE),
    #         samplerate=SAMPLE_RATE,
    #         channels=1,
    #         dtype="float32",
    #     )

    #     sd.wait()

    #     if not running:
    #         break

    #     segments = model.transcribe(audio.flatten())
    #     for seg in segments:
    #         print(seg.text)

    broker = Broker()
    broker.start()

    listener = Listener("Microphone", broker)
    logger = Logger("Logger", broker)
    inference = Inference("Inference", broker)

    listener.start()
    logger.start()
    inference.start()

    stop_event.wait()

    listener.stop()
    logger.stop()
    broker.stop()

    print(f"Closing {package_name()}-v{package_version()} project ...")

    sys.exit(0)


# TODO:
# The transcription takes time andd the audio recording stays paused until its next initialization.
# I have to separate these two modules (audio recording / audio transcription ) in separate threads.

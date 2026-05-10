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
from .modules.microphone import Microphone
from .modules.logger import Logger
from .modules.inference import Inference


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

    signal.signal(signal.SIGINT, handle_stop)  # Ctrl+C
    signal.signal(signal.SIGTERM, handle_stop)  # kill command

    broker = Broker()
    broker.start()

    microphone = Microphone("Microphone Controller", broker)
    logger = Logger("Logger Controller", broker)
    inference = Inference("Inference Controller", broker)

    microphone.start()
    logger.start()
    inference.start()

    stop_event.wait()

    microphone.stop()
    logger.stop()
    broker.stop()

    print(f"Closing {package_name()}-v{package_version()} project ...")

    sys.exit(0)


# TODO:
# Use a voice activity detector to get the start and end of a speech

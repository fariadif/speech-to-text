from importlib.metadata import distribution, version

import signal
import sys
import threading


from .broker import Broker
from .modules.microphone import Microphone
from .modules.logger import Logger
from .modules.inference import Inference

stop_event = threading.Event()


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

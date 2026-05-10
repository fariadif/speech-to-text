from ..module import Module, Message
from enum import Enum

from pywhispercpp.model import Model


class WhisperModel(Enum):
    TINY = "ggml-tiny.bin"
    BASE = "ggml-base.bin"
    SMALL = "ggml-small.bin"
    MEDIUM = "ggml-medium.bin"
    LARGE = "ggml-large.bin"


class Inference(Module):
    MODEL_NAME = WhisperModel.BASE
    MODEL_PATH = f"models/{MODEL_NAME.value}"

    def _download_model(self):
        import os
        import urllib.request

        if not os.path.exists(self.MODEL_PATH):
            os.makedirs("models", exist_ok=True)

            print(f"Downloading model {self.MODEL_NAME.value}")

            urllib.request.urlretrieve(
                f"https://huggingface.co/ggerganov/whisper.cpp/resolve/main/{self.MODEL_NAME.value}",
                self.MODEL_PATH,
            )

    def on_start(self):
        self._download_model()
        self.subscribe("listener.audio")

        self._model = Model(self.MODEL_PATH, language="en")

    def on_message(self, msg: Message):
        print(
            f"[{self.name}] Received a message from {msg.topic} @ {msg.timestamp:.2f}"
        )

        if msg.topic == "listener.audio":
            audio = msg.payload["value"]
            segments = self._model.transcribe(audio.flatten())

            for seg in segments:
                print(f"[{self.name}] {msg.topic} @ {msg.timestamp:.2f} -> {seg.text}")

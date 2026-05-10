from ..module import Module, Message
from ..topics import Topic


class Logger(Module):
    def on_start(self):
        self.subscribe(Topic.INFERENCE_TRANSCRIPTION)

    def on_message(self, msg: Message):
        if msg.topic == Topic.INFERENCE_TRANSCRIPTION:
            text_segments = msg.payload["value"]

            for seg in text_segments:
                print(f"[{self.name}] {msg.topic} @ {msg.timestamp:.2f} -> {seg.text}")

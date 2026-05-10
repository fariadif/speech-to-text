from ..module import Module, Message


class Logger(Module):
    def on_start(self):
        self.subscribe("inference.transcription")

    def on_message(self, msg: Message):
        if msg.topic == "inference.transcription":
            text_segments = msg.payload["value"]

            for seg in text_segments:
                print(f"[{self.name}] {msg.topic} @ {msg.timestamp:.2f} -> {seg.text}")

from ..module import Module, Message


class Logger(Module):
    def on_start(self):
        self.subscribe("inference.transcription")

    def on_message(self, msg: Message):
        print(f"[{self.name}] {msg.topic} @ {msg.timestamp:.2f} -> {msg.payload}")

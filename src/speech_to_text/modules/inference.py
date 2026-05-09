from ..module import Module, Message


class Inference(Module):
    def on_start(self):
        self.subscribe("listener.audio")

    def on_message(self, msg: Message):

        if msg.topic == "listener.audio":
            print(
                f"[{self.name}] {msg.topic} @ {msg.timestamp:.2f} -> Received an audio"
            )

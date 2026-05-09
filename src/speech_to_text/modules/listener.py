from ..module import Module


import sounddevice as sd
import time

SAMPLE_RATE = 16000
DURATION = 5  # seconds per chunk


class Listener(Module):
    def on_start(self):
        print(f"[{self.name}] started")

        self._running = True

        while not self._stop_event.is_set():
            audio = sd.rec(
                int(DURATION * SAMPLE_RATE),
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
            )

            sd.wait()

            self.publish("listener.audio", {"value": audio})

        self.publish("system.shutdown", None)

    def on_stop(self):
        print("Listener on stop called")

    def on_message(self, mesg):
        pass

from ..module import Module

import threading

import sounddevice as sd


class Listener(Module):
    SAMPLE_RATE = 16000
    # DURATION_S = 30 / 1000  # seconds per chunk
    DURATION_S = 5  # seconds per chunk

    def on_start(self):
        print(f"[{self.name}] started")
        self._producer = threading.Thread(target=self._produce, daemon=True)
        self._producer.start()

    def _produce(self):
        while True:
            audio = sd.rec(
                int(self.DURATION_S * self.SAMPLE_RATE),
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype="float32",
            )

            sd.wait()

            if self._stop_event.is_set():
                break

            self.publish("listener.audio", {"value": audio})

        self.publish("system.shutdown", None)

    def on_stop(self):
        print("Listener on stop called")
        self._producer.join()

    def on_message(self, msg):
        print(f"[{self.name}] received {msg.topic}")

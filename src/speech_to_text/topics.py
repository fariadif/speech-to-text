from enum import StrEnum


class Topic(StrEnum):
    MICROPHONE_AUDIO = "microphone.audio"
    INFERENCE_TRANSCRIPTION = "inference.transcription"
    SYSTEM_SHUTDOWN = "system.shutdown"

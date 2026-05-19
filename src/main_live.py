import json
import queue

import sounddevice as sd

from vosk import Model, KaldiRecognizer


MODEL_PATH = "vosk-model-small-en-us-0.15"

COMMANDS = ["up", "down", "left", "right"]

SAMPLERATE = 16000

audio_queue = queue.Queue()


def audio_callback(indata, frames, time, status):
    audio_queue.put(bytes(indata))


print("Loading Vosk model...")
model = Model(MODEL_PATH)

recognizer = KaldiRecognizer(model, SAMPLERATE)

print("Live speech recognition started.")
print("Say: up, down, left, or right")
print("Press CTRL + C to stop.")


with sd.RawInputStream(
    samplerate=SAMPLERATE,
    blocksize=8000,
    dtype="int16",
    channels=1,
    callback=audio_callback
):

    while True:

        data = audio_queue.get()

        if recognizer.AcceptWaveform(data):

            result = json.loads(recognizer.Result())

            text = result.get("text", "").lower()

            if text:

                print(f"Recognized: {text}")

                for command in COMMANDS:

                    if command in text.split():

                        print(f"Valid command: {command}")
                        break
import json
import queue

import sounddevice as sd

from vosk import Model, KaldiRecognizer


# Path to the downloaded Vosk speech recognition model
MODEL_PATH = "vosk-model-small-en-us-0.15"

# List of valid voice commands that the program accepts
COMMANDS = ["up", "down", "left", "right"]

# Audio sample rate required by the Vosk model
SAMPLERATE = 16000

# Queue used to store incoming audio data from the microphone
audio_queue = queue.Queue()


# Callback function that is automatically called whenever
# new audio data is captured from the microphone
def audio_callback(indata, frames, time, status):

    # Convert audio data into bytes and store it in the queue
    audio_queue.put(bytes(indata))


# Inform the user that the speech recognition model is loading
print("Loading Vosk model...")

# Load the Vosk speech recognition model
model = Model(MODEL_PATH)

# Create a recognizer object with the model and sample rate
recognizer = KaldiRecognizer(model, SAMPLERATE)

# Display instructions for the user
print("Live speech recognition started.")
print("Say: up, down, left, or right")
print("Press CTRL + C to stop.")


# Open the microphone audio stream
with sd.RawInputStream(

    # Use the same sample rate as defined above
    samplerate=SAMPLERATE,

    # Number of audio frames processed at once
    blocksize=8000,

    # Audio format: 16-bit integer
    dtype="int16",

    # Mono audio input (1 microphone channel)
    channels=1,

    # Function that handles incoming audio data
    callback=audio_callback
):

    # Keep the program running continuously
    while True:

        # Get the next chunk of recorded audio data
        data = audio_queue.get()

        # Check if Vosk has received enough audio data
        # to recognize a complete phrase
        if recognizer.AcceptWaveform(data):

            # Convert the recognition result from JSON format
            # into a Python dictionary
            result = json.loads(recognizer.Result())

            # Extract recognized text and convert it to lowercase
            text = result.get("text", "").lower()

            # Continue only if speech was recognized
            if text:

                # Print the recognized speech
                print(f"Recognized: {text}")

                # Check whether one of the valid commands
                # is included in the recognized text
                for command in COMMANDS:

                    # Split the text into words and compare
                    if command in text.split():

                        # Print the detected valid command
                        print(f"Valid command: {command}")

                        # Stop checking after the first match
                        break
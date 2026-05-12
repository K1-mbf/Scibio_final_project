import speech_recognition as sr

# Create recognizer
recognizer = sr.Recognizer()

# Valid commands
commands = ["up", "down", "left", "right"]

# Open microphone
with sr.Microphone() as source:

    print("Say a command:")
    print(commands)

    # Reduce background noise
    recognizer.adjust_for_ambient_noise(source)

    # Listen to microphone
    audio = recognizer.listen(source)

try:
    # Convert speech to text
    text = recognizer.recognize_google(audio)

    # Lowercase
    text = text.lower()

    print(f"Recognized: {text}")

    # Check if command is valid
    if text in commands:
        print(f"Valid command: {text}")
    else:
        print("Invalid command")

except sr.UnknownValueError:
    print("Could not understand audio")

except sr.RequestError:
    print("Speech recognition service error")
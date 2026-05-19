import speech_recognition as sr

# print("Available microphones:")
# for index, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(index, name)

# for index, name in enumerate(sr.Microphone.list_microphone_names()):

#     print(f"\nTesting microphone {index}: {name}")

#     try:
#         with sr.Microphone(device_index=index) as source:
#             print("SUCCESS")

#     except Exception as error:
#         print(f"FAILED: {error}")


recognizer = sr.Recognizer()
mic_index = 1  # try by figuring out which index corresponds to your microphone from the list printed above

# with sr.Microphone(device_index=mic_index) as source:
#     print(f"Using microphone index: {mic_index}")
#     print("Say something for 3 seconds...")

#     audio = recognizer.record(source, duration=3)

# with open("test_audio.wav", "wb") as file:
#     file.write(audio.get_wav_data())

# print("Saved recording as test_audio.wav")

commands = ["up", "down", "left", "right"]

with sr.Microphone(device_index=mic_index) as source:

    print(f"Using microphone index: {mic_index}")
    print("Calibrating microphone...")

    recognizer.adjust_for_ambient_noise(source, duration=1)

    print("Say a command:")
    print(commands)

    audio = recognizer.record(source, duration=3)

try:
    text = recognizer.recognize_google(
        audio,
        language="en-US"
    )

    text = text.lower().strip()

    print(f"Recognized: {text}")

    found_command = None

    for command in commands:
        if command in text.split():
            found_command = command
            break

    if found_command:
        print(f"Valid command: {found_command}")
    else:
        print("Invalid command")

except sr.UnknownValueError:
    print("Could not understand audio.")

except sr.RequestError as error:
    print(f"Speech recognition service error: {error}")
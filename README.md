# Scibio_final_project

# Maze Voice Control

Voice-controlled maze game built with Python, Pygame, and Vosk.

## Features
- Real-time voice commands
- Offline speech recognition
- Random maze generation
- Pygame GUI

## Installation

```bash
pip install -r requirements.txt
```

## Run

### Voice-Controlled Game
```bash
python maze_voice_control.py
```

### Keyboard-Only Game
```bash
python game.py
```

### Live Speech Recognition Test
```bash
python src/main_live.py
```

### One-Time Speech Recognition Test
```bash
python src/main_once.py
```

## Voice Commands

```text
up
down
left
right
exit
```

## Project Structure

```text
maze_voice_control/
│
├── maze_voice_control.py   # Main voice-controlled maze game
├── game.py                 # Keyboard-only maze game
├── requirements.txt        # Python dependencies
│
├── src/
│   ├── main_live.py        # Live offline speech recognition
│   └── main_once.py        # Single speech recognition test
│
└── vosk-model-small-en-us-0.15/   # Offline Vosk model
```

## File Description

### `maze_voice_control.py`
Main application:
- Maze generation
- Pygame rendering
- Voice recognition
- Player movement

### `game.py`
Keyboard-controlled version for testing gameplay without voice input.

### `src/main_live.py`
Continuous real-time speech recognition using Vosk.

### `src/main_once.py`
One-time speech recognition using Google Speech API.

### `requirements.txt`
Contains required Python packages.

### `vosk-model-small-en-us-0.15/`
Offline speech recognition model required for Vosk.

## Dependencies
- pygame
- vosk
- sounddevice
- SpeechRecognition
- pyaudio
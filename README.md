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
├── requirements.txt        # Python dependencies
│
├── doc/
│   ├── Report.docx         # Final Report
│   ├── Presentation.pptx   # Final Presentation
│   └── Project Plan.xlsx   # Gantt Diagramm of project plan
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
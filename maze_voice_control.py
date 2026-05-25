import json
import queue
import random
import sys
import threading

import pygame
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ==========================================
# CONFIGURATION & SETTINGS
# ==========================================
MAZE_COLS = 5
MAZE_ROWS = 5
CELL_SIZE = 40

START_X = MAZE_COLS // 2
START_Y = MAZE_ROWS // 2

RANDOM_SEED = None

BG_COLOR = (30, 30, 30)
WALL_COLOR = (0, 200, 200)
PLAYER_COLOR = (255, 80, 80)
GOAL_COLOR = (80, 255, 80)

FPS = 60

# Voice settings
MODEL_PATH = "vosk-model-small-en-us-0.15"
SAMPLERATE = 16000
VOICE_COMMANDS = {
    "up": "UP",
    "down": "DOWN",
    "left": "LEFT",
    "right": "RIGHT",
    "exit": "EXIT",
}
# ==========================================


class VoiceController:
    """Runs Vosk speech recognition in a background thread."""

    def __init__(self):
        self.audio_queue = queue.Queue()
        self.command_queue = queue.Queue()
        self.running = False
        self.thread = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.audio_queue.put(bytes(indata))

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()

    def _listen_loop(self):
        # print("Loading Vosk model...")
        model = Model(MODEL_PATH)
        recognizer = KaldiRecognizer(model, SAMPLERATE)

        print("Voice control started. Say: up, down, left, right")
        print("Press CTRL + C or say 'exit' to stop.")

        with sd.RawInputStream(
            samplerate=SAMPLERATE,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=self.audio_callback,
        ):
            while self.running:
                try:
                    data = self.audio_queue.get(timeout=0.1)
                except queue.Empty:
                    continue

                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "").lower()

                    if text:
                        print(f"Recognized: {text}")
                        words = text.split()

                        for spoken_word, action in VOICE_COMMANDS.items():
                            if spoken_word in words:
                                print(f"Voice command: {action}")
                                self.command_queue.put(action)
                                break

    def get_action(self):
        """Returns one voice command if available, otherwise None."""
        try:
            return self.command_queue.get_nowait()
        except queue.Empty:
            return None

    def stop(self):
        self.running = False


class Cell:
    """Represents a single square in the maze."""

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw(self, surface):
        px = self.x * CELL_SIZE
        py = self.y * CELL_SIZE

        if self.walls["top"]:
            pygame.draw.line(surface, WALL_COLOR, (px, py), (px + CELL_SIZE, py), 2)
        if self.walls["right"]:
            pygame.draw.line(surface, WALL_COLOR, (px + CELL_SIZE, py), (px + CELL_SIZE, py + CELL_SIZE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(surface, WALL_COLOR, (px + CELL_SIZE, py + CELL_SIZE), (px, py + CELL_SIZE), 2)
        if self.walls["left"]:
            pygame.draw.line(surface, WALL_COLOR, (px, py + CELL_SIZE), (px, py), 2)


class Maze:
    """Handles the grid and maze generation."""

    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.grid = [[Cell(x, y) for x in range(cols)] for y in range(rows)]
        self.generate()

    def generate(self):
        """Generates a perfect maze using Recursive Backtracking."""
        if RANDOM_SEED is not None:
            random.seed(RANDOM_SEED)

        current = self.grid[0][0]
        current.visited = True
        stack = []

        while True:
            neighbors = self._get_unvisited_neighbors(current)
            if neighbors:
                next_cell = random.choice(neighbors)
                stack.append(current)
                self._remove_walls(current, next_cell)
                current = next_cell
                current.visited = True
            elif stack:
                current = stack.pop()
            else:
                break

        self._clear_spawn_area(START_X, START_Y)

    def _clear_spawn_area(self, cx, cy):
        """Removes the internal walls of a 3x3 area centered on (cx, cy)."""
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = cx + dx, cy + dy

                if 0 <= nx < self.cols and 0 <= ny < self.rows:
                    cell = self.grid[ny][nx]
                    if dx > -1:
                        cell.walls["left"] = False
                    if dx < 1:
                        cell.walls["right"] = False
                    if dy > -1:
                        cell.walls["top"] = False
                    if dy < 1:
                        cell.walls["bottom"] = False

    def _get_unvisited_neighbors(self, cell):
        neighbors = []
        x, y = cell.x, cell.y
        if y > 0 and not self.grid[y - 1][x].visited:
            neighbors.append(self.grid[y - 1][x])
        if x < self.cols - 1 and not self.grid[y][x + 1].visited:
            neighbors.append(self.grid[y][x + 1])
        if y < self.rows - 1 and not self.grid[y + 1][x].visited:
            neighbors.append(self.grid[y + 1][x])
        if x > 0 and not self.grid[y][x - 1].visited:
            neighbors.append(self.grid[y][x - 1])
        return neighbors

    def _remove_walls(self, a, b):
        dx = a.x - b.x
        if dx == 1:
            a.walls["left"] = False
            b.walls["right"] = False
        elif dx == -1:
            a.walls["right"] = False
            b.walls["left"] = False

        dy = a.y - b.y
        if dy == 1:
            a.walls["top"] = False
            b.walls["bottom"] = False
        elif dy == -1:
            a.walls["bottom"] = False
            b.walls["top"] = False

    def draw(self, surface):
        for row in self.grid:
            for cell in row:
                cell.draw(surface)


class Game:
    """Main game controller."""

    def __init__(self):
        pygame.init()
        self.width = MAZE_COLS * CELL_SIZE
        self.height = MAZE_ROWS * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Voice-Controlled Maze Game")
        self.clock = pygame.time.Clock()

        self.maze = Maze(MAZE_COLS, MAZE_ROWS)
        self.voice = VoiceController()
        self.voice.start()

        self.player_x = START_X
        self.player_y = START_Y

        self.goal_x = 0
        self.goal_y = 0

    def get_action(self):
        """Reads keyboard input first, then voice input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    return "UP"
                if event.key == pygame.K_DOWN:
                    return "DOWN"
                if event.key == pygame.K_LEFT:
                    return "LEFT"
                if event.key == pygame.K_RIGHT:
                    return "RIGHT"

        return self.voice.get_action()

    def apply_action(self, action):
        """Applies the intended movement if no walls block the way."""
        if not action:
            return

        current_cell = self.maze.grid[self.player_y][self.player_x]

        if action == "UP" and not current_cell.walls["top"]:
            self.player_y -= 1
        elif action == "DOWN" and not current_cell.walls["bottom"]:
            self.player_y += 1
        elif action == "LEFT" and not current_cell.walls["left"]:
            self.player_x -= 1
        elif action == "RIGHT" and not current_cell.walls["right"]:
            self.player_x += 1

    def draw(self):
        self.screen.fill(BG_COLOR)

        goal_rect = pygame.Rect(
            self.goal_x * CELL_SIZE + 5,
            self.goal_y * CELL_SIZE + 5,
            CELL_SIZE - 10,
            CELL_SIZE - 10,
        )
        pygame.draw.rect(self.screen, GOAL_COLOR, goal_rect)

        player_rect = pygame.Rect(
            self.player_x * CELL_SIZE + 8,
            self.player_y * CELL_SIZE + 8,
            CELL_SIZE - 16,
            CELL_SIZE - 16,
        )
        pygame.draw.rect(self.screen, PLAYER_COLOR, player_rect)

        self.maze.draw(self.screen)
        pygame.display.flip()

    def quit_game(self):
        self.voice.stop()
        pygame.quit()
        sys.exit()

    def run(self):
        """Main game loop."""
        while True:
            action = self.get_action()

            if action == "EXIT":
                print("Exiting game...")
                break

            self.apply_action(action)

            if self.player_x == self.goal_x and self.player_y == self.goal_y:
                print("Goal Reached!")
                self.draw()
                pygame.display.flip()
                pygame.time.delay(2000)
                self.restart_level()
            self.draw()
            self.clock.tick(FPS)

    def restart_level(self):
        """Starts a new maze after the goal was reached."""
        self.maze = Maze(MAZE_COLS, MAZE_ROWS)
        self.player_x = START_X
        self.player_y = START_Y
        self.goal_x = 0
        self.goal_y = 0


if __name__ == "__main__":
    game = Game()
    game.run()

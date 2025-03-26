import pygame
import time
import sys
import random

pygame.init()

# Fenstergrösse
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Schriftart
font = pygame.font.SysFont("Arial", 24)

terminal_lines = []
user_input = ""

# Globale Variablen für den Spielstatus
in_riddle = False
current_answer = ""
cursor_visible = True
cursor_timer = pygame.time.get_ticks()
cursor_blink_speed = 500

time_limit = 300
level_start_time = None
waiting_for_next_level = False

# Hacker-Logs
hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum Server wird herstellen...",
    "[WARNUNG] Firewall erkannt! Versuche, die Sperre zu umgehen...",
    "[ERFOLG] Zugriff gewährt. Willkommen, Agent.",
    "[MISSION INFO] Bereite dich auf herausfordernde Missionen vor. Tippe 'start', um zu beginnen.",
    ""
]

def draw_terminal():
    # Terminal-Layout
    screen.fill(BLACK)
    line_height = 25
    input_area_height = 40  # Höhe des Eingabebereichs
    terminal_area_height = HEIGHT - input_area_height - 10
    max_lines = terminal_area_height // line_height

    displayed_lines = terminal_lines[-max_lines:]
    y_offset = 10
    for line in displayed_lines:
        text_surface = font.render(line, True, GREEN)
        screen.blit(text_surface, (10, y_offset))
        y_offset += line_height

    # Trennlinie zwischen Terminal- und Eingabebereich
    pygame.draw.line(screen, GREEN, (0, HEIGHT - input_area_height), (WIDTH, HEIGHT - input_area_height), 2)

    # Eingabebereich
    input_surface = font.render("> " + user_input, True, GREEN)
    screen.blit(input_surface, (10, HEIGHT - input_area_height + (input_area_height - line_height) // 2))
    pygame.display.flip()

# Player-Klasse
class Player:
    def __init__(self):
        self.level = 1
        self.solved_riddles = 0  
        self.points = 0

    def level_up(self):
        self.level += 1
        self.solved_riddles = 0  
        terminal_lines.append("")
        terminal_lines.append("-----------------------------")
        terminal_lines.append(f"[LEVEL-UP] Du bist jetzt auf Level {self.level}!")
        terminal_lines.append("-----------------------------")
        terminal_lines.append("")

# Riddle-Klasse
class Riddle:
    all_tasks = {
        "bypass": {
            1: [
                {"question": "Löse die Gleichung: 5 + 3 = ?", "answer": "8"},
                {"question": "Löse die Gleichung: 7 - 2 = ?", "answer": "5"}
            ],
            2: [
                {"question": "Was ist die Binärdarstellung von 5?", "answer": "101"},
                {"question": "Was ist die Binärdarstellung von 7?", "answer": "111"}
            ]
        },
        "wordhack": {
            1: [
                {"word": "CYBER"},
                {"word": "HACKER"}
            ],
            2: [
                {"word": "MALWARE"},
                {"word": "PHISHING"}
            ]
        },
        "math": {
            1: [
                {"question": "Berechne: 5 + 3 = ?", "answer": "8"},
                {"question": "Berechne: 4 + 4 = ?", "answer": "8"}
            ],
            2: [
                {"question": "Berechne: 12 + 15 = ?", "answer": "27"},
                {"question": "Berechne: 14 + 18 = ?", "answer": "32"}
            ]
        },
        "logic": {
            1: [
                {"question": "Welche Aussage ist wahr?\n  A) 2 + 2 = 5\n  B) 2 + 2 = 4", "answer": "B"}
            ],
            2: [
                {"question": "Welche Aussage ist korrekt?\n  A) Wasser siedet bei 100°C\n  B) Eisen schmilzt bei 50°C", "answer": "A"}
            ]
        },
        "sequence": {
            1: [
                {"question": "Welche Zahl folgt in der Reihe: 1, 2, 3, 4, ?", "answer": "5"}
            ],
            2: [
                {"question": "Welche Zahl folgt in der Reihe: 2, 3, 5, 8, 13, ?", "answer": "21"}
            ]
        }
    }
    available_tasks = {}

    @staticmethod
    def init_tasks_for_level(level):
        Riddle.available_tasks = {}
        level_key = level if level in [1, 2] else 2
        for typ in Riddle.all_tasks:
            Riddle.available_tasks[typ] = list(Riddle.all_tasks[typ][level_key])
    
    @staticmethod
    def generate_riddle(level):
        global current_answer
        if not Riddle.available_tasks:
            Riddle.init_tasks_for_level(level)
        available_types = [typ for typ in Riddle.available_tasks if Riddle.available_tasks[typ]]
        if not available_types:
            Riddle.init_tasks_for_level(level)
            available_types = list(Riddle.available_tasks.keys())
        typ = random.choice(available_types)
        task = random.choice(Riddle.available_tasks[typ])
        Riddle.available_tasks[typ].remove(task)
        if typ == "bypass":
            current_answer = task["answer"]
            return [task["question"]]
        elif typ == "wordhack":
            word = task["word"]
            scrambled = "".join(random.sample(word, len(word)))
            current_answer = word
            return ["Entschlüssele das Wort:", "", "  " + scrambled]
        elif typ == "math":
            current_answer = task["answer"]
            return [task["question"]]
        elif typ == "logic":
            current_answer = task["answer"]
            return task["question"].split("\n")
        elif typ == "sequence":
            current_answer = task["answer"]
            return [task["question"]]
        else:
            current_answer = ""
            return ["Kein Rätsel verfügbar."]

player = Player()

def run_game():
    global user_input
    running = True
    clock = pygame.time.Clock()

    # Hacker-Logs initial anzeigen
    for log in hacker_logs:
        terminal_lines.append(log)
        draw_terminal()
        time.sleep(1)

    while running:
        draw_terminal()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    terminal_lines.append("> " + user_input)
                    terminal_lines.append(f"[EXECUTING] {user_input}...")
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        clock.tick(30)

    pygame.quit()
    sys.exit()

run_game()

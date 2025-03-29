import pygame
import time
import sys
import random

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

font = pygame.font.SysFont("Arial", 24)

terminal_lines = []
user_input = ""

in_riddle = False
current_answer = ""
cursor_visible = True
cursor_timer = pygame.time.get_ticks()
cursor_blink_speed = 500

time_limit = 300  # 5 Minuten pro Level
level_start_time = None
waiting_for_next_level = False
riddle_start_time = None  # Zeitpunkt des aktuellen Rätsels

hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum Server wird hergestellt...",
    "[WARNUNG] Firewall erkannt! Starte Protokoll...",
    "[ERFOLG] Zugriff gewährt. Willkommen, Agent.",
    "[MISSION INFO] Jede Mission ist zeitkritisch! Du hast pro Level maximal 5 Minuten.",
    "[MISSION TASK] Aufgaben: Arithmetik, Binär, Wortspiel, Logik, Zahlenfolge, Rätsel.",
    "[READY] Dein Verstand ist gefragt. Bist du bereit, in die Tiefen des CyberHeists einzutauchen?",
    "[EINGABE] Tippe 'start', um das Spiel zu beginnen.",
    ""
]

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
        terminal_lines.append(f"[LEVEL-UP] 🎉 Du bist jetzt auf Level {self.level}!")
        terminal_lines.append("-----------------------------")
        terminal_lines.append("")

class Riddle:
    all_tasks = {
        "arithmetik": {
            1: [
                {"question": "Berechne: 3 + 4 = ?", "answer": "7"},
                {"question": "Berechne: 8 - 5 = ?", "answer": "3"},
                {"question": "Berechne: 6 + 2 = ?", "answer": "8"},
                {"question": "Berechne: 9 - 3 = ?", "answer": "6"},
                {"question": "Berechne: 4 + 3 = ?", "answer": "7"}
            ],
            2: [
                {"question": "Berechne: 12 + 15 = ?", "answer": "27"},
                {"question": "Berechne: 20 - 8 = ?", "answer": "12"},
                {"question": "Berechne: 7 * 3 = ?", "answer": "21"},
                {"question": "Berechne: 18 / 2 = ?", "answer": "9"},
                {"question": "Berechne: 14 + 6 = ?", "answer": "20"}
            ],
            3: [
                {"question": "Berechne: 15 * 4 = ?", "answer": "60"},
                {"question": "Berechne: 45 / 5 = ?", "answer": "9"},
                {"question": "Berechne: 23 + 37 = ?", "answer": "60"},
                {"question": "Berechne: 50 - 17 = ?", "answer": "33"}
            ]
        },
        "binär": {
            1: [
                {"question": "Was ist die Binärdarstellung von 2?", "answer": "10"},
                {"question": "Was ist die Binärdarstellung von 3?", "answer": "11"},
                {"question": "Was ist die Binärdarstellung von 4?", "answer": "100"},
                {"question": "Was ist die Binärdarstellung von 5?", "answer": "101"},
                {"question": "Was ist die Binärdarstellung von 6?", "answer": "110"}
            ],
            2: [
                {"question": "Was ist die Binärdarstellung von 10?", "answer": "1010"},
                {"question": "Was ist die Binärdarstellung von 12?", "answer": "1100"},
                {"question": "Was ist die Binärdarstellung von 14?", "answer": "1110"},
                {"question": "Was ist die Binärdarstellung von 15?", "answer": "1111"},
                {"question": "Was ist die Binärdarstellung von 9?", "answer": "1001"}
            ],
            3: [
                {"question": "Was ist die Binärdarstellung von 23?", "answer": "10111"},
                {"question": "Was ist die Binärdarstellung von 27?", "answer": "11011"},
                {"question": "Was ist die Binärdarstellung von 31?", "answer": "11111"}
            ]
        },
        "wortspiel": {
            1: [
                {"word": "CODE"},
                {"word": "HACK"},
                {"word": "NETZ"},
                {"word": "LOGIK"},
                {"word": "SPIEL"}
            ],
            2: [
                {"word": "PROGRAMM"},
                {"word": "TECHNIK"},
                {"word": "ALGORITHMUS"},
                {"word": "VIRUS"},
                {"word": "SYSTEM"}
            ],
            3: [
                {"word": "INNOVATION"},
                {"word": "DIGITALISIERUNG"},
                {"word": "CYBERSECURITY"}
            ]
        },
        "logik": {
            1: [
                {"question": "Welche Aussage ist korrekt?\n  A) Wasser ist trocken\n  B) Feuer ist heiß\n  C) Schnee ist schwarz", "answer": "B"},
                {"question": "Welche Aussage ist wahr?\n  A) 2 + 2 = 5\n  B) 2 + 2 = 4\n  C) 2 + 2 = 3", "answer": "B"}
            ],
            2: [
                {"question": "Welche Aussage ist richtig?\n  A) Die Erde ist rund\n  B) Die Erde ist flach\n  C) Die Erde ist eckig", "answer": "A"},
                {"question": "Welche Aussage ist korrekt?\n  A) Feuer ist kalt\n  B) Eis ist heiß\n  C) Wasser ist flüssig", "answer": "C"}
            ],
            3: [
                {"question": "Welche Aussage ist korrekt?\n  A) Alle Vögel können fliegen\n  B) Pinguine können nicht fliegen\n  C) Fische können fliegen", "answer": "B"},
                {"question": "Welche Aussage ist wahr?\n  A) Bäume produzieren Sauerstoff\n  B) Autos produzieren Sauerstoff\n  C) Steine produzieren Sauerstoff", "answer": "A"}
            ]
        },
        "zahlenfolge": {
            1: [
                {"question": "Welche Zahl folgt in der Reihe: 1, 2, 3, 4, ?", "answer": "5"},
                {"question": "Welche Zahl folgt in der Reihe: 2, 4, 6, 8, ?", "answer": "10"}
            ],
            2: [
                {"question": "Welche Zahl folgt in der Reihe: 3, 6, 9, 12, ?", "answer": "15"},
                {"question": "Welche Zahl folgt in der Reihe: 5, 10, 15, 20, ?", "answer": "25"}
            ],
            3: [
                {"question": "Welche Zahl folgt in der Reihe: 8, 13, 18, 23, ?", "answer": "28"},
                {"question": "Welche Zahl folgt in der Reihe: 2, 3, 5, 8, ?", "answer": "13"}
            ]
        },
        "rätsel": {
            1: [
                {"question": "Was hat einen Kopf, aber keinen Körper?", "answer": "Münze"},
                {"question": "Was wird nass, je mehr es trocknet?", "answer": "Handtuch"}
            ],
            2: [
                {"question": "Ich bin immer hungrig, muss ständig essen, doch wenn ich trinke, sterbe ich. Was bin ich?", "answer": "Feuer"},
                {"question": "Ich spreche ohne Mund und höre ohne Ohren. Was bin ich?", "answer": "Echo"}
            ],
            3: [
                {"question": "Ich kann fliegen ohne Flügel und weinen ohne Augen. Was bin ich?", "answer": "Wolke"}
            ]
        }
    }
    available_tasks = {}

    @staticmethod
    def init_tasks_for_level(level):
        Riddle.available_tasks = {}
        level_key = level if level in [1, 2, 3] else 3
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
        if typ in ["arithmetik", "binär", "zahlenfolge", "logik", "rätsel"]:
            current_answer = task["answer"].upper().strip()
            return task["question"].split("\n")
        elif typ == "wortspiel":
            word = task["word"]
            scrambled = "".join(random.sample(word, len(word)))
            current_answer = word.upper().strip()
            return ["Entschlüssele das Wort:", "", "  " + scrambled]
        else:
            current_answer = ""
            return ["Kein Rätsel verfügbar."]
            
player = Player()

def draw_terminal():
    screen.fill(BLACK)
    line_height = 25
    input_area_height = 40
    terminal_area_height = HEIGHT - input_area_height - 10
    max_lines = terminal_area_height // line_height

    # Countdown-Anzeige, falls ein Level läuft
    if level_start_time is not None:
        elapsed = time.time() - level_start_time
        remaining = max(0, int(time_limit - elapsed))
        minutes = remaining // 60
        seconds = remaining % 60
        countdown_text = f"Restzeit: {minutes:02d}:{seconds:02d}"
        countdown_surface = font.render(countdown_text, True, GREEN)
        screen.blit(countdown_surface, (WIDTH - countdown_surface.get_width() - 10, 10))

    displayed_lines = terminal_lines[-max_lines:]
    y_offset = 10
    for line in displayed_lines:
        text_surface = font.render(line, True, GREEN)
        screen.blit(text_surface, (10, y_offset))
        y_offset += line_height

    pygame.draw.line(screen, GREEN, (0, HEIGHT - input_area_height), (WIDTH, HEIGHT - input_area_height), 2)

    # Blinkender Cursor
    global cursor_visible, cursor_timer
    if pygame.time.get_ticks() - cursor_timer > cursor_blink_speed:
        cursor_visible = not cursor_visible
        cursor_timer = pygame.time.get_ticks()

    input_text = "> " + user_input + ("_" if cursor_visible else "")
    input_surface = font.render(input_text, True, GREEN)
    screen.blit(input_surface, (10, HEIGHT - input_area_height + (input_area_height - line_height) // 2))
    pygame.display.flip()

def start_game():
    global in_riddle, level_start_time, waiting_for_next_level, riddle_start_time
    terminal_lines.append("")
    terminal_lines.append("-----------------------------")
    terminal_lines.append(f"[MISSION] 6 Rätsel für Level {player.level} beginnen jetzt!")
    terminal_lines.append("-----------------------------")
    terminal_lines.append("")
    in_riddle = True
    waiting_for_next_level = False
    level_start_time = time.time()
    Riddle.init_tasks_for_level(player.level)
    ask_next_riddle()

def ask_next_riddle():
    global in_riddle, waiting_for_next_level, riddle_start_time
    riddle_start_time = time.time()  # Startzeit des aktuellen Rätsels
    if player.solved_riddles >= 6:
        show_level_summary()
    else:
        terminal_lines.append("")
        riddle_lines = Riddle.generate_riddle(player.level)
        terminal_lines.append("[RÄTSEL]")
        for line in riddle_lines:
            terminal_lines.append(line)
        in_riddle = True

def show_level_summary():
    global waiting_for_next_level, level_start_time
    elapsed = int(time.time() - level_start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    player.points += player.solved_riddles * 10
    terminal_lines.append("")
    if player.level < 5:
        terminal_lines.append("*****************************")
        terminal_lines.append(f"[LEVEL ABGESCHLOSSEN] Level {player.level} beendet!")
        terminal_lines.append(f"Verbrauchte Zeit: {minutes:02d}:{seconds:02d}")
        terminal_lines.append(f"Punkte: {player.points}")
        terminal_lines.append("*****************************")
        terminal_lines.append("")
        terminal_lines.append(f"Möchtest du mit Level {player.level + 1} starten? (Tippe 'start')")
    else:
        terminal_lines.append("*****************************")
        terminal_lines.append(f"[MISSION ABGESCHLOSSEN] Du hast alle Level erfolgreich abgeschlossen!")
        terminal_lines.append(f"Gesamte Punkte: {player.points}")
        terminal_lines.append("*****************************")
        terminal_lines.append("")
        terminal_lines.append("Tippe 'ende', um das Spiel zu beenden.")
    waiting_for_next_level = True
    global in_riddle
    in_riddle = False
    level_start_time = None

def run_game():
    global user_input, in_riddle, current_answer, waiting_for_next_level, level_start_time
    running = True
    clock = pygame.time.Clock()

    # Hacker-Logs initial anzeigen
    for log in hacker_logs:
        terminal_lines.append(log)
        draw_terminal()
        time.sleep(1)

    while running:
        if level_start_time is not None:
            elapsed = time.time() - level_start_time
            if elapsed > time_limit:
                terminal_lines.append("")
                terminal_lines.append("⏰ [ZEIT ABGELAUFEN] Du hast mehr als 5 Minuten gebraucht. Level verloren!")
                draw_terminal()
                time.sleep(3)
                running = False
                continue
        
        draw_terminal()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    terminal_lines.append("")
                    terminal_lines.append("> " + user_input)
                    if waiting_for_next_level:
                        if player.level < 5:
                            if user_input.lower() == "start":
                                player.level_up()
                                start_game()
                            elif user_input.lower() == "ende":
                                terminal_lines.append("")
                                terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                                running = False
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'start' oder 'ende'.")
                        else:
                            if user_input.lower() == "ende":
                                terminal_lines.append("")
                                terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                                running = False
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'ende', um das Spiel zu beenden.")
                    else:
                        if user_input.lower() == "start":
                            start_game()
                        elif in_riddle:
                            answer_time = time.time() - riddle_start_time
                            if user_input.upper().strip() == current_answer:
                                terminal_lines.append("")
                                terminal_lines.append("✅ [ERFOLG] Richtige Antwort! Rätsel gelöst.")
                                # Bonus für schnelle Lösungen: wenn in weniger als 10 Sekunden gelöst, gibt es Punktebonus
                                if answer_time < 10:
                                    bonus = 10 - int(answer_time)
                                    player.points += bonus
                                    terminal_lines.append(f"[BONUS] Schnelle Lösung! +{bonus} Punkte.")
                                terminal_lines.append("")
                                player.solved_riddles += 1
                                in_riddle = False
                                ask_next_riddle()
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("❌ [FEHLER] Falsche Antwort. Versuch es erneut!")
                        elif user_input.lower() == "ende":
                            terminal_lines.append("")
                            terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                            running = False
                        else:
                            terminal_lines.append("")
                            terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'start'.")
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        clock.tick(30)
    pygame.quit()
    sys.exit()

run_game()

import pygame
import time
import random
from player import Player
from riddles import Riddle
from renderer import Renderer

pygame.init()

# Fenster-Setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

# Farben und Schrift
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont("Arial", 24)

# Globale Variablen (Spielzustand)
terminal_lines = []
user_input = ""
in_riddle = False
current_answer = ""
current_hint = ""   # Neuer Wert für den Hinweis
time_limit = 300    # 5 Minuten pro Level
level_start_time = None
waiting_for_next_level = False
riddle_start_time = None  # Zeitpunkt des aktuellen Rätsels

hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum Server wird hergestellt...",
    "[WARNUNG] Firewall erkannt! Starte Protokoll...",
    "[ERFOLG] Zugriff gewährt. Willkommen, Agent.",
    "[MISSION INFO] Jede Mission ist zeitkritisch! Du hast pro Level maximal 5 Minuten.",
    "[MISSION TASK] Aufgaben: Arithmetik, Binär, Wortspiel, Zahlenfolge, Geografie, Allgemeinwissen.",
    "[READY] Dein Verstand ist gefragt. Bist du bereit, in die Tiefen des CyberHeists einzutauchen?",
    "[EINGABE] Tippe 'start', um das Spiel zu beginnen.",
    ""
]

player = Player()

# Erstelle eine Renderer-Instanz
renderer = Renderer(
    screen,
    font,
    {"BLACK": BLACK, "GREEN": GREEN},
    {"WIDTH": WIDTH, "HEIGHT": HEIGHT}
)

def draw_terminal():
    """Wrapper-Funktion, die den Renderer aufruft."""
    renderer.draw_terminal(terminal_lines, user_input, level_start_time, time_limit)

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
    """
    Holt das nächste Rätsel (Fragezeilen, Antwort und Hinweis) und zeigt es an.
    """
    global in_riddle, waiting_for_next_level, riddle_start_time, current_answer, current_hint
    riddle_start_time = time.time()
    if player.solved_riddles >= 6:
        show_level_summary()
    else:
        terminal_lines.append("")
        riddle_lines, current_answer, current_hint = Riddle.generate_riddle(player.level)
        terminal_lines.append("[RÄTSEL]")
        for line in riddle_lines:
            terminal_lines.append(line)
        in_riddle = True

def show_level_summary():
    global waiting_for_next_level, level_start_time, in_riddle
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
        terminal_lines.append("[MISSION ABGESCHLOSSEN] Du hast alle Level erfolgreich abgeschlossen!")
        terminal_lines.append(f"Gesamte Punkte: {player.points}")
        terminal_lines.append("*****************************")
        terminal_lines.append("")
        terminal_lines.append("Tippe 'ende', um das Spiel zu beenden.")
    waiting_for_next_level = True
    in_riddle = False

def run_game():
    global user_input, in_riddle, current_answer, waiting_for_next_level, level_start_time, current_hint
    running = True
    clock = pygame.time.Clock()
    exit_to_menu = False

    # Hacker-Logs initial anzeigen
    for log in hacker_logs:
        terminal_lines.append(log)
        renderer.draw_terminal(terminal_lines, user_input, level_start_time, time_limit)
        time.sleep(1)

    while running:
        # Zeitüberschreitung prüfen
        if level_start_time is not None:
            elapsed = time.time() - level_start_time
            if elapsed > time_limit:
                terminal_lines.append("")
                terminal_lines.append("⏰ [ZEIT ABGELAUFEN] Du hast mehr als 5 Minuten gebraucht. Level verloren!")
                renderer.draw_terminal(terminal_lines, user_input, level_start_time, time_limit)
                time.sleep(3)
                running = False
                exit_to_menu = True
                continue

        renderer.draw_terminal(terminal_lines, user_input, level_start_time, time_limit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit_to_menu = True
            elif event.type == pygame.KEYDOWN:
                # ESC: Spiel abbrechen
                if event.key == pygame.K_ESCAPE:
                    terminal_lines.append("")
                    terminal_lines.append("[ABBRUCH] Spiel wird abgebrochen und zum Menü zurückgekehrt.")
                    running = False
                    exit_to_menu = True
                    break
                elif event.key == pygame.K_RETURN:
                    terminal_lines.append("")
                    terminal_lines.append("> " + user_input)
                    cmd = user_input.lower().strip()

                    # Joker-Hint
                    if cmd == "joker":
                        if current_hint:
                            terminal_lines.append("")
                            terminal_lines.append("[HINT] " + current_hint)
                        else:
                            terminal_lines.append("")
                            terminal_lines.append("[HINT] Kein Hinweis verfügbar.")
                        user_input = ""
                        break

                    # Immer beenden möglich
                    elif cmd == "ende":
                        terminal_lines.append("")
                        terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                        running = False
                        exit_to_menu = True
                        user_input = ""
                        break

                    # Level‑Wechsel steuern
                    elif waiting_for_next_level:
                        if player.level < 5:
                            if cmd == "start":
                                player.level_up()
                                start_game()
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'start' oder 'ende'.")
                        else:
                            if cmd == "ende":
                                terminal_lines.append("")
                                terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                                running = False
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'ende', um das Spiel zu beenden.")
                    # Normales Spiel-Handling
                    else:
                        if cmd == "start":
                            start_game()
                        elif in_riddle:
                            answer_time = time.time() - riddle_start_time
                            if user_input.upper().strip() == current_answer:
                                terminal_lines.append("")
                                terminal_lines.append("✅ [ERFOLG] Richtige Antwort! Rätsel gelöst.")
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
                        else:
                            terminal_lines.append("")
                            terminal_lines.append("[FEHLER] Unbekannter Befehl. Tippe 'start'.")
                    user_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode
        clock.tick(30)

    # Gibt immer die bis dahin erspielten Punkte zurück
    return player.points

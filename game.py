import pygame
import time
import random
from player import Player
from riddles import Riddle
from renderer import Renderer
from sound_manager import SoundManager
import config

pygame.init()

# Fenster‑Setup
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Terminal‑Abenteuer")

# Farben und Schrift
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
font = pygame.font.SysFont("Consolas", 24)

# Spielzustand
terminal_lines = []
user_input = ""
in_riddle = False
current_answer = ""
current_hint = ""
time_limit = 300    # 5 Minuten pro Level
level_start_time = None
waiting_for_next_level = False
riddle_start_time = None

hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum Server wird hergestellt...",
    "[ERFOLG] Zugriff gewährt. Willkommen.",
    "[MISSION INFO] Du hast pro Level maximal 5 Minuten.",
    "[EINGABE] Dein Verstand ist gefragt. Tippe 'start', um das Spiel zu beginnen.",
    ""
]

player = Player()
renderer = Renderer(
    screen, font,
    {"BLACK": BLACK, "GREEN": GREEN},
    {"WIDTH": WIDTH, "HEIGHT": HEIGHT}
)

def draw_terminal():
    """Zeichnet das Terminal mit aktuellem State."""
    renderer.draw_terminal(terminal_lines, user_input, level_start_time, time_limit)

def start_game(sm: SoundManager):
    """Initialisiert ein neues Level."""
    global in_riddle, level_start_time, waiting_for_next_level, riddle_start_time
    terminal_lines.append("")
    terminal_lines.append("-----------------------------")
    terminal_lines.append(f"[MISSION] 6 Rätsel für Level {player.level} starten jetzt!")
    terminal_lines.append("-----------------------------")
    terminal_lines.append("")
    if config.SOUND_ON:
        sm.play("level_start")
    in_riddle = True
    waiting_for_next_level = False
    level_start_time = time.time()
    Riddle.init_tasks_for_level(player.level)
    ask_next_riddle(sm)

def ask_next_riddle(sm: SoundManager):
    """Gibt das nächste Rätsel aus oder fasst Level zusammen."""
    global in_riddle, waiting_for_next_level, riddle_start_time, current_answer, current_hint
    riddle_start_time = time.time()
    if player.solved_riddles >= 6:
        show_level_summary(sm)
    else:
        terminal_lines.append("")
        lines, current_answer, current_hint = Riddle.generate_riddle(player.level)
        terminal_lines.append("[RÄTSEL]")
        for line in lines:
            terminal_lines.append(line)
        if config.SOUND_ON:
            sm.play("prompt")
        in_riddle = True

def show_level_summary(sm: SoundManager):
    """Zeigt Statistiken am Ende eines Levels an."""
    global waiting_for_next_level, level_start_time, in_riddle
    elapsed = int(time.time() - level_start_time)
    minutes = elapsed // 60
    seconds = elapsed % 60
    player.points += player.solved_riddles * 10
    if config.SOUND_ON:
        sm.play("level_complete")
    terminal_lines.append("")
    terminal_lines.append("*****************************")
    if player.level < 5:
        terminal_lines.append(f"[LEVEL ABGESCHLOSSEN] Level {player.level} beendet!")
        terminal_lines.append(f"Verbrauchte Zeit: {minutes:02d}:{seconds:02d}")
        terminal_lines.append(f"Punkte: {player.points}")
        terminal_lines.append("*****************************")
        terminal_lines.append("")
        terminal_lines.append(f"Möchtest du mit Level {player.level + 1} starten? (Tippe 'start')")
    else:
        terminal_lines.append("[MISSION ABGESCHLOSSEN] Du hast alle Level geschafft!")
        terminal_lines.append(f"Gesamte Punkte: {player.points}")
        terminal_lines.append("*****************************")
        terminal_lines.append("")
        terminal_lines.append("Tippe 'ende', um das Spiel zu beenden.")
    waiting_for_next_level = True
    in_riddle = False

def run_game():
    """Hauptschleife: verarbeitet Input, steuert Level und Sound."""
    global user_input, in_riddle, current_answer, current_hint
    sm = SoundManager()
    sm.play_music()

    running = True
    clock = pygame.time.Clock()
    exit_to_menu = False
    last_warning = -1

    # Hacker‑Logs anzeigen
    for log in hacker_logs:
        terminal_lines.append(log)
        draw_terminal()
        if config.SOUND_ON:
            sm.play("type")
        time.sleep(1)

    # Haupt‑Loop
    while running:
        # Zeitlimit & Countdown‑Beep
        if level_start_time is not None:
            elapsed = time.time() - level_start_time
            if elapsed > time_limit:
                terminal_lines.append("")
                terminal_lines.append("⏰ [ZEIT ABGELAUFEN] Level verloren!")
                draw_terminal()
                time.sleep(2)
                running = False
                exit_to_menu = True
                continue
            remaining = int(time_limit - elapsed)
            if 0 < remaining <= 10 and remaining != last_warning:
                if config.SOUND_ON:
                    sm.play("beep")
                last_warning = remaining

        draw_terminal()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit_to_menu = True

            elif event.type == pygame.KEYDOWN:
                # Klick‑Sound bei jeder Taste
                if config.SOUND_ON:
                    sm.play("type")

                # ESC: Sofort abbrechen
                if event.key == pygame.K_ESCAPE:
                    terminal_lines.append("")
                    terminal_lines.append("[ABBRUCH] Spiel wird abgebrochen.")
                    if config.SOUND_ON:
                        sm.play("exit")
                    running = False
                    exit_to_menu = True
                    break

                # ENTER: Befehl verarbeiten
                elif event.key == pygame.K_RETURN:
                    terminal_lines.append("")
                    terminal_lines.append("> " + user_input)
                    cmd = user_input.lower().strip()

                    # Joker‑Hint
                    if cmd == "joker":
                        terminal_lines.append("")
                        terminal_lines.append("[HINT] " + (current_hint or "Kein Hinweis verfügbar."))
                        if config.SOUND_ON:
                            sm.play("prompt")
                        user_input = ""
                        break

                    # Immer «ende» möglich
                    elif cmd == "ende":
                        terminal_lines.append("")
                        terminal_lines.append("[ENDE] Das Spiel wird beendet.")
                        if config.SOUND_ON:
                            sm.play("exit")
                        running = False
                        exit_to_menu = True
                        user_input = ""
                        break

                    # Level‑Übergang
                    elif waiting_for_next_level:
                        if player.level < 5 and cmd == "start":
                            player.level_up()
                            start_game(sm)
                        else:
                            terminal_lines.append("")
                            terminal_lines.append("[FEHLER] Ungültiger Befehl.")
                    # Spiel starten oder Rätseleingabe
                    else:
                        if cmd == "start":
                            start_game(sm)
                        elif in_riddle:
                            answer_time = time.time() - riddle_start_time
                            if user_input.upper().strip() == current_answer:
                                terminal_lines.append("")
                                terminal_lines.append("✅ [ERFOLG] Richtige Antwort!")
                                if config.SOUND_ON:
                                    sm.play("success")
                                if answer_time < 10:
                                    bonus = 10 - int(answer_time)
                                    player.points += bonus
                                    terminal_lines.append(f"[BONUS] +{bonus} Punkte für Schnelligkeit.")
                                terminal_lines.append("")
                                player.solved_riddles += 1
                                in_riddle = False
                                ask_next_riddle(sm)
                            else:
                                terminal_lines.append("")
                                terminal_lines.append("❌ [FEHLER] Falsche Antwort.")
                                if config.SOUND_ON:
                                    sm.play("error")
                        else:
                            terminal_lines.append("")
                            terminal_lines.append("[FEHLER] Tippe 'start', um zu beginnen.")
                    user_input = ""

                # Rückschritt
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]

                # Normales Zeichen
                else:
                    user_input += event.unicode

        clock.tick(30)

    # Rückgabe der bis dahin erspielten Punkte
    return player.points

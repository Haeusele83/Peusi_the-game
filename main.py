import pygame
import time
import sys
import random

# Pygame initialisieren
pygame.init()

# Fenstergröße
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

# Farben
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# Schriftart
font = pygame.font.SysFont("Arial", 24)

# Terminal-Text speichern
terminal_lines = []
user_input = ""

# Simulierter Hacker-Log
hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum sicheren Server wird hergestellt...",
    "[WARNUNG] Firewall erkannt! Versuche, die Sperre zu umgehen...",
    "[ERFOLG] Zugriff gewährt. Willkommen, Agent.",
    "[EINGABE] Gib 'start' ein, um die erste Herausforderung zu starten:",
    ""
]

def draw_terminal():
    screen.fill(BLACK)
    y_offset = HEIGHT - 20
    for line in reversed(terminal_lines):
        text_surface = font.render(line, True, GREEN)
        screen.blit(text_surface, (10, y_offset))
        y_offset -= 25
    input_surface = font.render("> " + user_input, True, GREEN)
    screen.blit(input_surface, (10, HEIGHT - 20))
    pygame.display.flip()

def type_text(text, delay=0.05):
    for char in text:
        terminal_lines.append(char)
        draw_terminal()
        time.sleep(delay)
    terminal_lines.append("")

def run_game():
    global user_input
    running = True
    text_index = 0
    clock = pygame.time.Clock()
    
    while text_index < len(hacker_logs):
        terminal_lines.append(hacker_logs[text_index])
        draw_terminal()
        text_index += 1
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
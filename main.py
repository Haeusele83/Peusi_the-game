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

#Schriftart
font = pygame.font.SysFont("Arial", 24)

terminal_lines = []
user_input = ""

# Globale Variablen für den Spielstatus
in_riddle = False
current_answer = ""
cursor_visible = True
cursor_timer = pygame.time.get_ticks()
cursor_blink_speed = 500

time_limit = 300             # 5 Minuten in Sekunden
level_start_time = None      # Startzeit des aktuellen Levels
waiting_for_next_level = False

# Hacker-Logs
hacker_logs = [
    "[BOOT] System wird gestartet...",
    "[INFO] Verbindung zum Server wird hergestellt...",
    "[WARNUNG] Firewall erkannt! Versuche, die Sperre zu umgehen...",
    "[ERFOLG] Zugriff gewährt. Willkommen, Agent.",
    "[MISSION INFO] Bereite dich auf herausfordernde Missionen vor. Tippe 'start', um zu beginnen.",
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

def run_game():
    global user_input
    running = True
    clock = pygame.time.Clock()
    
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

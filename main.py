import pygame
from menu import MainMenu, OptionsScreen, HighscoreScreen, HighscoreEntryScreen
from game import run_game

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

clock = pygame.time.Clock()
current_screen = "menu"  # Mögliche Zustände: "menu", "options", "game", "highscore_entry", "highscore"

# Initialisiere die Screens
menu = MainMenu(screen)
options_screen = OptionsScreen(screen)
highscore_screen = None
highscore_entry_screen = None

running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    if current_screen == "menu":
        action = menu.update(events)
        menu.draw()
        if action == "start_game":
            current_screen = "game"
        elif action == "options":
            current_screen = "options"
        elif action == "highscores":
            current_screen = "highscore"
            highscore_screen = HighscoreScreen(screen)
        elif action == "quit":
            running = False

    elif current_screen == "options":
        action = options_screen.update(events)
        options_screen.draw()
        if action == "back":
            current_screen = "menu"

    elif current_screen == "game":
        # run_game() blockiert bis Spielende und gibt dann die erreichten Punkte zurück.
        score = run_game()
        # Immer in den Highscore-Eingabe-Screen wechseln, damit jeder Spieler seinen Score abspeichern kann.
        current_screen = "highscore_entry"
        highscore_entry_screen = HighscoreEntryScreen(screen, score)

    elif current_screen == "highscore_entry":
        name = highscore_entry_screen.update(events)
        highscore_entry_screen.draw()
        if name is not None and name != "":
            # Score in der Datenbank speichern.
            from highscores import update_highscores
            update_highscores(name, highscore_entry_screen.score)
            current_screen = "highscore"
            highscore_screen = HighscoreScreen(screen)

    elif current_screen == "highscore":
        action = highscore_screen.update(events)
        highscore_screen.draw()
        if action == "back":
            current_screen = "menu"

    clock.tick(30)

pygame.quit()

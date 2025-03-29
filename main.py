import pygame
from menu import MainMenu, OptionsScreen, HighscoreScreen, HighscoreEntryScreen, TestMenu, TestRiddleSummaryScreen, TestConnectionScreen, TestResetDBScreen
from game import run_game

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CyberHeist - Hacker Terminal")

clock = pygame.time.Clock()
current_screen = "menu"  # Zustände: "menu", "options", "game", "highscore_entry", "highscore", "test", "test_riddle_summary", "test_connection", "test_reset_db"

menu = MainMenu(screen, debug=True)
options_screen = OptionsScreen(screen)
highscore_screen = None
highscore_entry_screen = None
test_menu = None
test_riddle_summary_screen = None
test_connection_screen = None
test_reset_db_screen = None

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
        elif action == "test_modus":
            current_screen = "test"
            test_menu = TestMenu(screen)
        elif action == "quit":
            running = False

    elif current_screen == "options":
        action = options_screen.update(events)
        options_screen.draw()
        if action == "back":
            current_screen = "menu"

    elif current_screen == "game":
        score = run_game()
        current_screen = "highscore_entry"
        highscore_entry_screen = HighscoreEntryScreen(screen, score)

    elif current_screen == "highscore_entry":
        name = highscore_entry_screen.update(events)
        highscore_entry_screen.draw()
        if name is not None and name != "":
            from highscores import update_highscores
            update_highscores(name, highscore_entry_screen.score)
            current_screen = "highscore"
            highscore_screen = HighscoreScreen(screen)

    elif current_screen == "highscore":
        action = highscore_screen.update(events)
        highscore_screen.draw()
        if action == "back":
            current_screen = "menu"

    elif current_screen == "test":
        action = test_menu.update(events)
        test_menu.draw()
        if action == "test_highscore":
            current_screen = "highscore_entry"
            highscore_entry_screen = HighscoreEntryScreen(screen, 999)
        elif action == "test_riddle_summary":
            current_screen = "test_riddle_summary"
            test_riddle_summary_screen = TestRiddleSummaryScreen(screen)
        elif action == "test_connection":
            current_screen = "test_connection"
            test_connection_screen = TestConnectionScreen(screen)
        elif action == "test_reset_db":
            current_screen = "test_reset_db"
            test_reset_db_screen = TestResetDBScreen(screen)
        elif action == "back":
            current_screen = "menu"

    elif current_screen == "test_riddle_summary":
        action = test_riddle_summary_screen.update(events)
        test_riddle_summary_screen.draw()
        if action == "back":
            current_screen = "test"

    elif current_screen == "test_connection":
        action = test_connection_screen.update(events)
        test_connection_screen.draw()
        if action == "back":
            current_screen = "test"

    elif current_screen == "test_reset_db":
        action = test_reset_db_screen.update(events)
        test_reset_db_screen.draw()
        if action == "back":
            current_screen = "test"

    clock.tick(30)

pygame.quit()





import pygame
import config
from sound_manager import SoundManager
from highscores import load_highscores, reset_highscores
from riddles import Riddle
import random

class MainMenu:
    def __init__(self, screen, debug=False):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)
        self.options = ["Spiel starten", "Optionen", "Highscores", "Beenden"]
        if debug:
            self.options.append("Testmodus")
        self.selected = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    option = self.options[self.selected]
                    if option == "Spiel starten":
                        return "start_game"
                    elif option == "Optionen":
                        return "options"
                    elif option == "Highscores":
                        return "highscores"
                    elif option == "Beenden":
                        return "quit"
                    elif option == "Testmodus":
                        return "test_modus"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.font.render("Peusi-The Game", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        for idx, option in enumerate(self.options):
            color = (0, 255, 0) if idx == self.selected else (255, 255, 255)
            option_surface = self.font.render(option, True, color)
            self.screen.blit(option_surface, (100, 150 + idx * 50))
        pygame.display.flip()


class OptionsScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 28)
        # Sound‑Option initial nach config.SOUND_ON setzen
        sound_text = "Sound: ON" if config.SOUND_ON else "Sound: OFF"
        self.options = [
            sound_text,
            "Difficulty: Normal",
            "Zurück"
        ]
        self.selected = 0
        # SoundManager für play/stop Music
        self.sm = SoundManager()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    current = self.options[self.selected]
                    # Zurück
                    if current == "Zurück":
                        return "back"
                    # Sound‑Toggle
                    if current.startswith("Sound"):
                        config.SOUND_ON = not config.SOUND_ON
                        if config.SOUND_ON:
                            self.options[self.selected] = "Sound: ON"
                            self.sm.play_music()
                        else:
                            self.options[self.selected] = "Sound: OFF"
                            self.sm.stop_music()
                            pygame.mixer.stop()
                        return None
                    # Difficulty‑Toggle
                    if current.startswith("Difficulty"):
                        self.options[self.selected] = (
                            "Difficulty: Hard"
                            if "Normal" in current
                            else "Difficulty: Normal"
                        )
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.font.render("Optionen", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        for idx, option in enumerate(self.options):
            color = (0, 255, 0) if idx == self.selected else (255, 255, 255)
            opt_surf = self.font.render(option, True, color)
            self.screen.blit(opt_surf, (100, 150 + idx * 50))
        pygame.display.flip()


class HighscoreScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.highscores = load_highscores()

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "back"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Highscores", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        y_offset = 150
        if self.highscores:
            for idx, entry in enumerate(self.highscores):
                text = f"{idx+1}. {entry['name']} - {entry['score']}"
                entry_surface = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(entry_surface, (100, y_offset))
                y_offset += 40
        else:
            no_highscore = self.font.render("Noch keine Highscores vorhanden.", True, (255, 255, 255))
            self.screen.blit(no_highscore, (100, 150))
        back_text = self.font.render("Drücke Enter, um zurückzukehren.", True, (0, 255, 0))
        self.screen.blit(back_text, (100, y_offset + 20))
        pygame.display.flip()


class HighscoreEntryScreen:
    def __init__(self, screen, score):
        self.screen = screen
        self.score = score
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.player_name = ""
        self.prompt = "Gib deinen Namen ein: "
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_blink_speed = 500

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.player_name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Neuer Highscore!", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        score_surface = self.font.render(f"Deine Punkte: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (100, 120))
        prompt_surface = self.font.render(self.prompt + self.player_name, True, (255, 255, 255))
        self.screen.blit(prompt_surface, (100, 200))
        if pygame.time.get_ticks() - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = pygame.time.get_ticks()
        if self.cursor_visible:
            cursor_surface = self.font.render("_", True, (255, 255, 255))
            self.screen.blit(cursor_surface, (100 + prompt_surface.get_width(), 200))
        pygame.display.flip()


class TestMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)
        self.options = ["Test Highscore", "Test Rätseltypen", "Test Verbindung", "DB zurücksetzen", "Zurück"]
        self.selected = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    option = self.options[self.selected]
                    if option == "Test Highscore":
                        return "test_highscore"
                    elif option == "Test Rätseltypen":
                        return "test_riddle_summary"
                    elif option == "Test Verbindung":
                        return "test_connection"
                    elif option == "DB zurücksetzen":
                        return "test_reset_db"
                    elif option == "Zurück":
                        return "back"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.font.render("Testmodus", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        for idx, option in enumerate(self.options):
            color = (0, 255, 0) if idx == self.selected else (255, 255, 255)
            option_surface = self.font.render(option, True, color)
            self.screen.blit(option_surface, (100, 150 + idx * 50))
        pygame.display.flip()


class TestRiddleSummaryScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.summary = self.create_summary()

    def create_summary(self):
        summary_lines = []
        for typ, levels in Riddle.all_tasks.items():
            line = f"{typ.capitalize()}: "
            counts = []
            for level in sorted(levels.keys()):
                count = len(levels[level])
                counts.append(f"Level {level}: {count}")
            line += ", ".join(counts)
            summary_lines.append(line)
        return summary_lines

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "back"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Rätseltypen Übersicht", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        y = 120
        for line in self.summary:
            line_surface = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(line_surface, (100, y))
            y += 40
        back_surface = self.font.render("Drücke Enter, um zurückzukehren.", True, (0, 255, 0))
        self.screen.blit(back_surface, (100, y + 20))
        pygame.display.flip()


class TestConnectionScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.messages = []
        self.test_connections()

    def test_connections(self):
        try:
            import player
            _ = player.Player()
            self.messages.append("Player Modul: OK")
        except Exception as e:
            self.messages.append("Player Modul: Fehler " + str(e))
        try:
            Riddle.init_tasks_for_level(1)
            self.messages.append("Riddles Modul: OK")
        except Exception as e:
            self.messages.append("Riddles Modul: Fehler " + str(e))
        try:
            _ = load_highscores()
            self.messages.append("Highscore DB: OK")
        except Exception as e:
            self.messages.append("Highscore DB: Fehler " + str(e))

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "back"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("Verbindungstest", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        y = 120
        for msg in self.messages:
            msg_surface = self.font.render(msg, True, (255, 255, 255))
            self.screen.blit(msg_surface, (100, y))
            y += 40
        back_surface = self.font.render("Drücke Enter, um zurückzukehren.", True, (0, 255, 0))
        self.screen.blit(back_surface, (100, y + 20))
        pygame.display.flip()


class TestResetDBScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 36)
        self.message = ""
        self.reset_db()

    def reset_db(self):
        try:
            reset_highscores()
            self.message = "Highscore-Datenbank wurde zurückgesetzt."
        except Exception as e:
            self.message = "Fehler beim Zurücksetzen: " + str(e)

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return "back"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.title_font.render("DB zurücksetzen", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        msg_surface = self.font.render(self.message, True, (255, 255, 255))
        self.screen.blit(msg_surface, (100, 150))
        back_surface = self.font.render("Drücke Enter, um zurückzukehren.", True, (0, 255, 0))
        self.screen.blit(back_surface, (100, 250))
        pygame.display.flip()




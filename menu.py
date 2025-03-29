import pygame
from highscores import load_highscores

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 36)
        self.options = ["Spiel starten", "Optionen", "Highscores", "Beenden"]
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
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.font.render("CyberHeist", True, (0, 255, 0))
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
        self.options = ["Sound: ON", "Difficulty: Normal", "Tastenbelegung", "Zurück"]
        self.selected = 0

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    current_option = self.options[self.selected]
                    if current_option == "Zurück":
                        return "back"
                    # Toggle-Logik:
                    if current_option.startswith("Sound"):
                        if "ON" in current_option:
                            self.options[self.selected] = "Sound: OFF"
                        else:
                            self.options[self.selected] = "Sound: ON"
                    elif current_option.startswith("Difficulty"):
                        if "Normal" in current_option:
                            self.options[self.selected] = "Difficulty: Hard"
                        else:
                            self.options[self.selected] = "Difficulty: Normal"
        return None

    def draw(self):
        self.screen.fill((0, 0, 0))
        title_surface = self.font.render("Optionen", True, (0, 255, 0))
        self.screen.blit(title_surface, (100, 50))
        for idx, option in enumerate(self.options):
            color = (0, 255, 0) if idx == self.selected else (255, 255, 255)
            option_surface = self.font.render(option, True, color)
            self.screen.blit(option_surface, (100, 150 + idx * 50))
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
        self.screen.blit(back_text, (100, y_offset+20))
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

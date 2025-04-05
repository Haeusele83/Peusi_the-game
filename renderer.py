import pygame
import time

class Renderer:
    def __init__(self, screen, font, colors, dimensions):
        """
        :param screen: Das Pygame-Fenster
        :param font: Das verwendete Font-Objekt
        :param colors: Dictionary mit Farbinformationen, z. B. {"BLACK": (0,0,0), "GREEN": (0,255,0)}
        :param dimensions: Dictionary mit Dimensionen, z. B. {"WIDTH": 1000, "HEIGHT": 600}
        """
        self.screen = screen
        self.font = font
        self.BLACK = colors.get("BLACK", (0, 0, 0))
        self.GREEN = colors.get("GREEN", (0, 255, 0))
        self.WIDTH = dimensions.get("WIDTH", 1000)
        self.HEIGHT = dimensions.get("HEIGHT", 600)
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()
        self.cursor_blink_speed = 500

    def draw_terminal(self, terminal_lines, user_input, level_start_time, time_limit):
        """
        Zeichnet das Terminal inklusive aller Zeilen, Countdown und Eingabezeile.
        """
        self.screen.fill(self.BLACK)
        line_height = 25
        input_area_height = 40
        terminal_area_height = self.HEIGHT - input_area_height - 10
        max_lines = terminal_area_height // line_height

        # Countdown-Anzeige, falls ein Level läuft
        if level_start_time is not None:
            elapsed = time.time() - level_start_time
            remaining = max(0, int(time_limit - elapsed))
            minutes = remaining // 60
            seconds = remaining % 60
            countdown_text = f"Restzeit: {minutes:02d}:{seconds:02d}"
            countdown_surface = self.font.render(countdown_text, True, self.GREEN)
            self.screen.blit(countdown_surface, (self.WIDTH - countdown_surface.get_width() - 10, 10))

        displayed_lines = terminal_lines[-max_lines:]
        y_offset = 10
        for line in displayed_lines:
            text_surface = self.font.render(line, True, self.GREEN)
            self.screen.blit(text_surface, (10, y_offset))
            y_offset += line_height

        # Zeichne Trennlinie
        pygame.draw.line(self.screen, self.GREEN, (0, self.HEIGHT - input_area_height), (self.WIDTH, self.HEIGHT - input_area_height), 2)

        # Blinkender Cursor
        if pygame.time.get_ticks() - self.cursor_timer > self.cursor_blink_speed:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = pygame.time.get_ticks()

        input_text = "> " + user_input + ("_" if self.cursor_visible else "")
        input_surface = self.font.render(input_text, True, self.GREEN)
        self.screen.blit(input_surface, (10, self.HEIGHT - input_area_height + (input_area_height - line_height) // 2))
        pygame.display.flip()

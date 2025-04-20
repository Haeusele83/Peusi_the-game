import pygame
import config

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.effects = {}
        if config.SOUND_ON:
            for key, fname in config.SOUNDS.items():
                path = config.SOUND_FOLDER + fname
                snd = pygame.mixer.Sound(path)
                snd.set_volume(config.VOLUME["effects"])
                self.effects[key] = snd
        self._music_channel = None

    def play(self, key):
        if config.SOUND_ON and key in self.effects:
            self.effects[key].play()

    def play_music(self):
        """Spielt den Ambient‑Sound endlos via Sound-Channel."""
        if config.SOUND_ON and "ambient" in self.effects:
            ambient = self.effects["ambient"]
            ambient.set_volume(config.VOLUME["music"])
            self._music_channel = ambient.play(loops=-1)

    def stop_music(self):
        """Stoppt die Ambient‑Schleife."""
        if self._music_channel:
            self._music_channel.stop()



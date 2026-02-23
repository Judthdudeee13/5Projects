from settings import *

class AssetManager:
    def __init__(self):
        self.images = {}
        self.audio = {}
        self.fonts = {}

    def load_images(self, base_path, entity_name):
        frames = {}
        for folder_paths, sub_folders, file_names in walk(base_path):
            for folder in sub_folders:
                frames[folder] = []
            break
        
        if frames.keys():
            for state in frames.keys():
                for folder_path, sub_folders, file_names in walk(join(base_path, state)):
                    if file_names:
                            for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                                full_path = join(folder_path, file_name)
                                surf = pygame.image.load(full_path).convert_alpha()
                                surf = pygame.transform.scale(surf, (int(surf.get_width() * SCALE), int(surf.get_height() * SCALE)))
                                frames[state].append(surf)
        else:
            for folder_path, sub_folders, file_names in walk(base_path):
                if file_names:
                    for file_name in file_names:
                        frames[file_name.split('.')[0]] = []
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        surf = pygame.transform.scale(surf, (int(surf.get_width() * SCALE), int(surf.get_height() * SCALE)))
                        frames[file_name.split('.')[0]].append(surf)
        self.images[entity_name] = frames

    def get(self, entity):
        return self.images[entity]
    
    def load_audio(self, file_path, volume, name):
        audio = pygame.mixer.Sound(file_path)
        audio.set_volume(volume/100)
        self.audio[name] = audio

    def play_audio(self, name, duration=0):
        self.audio[name].play(duration)

    def load_music(self, path):
        pygame.mixer.music.load(path)

    def play_music(self, loops=-1, volume=0.5, fade_ms=0):
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(loops=loops, fade_ms=fade_ms)

    def stop_music(self, fade_ms=0):
        pygame.mixer.music.fadeout(fade_ms)

    def load_font(self, file_path, name, size):
        self.fonts[name] = pygame.font.Font(file_path, int(size*SCALE))
        
    def get_font(self, name):
        return self.fonts[name]

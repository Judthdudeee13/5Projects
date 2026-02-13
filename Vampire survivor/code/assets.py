from settings import *

class AssetManager:
    def __init__(self):
        self.images = {}

    def load_images(self, folder_path, entity_name):
        self.images[entity_name] = {}
        self.frames = {'left': [], 'right': [], 'up': [], 'down': []}
        for state in self.frames.keys():
            for folder_path, sub_folders, file_names in walk(join(folder_path, state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        self.frames[state].append(surf)

    def get(self, entity):
        return self.images[entity]
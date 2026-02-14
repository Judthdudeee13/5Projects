from settings import *

class AssetManager:
    def __init__(self):
        self.images = {}

    def load_images(self, folder_path, entity_name):
        frames = {}
        self.images[entity_name] = {}
        for folder_path, sub_folders, file_name in walk(folder_path):
            frames[sub_folders] = {}
            print(frames)
        for state in frames.keys():
            for folder_path, sub_folders, file_names in walk(join(folder_path, state)):
                if file_names:
                    for file_name in sorted(file_names, key= lambda name: int(name.split('.')[0])):
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        frames[state].append(surf)
        print(self.images)

    def get(self, entity):
        return self.images[entity]
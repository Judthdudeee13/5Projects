from settings import *

class AssetManager:
    def __init__(self):
        self.images = {}

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
                                frames[state].append(surf)
        else:
            for folder_path, sub_folders, file_names in walk(base_path):
                if file_names:
                    for file_name in file_names:
                        frames[file_name.split('.')[0]] = []
                        full_path = join(folder_path, file_name)
                        surf = pygame.image.load(full_path).convert_alpha()
                        frames[file_name.split('.')[0]].append(surf)
        self.images[entity_name] = frames

    def get(self, entity):
        return self.images[entity]
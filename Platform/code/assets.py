from settings import *

class Assets:
    def __init__(self):
        self.assets = {}
    def import_image(self, name, *path, format='png', alpha=True):
        full_path = join(*path)+f'.{format}'
        surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
        self.assets[name] = surf

    def import_folder(self, name, *path):
        frames = []
        for folder_path, sub_folders, file_names in walk(join(*path)):
            for file_name in sorted(file_names, key = lambda name: int(name.split('.')[0])):
                full_path = join(folder_path, file_name)
                surf = pygame.image.load(full_path)
                frames.append(surf)
        self.assets[name] = frames

    def import_audio(self, name, format, *path):
        self.assets[name] = join(*path)+f'.{format}'

    def load_asset(self, name):
        return self.assets[name]
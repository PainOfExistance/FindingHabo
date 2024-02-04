from game_manager import ClassManager as CM


class WorldManager:
    def __init__(self):
        pass
    
    def save(self, data, path):
        with open(path, 'w') as file:
            file.write(data)

    def load(self, path):
        with open(self.path, 'r') as file:
            return file.read()
        



class SaveManager:
    def __init__(self, path):
        self.path = path

    def save(self, data):
        with open(self.path, 'w') as file:
            file.write(data)

    def load(self):
        with open(self.path, 'r') as file:
            return file.read()
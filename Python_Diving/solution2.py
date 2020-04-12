import os

class FileReader:
    def __init__(self, path):
        self.path = path
        pass
    def read(self):
        if os.path.exists(self.path):
            with open(self.path) as f:
                try:
                    return f.read()
                except FileNotFoundError:
                    return ''
        else:
            return '' 
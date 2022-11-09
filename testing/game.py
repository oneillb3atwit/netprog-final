import json

class Player:
    def __init__(self):
        self.id = len(players)
        self.x = 0
        self.y = 0
    def __init__(self, data):
        self.update(data)
    def get_json(self):
        return {'id': self.id, 'x': self.x, 'y': self.y}
    def update(self, data):
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']

players = []

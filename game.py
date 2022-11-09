import json

HOST = 'localhost'
PORT = 8000

WINSIZE = (640, 480)
PLAYERSIZE = (64, 64)
PLAYERSPEED = 8
BALLSIZE = (64, 64)
BALLSPEED = 4
CLIENT_CONNECT_MESSAGE = "hello"
CLIENT_DISCONNECT_MESSAGE = "goodbye"

players = []
ball = None

class Player:
    def __init__(self, data):
        self.update(data)
        self.bounds = PLAYERSIZE

    def get_json(self):
        return {'id': self.id, 'x': self.x, 'y': self.y, 'team': self.team}

    def update(self, data):
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.team = data['team']

    def move(self, x_change, y_change):
        newx = self.x + (x_change * PLAYERSPEED)
        newy = self.y + (y_change * PLAYERSPEED)

        if newx <= 0:
            self.x = 0
        elif newx >= WINSIZE[0] - self.bounds[0]:
            self.x = WINSIZE[0] - self.bounds[0]
        else:
            self.x += x_change * PLAYERSPEED

        if newy <= 0:
            self.y = 0
        elif newy >= WINSIZE[1] - self.bounds[1]:
            self.y = WINSIZE[1] - self.bounds[1]
        else:
            self.y += y_change * PLAYERSPEED

class Ball:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_direction = 1
        self.y_direction = 1

    def handle_collision(self):
        # wall collision
        if self.x + BALLSIZE[0] >= WINSIZE[0]:
            self.x_direction = -1
        if self.x <= 0:
            self.x_direction = 1
        if self.y + BALLSIZE[1] >= WINSIZE[1]:
            self.y_direction = -1
        if self.y <= 0:
            self.y_direction = 1

        # player collision
        for p in players:
            xmin = p.x
            ymin = p.y
            xmax = p.x + p.bounds[0]
            ymax = p.y + p.bounds[1]

            if self.x <= xmax and self.y <= ymax and self.x >= p.x and self.y >= p.y:
               self.x_direction *= -1

    def move(self):
        self.handle_collision()
        self.x += self.x_direction * BALLSPEED
        self.y += self.y_direction * BALLSPEED

    def update(self, data):
        self.x = data['x']
        self.y = data['y']

    def get_json(self):
        return {'x': self.x, 'y': self.y}

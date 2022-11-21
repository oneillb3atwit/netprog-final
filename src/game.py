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
    """
    Represents a player in the game.

    Attributes
    ----------
    id : int
        The player ID (by default assigned from player count in server.py).
    x : int
        x position of the player.
    y : int
        y position of the player.
    team : int
        the player's team (0: left, or 1: right).
    bounds : (int, int)
        the size of the player sprite in the window.

    Methods
    -------
    get_json()
        Returns relevant JSON data to transfer between the client and server.
    move(x_change, y_change)
        Moves the player in the map by x_change * PLAYERSPEED and
        y_change * PLAYERSPEED.
    """

    def __init__(self, data):
        """
        Parameters
        ----------
        data : dict
            Values of self.id, self.x, self.y, and self.team in a dict object
        """
        self.update(data)
        self.bounds = PLAYERSIZE

    def get_json(self):
        """
        Returns a dict of relevant data for transfer between the client and server.

        Returns
        -------
        dict
            a list of relevant data to transfer
        """
        return {'id': self.id, 'x': self.x, 'y': self.y, 'team': self.team}

    def move(self, x_change, y_change):
        """
        Moves the player by x_change * PLAYERSPEED and y_change * PLAYERSPEED.
        Also handles wall collision.

        Parameters
        ----------
        x_change : int
            the change in x value
        y_change : int
            the change in y value
        """
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

    def update(self, data):
        """
        Updates the object to match values in the data parameter.
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        self.id = data['id']
        self.x = data['x']
        self.y = data['y']
        self.team = data['team']

class Ball:
    """
    Represents the ball in the game.

    Attributes
    ----------
    x : int
        The x value of the ball in the map
    y : int
        The y value of the ball in the map
    x_direction : int
        The x direction of the ball's movement (-1: left, 1: right)
    y_direction : int
        The y direction of the ball's movement (-1: up, 1: down)
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_direction = 1
        self.y_direction = 1

    def get_json(self):
        """
        Returns a dict of relevant data for transfer between the client and server.

        Returns
        -------
        dict
            a list of relevant data to transfer
        """
        return {'x': self.x, 'y': self.y}

    def handle_collision(self):
        """
        Handles player and wall collision.
        """
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

            if self.x <= xmax and self.y <= ymax and self.x >= xmin and self.y >= ymin:
               self.x_direction *= -1
               

    def move(self):
        """
        Moves the ball based on the direction and collision status
        """
        self.handle_collision()
        self.x += self.x_direction * BALLSPEED
        self.y += self.y_direction * BALLSPEED

    def update(self, data):
        """
        Updates the object to match values in the data parameter.
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        self.x = data['x']
        self.y = data['y']


from engine.game import *
from engine.client import *
from engine.server import *
import pygame, math

PLAYERSIZE = (64, 64)
PLAYERSPEED = 8
BALLSIZE = (64, 64)
BALLSPEED = 4
NETSIZE = (20, 480)

player_img = pygame.image.load('img/player.png')
player_img_rect = player_img.get_rect()
ball_img = pygame.image.load('img/ball.png')
ball_img_rect = ball_img.get_rect()

class Player(DrawableObject):
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
    get_dict() : dict
        Returns relevant data in dict format to transfer between the client and server.
    move(x_change, y_change)
        Moves the player in the map by x_change * PLAYERSPEED and
        y_change * PLAYERSPEED.
    """

    def __init__(self, data=None):
        """
        Parameters
        ----------
        data : dict
            Values of self.id, self.x, self.y, and self.team in a dict object
        """
        if data == None:
            self.x = 0
            self.y = 0
            self.team = 0
        else:
            self.client_update(data)

        self.sprite = pygame.image.load('img/player.png')
        self.bounds = (self.x + PLAYERSIZE[0], self.y + PLAYERSIZE[1])

    def client_update(self, data):
        """
        Updates the object to match values in the data parameter.
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        self.id = data['id']
        if data['id'] != self.id:
            return
        self.x = data['x']
        self.y = data['y']
        self.team = data['team']
        self.bounds = (self.x + PLAYERSIZE[0], self.y + PLAYERSIZE[1])

    def get_dict(self):
        """
        Returns a dict of relevant data for transfer between the client and server.

        Returns
        -------
        dict
            a list of relevant data to transfer
        """
        return {'type': 'Player', 'id': self.id, 'x': self.x, 'y': self.y, 'team': self.team}

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
        newx = self.x + x_change * PLAYERSPEED
        newy = self.y + y_change * PLAYERSPEED
        
        change_vec = [x_change, y_change]
        change_vec_magnitude = math.sqrt(pow(change_vec[0], 2) + pow(change_vec[1], 2))

        if change_vec[0] > 0:
            newx = self.x + ((change_vec[0]/change_vec_magnitude) * PLAYERSPEED)
        if change_vec[1] > 0:
            newy = self.y + ((change_vec[1]/change_vec_magnitude) * PLAYERSPEED)

        if newx <= (WINSIZE[0] / 2) * self.team:
            self.x = (WINSIZE[0] / 2) * self.team
        elif newx >= ((WINSIZE[0] / 2) * (self.team + 1))  - self.bounds[0]:
            self.x = ((WINSIZE[0] / 2) * (self.team + 1)) - self.bounds[0]
        else:
            self.x = newx

        if newy < 0:
            self.y = 0
        elif newy >= WINSIZE[1] - self.bounds[1]:
            self.y = WINSIZE[1] - self.bounds[1]
        else:
            self.y = newy

    def handle_inputs(self, keys):
        """
        Handles player movement based on key presses

        Parameters
        ----------
        player : Player
            The Player object to modify
        keys : list(str)
            The client's currently pressed keys

        """
        x = 0
        y = 0
        if pygame.K_w in keys:
            y -= 1
        if pygame.K_a in keys:
            x -= 1
        if pygame.K_s in keys:
            y += 1
        if pygame.K_d in keys:
            x += 1
        self.move(x, y)

    def server_update(self, data):
        """
        Runs the game logic on the server
        This is equivalent to an update function in a single player game
        """
        if data['id'] != self.id:
            return
        self.handle_inputs(data['keys'])

class Ball(DrawableObject):
    """
    Represents the ball in the tennis game.

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

    def __init__(self, data=None):
        """
        Initializes the Ball.
        
        Parameters
        ----------
        data : dict
            pre-set values if retrieved from the server.
        """
        self.sprite = pygame.image.load('img/ball.png')
        if data == None:
            self.x = 0
            self.y = 0
            self.x_direction = 1
            self.y_direction = 1
        else:
            self.client_update(data)

    def client_update(self, data):
        """
        Updates the object to match values in the data parameter.
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        self.x = data['x']
        self.y = data['y']


    def get_dict(self):
        """
        Returns
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        return {'type': 'Ball', 'x': self.x, 'y': self.y}

    def handle_collision(self):
        """
        Handles player and wall collision.
        """
        if self.x + BALLSIZE[0] >= WINSIZE[0]:
            self.x_direction = -1
        if self.x <= 0:
            self.x_direction = 1
        if self.y + BALLSIZE[1] >= WINSIZE[1]:
            self.y_direction = -1
        if self.y <= 0:
            self.y_direction = 1

    def move(self):
        """
        Moves the ball based on the direction and collision status
        """
        self.handle_collision()
        self.x += self.x_direction * BALLSPEED
        self.y += self.y_direction * BALLSPEED

    def server_update(self, data):
        """
        Runs the game logic on the server
        This is equivalent to an update function in a single player game

        Parameters
        ----------
        keys : list(str)
            The client's currently pressed keys
        """
        self.move()

class TennisClient(GameClient):
    def __init__(self, id, server_host, server_port, game_objects=[]):
        """
        Initialize the client.

        Parameters
        ----------
        id : int
            the client ID
        server_host : str
            the address of the server to connect to
        server_port : int
            the port of the server to connect to
        """
        super(TennisClient, self).__init__(id, server_host, server_port, game_objects)
        self.key_filter = [ pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d ]

    def serialize_game_objects(self, data):
        """
        Convert all elements data to their corresponding GameObjects and places
        the results in self.game_objects.

        Parameters
        ----------
        data : dict
            the data received from the server to store
        """
        self.game_objects = []
        for o in data['game_objects']:
            if o['type'] == "Player":
                self.game_objects.append(Player(o))
            elif o['type'] == "Ball":
                self.game_objects.append(Ball(o))

class TennisServer(GameServer):
    def __init__(self, server_host, server_port):
        """
        Initializes the server.

        Parameters
        ----------
        server_host : str
            the hostname or IP to bind to
        server_port : int
            the port to bind to
        """
        super(TennisServer, self).__init__(server_host, server_port)
        self.game_objects.append(Ball())

    def add_client(self, addr):
        """
        Adds a client to the server (called on new connection by the
        superclass).

        Parameters
        ----------
        addr : tuple(str, int)
            the address and port for the new client.
        """
        self.clients.append(addr)
        player = Player()
        player.id = len(self.clients)
        self.game_objects.append(player)
        return len(self.clients)

args = parse_args()
if args['server'] == True:
    print("Starting server")
    TennisServer(HOST, PORT).start()
else:
    print("Starting client")
    TennisClient(0, HOST, PORT).start()

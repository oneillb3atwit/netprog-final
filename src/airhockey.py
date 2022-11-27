from engine.game import *
from engine.client import *
from engine.server import *
import pygame

PLAYERSIZE = (64, 64)
PUCKSIZE = (64, 64)
GOALBOUNDS = (20, 100)
PUCKMAXSPEED = 50



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
    x_vel : int
        x velocity of the player (current x - prev x), server side
    y_vel : int
        y velocity of the player (current y - prev y), server side
    team : int
        the player's team (0: left, or 1: right).
    bounds : (int, int)
        the size of the player sprite in the window.

    Methods
    -------
    get_dict() : dict
        Returns relevant data in dict format to transfer between the client and server.
    move(pos)
        Moves the player to pos[0] as x and pos[1] as y
    """

    def __init__(self, data=None):
        """
        Parameters
        ----------
        data : dict
            Values of self.id, self.x, self.y, and self.team in a dict object
        """
        self.type = 'Player'
        if data == None:
            self.x = 0
            self.y = 0
            self.team = 0
        else:
            self.client_update(data)
        self.x_vel = 0
        self.y_vel = 0
        self.sprite = pygame.image.load('img/airhockey/paddle.png')
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

    def move(self, pos):
        """
        Moves the player to the mouse position within its bounds

        Parameters
        ----------
        x_change : int
            the change in x value
        y_change : int
            the change in y value
        """

        self.x_vel = self.x - pos[0]
        self.y_vel = self.y - pos[1]

        if pos[0] <= (WINSIZE[0] / 2) * self.team:
            self.x = (WINSIZE[0] / 2) * self.team
        elif pos[0] >= ((WINSIZE[0] / 2) * (self.team + 1))  - self.bounds[0]:
            self.x = ((WINSIZE[0] / 2) * (self.team + 1)) - self.bounds[0]
        else:
            self.x = pos[0]

        if pos[1] < 0:
            self.y = 0
        elif pos[1] >= WINSIZE[1] - self.bounds[1]:
            self.y = WINSIZE[1] - self.bounds[1]
        else:
            self.y = pos[1]

    def server_update(self, data):
        """
        Runs the game logic on the server
        This is equivalent to an update function in a single player game
        """
        if data['id'] != self.id:
            return
        self.move(data['mouse_pos'])

class Puck(DrawableObject):
    """
    Represents the puck in the tennis game.

    Attributes
    ----------
    x : int
        The x value of the puck in the map
    y : int
        The y value of the puck in the map
    x_vel : int
        The x velocity of the puck (-1: left, 1: right)
    y_vel : int
        The y velocity of the puck (-1: up, 1: down)
    """

    def __init__(self, data=None):
        """
        Initializes the puck.
        
        Parameters
        ----------
        data : dict
            pre-set values if retrieved from the server.
        """
        self.type = 'Puck'
        self.sprite = pygame.image.load('img/airhockey/puck.png')
        if data == None:
            self.x = 272
            self.y = 272
            self.x_vel = 0
            self.y_vel = 0
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
        return {'type': 'Puck', 'x': self.x, 'y': self.y}

    def handle_collision(self, game_objects):
        """
        Handles player and wall collision.
        """
        # collision goes here :D
        for g in game_objects:
            if (g.type == 'Player'):
                puckrect = pygame.Rect(self.x, self.y, PUCKSIZE[0], PUCKSIZE[1])
                playerrect = pygame.Rect(g.x, g.y, PLAYERSIZE[0], PLAYERSIZE[1]) 
                if (puckrect.colliderect(playerrect)):
                    print('colliding')
                    self.x_vel = max(min(PUCKMAXSPEED, -g.x_vel), -PUCKMAXSPEED)
                    self.y_vel = max(min(PUCKMAXSPEED, -g.y_vel), -PUCKMAXSPEED)
                    self.x += self.x_vel * 1.1
                    self.y += self.y_vel * 1.1
        if (self.x <= 0 or self.x >= WINSIZE[0]):
            self.x_vel *= -1
        if (self.y <= 0 or self.y >= WINSIZE[1]):
            self.y_vel *= -1
            
    def move(self):
        """
        Moves the puck based on the direction and collision status
        """
        self.x += self.x_vel * 1.1
        self.y += self.y_vel * 1.1

    def reset_puck(self):
        self.x = 272
        self.y = 272
        self.x_vel = 0
        self.y_vel = 0

    def server_update(self, game_objects):
        """
        Runs the game logic on the server
        This is equivalent to an update function in a single player game

        Parameters
        ----------
        keys : list(str)
            The client's currently pressed keys
        """
        self.handle_collision(game_objects)
        self.move()

class AirHockeyClient(GameClient):
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
        super(AirHockeyClient, self).__init__(id, server_host, server_port, game_objects)
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
            elif o['type'] == "Puck":
                self.game_objects.append(Puck(o))

class AirHockeyServer(GameServer):
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
        super(AirHockeyServer, self).__init__(server_host, server_port)
        self.game_objects.append(Puck())

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
        player.team = len(self.clients) % 2
        self.game_objects.append(player)
        return len(self.clients)
    def game_loop(self):
        """
        The main server loop. Overriding to send server info to the puck object
        """
        self.running = True
        while self.running:
            data, addr = self.sock.recvfrom(1024)
            game_objects_json = []
            for o in self.game_objects:
                game_objects_json.append(o.get_dict())

            if data == None: break
            data = str(data)[2:-1]
            if data == CLIENT_CONNECT_MESSAGE:
                client_id = self.add_client(addr)
                response = bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8')
                self.sock.sendto(bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8'), addr)
                continue

            try:
                data_dict = json.loads(data)
                client_id = data_dict['id']
                for o in self.game_objects:
                    if (o.type == 'Puck'):
                        o.server_update(self.game_objects)
                    else:
                        o.server_update(data_dict)
            except ValueError as e:
                printd('Malformed packet received.')
            self.sock.sendto(bytes(json.dumps({'id': client_id, 'game_objects': game_objects_json}), encoding='utf-8'), addr)
        self.halt()

args = parse_args()
if 'debug' in args:
    debug = True
if 'host' in args:
    HOST = args['host']
if 'port' in args:
    PORT = args['port']

if args['server'] == True:
    print('Starting server')
    AirHockeyServer(HOST, PORT).start()
else:
    print('Starting client')
    AirHockeyClient(0, HOST, PORT).start()

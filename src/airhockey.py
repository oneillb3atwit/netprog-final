from engine.game import *
from engine.client import *
from engine.server import *
import pygame

PLAYERSIZE = (64, 64)
PUCKSIZE = (64, 64)
GOALBOUNDS = (10, 100)
PUCKMINSPEED = 1
PUCKMAXSPEED = 8
MAX_SCORE = 7
BG_IMG = pygame.image.load("img/airhockey/bg.png")

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
        self.can_hit = True
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
            self.x_vel = 0
        elif pos[0] >= ((WINSIZE[0] / 2) * (self.team + 1))  - self.bounds[0]:
            self.x = ((WINSIZE[0] / 2) * (self.team + 1)) - self.bounds[0]
            self.x_vel = 0
        else:
            self.x = pos[0]

        if pos[1] < 0:
            self.y = 0
            self.y_vel = 0
        elif pos[1] >= WINSIZE[1] - self.bounds[1]:
            self.y = WINSIZE[1] - self.bounds[1]
            self.y_vel = 0
        else:
            self.y = pos[1]

    def reset_pos(self):
        if self.team == 0:
            self.x = 0
        else:
            self.x = WINSIZE[0]
        self.y = 240
    def server_update(self, data):
        """
        Runs the game logic on the server
        This is equivalent to an update function in a single player game
        """
        if data['id'] != self.id:
            return
        self.move(data['mouse_pos'])

class GameManager(GameObject):
    """
    Handles game logic

    Attributes
    ----------
    score : int[]
        The current score
    """

    def __init__(self):
        self.score = [0,0]
        self.type = 'GameManager'

    def client_update(self, data):
        """
        Updates the object to match values in the data parameter.
        This object only updates the score on the client. Not important otherwise

        Parameters
        ----------
        data : dict
            new values for the object.
        """
        self.score = data['score']

    def restart(self):
        self.score = [0,0]

    def get_dict(self):
        """
        Returns
        
        Parameters
        ----------
        data : dict
            new values for the object.
        """
        return {'type': 'GameManager', 'score': self.score}
    def server_update(self, data):
        printd(str(self.score))

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
            self.x = 240
            self.y = 208
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
        puckrect = pygame.Rect(self.x + 10, self.y + 10, PUCKSIZE[0] - 10, PUCKSIZE[1] - 10) # i am lying about the hitbox :)
        for g in game_objects:
            if (g.type == 'Player'):
                playerrect = pygame.Rect(g.x, g.y, PLAYERSIZE[0], PLAYERSIZE[1]) 
                if (puckrect.colliderect(playerrect)):
                    if (g.can_hit):
                        print(str(g.x_vel) + " " + str(g.y_vel))
                        if (g.x_vel == 0):
                            self.x_vel = -self.x_vel * 0.7
                        else:
                            gdir = 1
                            if (g.x_vel != 0):
                                gdir = g.x_vel/abs(g.x_vel)
                            speed = min(abs(g.x_vel/8), PUCKMAXSPEED)
                            self.x_vel = self.x_vel - speed * gdir
                        if (g.y_vel == 0):
                            self.y_vel = -self.y_vel * 0.7
                        else:
                            gdir = 1
                            if (g.y_vel != 0):
                                gdir = g.y_vel/abs(g.y_vel)
                            speed = min(abs(g.y_vel/8), PUCKMAXSPEED)
                            self.y_vel = self.y_vel - speed * gdir
                        self.x += self.x_vel
                        self.y += self.y_vel
                        g.can_hit = False
                else:
                    g.can_hit = True
        if (self.x <= 0):
            self.x_vel *= -0.7
            self.x = 0
        if (self.x + PUCKSIZE[0] >= WINSIZE[0]):
            self.x_vel *= -0.7
            self.x = WINSIZE[0] - PUCKSIZE[0]
        if (self.y <= 0):
            self.y_vel *= -0.7
            self.y = 0
        if (self.y + PUCKSIZE[1] >= WINSIZE[1]):
            self.y_vel *= -0.7
            self.y = WINSIZE[1] - PUCKSIZE[1]
                    
        goalrect_l = pygame.Rect(-GOALBOUNDS[0]/2, 240 - GOALBOUNDS[1]/2, GOALBOUNDS[0], GOALBOUNDS[1])
        goalrect_r = pygame.Rect(WINSIZE[0] - GOALBOUNDS[0]/2, 240 - GOALBOUNDS[1]/2, GOALBOUNDS[0], GOALBOUNDS[1])
        if puckrect.colliderect(goalrect_l):
            self.score(game_objects, 0)
        if puckrect.colliderect(goalrect_r):
            self.score(game_objects, 1)
    
    def score(self, game_objects, side):
        """
        Handles scoring a goal
        Side - 0 is left, 1 is right
        """
        self.reset_puck(side)
        for g in game_objects:
            if (g.type == 'Player'):
                g.can_hit = 20
            if (g.type == 'GameManager'):
                g.score[side] += 1
                if g.score[side] == MAX_SCORE:
                    g.restart()
        print(str(self.score))

    def move(self):
        """
        Moves the puck based on the direction and collision status
        """
        self.x += self.x_vel
        self.y += self.y_vel

    def reset_puck(self, side):
        self.x = 208 + (side * PUCKSIZE[0])
        self.y = 208
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
        
    def draw(self):
        """
        Draws all DrawableObjects in game_objects to the screen
        """
        if self.game_objects == None:
            return
        self.screen.blit(BG_IMG, pygame.Rect(0, 0, WINSIZE[0], WINSIZE[1]))
        for o in self.game_objects:
            if isinstance(o, DrawableObject):
                o.draw(self.screen)
        pygame.display.flip()

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
        self.game_objects.append(GameManager())
        self.game_objects.append(Puck())
        self.playing = False

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
                if (len(self.clients) > 1):
                    self.playing = True
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

import sys, pygame, socket, json
from engine.game import *

class GameClient:
    """
    Game Client class.

    Attributes
    ----------
    id : int
        unique identifier of the client
    server_host : str
        address of the server socket
    server_port : int
        port of the server socket
    game_objects : list(GameObject)
        list of GameObjects
    """

    def __init__(self, id, server_host, server_port, game_objects=[]):
        """
        Initializes the GameClient.

        Parameters
        ----------
        id : int
            unique identifier of the client
        server_host : str
            address of the server socket
        server_port : int
            port of the server socket
        """
        self.id = id
        self.game_objects = game_objects
        self.server_host = server_host
        self.server_port = server_port
        self.running = False
        self.key_filter = []
        self.sock = None
    
    def deserialize_game_objects(self):
        """
        Convert self.game_objects to an array from get_dict().
    
        Returns
        ----------
        result : list(dict)
            self.game_objects values converted to dict
        """
        if self.game_objects == None:
            return None
        result = []
        for o in self.game_objects:
            result.append(o.get_dict())
        return result

    def draw(self):
        """
        Draws all PositionalObjects in game_objects to the screen
        """
        if self.game_objects == None:
            return
        self.screen.fill((0,0,0))
        for o in self.game_objects:
            if isinstance(o, PositionalObject):
                o.draw(self.screen)
        pygame.display.flip()

    def get_pressed_keys(self):
        """
        Gets the currently pressed keys in filter.
        """
        pressed = []
        keys = pygame.key.get_pressed()
        for k in self.key_filter:
            if keys[k] == True:
                print(k)
                pressed.append(k)
        return pressed
    
    def serialize_game_objects(self, data):
        """
        Converts game_objects array from request to GameObjects. Designed to be overriden by the game
        developer's inherited version of GameClient.

        Parameters
        ----------
        data : dict
            data to convert to game object
        """
        return None

    def start(self):
        """
        Initializes connection with the server and begins the client game loop.
        """
        pygame.init()
        self.screen = pygame.display.set_mode(WINSIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.sendto(bytes(CLIENT_CONNECT_MESSAGE, 'utf-8'), (self.server_host, self.server_port))
        initial_response = self.sock.recvfrom(MAX_PACKET_SIZE)[0]
        initial_response_dict = json.loads(str(initial_response)[2:-1])
        self.id = initial_response_dict['id']
        self.serialize_game_objects(initial_response_dict)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()
            self.update()
            self.frame += 1
            self.draw()
            self.clock.tick(60)

    def update(self):
        """
        Send the current game state to the server, get a response, and load it.
        """
        if not self.running: return
        send_data = { 'id': self.id, 'game_objects': self.deserialize_game_objects(), 'keys': self.get_pressed_keys() }
        self.sock.sendto(bytes(json.dumps(send_data), 'utf-8'), (self.server_host, self.server_port))
        packet = self.sock.recvfrom(MAX_PACKET_SIZE)[0]
        data = json.loads(str(packet)[2:-1])
        self.serialize_game_objects(data)

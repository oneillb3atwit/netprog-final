import json, getopt, sys, pygame

HOST = 'localhost'
PORT = 7737
CLIENT_CONNECT_MESSAGE = "hello"
CLIENT_DISCONNECT_MESSAGE = "goodbye"
MAX_PACKET_SIZE = 4096
WINSIZE = (640, 480)
frame = 0
game_objects = []
debug = False
server_mode = False
screen = None
clock = None

class GameObject:
    def __init__(self, id, type):
        self.id = id
        self.type = "GameObject"
    def get_json(self):
        return {'id': self.id, 'type': self.type}
    def client_update(self, data):
        pass
    def server_update(self):
        pass

class DrawableObject(GameObject):
    def __init__(self, id, type, sprite):
        super(id, "DrawableObject")
        self.sprite = sprite

    def get_json(self):
        return {'id': self.id, 'type': self.type, 'sprite': self.sprite}

    def draw(self, screen, w=None, h=None):
        if w == None and h == None:
            to_draw = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        else:
            to_draw = pygame.Rect(self.x, self.y, w, h)
        screen.blit(image, to_draw)

    def client_update(self, data):
        self.sprite = data['sprite']

class PositionalObject(DrawableObject):
    def __init__(self, id, type, sprite, x, y):
        super(id, "PositionalObject", sprite)
        self.x = x
        self.y = y

    def draw(self, screen, w=None, h=None):
        if w == None and h == None:
            to_draw = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        else:
            to_draw = pygame.Rect(self.x, self.y, w, h)
        screen.blit(self.sprite, to_draw)

    def move(self, x, y):
        self.x = x
        self.y = y

    def client_update(self, data):
        super(data)
        self.x = data['x']
        self.y = data['y']

"""
Prints to stderr only if debug mode is enabled

Parameters
----------
s : str
    the string to print.
"""
def printd(s):
    if debug == True:
        print(s, file=sys.stderr)

"""
Parses command line arguments
"""
def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], 'sdi:p:')
    ret = {'server': False}
    for o, a in opts:
        if o == '-d':
            ret['debug'] = True
        elif o == '-i':
            HOST = a
            ret['host'] = a
        elif o == '-p':
            ret['port'] = a
        elif o == '-s':
            ret['server'] = True
        else:
            print("usage: " + sys.argv[0] + " [-d] [-i IP] [-p PORT]", file=sys.stderr)
            sys.exit(1)
    return ret

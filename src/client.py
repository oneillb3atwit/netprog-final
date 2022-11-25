import sys, pygame, socket, json
from game import *

ball = Ball()
server_objects = []
player_objects = []
# TODO: move the following to game.py
player_img = pygame.image.load('img/player.png')
player_img_rect = player_img.get_rect()
ball_img = pygame.image.load('img/ball.png')
ball_img_rect = ball_img.get_rect()
# end of todo 
frame = 0

# pygame initialization
pygame.init()
screen = pygame.display.set_mode(WINSIZE)
clock = pygame.time.Clock()

"""
Get currently pressed keys related to the game

Returns
-------
list
    a list of pressed keys in their ASCII uppercase values
"""
def get_pressed_keys():
    keys = pygame.key.get_pressed()
    pressed = []
    if keys[pygame.K_w]:
        pressed.append('W')
    if keys[pygame.K_a]:
        pressed.append('A')
    if keys[pygame.K_s]:
        pressed.append('S')
    if keys[pygame.K_d]:
        pressed.append('D')
    return pressed

"""
Syncs the client data with the server. The client's Player object and keypresses
are sent to the server as JSON, which returns the Player object of all connected
clients, as well as the Ball object.
"""
def update():
    # send client data to server
    send_data = { 'player': player.get_json(), 'keys': get_pressed_keys() }
    s.sendto(bytes(json.dumps(send_data), 'utf-8'), (HOST, PORT))

    recv_data, addr = s.recvfrom(1024)
    if not recv_data: return
    recv_data = json.loads(str(recv_data)[2:-1])

    for d in recv_data['player_objects']:
        player_ids = []
        for p in player_objects:
            player_ids.append(p.id)
            if p.id == d['id']:
                p.client_update(d)
                continue
        if d['id'] not in player_ids:
            player_objects.append(Player(d))
    # TODO: implement this not as pseudocode
    # for d in recv_data['server_objects']:
        # if the received server object is not in server_objects, add it
        # if a server object in server_objects is not in received or gets destroyed in some way, remove it

        # server objects will be received as x, y, w, h, and an image to draw
        # image is just image name, all images will be loaded in game.py so it just has to refer to that
    # for s in server_objects:
        # s.client_update() or maybe just draw_sprite(s.x, s.y, s.img.get_width(), s.img.get_height(), s.img)
    print(f"{frame} {player_objects}\n")
    print("\n")
    ball.client_update(recv_data['ball'])

"""
Draws the player_objects and Ball to the Pygame window.
"""
# TODO: move to game.py
def draw():
    screen.fill((0,0,0))
    for p in player_objects:
        draw_sprite(player_img, screen, p.x, p.y)

    # TODO: implement this with the draw_sprite function in game.py
    # for s in server_objects:
        # draw the received objects 

    draw_sprite(ball_img, screen, ball.x, ball.y)
    pygame.display.flip()

"""
Initializes connection with the server and obtains a Player object with the
client ID.

Returns
-------
A new Player object using the data received from the surver
"""
def initialize_client(s):
    s.sendto(bytes(CLIENT_CONNECT_MESSAGE, 'utf-8'), (HOST, PORT))
    data, addr = s.recvfrom(1024)
    if not data:
        print("failed to connect to server")
        sys.exit()
    data = json.loads(str(data)[2:-1])
    return Player(data)

"""
Parses command line arguments
"""
def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], 'di:p:')
    for o, a in opts:
        if o == '-d':
            debug = True 
        elif o == '-i':
            HOST = a
        elif o == '-p':
            PORT = int(a)
        else:
            print("usage: " + sys.argv[0] + " [-d] [-i IP] [-p PORT]", file=sys.stderr)
            sys.exit(1)

parse_args()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    player = initialize_client(s)
    if player == None:
        print('failed to initialize client')
        sys.exit()
    else:
        print('client initialized')
    player_objects.append(player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        update()
        frame += 1
        draw()
        clock.tick(60)

import sys, pygame, socket, json
from game import *

HOST = 'localhost'
PORT = 8000

players = []
player_id = None

def update():
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

    send_data = { 'player': player.get_json(), 'keys': pressed }
    s.sendto(bytes(json.dumps(send_data), 'utf-8'), (HOST, PORT))

    recv_data, addr = s.recvfrom(1024)
    if not recv_data: return
    recv_data = json.loads(str(recv_data)[2:-1])

    for d in recv_data['players']:
        for p in players:
            if p.id == d['id']:
                p.update(d)
                continue
        players.append(Player(d))

def draw():
    screen.fill((0,0,0))
    for p in players:
        imgrect.x = p.x
        imgrect.y = p.y
        screen.blit(img, imgrect)
    pygame.display.flip()

def player_init(s):
    s.sendto(bytes("new", 'utf-8'), (HOST, PORT))
    data, addr = s.recvfrom(1024)
    if not data:
        print("failed to connect to server")
        sys.exit()
    data = json.loads(str(data)[2:-1])
    return Player(data)


# pygame initialization
pygame.init()
size = width, height = 320, 240
screen = pygame.display.set_mode(size)
img = pygame.image.load('img.png')
imgrect = img.get_rect()
clock = pygame.time.Clock()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    player = player_init(s)
    if player == None:
        print('failed to initialize client')
        sys.exit()
    else:
        print('client initialized')
    players.append(player)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        update()
        draw()
        clock.tick(60)

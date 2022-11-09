import sys, pygame, socket, json
from game import *

players = []
player_id = None

player_img = pygame.image.load('player.png')
player_img_rect = player_img.get_rect()

ball_img = pygame.image.load('ball.png')
ball_img_rect = ball_img.get_rect()

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

def update():
    # send client data to server
    send_data = { 'player': player.get_json(), 'keys': get_pressed_keys() }
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

    ball.update(recv_data['ball'])

def draw():
    screen.fill((0,0,0))
    for p in players:
        player_img_rect.x = p.x
        player_img_rect.y = p.y
        screen.blit(player_img, player_img_rect)

    ball_img_rect.x = ball.x
    ball_img_rect.y = ball.y
    screen.blit(ball_img, ball_img_rect)
    pygame.display.flip()

def initialize_client(s):
    s.sendto(bytes(CLIENT_CONNECT_MESSAGE, 'utf-8'), (HOST, PORT))
    data, addr = s.recvfrom(1024)
    if not data:
        print("failed to connect to server")
        sys.exit()
    data = json.loads(str(data)[2:-1])
    return Player(data)

# pygame initialization
pygame.init()
screen = pygame.display.set_mode(WINSIZE)
clock = pygame.time.Clock()

ball = Ball()

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    player = initialize_client(s)
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

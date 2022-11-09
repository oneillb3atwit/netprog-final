import socket, json, pygame
from _thread import *
from game import *

def game_loop(conn):
    while True:
        # handle connections
        data, addr = conn.recvfrom(1024)
        if data == None: break
        data = str(data)[2:-1]
        if data == CLIENT_CONNECT_MESSAGE:
            print('client connected')
            add_client(conn, addr)
            continue

        data = json.loads(data)
        keys = data['keys']
        player = players[data['player']['id']]
        addr = players[data['player']['id']].addr

        handle_keys(player, keys)
        ball.move()

        players_json = []
        for p in players:
            players_json.append(p.get_json())
        conn.sendto(bytes(json.dumps({'players': players_json, 'ball': ball.get_json()}), encoding="utf8"), addr)

    conn.close()

def add_client(conn, addr):
    p = Player({ 'id': len(players), 'x': 0, 'y': 0, 'team': (len(players) % 2) })
    p.addr = addr
    players.append(p)
    pjson = p.get_json()
    conn.sendto(bytes(json.dumps(pjson), encoding='utf8'), addr)

def handle_keys(player, keys):
    if 'W' in keys:
        player.move(0, -1)
    if 'A' in keys:
        player.move(-1, 0)
    if 'S' in keys:
        player.move(0, 1)
    if 'D' in keys:
        player.move(1, 0)

ball = Ball()

# bind UDP socket and begin game loop
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    game_loop(s)

import socket, json, pygame
from _thread import *
from game import *

HOST = 'localhost'
PORT = 8000

def game_loop(conn):
    while True:
        data, addr = conn.recvfrom(1024)
        if data == None: break

        data = str(data)[2:-1]
        if data == "new":
            print('client connected')
            add_client(conn, addr)
            continue

        print(data)
        data = json.loads(data)

        k = data['keys']
        p = players[data['player']['id']][0]
        addr = players[data['player']['id']][1]
        if 'W' in k:
            p.y -= 1
        if 'A' in k:
            p.x -= 1
        if 'S' in k:
            p.y += 1
        if 'D' in k:
            p.x += 1
        conn.sendto(bytes(json.dumps({'player': p.get_json()}), encoding="utf8"), addr)

    conn.close()

def add_client(conn, addr):
    p = Player(len(players), 0, 0)
    players.append((p, addr))
    conn.sendto(bytes(json.dumps(p.get_json()), encoding='utf8'), addr)

# bind UDP socket and begin game loop
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    game_loop(s)

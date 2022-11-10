import socket, json, pygame
from game import *

"""
The main server game loop. Handles new connections and updates the game state.
Runs indefinitely.

Parameters
----------
conn : Socket
    The server's UDP socket
"""
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

"""
Initializes a new Player by assigning the client an ID and team, then sending it
to the client.

Parameters
----------
conn : Socket
    The server's socket
addr : (str, int)
    The address and port of the client socket.
"""
def add_client(conn, addr):
    p = Player({ 'id': len(players), 'x': 0, 'y': 0, 'team': (len(players) % 2) })
    p.addr = addr
    players.append(p)
    pjson = p.get_json()
    conn.sendto(bytes(json.dumps(pjson), encoding='utf8'), addr)

"""
Handles player movement based on key presses

TODO this could be moved to the Player class

Parameters
----------
player : Player
    The Player object to modify
keys : list(str)
    The client's currently pressed keys
"""
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

# bind socket and begin game loop
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    game_loop(s)
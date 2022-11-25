import socket, json, pygame
from threading import Thread
from game import *

clock = pygame.time.Clock()
ball = Ball()

"""
The main client game loop. Handles new connections, updates game state based off of keypresses, and sends the game state to its connection.
Runs indefinitely for each connection, until the connection is closed.

Parameters
----------
conn : Socket
    The server's UDP socket
TODO remove player upon connection termination
"""
def client_game_loop(conn):
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
        player = player_objects[data['player']['id']]
        addr = player_objects[data['player']['id']].addr

        player.server_update(keys)

        player_objects_json = []
        for p in player_objects:
            player_objects_json.append(p.get_json())
        #print(f"{player_objects}\n")
        conn.sendto(bytes(json.dumps({'player_objects': player_objects_json, 'ball': ball.get_json()}), encoding="utf8"), addr)
    conn.close()

"""
The main server game loop. Updates the state of server-linked objects.
Runs indefinitely.
"""
def server_game_loop():
    while True:
        ball.server_update()
        clock.tick(60)
        

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
    p = Player({ 'id': len(player_objects), 'x': 0, 'y': 0, 'team': (len(player_objects) % 2) })
    p.addr = addr
    player_objects.append(p)
    pjson = p.get_json()
    conn.sendto(bytes(json.dumps(pjson), encoding='utf8'), addr)

parse_args()

# start the server's loop
server_logic_thread = Thread(target = server_game_loop)
server_logic_thread.start()
# bind socket and begin game loop
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    s.bind((HOST, PORT))
    client_game_loop(s)

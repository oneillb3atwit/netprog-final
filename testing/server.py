import socket
import threading

HOST = 'localhost'
PORT = 8001
listening = False

cur_data = ""

class player:
    player_id = 0
    x = 0
    y = 0
    def __init__(self, id):
        self.id = id

def clientThread(connection, player):
    conn.send(bytes(player_count))
    while listening:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
        #for player in players:
         #   conn.send(bytes('{"x": ' + str(x) + '}', encoding='utf8'))

players = []

x = 0
y = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)
listening = True
player_count = 0
while listening:
    conn, addr = s.accept()
    threading.Thread(target=clientThread(conn, player_count)).start()
    player_count += 1

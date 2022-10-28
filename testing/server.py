import socket

HOST = 'localhost'
PORT = 8001

x = 0
y = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.send(bytes('{"x": ' + str(x) + '}', encoding='utf8'))
            x += 1

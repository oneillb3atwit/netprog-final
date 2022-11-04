import sys, pygame, socket, json

## NET INIT
# server side
HOST = sys.argv[1]
PORT = 8001
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

send_pos = (0,0)
delay = 3 # 3 frame delay for now, will experiment with
recv_json = []

# client side
player_num = 0
client_pos = (0,0)
frame_num = 0
game_playing = True

## PYGAME INIT
# pygame setup and file load
pygame.init()
size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)
img = pygame.image.load('img.png')
imgrect = img.get_rect()
clock = pygame.time.Clock()

## GAME FUNCTIONS
# send attributes as json (change to really small bytes? tcp is slow)
def send(x, y, frame):
	to_send = ""
	to_send += f"{{x: {x}}}"
	to_send += f"{{y: {y}}}"
	to_send += f"{{frame: {frame}}}"

	s.send(bytes(to_send))

# draw 
def draw():
	screen.fill(black)
	screen.blit(img, imgrect)
	# for entity in entity list, entity.draw()

# update
def update():
	parse_recv_json(frame_num)

# input handling
def handle_inputs(event):
    if event.key == pygame.K_LEFT:
        send_pos[0] -= 1
    if event.key == pygame.K_RIGHT:
        send_pos[0] += 1
    if event.key == pygame.K_UP:
        send_pos[1] -= 1
    if event.key == pygame.K_DOWN:
        send_pos[1] += 1

def parse_recv_json(frame):
	# this will read packet at frame time frame
	jdata = recv_json[frame]
	imgrect.x = jdata['x']
	imgrect.y = jdata['y']

# connect, should wrap into a function eventually and have host, port as arguments
s.connect((HOST, PORT))
player_num = int.from_bytes(s.recv(1024)) # receive player number

# pygame loop
while game_playing:
	frame_num += 1 
	for event in pygame.event.get():
		if event.type == pygame.QUIT: sys.exit()
		if event.type == pygame.KEYDOWN: handle_inputs(event)

	update()
	draw()

	## server code, run after update and draw
	data = None
	# send attributes    add player num 
	send(send_pos[0], send_pos[1], frame_num+delay)

	# receive attributes from other clients
	data = s.recv(1024)
	data = str(data)[2:-1]
	jdata = json.loads(str(data))
	recv_json.insert(frame_num + delay, jdata)
	

	pygame.display.flip()
	clock.tick(60)

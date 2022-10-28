import sys, pygame, socket, json

# NET INIT
HOST = 'localhost'
PORT = 8001

# PYGAME INIT
pygame.init()
size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)
img = pygame.image.load('img.png')
imgrect = img.get_rect()
clock = pygame.time.Clock()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		data = None
		s.send(b'give me a new x')
		data = s.recv(1024)
		data = str(data)[2:-1]
		jdata = json.loads(str(data))
		imgrect.x = jdata['x']

		screen.fill(black)
		screen.blit(img, imgrect)
		pygame.display.flip()
		clock.tick(60)

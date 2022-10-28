import sys, pygame, socket, json

# NET INIT
HOST = 'localhost'
PORT = 8001


# PYGAME INIT
pygame.init()
size = width, height = 320, 240
speed = [2, 2]
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball = pygame.image.load('img.png')
ballrect = ball.get_rect()
clock = pygame.time.Clock()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.connect((HOST, PORT))
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()
		if ballrect.left < 0 or ballrect.right > width:
			speed[0] = -speed[0]
		if ballrect.top < 0 or ballrect.bottom > height:
			speed[1] = -speed[1]
	
		data = None
		s.send(b'give me a new x')
		data = s.recv(1024)
		data = str(data)[2:-1]
		jdata = json.loads(str(data))
		ballrect.x = jdata['x']
	
		screen.fill(black)
	
		screen.blit(ball, ballrect)
		pygame.display.flip()
		clock.tick(60)

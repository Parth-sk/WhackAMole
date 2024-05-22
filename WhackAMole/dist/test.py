import pygame
pygame.init()

screen = pygame.display.set_mode((1080,720))
clock = pygame.time.Clock()

running = True

while(running):
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            running = False
            continue
    
    clock.tick(30)
    pygame.display.update()
    
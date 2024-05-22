import pygame
import random
import math
pygame.init()

#screen and clock
screen_width=1040
screen_height=1040
screen = pygame.display.set_mode((screen_width,screen_height))
screen.fill((217,160,102))
clock = pygame.time.Clock()

#global variables
score = 0
total_moles = 0

#title
start_up = pygame.image.load(r'start_up.png')
start_up_rect = start_up.get_rect()
start_down = pygame.image.load(r'start_down.png')
start_down_rect = start_down.get_rect()

#mole
moleup_image = pygame.image.load(r'up.png')
moledown_image = pygame.image.load(r'down.png')

class mole:
    state = 0
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.image = moledown_image

    def display(self):
        if (self.state):
            self.image = moleup_image
        else:
            self.image = moledown_image


#creating the grid as a matrix
grid = []
grid_size = 10 # n x n grid
grid_image = pygame.image.load(r'grid.png')
grid_rect = pygame.Rect((screen_width/2)-(grid_size*50),(screen_height/2)-(grid_size*50),grid_size*100,grid_size*100)

for i in range(grid_size):
    grid.append([])
    for j in range(grid_size):
        grid[i].append(mole(i,j))

#choosing moles to stand
def stand_moles(start_time):
    global total_moles
    current_time = pygame.time.get_ticks()

    if ((current_time-start_time)<7000):
        num_moles = random.randint(1,3)
    elif ((current_time-start_time)<12000):
        num_moles = random.randint(3,6)
    elif ((current_time-start_time)<20000):
        num_moles = random.randint(9,13)
    else:
        num_moles = random.randint(15,16)
    
    for i in range(num_moles):
        coordinate = random.randint(0,99)
        if grid[int(coordinate/10)][coordinate%10].state == 0:
            grid[int(coordinate/10)][coordinate%10].state = 1
            grid[int(coordinate/10)][coordinate%10].display()
            total_moles+=1


#blitting moles
def blit_moles():
    for i in range(grid_size):
        for j in range(grid_size):
            grid[i][j].display()
            screen.blit(grid[i][j].image,((screen_width/2)-(grid_size*50)+(j*100),(screen_height/2)-(grid_size*50)+(i*100)))




def end():
    running = 1
    infested = pygame.image.load(r'infested.png')
    end_sound = pygame.mixer.Sound(r'game_over.wav')
    end_sound.set_volume(0.3)
    end_sound.play()
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()

        screen.blit(infested,((screen_width/2 - 500),0))
        pygame.display.update()

def game():
    global score,total_moles
    start_time = pygame.time.get_ticks()
    round_start_time = start_time
    running = 1
    boink = pygame.mixer.Sound(r'thud.wav')

    while(running):
        #background
        screen.blit(grid_image,grid_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()
            #player input
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                grid_j = int((mouse_x+(grid_size *50)-(screen_width/2))/100)
                grid_i = int((mouse_y+(grid_size *50)-(screen_height/2))/100)
                #print(grid_i,grid_j)
                if grid[grid_i][grid_j].state == 1:
                    boink.play()
                    score += 1
                    total_moles -= 1
                    grid[grid_i][grid_j].state = 0
                    grid[grid_i][grid_j].display()
                    screen.blit(grid[i][j].image,((screen_width/2)-(grid_size*50)+(j*100),(screen_height/2)-(grid_size*50)+(i*100)))
                    pygame.display.update((screen_width/2)-(grid_size*50)+(j*100),(screen_height/2)-(grid_size*50)+(i*100),100,100)
        
        
        #checking if enough time has elapsed since last stand_moles()
        current_time = pygame.time.get_ticks()
        delta = current_time - round_start_time
        if delta > 1000:
            round_start_time = current_time
            stand_moles(start_time)    
        
        blit_moles()
        pygame.display.update()

        if total_moles>80:
            pygame.mixer.music.stop()
            end()

        clock.tick(15)
        pygame.display.update()

def start_menu():
    button_sound = pygame.mixer.Sound(r'button.wav')
    down = 0
    running = 1
    while(running):
        pygame.draw.rect(screen,(217,160,102),pygame.Rect(0,0,1040,1040))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = 0
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x,mouse_y = pygame.mouse.get_pos()
                if ((mouse_x > screen_width/2 - start_up_rect.width/2) and (mouse_x < screen_width/2 + start_up_rect.width/2) and(mouse_y > screen_height/2 - start_up_rect.height/2)and (mouse_y < screen_height/2 + start_up_rect.height/2)):
                    down=1
                    button_sound.play()
            if event.type== pygame.MOUSEBUTTONUP:
                down = 0
                if ((mouse_x > screen_width/2 - start_up_rect.width/2) and (mouse_x < screen_width/2 + start_up_rect.width/2) and(mouse_y > screen_height/2 - start_up_rect.height/2)and (mouse_y < screen_height/2 + start_up_rect.height/2)):
                    game()


            
        if (not down):
            screen.blit(start_up,(screen_width/2 - start_up_rect.width/2,screen_height/2 - start_up_rect.height/2))
        else:
            screen.blit(start_down,(screen_width/2 - start_down_rect.width/2,screen_height/2 + start_up_rect.height/2-start_down_rect.height))

        pygame.display.update()
        clock.tick(30)
                


pygame.mixer.music.load(r'background.wav')
pygame.mixer.music.play(-1)
start_menu()
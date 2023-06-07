import pygame
import random
from pygame.locals import *

pygame.init()

clock = pygame.time.Clock()
fps = 60
screen_width = 1000
screen_height = 1000
tile_size = 100

screen=pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption('geme')

block_img = pygame.image.load('images/block.png')


def drawGrid():
    for line in range(1,10):
        pygame.draw.line(screen, (255,255,255), (tile_size, line * tile_size), (screen_width-tile_size, line * tile_size))
        pygame.draw.line(screen, (255,255,255), (line * tile_size, tile_size), (line * tile_size, screen_height-tile_size))


class Player():
    def __init__(self, x, y):
        img = pygame.image.load('images/player.png')
        self.image = pygame.transform.scale(img, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False

    def update(self):

        dx = 0
        dy = 0

        key = pygame.key.get_pressed()
        if key[pygame.K_w] and self.jumped == False:
            self.vel_y = -30
            self.jumped = True
        if self.vel_y == 0 and key[pygame.K_w]==False:
            self.jumped = False
        if key[pygame.K_a]:
            dx -= 15
        if key[pygame.K_d]:
            dx += 15

        self.vel_y += 3.1
        if self.vel_y > 25:
            self.vel_y = 25
        dy += self.vel_y
        
        count = 0
        for tile in world.tileList:
            if tile == world.trophy:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) or tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    self.rect.x = 200
                    self.rect.y = screen_height-100
                    worldData[world.trophyCords[0]][world.trophyCords[1]]=0
                    world.tileList.pop(count)
            else:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0

                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0.1
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
            count+=1
            
        
        
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height


        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (255,255,255), self.rect, 2)

class World():
    def __init__(self, data):
        self.tileList = []
        self.trophy = None
        self.trophyCords = ()


        blockImg = pygame.image.load('images/block.png')
        trophyImg = pygame.image.load('images/trophy.png')
        dirtImg = pygame.image.load('images/dirt.png')

        rowCount = 0
        for row in data:
            colCount = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(blockImg, (tile_size, tile_size))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tile_size
                    imgRect.y = rowCount * tile_size
                    tile = (img, imgRect)
                    self.tileList.append(tile)
                
                if tile == 2:
                    img = pygame.transform.scale(trophyImg, (tile_size, tile_size))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tile_size
                    imgRect.y = rowCount * tile_size
                    self.trophy = (img, imgRect)
                    self.trophyCords = (rowCount, colCount)
                    self.tileList.append(self.trophy)
                    
                if tile == 3:
                    img = pygame.transform.scale(dirtImg, (tile_size, tile_size))
                    imgRect = img.get_rect()
                    imgRect.x = colCount * tile_size
                    imgRect.y = rowCount * tile_size
                    tile = (img, imgRect)
                    self.tileList.append(tile)
                colCount += 1
            rowCount += 1

    def draw(self):
        for tile in self.tileList:
            screen.blit(tile[0], tile[1])
            # pygame.draw.rect(screen, (255,255,255), tile[1], 2)


worldData = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

class GameState():
    def __init__(self):
        self.state = 'intro'
        self.isTrophySpawned = False
    
    
    def intro(self):
        drawGrid()
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.state = 'main_game'
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN :
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                for row in range(1,9):
                    for col in range(1,9):
                        if mouseX >= col*tile_size and mouseX <= (col+1)*tile_size and mouseY >= row*tile_size and mouseY <= (row+1)*tile_size:
                            if worldData[row][col]==3:
                                worldData[row][col]=0
                                screen.fill((30,30,30))
                                world = World(worldData)
                                world.draw()
                            elif worldData[row][col]==0:
                                worldData[row][col]=3
                                screen.fill((30,30,30))
                                world = World(worldData)
                                world.draw()
                                
        pygame.display.update()

    def main_game(self):
        screen.fill((30,30,30))
        self.isTrophySpawned = False
        for row in worldData:
            for i in row:
                if i == 2:
                    self.isTrophySpawned=True
        
        if self.isTrophySpawned==False:
            tX = random.randint(1,8)
            tY = random.randint(1,5)
            for j in range(1,9):
                for i in range(1,9):
                    worldData[j][i]=0
            worldData[tY][tX] = 2
            self.isTrophySpawned = True
            world = World(worldData)
            world.draw()
            game_state.state = "intro"
        else:
            world = World(worldData)
            world.draw()
            player.update()
            key = pygame.key.get_pressed()
            if key[pygame.K_BACKSPACE]:
                screen.fill((30,30,30))
                world.draw()
                self.state = 'intro'
            pygame.display.update()
    
    def state_manager(self):
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()

game_state = GameState()
screen.fill((30,30,30))
player = Player(200, screen_height-100)
world = World(worldData)
world.draw()
temp = True
run = True
while run:
    clock.tick(fps)
    print(clock.get_fps())
    game_state.state_manager()
    # runs only once
    if game_state.state == 'intro' and temp == True:
        temp = False
    if game_state.state == "main_game" and temp == False:
        world = World(worldData)
        temp = True
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
pygame.quit()

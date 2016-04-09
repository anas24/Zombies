import pygame, sys, Funk
from tileC import Tile
from object_classes import *
from interaction import interaction
from A_Star import A_Star
from time import sleep

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((704, 448)) # 32, 32

for y in range(0, screen.get_height(), 32):
    for x in range(0, screen.get_width(), 32):
        if Tile.total_tiles in Tile.invalids:
            Tile(x, y, 'solid')
        else:
            Tile(x, y, 'empty')

clock = pygame.time.Clock()
FPS = 20
total_frames = 0

pygame.mixer.init()
pygame.mixer.music.load('Audio/zombie_theme.ogg')
pygame.mixer.music.play(-1) 
dungeon = pygame.image.load('images/dungeon.jpg')
survivor = Survivor(32 * 2, 32 * 4)
f=open("highscore.txt","rw")
last=f.read()
last_no=int(last)

while survivor.health>1:

    screen.blit(dungeon, (0,0) )
    # if total_frames % 6*FPS  == 0:
        # print len7(Zombie.List)
    Zombie.spawn(total_frames, FPS)
    # Zombie.movement()
    Zombie.update(screen,survivor)
    survivor.movement()
    Bullet.bullet_action(screen)
    A_Star(screen, survivor, total_frames, FPS)

    interaction(screen, survivor)
    Tile.draw_tiles(screen)
    survivor.draw(screen)
    # Zombie.draw_zombies(screen)
    Funk.text_to_screen(screen,'Health:{0}'.format(survivor.health),0,0)
    pygame.display.flip()
    
    Funk.text_to_screen(screen,'You killed:{0}'.format(survivor.score),400,0)   
    Funk.text_to_screen(screen,'Highest:{0}'.format(last_no),600,0)
    pygame.display.update()
    clock.tick(FPS)
    total_frames += 1

    if survivor.health<=0:
        sleep(2.5)
        f=open("highscore.txt","r+")
        last=f.read()
        last_no=int(last)
        # if last<survivor.score:
        score=str(survivor.score)
        if survivor.score > last_no:
            # f.clear()
            f=open("highscore.txt","w")
            f.write(score)
            f.close()
        # else:
        #     f.write(last) 

        screen.blit(pygame.image.load('images/dead.jpg'),(0,0))
        pygame.display.update()
        sleep(4)
        break
    



import pygame, sys
from tileC import Tile
from object_classes import Bullet
def interaction(screen, survivor):

    Mpos = pygame.mouse.get_pos() # [x, y] 
    Mx = Mpos[0] / Tile.width
    My = Mpos[1] / Tile.height

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for tile in Tile.List:
                if tile.x == (Mx * Tile.width) and tile.y == (My * Tile.width):
                    tile.type = 'solid'
                    tile.walkable = False
                    break
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_e:
                survivor.current+=1
                survivor.current%=3

    keys=pygame.key.get_pressed()  
    if  keys[pygame.K_UP]: # North
        future_tile_number = survivor.get_number() - Tile.V
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile=Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                        # survivor.y -= survivor.height
                            
                survivor.set_target(future_tile)
                survivor.rotate('n')                   

    if keys[pygame.K_DOWN]: # South
        future_tile_number = survivor.get_number() + Tile.V
        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile=Tile.get_tile(future_tile_number)

            if future_tile.walkable:
                
                survivor.set_target(future_tile)
                survivor.rotate('s')
                        # survivor.y += survivor.height


    if keys[pygame.K_LEFT]: # West
        future_tile_number = survivor.get_number() - Tile.H

        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile=Tile.get_tile(future_tile_number)
            if future_tile.walkable:
                
                survivor.set_target(future_tile)
                survivor.rotate('w')
                        # survivor.x -= survivor.width 
    if keys[pygame.K_RIGHT]: # East
        future_tile_number = survivor.get_number() + Tile.H

        if future_tile_number in range(1, Tile.total_tiles + 1):
            future_tile=Tile.get_tile(future_tile_number)
            if future_tile.walkable:

                survivor.set_target(future_tile)
                survivor.rotate('e')
                        # survivor.x += survivor.width
    if keys[pygame.K_w]:
        
        survivor.rotate('n')
        Bullet(survivor.centerx,survivor.centery,0,-10,'n',survivor.get_bullet_type())

    elif keys[pygame.K_a]:
        survivor.rotate('w')
        Bullet(survivor.centerx,survivor.centery,-10,0,'w',survivor.get_bullet_type())
    elif keys[pygame.K_s]:
        survivor.rotate('s')
        Bullet(survivor.centerx,survivor.centery,0,10,'s',survivor.get_bullet_type())
    elif keys[pygame.K_d]:
        survivor.rotate('e')
        Bullet(survivor.centerx,survivor.centery,10,0,'e',survivor.get_bullet_type())


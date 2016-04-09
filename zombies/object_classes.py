import pygame
from tileC import Tile
from random import randint 

class Character(pygame.Rect):

    width, height = 32, 32

    def __init__(self, x, y):
        self.tx,self.ty=None,None

        pygame.Rect.__init__(self, x, y, Character.width, Character.height)

    def __str__(self):
        return str(self.get_number())
    def set_target(self, next_tile):
        if self.tx == None and self.ty == None:
            self.tx = next_tile.x
            self.ty = next_tile.y

    def get_number(self):
        
        return ((self.x / self.width) + Tile.H) + ((self.y / self.height) * Tile.V)

    def get_tile(self):

        return Tile.get_tile(self.get_number())

class Zombie(Character):

    List = []
    spawn_tiles = (9,42,91,134,193,219,274)
    original_image=pygame.image.load('images/zombie.png')
    health=100

    def __init__(self, x, y):

        self.tx, self.ty = None, None
        self.health=Zombie.health
        Character.__init__(self, x, y)
        self.image=Zombie.original_image
        self.direction='w'
        Zombie.List.append(self)


    def rotate(self,direction,original_image):
        if direction=='n':
            if self.direction!='n':
                self.direction='n'
                south=pygame.transform.rotate(original_image,90)#anti clock wise 90 degree rotation

                self.image=pygame.transform.flip(south,False,True)
        if direction == 'e':
            if self.direction!='e':
                self.direction='e'
                self.image=pygame.transform.flip(original_image,True,False)
        if direction == 'w':
            if self.direction!='w':
                self.direction='w'
                self.image=original_image
        if  direction =='s':
            if self.direction!='s':
                self.direction='s'
                self.image=pygame.transform.rotate(original_image,90)#anti clock wise 90 degree rotation

    @staticmethod
    def update(screen,survivor):
        for zombie in Zombie.List:

            screen.blit(zombie.image,(zombie.x,zombie.y))
            if zombie.health<=0:
                Zombie.List.remove(zombie)
                survivor.score+=1
                



            if survivor.x%Tile.width==0 and survivor.y % Tile.height==0:
                if zombie.x%Tile.width==0 and zombie.y % Tile.height==0:
                    tn=survivor.get_number()
                    N=tn + -(Tile.V)
                    S=tn +  (Tile.V)
                    E=tn +  (Tile.H)
                    W=tn + -(Tile.H)
                    NSEW=[N,S,E,W,tn]
                    # for n in NSEW:
                    if zombie.get_number() in NSEW:
                        survivor.health-=5    
            if zombie.tx != None and zombie.ty != None: # Target is set

                X = zombie.x - zombie.tx
                Y = zombie.y - zombie.ty

                vel = 4

                if X < 0: # --->
                    zombie.x += vel
                    zombie.rotate('e',Zombie.original_image)
                elif X > 0: # <----
                    zombie.x -= vel
                    zombie.rotate('w',Zombie.original_image)

                if Y > 0: # up
                    zombie.y -= vel
                    zombie.rotate('n',Zombie.original_image)
                elif Y < 0: # dopwn
                    zombie.y += vel
                    zombie.rotate('s',Zombie.original_image)

                if X == 0 and Y == 0:
                    zombie.tx, zombie.ty = None, None
 
    @staticmethod
    def spawn(total_frames, FPS):
        if total_frames % (2*FPS)  == 0:
            if total_frames %(6*FPS)==0:
                r=randint(0,2)
                sounds=[pygame.mixer.Sound('Audio/zs1.ogg'),pygame.mixer.Sound('Audio/zs2.ogg'),
                pygame.mixer.Sound('Audio/zs3.ogg')]
                sound=sounds[r]
                sound.play()
            r = randint(0, len(Zombie.spawn_tiles) - 1)
            tile_num = Zombie.spawn_tiles[r]
            spawn_node = Tile.get_tile(tile_num)
            Zombie(spawn_node.x, spawn_node.y)


    
class Survivor(Character):
    guns_img=[pygame.image.load('images/pistol.png'),pygame.image.load('images/shotgun.png'),
    pygame.image.load('images/automatic.png')  ]
       
    def __init__(self, x, y):

        
        Character.__init__(self, x, y)
        self.current=0
        self.score=0
        self.health=1000
        self.image=pygame.image.load('images/survivor_w.png')
        self.direction='w'    
 
    def get_bullet_type(self):
        if self.current ==0:
            return 'pistol'
        elif self.current==1:
            return 'shotgun'
        elif self.current==2:
            return 'automatic'


    def movement(self):
        
        if self.tx != None and self.ty != None: # Target is set

            X = self.x - self.tx
            Y = self.y - self.ty

            vel = 8

            if X < 0: # --->
                self.x += vel
            elif X > 0: # <----
                self.x -= vel

            if Y > 0: # up
                self.y -= vel
            elif Y < 0: # dopwn
                self.y += vel

            if X == 0 and Y == 0:
                self.tx, self.ty = None, None

    


    def rotate(self,direction):
        if direction=='n':
            if self.direction!='n':
                self.direction='n'
                # south=pygame.transform.rotate(Survivor.original_image,90)#anti clock wise 90 degree rotation

                # self.image=pygame.transform.flip(south,False,True)
                self.image=pygame.image.load('images/survivor_n.png')
        if direction == 'e':
            if self.direction!='e':
                self.direction='e'
                # self.image=pygame.transform.flip(Survivor.original_image,True,False)
                self.image=pygame.image.load('images/survivor_e.png')
        if direction == 'w':
            if self.direction!='w':
                self.direction='w'
                self.image=pygame.image.load('images/survivor_w.png')
        if  direction =='s':
            if self.direction!='s':
                self.direction='s'
                self.image=pygame.image.load('images/survivor_s.png')#anti clock wise 90 degree rotation

                

    def draw(self, screen):
        screen.blit(self.image,(self.x,self.y))
        img=Survivor.guns_img [self.current]
        h=self.width/2
        if self.direction=='e':
            img=pygame.transform.flip(img,True,False)
            screen.blit(img,(self.x+h,self.y+h))
        if self.direction == 'w':
            screen.blit(img,(self.x,self.y+h))
        if self.direction == 'n':
            south=pygame.transform.rotate(img,90)
            img=pygame.transform.flip(south,False,True)
        if self.direction =='s':

            img=pygame.transform.rotate(img,90)
            screen.blit(img,(self.x+h,self.y+h))

        # r = self.width / 2
        # pygame.draw.circle(screen, [77, 234, 156], (self.x + r, self.y + r), r)
class Bullet(pygame.Rect):
    width,height=7,10
    List=[]
    imgs={
                'pistol':pygame.image.load('images/pistol_b.png'),
                'shotgun':pygame.image.load('images/shotgun_b.png'),
                'automatic':pygame.image.load('images/automatic_b.png')
         }
    gun_dmg={
                'pistol':(Zombie.health/3) +1,
                'shotgun':(Zombie.health)/2,
                'automatic':(Zombie.health/6)+1
    }
    def __init__(self,x,y,velx,vely,direction,type_):
        if type_=='shotgun' or type_=='pistol':
            try:
                dx=abs(Bullet.List[-1].x-x)
                dy=abs(Bullet.List[-1].y-y)
                if dx<50 and dy<50 and type_=='shotgun':
                    return
                if dx<30 and dy<30 and type_=='pistol':
                    return
                pass
            except:
                pass
        self.type=type_
        self.direction=direction
        self.velx=velx
        self.vely=vely
        if direction=='n':
            
            south=pygame.transform.rotate(Bullet.imgs[type_],90)#anti clock wise 90 degree rotation

            self.image=pygame.transform.flip(south,False,True)
        if direction == 'e':
            
            self.image=pygame.transform.flip(Bullet.imgs[type_],True,False)
        if direction == 'w':
            
            self.image=Bullet.imgs[type_]
        if  direction =='s':
            
            self.image=pygame.transform.rotate(Bullet.imgs[type_],90)#anti clock wise 90 degree rotation
        pygame.Rect.__init__(self,  x,y,Bullet.width,Bullet.height)
        Bullet.List.append(self)
    def offscreen(self,screen):
        if self.x<0:
            return True
        elif self.y<0:
            return True
        elif self.x+self.width>screen.get_width():
            return True
        elif self.y +self.width >screen.get_height():
            return True
        return False 
    @staticmethod       
    def bullet_action(screen):
        for bullet in Bullet.List:

            bullet.x+=bullet.velx
            bullet.y+=bullet.vely
            screen.blit(bullet.image,(bullet.x,bullet.y))
            if bullet.offscreen(screen):
                Bullet.List.remove(bullet)
                continue
            for zombie in Zombie.List:
                if bullet.colliderect(zombie):
                    zombie.health-=Bullet.gun_dmg[bullet.type]
                    try:
                        Bullet.List.remove(bullet)
                    except Exception, e:
                        pass# bullet not in list
            for tile in Tile.List:
                if bullet.colliderect(tile)and not (tile.walkable):
                    try:
                        Bullet.List.remove(bullet)
                    except Exception, e:
                        pass# bullet not in list







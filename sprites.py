from math import trunc
from operator import truediv
import pygame as pg
from pygame import image
vec = pg.math.Vector2
from random import gammavariate, randint
from pygame import mixer


JUMPING1 = pg.transform.scale(pg.image.load('Jump__001.png'),(245,455))
JUMPING2 = pg.transform.scale(pg.image.load('Jump__002.png'),(252,430))
JUMPING3 = pg.transform.scale(pg.image.load('Jump__003.png'),(253,430))
JUMPING4 = pg.transform.scale(pg.image.load('Jump__004.png'),(249,430))
JUMPING5 = pg.transform.scale(pg.image.load('Jump__005.png'),(252,427))
JUMPING6 = pg.transform.scale(pg.image.load('Jump__006.png'),(272,422))
JUMPING7 = pg.transform.scale(pg.image.load('Jump__007.png'),(296,419))
JUMPING8 = pg.transform.scale(pg.image.load('Jump__008.png'),(329,411))
JUMPING9 = pg.transform.scale(pg.image.load('Jump__009.png'),(323,411))

SLIDING = pg.transform.scale(pg.image.load('Slide__000.png'),(373,351))
SLIDING1 = pg.transform.scale(pg.image.load('Slide__001.png'),(373,351))
SLIDING2 = pg.transform.scale(pg.image.load('Slide__002.png'),(373,351))
SLIDING3 = pg.transform.scale(pg.image.load('Slide__003.png'),(373,351))
SLIDING4 = pg.transform.scale(pg.image.load('Slide__004.png'),(373,351))
SLIDING5 = pg.transform.scale(pg.image.load('Slide__005.png'),(373,351))
SLIDING6 = pg.transform.scale(pg.image.load('Slide__006.png'),(373,351))
SLIDING7 = pg.transform.scale(pg.image.load('Slide__007.png'),(373,351))
SLIDING8 = pg.transform.scale(pg.image.load('Slide__008.png'),(373,351))
SLIDING9 = pg.transform.scale(pg.image.load('Slide__009.png'),(373,351))



ninja_star = pg.image.load("Kunai.png")
player_image = pg.image.load("Run__000.png")
ninja_star_rotated = pg.transform.rotate(ninja_star, -90)
class Player(pg.sprite.Sprite):
    def __init__(self, game, run_frames):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = player_image 
        self.image = pg.transform.scale(self.image, (200,200))
        self.rect = self.image.get_rect()
        self.start_y = 990
        self.pos = vec(400, self.start_y)
        self.jump_height = 500
        self.rect.bottomleft = self.pos
        self.speed = 5
        self.score = 0
        self.obstacles = 0
        self.current_frame = 0
        self.last_update = 0
        self.ammo = 100
        self.max_ammo = 100
        self.hp = 100
        self.running = True
        self.jumping = False
        self.attacking = False
        self.throwing = False
        self.falling = False
        self.sliding = False
        self.slide_start = 0
        self.running_frames = run_frames
        self.falling_speed = 10
        for img in self.running_frames:
            img = pg.transform.scale(img, (50, 50))
            test = img.get_size()
            #print(test)

        for img in self.running_frames:
            print(img)

        self.jumping_frames = [JUMPING1, JUMPING2, JUMPING3, JUMPING4, JUMPING5, JUMPING6, JUMPING7, JUMPING8, JUMPING9]
        self.sliding_frames = [SLIDING, SLIDING1, SLIDING2, SLIDING3, SLIDING4, SLIDING5, SLIDING6, SLIDING7, SLIDING8, SLIDING9]
    def update(self):
        self.animate()
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            self.pos.x += self.speed
        if keys[pg.K_s]:
            self.pos.x -= self.speed
    
        if keys[pg.K_4] and self.ammo >= self.max_ammo:
            self.shoot()
            
        if self.ammo < self.max_ammo:
            self.ammo += 1

        if keys[pg.K_SPACE] and not self.jumping and not self.falling and not self.sliding:
            self.jumping = True
            self.running = False
            self.sliding = False
            self.pos.y = 820
        if keys[pg.K_LCTRL] and not self.sliding and not self.jumping and not self.falling:
            print('slide start')
            self.sliding = True
            self.running = False
            
            self.slide_start = pg.time.get_ticks()   

        if self.pos.y < self.jump_height:
            self.jumping = False
            self.falling = True
            

        if self.jumping:
            self.pos.y -= 10
            self.running = False
        

        if self.falling:
            self.pos.y += self.falling_speed
        
        if self.pos.y > self.start_y and not self.sliding:
            self.falling = False
            self.running = True
            self.pos.y = self.start_y

        if self.sliding:
            self.pos.x += 2
            
            now = pg.time.get_ticks()
            if now - self.slide_start > 1000:
                self.sliding = False
                self.running = True
                print('slide stop')
        

        self.rect.bottomleft = self.pos
        
        #print('falling is: ', self.falling, 'jumping is: ', self.jumping)
    
    def shoot(self):
        if self.ammo >= self.max_ammo:
            self.ammo -= self.max_ammo
            ninja_star_sound = mixer.Sound("Knife.mp3")
            ninja_star_sound.play()
            self.projectile = Projectile(self, self.game)



    def animate(self):
        now = pg.time.get_ticks()

        if self.running:
            if now - self.last_update > 45:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.running_frames)
                self.image = self.running_frames[self.current_frame]
                self.rect = self.image.get_rect()
                #print ("running")
        if self.jumping:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.jumping_frames)
                self.image = self.jumping_frames[self.current_frame]
                self.rect = self.image.get_rect()            
        if self.sliding:
            if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.sliding_frames)
                self.image = self.sliding_frames[self.current_frame]
                self.rect = self.image.get_rect()    
                #print ("sliding")


class Projectile(pg.sprite.Sprite):
    def __init__(self, player, game):
        pg.sprite.Sprite.__init__(self)
        self.player = player
        self.game = game
        self.game.all_sprites.add(self)
        self.game.projectiles.add(self)
        self.image = ninja_star_rotated
        self.image = pg.transform.scale(self.image, (160, 32))
        self.rect = self.image.get_rect()
        self.pos = vec(self.player.pos.x, self.player.pos.y)
        self.rect.center = self.pos
        self.speed_x = 25

    def update(self):
        self.pos.x += self.speed_x

        self.rect.center = self.pos
class Obstacle(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)
        self.game.obstacles.add(self)
        self.image = self.game.rock_image

     
        
        self.rect = self.image.get_rect()
        self.pos = vec(2300, 900)
        self.image = pg.transform.scale(self.image, (300, 300))
        self.rect.center = self.pos
        self.speed_x = 15
        self.damage = 33
    def update(self):
        self.pos.x -= self.speed_x

        self.rect.center = self.pos

class Bird(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.game.all_sprites.add(self)
        self.game.obstacles.add(self)
        self.image = self.game.bird_frames[0]
        self.images = self.game.bird_frames
        self.current_frame = 0
        self.last_update = 0
        self.rect = self.image.get_rect()
        self.pos = vec(2300, 450)
        self.image = pg.transform.scale(self.image, (300, 300))
        self.rect.center = self.pos
        self.speed_x = 15

        self.living = True
        
    def update(self):
        self.animate()
        self.pos.x -= self.speed_x

        self.rect.center = self.pos

        if self.pos.x < -200:
            self.kill()

    def animate(self):

        now = pg.time.get_ticks()

        
        if now - self.last_update > 80:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.images)
                self.image = self.images[self.current_frame]
                self.rect = self.image.get_rect()   
                #print("animated")
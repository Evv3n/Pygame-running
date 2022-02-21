from pickle import FALSE
import pygame as pg
from sprites import *
from pygame import mixer
from random import randint

#settings
WIDTH = 1920
HEIGHT = 1080
FPS = 60

MIDDLE = (WIDTH/2, HEIGHT/2)

	

icon = pg.image.load("icon.png")
pg.display.set_icon(icon)
pg.display.set_caption("Ninja running game")


GRAY = (20,20,20)
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED= (255,0,0)
mixer.init()
mixer.music.load("Blades of Might.mp3")
mixer.music.set_volume(1)
mixer.music.play()
class Game():
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.load_images()
        self.bg_img = pg.image.load("mainbg.png").convert_alpha()
        self.bg_i = 0
        self.bahnschrift50 = pg.font.SysFont("bahnschrift", 50)
        self.bahnschrift100 = pg.font.SysFont("bahnschrift", 100)
        self.clock = pg.time.Clock()
        self.start_bg = pg.image.load("startscreenbg.png").convert_alpha()
        
        self.start_text= self.bahnschrift100.render("Press Backspace to start", False, (WHITE))
        self.game_text = self.bahnschrift100.render("Game over", False, (WHITE))
        self.game_end_text = self.bahnschrift100.render("Press Escape to quit game", False, (WHITE))
        self.game_restart_text = self.bahnschrift100.render("Press Backspace to try again", False, (WHITE))
        self.start_screen_func()
 


    def load_images(self):
        RUNNING = pg.transform.scale(pg.image.load('Run__000.png'),(368,450)).convert_alpha()
        RUNNING1 = pg.transform.scale(pg.image.load('Run__001.png'),(368,450)).convert_alpha()
        RUNNING2 = pg.transform.scale(pg.image.load('Run__002.png'),(368,450)).convert_alpha()
        RUNNING3 = pg.transform.scale(pg.image.load('Run__003.png'),(368,450)).convert_alpha()
        RUNNING4 = pg.transform.scale(pg.image.load('Run__004.png'),(368,450)).convert_alpha()
        RUNNING5 = pg.transform.scale(pg.image.load('Run__005.png'),(368,450)).convert_alpha()
        RUNNING6 = pg.transform.scale(pg.image.load('Run__006.png'),(368,450)).convert_alpha()
        RUNNING7 = pg.transform.scale(pg.image.load('Run__007.png'),(368,450)).convert_alpha()
        RUNNING8 = pg.transform.scale(pg.image.load('Run__008.png'),(368,450)).convert_alpha()
        RUNNING9 = pg.transform.scale(pg.image.load('Run__009.png'),(368,450)).convert_alpha()
        self.rock_image = pg.image.load("Rock.png").convert_alpha()
        BIRD1 = pg.transform.scale(pg.image.load('bird-1.png'),(323,411)).convert_alpha()
        BIRD2 = pg.transform.scale(pg.image.load('bird-2.png'),(323,411)).convert_alpha()

        BIRD1 = pg.transform.flip(BIRD1, True, False).convert_alpha()
        BIRD2 = pg.transform.flip(BIRD2, True, False).convert_alpha()

        self.bird_frames = [BIRD1, BIRD2]

        self.running_frames = [RUNNING, RUNNING1, RUNNING2, RUNNING3, RUNNING4, RUNNING5, RUNNING6, RUNNING7, RUNNING8, RUNNING9]
    def start_screen_func(self):
        start_screen = True
        while start_screen:
            self.screen.blit(self.start_bg,(0,0))
            text_width = self.start_text.get_width()
            self.screen.blit(self.start_text, ((WIDTH - text_width)/2, HEIGHT/2))

            pg.display.update()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    start_screen = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        start_screen = False

        self.new()
        mixer.music.play()
    def game_over_func(self):
            gameover_screen = True
            while gameover_screen:
                self.screen.blit(self.start_bg,(0,0))
                text_width = self.game_text.get_width()
                text2_width = self.game_end_text.get_width()
                text3_width = self.game_restart_text.get_width()
                self.screen.blit(self.game_text, ((WIDTH - text_width)/2, HEIGHT/2))
                self.screen.blit(self.game_end_text, ((WIDTH - text2_width)/2, HEIGHT/2 + 100))
                self.screen.blit(self.game_restart_text, ((WIDTH - text3_width)/2,HEIGHT/2 + 200))
                pg.display.update()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        gameover_screen = False
                        pg.quit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            gameover_screen = False
                        if event.key == pg.K_BACKSPACE:
                            self.start_screen_func()
            self.new()

        
    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.projectiles = pg.sprite.Group()
        self.my_player = Player(self, self.running_frames)
        self.all_sprites.add(self.my_player)
        self.difficulty = -3
        self.difficulty_amount = 100
        self.increase_difficulty = False
        self.last_score = 0
        
    


        self.run()
        
    def run(self):
        self.playing = True
        while self.playing: #GAME LOOP
            self.clock.tick(FPS)
            #print(self.clock.get_fps())

            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    self.playing = False
                    self.new()
            if event.type == pg.MOUSEBUTTONUP:
                self.my_player.shoot()
                
    def update (self):
        self.all_sprites.update()

        now = pg.time.get_ticks()

        if self.last_score + 800 < now:
            self.last_score = now

            self.my_player.score += 8
        
        self.hits = pg.sprite.spritecollide(self.my_player, self.obstacles, True)
        

        self.hits2 = pg.sprite.groupcollide(self.projectiles, self.obstacles, True, True)
        if self.hits:
            self.my_player.hp -= 35
    
        if self.my_player.hp <= 0:
            self.game_over_func()

     
        if self.increase_difficulty:
            self.difficulty_amount += 100
            self.increase_difficulty = False
            self.difficulty -= 2
    def draw(self): 
        self.screen.blit(self.bg_img,(self.bg_i,0))
        self.screen.blit(self.bg_img,(WIDTH+self.bg_i,0))
        if(self.bg_i<= -WIDTH):
            self.screen.blit(self.bg_img,(WIDTH+self.bg_i,0))
            self.bg_i=0
        #skjerm fart
        self.bg_i-=20
        while len(self.obstacles) < 1:
            rand = randint(1,2)
            if rand == 1:
                self.box = Obstacle(self)
            if rand == 2:
                self.bird = Bird(self)

       
            
            
        

        self.all_sprites.draw(self.screen) 
        self.text_player_score = self.bahnschrift50.render(str(self.my_player.score) + " Score", False, (WHITE))
        self.text_player_ammo = self.bahnschrift50.render( "Cooldown: " + str(self.my_player.ammo) + "%", False, (WHITE))
        self.text_player_hp = self.bahnschrift50.render("HP: " + str(self.my_player.hp), False, (WHITE))
        self.screen.blit(self.text_player_score, (1700, 0))
        self.screen.blit(self.text_player_ammo, (40, 0))
        self.screen.blit(self.text_player_hp, (100, 100))
        #Oppdaterer alt på skjermen
        pg.display.update()

g = Game()


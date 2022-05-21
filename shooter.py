import pygame,sys,time,random
from pygame.locals import *


class Main:
    def __init__(self):
        pygame.init()
        #WINDOW DISPLAY
        self.WIDTH = 800
        self.HEIGHT = 600
        self.DISPLAY_SURF = pygame.display.set_mode((self.WIDTH,self.HEIGHT))
        pygame.display.set_caption('Shooter')
        icon = pygame.image.load('gameart/tank.png')
        pygame.display.set_icon(icon)
        
       
        #IMAGES
        self.bullet = pygame.image.load('gameart/bullet.png').convert_alpha()
        self.enemy1 = pygame.image.load('gameart/smallenemy1.png').convert_alpha()
        self.enemy2 = pygame.image.load('gameart/smallenemy2.png').convert_alpha()
        self.smoke = pygame.image.load('gameart/smoke.png').convert_alpha()
        self.smoke2 = pygame.image.load('gameart/smoke3.png').convert_alpha()
        self.hiteffect = pygame.image.load('gameart/explode.png').convert_alpha()
        self.tank = pygame.image.load('gameart/main_tank.png').convert_alpha()

        #SOUNDS
        self.firesound = pygame.mixer.Sound('gamesound/fire.wav')
        self.clashsound = pygame.mixer.Sound('gamesound/explosion.wav')

        #FONTS
        self.font1 = pygame.font.SysFont('Lobster Regular',30)
        self.font2 = pygame.font.SysFont('Nerko One Regular',120)

        #PARAMETERS
        self.bulletwidth = 10
        self.bulletheight = 10
        self.enemyheight = 25
        self.looper = 1
        self.enemywidth = 50
        self.lighting = False
        self.enemyspeed = 5
        self.bulletspeed = 10
        self.score = 0
        self.gameover = False
        self.life = 5
        self.tankwidth = 70
        self.tankheight = 70
        self.bullet_rect = self.bullet.get_rect()
        self.bulletlist = []
        self.enemylist = []
        self.healthbarheight = 10
        self.healthbarwidth = self.tankwidth
        self.healthbarmargin = self.healthbarheight + 5
        self.lifemargin = self.tankwidth/self.life
        self.FPS = 30
        self.mainlifewidth = (self.lifemargin * self.life) - 3
        self.quarterlifewidth = 25/100 * self.mainlifewidth
        self.halflifewidth = 50/100 * self.mainlifewidth

        #COLORS
        self.DARKGREEN = (13,105,56)
        self.LIGHTGREEN = (14,235,62)
        self.DARKRED = (115,15,30)
        self.LIGHTRED = (240,14,52)
        self.DARKBLUE = (16,61,209)
        self.LIGHTBLUE = (113,143,240)
        self.LIGHTYELLOW = (245,241,10)
        self.DARKYELLOW = (173,170,5)
        self.BLACK = (0,0,0)
        self.WHITE= (255,255,255)
        self.healthcolor = self.LIGHTGREEN
       
       

        self.game()


    def game(self):
        running = True
        self.lastshoottime = time.time()
        self.tank_posx = self.WIDTH/2 - 35
        self.tank_posy = self.HEIGHT - 70 - self.healthbarmargin
        self.clock = pygame.time.Clock()
        while running:
            self.gamebackground()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEMOTION:
                    mousex,mousey = event.pos
                    if mousex < self.WIDTH - 70:
                        self.tank_posx = mousex
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.createcannonball_keyevent()
                        self.firesound.play()

            self.createsmallenemy()
            self.drawsmallenemy()
            self.movesmallenemy()
            self.removesmallenemy()
            self.drawcannonball()
            self.movecannonball()
            self.removebullet()
            
            self.drawtank(self.tank_posx,self.tank_posy)
            self.healthbar()
            self.scorelabel()
            
            if self.lighting:
                self.drawlighting()
                self.lighting = False
            if self.gameover:
                self.gameoverscreen()                
                time.sleep(2)
                running = False
                break
            self.enemybulletcollision()
            self.enemytankcollision()
            
            

            pygame.display.update()
            self.clock.tick(self.FPS)
    def gamebackground(self):
        background = pygame.image.load('gameart/background.png')
        background_rect = background.get_rect()
        background_rect.topleft = (0,0)
        self.DISPLAY_SURF.blit(background,background_rect)
    def drawtank(self,tankposx,tankposy):
        self.DISPLAY_SURF.blit(self.tank,(tankposx,tankposy))
    def createcannonball_keyevent(self):
        x = self.tank_posx + 30
        y = self.tank_posy - self.bulletheight -5 
        self.bulletlist.append([x,y])
        self.lighting = True
    def createcannonball(self):
        if len(self.bulletlist) < 10:
            delay = random.random()
            if delay < 0.1:
                x = self.tank_posx + 30
                y = self.tank_posy - self.bulletheight -5 
                self.bulletlist.append([x,y])
    def movecannonball(self):
        for x in self.bulletlist:
            x[1] -= self.bulletspeed
            
    def drawcannonball(self):
        for x in self.bulletlist:
            self.DISPLAY_SURF.blit(self.bullet,x)
            self.firesound.play()
            
    def createsmallenemy(self):
        if len(self.enemylist) < 20:
            delay = random.random()
            if delay < 0.1:
                x = random.randint(0,self.WIDTH - self.enemywidth)
                y = 0
                self.enemylist.append([x,y])
    def removesmallenemy(self):
        for x in self.enemylist:
            if x[1] > self.HEIGHT:
                self.enemylist.remove(x)
    def movesmallenemy(self):
        for x in self.enemylist:
            x[1] += self.enemyspeed
    def drawsmallenemy(self):
        if self.looper <= 20:
            for x in self.enemylist:
                self.DISPLAY_SURF.blit(self.enemy1,x)
            self.looper += 1
        else:
            if self.looper <= 50:
                for x in self.enemylist:
                    self.DISPLAY_SURF.blit(self.enemy2,x)
                self.looper =+ 1
            else:
                self.looper = 1
    def drawsmallenemy2(self):
        for x in self.enemylist:
            for _ in range(255):
                self.DISPLAY_SURF.blit(self.enemy2,x)
            for _ in range(255):
                self.DISPLAY_SURF.blit(self.enemy2,x)

    def removebullet(self):
        for x in self.bulletlist:
            if x[1] < 0:
                self.bulletlist.remove(x)
    def enemybulletcollision(self):
        for a in self.bulletlist:
            for b in self.enemylist:

                x = pygame.Rect(a[0],a[1],self.bulletwidth,self.bulletheight)
                y = pygame.Rect(b[0],b[1],self.enemywidth,self.enemyheight)

                if x.colliderect(y):
                    self.bulletlist.remove(a)
                    self.enemylist.remove(b)
                    self.score += 1
                    self.clashsound.play()
                    for _ in range(500):
                        self.DISPLAY_SURF.blit(self.smoke,y)
    def drawlighting(self):
        for _ in range(255):
            x = self.tank_posx + 30
            y = self.tank_posy - self.bulletheight -5 
            self.DISPLAY_SURF.blit(self.smoke2,(x,y))
    def scorelabel(self):
        score_text = self.font1.render('SCORE: '+str(self.score),1,self.DARKGREEN)
        score_rect = score_text.get_rect()
        score_rect.topright = (self.WIDTH - 30,20)
        self.DISPLAY_SURF.blit(score_text,score_rect)
    def enemytankcollision(self):
        x = self.tank_posx
        y = self.tank_posy
        for a in self.enemylist:
            if x >= a[0] and x < a[0] + self.enemywidth or a[0] >= x and  a[0] < x +self.tankwidth:
                if y >= a[1] and y < a[1] + self.enemyheight or a[1] >= y and a[1] < y + self.tankheight:
                    if self.life <= 0:
                        self.gameover = True
                    else:
                        self.life -= 1
                        w = a
                        self.enemylist.remove(a)
                        self.DISPLAY_SURF.blit(self.hiteffect,w)

    def healthbar(self):
        x = self.tank_posx
        y = self.tank_posy + self.tankheight
        a = self.tank_posx + 2
        b = y + 2 
        lifebarwidth = int(self.lifemargin * self.life) - 3
        lifebarheight = self.healthbarheight - 2
        pygame.draw.rect(self.DISPLAY_SURF,self.DARKGREEN,[x,y,self.healthbarwidth,self.healthbarheight],2)
        
        if self.life:
            pygame.draw.rect(self.DISPLAY_SURF,self.healthcolor,[a,b,lifebarwidth,lifebarheight])
        if lifebarwidth <= self.quarterlifewidth:
            self.healthcolor = self.LIGHTRED
        if lifebarwidth <= self.halflifewidth and lifebarwidth > self.quarterlifewidth:
            self.healthcolor = self.LIGHTYELLOW
        
    def gameoverscreen(self):
        text = self.font2.render('G A M E O V E R',1,self.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (self.WIDTH/2,self.HEIGHT/2)
        self.DISPLAY_SURF.blit(text,text_rect)
        pygame.display.update()
    def highscoretext(self):
        pass
    def mainscreen(self):
        text = self.font1.render('S H O O T E R',1,self.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (self.WIDTH/2,self.HEIGHT/2)
        self.DISPLAY_SURF.blit(text,text_rect)
        pygame.display.update()
    def optionscreen(self):
        pass



        

pygame.init()
main = Main()


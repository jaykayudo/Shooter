import pygame,sys,time,random,yaml
import tkinter as tk
import tkinter.messagebox as msgbox
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
        self.bullet = pygame.image.load('gameart/bullet.png')#.convert_alpha()
        self.enemy1 = pygame.image.load('gameart/smallenemy1.png')#.convert_alpha()
        self.enemy2 = pygame.image.load('gameart/smallenemy2.png')#.convert_alpha()
        self.smoke = pygame.image.load('gameart/smoke.png')#.convert_alpha()
        self.smoke2 = pygame.image.load('gameart/smoke3.png')#.convert_alpha()
        self.hiteffect = pygame.image.load('gameart/explode.png')#.convert_alpha()
        self.tank = pygame.image.load('gameart/main_tank.png')#.convert_alpha()

        #SOUNDS
        self.firesound = pygame.mixer.Sound('gamesound/fire.wav')
        self.clashsound = pygame.mixer.Sound('gamesound/explosion.wav')
        self.clicksound = pygame.mixer.Sound('gamesound/click.wav')
        self.hoversound = pygame.mixer.Sound('gamesound/hover.wav')
        self.all_sounds = [self.firesound,self.clashsound,self.clicksound,self.hoversound]

        #FONTS
        self.font1 = pygame.font.SysFont('Lobster Regular',30)
        self.font2 = pygame.font.SysFont('Nerko One Regular',120)
        self.font3 = pygame.font.SysFont('Modak',120)
        self.symbols = pygame.font.SysFont('Webdings',30)
        self.font4 = pygame.font.SysFont('Pristina',50)
        self.font5 = pygame.font.SysFont('Modak',70)
        self.font6 = pygame.font.SysFont('Dancing Script',40)

        #PARAMETERS
        self.bulletwidth = 10
        self.bulletheight = 10
        self.enemyheight = 25
        self.looper = True
        self.enemywidth = 50
        self.lighting = False
        self.enemyspeed = 5
        self.bulletspeed = 10
        self.score = 0
        self.gameover = False
        self.originallife = 10
        self.life = 10
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
        self.main_volume = 250
        self.main_music_volume = 250
        self.highscore = 0
        self.playerspeed = 5
        self.pause = False

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

        #CONTROLS
        self.left_controller = K_LEFT
        self.right_controller = K_RIGHT
       
       

        #self.game()
        self.load_saves()
        self.load_volume()
        self.menu()


    def game(self):
        self.running = True
        movex = 0
        self.reset_all()
        self.gameover = False
        self.lastshoottime = time.time()
        
        self.clock = pygame.time.Clock()
        while self.running:
            self.gamebackground()
            for event in pygame.event.get():
                if event.type == QUIT:
                    confirm = self.confirm_quit()
                    if confirm:

                        self.save()
                        
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEWHEEL:
                    print(event)
                    
                # if event.type == MOUSEMOTION:
                #     mousex,mousey = event.pos
                #     if mousex < self.WIDTH - 70:
                #         self.tank_posx = mousex
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.createcannonball_keyevent()
                        
                    if event.key == self.left_controller:
                        movex -= self.playerspeed
                    if event.key == self.right_controller:
                        movex += self.playerspeed
                    if event.key == K_p:
                        self.pause = True
                        self.paused()
                if event.type == KEYUP:
                    if event.key == self.left_controller or event.key == self.right_controller:
                        movex = 0

            if self.tank_posx >= 0 and self.tank_posx <= self.WIDTH - self.tankwidth:
                self.tank_posx += movex
            else:
                if self.tank_posx <=0:
                    self.tank_posx += 5
                else:
                    self.tank_posx -= 5
                
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
                self.running = False
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
        self.firesound.play()
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
        if self.looper:
            for x in self.enemylist:
                self.DISPLAY_SURF.blit(self.enemy1,x)
        
        else:
            for x in self.enemylist:
                self.DISPLAY_SURF.blit(self.enemy2,x)
            self.looper = True

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
                        w = a
                        self.enemylist.remove(a)
                        self.DISPLAY_SURF.blit(self.hiteffect,w)
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
        lifebarheight = self.healthbarheight - 3
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
        text_rect.center = (int(self.WIDTH/2),int(self.HEIGHT/2))
        self.DISPLAY_SURF.blit(text,text_rect)
        pygame.display.update()
    def highscoretext(self):
        pass
    def mainscreen(self):
        # text = pygame.image.load('gameart/shootertext3.png')
        # text_rect = text.get_rect()
        # text_rect.center = (int(self.WIDTH/2),int(self.HEIGHT/2 -200))
        text = self.font3.render('S H O O T E R',1,self.BLACK)
        text_rect = text.get_rect()
        text_rect.center = (int(self.WIDTH/2),int(self.HEIGHT/2 - 100))
        self.DISPLAY_SURF.blit(text,text_rect)
    def menubackground(self):
        image = pygame.image.load('gameart/menubackground.png')
        image_rect = image.get_rect()
        image_rect.topleft = (0,0)
        self.DISPLAY_SURF.blit(image,image_rect)
    def startgametext(self,text,text2,text3):
        starttext = self.font4.render(text,1,self.DARKBLUE,self.LIGHTGREEN)
        optiontext = self.font4.render(text2,1,self.DARKBLUE)
        quittext = self.font4.render(text3,1,self.DARKBLUE)
        indicator = self.font4.render('>>',1,self.DARKGREEN)
        self.DISPLAY_SURF.blit(starttext,(60,300))
        self.DISPLAY_SURF.blit(indicator,(10,300))
        self.DISPLAY_SURF.blit(optiontext,(30,350))
        self.DISPLAY_SURF.blit(quittext,(30,400))
    def optiongametext(self,text,text2,text3):
        starttext = self.font4.render(text,1,self.DARKBLUE)
        optiontext = self.font4.render(text2,1,self.DARKBLUE,self.LIGHTGREEN)
        quittext = self.font4.render(text3,1,self.DARKBLUE)
        indicator = self.font4.render('>>',1,self.DARKGREEN)
        self.DISPLAY_SURF.blit(starttext,(30,300))
        self.DISPLAY_SURF.blit(indicator,(10,350))
        self.DISPLAY_SURF.blit(optiontext,(60,350))
        self.DISPLAY_SURF.blit(quittext,(30,400))
    def endgametext(self,text,text2,text3):
        starttext = self.font4.render(text,1,self.DARKBLUE)
        optiontext = self.font4.render(text2,1,self.DARKBLUE)
        quittext = self.font4.render(text3,1,self.DARKBLUE,self.LIGHTGREEN)
        indicator = self.font4.render('>>',1,self.DARKGREEN)
        self.DISPLAY_SURF.blit(starttext,(30,300))
        self.DISPLAY_SURF.blit(indicator,(10,400))
        self.DISPLAY_SURF.blit(optiontext,(30,350))
        self.DISPLAY_SURF.blit(quittext,(60,400))
    def optionscreen(self):
        opt = True
        while opt:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit('success')
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.clicksound.play()
                        opt = False
            
            self.menubackground()
            head = self.font5.render('O P T I O N S',1,self.DARKGREEN)
            head_rect = head.get_rect()
            head_rect.center = (int(self.WIDTH/2),int(self.HEIGHT/2 - 250))
            self.DISPLAY_SURF.blit(head,head_rect)
            self.volume_toggle(220,130)
            self.music_volume_toggle(220,170)
            pygame.display.update()




    def menu(self):
        controller = 1
        gaming = True
        while gaming:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit('success')
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if controller > 1:
                            controller -= 1
                            self.hoversound.play()
                
                            
                    if event.key == K_DOWN:
                        if controller < 3:
                            controller += 1
                            self.hoversound.play()
                    if event.key == K_RETURN:
                        self.clicksound.play()
                        if controller == 1:
                            self.game()
                        elif controller == 2:
                            self.optionscreen()
                        
                            
            
            
            
            self.menubackground()
            self.mainscreen()
            if controller == 1:
                self.startgametext("PLAY",'OPTIONS','QUIT')
            elif controller == 2:
                self.optiongametext('PLAY','OPTIONS','QUIT')
            elif controller == 3:
                self.endgametext('PLAY','OPTIONS','QUIT')
            pygame.display.update()


    def volume_toggle(self,posx,posy):
    	

        pygame.draw.rect(self.DISPLAY_SURF,self.DARKBLUE,[posx,posy,500,20])
        mouse_pos = pygame.mouse.get_pos()
        click_pos = pygame.mouse.get_pressed()


        label = self.font6.render("S o u n d",1,self.DARKGREEN)
        self.DISPLAY_SURF.blit(label,(10,posy - 15))
        if posx+500 >mouse_pos[0]> posx and posy + 20 > mouse_pos[1] >posy:    
            if click_pos[0] == 1:
                self.main_volume = mouse_pos[0]
                pygame.draw.line(self.DISPLAY_SURF,self.LIGHTBLUE,(posx + 5,posy+10),(self.main_volume,posy+10),5)

        pygame.draw.line(self.DISPLAY_SURF,self.WHITE,(posx +5 ,posy + 10),(self.main_volume,posy+10),5)

        
        volume = (self.main_volume-210)/500
        
        
        for x in self.all_sounds:
            x.set_volume(volume)
       
    def music_volume_toggle(self,posx,posy):
    	

        pygame.draw.rect(self.DISPLAY_SURF,self.DARKBLUE,[posx,posy,500,20])
        mouse_pos = pygame.mouse.get_pos()
        click_pos = pygame.mouse.get_pressed()


        label = self.font6.render("M u s i c",1,self.DARKGREEN)
        self.DISPLAY_SURF.blit(label,(10,posy - 15))
        if posx+500 >mouse_pos[0]> posx and posy + 20 > mouse_pos[1] >posy:    
            if click_pos[0] == 1:
                self.main_music_volume = mouse_pos[0]
                pygame.draw.line(self.DISPLAY_SURF,self.LIGHTBLUE,(posx + 5,posy+10),(self.main_music_volume,posy+10),5)

        pygame.draw.line(self.DISPLAY_SURF,self.WHITE,(posx +5 ,posy + 10),(self.main_music_volume,posy+10),5)

        
        volume = (self.main_music_volume-210)/500
        #pygame.mixer.music.set_volume(volume)
            


        
    def reset_all(self):
        self.enemylist = []
        self.life = self.originallife
        self.bulletlist = []
        self.gameover = False
        self.healthcolor = self.LIGHTGREEN
        self.tank_posx = self.WIDTH/2 - 35
        self.tank_posy = self.HEIGHT - 70 - self.healthbarmargin

    def save(self):
        content = f"life: {self.originallife}\n" \
                    +f"music_volume: {self.main_music_volume}\n" \
                        +f"sound_volume: {self.main_volume}\n" \
                            +f"high_score: {self.highscore}\n" \
                                +f"enemyspeed: {self.enemyspeed}\n" \
                                    +f"left_controller: {self.left_controller}\n" \
                                        +f"right_controller: {self.right_controller}\n" \
                                            +f"playerspeed: {self.playerspeed}\n"
        with open('shootersave.yaml','w') as file:
            file.write(content)
    def load_saves(self):
        try:
            with open('shootersave.yaml','r') as stream:
                try:
                    config = yaml.load(stream)
                except :
                    print("Error Occurred with Yaml File")
                    return
        except FileNotFoundError as err:
            print(err)
            return
        try:
            self.life = int(config['life'])
            self.originallife = int(config['life'])
            self.main_music_volume = int(config['music_volume'])
            self.main_volume = int(config['sound_volume'])
            self.highscore = int(config['high_score'])
            self.enemyspeed = int(config['enemyspeed'])
            self.playerspeed = int(config['playerspeed'])
            self.enemyspeed = int(config['enemyspeed'])
            self.left_controller = int(config['left_controller'])
            self.right_controller = int(config['right_controller'])
        except:
            return

    def confirm_quit(self):
        if msgbox.askyesno('Quit Shooter','Are you Sure you want to Quit:'):
            return True
        else:
            return False

    def load_volume(self):
        volume = (self.main_volume - 210)/500
        for x in self.all_sounds:
            x.set_volume(volume)
    def paused(self):
        controller = 1
        
        while self.pause:
            self.gamebackground()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        if controller > 1:
                            controller -= 1
                            self.hoversound.play()
                            
                    if event.key == K_DOWN:
                        if controller < 3:
                            controller += 1
                            self.hoversound.play()
                    if event.key == K_RETURN:
                        self.clicksound.play()
                        if controller == 1:
                            self.pause = False
                        elif controller == 2:
                            self.optionscreen()
                        elif controller == 3:
                            self.pause = False
                            self.running = False
                            self.save()
                    if event.key == K_ESCAPE or event.key == K_p:
                        self.pause = False
                        
                            
            
            text = self.font2.render('P A U S E D',1,self.BLACK)
            text_rect = text.get_rect()
            text_rect.center = (int(self.WIDTH/2),int(self.HEIGHT/2) - 100)
            self.DISPLAY_SURF.blit(text,text_rect)
            
            
            if controller == 1:
                self.startgametext("RESUME",'OPTIONS','MAIN MENU')
            elif controller == 2:
                self.optiongametext('RESUME','OPTIONS','MAIN MENU')
            elif controller == 3:
                self.endgametext('RESUME','OPTIONS','MAIN MENU')
            

            pygame.display.update()
            




        

pygame.init()
main = Main()


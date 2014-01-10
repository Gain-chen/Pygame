#coding=utf-8
#1 load library
import pygame
from pygame.locals import *
from bbSprite import Player,Badguy,Bullet,Castle
from sys import exit
import random
import math
class BB:
    def __init__(self,width,height):
        pygame.init()
        self.width=width
        self.height=height
        # set screen size
        self.screen = pygame.display.set_mode((self.width,self.height))
        #load sprites
        self.playerImg = pygame.image.load("resources/bb/images/dude.png")
        self.grassImg = pygame.image.load("resources/bb/images/grass.png")
        self.castleImg = pygame.image.load("resources/bb/images/castle.png")
        self.bulletImg = pygame.image.load("resources/bb/images/bullet.png")
        self.badguyImg = pygame.image.load("resources/bb/images/badguy.png")
        self.gameoverImg = pygame.image.load("resources/bb/images/gameover.png")
        self.gamewinImg = pygame.image.load("resources/bb/images/youwin.png")
        self.healthbarImg = pygame.image.load("resources/bb/images/healthbar.png")
        self.healthImg = pygame.image.load("resources/bb/images/health.png")
        #load sound
        self.hitSound = pygame.mixer.Sound("resources/bb/audio/explode.wav")
        self.enemySound = pygame.mixer.Sound("resources/bb/audio/enemy.wav")
        self.shootSound = pygame.mixer.Sound("resources/bb/audio/shoot.wav")
        self.hitSound.set_volume(0.05)
        self.enemySound.set_volume(0.05)
        self.shootSound.set_volume(0.05)
        pygame.mixer.music.load("resources/bb/audio/moonlight.wav")
        pygame.mixer.music.play(-1,0.0)
        pygame.mixer.music.set_volume(0.25)
        #set activity params 
        self.playerPos = [100,100]
        self.player = Player(self.playerImg,self.playerPos)   
        #define frequency params
        self.bulletFrequency = 0 # define bullet shoot frequency
        self.badguyFrequency = 0 # define badguy frequency
        #define sprite groups
        self.badguys = pygame.sprite.Group()
        self.badguysLeft = pygame.sprite.Group()
        #mark the game whether it is started or not 
        self.running = True
        # score
        self.score = 0
        self.winScore = 10000
        #castle health definition
        self.healthvalue = 194
    #draw object
    def bbDrawText(self,drawStr,drawColor,drawPos):
        draw_font=pygame.font.Font(None,36)
        draw_text=draw_font.render(drawStr,True,drawColor)
        draw_rect = draw_text.get_rect()
        draw_rect.topleft = drawPos
        self.screen.blit(draw_text,draw_rect)
    def bbDraw(self):
        #clear the screen before drawing it            
        self.screen.fill(0)
        # according to relative window size to draw glass 
        for x in range(self.width/self.grassImg.get_width()+1):
            for y in range(self.height/self.grassImg.get_height()+1):
                self.screen.blit(self.grassImg,(x*100,y*100))
        # draw castles
        for posY in range(30,346,105):
            self.screen.blit(self.castleImg,(0,posY)) 
                      
        if not self.player.isHit: 
            self.screen.blit(self.playerImg,self.player.rect)             
        #draw bullet and enemy plane
        self.player.bullets.draw(self.screen)
        self.badguys.draw(self.screen)
        
        #draw health and healthbar
        self.screen.blit(self.healthbarImg,(5,5))
        for hv in range(self.healthvalue):
            self.screen.blit(self.healthImg,(hv+8,8))
        #draw score
        tmpDrawPos = [self.width-100,10]
        tmpDrawColor = [255,0,255]
        self.bbDrawText(str(self.score),tmpDrawColor,tmpDrawPos)
        #update the screen
        pygame.display.update()
    #event loop control  
    def bbEvent(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        keyInput = pygame.key.get_pressed()
        if not self.player.isHit:
            if keyInput[K_UP] or keyInput[K_w]:
                self.player.moveUp()   
            if keyInput[K_DOWN] or keyInput[K_s]:
                self.player.moveDown()
            if keyInput[K_LEFT] or keyInput[K_a]:
                self.player.moveLeft()
            if keyInput[K_RIGHT] or keyInput[K_d]:
                self.player.moveRight()       
    #game control function
    def bbDone(self):
        if not self.player.isHit:
            if self.bulletFrequency == 15: #define the shoot frequency of bullet
                self.shootSound.play()
                self.player.shoot(self.bulletImg) #draw arrow bullet
                self.bulletFrequency = 0
            self.bulletFrequency += 1
                        
        if self.badguyFrequency == 50: #define the enemy frequency
            #generate badguys random
            badguyPos = [self.width-self.badguyImg.get_rect().width,random.randint(0,self.height-self.badguyImg.get_rect().height)]
            tmpBadguy = Badguy(self.badguyImg,badguyPos)
            self.badguys.add(tmpBadguy)
            self.badguyFrequency = 0
        self.badguyFrequency += 1        
        if self.score >=self.winScore: # judge the scrore
            self.running = False
            self.player.isWin = True  
        elif self.healthvalue <=0:
            self.running = False
            self.player.isDead = True  
        for bullet in self.player.bullets:
            bullet.move()
            if bullet.rect.right >= self.width:
                self.player.bullets.remove(bullet)
        for badguy in self.badguys:
            badguy.move()
            if pygame.sprite.collide_circle(badguy,self.player):
                self.badguysLeft.add(badguy)
                self.badguys.remove(badguy)
                self.player.isHit = True  
                self.running = False              
                break
            elif badguy.rect.left <64:
                self.hitSound.play()
                self.healthvalue -= random.randint(5,20)
                self.badguys.remove(badguy)
                
        badguyHitDown = pygame.sprite.groupcollide(self.badguys,self.player.bullets,1,1)
        for badguyDown in badguyHitDown:
            self.badguysLeft.add(badguyDown) 
        for badguyDown in self.badguysLeft: 
            if badguyDown.downIndex == 0:
                self.enemySound.play()           
            if badguyDown.downIndex >7:
                self.badguysLeft.remove(badguyDown)
                self.score += 1000
                continue            
            badguyDown.downIndex +=1 
          
    def bbLoop(self): 
        #timer params    
        self.clock = pygame.time.Clock()   
        while self.running:
            self.clock.tick(60) # set max frame speed per second
            #deal with game task
            self.bbDone()
            #draw screen elements
            self.bbDraw()             
            #loop through the events 
            self.bbEvent()
       #deal with gameover or win task        
        if self.player.isHit or self.player.isDead:                        
            self.screen.blit(self.gameoverImg,(0,0))  
        elif self.player.isWin:            
            self.screen.blit(self.gamewinImg,(0,0))
        tmpDrawPos = [self.screen.get_rect().centerx-100,self.screen.get_rect().centery+100]
        tmpDrawColor = [0,255,0]
        self.bbDrawText("Score:" + str(self.score),tmpDrawColor,tmpDrawPos)
        while True:
            self.bbEvent()
            pygame.display.update()
    
if __name__ =='__main__':
    #construct bb object with window size
    b=BB(640,480)
    b.bbLoop()  
#coding=utf-8
import pygame
from pygame.locals import *
#bullet class
SCREEN_WIDTH=480
SCREEN_HEIGHT=800
class Bullet(pygame.sprite.Sprite):
    def __init__(self,bulletImg,initPos):
        pygame.sprite.Sprite.__init__(self)
        self.image=bulletImg
        self.rect=self.image.get_rect()
        self.rect.midbottom = initPos
        self.speed = 10
    def move(self):
        self.rect.top-=self.speed
class Player(pygame.sprite.Sprite):
    def __init__(self,planeImg,planeRect,initPos):
        pygame.sprite.Sprite.__init__(self)
        self.image=[]  #store player's sprites
        rectSize=len(planeRect)
        for i in range(rectSize):
            self.image.append(planeImg.subsurface(planeRect[i]).convert_alpha())
        self.rect = planeRect[0]  # init the rect of image
        self.rect.topleft = initPos # init the left-up coordinate of rect
        self.speed = 8 # init player speed
        self.bullets = pygame.sprite.Group() # group of player's bullet shot
        
        self.imgIndex=0
        self.is_hit = False    
    def shoot(self,bulletImg):
        bullet=Bullet(bulletImg,self.rect.midtop)
        self.bullets.add(bullet)
    def moveUp(self):
        if self.rect.top<=0:
            self.rect.top=0
        else:
            self.rect.top -=self.speed
    def moveDown(self):
        if self.rect.top >=SCREEN_HEIGHT-self.rect.height:
            self.rect.top = SCREEN_HEIGHT-self.rect.height
        else:
            self.rect.top +=self.speed
    def moveLeft(self):
        if self.rect.left<=0:
            self.rect.left=0
        else:
            self.rect.left -=self.speed
    def moveRight(self):
        if self.rect.right>=SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        else:
            self.rect.right += self.speed
class Enemy(pygame.sprite.Sprite):
    def __init__(self,enemyImg,enemyDownImgs,initPos):
        pygame.sprite.Sprite.__init__(self)
        self.image= enemyImg
        self.rect = self.image.get_rect()
        self.rect.topleft = initPos
        self.downImgs = enemyDownImgs
        self.speed = 2
        self.downIndex = 0
    def move(self):
        self.rect.top +=self.speed
    
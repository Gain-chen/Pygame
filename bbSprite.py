#coding=utf-8
import pygame
width,height=640,480
class Player(pygame.sprite.Sprite):
    def __init__(self,playerImg,playerInitPos):
        pygame.sprite.Sprite.__init__(self)
        self.image=playerImg
        self.rect=self.image.get_rect()
        self.rect.topleft=playerInitPos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.isHit = False # judge whether player is hit or not
        self.isWin = False #judge whether player is win or not
        self.isDead = False #judge whether castle has health or not
    def shoot(self,bulletImg):
        bullet=Bullet(bulletImg,self.rect.midright)
        self.bullets.add(bullet)
    def moveUp(self):
        if self.rect.top <=0:
            self.rect.top=0
        else:
            self.rect.top -=self.speed
    def moveDown(self):
        if self.rect.top >= height-self.rect.height:
            self.rect.top = height-self.rect.height
        else:
            self.rect.top += self.speed
    def moveLeft(self):
        if self.rect.left<=0:
            self.rect.left=0
        else:
            self.rect.left -= self.speed
    def moveRight(self):
        if self.rect.right >= width:
            self.rect.right = width
        else:
            self.rect.right += self.speed
        
class Castle(pygame.sprite.Sprite):
    def __init__(self,castleImg,castleRect,castleHeath,castleInitPos):
        pygame.sprite.Sprite.__init__(self)
        self.images = castleImg
        self.rect = castleRect
        self.heath = castleHeath
        
class Badguy(pygame.sprite.Sprite):
    def __init__(self,badguyImg,badguyInitPos):
        pygame.sprite.Sprite.__init__(self)
        self.image= badguyImg
        self.rect = self.image.get_rect()
        self.rect.topright = badguyInitPos        
        self.speed = 2 
        self.downIndex = 0       
    def move(self):
        self.rect.left -= self.speed
class Bullet(pygame.sprite.Sprite):
    def __init__(self,bulletImg,bulletInitPos):
        pygame.sprite.Sprite.__init__(self)
        self.image=bulletImg
        self.rect=self.image.get_rect()
        self.rect.midleft = bulletInitPos
        self.speed = 10
    def move(self):
        self.rect.right += self.speed
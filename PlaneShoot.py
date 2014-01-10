#-*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from sys import exit
import random
from PlaneSprite import Bullet,Player,Enemy

SCREEN_WIDTH=480
SCREEN_HEIGHT=800
def PlaneShoot():
    #init game
    pygame.init()
    screen_size=(SCREEN_WIDTH,SCREEN_HEIGHT)
    screen=pygame.display.set_mode(screen_size)
    pygame.display.set_caption('Shoot Plane')
    
    #load background sound
    bulletSound=pygame.mixer.Sound('resources/plane/sound/bullet.wav')
    enemyDownSound = pygame.mixer.Sound('resources/plane/sound/enemy1_down.wav')
    gameOverSound = pygame.mixer.Sound('resources/plane/sound/game_over.wav')
    bulletSound.set_volume(0.3)
    enemyDownSound.set_volume(0.3)
    gameOverSound.set_volume(0.3)
    pygame.mixer.music.load('resources/plane/sound/game_music.wav')
    pygame.mixer.music.play(-1,0.0)
    pygame.mixer.music.set_volume(0.25)
    
    #load background
    background=pygame.image.load('resources/plane/image/background.png').convert()
    shoot_bk=pygame.image.load('resources/plane/image/shoot_background.png')
    gameOverBk=pygame.image.load('resources/plane/image/gameover.png')
    planeImg = pygame.image.load('resources/plane/image/shoot.png')
    startImg=pygame.image.load('resources/plane/image/start.png')
    stopImg=pygame.image.load('resources/plane/image/stop.png')
    planeRects = []
    planeRects.append(pygame.Rect(0,99,102,126))
    planeRects.append(pygame.Rect(165,360,102,126))
    planeRects.append(pygame.Rect(165,234,102,126))
    planeRects.append(pygame.Rect(330,624,102,126))
    planeRects.append(pygame.Rect(330,498,102,126))
    planeRects.append(pygame.Rect(432,624,102,126))
    
    
    planePos=[200,600]
    player = Player(planeImg,planeRects,planePos)
    
    #define bullet surface params
    bulletRect = pygame.Rect(1004,987,9,21)
    bulletImg = planeImg.subsurface(bulletRect)
    
    #define start gui
    titleRect = pygame.Rect(480,702,440,225)
    titleImg = shoot_bk.subsurface(titleRect)
    screen.blit(titleImg,(20,100))
    #define button
    screen.blit(startImg,(150,325))
    screen.blit(stopImg,(130,420))
    
    
    enemyRect = pygame.Rect(534,612,57,43)
    enemyImg = planeImg.subsurface(enemyRect)
    enemyDownImgs=[]
    enemyDownImgs.append(planeImg.subsurface(pygame.Rect(267,347,57,43)))
    enemyDownImgs.append(planeImg.subsurface(pygame.Rect(873,697,57,43)))
    enemyDownImgs.append(planeImg.subsurface(pygame.Rect(267,296,57,43)))
    enemyDownImgs.append(planeImg.subsurface(pygame.Rect(930,697,57,43)))
    enemies = pygame.sprite.Group()
    enemiesDown = pygame.sprite.Group()
    shootFrequency = 0
    enemyFrequency = 0
    planeDownIndex=16
    score = 0
    clock = pygame.time.Clock()
    running = False
    waitBtnPress=False
    
    while not waitBtnPress:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit() 
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if 150<=event.pos[0]<=startImg.get_rect().width+150 and 325<=event.pos[1]<=startImg.get_rect().height+325:
                    running=True
                    waitBtnPress=True
                    break
                elif 130<=event.pos[0]<=stopImg.get_rect().width+130 and 420<=event.pos[1]<=stopImg.get_rect().height+420:
                    pygame.quit()
                    exit()
                
        pygame.display.update() 
        
    while running:
        clock.tick(60) # control max frame speed
        # control bullet speed 
        if not player.is_hit:
            if shootFrequency % 15 == 0:
                bulletSound.play()
                player.shoot(bulletImg)
            shootFrequency +=1
            if shootFrequency >=15:
                shootFrequency = 0
        #generate enemy
        if enemyFrequency % 50 == 0:
            enemyPos = [random.randint(0,SCREEN_WIDTH-enemyRect.width),0]
            
            tmpEnemy = Enemy(enemyImg,enemyDownImgs,enemyPos)
            enemies.add(tmpEnemy)
        enemyFrequency+=1
        if enemyFrequency>=100:
            enemyFrequency = 0
        #move bullet, if out of range then delete
        for bullet in player.bullets:
            bullet.move()
            if bullet.rect.bottom<0:
                player.bullets.remove(bullet)
        for enemy in enemies:
            enemy.move()
            #judge player is hit or not
            if pygame.sprite.collide_circle(enemy,player):
                enemiesDown.add(enemy)
                enemies.remove(enemy)
                player.is_hit = True
                gameOverSound.play()
                break
            if enemy.rect.top <0:
                enemies.remove(enemy)
        #add those planes which have been hit into group
        enemiesHitDown = pygame.sprite.groupcollide(enemies,player.bullets,1,1)
        for enemy_down in enemiesHitDown:
            enemiesDown.add(enemy_down)
        
        
        #draw background
        screen.fill(0)
        screen.blit(background,(0,0))
        
        #draw player plane
        if not player.is_hit:
            screen.blit(player.image[player.imgIndex],player.rect)
            #change img index and make plane have moving scene
            player.imgIndex = shootFrequency/8
        else:
            player.imgIndex = planeDownIndex/8
            screen.blit(player.image[player.imgIndex],player.rect)
            planeDownIndex+=1
            if planeDownIndex>47:
                running = False
        #draw hit scene
        for enemy_down in enemiesDown:
            if enemy_down.downIndex==0:
                enemyDownSound.play()
            if enemy_down.downIndex >7:
                enemiesDown.remove(enemy_down)
                score += 1000
                continue
            screen.blit(enemy_down.downImgs[enemy_down.downIndex/2],enemy_down.rect)
            enemy_down.downIndex +=1
        
        #draw bullet and enemy plane
        player.bullets.draw(screen)
        enemies.draw(screen)
        #draw score
        score_font=pygame.font.Font(None,36)
        score_text=score_font.render(str(score),True,(128,128,128))
        text_rect = score_text.get_rect()
        text_rect.topleft = [10,10]
        screen.blit(score_text,text_rect)
        
        # update screen
        pygame.display.update()
        
        
        #deal with game exit
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
        keyInput=pygame.key.get_pressed()
        
        if not player.is_hit:
            if keyInput[K_UP] or keyInput[K_w]:
                player.moveUp()    
            if keyInput[K_DOWN] or keyInput[K_s]:
                player.moveDown()
            if keyInput[K_LEFT] or keyInput[K_a]:
                player.moveLeft()
            if keyInput[K_RIGHT] or keyInput[K_d]:
                player.moveRight()
    font = pygame.font.Font(None,48)
    text=font.render('Score: '+str(score),True,(255,0,0))
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery
    screen.blit(gameOverBk,(0,0))
    screen.blit(text,text_rect)
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit() 
        pygame.display.update() #init game
       

    
        
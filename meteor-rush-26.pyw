# Meteor Rush v26 (publicly shared version 1.0) 
# Coding, graphics, and sound: Jason R. Carroll (Twitter: @JasonRobertC) 
# Music credits: 'Battle Theme' by Alex Smith, 'Level 1' by Juhani Junkala, 
# 'Frozen Jam' by Jordan Trudgett 

# *****************
# ***           ***
# ***           ***
# ***           ***
# ***   SETUP   ***
# ***           ***
# ***           ***
# ***           ***
# *****************

import pygame,random,time,sys
from os import path

# graphics and sound file paths 
img_dir = path.join(path.dirname(__file__),'img') 
snd_dir = path.join(path.dirname(__file__),'snd') 

# game constants 
WIDTH = 480 
HEIGHT = 800 
FPS = 60 
POWERUP_TIME = 5000 
INDESTRUCT_DURATION = 5000 

# define colors
WHITE = (255,255,255)
ALMOST_WHITE = (250,220,255)
GRAY1 = (205,205,205)
GRAY2 = (155,155,155)
GRAY3 = (105,105,105)
GRAY3A = (55,55,55)
GRAY4 = (40,40,40)
GRAY5 = (20,20,20)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
PINK = (255,20,147) 

# initialize pygame, sound, clock, create window 
pygame.init() 
pygame.mixer.init() 
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('meteor::RUSH')
clock = pygame.time.Clock()

# initialize high scores 
last_score_3 = [0,0,0] 
last_score_2 = [0,0,0]
last_score_1 = [0,0,0] 
score = 0

# *****************
# ***           ***
# ***           ***
# ***           ***
# *** FUNCTIONS ***
# ***           ***
# ***           ***
# ***           ***
# *****************

def draw_text(surf,text,size,x,y,color=WHITE):
    font = pygame.font.Font(None,size) 
    text_surface = font.render(text,True,color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)
    global mob_count
    mob_count += 1 

def draw_shield_bar(surf,x,y,length,height,outline,color,pct):
    if pct < 0:
        pct = 0
    fill = (pct / 100) * length
    outline_rect = pygame.Rect(x,y,length,height)
    fill_rect = pygame.Rect(x,y,fill,height)
    pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,outline)

def draw_od_bar(surf,x,y,length,height,outline,color,pct):
    if pct < 0:
        pct = 0
    fill = (pct / 100) * height
    outline_rect = pygame.Rect(x,y+height,length,-height) 
    fill_rect = pygame.Rect(x,y+height,length,-fill) 
    pygame.draw.rect(surf,color,fill_rect)
    pygame.draw.rect(surf,WHITE,outline_rect,outline)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img,img_rect)

def show_go_screen():
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    screen.blit(foreground,foreground_rect)
    if last_score_1[1] != 0:
        draw_text(screen,'LAST SCORE / LEVEL:',16,WIDTH/2,HEIGHT*1/64)    
        draw_text(screen,str(last_score_1[0])+' / Lv. '+str(last_score_1[1])
                             +' :: Boss '+str(last_score_1[2]),26,WIDTH/2,
                             HEIGHT*5/128)
    if last_score_2[1] != 0:
        draw_text(screen,str(last_score_2[0])+' / Lv. '+str(last_score_2[1])
                             +' :: Boss '+str(last_score_2[2]),22,WIDTH/2,
                             HEIGHT*9/128,GRAY2)
    if last_score_3[1] != 0:
        draw_text(screen,str(last_score_3[0])+' / Lv. '+str(last_score_3[1])
                             +' :: Boss '+str(last_score_3[2]),18,WIDTH/2,
                             HEIGHT*13/128,GRAY3)
    title_card_rect.midtop = (WIDTH/2,HEIGHT*3/16) 
    screen.blit(title_card,title_card_rect)  
    draw_text(screen,'a   b u l l e t   h e l l   g a m e   b y   '
                     'j .   c a r r o l l',20,WIDTH*8/16,HEIGHT*33/128)
    draw_text(screen,'press -- SPACE -- to begin',20,WIDTH/2,HEIGHT*11/32)
    draw_text(screen,'p o w e r u p s',22,WIDTH*1/2,HEIGHT*28/64)
    draw_text(screen,'shot',20,WIDTH*29/64,HEIGHT*31/64)
    shot_icon = powerup_images['gun']
    shot_icon_rect = shot_icon.get_rect()
    shot_icon_rect.midtop = (WIDTH*35/64,HEIGHT*31/64)
    screen.blit(shot_icon,shot_icon_rect)
    draw_text(screen,'shield',20,WIDTH*29/64,HEIGHT*34/64)
    shield_icon = powerup_images['shield']
    shield_icon_rect = shield_icon.get_rect()
    shield_icon_rect.midtop = (WIDTH*35/64,HEIGHT*34/64)
    screen.blit(shield_icon,shield_icon_rect)
    draw_text(screen,'bomb',20,WIDTH*29/64,HEIGHT*37/64)
    bomb_icon = powerup_images['bomb']
    bomb_icon_rect = bomb_icon.get_rect()
    bomb_icon_rect.midtop = (WIDTH*35/64,HEIGHT*37/64)
    screen.blit(bomb_icon,bomb_icon_rect)
    draw_text(screen,'[ ARROW keys or WASD to move -- SPACE to fire ]',
              20,WIDTH/2,HEIGHT*22/32)
    draw_text(screen,'[ B to bomb -- V for shields ]',20,WIDTH/2,HEIGHT*23/32)
    draw_text(screen,'[ press -- P -- to pause / unpause the game ]',20,
              WIDTH/2,HEIGHT*25/32)
    draw_text(screen,'[ press -- M -- at any time to switch music ]',20,
              WIDTH/2,HEIGHT*26/32) 
    draw_text(screen,'press -- Q -- to quit',20,WIDTH/2,HEIGHT*31/32) 
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  
                    play_next_song()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE: 
                    waiting = False

def check_player_die(): 
    if player.shield <= 0:
        player_die_sound.play()
        global death_explosion
        death_explosion = Explosion(player.rect.center,'player') 
        all_sprites.add(death_explosion)
        player.hide() 
        player.lives -= 1 
        player.shield = 100 

def check_boss_die(): 
    if boss.health <= 0:
        player_die_sound.play()
        global death_explosion
        death_explosion = Explosion(boss.rect.center,'player') 
        all_sprites.add(death_explosion)
        global death_explosion_2
        death_explosion_2 = Explosion(boss.rect.topright,'boss') 
        all_sprites.add(death_explosion_2)
        global death_explosion_3
        death_explosion_3 = Explosion(boss.rect.topleft,'boss') 
        all_sprites.add(death_explosion_3)
        global death_explosion_4
        death_explosion_4 = Explosion(boss.rect.bottomleft,'boss') 
        all_sprites.add(death_explosion_4)
        global death_explosion_5
        death_explosion_5 = Explosion(boss.rect.bottomright,'boss') 
        all_sprites.add(death_explosion_5)
        global boss_flag
        boss_flag = 0
        global score 
        score += 1000000
        global level
        level = 1
        global macro_level
        macro_level += 1
        global boss_level
        boss_level += 5 
        global boss_shoot_rate
        boss_shoot_rate -= 0.1 
        global max_boss_health
        max_boss_health += 1000 
        global last_boss_health
        last_boss_health = max_boss_health
        player.power = 4
        player.shield = 100 
        player.lives += 1
        if player.lives > 3:
            player.lives = 3 
        player.bombs += 1
        if player.bombs > 3:
            player.bombs = 3
        player.indestruct_shield_count += 1
        if player.indestruct_shield_count > 3:
            player.indestruct_shield_count = 3 
        boss.kill()
        global boss_alert
        if boss_alert == 0:
            boss_announce = Shout('boss',WIDTH/2,-10,3)
            all_sprites.add(boss_announce)
            boss_alert = 1
        for i in range(7):
            newmob() 

def respawn(boss_respawn = True): 
    last_mobs_count = len(mobs)
    for mob in mobs:
        mob.kill()
    for mob in mobs2:
        mob.kill()
    for mob in mobs4:
        mob.kill()
    for bullet in bullets:
        bullet.kill()
    for enemy_bullet in enemy_bullets:
        enemy_bullet.kill()
    for i in range(last_mobs_count):
        newmob()
    global mob_count 
    mob_count -= last_mobs_count 
    if boss_respawn:
        global boss_flag
        for boss in boss_group:
            boss.kill() 
        if boss_flag == 1:
            global last_boss_health
            last_boss_health = boss.health
            boss_flag = 0

def play_next_song():
    global songs
    songs = songs[1:] + [songs[0]] 
    pygame.mixer.music.load(path.join(snd_dir,songs[0]))
    pygame.mixer.music.play(-1)

def pause(): 
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_q:
                    global game_over
                    game_over = True
                    paused = False 

# *****************
# ***           ***
# ***           ***
# ***           ***
# ***  OBJECTS  ***
# ***           ***
# ***           *** 
# ***           ***
# *****************

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img 
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 18 
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT-25 
        self.speedx = 0
        self.speedy = 0 
        self.shield = 100
        self.indestruct_shield_count = 3
        self.shoot_delay = 600 
        self.last_shot = pygame.time.get_ticks()
        self.bombs = 3 
        self.bomb_delay = 1000 
        self.last_bomb = pygame.time.get_ticks() 
        self.lives = 3 
        self.hidden = False
        self.hide_time = pygame.time.get_ticks()
        self.prev_power = 2
        self.power = 2  
        self.power_time = pygame.time.get_ticks() 
        self.last_music = pygame.time.get_ticks() 
        self.indestruct = False 
        self.indestruct_time = pygame.time.get_ticks() 
        self.last_indestruct = pygame.time.get_ticks() 
    def update(self):
        if (self.indestruct and (pygame.time.get_ticks() 
            - self.indestruct_time > INDESTRUCT_DURATION)):
            self.indestruct = False
            self.indestruct_time = pygame.time.get_ticks() 
        if self.power > 7: #17
            self.power = 7
        if (self.power >= 7 and (pygame.time.get_ticks() - self.power_time 
            > POWERUP_TIME)):
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT-25 
            respawn() 
        self.speedx = 0
        self.speedy = 0 
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_m]: 
            now_m = pygame.time.get_ticks()
            if now_m - self.last_music > 250:
                self.last_music = now_m
                play_next_song()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx = -4
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx = 4
        if keystate[pygame.K_UP] or keystate[pygame.K_w]: 
            self.speedy = -4
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]: 
            self.speedy = 4
        if keystate[pygame.K_b]: 
            self.bomb() 
        if keystate[pygame.K_v]: 
            self.indestructible() 
        if not self.hidden: 
            if (keystate[pygame.K_SPACE] or keystate[pygame.K_z] 
                or keystate[pygame.K_PERIOD]):
                self.shoot() 
        self.rect.x += self.speedx
        self.rect.y += self.speedy 
        if not self.hidden: 
            if self.rect.left < 0: 
                self.rect.left = 0
            if self.rect.right > WIDTH: 
                self.rect.right = WIDTH
            if self.rect.bottom > (HEIGHT-25):
                self.rect.bottom = (HEIGHT-25) 
            if self.rect.top < (HEIGHT-200): 
                self.rect.top = (HEIGHT-200)
    def powerup(self):
        self.power += 1
        self.prev_power = self.power
        if self.prev_power > 7:
            self.prev_power = 7
        self.power_time = pygame.time.get_ticks()
    def shoot(self):
        global shout_count
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1: 
                self.shoot_delay = 600
                bullet = Bullet(self.rect.centerx,self.rect.top,11,1)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 2: 
                self.shoot_delay = 300
                bullet = Bullet(self.rect.centerx,self.rect.top,15,1)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 3: 
                self.shoot_delay = 200
                bullet = Bullet(self.rect.centerx,self.rect.top,20,2)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power == 4: 
                self.shoot_delay = 225 
                bullet1 = Bullet(self.rect.left+15,self.rect.centery,21,2) 
                bullet2 = Bullet(self.rect.right-15,self.rect.centery,22,2)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if self.power == 5: 
                self.shoot_delay = 200 
                bullet1 = Bullet(self.rect.left+5,self.rect.centery,23,2) 
                bullet2 = Bullet(self.rect.right-5,self.rect.centery,24,2)
                bullet3 = Bullet(self.rect.centerx,self.rect.centery,25,2)  
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
            if self.power == 6: 
                self.shoot_delay = 175 
                bullet1 = Bullet(self.rect.left+5,self.rect.centery,26,2) 
                bullet2 = Bullet(self.rect.right-5,self.rect.centery,27,2) 
                bullet3 = Bullet(self.rect.centerx,self.rect.centery,28,3) 
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                shoot_sound.play()
                shout_count = 0
            if self.power >= 7: 
                self.shoot_delay = 125
                bullet1 = Bullet(self.rect.left-5,self.rect.centery,29,3) 
                bullet2 = Bullet(self.rect.right+5,self.rect.centery,30,3)
                bullet3 = Bullet(self.rect.centerx-10,self.rect.centery,31,3)
                bullet4 = Bullet(self.rect.centerx+10,self.rect.centery,32,3) 
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
                shoot_sound.play()
                if shout_count == 0:
                    if level < boss_level:
                        shout = Shout('overdrive',WIDTH/2,-10,11)
                        all_sprites.add(shout)
                        shout_count = 1
    def hide(self): 
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (-1000,-1000)  
    def indestructible(self):
        now = pygame.time.get_ticks()
        if ((now - self.last_indestruct > self.bomb_delay) and 
            (not self.hidden) and (self.indestruct_shield_count > 0) and 
            (not self.indestruct)):
            self.last_indestruct = now 
            if self.indestruct_shield_count < 0:
                self.indestruct_shield_count = 0 
            self.indestruct = True
            self.indestruct_shield_count -= 1
            self.indestruct_time = pygame.time.get_ticks() 
    def bomb(self): 
        global score
        global mob_count
        global level 
        global bombing
        now = pygame.time.get_ticks()
        if ((now - self.last_bomb > self.bomb_delay) and (not self.hidden) and 
            (self.bombs > 0)): 
            player_die_sound.play()
            self.last_bomb = now
            bombing = True 
            level += 1 
            self.bombs -= 1
            if self.bombs < 0:
                self.bombs = 0 
            for mob in mobs: 
                score += ((60 - mob.radius)*10)
                expl = Explosion(mob.rect.center,random.choice(['lg','sm']))
                all_sprites.add(expl)
                mob_count += 1
            for mob2 in mobs2: 
                score += ((60 - mob2.radius)*10)
                expl = Explosion(mob2.rect.center,'lg')
                all_sprites.add(expl)
            for mob4 in mobs4: 
                score += ((60 - mob4.radius)*10)
                expl = Explosion(mob4.rect.center,'sm')
                all_sprites.add(expl)
            for enemy_bullet in enemy_bullets: 
                expl = Explosion(enemy_bullet.rect.center,'sm')
                all_sprites.add(expl)
            if boss_flag == 1:
                boss.health -= 500
            respawn(False) 

class Shout(pygame.sprite.Sprite): 
    def __init__(self,type,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.type = type 
        if self.type == 'overdrive':
            self.image = shout_img
        elif self.type == 'intro':
            self.image = intro_img
        elif self.type == 'alert_odl':
            self.image = alert_odl_img
        elif self.type == 'boss':
            self.image = boss_alert_img
        else:
            self.image = alert_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT+100: 
            self.kill()

class Mob(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images) 
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy() 
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2) 
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = random.randrange(-200,-100)
        self.speedy = random.randrange(3,9) 
        self.speedx = random.randrange(-2,2)
        self.rot = 0 
        self.rot_speed = random.randrange(-8,8) 
        self.last_update = pygame.time.get_ticks() 
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig,self.rot) 
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate() 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if ((self.rect.top > HEIGHT + 10) or (self.rect.right < -25) or 
            (self.rect.left > WIDTH + 25)):
            self.rect.x = random.randrange(0,WIDTH - self.rect.width)
            self.rect.y = random.randrange(-200,-100)
            self.speedy = random.randrange(3,9)
            self.speedx = random.randrange(-2,2)

class Mob2(pygame.sprite.Sprite): 
    def __init__(self,type):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if self.type == 1:
            self.image = enemy_img
        elif self.type == 2:
            self.image = enemy2_img
        else:
            self.image = enemy3_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2) 
        self.rect.x = random.choice([0,WIDTH])
        self.rect.y = random.randrange(50,300)
        self.speedy = random.randrange(2,6) 
        self.shoot_delay = 500 
        self.last_shot = pygame.time.get_ticks() 
        if self.rect.x == 0:
            self.speedx = random.randrange(2,5)
        else:
            self.speedx = random.randrange(-5,-2)
    def shoot(self):
        now = pygame.time.get_ticks() 
        if now - self.last_shot > self.shoot_delay: 
            self.last_shot = now
            enemy_bullet = Bullet2(self.rect.centerx,self.rect.bottom+15,5)
            all_sprites.add(enemy_bullet)
            enemy_bullets.add(enemy_bullet)
    def update(self):        
        if (player.rect.centerx-11 <= self.rect.centerx 
            <= player.rect.centerx+11):
            self.shoot()
        if random.random() > .97:
            self.shoot()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if ((self.rect.top > HEIGHT + 10) or (self.rect.right < -25) or 
            (self.rect.left > WIDTH + 25)):
            self.kill()

class Mob3(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = storm_bolt
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*1.5) 
        self.rect.x = random.choice([0,WIDTH])
        self.rect.y = random.randrange(-700,600)
        self.speedy = 4.25
        if self.rect.x == 0:
            self.image = pygame.transform.rotate(storm_bolt,35)
            self.speedx = 1.5
        else:
            self.image = pygame.transform.rotate(storm_bolt,-35)
            self.speedx = -1.5
    def update(self):        
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if ((self.rect.top > HEIGHT + 10) or (self.rect.right < -25) or 
            (self.rect.left > WIDTH + 25)):
            self.kill()

class Mob4(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.5) 
        self.rect.x = random.randrange(0,WIDTH)
        self.rect.y = -100
        self.speedy = random.randrange(4,7) 
        self.speedx = 0
    def update(self):        
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if ((self.rect.top > HEIGHT + 10) or (self.rect.right < -25) or 
            (self.rect.left > WIDTH + 25)):
            self.kill()

class Bullet(pygame.sprite.Sprite): 
    def __init__(self,x,y,speed,blevel):
        pygame.sprite.Sprite.__init__(self)
        self.blevel = blevel
        if blevel == 2:
            self.image = bullet_upgrade_img
        elif blevel == 3:
            self.image = bullet_overdrive_img
        else:
            self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -speed
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0: 
            self.kill()

class Bullet2(pygame.sprite.Sprite): 
    def __init__(self,x,y,speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = speed
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT: 
            self.kill()

class Bullet3(pygame.sprite.Sprite): 
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = random.choice([-2,-1,3,4,5,6]) 
        self.speedx = random.choice([-4,-3,-2,-1,0,1,2,3,4]) 
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if ((self.rect.bottom > HEIGHT) or (self.rect.top < 0) or 
            (self.rect.right > WIDTH) or (self.rect.left < 0)):
            self.kill()

class Pow(pygame.sprite.Sprite): 
    def __init__(self,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['gun','gun','shield','bomb'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center 
        self.speedy = 3 
    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT: 
            self.kill()

class Explosion(pygame.sprite.Sprite): 
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        if self.size == 'boss':
            self.frame_rate = 50
        else:
            self.frame_rate = 75 
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate: 
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center 

class Boss(pygame.sprite.Sprite): 
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if macro_level == 1:
            self.image_orig = boss_img 
        elif macro_level == 2:
            self.image_orig = boss2_img
        elif macro_level == 3:
            self.image_orig = boss3_img
        elif macro_level == 4:
            self.image_orig = boss4_img
        elif macro_level == 5:
            self.image_orig = boss5_img
        else:
            self.image_orig = boss6_img 
        self.image_orig.set_colorkey(BLACK) 
        self.image = self.image_orig.copy() 
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 * .825) 
        self.rect.x = random.randrange(0,WIDTH - self.rect.width)
        self.rect.y = -325
        self.speedy = 2 
        self.speedx = 0
        self.rot = 0 
        self.rot_speed = -1 
        self.last_update = pygame.time.get_ticks() 
        self.shoot_delay = 50
        self.last_shot = pygame.time.get_ticks()
        self.health = last_boss_health     
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360 
            new_image = pygame.transform.rotate(self.image_orig,self.rot) 
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def shoot(self):
        now = pygame.time.get_ticks() 
        if now - self.last_shot > self.shoot_delay: 
            self.last_shot = now
            boss_bullet = Bullet3(self.rect.centerx,self.rect.centery)
            all_sprites.add(boss_bullet)
            enemy_bullets.add(boss_bullet)
    def update(self):
        self.rotate() 
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if random.random() > boss_shoot_rate:
            self.shoot()
        if ((self.rect.top > HEIGHT + 10) or (self.rect.right < -25) or 
            (self.rect.left > WIDTH + 25)):
            self.rect.x = random.randrange(0,max(1,WIDTH - self.rect.width))
            self.rect.y = -325
            self.speedy = 2 
            self.speedx = 0

# *****************
# ***           ***
# ***           ***
# ***           ***
# ***  ASSETS   ***
# ***           ***
# ***           ***
# ***           *** 
# *****************

# graphics

title_card = pygame.image.load(
             path.join(img_dir,'title-card.png')
             ).convert() 
title_card.set_colorkey(BLACK)
title_card_rect = title_card.get_rect() 

game_over_card = pygame.image.load(
                 path.join(img_dir,'game-over-blue.png')
                 ).convert()
game_over_card.set_colorkey(BLACK)
game_over_card_rect = game_over_card.get_rect()

background = pygame.image.load(
             path.join(img_dir,'starfield-blue.png')
             ).convert()
background_rect = background.get_rect() 
background.set_colorkey(BLACK) 

foreground = pygame.image.load(
             path.join(img_dir,'starfield-white.png')
             ).convert() 
foreground.set_colorkey(BLACK) 
foreground_rect = foreground.get_rect() 

player_img = pygame.image.load(
             path.join(img_dir,'playerShip3a-h-vector.png')
             ).convert()

player_mini_img = pygame.image.load(
                  path.join(img_dir,'playerShip3a-h-mini-vector.png')
                  ).convert() 
player_mini_img.set_colorkey(BLACK)

enemy_img = pygame.image.load(
            path.join(img_dir,'enemyRed1V-small.png')
            ).convert()
enemy_img.set_colorkey(BLACK)

enemy2_img = pygame.image.load(
             path.join(img_dir,'enemyBlack2V-small.png')
             ).convert()
enemy2_img.set_colorkey(BLACK)

enemy3_img = pygame.image.load(
             path.join(img_dir,'enemyBlue3V-small.png')
             ).convert()
enemy3_img.set_colorkey(BLACK)

bullet_img = pygame.image.load(
             path.join(img_dir,'laserRed02-vector.png')
             ).convert()

bullet_upgrade_img = pygame.image.load(
                     path.join(img_dir,'laserRed02u-vector.png')
                     ).convert()

bullet_overdrive_img = pygame.image.load(
                       path.join(img_dir,'laserRed02u-od-vector.png')
                       ).convert()

enemy_bullet_img = pygame.image.load(
                   path.join(img_dir,'laserBlue08V-sm.png')
                   ).convert()

storm_bolt = pygame.image.load(
             path.join(img_dir,'laserBlue15V.png')
             ).convert() 
storm_bolt.set_colorkey(BLACK)

fireball = pygame.image.load(
           path.join(img_dir,'fireballV.png')
           ).convert() 
fireball.set_colorkey(BLACK)

meteor_images = [] 
meteor_list = ['meteorGrey_big1a-vector.png','meteorBrown_big2a-vector.png',
               'meteorBrown_med1a-vector.png','meteorBrown_med3a-vector.png',
               'meteorBrown_small1a-vector.png','meteorGrey_med1a-vector.png',
               'meteorGrey_med2a-vector.png','meteorGrey_small1a-vector.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['boss'] = []
explosion_anim['player'] = [] 
for i in range(9): 
    filename = 'regularExplosionV0{}.png'.format(i)
    img_lg = pygame.image.load(path.join(img_dir,filename)).convert()
    img_lg.set_colorkey(BLACK)
    explosion_anim['lg'].append(img_lg)
    filename = 'tinyExplosionV0{}.png'.format(i) 
    img_sm = pygame.image.load(path.join(img_dir,filename)).convert()
    img_sm.set_colorkey(BLACK)
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosionV0{}.png'.format(i) 
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
    filename = 'bossExplosionV0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['boss'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(
                           path.join(img_dir,'shield_goldV.png')
                           ).convert() 
powerup_images['gun'] = pygame.image.load(
                        path.join(img_dir,'bolt_goldV.png')
                        ).convert() 
powerup_images['bomb'] = pygame.image.load(
                         path.join(img_dir,'bomb.png')
                         ).convert() 

bomb_mini_img = pygame.image.load(
                path.join(img_dir,'bomb_mini.png')
                ).convert()
bomb_mini_img.set_colorkey(BLACK) 

shield_mini_img = pygame.image.load(
                  path.join(img_dir,'shield_mini.png')
                  ).convert() 
shield_mini_img.set_colorkey(BLACK) 

shout_img = pygame.image.load(
            path.join(img_dir,'overdriveV.png')
            ).convert()
shout_img.set_colorkey(BLACK)

alert_img = pygame.image.load(
            path.join(img_dir,'alertV.png')
            ).convert()
alert_img.set_colorkey(BLACK)

intro_img = pygame.image.load(
            path.join(img_dir,'intro_alert.png')
            ).convert()
intro_img.set_colorkey(BLACK)

alert_odl_img = pygame.image.load(
                path.join(img_dir,'overdrive-lock-V.png')
                ).convert()
alert_odl_img.set_colorkey(BLACK)

boss_img = pygame.image.load(
           path.join(img_dir,'boss.png')
           ).convert()
boss_img.set_colorkey(BLACK)

boss2_img = pygame.image.load(
            path.join(img_dir,'boss2.png')
            ).convert()
boss2_img.set_colorkey(BLACK)

boss3_img = pygame.image.load(
            path.join(img_dir,'boss3.png')
            ).convert()
boss3_img.set_colorkey(BLACK)

boss4_img = pygame.image.load(
            path.join(img_dir,'boss4.png')
            ).convert()
boss4_img.set_colorkey(BLACK)

boss5_img = pygame.image.load(
            path.join(img_dir,'boss5.png')
            ).convert() 
boss5_img.set_colorkey(BLACK) 

boss6_img = pygame.image.load(
            path.join(img_dir,'boss6.png')
            ).convert() 
boss6_img.set_colorkey(BLACK) 

boss_bullet_img = pygame.image.load(
                  path.join(img_dir,'boss_bullet.png')
                  ).convert()
boss_bullet_img.set_colorkey(BLACK)

boss_alert_img = pygame.image.load(
                 path.join(img_dir,'boss_destroyed.png')
                 ).convert()
boss_alert_img.set_colorkey(BLACK)

player_shield_img = pygame.image.load(
                    path.join(img_dir,'player_shield.png')
                    ).convert()
player_shield_img.set_colorkey(BLACK)
player_shield_img_rect = player_shield_img.get_rect()

# sound & music 

shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'laz.wav'))
shoot_sound.set_volume(0.14) 

shield_sound = pygame.mixer.Sound(path.join(snd_dir,'pow4.wav')) 

power_sound = pygame.mixer.Sound(path.join(snd_dir,'pow5.wav')) 

expl_sound = pygame.mixer.Sound(path.join(snd_dir,'rumble.wav')) 
expl_sound.set_volume(0.5)

player_die_sound = pygame.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
player_die_sound.set_volume(.5)

pygame.mixer.music.load(path.join(snd_dir,'JuhaniJunkalaLevel1.ogg')) 
songs = ['JuhaniJunkalaLevel1.ogg', 'battleThemeA.ogg', 
         'tgfcoder-FrozenJam-SeamlessLoop.ogg'] 
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1) 

# *****************
# ***           ***
# ***           ***
# ***           ***
# *** GAME LOOP ***
# ***           ***
# ***           ***
# ***           *** 
# *****************

game_over = True 
running = True 

while running:

    # ********** GAME OVER STATE / TITLE SCREEN / GAME START ********** 
    if game_over:

        # game over state 
        show_go_screen() 

        # after exiting game over screen, set up game 
        game_over = False
        all_sprites = pygame.sprite.Group() 
        mobs = pygame.sprite.Group() 
        mobs2 = pygame.sprite.Group() 
        mobs4 = pygame.sprite.Group() 
        boss_group = pygame.sprite.Group() 
        bullets = pygame.sprite.Group() 
        enemy_bullets = pygame.sprite.Group() 
        powerups = pygame.sprite.Group() 
        player = Player()
        all_sprites.add(player)
        shout_count = 0
        level = 1
        macro_level = 1
        drop_probability = 0.955 
        mob_count = 0 
        for i in range(5): 
            newmob()
        mob_count = 1 
        last_score_3[0] = last_score_2[0]
        last_score_3[1] = last_score_2[1]
        last_score_3[2] = last_score_2[2]
        last_score_2[0] = last_score_1[0]
        last_score_2[1] = last_score_1[1]
        last_score_2[2] = last_score_1[2]
        score = 0 
        intro_alert = 0
        alert_1 = 0
        alert_2 = 0
        alert_3 = 0
        alert_4 = 0
        alert_5 = 0
        alert_6 = 0 
        boss_alert = 0 
        scrolly = 0 
        scrolly2 = 0 
        boss_flag = 0
        boss_level = 70 
        max_boss_health = 3000 
        last_boss_health = max_boss_health
        boss_shoot_rate = 0.85 
        od_chain = 0 
        od_chain_announce = 0 
        flash_timer = 0 
        bombing = False 
 
    # *********************************************
    # **                                         **
    # **  GAME LOOP:  1. PROCESS INPUT (EVENTS)  **
    # **                                         **
    # *********************************************

    clock.tick(FPS) 

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: 
                pygame.event.clear()
                pause()
 
    # *********************************************
    # **                                         **
    # **       GAME LOOP:  2. UPDATE GAME        **
    # **                                         **
    # *********************************************

    all_sprites.update() 
    
    # ********** GAME LEVELS ********** 

    # game start message 
    if intro_alert == 0:
        intro_alert = Shout('intro',WIDTH/2,-10,4)
        all_sprites.add(intro_alert)
        intro_alert = 1

    # advance game level as meteors are destroyed 
    if mob_count % 19 == 0: 
        level += 1
        if level < 40:
            newmob()
        else:
            if level % 10 == 0: 
                newmob() 
        if level == 2:
            drop_probability = 0.965 
        elif level == 3:
            drop_probability = 0.9675 
        else:
            drop_probability += 0.00125 
            if drop_probability >= 0.9825:
                drop_probability = 0.9825

    # spaceships 
    if level >= 3:
        if alert_1 == 0:
            ships_alert = Shout('alert',WIDTH/2,-10,11)
            all_sprites.add(ships_alert)
            alert_1 = 1
        if level >= 10:
            if alert_2 == 0:
                ships_alert = Shout('alert',WIDTH/2,-10,11)
                all_sprites.add(ships_alert)
                alert_2 = 1
            if level >= 20:
                if alert_3 == 0:
                    ships_alert = Shout('alert',WIDTH/2,-10,11)
                    all_sprites.add(ships_alert)
                    alert_3 = 1
                if level < boss_level:
                    if random.random() > 0.975: 
                        mob2 = Mob2(3)
                        all_sprites.add(mob2)
                        mobs2.add(mob2)
                else:
                    if random.random() > 0.99: 
                        mob2 = Mob2(3)
                        all_sprites.add(mob2)
                        mobs2.add(mob2)
            elif random.random() > 0.985: 
                mob2 = Mob2(2)
                all_sprites.add(mob2)
                mobs2.add(mob2)
        elif random.random() > 0.995: 
            mob2 = Mob2(1)
            all_sprites.add(mob2)
            mobs2.add(mob2)

    # storm bolts 
    if level >= 30: 
        if alert_4 == 0:
            ships_alert = Shout('alert',WIDTH/2,-10,11)
            all_sprites.add(ships_alert)
            alert_4 = 1
        if random.random() > .97: 
            mob3 = Mob3()
            all_sprites.add(mob3)
            enemy_bullets.add(mob3)

    # fireballs 
    if level >= 45: 
        if alert_5 == 0:
            ships_alert = Shout('alert',WIDTH/2,-10,11)
            all_sprites.add(ships_alert)
            alert_5 = 1
        if level >= boss_level: 
            if random.random() > 0.9875: 
                mob4 = Mob4()
                all_sprites.add(mob4)
                mobs4.add(mob4)
        else:
            if random.random() > (0.99 - ((level - 45) * 0.00025)): 
                mob4 = Mob4()
                all_sprites.add(mob4)
                mobs4.add(mob4)

    # boss fight 
    if level >= boss_level: 
        player.power = 7 
        if alert_6 == 0:
            ships_alert = Shout('alert_odl',WIDTH/2,-10,7)
            all_sprites.add(ships_alert)
            alert_6 = 1
        if boss_flag == 0:
            boss_flag = 1
            boss_alert = 0 
            boss = Boss()
            all_sprites.add(boss)
            boss_group.add(boss)
        if random.random() > .9875:
            newmob() 

    # ********** COLLISION CHECKS ********** 

    # meteor / player bullet collision 
    hits = pygame.sprite.groupcollide(
           mobs,bullets,True,True,pygame.sprite.collide_circle)
    for hit in hits: 
        expl_sound.play()
        score += ((60 - hit.radius)*10) 
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() > drop_probability: 
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        if level >= boss_level:
            if random.random() > 0.9: 
                newmob() 
        else:
            newmob()

    # enemy ship / player bullet collision 
    hits = pygame.sprite.groupcollide(
           mobs2,bullets,True,True,pygame.sprite.collide_circle)
    for hit in hits: 
        expl_sound.play()
        score += ((60 - hit.radius)*10)
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        if random.random() > drop_probability:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    # fireball / player bullet collision 
    hits = pygame.sprite.groupcollide(
           mobs4,bullets,False,True,pygame.sprite.collide_circle)
    for hit in hits: 
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)

    # boss / player bullet collision 
    hits = pygame.sprite.groupcollide(
           boss_group,bullets,False,True,pygame.sprite.collide_circle)
    for hit in hits: 
        expl_sound.play() 
        boss.health -= 10
        expl = Explosion(hit.rect.center,'boss')
        all_sprites.add(expl)
        check_boss_die()

    # player / meteor collision 
    hits = pygame.sprite.spritecollide(
           player,mobs,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play() 
        if not player.indestruct:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        newmob()
        check_player_die() 

    # player / enemy ship collision 
    hits = pygame.sprite.spritecollide(
           player,mobs2,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play() 
        if not player.indestruct:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        check_player_die() 

    # player / enemy bullet collision 
    hits = pygame.sprite.spritecollide(
           player,enemy_bullets,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play() 
        if not player.indestruct:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        check_player_die() 

    # player / fireball collision 
    hits = pygame.sprite.spritecollide(
           player,mobs4,True,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play() 
        if not player.indestruct:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(expl)
        check_player_die() 

    # player / boss collision 
    hits = pygame.sprite.spritecollide(
           player,boss_group,False,pygame.sprite.collide_circle)
    for hit in hits:
        expl_sound.play() 
        if not player.indestruct:
            player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center,'boss')
        all_sprites.add(expl)
        check_player_die() 

    # player / powerup collision 
    hits = pygame.sprite.spritecollide(player,powerups,True)
    for hit in hits:
        if hit.type == 'shield':
            shield_sound.play()
            if player.shield >= 100: 
                if player.indestruct_shield_count < 3: 
                    player.indestruct_shield_count += 1
                    if player.indestruct_shield_count > 3:
                        player.indestruct_shield_count = 3 
                else:
                    score += max(50000,(5000 * level)) 
            else:
                player.shield += random.randrange(34,50) 
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            if player.prev_power == 7: 
                od_chain += 1
                od_chain_announce = 1
                score += (od_chain * 50000) 
            if level < boss_level: 
                if player.power >= 6:
                    power_sound.play() 
                else:
                    power_sound.play()
                player.powerup() 
            else: 
                if player.shield == 100: 
                    score += max(50000,(5000 * level))
                player.shield += random.randrange(34,50) 
                if player.shield >= 100:
                    player.shield = 100
        if hit.type == 'bomb':
            shield_sound.play() 
            if player.bombs < 3: 
                player.bombs += 1
            else: 
                if player.shield == 100: 
                    score += max(50000,(5000 * level))
                player.shield += random.randrange(34,50) 
                if player.shield >= 100:
                    player.shield = 100

    # ********** GAME OVER CHECK **********  

    if player.lives == 0 and not death_explosion.alive(): 
        last_score_1[0] = score 
        last_score_1[1] = level 
        last_score_1[2] = macro_level
        game_over_card_rect.midtop = (WIDTH/2,HEIGHT/4) 
        screen.blit(game_over_card,game_over_card_rect) 
        draw_text(screen,'meteor::RUSH   by   Jason R. Carroll',
                  26,WIDTH*8/16,HEIGHT*28/64)
        draw_text(screen,'Graphics, Sound, Programming:  J. Carroll',
                  20,WIDTH*8/16,HEIGHT*32/64)
        draw_text(screen,'Music:  Alex Smith, Jordan Trudgett, '
                  'Juhani Junkala',20,WIDTH*8/16,HEIGHT*36/64)
        draw_text(screen,'\"Have a nice day!\"',20,WIDTH*8/16,HEIGHT*13/16)
        pygame.display.flip()
        time.sleep(6)
        pygame.event.clear() 
        game_over = True

    # *********************************************
    # **                                         **
    # **   GAME LOOP:  3. DRAW / RENDER SCREEN   **
    # **                                         **
    # *********************************************

    # draw black screen and player movement area 
    screen.fill(BLACK)
    pygame.draw.rect(screen,GRAY5,(0,HEIGHT-200,WIDTH,200)) 
    pygame.draw.line(screen,GRAY4,(0,HEIGHT-200),(WIDTH,HEIGHT-200),1) 

    # bomb flash 
    if bombing:
        screen.fill(BLUE) 
        flash_timer += 1
    else: 
        screen.fill(BLACK) 
        pygame.draw.rect(screen,GRAY5,(0,HEIGHT-200,WIDTH,200)) 
        pygame.draw.line(screen,GRAY4,(0,HEIGHT-200),(WIDTH,HEIGHT-200),1) 
    if flash_timer > 2: 
            bombing = False 
            flash_timer = 0 

    # draw and scroll deep background stars 
    rel_y = scrolly % background.get_rect().height 
    screen.blit(background,(0,rel_y - background.get_rect().height)) 
    if rel_y < HEIGHT: 
        screen.blit(background,(0,rel_y)) 
    scrolly += 0.75 

    # draw and scroll nearer background stars (parallax) 
    rel_y2 = scrolly2 % foreground.get_rect().height 
    screen.blit(foreground,(0,rel_y2 - foreground.get_rect().height)) 
    if rel_y2 < HEIGHT: 
        screen.blit(foreground,(0,rel_y2)) 
    scrolly2 += 1.0 

    # draw all sprites 
    all_sprites.draw(screen) 

    # draw score and other screen text 
    draw_text(screen,str(score),24,WIDTH/2,10)
    draw_text(screen,'[Hits: '+str(mob_count)+']',16,WIDTH*5/16,10) 
    draw_text(screen,'Level '+str(level)+' :: '+'Boss '+str(macro_level),
              18,WIDTH/2,35)
    draw_text(screen,'[Power: '+str(player.power)+']',16,WIDTH*11/16,10) 
    draw_text(screen,'Meteor Density: '+str(len(mobs)),18,WIDTH/2,55)

    # set player shield bar color 
    if player.shield <= 50:
        if player.shield <= 25:
            player_shield_bar_color = RED
        else:
            player_shield_bar_color = YELLOW
    elif player.shield == 100:
        player_shield_bar_color = ALMOST_WHITE
    else:
        player_shield_bar_color = GREEN

    # draw player shield bar at top of screen 
    draw_shield_bar(screen,5,10,90,8,2,player_shield_bar_color,player.shield)

    # draw player-centered shield bar 
    draw_shield_bar(screen,player.rect.x+5,player.rect.y+72,50,4,-1,
                    player_shield_bar_color,player.shield)

    # draw indestructible shield icons 
    draw_lives(screen,8,35,player.indestruct_shield_count,shield_mini_img) 

    # draw shield timer upon player use 
    if player.indestruct:
        draw_text(screen,str(INDESTRUCT_DURATION - (pygame.time.get_ticks() 
                  - player.indestruct_time)),28,WIDTH/2,HEIGHT-190,PINK)
        draw_text(screen,'S H I E L D',16,WIDTH/2,HEIGHT-170,PINK) 
        player_shield_img_rect = player.rect
        screen.blit(player_shield_img,player_shield_img_rect)

    # check for overdrive bonus chain 
    if player.power == 7 and level < boss_level:
        od_remain = (POWERUP_TIME - (pygame.time.get_ticks() 
                     - player.power_time))
        draw_od_bar(screen,0,30,5,HEIGHT-30,-1,PINK,
                    od_remain/POWERUP_TIME*100)
        draw_od_bar(screen,WIDTH-5,30,5,HEIGHT-30,-1,PINK,
                    od_remain/POWERUP_TIME*100)
        if od_chain_announce == 1:
            draw_text(screen,'O v e r D r i v e    C H A I N    :    '
                      '5 0 , 0 0 0    X    '+str(od_chain),20,WIDTH/2,
                      HEIGHT-220,PINK)
    if player.power < 7:
        od_chain_announce = 0
        od_chain = 0
        player.prev_power = 6

    # draw boss health bar when boss is present 
    if boss_flag == 1:
        draw_shield_bar(screen,0,HEIGHT-7,WIDTH,7,-1,RED,
                        boss.health/max_boss_health*100)

    # draw player lives icons 
    draw_lives(screen,WIDTH-100,5,player.lives,player_mini_img)

    # draw bomb icons 
    draw_lives(screen,WIDTH-100,35,player.bombs,bomb_mini_img)

    # render screen 
    pygame.display.flip() 

# quit after game loop ends 
pygame.quit()
sys.exit()

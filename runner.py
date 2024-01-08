import pygame as pg;from sys import exit;from math import floor as round;from random import choice,randint

Sprites = []
badSprites = []
    
class AnimatedSprites:
    surf = None
    rect = None
    frames = None
    evil = False
    pos = None
    speed = (0,0)
    frame = 0
    delay = 1

    def __init__(self,frames,pos,moving,isBad):
        self.frnum = 0
        self.frames = frames
        self.frame = 0
        self.surf = frames[self.frnum]
        self.rect = self.surf.get_rect()
        self.pos = pos
        self.speed = moving
        self.delay = 0.125
        self.evil = isBad
        if isBad == True:badSprites.append(self)
        elif isBad == False:Sprites.append(self)

    def place(self,place):
        if place == "center":self.rect = self.surf.get_rect(center = self.pos)
        elif place == "bottomleft":self.rect = self.surf.get_rect(bottomleft = self.pos)
        elif place == "topleft":self.rect = self.surf.get_rect(topleft = self.pos)
        return self.rect
    
    def move(self,place):
        self.pos[0] += self.speed[0]
        self.pos[1] += self.speed[1]
        if place == "center":self.rect = self.surf.get_rect(center = self.pos)
        elif place == "bottomleft":self.rect = self.surf.get_rect(bottomleft = self.pos)
        elif place == "topleft":self.rect = self.surf.get_rect(topleft = self.pos)
        elif place == "midbottom":self.rect = self.surf.get_rect(midbottom = self.pos)
        if self.pos[0] < -self.rect.width or self.pos[1] < 0:self.destroy()
        return self.rect
    
    def playAnim(self):
        if self.frame/60 >= self.delay:
            self.surf = self.frames[self.frnum]
            self.frnum = 1 + self.frnum if len(self.frames) > self.frnum + 1 else 0
            self.frame = 0

    def stopAnim(self):self.surf = self.frames[0]

    def destroy(self):
        global badSprites
        global Sprites
        if self.evil == True:badSprites = [x for x in badSprites if x != self];del self
        elif self.evil == False:Sprites = [x for x in Sprites if x != self];del self

def buildGround(scr,xPos,yPos):
    for h in range(3):
        x = xPos
        y = h*64 + yPos
        if h == 0:
            for _ in range(12):
                scr.blit(grassSurf,(x,y));x += 64
        else:
            y+= 6
            for _ in range(12):
                scr.blit(dirtSurf,(x,y));x += 64

def getDecor():return choice(decors)

on = True
if on:
    pg.init()
    pg.display.set_caption("Runner")
    screen = pg.display.set_mode((768,386))
    clock = pg.time.Clock()
font = pg.font.Font('assets/Minecraft.ttf',50)
font_surf = font.render("Press any key to start",False,"Black")

frames1 = 0
playing = False

plr = AnimatedSprites([pg.image.load('assets/cat/Cat Sprite1.png'),pg.image.load('assets/cat/Cat Sprite2.png'),pg.image.load('assets/cat/Cat Sprite3.png'),pg.image.load('assets/cat/Cat Sprite2.png')],[150,250],(0,0),False)
enemy = AnimatedSprites([pg.image.load('assets/cat/uncat1.png'),pg.image.load('assets/cat/uncat2.png'),pg.image.load('assets/cat/uncat3.png'),pg.image.load('assets/cat/uncat2.png')],[0,plr.pos[1]],(0,0),False)

isJumping = False
floor = int(plr.pos[1])
gravSpeed = .75
gravity = 0

xGround = 0
xGround2 = 768

#game stuff
gameSpeed = 6
scores_val = 0
hp = 0
interval = pg.USEREVENT + 1
invincible_interval = pg.USEREVENT + 2
invincible,shown = False,False
spawnDecor = pg.USEREVENT + 3
timer = 4000
stagelv = 500
showPlr = True
hp = 3
pg.time.set_timer(interval,timer)
pg.time.set_timer(spawnDecor,2000)
#assets
rockSurf = pg.image.load('assets/rock.png')
dirtSurf = pg.image.load('assets/dirt1.png')
grassSurf = pg.image.load('assets/grass.png')
healthSurf,unhealthSurf = pg.image.load('assets/health.png'),pg.image.load('assets/unhealth.png')
fightScene = AnimatedSprites([pg.image.load('assets/fcloud1.png'),pg.image.load('assets/fcloud2.png'),pg.image.load('assets/fcloud3.png')],[-64,0],(0,0),False);fightScene.delay = 0.25
decors = [AnimatedSprites([pg.image.load('assets/clouds/cloud.png')],[768,50],(-gameSpeed,0),None),
          AnimatedSprites([pg.image.load('assets/clouds/cloud2 .png')],[768,100],(-gameSpeed,0),None),
          AnimatedSprites([pg.image.load('assets/clouds/cloud3 .png')],[768,150],(-gameSpeed,0),None)]

while on:
    for event in pg.event.get():
        if event.type == pg.QUIT:pg.quit();exit()
        if event.type == pg.KEYDOWN:
            if not playing:
                badSprites = []
                playing = True
                showPlr = True
                gameSpeed = 8
                timer = 4000
                hp = 3
                fightScene.pos[1] = -64
            if pg.key.get_pressed()[pg.K_SPACE]:isJumping = True
        if event.type == pg.KEYUP:
            if not pg.key.get_pressed()[pg.K_SPACE]:isJumping = False
        if event.type == interval and playing:
            AnimatedSprites([rockSurf],[800,250],(-gameSpeed,0),True)
            pg.time.set_timer(interval,timer)
        if event.type == invincible_interval:invincible = False;pg.time.set_timer(invincible_interval,0)
        if event.type == spawnDecor:
            decor = getDecor()
            newDecor = AnimatedSprites(decor.frames,decor.pos,decor.speed,False)
            pg.time.set_timer(spawnDecor,randint(500,2000))

    #enemy mover
    if enemy.pos[0] != 150 - hp*50:
        if enemy.pos[0] < 150 - hp*50:enemy.speed = (5,0)
        elif enemy.pos[0] > 150 - hp*50:enemy.speed = (-5,0)
    else:enemy.speed = (0,0)

    #losing
    if enemy.pos[0] == plr.pos[0] and playing:
        playing = False
        showPlr = False
        gameSpeed = 0
        timer = 0
        enemy.pos = [0,plr.pos[1]]
        scores_val = 0
    
    #Jumping
    gravity = -20 if isJumping and plr.pos[1] == floor and playing else gravity
    if gravity != 0:
        plr.pos[1] += gravity
        gravity += gravSpeed
    if plr.pos[1] < floor:gravity += gravSpeed
    else:plr.pos[1] = floor;gravity = 0

    #Screen Elements
    screen.fill((59, 237, 199))
    buildGround(screen,xGround,245)
    buildGround(screen,xGround2,245)

    #Sprites Animation
    if playing:
        for sprite1 in Sprites:
            sprite1.frame += 1;sprite1.playAnim();sprite1.move("bottomleft")
            if sprite1 != enemy and sprite1 != plr:screen.blit(sprite1.surf,sprite1.pos)

    if showPlr and invincible and playing:
        if not shown:
            shown = True
            screen.blit(plr.surf,plr.place("bottomleft"))
        else:shown = False
    else:
        if showPlr:screen.blit(plr.surf,plr.place("bottomleft"))
    if showPlr:enemy.move("bottomleft");screen.blit(enemy.surf,enemy.place("bottomleft"))

    scoreText = font.render(str(round(scores_val)),False,"Black")

    if not showPlr:fightScene.frame+=1;fightScene.playAnim();screen.blit(fightScene.surf,(plr.pos[0],floor-64))

    if not showPlr:screen.blit(fightScene.surf,fightScene.place("bottomleft"))

    #Gameplay
    if playing:
        scores_val+= 0.145

        xGround = xGround - gameSpeed if xGround - gameSpeed > -768 else 768 - gameSpeed
        xGround2 = xGround2 - gameSpeed if xGround2 - gameSpeed > -768 else 768 - gameSpeed
        
        screen.blit(scoreText,scoreText.get_rect(center = (384,50)))

        for p in range(3):
            if hp >= p+1:screen.blit(healthSurf,(p*66,0))
            else:screen.blit(unhealthSurf,(p*66,0))
    
    #Obstacle manager
    for bSprites in badSprites:
        if playing:
            bSprites.move("bottomleft")
            if bSprites.rect.colliderect(plr.rect) and not invincible:
                hp -= 1
                invincible = True
                pg.time.set_timer(invincible_interval,1000)
        screen.blit(bSprites.surf,bSprites.rect)

    if not playing:screen.blit(font_surf,font_surf.get_rect(center = (400,100)));xGround,xGround2 = 0,768

    pg.display.update()
    clock.tick(60)
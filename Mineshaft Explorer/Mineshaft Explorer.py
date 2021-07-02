from livewires import games, color
from generate4 import *
import pygame,math

screen_width = 620
screen_height = 620
tilesize = 20


games.init(screen_width = screen_width,screen_height = screen_height, fps=50)

shaft123 = games.load_image("hidden\\shaft.png", transparent=False)
tiles = [games.load_image("hidden\\plank1.png",transparent=False),
         games.load_image("hidden\\plank2.png",transparent=False),
         games.load_image("hidden\\plank3.png",transparent=False),
         games.load_image("hidden\\plank4.png",transparent=False),
         games.load_image("hidden\\plank5.png",transparent=False)]
tiles = [pygame.transform.rotate(tiles[2],180), #l end              1
         tiles[2], #r end                                           2
         tiles[0], #horizontal                                      3
         pygame.transform.rotate(tiles[2],90), #t end               4
         tiles[1], #tl corner                                       5
         pygame.transform.rotate(tiles[1],270), #tr corner          6
         pygame.transform.rotate(tiles[3],270), #3t                 7
         pygame.transform.rotate(tiles[2],270), #b end              8
         pygame.transform.rotate(tiles[1],90), #bl corner           9
         pygame.transform.rotate(tiles[1],180), #br corner          10
         pygame.transform.rotate(tiles[3],90), #3b                  11
         pygame.transform.rotate(tiles[0],90), #vertical            12
         tiles[3], #3l                                              13
         pygame.transform.rotate(tiles[3],180), #3r                 14
         tiles[4], #4 way                                           15
         games.load_image("hidden\\elevator.png",transparent=False)] #elevator 16

         
class Start(games.Sprite):
    def __init__(self,x,y,score):
        super(Start, self).__init__(x=-283746,
                                    y=-239847,
                                    image=tiles[7])
        self.px = x
        self.py = y
        if score >= 0:
            sctext = "Total Score: "+str(score)
        else:
            sctext = "Welcome to Mineshaft Explorer"
        games.screen.background = pygame.Surface((screen_width,screen_height))
        self.presstxt = games.Text(value="Press Enter to Start",x=screen_width/2,y=screen_height/2+20,size=40,color=color.red)
        games.screen.add(self.presstxt)
        self.score = games.Text(value=sctext,x=screen_width/2,y=screen_height/2-20,size=40,color=color.red)
        games.screen.add(self.score)
        
    def update(self):
        if games.keyboard.is_pressed(games.K_RETURN):
            self.presstxt.destroy()
            self.score.destroy()
            games.screen.add(Player(self.px,self.py))
            self.destroy()
            return False
class Player(games.Sprite):
    def __init__(self,x,y):
        self.start()
        super(Player, self).__init__(left=x*tilesize,
                                     top=y*tilesize,
                                     image=games.load_image("hidden\\player.png")
        )
        self.elevc = [[0,0],[0,0],[0,0]]
        level,self.elevc[0] = generate(screen_width//tilesize,screen_height//tilesize,1,x,y)
        self.spritelist = []
        self.xc = x
        self.yc = y
        self.default = self.image
        self.movingdir = None
        self.moveleft = 0
        self.full = [(x,y) for x in range(screen_width//tilesize) for y in range(screen_height//tilesize)]
        level2,self.elevc[1] = generate(screen_width//tilesize,screen_height//tilesize,2,self.elevc[0][1],self.elevc[0][0])
        level3,self.elevc[2] = generate(screen_width//tilesize,screen_height//tilesize,3,self.elevc[1][1],self.elevc[1][0])
        back = pygame.Surface((screen_width, screen_height))
        self.val=4
        shaft = pygame.transform.scale(games.load_image("hidden\\shaft.png", transparent=False), (screen_width, screen_height))
        a=255*.6
        shaft.fill((a,a,a), special_flags=pygame.BLEND_RGB_MULT)
        back.blit(shaft, (0,0))
        self.nomove = list(filter(lambda x: level[x[1]][x[0]]==0,self.full))
        self.levels = [level, level2, level3]
        self.levelsp = [1,.6,.6**2]
        self.levelshow(level3, .6**2, back)
        self.levelshow(level2, .6, back)
        self.levelshow(level, 1, back)
        games.screen.set_background(back)
        self.advancing=0
        self.currlevel = games.Text(value="Level: "+str(self.val-3),left=5,top=5,color=color.red,size=25,is_collideable=False)
        games.screen.add(self.currlevel)
        self.score=0
        self.coinlist = []
        self.tscore = games.Text(value="Score: "+str(self.score),left=5,top=30,color=color.red,size=25,is_collideable=False)
        games.screen.add(self.tscore)
        self.spritelist.append(self.tscore)
        self.spritelist.append(self.currlevel)
        self.make_coins()
        self.make_enemies()
        self.cooldown = 50


    def levelshow(self, lvl, perc, scr):
        size = tilesize*perc
        startx = screen_width*(1-perc)/2
        starty = screen_height*(1-perc)/2
        a = 255*perc
        tmptiles = []
        for i in tiles:
            tile = pygame.transform.scale(i, (math.ceil(size), math.ceil(size)))
            tile.fill((a,a,a), special_flags=pygame.BLEND_RGB_MULT)
            tmptiles.append(tile)
        for j in range(len(lvl)):
            for i in range(len(lvl[j])):
                num = lvl[j][i]-1
                if num >= 0: scr.blit(tmptiles[lvl[j][i]-1],(int(startx+size*i),int(starty+size*j)))

    def make_coins(self):
        image = games.load_image("hidden\\coin.png")
        back = games.screen.background
        for row in range(len(self.levels[0])):
            for col in range(len(self.levels[0][row])):
                if self.levels[0][row][col] not in [0, 16] and (col,row) != (self.xc,self.yc):
                    if random.randint(1, round(1+2000/(self.val+7))) == 1:
                            self.coinlist.append([col,row])
                            back.blit(image,(col*tilesize,row*tilesize))
        games.screen.set_background(back)

    def make_enemies(self):
        for row in range(len(self.levels[0])):
            for col in range(len(self.levels[0][row])):
                if self.levels[0][row][col] not in [0, 16] and (col,row) != (self.xc,self.yc):
                    if random.randint(1, round(1+10000/(self.val+7))) == 1:
                        enemy = Enemy(col,row,self.levels[0],self)
                        self.spritelist.append(enemy)
                        games.screen.add(enemy)


    def checktile(self):
        if (self.xc,self.yc) in self.nomove or self.xc<0 or self.xc>=screen_width//tilesize or self.yc<0 or self.yc>=screen_height//tilesize:
            return False
        return True

    def add_score(self, value):
        self.score+=value
        self.tscore.value = "Score: "+str(self.score)
        self.tscore.left = 5

    def advance(self):
        for i in self.spritelist:
            if type(i) in [Bullet, Enemy]:
                self.spritelist.remove(i)
                i.destroy()
        self.advancing-=1
        mult = (1/.6)**(1/80)
        amult = 1/mult
        back = pygame.Surface((screen_width, screen_height))
        if self.advancing == 0:
            sizex=screen_width
            sizey=screen_height
            startx=0
            starty=0
            a=255*.6
        else:
            a = 255*.6*(mult**(80-self.advancing))
            sizex = screen_width*(mult**(80-self.advancing))
            sizey = screen_height*(mult**(80-self.advancing))
            startx = (screen_width-sizex)/2
            starty = (screen_height-sizey)/2
        #sizex=400*(1/.6)
        #sizey=sizex
        #shaft = games.load_image("hidden\\shaft.png", transparent=False)
        shaft = pygame.transform.scale(shaft123, (math.floor(sizex), math.floor(sizey)))
        shaft.fill((a,a,a), special_flags=pygame.BLEND_RGB_MULT)
        back.blit(shaft,(int(startx),int(starty)))
        if self.advancing == 79:
                self.levelsp.pop(0)                
                self.levels.pop(0)
                self.elevc.pop(0)
                self.add_score(100*(self.val-3))
        if self.advancing == 0:
            self.levelsp = [1*amult,.6*amult,.6**2*amult]
            l,elev = generate(screen_width//tilesize,screen_height//tilesize,self.val,self.elevc[-1][1],self.elevc[-1][0])
            self.val+=1
            self.currlevel.value = "Level: "+str(self.val-3)
            self.currlevel.left = 5
            self.levels.append(l)
            self.elevc.append(elev)
        for n,i in enumerate(self.levels[::-1]):
            self.levelsp[-n-1] *= mult
            self.levelshow(i, self.levelsp[-n-1], back)
        games.screen.set_background(back)
        self.nomove = list(filter(lambda x: self.levels[0][x[1]][x[0]]==0,self.full))
        if self.advancing == 0:
            self.make_coins()
            self.make_enemies()

    def update(self):
        for sprite in self.overlapping_sprites:
            if type(sprite) == Enemy:
                self.lose()
                return False
        self.currlevel.elevate()
        self.tscore.elevate()
        oldc = [self.xc,self.yc]
        if self.moveleft:
                if self.movingdir=="up":
                    self.y-=2
                    self.moveleft-=2
                elif self.movingdir=="right":
                    self.x+=2
                    self.moveleft-=2
                elif self.movingdir=="down":
                    self.y+=2
                    self.moveleft-=2
                elif self.movingdir=="left":
                    self.x-=2
                    self.moveleft-=2
                if self.moveleft <= 0:
                    self.moveleft = False
        elif self.advancing:
            self.image = tiles[15]
            self.advance()
        elif oldc in self.coinlist:
            self.coinlist.remove(oldc)
            self.add_score(50)
            image = tiles[self.levels[0][oldc[1]][oldc[0]]-1]
            back = games.screen.background
            back.blit(image,(oldc[0]*tilesize,oldc[1]*tilesize))
            games.screen.set_background(back)
        else:
            if oldc == self.elevc[0][::-1] and games.keyboard.is_pressed(games.K_SPACE):
                self.advancing=80
            self.image=self.default
            self.levelsp = [1,.6,.6**2]
            if games.keyboard.is_pressed(games.K_w) and not self.moveleft:
                self.movingdir = "up"
                self.moveleft = tilesize
                self.yc-=1
                if not self.checktile():
                    self.moveleft = 0
                    self.xc,self.yc=oldc
            if games.keyboard.is_pressed(games.K_d) and not self.moveleft:
                self.movingdir = "right"
                self.moveleft = tilesize
                self.xc+=1
                if not self.checktile():
                    self.moveleft = 0
                    self.xc,self.yc=oldc
            if games.keyboard.is_pressed(games.K_s) and not self.moveleft:
                self.movingdir = "down"
                self.moveleft = tilesize
                self.yc+=1
                if not self.checktile():
                    self.moveleft = 0
                    self.xc,self.yc=oldc
            if games.keyboard.is_pressed(games.K_a) and not self.moveleft:
                self.movingdir = "left"
                self.moveleft = tilesize
                self.xc-=1
                if not self.checktile():
                    self.moveleft = 0
                    self.xc,self.yc=oldc
            if self.cooldown <= 0:
                if games.keyboard.is_pressed(games.K_LEFT):
                    bullet = Bullet(self.xc,self.yc,"left",self)
                    self.spritelist.append(bullet)
                    games.screen.add(bullet)
                    self.cooldown=50
                elif games.keyboard.is_pressed(games.K_UP):
                    bullet = Bullet(self.xc,self.yc,"up",self)
                    self.spritelist.append(bullet)
                    games.screen.add(bullet)
                    self.cooldown=50
                elif games.keyboard.is_pressed(games.K_RIGHT):
                    bullet = Bullet(self.xc,self.yc,"right",self)
                    self.spritelist.append(bullet)
                    games.screen.add(bullet)
                    self.cooldown=50
                elif games.keyboard.is_pressed(games.K_DOWN):
                    bullet = Bullet(self.xc,self.yc,"down",self)
                    self.spritelist.append(bullet)
                    games.screen.add(bullet)
                    self.cooldown=50
        self.cooldown-=1

    def lose(self):
        for sprite in self.spritelist:
            sprite.destroy()
        games.screen.add(Start(screen_width//tilesize-1,0,self.score))
        self.destroy()

class Bullet(games.Sprite):
    default = games.load_image("hidden\\bullet.png")
    def __init__(self,x,y,movedir,player):
        self.movingdir = movedir
        self.player=player
        self.xc=x
        self.yc=y
        self.moveleft=0
        angles = {"left":0,
                  "down":90,
                  "right":180,
                  "up":270}
        super(Bullet, self).__init__(left=x*tilesize,
                                     top=y*tilesize,
                                     image=pygame.transform.rotate(Bullet.default,angles[movedir]))

    def checktile(self):
        if (self.xc,self.yc) in self.player.nomove or self.xc<0 or self.xc>=screen_width//tilesize or self.yc<0 or self.yc>=screen_height//tilesize:
            return False
        return True

    def update(self):
        if not self.checktile():
            self.player.spritelist.remove(self)
            self.destroy()
            return False
        for i in self.overlapping_sprites:
            if type(i) == Enemy:
                i.hp-=1
                self.player.spritelist.remove(self)
                self.destroy()
                return False
        if self.moveleft:
            if self.movingdir=="up":
                self.y-=4
                self.moveleft-=4
            elif self.movingdir=="right":
                self.x+=4
                self.moveleft-=4
            elif self.movingdir=="down":
                self.y+=4
                self.moveleft-=4
            elif self.movingdir=="left":
                self.x-=4
                self.moveleft-=4
            if self.moveleft <= 0:
                self.moveleft = False
        else:
            if self.movingdir=="up":
                self.yc-=1
            elif self.movingdir == "left":
                self.xc-=1
            elif self.movingdir == "down":
                self.yc+=1
            else:
                self.xc+=1
            self.moveleft=tilesize
            
        

class Enemy(games.Sprite):
    default = games.load_image("hidden\\enemy.png")
    def __init__(self, x, y, level, player):
        super(Enemy, self).__init__(left=x*tilesize,
                                    top=y*tilesize,
                                    image=Enemy.default)
        self.xc = x
        self.yc = y
        self.player = player
        self.level = level
        self.moveleft = 0
        self.movedir = None
        self.hp=3

    def checktile(self):
        if (self.xc,self.yc) in self.player.nomove or self.xc<0 or self.xc>=screen_width//tilesize or self.yc<0 or self.yc>=screen_height//tilesize:
            return False
        return True

    def update(self):
        if self.hp<=0:
            self.player.spritelist.remove(self)
            self.player.add_score(100)
            self.destroy()
            return False
        oldc = [self.xc,self.yc]
        if self.moveleft:
            if self.movingdir=="up":
                self.y-=2
                self.moveleft-=2
            elif self.movingdir=="right":
                self.x+=2
                self.moveleft-=2
                self.image = Enemy.default
            elif self.movingdir=="down":
                self.y+=2
                self.moveleft-=2
            elif self.movingdir=="left":
                self.x-=2
                self.moveleft-=2
                self.image = pygame.transform.flip(Enemy.default,True,False)
        else:
            possible = ["left","right","up","down"]
            if self.player.xc == self.xc:
                try: ttiles = [self.level[n][self.xc] for n in range(self.player.yc,self.yc,int((self.yc-self.player.yc)/abs(self.yc-self.player.yc)))]
                except: ttiles = [0]
                if 0 not in ttiles:
                    if self.yc>self.player.yc:
                        self.movingdir="up"
                        self.yc-=1
                    else:
                        self.movingdir="down"
                        self.yc+=1
                    self.moveleft=tilesize
                    if not self.checktile():
                        self.moveleft = 0
                        self.xc,self.yc=oldc
                else:
                    self.movingdir=random.choice(["left","right","up","down"])
                    if self.movingdir=="left":
                        self.xc-=1
                    elif self.movingdir=="right":
                        self.xc+=1
                    elif self.movingdir=="up":
                        self.yc-=1
                    else:
                        self.yc+=1
                    self.moveleft=tilesize
                    if not self.checktile():
                        self.moveleft = 0
                        self.xc,self.yc=oldc
            elif self.player.yc == self.yc:
                ttiles = [self.level[self.yc][n] for n in range(self.player.xc,self.xc,int((self.xc-self.player.xc)/abs(self.xc-self.player.xc)))]
                if 0 not in ttiles:
                    if self.xc>self.player.xc:
                        self.movingdir="left"
                        self.xc-=1
                    else:
                        self.movingdir="right"
                        self.xc+=1
                    self.moveleft=tilesize
                    if not self.checktile():
                        self.moveleft = 0
                        self.xc,self.yc=oldc
                else:
                    self.movingdir=random.choice(["left","right","up","down"])
                    if self.movingdir=="left":
                        self.xc-=1
                    elif self.movingdir=="right":
                        self.xc+=1
                    elif self.movingdir=="up":
                        self.yc-=1
                    else:
                        self.yc+=1
                    self.moveleft=tilesize
                    if not self.checktile():
                        self.moveleft = 0
                        self.xc,self.yc=oldc
            else:
                self.movingdir=random.choice(["left","right","up","down"])
                if self.movingdir=="left":
                    self.xc-=1
                elif self.movingdir=="right":
                    self.xc+=1
                elif self.movingdir=="up":
                    self.yc-=1
                else:
                    self.yc+=1
                self.moveleft=tilesize
                if not self.checktile():
                    self.moveleft = 0
                    self.xc,self.yc=oldc
def main():
    games.screen.add(Start(screen_width//tilesize-1,0,-3))
    games.screen.mainloop()
    
main()

from livewires import games,color
import pygame, math, os, time

enemy_list = open("hidden\\enemy.txt","r").readlines()
turret_list = open("hidden\\turret.txt","r").readlines()

os.environ['SDL_VIDEO_CENTERED'] = '1'

games.init(screen_width = 800, screen_height = 600, fps = 50)

class Wait(games.Sprite):
    def __init__(self, parent):
        super(Wait, self).__init__(x = -10000,
                                   y = -10000,
                                   image = games.load_image("hidden\\char.png"))
        self.parent = parent
    def update(self):
        if games.keyboard.is_pressed(games.K_RETURN):
            self.parent.level_select()
            self.destroy()

class Cursor(games.Sprite):
    def __init__(self, game):
        self.spritelist = []
        super(Cursor, self).__init__(x = 100,
                                     y = 200,
                                     image = games.load_image("hidden\\select.png"))
        self.game = game
        self.levels = open("hidden\\levels.txt","r").read()
        self.positions = {1:[100,350],2:[250,350],3:[400,350],4:[550,350],5:[700,350]}
        for i in range(1,int(self.levels)+1):
            thing = games.Sprite(x = self.positions[i][0], y = self.positions[i][1], image = games.load_image("hidden\\unbut.png"))
            self.spritelist.append(thing)
            games.screen.add(thing)
            text = games.Text(x = self.positions[i][0], y = self.positions[i][1], color = color.black, size = 80, value = str(i))
            self.spritelist.append(text)
            games.screen.add(text)
        for i in range(int(self.levels)+1,6):
            thing = games.Sprite(x = self.positions[i][0], y = self.positions[i][1], image = games.load_image("hidden\\lobut.png"))
            self.spritelist.append(thing)
            games.screen.add(thing)
            text = games.Text(x = self.positions[i][0], y = self.positions[i][1], color = color.black, size = 80, value = str(i))
            self.spritelist.append(text)
            games.screen.add(text)
        self.selected = 1
        self.cooldown = 0
        self.time = time.time()
        self.oldtime = time.time()
        self.levels = int(self.levels)

    def update(self):
        self.time = time.time()
        self.cooldown -= 1*self.game.fps*(self.time-self.oldtime)
        if self.cooldown <= 0:
            if (games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT)) and not self.selected in [1]:
                self.selected -= 1
                self.cooldown = 15
            elif (games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT)) and not self.selected in [5]:
                self.selected += 1
                self.cooldown = 15
                if self.selected > self.levels:
                    self.selected -= 1
                    self.cooldown = 0
            if games.keyboard.is_pressed(games.K_SPACE):
                for i in self.spritelist:
                    i.destroy()
                self.game.enter(self.selected)
                self.destroy()
        self.x = self.positions[self.selected][0]
        self.y = self.positions[self.selected][1]
        self.oldtime = self.time

class Game(object):
    def __init__(self):
        games.screen.set_background(games.load_image("hidden\\title.png",transparent = False))
        wait = Wait(self)
        games.screen.add(wait)
        self.level = 1
        self.screen = 1
        self.spritelist = []
        self.fps = 94
        
    def level_select(self):
        games.screen.set_background(games.load_image("hidden\\levelselect.png",transparent = False))
        cursor = Cursor(self)
        games.screen.add(cursor)

    def enter(self, level):
        self.clear()
        self.level = level
        self.player = Player(100,300,self)
        games.screen.add(self.player)
        self.screen = 1
        try:
            games.screen.set_background(games.load_image("hidden\\level"+str(self.level)+"_"+str(self.screen)+".png",transparent = False))
        except:
            pass
        self.player.spawncoord = [self.player.x, self.player.y, self.player.gravity]
        self.spawn()

    def advance(self):
        self.clear()
        self.player.left = 0
        self.screen += 1
        try:
            games.screen.set_background(games.load_image("hidden\\level"+str(self.level)+"_"+str(self.screen)+".png",transparent = False))
        except:
            pass
        self.player.spawncoord = [self.player.x, self.player.y, self.player.gravity]
        self.spawn()

    def devance(self):
        self.clear()
        self.player.right = 800
        self.screen -= 1
        try:
            games.screen.set_background(games.load_image("hidden\\level"+str(self.level)+"_"+str(self.screen)+".png",transparent = False))
        except:
            pass
        self.player.spawncoord = [self.player.x, self.player.y, self.player.gravity]
        self.spawn()

    def adlevel(self):
        self.clear()
        try:
            self.player.text.destroy()
        except:
            pass
        sofar = int(open("hidden\\levels.txt","r").read())
        if self.level == 5:
            self.player.pausething.destroy()
            self.player.destroy()
            games.screen.set_background(games.load_image("hidden\\win.png",transparent = False))
            wait = Wait(self)
            games.screen.add(wait)
        elif self.level == sofar and sofar != 5:
            file = open("hidden\\levels.txt","w")
            file.write(str(sofar+1))
            file.close()
            self.player.pausething.destroy()
            self.player.destroy()
            self.level_select()
        else:
            self.player.pausething.destroy()
            self.player.destroy()
            self.level_select()

    def spawn(self):
        line = enemy_list[self.level-1]
        coordset = line.split()[self.screen-1]
        coords = coordset.split("_")
        for i in coords:
            if i:
                enemy = Enemy(i.split(",")[0],i.split(",")[1],i.split(",")[2],self)
                games.screen.add(enemy)
                self.spritelist.append(enemy)
        line = turret_list[self.level-1]
        coordset = line.split()[self.screen-1]
        coords = coordset.split("_")
        for i in coords:
            if i:
                turret = Turret(i.split(",")[0],i.split(",")[1],i.split(",")[2],self,i.split(",")[3])
                games.screen.add(turret)
                self.spritelist.append(turret)

    def clear(self):
        for i in self.spritelist:
            try:
                i.destroy()
            except:
                pass
        self.spritelist = []
        

class Player(games.Sprite):
    def __init__(self, x, y, game):
        super(Player, self).__init__(x = x,
                                     y = y,
                                     image = games.load_image("hidden\\char.png"))
        self.game = game
        self.default_image = self.image
        self.x = x
        self.y = y
        self.y_vel = 0
        self.x_vel = 0
        self.falling = True
        self.xflipped = False
        self.jumped = False
        self.gravity = 1
        self.flop = False
        self.flopdown = 3
        self.spawncoord = []
        self.prevtime = time.time()
        self.paused = False
        self.pautime = 10
        self.oldtime = time.time()
        self.time = time.time()
        self.pausething = games.Sprite(x = -10000, y = -10000, image = games.load_image("hidden\\paused.png"))
        games.screen.add(self.pausething)
        if self.game.level != 1:
            self.text = games.Text(x = 400, y = 50, size = 50, color = color.red, value = str(math.ceil(10*self.flopdown)/10))
            games.screen.add(self.text)

    def update(self):
        self.oldtime = self.time
        self.time = time.time()
        self.pautime -= self.game.fps*(self.time-self.oldtime)
        if games.keyboard.is_pressed(games.K_p) and self.pautime <= 0:
            self.paused = not self.paused
            self.prevtime = self.time
            self.pautime = 50
            self.pausething.x = -10000
            self.pausething.y = -10000
        if self.paused:
            self.pausething.x = 400
            self.pausething.y = 300
            self.pausething.elevate()
            if games.keyboard.is_pressed(games.K_q):
                self.game.clear()
                try:
                    self.text.destroy()
                except:
                    pass
                self.game.level_select()
                self.pausething.destroy()
                self.destroy()
        else:
            self.elevate()
            for i in self.overlapping_sprites:
                if type(i) == Enemy or type(i) == Bullet:
                    self.reset()
            if self.game.level != 1:
                self.text.value = str(math.ceil(10*self.flopdown)/10)
                if self.gravity < 0:
                    self.flop = True
                else:
                    self.flop = False
                self.flopdown -= self.time-self.prevtime
                self.prevtime = self.time
                if self.flopdown <= 0:
                    self.gravity *= -1
                    self.flopdown = 3
            b = 0
            if (games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT)):
                self.x_vel -= round(self.game.fps*(self.time-self.oldtime))/4
                if self.x_vel < -4:
                    self.x_vel = -4
                if not (games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT)):
                    self.xflipped = True
                b += 1
            if (games.keyboard.is_pressed(games.K_d) or games.keyboard.is_pressed(games.K_RIGHT)):
                self.x_vel += round(self.game.fps*(self.time-self.oldtime))/4
                if self.x_vel > 4:
                    self.x_vel = 4
                if not (games.keyboard.is_pressed(games.K_a) or games.keyboard.is_pressed(games.K_LEFT)):
                    self.xflipped = False
                b += 1
            if b == 0 or b == 2:
                if self.x_vel > 0:
                    self.x_vel -= round(self.game.fps*(self.time-self.oldtime))/4
                    if self.x_vel < 0:
                        self.x_vel = 0
                elif self.x_vel < 0:
                    self.x_vel += round(self.game.fps*(self.time-self.oldtime))/4
                    if self.x_vel > 0:
                        self.x_vel = 0
            try:
                if self.x_vel < 0:
                    for x in range(round(self.left),round(self.left+math.floor(self.x_vel*self.game.fps*(self.time-self.oldtime))),-1):
                        if games.screen._display.get_at((round(x),round(self.top+2))) == (0,0,0,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (0,0,0,255):
                            self.left = x
                            self.x_vel = 0
                            break
                        elif games.screen._display.get_at((round(x),round(self.top+2))) == (255,127,39,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (255,127,39,255):
                            self.reset()
                            break
                else:
                    for x in range(round(self.right),round(self.right+math.ceil(self.x_vel*self.game.fps*(self.time-self.oldtime)))):
                        if games.screen._display.get_at((round(x),round(self.top+2))) == (0,0,0,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (0,0,0,255):
                            self.right = x
                            self.x_vel = 0
                            break
                        elif games.screen._display.get_at((round(x),round(self.top+2))) == (255,127,39,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (255,127,39,255):
                            self.reset()
                            break
            except:
                pass
            self.x += self.x_vel*self.game.fps*(self.time-self.oldtime)
            try:
                if games.screen._display.get_at((round(self.x),round(self.bottom-1))) == (0,0,0,255):
                    self.y -= 1
                if games.screen._display.get_at((round(self.x),round(self.top+1))) == (0,0,0,255):
                    self.y += 1
            except:
                pass
            try:
                if self.gravity > 0:
                    if self.y_vel < 0:
                        for y in range(round(self.bottom-1),round(self.bottom - self.y_vel*self.game.fps*(self.time-self.oldtime))):
                            if games.screen._display.get_at((round(self.right-1),round(y))) == (0,0,0,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (0,0,0,255):
                                self.bottom = y
                                self.falling = False
                                self.y_vel = 0
                                break
                            elif games.screen._display.get_at((round(self.right-1),round(y))) == (255,127,39,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (255,127,39,255):
                                self.reset()
                                break
                    else:
                        for y in range(round(self.top),round(self.top - self.y_vel*self.game.fps*(self.time-self.oldtime)),-1):
                            if games.screen._display.get_at((round(self.right-1),round(y))) == (0,0,0,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (0,0,0,255):
                                self.top = y
                                self.y_vel *= -1/2
                                break
                            elif games.screen._display.get_at((round(self.right-1),round(y))) == (255,127,39,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (255,127,39,255):
                                self.reset()
                                break
                else:
                    if self.y_vel > 0:
                        for y in range(round(self.top+1),round(self.top - self.y_vel*self.game.fps*(self.time-self.oldtime)),-1):
                            if games.screen._display.get_at((round(self.right-1),round(y))) == (0,0,0,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (0,0,0,255):
                                self.top = y
                                self.falling = False
                                self.y_vel = 0
                                break
                            elif games.screen._display.get_at((round(self.right-1),round(y))) == (255,127,39,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (255,127,39,255):
                                self.reset()
                                break
                    else:
                        for y in range(round(self.bottom),round(self.bottom - self.y_vel*self.game.fps*(self.time-self.oldtime))):
                            if games.screen._display.get_at((round(self.right-1),round(y))) == (0,0,0,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (0,0,0,255):
                                self.bottom = y
                                self.y_vel *= -1/2
                                break
                            elif games.screen._display.get_at((round(self.right-1),round(y))) == (255,127,39,255) or games.screen._display.get_at((round(self.left+1),round(y))) == (255,127,39,255):
                                self.reset()
                                break
            except:
                pass
            self.y -= self.y_vel*self.game.fps*(self.time-self.oldtime)
            if self.left < 0:
                    self.game.devance()
                    self.flopdown = 3
            elif self.right > 800:
                    self.game.advance()
                    self.flopdown = 3
            if self.falling:
                value = .3
                if not (games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP)):
                    self.jumped = False
                if self.jumped:
                    value = .08
                self.y_vel -= value*self.gravity*self.game.fps*(self.time-self.oldtime)
                if self.y_vel < -10:
                    self.y_vel = -10
                if self.y_vel > 10:
                    self.y_vel = 10
            if self.bottom > 600 or self.top < 0:
                self.reset()
            else:
                try:
                    if self.gravity > 0:
                        col = games.screen._display.get_at((round(self.left+1),round(self.bottom+1)))
                        col2 = games.screen._display.get_at((round(self.right-1),round(self.bottom+1)))
                    else:
                        col = games.screen._display.get_at((round(self.left+1),round(self.top-1)))
                        col2 = games.screen._display.get_at((round(self.right-1),round(self.top-1)))
                except:
                    self.falling = False
                else:
                    if col == (0,0,0,255) or col2 == (0,0,0,255):
                        self.falling = False
                    else:
                        self.falling = True
            if (games.keyboard.is_pressed(games.K_w) or games.keyboard.is_pressed(games.K_UP)) and not self.falling and not self.y_vel:
                self.y_vel = 4*self.gravity
                self.jumped = True
            if self.xflipped:
                self.image = pygame.transform.flip(self.default_image, True, self.flop)
            else:
                self.image = pygame.transform.flip(self.default_image, False, self.flop)
            thing = games.screen._display.get_at((round(self.x),round(self.y)))
            if thing == (0,0,64,255):
                self.game.adlevel()
            elif thing == (255,127,39,255):
                self.reset()

    def reset(self):
        self.x = self.spawncoord[0]
        self.y = self.spawncoord[1]
        self.gravity = self.spawncoord[2]
        self.y_vel = 0
        self.falling = False
        self.vel_x = 0
        self.flopdown = 3

class Enemy(games.Sprite):
    def __init__(self, x, y, value, game):
        self.value = int(value)
        if int(value) == 1:
            super(Enemy, self).__init__(x = int(x),
                                        bottom = int(y),
                                        image = games.load_image("hidden\\enemy.png"))
        else:
            super(Enemy, self).__init__(x = int(x),
                                        top = int(y),
                                        image = pygame.transform.flip(games.load_image("hidden\\enemy.png"), False, True))
        self.direct = 3
        self.game = game

    def update(self):
        if not self.game.player.paused:
            try:
                if self.direct < 0:
                    for x in range(round(self.left),round(self.left+math.floor(self.direct)),-1):
                        if games.screen._display.get_at((round(x),round(self.top+2))) == (0,0,0,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (0,0,0,255):
                            self.left = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
                        elif games.screen._display.get_at((round(x),round(self.top+2))) == (255,127,39,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (255,127,39,255):
                            self.left = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
                        elif (games.screen._display.get_at((round(x),round(self.top-10))) != (0,0,0,255) and self.value == 2) or (games.screen._display.get_at((round(x),round(self.bottom+10))) != (0,0,0,255) and self.value == 1):
                            self.left = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
                else:
                    for x in range(round(self.right),round(self.right+math.ceil(self.direct))):
                        if games.screen._display.get_at((round(x),round(self.top+2))) == (0,0,0,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (0,0,0,255):
                            self.right = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
                        elif games.screen._display.get_at((round(x),round(self.top+2))) == (255,127,39,255) or games.screen._display.get_at((round(x),round(self.bottom-2))) == (255,127,39,255):
                            self.right = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
                        elif (games.screen._display.get_at((round(x),round(self.top-10))) != (0,0,0,255) and self.value == 2) or (games.screen._display.get_at((round(x),round(self.bottom+10))) != (0,0,0,255) and self.value == 1):
                            self.right = x
                            self.direct *= -1
                            self.image = pygame.transform.flip(self.image, True, False)
                            break
            except:
                pass
            self.x += self.direct*self.game.fps*(self.game.player.time-self.game.player.oldtime)
            if self.right > 800:
                self.right = 800
                self.direct *= -1
                self.image = pygame.transform.flip(self.image, True, False)
            if self.left < 0:
                self.left = 0
                self.direct *= -1
                self.image = pygame.transform.flip(self.image, True, False)

class Turret(games.Sprite):
    def __init__(self, x, y, direct, game, buu):
        super(Turret, self).__init__(x = int(x), y = int(y),
                                     image = games.load_image("hidden\\turret.png"))
        self.game = game
        self.angle = 90*int(direct)
        self.shoot_time = int(buu)

    def update(self):
        if not self.game.player.paused:
            self.shoot_time -= self.game.fps*(self.game.player.time-self.game.player.oldtime)
            if self.shoot_time <= 0:
                bullet = Bullet(self.x,self.y,self.angle,self.game)
                games.screen.add(bullet)
                self.game.spritelist.append(bullet)
                self.shoot_time = 100

class Bullet(games.Sprite):
    def __init__(self, x, y, angle, game):
        super(Bullet, self).__init__(x = x, y = y, image = games.load_image("hidden\\bullet.png"))
        self.angle = angle*math.pi/180
        self.game = game

    def update(self):
        if not self.game.player.paused:
            self.x += 4*math.sin(self.angle)*self.game.fps*(self.game.player.time-self.game.player.oldtime)
            self.y -= 4*math.cos(self.angle)*self.game.fps*(self.game.player.time-self.game.player.oldtime)
            try:
                thing = games.screen._display.get_at((round(self.x),round(self.y)))
            except:
                self.destroy()
            else:
                if thing == (0,0,0,255):
                    self.destroy()

def main():
    game = Game()
    games.screen.mainloop()
main()

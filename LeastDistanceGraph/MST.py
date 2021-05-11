import pygame, random

import tkinter as tk
from tkinter import *
import os, sys

##root = tk.Tk()
##embed = tk.Frame(root, width = 600, height = 600) #creates embed frame for pygame window
##embed.grid(columnspan = 60, rowspan = 60) # Adds grid
##embed.pack(side = LEFT) #packs window to the left
####buttonwin = tk.Frame(root, width = 75, height = 500)
####buttonwin.pack(side = LEFT)
##os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
##os.environ['SDL_VIDEODRIVER'] = 'windib'
##disp = pygame.display.set_mode((600,600))
##disp.fill(pygame.Color(255,255,255))
##pygame.display.init()
##disp = pygame.display.set_mode((600,600))
class DS():
    class Soot():
        def __init__(self, v):
            self.value = v
            self.parent = None

        def get_set(self):
            if not self.parent:
                return self
            self.parent = self.parent.get_set()
            return self.parent

        def join(self, s2):
            self.get_set().parent = s2

        def share(self, s2):
            return self.get_set() == s2.get_set()
    
    def __init__(self, arr):
        self.soots = {v:DS.Soot(v) for v in arr}

    def join(self, v1, v2):
        self.soots[v1].join(self.soots[v2])

    def test(self, v1, v2):
        return self.soots[v1].share(self.soots[v2])

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.parent = self
        self.disp = None

        self.num = 20
        self.regen()
        self.moving = True
        self.m = 2
        
        self.setup_screen()

    def regen(self):
        self.beeps = [(random.random()*500+50,random.random()*500+50) for i in range(self.num)]
        self.speeds = [[random.random()*2-1,random.random()*2-1] for i in range(self.num)]

    def setup_screen(self):
        embed = tk.Frame(self.parent, width = 600, height = 600) #creates embed frame for pygame window
        embed.grid(columnspan = 60, rowspan = 60) # Adds grid
        embed.pack(side = LEFT) #packs window to the left
        ##buttonwin = tk.Frame(root, width = 75, height = 500)
        ##buttonwin.pack(side = LEFT)
        os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        pygame.display.init()
        self.disp = pygame.display.set_mode((600,600))
        self.disp.fill(pygame.Color(255,255,255))
        self.main()

##    def mainloop(self):
##        while True:
####            print("beep")
##            if pygame.display.get_init():
##                self.main()
##            self.update_idletasks()
##            self.update()
    
    def main(self):
        if self.moving:
            for i in range(self.num):
                self.beeps[i] = (self.beeps[i][0]+self.m*self.speeds[i][0],self.beeps[i][1]+self.m*self.speeds[i][1])
                if int(self.beeps[i][0]) not in range(50,550):
                    self.speeds[i][0] *= -1
                if int(self.beeps[i][1]) not in range(50,550):
                    self.speeds[i][1] *= -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.destroy()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: self.destroy()
                elif event.key == pygame.K_r:
                    self.regen()
                elif event.key == pygame.K_UP:
                    self.num += 1
                    self.beeps.append((random.random()*500+50,random.random()*500+50))
                    self.speeds.append([random.random()*2-1,random.random()*2-1])
                elif event.key == pygame.K_DOWN and self.num:
                    self.num -= 1
                    del self.beeps[-1]
                elif event.key == pygame.K_c:
                    self.num = 0
                    self.beeps = []
        self.disp.fill((255,255,255))
        dists0 = []
        for i in range(len(self.beeps)):
            for j in range(i+1,len(self.beeps)):
                dists0.append((self.beeps[i],self.beeps[j],(self.beeps[i][0]-self.beeps[j][0])*(self.beeps[i][0]-self.beeps[j][0]) + (self.beeps[i][1]-self.beeps[j][1])*(self.beeps[i][1]-self.beeps[j][1])))
        ds = DS(self.beeps)
        dists = sorted(dists0, key=lambda x:x[2])
        out = []
        for dist in dists:
            if not ds.test(dist[0], dist[1]):
                ds.join(dist[0],dist[1])
                out.append(dist)
        for connection in out:
            pygame.draw.line(self.disp,(0,0,0),connection[0],connection[1],5)
        for beep in self.beeps:
            pygame.draw.circle(self.disp,(255,0,0),(int(beep[0]),int(beep[1])),5)
    ##    if num >= 2:
    ##        for i in range(2):
    ##            b = pygame.Surface((600,600),pygame.SRCALPHA)
    ##            b.set_alpha(0)
    ##            beep = beeps[i]
    ##            pygame.draw.circle(b,pygame.Color(0,255*i,255-255*i,50),(int(beep[0]),int(beep[1])),int(dists0[0][2]**.5))
    ##            disp.blit(b,(0,0))
        pygame.display.update()
        self.after(50,self.main)

##top = Tk()
##app = App(top)
##app.pack()
##top.mainloop()
app = App()
app.mainloop()









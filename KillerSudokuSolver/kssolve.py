import pygame, random, sys

pygame.init()
disp = pygame.display.set_mode((600, 600))
font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
nums = [font.render(str(x+1),False,(0,0,0)) for x in range(9)]
tinyfont = pygame.font.SysFont(pygame.font.get_default_font(), 20)
tinynums = [tinyfont.render(str(x),False,(0,0,0)) for x in range(10)]

class Cell:
    def __init__(self, gridx, gridy):
        self.num = None
        self.x = gridx
        self.y = gridy
        Board.cols[gridx].add_cell(self)
        Board.rows[gridy].add_cell(self)
        self.non = gridy//3*3+gridx//3
        Board.nonets[self.non].add_cell(self)
        self.basex = 17 + 62*self.x + self.non%3*5
        self.basey = 17 + 62*self.y + self.non//3*5
        self.bg = (255,255,255)
        self.nbg = (255,255,255)
        self.t = None
        self.tt = None
        self.possible = [4]*9

    def __repr__(self):
        return "("+str(self.x+1)+", "+str(self.y+1)+")"

    def set_num(self, num):
        if not num or self.possible[num-1] == 4:
            if self.t and not self.t.set_num(self, num):
                return False
            Board.cols[self.x].unset(self.num)
            Board.rows[self.y].unset(self.num)
            Board.nonets[self.non].unset(self.num)
            if self.t:
                self.t.unset(self.num)
                #self.t.set_num(self, num)
            Board.cols[self.x].set_num(self, num)
            Board.rows[self.y].set_num(self, num)
            Board.nonets[self.non].set_num(self, num)
            if not self.num and num:
                Board.unfilled.remove(self)
            elif self.num and not num:
                Board.unfilled.append(self)
            self.num = num
            #if not random.randint(0, 2000): self.render()
            return True
        return False
##        if not Board.cols[self.x].set_num(self, num):
##            return False
##        if not Board.rows[self.y].set_num(self, num):
##            Board.cols[self.x].unset(num)
##            return False
##        if not Board.nonets[self.non].set_num(self, num):
##            Board.cols[self.x].unset(num)
##            Board.rows[self.y].unset(num)
##            return False
##        if self.t and not self.t.set_num(self, num):
##            Board.cols[self.x].unset(num)
##            Board.rows[self.y].unset(num)
##            Board.nonets[self.non].unset(num)
##            return False
##        if self.num:
##            Board.cols[self.x].unset(self.num)
##            Board.rows[self.y].unset(self.num)
##            Board.nonets[self.non].unset(self.num)
##            if self.t: self.t.unset(self.num)
##        self.num = num
##        if not num:
##            num = 9
##        #draw num
##        tb = nums[num-1]
##        width, height = tb.get_size()
##        x = 17 + 62*self.x + self.non%3*5 + 30 - width/2 + 1
##        y = 17 + 62*self.y + self.non//3*5 + 30 - height/2 + 1
##        disp.fill(self.bg,(x,y,width,height))
##        if self.num: disp.blit(tb,(x,y))
##        if not random.randint(0, 2000): pygame.display.flip()
##        return True

    def reset_back(self):
        self.switch_back(self.nbg)

    def render(self):
        if self.num: num = self.num
        else: num = 9
        tb = nums[num-1]
        width, height = tb.get_size()
        xoff = 30 - width/2 + 1
        yoff = 30 - height/2 + 1
        disp.fill(self.bg,(self.basex+xoff,self.basey+yoff,width,height))
        if self.num: disp.blit(tb,(self.basex+xoff,self.basey+yoff))                
        pygame.display.update((self.basex+xoff,self.basey+yoff,width,height))

    def rendert(self):
        width, height = tinynums[0].get_size()
        if self.tt:
            temp = self.tt
            ns = []
            while temp:
                ns.append(tinynums[temp%10])
                temp //= 10
            for i, num in enumerate(ns[::-1]):
                disp.fill(self.bg,(self.basex+width*i,self.basey,width,height))
                disp.blit(num,(self.basex+width*i,self.basey))

    def switch_back(self, color):
        self.bg = color
        basex = 17 + 62*self.x + self.non%3*5
        basey = 17 + 62*self.y + self.non//3*5
        pygame.draw.rect(disp, color, (basex, basey, 60, 60))
        if self.num:
            tb = nums[self.num-1]
            width, height = tb.get_size()
            x = basex + 30 - width/2 + 1
            y = basey + 30 - height/2 + 1
            disp.blit(tb,(x,y))
        self.rendert()
        pygame.display.update((basex, basey, 60, 60))

class Group:
    def __init__(self):
        self.cells = []
        self.nums = {x+1 : None for x in range(9)}

    def __repr__(self):
        a = self.cells[0]
        b = self.cells[-1]
        if a.non == b.non: return "Nonet "+str(a.non+1)
        elif a.x == b.x: return "Column "+str(a.x+1)
        elif a.y == b.y: return "Row "+str(a.y+1)
        else: return "WTF"

    def add_cell(self, cell):
        self.cells.append(cell)

    def set_num(self, cell, num):
        if not num: return True
##        if self.nums[num]:
##            #print(self.nums)
##            return False
##        else:
        self.nums[num] = cell
        for cell in self.cells:
            cell.possible[num-1] -= 1
##            return True

    def unset(self, num):
        if num and self.nums[num]:
            self.nums[num] = None
            for cell in self.cells:
                cell.possible[num-1] += 1

    def set_group(self, nums, cells):
        for cell in [x for x in self.cells if x not in cells]:
            for num in nums:
                cell.possible[num-1] -= 1

    def unset_group(self, nums, cells):
        for cell in [x for x in self.cells if x not in cells]:
            for num in nums:
                cell.possible[num-1] += 1

class Total:
    def __init__(self, tsc):
        self.cells = []
        self.nums = {x+1 : None for x in range(9)}
        self.numsets = 0
        self.total = 0
        self.tsc = tsc
        self.tl = None

    def add_cell(self, cell):
        if not self.tl: self.tl = cell
        else:
            if cell.y < self.tl.y: self.tl = cell
            elif cell.y == self.tl.y and cell.x < self.tl.x: self.tl = cell
        self.cells.append(cell)
        cell.switch_back(tsc)
        cell.nbg = self.tsc
        cell.t = self

    def set_num(self, cell, num):
        if not num: return True
        if self.nums[num]:
            return False
        elif num > self.total:
            return False
        elif num != self.total and self.numsets+1 == len(self.cells):
            return False
        else:
            self.nums[num] = cell
            self.total -= num
            self.numsets += 1
            for cell in self.cells:
                cell.possible[num-1] -= 1
                for i in range(self.total+1, min(self.total+num+1,10)):
                    if i != num and not self.nums[i]:
                        cell.possible[i-1] -= 1
            return True

    def draw_t(self):
##        for cell in self.cells:
##            cell.possible = [4]*9
##            for i in range(self.total-1, 9):
##                cell.possible[i] -= 1
        combs = self.combs(len(self.cells))
        seen = [0]*9
        for comb in combs:
            for num in comb:
                seen[num-1]+=1
        for i,n in enumerate(seen):
            if n == 0:
                for cell in self.cells:
                    cell.possible[i] -= 1
        self.tl.tt = self.total
        self.tl.rendert()

    def unset(self, num):
        if num and self.nums[num]:
            self.nums[num] = None
            self.total += num
            self.numsets -= 1
            for cell in self.cells:
                cell.possible[num-1] += 1
                for i in range(self.total-num+1, min(self.total+1,10)):
                    if i != num and not self.nums[i]:
                        cell.possible[i-1] += 1

    def combs(self, num, cur=0, rem = [1,2,3,4,5,6,7,8,9]):
        if num == 1:
            if self.total-cur not in rem:
                return []
            return [(self.total-cur,)]
        c = []
        for i in rem:
            b = self.combs(num-1,cur+i,[k for k in rem if k > i])
            c += [(i,)+k for k in b]
        return c

    def explode(self):
        for cell in self.cells:
            cell.t = None
            cell.tt = None
            cell.nbg = (255,255,255)
            cell.set_num(None)
            cell.reset_back()
        for cell in self.cells:
            cell.possible = [4]*9
        Board.totals.remove(self)

class Board:
    rows = []
    cols = []
    nonets = []
    cells = []
    unfilled = []
    totals = []
    
    def __init__(self):
        Board.rows = [Group() for i in range(9)]
        Board.cols = [Group() for i in range(9)]
        Board.nonets = [Group() for i in range(9)]
        Board.cells = [Cell(x,y) for y in range(9) for x in range(9)]
        Board.unfilled = Board.cells.copy()
        self.draw_base()

    def draw_base(self):
        disp.fill((255,255,255))
        pygame.draw.rect(disp, (0,0,0), (10,10,580,580))
        for non in range(9):
            basex = non%3*191+17
            basey = non//3*191+17
            #pygame.draw.rect(disp, (255,255,255), (basex, basey, 184, 184))
            for nonon in range(9):
                shiftx = nonon%3*62
                shifty = nonon//3*62
                pygame.draw.rect(disp, (255,255,255), (basex+shiftx, basey+shifty, 60, 60))
        
board = Board()
##for cell in Board.cells:
##    cell.set_num(random.randint(1,9))

counterx = 0
countery = 0
ts = None

pairs = []

def forced():
    changed = []
    for cell in Board.unfilled:
        possible = cell.possible.count(4)
        if possible == 1:
            num = cell.possible.index(4)+1
            if not cell.set_num(num):
                return (False, changed)
            #print(Board.cells[9*8+3].possible[0],": set from num",num,cell)
            #cell.render()
            changed.append(cell)
        elif possible == 0:
            return (False, changed)
    for total in Board.totals:
        if len(total.cells)-total.numsets == 1:
            for cell in total.cells:
                if cell.num == None:
                    if total.total not in range(1,10) or not cell.set_num(total.total):
                        return (False, changed)
                    #cell.render()
                    changed.append(cell)
                    break
    for groupie in [Board.rows, Board.cols, Board.nonets]:
        for group in groupie:
            cells = {cell:[i+1 for i in range(9) if cell.possible[i] == 4] for cell in group.cells if not cell.num}
            if not cells: continue
            for i in [x for x in range(1,10) if not group.nums[x]]:
                found = 0
                spot = -1
                for j, cell in enumerate(group.cells):
                    if cell.possible[i-1] == 4 and not cell.num:
                        found += 1
                        spot = j
                if found == 1:
                    if group.cells[spot].num or not group.cells[spot].set_num(i):
                        return (False, changed)
                    #print(Board.cells[9*8+3].possible[0],": set from group",i,group.cells[spot])
                    #group.cells[spot].render()
                    changed.append(group.cells[spot])
                elif found == 0:
                    return (False, changed)
##            if changed: continue
##            finished = []
##            for cell in cells:
##                if cell in finished:
##                    continue
##                found = []
##                num = len(cells[cell])
##                if num == len(cells) or num < 2:
##                    finished.append(cell)
##                    continue
##                req = cells[cell]#.copy()
##                for cell2 in cells:
##                    if cell2 in finished:
##                        continue
##                    if all(x in req for x in cells[cell2]):
##                        found.append(cell2)
##                if found in pairs:
##                    continue
##                if len(found) == num:
##                    if all(found[0].x == other.x for other in found[1:]):
##                        Board.cols[found[0].x].set_group(req, found)
##                        pairs.append(found)
##                        changed.append((Board.cols[found[0].x], req, found))
##                    if all(found[0].y == other.y for other in found[1:]):
##                        Board.rows[found[0].y].set_group(req, found)
##                        pairs.append(found)
##                        changed.append((Board.rows[found[0].y], req, found))
##                    if all(found[0].non == other.non for other in found[1:]):
##                        Board.nonets[found[0].non].set_group(req, found)
##                        pairs.append(found)
##                        changed.append((Board.nonets[found[0].non], req, found))
##                    for cell in found:
##                        finished.append(cell)
                    #print(found)
            
    return (True,changed)

def clear(stuff, end = False):
    for thing in stuff:
        if type(thing) == Cell:
            #print(Board.cells[9*8+3].possible[0],": unsetting",thing.num,thing)
            if not end: thing.set_num(None)
        else:
            #print(Board.cells[9*8+3].possible[0],": unpairing:",thing[2],"from group",thing[0])
            try: pairs.remove(thing[2])
            except Exception as e:
                #print("tried to unpair:",thing[2])
                continue
##                print(thing[2])
##                print(pairs)
##                raise e
            else:
                thing[0].unset_group(thing[1],thing[2])
                #print(Board.cells[9*8+3].possible[0],":thumbs up")

def brute_solve(pos = 0):
    if not random.randint(0, 2000):
        for cell in Board.cells:
            cell.render()
    e = pygame.event.get()
    for event in e:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    if Board.cells[pos].num:
        if pos == 80: return True
        else: return brute_solve(pos+1)
    else:
        a = Board.cells[pos].possible
        poss = []
        for i in range(9):
            if a[i] == 4: poss.append(i)
        for i in poss:
            if Board.cells[pos].set_num(i+1):
                if pos == 80 or brute_solve(pos+1):
                    Board.cells[pos].render()
                    return True
                else:
                    Board.cells[pos].set_num(None)
        return False

def less_brute(pos = 0, step = False):
    #print(pairs)
    if Board.unfilled == []: return True
    if step:
        print(pos+1)
        for cell in Board.cells:
            cell.render()
        flag = True
        while flag:
            e = pygame.event.get()
            for event in e:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return True
                    elif event.key == pygame.K_a:
                        flag = False
                    elif event.key == pygame.K_SPACE:
                        flag = False
                        step = False
    e = pygame.event.get()
    for event in e:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return True
    if Board.cells[pos].num:
        if pos == 80: return True
        else: return less_brute(pos+1, step)
    else:
        #smart solving
        cells = []
        val = forced()
        cells += val[1]
        if not val[0]:
            clear(cells)
            return False
        while val[1]:
            val = forced()
            cells += val[1]
            if not val[0]:
                clear(cells)
                return False
        if step: print(cells)
        if not random.randint(0, 10):
            for cell in Board.cells:
                cell.render()

        if Board.cells[pos].num:
            if pos == 80:
                clear(cells, True)
                return True
            else:
                if less_brute(pos+1, step):
                    clear(cells, True)
                    return True
                else:
                    clear(cells)
                    return False

        #dumb solving
        a = Board.cells[pos].possible
        poss = [i for i in range(9) if a[i] == 4]
        for i in poss:
            if Board.cells[pos].set_num(i+1):
                if pos == 80 or less_brute(pos+1, step):
                    Board.cells[pos].render()
                    clear(cells, True)
                    return True
                else:
                    #print(Board.cells[9*8+3].possible[0],": undoing",i+1,Board.cells[pos])
                    Board.cells[pos].set_num(None)
                    #print(Board.cells[9*8+3].possible[0],": undone",i+1,Board.cells[pos])
        clear(cells)
        if step: print("removing",cells)
        return False

def solve(step = False):
    val = forced()
    if not val[0]:
        return False
    while val[1]:
        val = forced()
        if not val[0]:
            return False
    #return brute_solve()
    ans = less_brute(0, step)
    pairs.clear()
    return ans

def tscreating(event):
    global counterx, countery, ts
    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()
        elif event.key == pygame.K_UP:
            countery -= 1
            countery = countery % 9
            if Board.cells[9*countery+counterx] not in ts.cells:
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
        elif event.key == pygame.K_DOWN:
            countery += 1
            countery = countery % 9
            if Board.cells[9*countery+counterx] not in ts.cells:
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
        elif event.key == pygame.K_LEFT:
            counterx -= 1
            counterx = counterx % 9
            if Board.cells[9*countery+counterx] not in ts.cells:
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
        elif event.key == pygame.K_RIGHT:
            counterx += 1
            counterx = counterx % 9
            if Board.cells[9*countery+counterx] not in ts.cells:
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
        elif event.key == pygame.K_BACKSPACE:
            ts.total //= 10
        elif event.key == pygame.K_0:
            ts.total = 10*ts.total
        elif event.key == pygame.K_1:
            ts.total = 10*ts.total + 1
        elif event.key == pygame.K_2:
            ts.total = 10*ts.total + 2
        elif event.key == pygame.K_3:
            ts.total = 10*ts.total + 3
        elif event.key == pygame.K_4:
            ts.total = 10*ts.total + 4
        elif event.key == pygame.K_5:
            ts.total = 10*ts.total + 5
        elif event.key == pygame.K_6:
            ts.total = 10*ts.total + 6
        elif event.key == pygame.K_7:
            ts.total = 10*ts.total + 7
        elif event.key == pygame.K_8:
            ts.total = 10*ts.total + 8
        elif event.key == pygame.K_9:
            ts.total = 10*ts.total + 9
        elif event.key == pygame.K_LSHIFT:
##            print(ts.total)
            Board.totals.append(ts)
            ts.draw_t()
            ts = None

            

Board.cells[9*countery+counterx].switch_back((255,0,255))

while True:
    for event in pygame.event.get():
        if ts: tscreating(event)
        elif event.type == pygame.QUIT: pygame.quit(); sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: pygame.quit(); sys.exit()

            #move cursor
            elif event.key == pygame.K_UP:
                Board.cells[9*countery+counterx].reset_back()
                countery -= 1
                countery = countery % 9
                Board.cells[9*countery+counterx].switch_back((255,0,255))
            elif event.key == pygame.K_DOWN:
                Board.cells[9*countery+counterx].reset_back()
                countery += 1
                countery = countery % 9
                Board.cells[9*countery+counterx].switch_back((255,0,255))
            elif event.key == pygame.K_LEFT:
                Board.cells[9*countery+counterx].reset_back()
                counterx -= 1
                counterx = counterx % 9
                Board.cells[9*countery+counterx].switch_back((255,0,255))
            elif event.key == pygame.K_RIGHT:
                Board.cells[9*countery+counterx].reset_back()
                counterx += 1
                counterx = counterx % 9
                Board.cells[9*countery+counterx].switch_back((255,0,255))
            
            elif event.key == pygame.K_c: #clear
                for cell in Board.cells:
                    cell.t = None
                    cell.tt = None
                    cell.nbg = (255,255,255)
                    cell.set_num(None)
                    cell.reset_back()
                for cell in Board.cells:
                    cell.possible = [4]*9
                Board.totals = []
                Board.cells[9*countery+counterx].switch_back((255,0,255))
            elif event.key == pygame.K_SPACE:
                print(solve())
                for cell in Board.cells:
                    cell.render()
            elif event.key == pygame.K_LCTRL:
                print(solve(True))
                for cell in Board.cells:
                    cell.render()
            elif event.key == pygame.K_f:
                print(forced())
            elif event.key == pygame.K_s:
                print(Board.cells[9*countery+counterx].possible)
            elif event.key == pygame.K_LSHIFT:
                tsc = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
                ts = Total(tsc)
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
            elif event.key == pygame.K_b: #shade cell blue for testing
                Board.cells[9*countery+counterx].switch_back((0,0,255))
            elif event.key == pygame.K_BACKSPACE:
                Board.cells[9*countery+counterx].set_num(None)
            elif event.key == pygame.K_DELETE:
                if Board.totals: Board.totals[-1].explode()
            elif event.key == pygame.K_1:
                Board.cells[9*countery+counterx].set_num(1)
            elif event.key == pygame.K_2:
                Board.cells[9*countery+counterx].set_num(2)
            elif event.key == pygame.K_3:
                Board.cells[9*countery+counterx].set_num(3)
            elif event.key == pygame.K_4:
                Board.cells[9*countery+counterx].set_num(4)
            elif event.key == pygame.K_5:
                Board.cells[9*countery+counterx].set_num(5)
            elif event.key == pygame.K_6:
                Board.cells[9*countery+counterx].set_num(6)
            elif event.key == pygame.K_7:
                Board.cells[9*countery+counterx].set_num(7)
            elif event.key == pygame.K_8:
                Board.cells[9*countery+counterx].set_num(8)
            elif event.key == pygame.K_9:
                Board.cells[9*countery+counterx].set_num(9)
    Board.cells[9*countery+counterx].render()
    pygame.display.flip()

import pygame, random, sys

pygame.init()
disp = pygame.display.set_mode((600, 600))
font = pygame.font.SysFont(pygame.font.get_default_font(), 60)
nums = [font.render(str(x+1),False,(0,0,0)) for x in range(9)]
tinyfont = pygame.font.SysFont(pygame.font.get_default_font(), 20)
tinynums = [tinyfont.render(str(x),False,(0,0,0)) for x in range(10)]
minifont = pygame.font.SysFont(pygame.font.get_default_font(), 15)
mininums = [tinyfont.render(str(x+1),False,(127,255,127)) for x in range(9)]

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
        self.possible = [False]*9

    def __repr__(self):
        return "("+str(self.x+1)+", "+str(self.y+1)+")"

    def set_num(self, num):
        self.num = num
        if num: self.possible = [False]*9

    def reset_back(self):
        self.switch_back(self.nbg)

    def render(self):
        if self.num:
            tb = nums[self.num-1]
            width, height = tb.get_size()
            xoff = 30 - width/2 + 1
            yoff = 30 - height/2 + 1
            disp.fill(self.bg,(int(self.basex+xoff-10),int(self.basey+yoff),width+20,height))
            disp.blit(tb,(int(self.basex+xoff),int(self.basey+yoff)))
            pygame.display.update((int(self.basex+xoff-10),int(self.basey+yoff),width+20,height))
        else:
            width, height = mininums[0].get_size()
            xdisp = 12
            ydisp = 12
            disp.fill(self.bg,(self.basex+xdisp,self.basey+ydisp,3*height,3*height))
            for num in [i for i in range(9) if self.possible[i]]:
                disp.blit(mininums[num],(self.basex+xdisp+(num%3)*height,self.basey+ydisp+(num//3)*height,width,height))
            pygame.display.update((self.basex+xdisp,self.basey+ydisp,3*height,3*height))

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
        self.rendert()
        self.render()
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
##        combs = self.combs(len(self.cells))
##        seen = [0]*9
##        for comb in combs:
##            for num in comb:
##                seen[num-1]+=1
##        for i,n in enumerate(seen):
##            if n == 0:
##                for cell in self.cells:
##                    cell.possible[i] -= 1
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

def fill_possible():
    for cell in Board.cells:
        if not cell.num: cell.possible = [True]*9

def naked_single():
    print("naked single")
    changed = False
    for cell in Board.cells:
        if cell.possible.count(True) == 1:
            cell.set_num(cell.possible.index(True)+1)
            changed = True
    return changed

def remove_possible():
    print("removing")
    changed = False
    for cell in Board.cells:
        if cell.num:
            for group in [Board.rows[cell.y], Board.cols[cell.x], Board.nonets[cell.non]]:
                for cell2 in group.cells:
                    if cell2.possible[cell.num-1]:
                        cell2.possible[cell.num-1] = False
                        changed = True
    return changed

def hidden_single():
    print("hidden single")
    to_set = []
    for groupie in [Board.rows, Board.cols, Board.nonets]:
        for group in groupie:
            for num in range(9):
                spots = [cell for cell in group.cells if cell.possible[num]]
                if len(spots) == 1:
                    to_set.append((num+1,spots[0]))
    for num, cell in to_set:
        cell.set_num(num)
    if to_set: return True
    return False

def naked_pairs():
    def test_combos(cells, built = [], current = [False]*9):
        #if len(cells) == 1: return False
        cur = len(built)+1
        for i, cell in enumerate(cells):
            current2 = [current[j] or cell.possible[j] for j in range(9)]
            t = current2.count(True)
            if cur == t:
                return (built + [cell], current2)
            elif t-cur >= len(cells)-1 or t>4:
                continue
            else:
                val = test_combos(cells[i+1:], built + [cell], current2)
                if val: return val
                continue
        return False
            
    print("naked pairs")
    changed = False
    for groupie in [Board.rows, Board.cols, Board.nonets]:
        for group in groupie:
            cells = [cell for cell in group.cells if not cell.num]
            #cells = [cell for cell in cells if cell.possible.count(True) < min(5, len(cells))]
            val = test_combos(cells)
            if val and val[0] != cells:
                other_cells = [cell for cell in group.cells if cell not in val[0]]
                nums = [i for i, x in enumerate(val[1]) if x]
                for cell in other_cells:
                    for num in nums:
                        if not changed and cell.possible[num]:
                            changed = True
                        cell.possible[num] = False
    return changed

def hidden_pairs():
    changed = []
    sel_group = None
    def test_pairs(spots, built = [], current = []):
        #if len(spots) == 1: return False
        cur = len(built)+1
        for i, spot in enumerate(spots):
            current2 = current + [cell for cell in spot if cell not in current]
            t = len(current2)
            #if sel_group == Board.nonets[6]: print(cur,":",i,"-",t,"?",len(spots))
            if cur == t:
                return (built + [spot], current2)
            elif t-cur >= len(spots)-1 or t>4:
                continue
            else:
                val = test_pairs(spots[i+1:], built + [spot], current2)
                if val:
                    built2, current2 = val
                    orig_spots = [[cell for cell in sel_group.cells if cell.possible[num]] for num in range(9)]
                    nums = []
                    for i, spot in enumerate(orig_spots):
                        for spot2 in built2:
                            if spot == spot2:
                                nums += [i]
                    out_of_place = [num for num in [i for i in range(9) for cell in current2 if cell.possible[i]] if num not in nums]
                    if out_of_place:
                        for num in out_of_place:
                            for cell in current2:
                                cell.possible[num] = False
                        if not changed: changed.append(1)
                        continue
                continue
        return False
    
    print("hidden pairs")
    to_set = []
    for groupie in [Board.rows, Board.cols, Board.nonets]:
        for group in groupie:
            sel_group = group
            spots = [[cell for cell in group.cells if cell.possible[num]] for num in range(9)]
            spots2 = [spot for spot in spots if spot]
            test_pairs(spots2)
    return changed

def line_to_box():
    print("line to box")
    changed = False
    for groupie in [Board.rows, Board.cols]:
        for group in groupie:
            spots = [[cell for cell in group.cells if cell.possible[num]] for num in range(9)]
            for i in range(9):
                if spots[i]:
                    non = spots[i][0].non
                    if all(spots[i][x].non == non for x in range(len(spots[i]))):
                        for cell in Board.nonets[non].cells:
                            if cell not in spots[i] and cell.possible[i]:
                                changed = True
                                cell.possible[i] = False
    return changed

def box_to_line():
    print("box to line")
    changed = False
    for group in Board.nonets:
        spots = [[cell for cell in group.cells if cell.possible[num]] for num in range(9)]
        for i in range(9):
            if spots[i]:
                row, col = spots[i][0].y, spots[i][0].x
                if all(spots[i][j].y == row for j in range(len(spots[i]))):
                    for cell in Board.rows[row].cells:
                            if cell not in spots[i] and cell.possible[i]:
                                changed = True
                                cell.possible[i] = False
                elif all(spots[i][j].x == col for j in range(len(spots[i]))):
                    for cell in Board.cols[col].cells:
                            if cell not in spots[i] and cell.possible[i]:
                                changed = True
                                cell.possible[i] = False
    return changed

def xwing():
    print("x-wing")
    for num in range(9):
        rows = []
        for row in range(9):
            rows.append([col for col in range(9) if Board.rows[row].cells[col].possible[num]])
        for i, row in enumerate(rows):
            if len(row) == 2 and rows.count(row) == 2 and rows[i+1:].count(row) == 1:
                otherrow = rows[i+1:].index(row)+i+1
                changed = False
                for col in row:
                    for cell in Board.cols[col].cells:
                        if cell.y != i and cell.y != otherrow and cell.possible[num]:
                            cell.possible[num] = False
                            changed = True
                if changed: return True
        cols = []
        for col in range(9):
            cols.append([row for row in range(9) if Board.cols[col].cells[row].possible[num]])
        for i, col in enumerate(cols):
            if len(col) == 2 and cols.count(col) == 2 and cols[i+1:].count(col) == 1:
                othercol = cols[i+1:].index(col)+i+1
                changed = False
                for row in col:
                    for cell in Board.rows[row].cells:
                        if cell.x != i and cell.x != othercol and cell.possible[num]:
                            cell.possible[num] = False
                            changed = True
                if changed: return True
    return False

def ywing():
    print("y-wing")
    candidates = [cell for cell in Board.cells if cell.possible.count(True) == 2]
    for pcell in candidates:
##        sharerows = [cell for cell in candidates if cell != pcell and cell.y == pcell.y]
##        sharecols = [cell for cell in candidates if cell != pcell and cell.x == pcell.x]
##        sharenons = [cell for cell in candidates if cell != pcell and cell.non == pcell.non]
        nums = [i for i in range(9) if pcell.possible[i]] # this cell's nums
        can2 = [] # cells that share a single number with this cell, other number
        for cell in candidates:
            total = 0
            for num in nums:
                if cell.possible[num]: total += 1
            if total == 1: can2.append((cell, [i for i in range(9) if i not in nums and cell.possible[i]]))
        others = [gr[1][0] for gr in can2] # list of the other numbers
        finals = [] # number, list of the groups of the other cells
        for i in range(9):
            if others.count(i) >= 2:
                finals.append((i, [cell[0] for cell in can2 if cell[1][0] == i]))
        for final in finals:
            def testpairs(remain, num, first = None):
                if not first:
                    for i, cell in enumerate(remain):
                        if testpairs(remain[i+1:], num, cell): return True
                    return False
                else:
                    for cell in remain:
                        passing = []
                        flag = False
                        for cell2 in (first, cell):
                            if cell2.x == pcell.x: passing += ["x"]
                            elif cell2.y == pcell.y: passing += ["y"]
                            elif cell2.non == pcell.non: passing += ["non"]
                            else: flag = True
                        if flag: continue
                        if passing[0] == passing[1]: continue
                        changed = False
                        if Board.cols[first.x].cells[cell.y].possible[num]:
                            changed = True
                            Board.cols[first.x].cells[cell.y].possible[num] = False
                        if Board.cols[cell.x].cells[first.y].possible[num]:
                            changed = True
                            Board.cols[cell.x].cells[first.y].possible[num] = False
                        return changed
            if testpairs(final[1], final[0]): return True
    return False
                        
        
            

strats = [naked_single, remove_possible, hidden_single, naked_pairs, hidden_pairs, line_to_box, box_to_line, xwing, ywing]

def solve(step = False):
    fill_possible()
    for cell in Board.cells:
        cell.render()
    changed = True
    while changed:
        flag = True
        e = pygame.event.get()
        for event in e:
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
                elif event.key == pygame.K_a:
                    flag = False
        if step and flag: continue
        changed = False
        for strat in strats:
            if strat():
                changed = True
                break
        for cell in Board.cells:
            cell.render()

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
                    cell.possible = [False]*9
                    cell.reset_back()
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
            elif event.key == pygame.K_s:
                file = open("sudo.txt", "w")
                string = ""
                for cell in Board.cells:
                    if not cell.num:
                        string += " "
                    else:
                        string += str(cell.num)
                file.write(string)
                file.close()
                print("board saved")
            elif event.key == pygame.K_l:
                for cell in Board.cells:
                    cell.t = None
                    cell.tt = None
                    cell.nbg = (255,255,255)
                    cell.set_num(None)
                    cell.possible = [False]*9
                Board.totals = []
                Board.cells[9*countery+counterx].switch_back((255,0,255))
                file = open("sudo.txt", "r")
                string = file.readline()
                file.close()
                for i, letter in enumerate(string):
                    if letter != " ":
                        Board.cells[i].set_num(int(letter))
                    Board.cells[i].reset_back()
                print("board loaded")
            elif event.key == pygame.K_LSHIFT:
                tsc = (random.randint(100,255),random.randint(100,255),random.randint(100,255))
                ts = Total(tsc)
                if Board.cells[9*countery+counterx].t:
                    Board.cells[9*countery+counterx].t.explode()
                ts.add_cell(Board.cells[9*countery+counterx])
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

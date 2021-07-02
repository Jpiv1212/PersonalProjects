import random

def generate(columns, rows, often, spawnx, spawny):
    level = [[0 for i in range(columns)] for i in range(rows)]
    level[spawny][spawnx] = 1
    elevator = [spawny, spawnx]
    while elevator == [spawny, spawnx] or elevator[0]%2 == 1 or elevator[1]%2 == 1:
        elevator = [random.randint(0, rows-1), random.randint(0, columns-1)]
    level[elevator[0]][elevator[1]] = 16
    x = spawnx
    y = spawny
    way = random.randint(1, 4)
    tried = []
    one = []
    while True:
        try:
            if level[y][x+1] == 16:
                level[y][x+1] = 2
        except: pass
        if level[y][x-1] == 16 and x-1 >= 0:
            level[y][x-1] = 2
        try:
            if level[y+1][x] == 16:
                level[y+1][x] = 2
        except: pass
        if level[y-1][x] == 16 and y-1 >= 0:
            level[y-1][x] = 2
        change = False
        if random.randint(1, often) == 1:
            change = "eggs"
        if way == 1:
            try:
                if level[y][x+1] == 0:
                    if y%2 == 0 or x%2 == 1:
                        good = 0
                        try:
                            if level[y][x+2] in [0, 16]:
                                good += 1
                        except: good += 1
                        try:
                            if level[y+1][x+1] in [0, 16]:
                                good += 1
                        except: good += 1
                        try:
                            if level[y-1][x+1] in [0, 16] or y-1 < 0:
                                good += 1
                        except: good += 1
                        if good < 3:
                            change = True
                        else:
                            x += 1
                            level[y][x] = 1
                            tried = []
                    else:
                        change = True
                elif level[y][x+1] == 1:
                    one = [y, x+1]
                    change = True
                else:
                    change = True
            except: change = True
        elif way == 2:
            if level[y][x-1] == 0 and x-1 >= 0:
                if y%2 == 0 or x%2 == 1:
                    good = 0
                    if level[y][x-2] in [0, 16] or x-2 < 0:
                        good += 1
                    try:
                        if level[y+1][x-1] in [0, 16]:
                            good += 1
                    except: good += 1
                    if level[y-1][x-1] in [0, 16] or y-1 < 0:
                        good += 1
                    if good < 3:
                        change = True
                    else:
                        x -= 1
                        level[y][x] = 1
                        tried = []
                else:
                    change = True
            elif level[y][x-1] == 1 and x-1 >= 0:
                one = [y, x-1]
                change = True
            else:
                change = True
        elif way == 3:
            try:
                if level[y+1][x] == 0:
                    if y%2 == 1 or x%2 == 0:
                        good = 0
                        try:
                            if level[y+2][x] in [0, 16]:
                                good += 1
                        except: good += 1
                        try:
                            if level[y+1][x+1] in [0, 16]:
                                good += 1
                        except: good += 1
                        try:
                            if level[y+1][x-1] in [0, 16] or x-1 < 0:
                                good += 1
                        except: good += 1
                        if good < 3:
                            change = True
                        else:
                            y += 1
                            level[y][x] = 1
                            tried = []
                    else:
                        change = True
                elif level[y+1][x] == 1:
                    one = [y+1, x]
                    change = True
                else:
                    change = True
            except: change = True
        elif way == 4:
            if level[y-1][x] == 0 and y-1 >= 0:
                if y%2 == 1 or x%2 == 0:
                    good = 0
                    if level[y-2][x] in [0, 16] or y-2 < 0:
                        good += 1
                    try:
                        if level[y-1][x+1] in [0, 16]:
                            good += 1
                    except: good += 1
                    try:
                        if level[y-1][x-1] in [0, 16] or x-1 < 0:
                            good += 1
                    except: good += 1
                    if good < 3:
                        change = True
                    else:
                        y -= 1
                        level[y][x] = 1
                        tried = []
                else:
                    change = True
            elif level[y-1][x] == 1 and y-1 >= 0:
                one = [y-1, x]
                change = True
            else:
                change = True
        if change:
            if change == True:
                tried += [way]
            if len(tried) == 4:
                level[y][x] = 2
                if one not in [[y, x+1], [y, x-1], [y+1, x], [y-1, x]]:
                    return changef(level, columns, rows, elevator)
                y,x = one[0],one[1]
                tried = []
            else:
                way = random.choice([x for x in [1, 2, 3, 4] if x not in tried])
            change = False
def changef(level, columns, rows, elevator):
    level[elevator[0]][elevator[1]] = 16
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] not in [0, 16]:
                dirs = 0
                if j+1 < columns:
                    if level[i][j+1]:
                        dirs += 1
                if j-1 >= 0:
                    if level[i][j-1]:
                        dirs += 2
                if i+1 < rows:
                    if level[i+1][j]:
                        dirs += 4
                if i-1 >= 0:
                    if level[i-1][j]:
                        dirs += 8
                level[i][j] = dirs
    return level, elevator

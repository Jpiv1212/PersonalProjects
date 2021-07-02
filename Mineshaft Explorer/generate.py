import random
def generate(columns, rows, often, spawnx, spawny):
    level = [[0 for i in range(columns)] for i in range(rows)]
    level[spawny][spawnx] = 1
    elevator = [0, 0]
    while elevator == [0, 0]:
        elevator = [random.randint(0, rows-1), random.randint(0, columns-1)]
    level[elevator[0]][elevator[1]] = 16
    x = spawnx
    y = spawny
    way = 1
    while True:
        go = random.randint(1, often)
        if go == 1:
            way = random.randint(1, 4)
        if way == 1:
            if x+1 < columns:
                x += 1
            else:
                way = random.choice([2, 3, 4])
        elif way == 2:
            if x-1 >= 0:
                x -= 1
            else:
                way = random.choice([1, 3, 4])
        elif way == 3:
            if y+1 < rows:
                y += 1
            else:
                way = random.choice([1, 2, 4])
        elif way == 4:
            if y-1 >= 0:
                y -= 1
            else:
                way = random.choice([1, 2, 3])
        if level[y][x] == 16:
            return change(level, columns, rows),elevator
        else:
            level[y][x] = 1
def change(level, columns, rows):
    for i,row in enumerate(level):
        for j,column in enumerate(level[i]):
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
    return level

import pygame
import random
import heapq

pygame.init()
WIDTH, HEIGHT = 500, 500
GRID = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man AI Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
ORANGE = (255,165,0)
RED = (255,0,0)
WHITE = (255,255,255)

def carve(x,y,maze,rows):
    directions = [(2,0),(-2,0),(0,2),(0,-2)]
    random.shuffle(directions)
    for dx,dy in directions:
        nx, ny = x+dx, y+dy
        if 0 < nx < len(maze[0])-1 and 0 < ny < rows-1 and maze[ny][nx] == 1:
            maze[ny][nx] = 0
            maze[y + dy//2][x + dx//2] = 0
            carve(nx, ny, maze, rows)

def astar(start, target, maze):
    rows = len(maze)
    cols = 25

    def h(a, b):
        manhattan = abs(a[0]-b[0]) + abs(a[1]-b[1])
        noise = random.uniform(0, 0.5)
        return manhattan + noise

    open_set = []
    heapq.heappush(open_set, (h(start, target), 0, start))

    came_from = {}
    g_score = {tuple(start): 0}

    while open_set:
        _, g, current = heapq.heappop(open_set)

        if current == target:
            path = []
            cur = tuple(target)
            while cur != tuple(start):
                path.append(list(cur))
                cur = came_from[cur]
            path.reverse()
            return path

        x, y = current
        neighbors = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]

        for nx, ny in neighbors:
            if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 0:
                new_g = g + 1
                if (nx, ny) not in g_score or new_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = new_g
                    f = new_g + h([nx, ny], target)
                    heapq.heappush(open_set, (f, new_g, [nx, ny]))
                    came_from[(nx, ny)] = (x, y)

    return []


def generate(level):
    rows = 7 + (level - 1) * 3
    rows = min(rows, 20)

    maze = [[1]*25 for _ in range(rows)]
    maze[1][1] = 0

    carve(1, 1, maze, rows)

    for _ in range(20):
        x = random.randint(1, 23)
        y = random.randint(1, rows - 2)
        if maze[y][x] == 1:
            neighbors = [
            maze[y+1][x],
            maze[y-1][x],
            maze[y][x+1],
            maze[y][x-1]
            ]
            if 0 in neighbors:
                maze[y][x]=0

    return maze

def generatecoins(maze):
    coins = []
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 0 and random.random() < 0.2:
                coins.append([x,y])
    return coins

def generate_special_coins(maze):
    special = []
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 0 and random.random() < 0.05:
                special.append([x,y])
    return special

def generateghost(maze):
    while True:
        gx = random.randint(0,24)
        gy = random.randint(0,len(maze)-1)

        if maze[gy][gx] == 0:
            if gx != pacman[0] and gy != pacman[1]:
                
                distance = abs(gx - pacman[0]) + abs(gy - pacman[1])
                if distance > 6:
                    return [gx,gy]

def reset_game():
    global level, maze, coins,special_coins, pacman, ghost, score, speed, game_over
    level = 1
    maze = generate(level)
    coins = generatecoins(maze)
    special_coins = generate_special_coins(maze)
    pacman = [1,1]
    ghost = generateghost(maze)
    score = 0
    speed = 5 + level * 2
    game_over = False

level = 1
maze = generate(level)
coins = generatecoins(maze)
pacman = [1,1]
special_coins = generate_special_coins(maze)
blink_timer = 0
blink_state = True
ghost = generateghost(maze)
ghost_prev=None
ghost_delay = 2
ghost_timer=0
dx, dy = 0,0
score = 0
speed = 5 + level * 2
high_score = 0
game_over = False

running = True
while running:
    clock.tick(speed)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_UP]: dx,dy = 0,-1
        if keys[pygame.K_DOWN]: dx,dy = 0,1
        if keys[pygame.K_LEFT]: dx,dy = -1,0
        if keys[pygame.K_RIGHT]: dx,dy = 1,0

        newX = pacman[0] + dx
        newY = pacman[1] + dy
        if 0 <= newY < len(maze) and 0 <= newX < 25 and maze[newY][newX] == 0:
            pacman = [newX,newY]

        for c in coins[:]:
            if c == pacman:
                coins.remove(c)
                score += 1 * level
        for sc in special_coins[:]:
            if sc == pacman:
                special_coins.remove(sc)
                score += 5 * level

        if len(coins) <= 2:
            level += 1
            maze = generate(level)
            coins = generatecoins(maze)
            pacman = [1,1]
            ghost = generateghost(maze)
            special_coins = generate_special_coins(maze)
            speed = min(15, 5 + level * 2)

        
        ghost_timer += 1
        if ghost_timer >= ghost_delay:
            ghost_timer = 0

            distance = abs(ghost[0]-pacman[0]) + abs(ghost[1]-pacman[1])

            if distance < (6+level):
                if random.random() < 0.7:  
                    path = astar(ghost, pacman, maze)
                    if path:
                        ghost = path[0]
                else:
                    moves = [
                        [ghost[0]+1, ghost[1]],
                        [ghost[0]-1, ghost[1]],
                        [ghost[0], ghost[1]+1],
                        [ghost[0], ghost[1]-1]
                    ]

                    valid = [m for m in moves if 0 <= m[1] < len(maze) and 0 <= m[0] < 25 and maze[m[1]][m[0]] == 0]

                    if valid:
                        ghost = random.choice(valid)
            else:
                moves = [
                    [ghost[0]+1, ghost[1]],
                    [ghost[0]-1, ghost[1]],
                    [ghost[0], ghost[1]+1],
                    [ghost[0], ghost[1]-1]
                ]

                valid = [m for m in moves if 0 <= m[1] < len(maze) and 0 <= m[0] < 25 and maze[m[1]][m[0]] == 0]

                valid.sort(key=lambda m: abs(m[0]-pacman[0]) + abs(m[1]-pacman[1]))

                if random.random() < 0.7:
                    ghost = valid[0]
                else:
                    ghost = random.choice(valid)

            if pacman == ghost:
                game_over = True

    blink_timer += 1
    if blink_timer > 5:
        blink_timer = 0
        blink_state = not blink_state

    if pacman == ghost:
        game_over = True


    for y in range(len(maze)):
        for x in range(len(maze[y])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, BLUE, (x*GRID,y*GRID+50,GRID,GRID))

    for c in coins:
        pygame.draw.circle(screen, YELLOW, (c[0]*GRID+10,c[1]*GRID+10+50),3)

    center_x = pacman[0]*GRID + GRID//2
    center_y = pacman[1]*GRID + GRID//2 + 50

    pygame.draw.circle(screen, YELLOW, (center_x, center_y), GRID//2)

    gx = ghost[0]*GRID + GRID//2
    gy = ghost[1]*GRID + GRID//2 + 50
    pygame.draw.circle(screen, RED, (gx,gy), GRID//2)
    pygame.draw.circle(screen, WHITE, (gx-4,gy-3), 2)
    pygame.draw.circle(screen, WHITE, (gx+4,gy-3), 2)

    if blink_state:
        for c in special_coins:
            pygame.draw.circle(
                screen,
                WHITE,
                (c[0]*GRID + GRID//2, c[1]*GRID + GRID//2 + 50),
                5
            )

    pygame.draw.rect(screen,(30,30,30), (0,0,WIDTH,50))
    pygame.draw.line(screen, WHITE, (0,50), (WIDTH,50), 2)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10,10))
    screen.blit(level_text, (200,10))
    screen.blit(high_score_text, (370,10))

    if game_over:
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        level_text = font.render(f"Reached Level: {level}", True, WHITE)
        over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        if(high_score<score):
            high_score = score
        high_text=font.render("High Score: "+str(high_score), True, WHITE)

        screen.fill(BLACK)
        rect = score_text.get_rect(center=(WIDTH//2, (HEIGHT-80)//2))
        screen.blit(score_text, rect)
        rect = over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(over_text, rect)
        rect = level_text.get_rect(center=(WIDTH//2, (HEIGHT-40)//2))
        screen.blit(level_text, rect)
        rect=high_text.get_rect(center=(WIDTH//2, (HEIGHT+40)//2))
        screen.blit(high_text, rect)
        rect = restart_text.get_rect(center=(WIDTH//2, (HEIGHT+80)//2))
        screen.blit(restart_text, rect)

    pygame.display.update()

pygame.quit()

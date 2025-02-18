import pygame
import math

pygame.init()
WIDTH, HEIGHT = 1000, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("cats vs cats")

background1_img = pygame.image.load("bg2.png")
background1_img = pygame.transform.scale(background1_img, (WIDTH, HEIGHT))
background2_img = pygame.image.load("bg3.png")
background2_img = pygame.transform.scale(background2_img, (WIDTH, HEIGHT))
over_img = pygame.image.load("over.png")
over_scaled = pygame.transform.scale(over_img, (500, 320))
win_img = pygame.image.load("win.png")
win_scaled = pygame.transform.scale(win_img, (500, 320))

fireball_img = pygame.image.load("fire.png")
fireball2_img = pygame.image.load("fire3.png")
fireball3_img = pygame.image.load("fire2.png")
fireball_size = (90, 90)
fireball_scaled = pygame.transform.scale(fireball_img, fireball_size)
fireball2_scaled = pygame.transform.scale(fireball2_img, fireball_size)
fireball3_scaled = pygame.transform.scale(fireball3_img, fireball_size)
fireball_speed = 15
fireball_range = 300 

hero_img = pygame.image.load("hero.png")
hero_size = (200,200)
hero_scaled = pygame.transform.scale(hero_img, hero_size)
fireball_hero= None
hero_x = 100
hero_y = 220
hero_speed = 15
hero_health = 5
jump_speed = 30

villain_size = (200, 200)
villain_fireball_range = 500

villain1_img = pygame.image.load("villain2.png")
villain1_scaled = pygame.transform.scale(villain1_img, villain_size)

pygame.mixer.music.load("bg_music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

s = pygame.mixer.Sound("crash.mp3")

villain1_x = 800
villain1_y = 220
villain1_speed = 15
villain1_health=6
fireballs_villain = []
villain1_fire_rate = 25 
villain_timer = 0

villain2_x = 800
villain2_y = 220
villain2_img = pygame.image.load("villain1.png")
villain2_scaled = pygame.transform.scale(villain2_img, villain_size)
villain2_speed = 15
villain2_health=8

health_img=pygame.image.load("heart.png")
health_size=(45,45)
health_scaled = pygame.transform.scale(health_img, health_size)

WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
font = pygame.font.Font(None, 60)

def show_menu():
    menu = True
    button_1 = pygame.Rect(350, 270, 300, 80)
    button_2 = pygame.Rect(350, 420, 300, 80)

    while menu:
        screen.blit(background2_img, (0, 0))
        
        pygame.draw.rect(screen, WHITE, button_1, border_radius=10)
        level1_text = font.render("Уровень 1", True, BLUE)
        screen.blit(level1_text, (button_1.x + 40, button_1.y + 20))

        pygame.draw.rect(screen, WHITE, button_2, border_radius=10)
        level2_text = font.render("Уровень 2", True, BLUE)
        screen.blit(level2_text, (button_2.x + 40, button_2.y + 20))
    
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_1.collidepoint(event.pos):
                    return 1
                elif button_2.collidepoint(event.pos):
                    return 2  
                
def show_game_over(img):
    darken_surface = pygame.Surface((WIDTH, HEIGHT)) 
    darken_surface.fill((0, 0, 0))
    darken_surface.set_alpha(150)
    screen.blit(darken_surface, (0, 0))
    screen.blit(img, (250, 160))
    pygame.display.flip() 
    pygame.time.delay(2000)  

def draw_health(health, x,y):
    for i in range(health):
        screen.blit(health_scaled, (x + i * health_size[0] , y))

def draw_fireballs_villain2():
    for fireball in fireballs_villain[:]:
        fireball["y"] += math.sin(fireball["distance"] * 0.05) * 15 
        fireball["distance"] += fireball_speed  
        fireball["x"] -= fireball_speed  
        if fireball["distance"] > villain_fireball_range:
            fireballs_villain.remove(fireball)
        else:
            screen.blit(fireball3_scaled, (fireball["x"], fireball["y"]))

def move_hero(hero_x, hero_y):
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        hero_x -= hero_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]: 
        hero_x += hero_speed
    if keys[pygame.K_UP] or keys[pygame.K_w]:
       hero_y -= hero_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]: 
         hero_y += hero_speed

    if keys[pygame.K_SPACE]:
        hero_y -= jump_speed

    hero_x = max(0, min(WIDTH - hero_size[0], hero_x))
    hero_y = max(0, min(HEIGHT - hero_size[1], hero_y))

    return hero_x, hero_y

def move_villain1(hero_y, villain1_y):
    if villain1_y < hero_y:
        villain1_y += min(villain1_speed, hero_y - villain1_y)  
    elif villain1_y > hero_y:
        villain1_y -= min(villain1_speed, villain1_y - hero_y)

    return villain1_y

def move_villain2(hero_y, villain2_y, villain2_x, hero_x):
    distance_x = abs(hero_x - villain2_x) 

    if villain2_y < hero_y:
        villain2_y += min(villain2_speed, hero_y - villain2_y)  
    elif villain2_y > hero_y:
        villain2_y -= min(villain2_speed, villain2_y - hero_y)

    villain2_y = max(0, min(HEIGHT - villain_size[1], villain2_y))
    if distance_x > 500:
        villain2_x -= villain2_speed * 1.5
    if distance_x < 300:
        villain2_x += villain2_speed * 1.5

    villain2_x = max(0, min(WIDTH - villain_size[0], villain2_x))

    return villain2_y, villain2_x

def attack_villain(villain_x, villain_y, villain_size):
    fireballs_villain.append({"x": villain_x, "y": villain_y + villain_size[1] // 2,"distance": 0})

def attack(hero_x, hero_y):
    global fireball_hero
    if fireball_hero is None: 
        fireball_hero = {"x": hero_x + hero_size[0] // 2, "y": hero_y + hero_size[1] // 2, "distance": 0}
        

def collision(victim_x, victim_y, victim_size, fireballs):
    victim_rect = pygame.Rect(victim_x+30, victim_y+30, victim_size[0]-60, victim_size[1]-60)
    for fireball in fireballs[:]:
        fireball_rect = pygame.Rect(fireball["x"]+20, fireball["y"]+20, fireball_size[0]-25, fireball_size[1]-25)
        if victim_rect.colliderect(fireball_rect):
            fireballs.remove(fireball)
            s.play()
            return True
    return False

def draw_fireballs_villain():
    for fireball in fireballs_villain[:]:  
        fireball["x"] -= fireball_speed  
        fireball["distance"] += fireball_speed  

        if fireball["distance"] > villain_fireball_range:  
            fireballs_villain.remove(fireball)  
        else:
            screen.blit(fireball2_scaled, (fireball["x"], fireball["y"]))

def draw_fireball_hero():
    global fireball_hero 

    if fireball_hero:
        fireball_hero["x"] += fireball_speed 
        fireball_hero["distance"] += fireball_speed

        if fireball_hero["distance"] > fireball_range:  
            fireball_hero = None  
        else:
            screen.blit(fireball_scaled, (fireball_hero["x"], fireball_hero["y"]))

def run_level1(hero_x, hero_y, hero_health, villain_health, villain1_y): 
    running = True
    global fireball_hero
    global villain_timer
    fireballs_villain.clear()
    fireball_hero=None
    
    while running:
        screen.blit(background2_img, (0, 0))
        screen.blit(hero_scaled, (hero_x, hero_y)) 
        screen.blit(villain1_scaled, (villain1_x, villain1_y)) 
        
        if collision(hero_x, hero_y, hero_size, fireballs_villain):
            hero_health -= 1
            if hero_health <= 0:
                show_game_over(over_scaled)
                villain_timer = 0
                fireball_hero=None
                running = False

        if fireball_hero and collision(villain1_x, villain1_y, villain_size, [fireball_hero]):
            villain_health -= 1
            fireball_hero = None 
            if villain_health <= 0:
                show_game_over(win_scaled)
                villain_timer = 0
                fireball_hero=None
                running = False

        draw_health(hero_health, 10,10)
        draw_health(villain_health, WIDTH - (villain_health * health_size[0]) - 10,10)
    
        villain1_y = move_villain1(hero_y, villain1_y)

        villain_timer += 1
        if villain_timer >= villain1_fire_rate:
            attack_villain(villain1_x, villain1_y, villain_size)
            villain_timer = 0

        draw_fireballs_villain()
        draw_fireball_hero()

        pygame.display.flip() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    attack(hero_x, hero_y)

        hero_x, hero_y = move_hero(hero_x, hero_y) 

        pygame.time.delay(30)


def run_level2(hero_x, hero_y,hero_health, villain_health, villain2_y, villain2_x):
    running = True
    global fireball_hero
    global villain_timer
    fireballs_villain.clear()
    fireball_hero=None

    while running:
        screen.blit(background1_img, (0, 0))
        screen.blit(hero_scaled, (hero_x, hero_y)) 
        screen.blit(villain2_scaled, (villain2_x, villain2_y)) 
    
        if collision(hero_x, hero_y, hero_size, fireballs_villain):
            hero_health -= 1
            if hero_health <= 0:
                villain_timer = 0
                fireball_hero=None
                show_game_over(over_scaled)
                running = False

        if fireball_hero and collision(villain2_x, villain2_y, villain_size, [fireball_hero]):
            villain_health -= 1
            fireball_hero = None 
            if villain_health <= 0:
                villain_timer = 0
                fireball_hero=None
                show_game_over(win_scaled)
                running = False

        draw_health(hero_health,10,10)
        draw_health(villain2_health, WIDTH - (villain_health * health_size[0]) - 10,10)
        
        villain2_y, villain2_x = move_villain2(hero_y, villain2_y, villain2_x, hero_x)
        
        draw_fireball_hero()
        draw_fireballs_villain2() 

        villain_timer += 1
        if villain_timer >= villain1_fire_rate:
            attack_villain(villain2_x, villain2_y, villain_size)
            villain_timer = 0

        pygame.display.flip() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    attack(hero_x, hero_y)

        hero_x, hero_y = move_hero(hero_x, hero_y) 
        pygame.time.delay(30)


while True:
    level = show_menu()
    if level == 1:
        run_level1(hero_x, hero_y, hero_health, villain1_health, villain1_y) 
    elif level == 2:
        run_level2(hero_x, hero_y,hero_health,villain2_health,villain2_y, villain2_x)


import pygame
import random
import os
import sys
import Assets.Particle_Engine as PE


""" ----------------------------------------------------------------
Things to add:

    - Fix entity positions when game restarted

    ?- Add player dash when shift is pressed
    ?- Add particle for aarrecar when shooting

    - After every 25 kills u get + 1 bullet at once
        - stacks only for 5
        - goes back to 1 if health goes down
    - after a while enemies go faster

    - add top highscore to startmenu

 ---------------------------------------------------------------- """

WIDTH = 700
HEIGHT = 500
pygame.init()
pygame.display.set_caption("PP SHOOTER")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bg = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "game_background.png"))
bg_x = 0
radius_random_x = random.randint(7, 10)
radius_random_y = random.randint(10, 14)
radius_enemy_x = random.randint(15, 19)
radius_enemy_y = random.randint(19, 23)

# Colorkeys
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (200, 0, 120)

# Player
player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
player_img.convert()
player_img.set_colorkey(WHITE)
player_hurt_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player_hurt.png"))
player_hurt_img.convert()
player_hurt_img.set_colorkey(WHITE)
player_heart_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "heart.png"))
player_heart_img.convert()

# Enemy
Woman = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "enemy.png"))
Woman.convert()
Woman.set_colorkey(WHITE)

# Pregenant Enemy
PregWoman = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Pregeny.png"))
PregWoman.convert()
PregWoman.set_colorkey(WHITE)

# Baby
Babyimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Pregeny_bullet.png"))
Babyimg.convert()
Babyimg.set_colorkey(WHITE)

# Aarre car
Aarrecarimg = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "Aarrecar.png"))
Aarrecarimg.convert()
Aarrecarimg.set_colorkey(WHITE)

# Text
font = pygame.font.SysFont(None, 25)
outline_font = pygame.font.SysFont('freesansbold.ttf', 25)
health_text = font.render("", True, (50, 50, 50))
health_text_outline = outline_font.render("", True, WHITE)

# Score
game_score = 0
game_score_text = font.render("", True, (50, 255, 50))
game_score_text_outline = outline_font.render("", True, WHITE)

# Timer
current_time = 0
collision_time = 0


# Game start --------------------------------------------------------------------------------
start = False
startfont = pygame.font.SysFont("Sans-serif", 60)
starttext = startfont.render("", True, (0, 0, 0))
startgamefont = pygame.font.SysFont("Sans-serif", 40)
startgametext = startfont.render("", True, (0, 0, 0))
# Gui
startgui = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "gui", "startmenugui.png"))
startgui.set_colorkey(WHITE)
startgui.set_alpha(150) # 0 fully transparent and 255 fully opaque
# Game start --------------------------------------------------------------------------------

# Game version
game_version = "0.3"
versionfont = pygame.font.SysFont(None, 30)
version = versionfont.render("", True, (0, 0, 0))

# Game over ---------------------------------------------------------------------------------
gameover = False
# Game over text
overfont = pygame.font.SysFont(None, 60)
yourded = overfont.render("", True, (255, 50, 50))
# Game over score text
overscorefont = pygame.font.SysFont(None, 40)
overscore = overscorefont.render("", True, (0, 0, 0))
overhighscore = overscorefont.render("", True, (0, 0, 0))
# Highscore
game_highscore = 0
# Restart text and font
restartfont = pygame.font.SysFont(None, 30)
restarttext = restartfont.render("", True, (0, 0, 0))
newhighscoretext = restartfont.render("", True, (0, 0, 0))
# GUI
gameovergui = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "gui", "gameovergui.png"))
gameovergui.set_colorkey(WHITE)
gameovergui.set_alpha(150) # 0 fully transparent and 255 fully opaque
# Game over ---------------------------------------------------------------------------------


class Bullet(object):
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.height = 4
        self.width = 70
        self.color = PINK
        self.facing = facing
        self.vel = 8 * facing
        # self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
    
    def draw(self, screen):
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(screen, self.color, self.rect)


class Player:
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()

        # pos and direction
        self.pos = [100, 250]
        self.health = 5
        self.vel = 8
        self.acc = 0

        self.direction = "RIGHT"
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False

    def move(self):
        self.acc = 0

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            # self.direction = "LEFT"
            self.pos[0] -= self.vel + 0.5 * self.acc
            self.move_left = True
        else:
            self.move_left = False
        if keys_pressed[pygame.K_d]:
            self.direction = "RIGHT"
            self.pos[0] += self.vel + 0.5 * self.acc
            self.move_right = True
        else:
            self.move_right = False
        if keys_pressed[pygame.K_w]:
            self.pos[1] -= self.vel + 0.5 * self.acc
            self.move_down = True
        else:
            self.move_down = False
        if keys_pressed[pygame.K_s]:
            self.pos[1] += self.vel + 0.5 * self.acc
            self.move_up = True
        else:
            self.move_up = False

        if self.pos[0] < 40:
            self.pos[0] += self.vel
        elif self.pos[0] > 660:
            self.pos[0] -= self.vel
        if self.pos[1] < 40:
            self.pos[1] += self.vel
        elif self.pos[1] > 450:
            self.pos[1] -= self.vel

        self.rect.midbottom = self.pos

        if self.move_right == True:
            self.vel += self.acc
        if self.move_left == True:
            self.vel += self.acc
        if self.move_up == True:
            self.vel += self.acc
        if self.move_down == True:
            self.vel += self.acc

    def update(self):
        if self.direction == "RIGHT":
            self.image = player_img
        elif self.direction == "LEFT":
            self.image = pygame.transform.flip(player_img, True, False)
            self.image.set_colorkey(WHITE)


class Enemy(object):
    def __init__(self):
        self.image = Woman
        self.rect = self.image.get_rect()
        
        self.pos = [800, random.randint(100, 400)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.midbottom = self.pos


class PregEnemy(object):
    def __init__(self):
        self.image = PregWoman
        self.rect = self.image.get_rect()
        
        self.pos = [800, random.randint(100, 400)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.midbottom = self.pos


class Baby(object):
    def __init__(self, x, y):
        self.image = Babyimg
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.midbottom = (self.x, self.y)


class AarreCar(object):
    def __init__(self, x):
        self.image = Aarrecarimg
        self.rect = self.image.get_rect()

        self.x = x
        self.y = 500
        self.vel = 6
        self.control = False
        self.move_right = False 
        self.move_left = False
        self.direction = "RIGHT"

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.rect.midbottom = (self.x, self.y)

    def move(self):
        if self.control == False:
            if self.move_right == True:
                self.x += self.vel  
            elif self.move_left == True:
                self.x -= self.vel
            if self.x < 10:
                self.move_right = True
                self.move_left = False
            elif self.x > 680:
                self.move_right = False
                self.move_left = True

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RCTRL]:
            self.control = True

        if self.control == True:
            self.move_right = False
            self.move_left = False
            if keys_pressed[pygame.K_LEFT]:
                self.x -= self.vel
                self.direction = "LEFT"
            elif keys_pressed[pygame.K_RIGHT]:
                self.x += self.vel
                self.direction = "RIGHT"

        # Direction
        if self.move_right == True:
            self.direction = "RIGHT"
        if self.move_left == True:
            self.direction = "LEFT"

    def update(self):
        if self.direction == "LEFT":
            self.image = Aarrecarimg
        elif self.direction == "RIGHT":
            self.image = pygame.transform.flip(Aarrecarimg, True, False)
            self.image.set_colorkey(WHITE)


class AarreBullet(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 10
        self.color = BLACK
        self.vel = 12

    def draw(self, screen):
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        pygame.draw.rect(screen, self.color, self.rect)


def draw_window():
    # screen.fill((177, 177, 177))
    # screen.blit(bg, (bg_x, 0))

    # Player render, movement, direction, health
    player.update()
    player.move()
    screen.blit(player.image, player.rect)
    screen.blit(health_text_outline, (50, 20))
    screen.blit(health_text, (50, 20))
    screen.blit(player_heart_img, (15, 15))

    # Aarre Car
    aarrecar.update()
    aarrecar.move()
    aarrecar.draw(screen)

    # Enemy
    for enemy in enemies:
        enemy.draw(screen)

    # PregEnemy
    for pregenemy in pregenemies:
        pregenemy.draw(screen)

    # Baby draw
    for baby in babies:
        baby.draw(screen)

    # Bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    for aarrebullet in aarrebullets:
        aarrebullet.draw(screen)

    # Score
    screen.blit(game_score_text_outline, (WIDTH//2 - 40, 20))
    screen.blit(game_score_text, (WIDTH//2 - 40, 20))

def gameisover():
    # Gui
    screen.blit(gameovergui, (100, 15))
    # Score
    screen.blit(overscore, (WIDTH//2 - 140, 160))
    # Highscore and New Highscore
    screen.blit(overhighscore, (WIDTH//2 - 180, 220))
    screen.blit(newhighscoretext, (WIDTH//2 - 70, 280))
    # you died text
    screen.blit(yourded, (WIDTH//2 - 120, 40))
    # Restart text
    screen.blit(restarttext, (WIDTH//2 - 170, 400))

def startmenu():
    # Player
    screen.blit(player.image, (player.pos[0] - 40, player.pos[1] - 40))
    # Gui
    screen.blit(startgui, (100, 15))
    # Start text
    screen.blit(starttext, (WIDTH//2 - 120, 40))
    screen.blit(startgametext, (WIDTH//2 - 200, 400))

# Player
player = Player()
# Aarre Car
aarrecar = AarreCar(-5)
# Enemies
enemies = []
pregenemies = []
babies = []
# Bullet
bullets = []
aarrebullets = []
# Particle groups
playerparticle = PE.CreateParticle(screen, 0.35, radius_random_x, radius_random_y, 0.1)
playerhurtparticle = PE.CreateParticle(screen, 0.3, radius_random_x, radius_random_y, 0.1)
enemyparticle = PE.CreateParticle(screen, 0.5, radius_enemy_x, radius_enemy_y, 0.05)
# Particle Events
PARTICLE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(PARTICLE_EVENT, 40)

run = True
while run:
    current_time = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    bg_x += -2
    screen.blit(bg, (bg_x, 0))
    screen.blit(version, (0, HEIGHT - 25))
    version = versionfont.render("Version: " + game_version, True, (22, 219, 219))
    if player.health < 1:
        gameover = True
    if bg_x < -1400:
        bg_x = 0
    if start == True:
        if gameover == False:
            draw_window()

            for enemy in enemies:
                for pregenemy in pregenemies:
                    if enemy.pos[0] == pregenemy.pos[0]:
                        enemy.pos[0] + 3
            
            # Health
            #print(player.health)
            health_text = font.render(": " + str(player.health), True, (255, 50, 50))
            health_text_outline = outline_font.render(": " + str(player.health), True, WHITE)
            # if player.health == 0:
                # run = False

            # Score
            game_score_text = font.render("Score : " + str(game_score), True, (50, 255, 50))
            game_score_text_outline = outline_font.render("Score : " + str(game_score), True, WHITE)

            # Enemies
            for enemy in enemies:
                if enemy.rect.colliderect(player.rect):
                    enemies.pop(enemies.index(enemy))
                    collision_time = pygame.time.get_ticks()
                    player.health -= 1
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    player_img = player_hurt_img
                    
                if current_time - collision_time > 1000:
                    player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                    player_img.convert()
                    player_img.set_colorkey(WHITE)
                # print(f"current time: {current_time} collision time: {collision_time}")

                if enemy.pos[0] < 0:
                    player.health -= 1
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    player_img = player_hurt_img
                    if current_time - collision_time > 1000:
                        player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                        player_img.convert()
                        player_img.set_colorkey(WHITE)

                if enemy.pos[0] < 900 and enemy.pos[0] > 0:
                    enemy.pos[0] -= 3
                else:
                    enemies.pop(enemies.index(enemy))
                    enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                    enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                    collision_time = pygame.time.get_ticks()

            for pregenemy in pregenemies:
                if pregenemy.rect.colliderect(player.rect):
                    pregenemies.pop(pregenemies.index(pregenemy))
                    enemyparticle.add_particles(pregenemy.pos[0], pregenemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                    collision_time2 = pygame.time.get_ticks()
                    player.health -= 1
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    player_img = player_hurt_img

                if current_time - collision_time > 1000:
                    player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                    player_img.convert()
                    player_img.set_colorkey(WHITE)
                
                if pregenemy.pos[0] < 900 and pregenemy.pos[0] > 0:
                    pregenemy.pos[0] -= 3
                else:
                    pregenemies.pop(pregenemies.index(pregenemy))
                    enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                    player.health -= 1
                    player_img = player_hurt_img
                    collision_time = pygame.time.get_ticks()

            for baby in babies:
                if baby.rect.colliderect(player.rect):
                    babies.pop(babies.index(baby))
                    collision_time2 = pygame.time.get_ticks()
                    player.health -= 1
                    player_img = player_hurt_img
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                    playerhurtparticle.add_particles(player.pos[0], player.pos[1] - 20, random.randint(-5, 5), random.randint(-3, 3))
                
                if current_time - collision_time > 1000:
                    player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                    player_img.convert()
                    player_img.set_colorkey(WHITE)

                if baby.x < 900 and baby.x > 0:
                    baby.x -= 6
                else:
                    babies.pop(babies.index(baby))

            if len(enemies) < 3:
                    enemies.append(Enemy())

            if len(pregenemies) < 1:
                pregenemies.append(PregEnemy())

            # Bullets
            for bullet in bullets:
                for pregenemy in pregenemies:
                    if bullet.rect.colliderect(pregenemy.rect):
                        pregenemies.pop(pregenemies.index(pregenemy))
                        game_score += 1
                        enemyparticle.add_particles(pregenemy.pos[0], pregenemy.pos[1], random.randint(0, 5), random.randint(0, 3))
                        enemyparticle.add_particles(pregenemy.pos[0], pregenemy.pos[1], random.randint(0, 5), random.randint(0, 3))
                #for baby in babies:
                    #if bullet.rect.colliderect(pregenemy.rect):
                        babies.append(Baby(pregenemy.pos[0], pregenemy.pos[1]))
                        try:
                            bullets.pop(bullets.index(bullet))
                        except:
                            pass

                for enemy in enemies:
                    if bullet.rect.colliderect(enemy.rect):
                        enemies.pop(enemies.index(enemy))
                        enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                        enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                        try:
                            bullets.pop(bullets.index(bullet))
                        except:
                            pass
                        game_score += 1
                if bullet.x < 700 and bullet.x > 0:
                    bullet.x += bullet.vel # Moves the bullet by it's vel
                else:
                    try:
                        bullets.pop(bullets.index(bullet)) # This will remove the bullet if it's off screen
                    except:
                        pass

            for aarrebullet in aarrebullets:
                if player.rect.colliderect(aarrebullet.rect):
                    player.health -= 1
                    player_img = player_hurt_img
                    if current_time - collision_time > 1000:
                        player_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                        player_img.convert()
                        player_img.set_colorkey(WHITE)
                    try:
                        aarrebullets.pop(aarrebullets.index(aarrebullet))
                    except:
                        pass

                for pregenemy in pregenemies:
                    if aarrebullet.rect.colliderect(pregenemy.rect):
                        pregenemies.pop(pregenemies.index(pregenemy))
                        enemyparticle.add_particles(pregenemy.pos[0], pregenemy.pos[1], random.randint(0, 5), random.randint(0, 3))
                        enemyparticle.add_particles(pregenemy.pos[0], pregenemy.pos[1], random.randint(0, 5), random.randint(0, 3))
                        babies.append(Baby(pregenemy.pos[0], pregenemy.pos[1]))
                        try:
                            aarrebullets.pop(aarrebullets.index(aarrebullet))
                        except:
                            pass

                for enemy in enemies:
                    if aarrebullet.rect.colliderect(enemy.rect):
                        enemies.pop(enemies.index(enemy))
                        enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                        enemyparticle.add_particles(enemy.pos[0], enemy.pos[1], random.randint(-5, 5), random.randint(-3, 3))
                        try:
                            aarrebullets.pop(aarrebullets.index(aarrebullet))
                        except:
                            pass
                if aarrebullet.y < HEIGHT + 50 and aarrebullet.y > -10:
                    aarrebullet.y -= aarrebullet.vel
                else:
                    try:
                        aarrebullets.pop(aarrebullets.index(aarrebullet)) # Will remove the car bullet if it's off screen
                    except:
                        pass


            # pygame Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # Particle Testing
                # if enemypop == True:
                    # enemypop_time = pygame.time.get_ticks()
                    # if event.type == PARTICLE_EVENT:
                        # enemyparticle.add_particles(enemy.pos[0], enemy.pos[1])
                    # elif current_time - enemypop_time > 1000:
                        # enemypop = False
                # Particle Testing

                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_SPACE]:
                        # if player.direction == "LEFT":
                            # facing = -1
                            # bonus = -35
                        if player.direction == "RIGHT":
                            facing = 1
                            bonus = 30
                        if len(bullets) < 5:
                            bullets.append(Bullet(player.pos[0]+bonus, player.pos[1]-22, facing))
                            playerparticle.add_particles(player.pos[0] + 47, player.pos[1] - 20, 3, random.randint(-3, 3))
                            playerparticle.add_particles(player.pos[0] + 47, player.pos[1] - 20, 3, random.randint(-3, 3))
                            playerparticle.add_particles(player.pos[0] + 47, player.pos[1] - 20, 3, random.randint(-3, 3))

                    if keys_pressed[pygame.K_UP]:
                        if len(aarrebullets) < 5:
                            aarrebullets.append(AarreBullet(aarrecar.x, aarrecar.y - 40))

    if start == False:
        startmenu()

        # Start text render
        starttext = startfont.render("Start Menu", True, (95, 150, 8))
        startgametext = startfont.render("Press Enter to Start", True, (20, 144, 191))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_RETURN]:
                    start = True

    elif gameover == True:
        gameisover()
        if game_score > game_highscore:
            newhighscoretext = restartfont.render("New Highscore", True, (200, 200, 200))
            newhighscoretext.set_alpha(255)
            game_highscore = game_score
        elif game_score < game_highscore:
            newhighscoretext.set_alpha(0)

        # pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Restart game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed(num_buttons=3):
                    # Resets everything back to default
                    gameover = False
                    start = False
                    player.pos = [100, 250]
                    player.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                    player.image.convert()
                    player.image.set_colorkey(WHITE)
                    player.health = 5
                    game_score = 0

                if event.type == pygame.KEYDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    if keys_pressed[pygame.K_RETURN]:
                        # Resets everything back to default
                        gameover = False
                    start = False
                    player.pos = [100, 250]
                    player.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Assets", "player.png"))
                    player.image.convert()
                    player.image.set_colorkey(WHITE)
                    player.health = 5
                    game_score = 0
                    
        
        # Game over text render
        overscore = overfont.render("Your Score: " + str(game_score), True, (255, 150, 50))
        overhighscore = overfont.render("Your High Score: " + str(game_highscore), True, (255, 150, 50))
        yourded = overfont.render("GAME OVER", True, (255, 50, 50))
        restarttext = restartfont.render("Click anywhere to restart the game", True, (WHITE))

    enemyparticle.emit((255,201,158))
    playerparticle.emit(PINK)
    playerhurtparticle.emit((166,16,30))
    pygame.display.update()
    clock.tick(60)
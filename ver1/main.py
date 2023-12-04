import pygame
import os
import random
pygame.init()

# Create Font Object
font = pygame.font.Font(None,36)

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("Assets/Cat", "CatRun1.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatRun2.png"))]
JUMPING = pygame.image.load(os.path.join("Assets/Cat", "CatJump.png"))
DUCKING = [pygame.image.load(os.path.join("Assets/Cat", "CatDuck1.png")),
           pygame.image.load(os.path.join("Assets/Cat", "CatDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("Assets/Bird", "Bird2.png"))]

# Add DOG obstacle IMG 4
DOG = [pygame.image.load(os.path.join("Assets/Dog", "Dog1.png")),
       pygame.image.load(os.path.join("Assets/Dog", "Dog2.png")),
       pygame.image.load(os.path.join("Assets/Dog", "Dog3.png")),
       pygame.image.load(os.path.join("Assets/Dog", "Dog4.png"))]
# Add BANANA obstacle IMG 3
BANANA = [pygame.image.load(os.path.join("Assets/Banana", "Banana1.png")),
          pygame.image.load(os.path.join("Assets/Banana", "Banana2.png")),
          pygame.image.load(os.path.join("Assets/Banana", "Banana3.png"))]
CHASER =[pygame.image.load(os.path.join("Assets/Chaser", "Chaser1.png")),
         pygame.image.load(os.path.join("Assets/Chaser", "Chaser2.png"))]

CLOUD = pygame.image.load(os.path.join("Assets/Other", "Cloud.png"))
BG = pygame.image.load(os.path.join("Assets/Other", "Track.png"))

class Cat:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.Cat_duck = False
        self.Cat_run = True
        self.Cat_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.Cat_rect = self.image.get_rect()
        self.Cat_rect.x = self.X_POS
        self.Cat_rect.y = self.Y_POS

    def update(self, userInput):
        if self.Cat_duck:
            self.duck()
        if self.Cat_run:
            self.run()
        if self.Cat_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.Cat_jump:
            self.Cat_duck = False
            self.Cat_run = False
            self.Cat_jump = True
        elif userInput[pygame.K_DOWN] and not self.Cat_jump:
            self.Cat_duck = True
            self.Cat_run = False
            self.Cat_jump = False
        elif not (self.Cat_jump or userInput[pygame.K_DOWN]):
            self.Cat_duck = False
            self.Cat_run = True
            self.Cat_jump = False

## Press Q or ENTER to end
        if userInput[pygame.K_q] or userInput[pygame.K_RETURN]:
            pygame.quit()
            quit()

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.Cat_rect = self.image.get_rect()
        self.Cat_rect.x = self.X_POS
        self.Cat_rect.y = self.Y_POS_DUCK
        self.step_index += 1
    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.Cat_rect = self.image.get_rect()
        self.Cat_rect.x = self.X_POS
        self.Cat_rect.y = self.Y_POS
        self.step_index += 1
    def jump(self):
        self.image = self.jump_img
        if self.Cat_jump:
            self.Cat_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.Cat_jump = False
            self.jump_vel = self.JUMP_VEL
    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.Cat_rect.x, self.Cat_rect.y))
# Add Chaser
class Chaser:
    def __init__(self, image):
        self.images = image
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = 310
        self.index = 0
        self.speed = 0

    def update(self):
        if self.index >= 10:
            self.index = 0
        self.image = self.images[self.index // 5]
        self.index += 1
        self.rect.x -= self.speed
        # Reset Chaser Position & Speed
        if self.rect.x < -self.rect.width:
            self.speed = 0
            self.rect.x = SCREEN_WIDTH

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1
# Add Obstacle Dog
class Dog(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325
        self.motion_index = 0
        self.direction = 1
        self.speed = 2

    def update(self):
        global points 
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()
            points -= 50  # lose 50 pts

        self.rect.x += self.speed * self.direction

        if self.motion_index >= 15:
            self.motion_index = 0
            self.direction *= -1

        if self.direction == 1:
            self.image = self.image[self.motion_index // 5]  # When it move left > Dog1, Dog2
        # Dog List // 5 -> return 0 or 1  >> [Dog1.png, Dog2.png ...] 
            # IF YOU WANT TO CHANGE, CHANGE LIST ORDER
        else:
            self.image = self.image[self.motion_index // 5 + 2]  # When it move right > Dog3, Dog4

        self.motion_index += 1
# Add Obstacle Banana
class Banana(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325



def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, highest_points
    run = True
    clock = pygame.time.Clock()
    player = Cat()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    # Save HIGHTEST pts
    high_score = 0

    # Chaser System
    chaser = Chaser(CHASER)
    chaser_start_time = None
    chaser_end_time = None
    chaser_hit_count = 0

    def score():
        global points, game_speed, highest_points
        points += 1
        if points % 100 == 0:
            game_speed += 1

        ## Give Churu when pts get 500
        # if points % 500 == 0:
            # Give Churu

        # Update HIGHTEST pts
        if points > highest_points:
            highest_points = points

        text = font.render("Points: " + str(points), True, (0, 0, 0))

        textRect = text.get_rect()
        textRect.center = (1000, 40)
        SCREEN.blit(text, textRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255, 255, 255))

        userInput = pygame.key.get_pressed()

        player.draw(SCREEN)
        player.update(userInput)

        # Show Highest pts
        hp_text = font.render("Highest Point: " + str(highest_points), True, (0, 0, 0))
        SCREEN.blit(hp_text, (886, 55))

        # Add Dog obstacle
        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
            elif random.randint(0, 2) == 3:
                obstacles.append(Dog(DOG))
            elif random.randint(0, 2) == 4:
                obstacles.append(Banana(BANANA))

        for obstacle in obstacles:
            obstacle.draw(SCREEN)
            obstacle.update()
            if player.Cat_rect.colliderect(obstacle.rect):
                # Check if obstacle is a Dog
                if isinstance(obstacle, Dog):
                    points -= 50        # Lose 50 pts
                    obstacles.remove(obstacle)  # Remove DOG in obstacle list >> DIFFERENT Condition
                if isinstance(obstacle, Banana):
                # Check if obstacle is a Banana > Chaser system
                    if chaser_start_time is None or pygame.time.get_ticks() - chaser_start_time > 7000:
                        chaser_start_time = pygame.time.get_ticks()
                        chaser_end_time = chaser_start_time + 7000
                        chaser.speed = 2
                        chaser.rect.x = 0
                    else:
                        chaser_hit_count += 1
                        if chaser_hit_count == 2:   # Plater hit Banana twice in 7 sec
                            pygame.time.delay(2000)
                            death_count += 1
                            menu(death_count)
                else:
                    pygame.time.delay(2000)
                    death_count += 1
                    menu(death_count)

        background()

        cloud.draw(SCREEN)
        cloud.update()

        # Chaser's Rogic , Check if it is activation or not
        # ???? NEED MORE CHECK TO ADD
        if chaser_start_time is not None:
            if pygame.time.get_ticks() < chaser_end_time:
                chaser.speed += 0.01
            else:
                chaser.speed -= 0.01    # Change chaser's speed to negative
            chaser.update()
            chaser.draw(SCREEN)

        score()

        clock.tick(30)
        pygame.display.update()

def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()
menu(death_count=0)
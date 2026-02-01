import pygame
import os
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("DragonHunter")
background_img = pygame.image.load('images/background/default.png').convert_alpha()
original_width, original_height = background_img.get_size()
new_width = original_width * 4
new_height = original_height * 4
new_size = (new_width, new_height)
new_bg = pygame.transform.scale(background_img, new_size)
floor_img = pygame.image.load('images/tiles/floor.png').convert_alpha()
original_floor_width, original_floor_height = floor_img.get_size()
new_floor_width = original_floor_width * 4
new_floor_height = original_floor_height * 4
new_floor_size = (new_floor_width, new_floor_height)
new_floor = pygame.transform.scale(floor_img, new_floor_size)

health_bar_img = pygame.image.load('images/healthbar.png').convert_alpha()
damage_bar_img = pygame.image.load('images/damage.png').convert_alpha()

damage_bar_img = pygame.transform.scale(damage_bar_img, (100, 20))
health_bar_img = pygame.transform.scale(health_bar_img, (100, 20))

# floor_img & background_img

GRAVITY = 0.75
SCROLL_THRESH = 200
screen_scroll = 0
floor_scroll = 0
bg_scroll = 0

moving_left = False
moving_right = False

tile_width = 32
floor_y = 700

FPS = 60

def draw_bg():
    for x in range(-1, 3):
        screen.blit(new_bg, (x * new_bg.get_width() + bg_scroll, 0))
        screen.blit(new_floor, (x * new_floor.get_width() + floor_scroll, floor_y))

class Player(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.health = 100
        self.max_health = self.health
        self.char_type = char_type

        animation_types = ['idle']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height()) * scale))
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = img.get_rect()
        self.rect.center = (x, y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = x
        self.y = y
        self.flip = False
        self.scale = scale
        self.speed = speed
        self.direction = 1
        self.jump = False
        self.vel_y = 0

    def update(self):
        self.update_animation()

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

    def move(self, moving_left, moving_right):
        global screen_scroll, bg_scroll, floor_scroll

        screen_scroll = 0
        
        dx = 0
        dy = 0
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True:
            self.vel_y = -11
            self.jump = False

        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # check collision
        if self.rect.bottom + dy > 700:
            dy = 700 - self.rect.bottom


        self.rect.x += dx
        self.rect.y += dy

        if self.rect.right > 1280 - SCROLL_THRESH:
            screen_scroll = self.rect.right - (1280 - SCROLL_THRESH)
            self.rect.right = 1280 - SCROLL_THRESH

        elif self.rect.left < SCROLL_THRESH:
            screen_scroll = self.rect.left - SCROLL_THRESH
            self.rect.left = SCROLL_THRESH

        bg_scroll -= screen_scroll // 4
        floor_scroll -= screen_scroll

    def draw_healthbar(self):
        bar_x = self.rect.centerx - health_bar_img.get_width() // 2
        bar_y = self.rect.top - 25

        screen.blit(health_bar_img, (bar_x, bar_y))

        health_ratio = self.health / self.max_health
        current_health_width = int(damage_bar_img.get_width() * health_ratio)

        if current_health_width > 0:
            green_bar = pygame.transform.scale(health_bar_img, (current_health_width, health_bar_img.get_height()))
            screen.blit(green_bar, (bar_x, bar_y))

def draw_enemy(enemy, scroll):
    screen.blit(pygame.transform.flip(enemy.image, enemy.flip, False), (enemy.rect.x + scroll, enemy.rect.y))

player = Player("player", 200, 400, 3, 5)
enemy = Player("zombie", 200, 650, 3, 5)

running = True
while running:
    clock.tick(FPS)
    draw_bg()
    player.update()
    player.draw()
    player.draw_healthbar()
    player.move(moving_left, moving_right)
    enemy.update()
    draw_enemy(enemy, floor_scroll)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                player.jump = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                player.jump = False
            
    pygame.display.update()

pygame.quit()
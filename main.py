import pygame
import os
pygame.init()
screen = pygame.display.set_mode((1280, 960))
pygame.display.set_caption("DragonHunter")
background_img = pygame.image.load('images/background/default.png').convert_alpha()
original_width, original_height = background_img.get_size()
new_width = original_width * 4
new_height = original_height * 4
new_size = (new_width, new_height)
new_bg = pygame.transform.scale(background_img, new_size)

def draw_bg():
    screen.blit(new_bg, (0, 0))

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        

        animation_types = ['idle']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'images/player/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'images/player/{animation}/{i}.png').convert_alpha()
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

player = Player(200, 400, 3, 5)


running = True
while running:
    draw_bg()
    player.update()
    player.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
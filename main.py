import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 960))
background_img = pygame.image.load('images/background/default.png').convert_alpha()
original_width, original_height = background_img.get_size()
new_width = original_width * 4
new_height = original_height * 4
new_size = (new_width, new_height)
new_bg = pygame.transform.scale(background_img, new_size)

running = True
while running:
    screen.blit(new_bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()
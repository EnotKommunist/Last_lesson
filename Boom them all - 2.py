import sys
import random
import pygame
import os


def load_image(name, colorkey=-1):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        # image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


pygame.init()
size = width, height = (500, 500)


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")
    list_of_coords = []

    def __init__(self, *group):
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.add_coords()

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom

    def convert_rect(self, x, y, w, h):
        return (x, x + w), (y, y + h)

    def add_coords(self):
        t = True
        while t:
            x = random.randrange(width - 51)
            y = random.randrange(height - 51)
            if len(Bomb.list_of_coords) == 0:
                Bomb.list_of_coords.append((x, y))
                self.rect.x = x
                self.rect.y = y
                t = False
            else:
                for i in Bomb.list_of_coords:
                    rect1 = self.convert_rect(x, y, 51, 51)
                    rect2 = self.convert_rect(i[0], i[1], 51, 51)
                    if rect1[0][1] - rect1[0][0] < rect2[0][1] - rect2[0][0] and \
                        rect1[1][1] - rect1[1][0] < rect2[1][1] - rect2[1][0]:
                        rect1, rect2 = rect2, rect1

                    if (rect1[0][0] <= rect2[0][0] <= rect1[0][1] or
                        rect1[0][0] <= rect2[0][1] <= rect1[0][1]) and \
                            (rect1[1][0] <= rect2[1][0] <= rect1[1][1] or
                             rect1[1][0] <= rect2[1][1] <= rect1[1][1]):
                        f = False
                        break
                    else:
                        f = True
                if f:
                    Bomb.list_of_coords.append((x, y))
                    self.rect.x = x
                    self.rect.y = y
                    t = False


screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
for _ in range(20):
    Bomb(all_sprites)
running = True
cords_mouse = None, None
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for bomb in all_sprites:
                bomb.update(event)
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
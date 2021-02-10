import os
import sys

import pygame
import requests


class Paramests(object):
    def __init__(self):
        self.ll = "37.530887,55.703118"
        self.z = 12
        self.l = "map"
        self.size = "650,450"


def load_map(p):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={p.ll}&z={p.z}&l={p.l}&size={p.size}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    return response


def move(x, y, size):
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        if y + 10 <= 0:
            y += 10
    if key[pygame.K_DOWN]:
        if y + size[1] - 10 >= 450:
            y -= 10
    if key[pygame.K_LEFT]:
        if x + 10 <= 0:
            x += 10
    if key[pygame.K_RIGHT]:
        if x + size[0] - 10 >= 600:
            x -= 10

    return x, y


p = Paramests()
response = load_map(p)
# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

image = pygame.image.load(map_file)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
x, y = 0, 0
image = pygame.image.load(map_file)
screen.blit(image, (x, y))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        x, y = move(x, y, image.get_size())

    screen.blit(image, (x, y))
    pygame.display.flip()

pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
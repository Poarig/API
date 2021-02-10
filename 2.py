import os
import sys
import pygame
import requests


class Params(object):
    def __init__(self, ll="37.530887,55.703118", z=11,l="map", size='600,450'):
        self.ll = ll
        self.z = z
        self.l = l
        self.size = size


def load_map(p):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={p.ll}&z={p.z}&size={p.size}&l={p.l}"
    response = requests.get(map_request)
    # print(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


pygame.init()

params = Params()
map_file = load_map(params)

screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEDOWN:
                if params.z < 20:
                    params.z += 1
                    print(params.z)
            if event.key == pygame.K_PAGEUP:
                if params.z > 0:
                    params.z -= 1
                    print(params.z)

    map_file = load_map(params)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()

pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)

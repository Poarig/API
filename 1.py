import os
import sys

import pygame
import requests


class Paramests(object):
    def __init__(self):
        self.ll = "37.530887,55.703118"
        self.z = 12
        self.l = "map"
        self.size = "600,450"


def load_map(p):
    map_request = f"http://static-maps.yandex.ru/1.x/?ll={p.ll}&z={p.z}&l={p.l}&size={p.size}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    return response


p = Paramests()
response = load_map(p)
# Запишем полученное изображение в файл.
map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(map_file)
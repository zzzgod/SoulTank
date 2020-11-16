import pygame
import json


def show_block(block: dict) -> None:
    img = None
    if block['BlockType'] == 'Wall':
        img = pygame.image.load('../img/walls.gif')
    elif block['BlockType'] == 'Grass':
        img = pygame.image.load('../img/grass.gif')
    elif block['BlockType'] == 'Steel':
        img = pygame.image.load('../img/steels.gif')
    elif block['BlockType'] == 'Water':
        img = pygame.image.load('../img/water.gif')
    if img is not None:
        window.blit(img, (block['x'] * 60, block['y'] * 60))


def load_map(index: int) -> None:
    path = '../maps/map' + str(index) + '.json'
    with open(path, 'r') as f:
        info: dict = json.load(f)
        for block in info['MapBlocks']:
            show_block(block)


if __name__ == '__main__':
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('地图编辑器')
    load_map(1)
    img_imformation = pygame.image.load('imformation.gif')
    while True:
        window.blit(img_imformation, (1140, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)
        pygame.time.wait(10)
        pygame.display.update()

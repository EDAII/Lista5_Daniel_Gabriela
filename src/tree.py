import sys
import pygame
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGRAY = (169, 169, 169)
YELLOW = (222, 178, 0)
PINK = (225, 96, 253)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
ORANGE = (255, 99, 71)
GRAY = (119, 136, 153)
LIGHTORANGE = (255, 176, 56)
INTERMEDIARYORANGE = (255, 154, 0)
LIGHTBLUE = (60, 170, 255)
DARKBLUE = (0, 101, 178)
BEIGE = (178, 168, 152)

SCREEN_BACKGROUND_COLOR = BLACK

WIDTH = 1600
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)

class Node():
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.color = color
        self.node_left = None
        self.node_right = None

    def render(self, background):
        pygame.draw.circle(background, self.color, self.position, self.size)
         

class Tree():
    def __init__(self):
        self.nodes = []

    def append_node(self, node):
        self.nodes.append(node)

    def render(self, background):
        for node in self.nodes:
            node.render(background)


class Game():
    def __init__(self):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Tree')

        self.tree = self.create_tree()

    def create_tree(self):
        tree = Tree()
        # 9 niveis eh o maximo com a tela de 800 de altura
        # TODO: montar a arvore colocando as referencias de node_left e node_right
        # inserir, travessia -> verificar onde ele vai ser colocado, pegar a posição com referencia pro pai e criar as arestas
        initial_size = WIDTH // 2
        for h in range(40, 90 * 5 + 40, 90):
            for pos in range(initial_size, WIDTH, initial_size * 2):
                node = Node([pos, h], 25, WHITE)
                tree.append_node(node)
            initial_size = initial_size // 2
        return tree

    def render(self):
        self.tree.render(self.background)

    def run(self):
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True

            self.render()
            
            pygame.display.update()

        pygame.quit()
        sys.exit(0)


def main():
    mygame = Game()
    mygame.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interruption')

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

NODE_SIZE = 25
NODES_QTT = 31
MARGIN = 40
X_DISTANCE = 50
Y_DISTANCE = 80

WIDTH = 1400
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)

class Node():
    def __init__(self, size, color, data):
        self.parent = None
        self.y_position = 0
        self.x_position = 0
        self.size = size
        self.color = color
        self.node_left = None
        self.node_right = None
        self.data = data

    def render(self, background):       
        circle = pygame.draw.circle(background, self.color, [self.x_position, self.y_position], self.size)
        circle.center = (self.x_position + self.size/2 + 7, self.y_position + self.size/2 + 7)

        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(str(self.data), True, BLACK, WHITE) 

        background.blit(text, circle)
    def __str__(self):
        return str(self.data)

class Tree():
    def __init__(self):
        self.nodes = []
        self.adj_list = []
        self.root = None

    def append_node(self, node):
        self.nodes.append(node)

    # def insert_in_tree(self, node): 
    #     if self.root is None: 
    #         self.root = node
    #     else: 

    #         if root.val < node.val: 
    #             if root.right is None: 
    #                 root.right = node 
    #             else: 
    #                 self.insert_in_tree(root.right, node) 
    #         else: 
    #             if root.left is None: 
    #                 root.left = node 
    #             else: 
    #                 self.insert_in_tree(root.left, node) 
    
    def insert_in_tree(self, node):
        self.append_node(node)
        if self.root == None:
          self.root = node
          self.root.x_position = WIDTH // 2
          self.root.y_position = MARGIN

        else: 
            # se nao for a raiz
            temp = self.root

            right_side = True
            left_side = True

            while True:
                parent = temp
                if node.data <= temp.data:
                    right_side = False
                    # ir para esquerda
                    temp = temp.node_left
                    if temp == None:
                        parent.node_left = node
                        node.parent = parent
                        if left_side:
                            node.x_position = parent.x_position // 2
                            node.y_position = parent.y_position + Y_DISTANCE
                        elif node == parent.node_left and parent == parent.parent.node_left:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) - (parent.parent.x_position - parent.x_position)
                            node.y_position = parent.y_position + Y_DISTANCE
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                            node.y_position = parent.y_position + Y_DISTANCE
                        # if left_tree:
                        # else:
                        #     temp.node_left.x_position = temp.x_position -  (WIDTH - temp.x_position) // 2
                        #     temp.node_left.y_position = temp.y_position + Y_DISTANCE
                        return
                else:
                    left_side = False
                    # ir para direita
                    temp = temp.node_right
                    if temp == None:
                        parent.node_right = node
                        node.parent = parent
                        if right_side:
                            node.x_position = (WIDTH + parent.x_position) // 2
                            node.y_position = parent.y_position + Y_DISTANCE
                        elif node == parent.node_right and parent == parent.parent.node_right:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) + (parent.x_position - parent.parent.x_position)
                            node.y_position = parent.y_position + Y_DISTANCE
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                            node.y_position = parent.y_position + Y_DISTANCE
                        # temp.node_right.x_position = (temp.x_position + WIDTH) // 2 # temp.x_position  + temp.x_position // 2
                        # temp.node_right.y_position = temp.y_position + Y_DISTANCE
                         # fim da condição ir a direita
                        return

    def get_nodes_for_level(self):          
        if self.root is None: 
            return []
        # Create an empty queue for level order traversal 
        queue = []         
        # Enqueue root and initialize height 
        queue.append(self.root)

        while queue:
            count = len(queue)
            while count > 0:
                temp = queue.pop(0)
                self.nodes.append(temp)
                if temp.node_left:
                    queue.append(temp.node_left)
                if temp.node_right:
                    queue.append(temp.node_right)

                count -= 1
        

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

        # aqui já iremos ter o array de valores inseridos pelo usuário
        random_nodes = random.sample(range(1, 100), NODES_QTT)
        # erros: 19, 21, 28, 27, 29
        n_nodes = [30, 20, 15, 10, 5, 12, 18, 19, 17, 25, 23, 24, 21, 28, 27, 29, 40, 45, 50, 55, 35, 33, 38, 43, 31, 34, 36, 39, 42, 44, 48]
        for i in n_nodes:
            node = Node(NODE_SIZE, WHITE, i)
            tree.insert_in_tree(node)

        # TODO verificar se a raíz é nula
        # após ter a árvore formada, fazemos uma travessia por níveis
        tree.get_nodes_for_level()
        # 9 niveis eh o maximo com a tela de 800 de altura

        # inserir, travessia -> verificar onde ele vai ser colocado, pegar a posição com referencia pro pai e criar as arestas

        # initial_size = WIDTH // 2
        # count = 0
        # for h in range(40, 90 * 5 + 40, 90):
        #     for pos in range(initial_size, WIDTH, initial_size * 2):
        #         # node = Node([pos, h], 25, WHITE, random.randint(0, 100))
        #         #insere as posições
        #         tree.nodes[count].position.append(pos)
        #         tree.nodes[count].position.append(h)         
        #         count += 1

        #     initial_size = initial_size // 2

        for node in tree.nodes:
            print(node.data)
            if node.node_left:
                print(node.node_left.data)
            if node.node_right:
                print(node.node_right.data)
            print("_________________")
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
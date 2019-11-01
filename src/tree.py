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

SCREEN_BACKGROUND_COLOR = WHITE

NODE_SIZE = 25
NODES_QTT = 31
MARGIN = 40
X_DISTANCE = 50
Y_DISTANCE = 80

WIDTH = 1330
HEIGHT = 800
SCREEN_SIZE = (WIDTH, HEIGHT)

# red and black insert cases


class Edge():
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
    def render(self, background):
        pygame.draw.line(background, 
                        BLACK, 
                        (self.from_node.x_position, self.from_node.y_position), 
                        (self.to_node.x_position, self.to_node.y_position), 1)

class Node():
    def __init__(self, color, data, node_left, node_right):
        self.y_position = None
        self.x_position = None
        
        self.size = NODE_SIZE
        self.color = color
        self.data = data

        self.parent = None
        self.node_left = node_left
        self.node_right = node_right

    def render(self, background):
        circle = pygame.draw.circle(background, self.color, [self.x_position, self.y_position], self.size)
        circle.center = (self.x_position + self.size//2 + 5, self.y_position + self.size//2 + 7)

        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(str('{:02d}'.format(self.data)), True, WHITE, self.color)

        background.blit(text, circle)

    def __str__(self):
        return str(self.data)

class Tree():
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.root = None

    def get_edge(self, from_node, to_node):
        for edge in self.edges:
            if edge.from_node == from_node and edge.to_node == to_node:
                return edge
        return None

    def append_node(self, node):
        self.nodes.append(node)

    def get_level_util(self, node, data, level):
        if (node == None):
            return 0
    
        if (node.data == data):
            return level
    
        downlevel = self.get_level_util(node.node_left, data, level + 1)
        if (downlevel != 0):
            return downlevel
    
        downlevel = self.get_level_util(node.node_right, data, level + 1)
        return downlevel
    
    def get_level(self, node):
        return self.get_level_util(self.root, node.data, 1)

    def insert_in_tree(self, node):
        if self.root == None:
            self.root = node
            self.root.x_position = WIDTH // 2
            self.root.y_position = MARGIN

            self.append_node(node)
            if node.node_right != None:
                self.append_node(node.node_right)
                self.edges.append(Edge(node, node.node_right))
                node.node_right.parent = node
                node.node_right.x_position = node.x_position + 30
                node.node_right.y_position = node.y_position + Y_DISTANCE
            if node.node_left != None:
                self.append_node(node.node_left)
                self.edges.append(Edge(node, node.node_left))
                node.node_left.parent = node
                node.node_left.x_position = node.x_position - 30
                node.node_left.y_position = node.y_position + Y_DISTANCE

        else:
            temp = self.root
            right_side = True
            left_side = True
            
            while True:
                parent = temp
                if node.data <= temp.data:
                    right_side = False
                    temp = temp.node_left

                    if temp.data == -1:
                        self.edges.remove(self.get_edge(parent, temp))
                        self.nodes.remove(temp)
                        temp = None
                        
                    if temp == None:
                        if self.get_level(parent) >= 5:
                            print("Erro, insira outro nó")
                            break
                        parent.node_left = node
                        node.parent = parent
                        self.append_node(node)

                        self.edges.append(Edge(parent, node))

                        if left_side:
                            node.x_position = parent.x_position // 2
                        elif node == parent.node_left and parent == parent.parent.node_left:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) - (parent.parent.x_position - parent.x_position)
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                        node.y_position = parent.y_position + Y_DISTANCE
                        
                        if node.node_right != None:
                            self.append_node(node.node_right)
                            self.edges.append(Edge(node, node.node_right))
                            node.node_right.parent = node
                            node.node_right.x_position = node.x_position + 30
                            node.node_right.y_position = node.y_position + Y_DISTANCE
                        if node.node_left != None:
                            self.append_node(node.node_left)
                            self.edges.append(Edge(node, node.node_left))
                            node.node_left.parent = node
                            node.node_left.x_position = node.x_position - 30
                            node.node_left.y_position = node.y_position + Y_DISTANCE

                        return
                else:
                    left_side = False
                    temp = temp.node_right

                    if temp.data == -1:
                        self.edges.remove(self.get_edge(parent, temp))
                        self.nodes.remove(temp)
                        temp = None

                    if temp == None:
                        if self.get_level(parent) >= 5:
                            print("Erro, insira outro nó")
                            break
                        parent.node_right = node
                        node.parent = parent

                        self.append_node(node)

                        self.edges.append(Edge(parent, node))

                        if right_side:
                            node.x_position = (WIDTH + parent.x_position) // 2
                        elif node == parent.node_right and parent == parent.parent.node_right:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) + (parent.x_position - parent.parent.x_position)
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                        node.y_position = parent.y_position + Y_DISTANCE
                        
                        if node.node_right != None:
                            self.append_node(node.node_right)
                            self.edges.append(Edge(node, node.node_right))
                            node.node_right.parent = node
                            node.node_right.x_position = node.x_position + 30
                            node.node_right.y_position = node.y_position + Y_DISTANCE
                        if node.node_left != None:
                            self.append_node(node.node_left)
                            self.edges.append(Edge(node, node.node_left))
                            node.node_left.parent = node
                            node.node_left.x_position = node.x_position - 30
                            node.node_left.y_position = node.y_position + Y_DISTANCE
                        return

    def grandpa(self, node):
        if node != None and node.parent != None:
            return (node.parent).parent
        else:
            return None

    def uncle(self, node):
        if self.grandpa(node) == None:
            return None
        if node.parent == self.grandpa(node).node_left:
            return self.grandpa(node).node_right
        else:
            return self.grandpa(node).node_left

    def render(self, background):
        for edge in self.edges:
            edge.render(background)     
        for node in self.nodes:
            node.render(background)

class Game():
    def __init__(self, option):
        try:
            pygame.init()
        except:
            print('The pygame module did not start successfully')

        self.background = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption('Tree')
        self.background.fill(SCREEN_BACKGROUND_COLOR)
        pygame.display.update()

        self.option = option
        self.tree = Tree()

    def render(self):
        self.background.fill(SCREEN_BACKGROUND_COLOR)
        print(self.tree.nodes)
        node_value = int(input("Digite o valor do nó:"))
        # TODO: tratamento de erro de input
        self.tree.insert_in_tree(Node(RED, node_value, Node(BLACK, -1, None, None), Node(BLACK, -1, None, None)))
        if(self.option == "1"):
            pass
        elif(self.option == "2"):
            pass
        else:
            self.tree.render(self.background)
        pygame.display.update()

    def run(self):
        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        exit = True
            
            # TODO: render rodar sobre thread
            self.render()
            pygame.display.update()

        pygame.quit()
        sys.exit(0)


def menu():
    option = 0
    while(option != "1" and option != "2" and option != "3"):
        if(option != 0):
            print("!!!! Opção Inválida !!!!\n")
        print("\nEscolha o tipo de árvore:\n")
        print("1 - Árvore AVL")
        print("2 - Árvore Vermelho e Preto")
        print("3 - Árvore Binária de Busca\n")
        option = input()
    return option

def main():
    option = menu()
    mygame = Game(option)
    mygame.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interruption')
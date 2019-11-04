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

class InputBox:

    def __init__(self, x, y, w, h, text='', desc=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('lightskyblue3')
        self.text = text
        self.label_input = pygame.font.Font(None, 32).render(desc, True, DARKBLUE)
        self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the self.input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')
        if event.type == pygame.KEYDOWN:
            if self.active:
                # if event.key == pygame.K_RETURN:
                #    print(self.text)
                #    self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key != pygame.K_RETURN and event.key != pygame.K_TAB and len(self.text) < 18:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

        screen.blit(self.label_input, (self.rect.x, self.rect.y - 30))


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
        self.x_position = None
        self.y_position = None

        self.size = NODE_SIZE
        self.color = color
        self.data = data

        self.parent = None
        self.node_left = node_left
        self.node_right = node_right
    
    def render(self, background):
        circle = pygame.draw.circle(background, self.color, [self.x_position, self.y_position], self.size)
        circle.center = (self.x_position + self.size//2, self.y_position + self.size//2 + 7)

        font = pygame.font.Font('freesansbold.ttf', 15)
        text = font.render(str('{:03d}'.format(self.data)), True, WHITE, self.color)

        background.blit(text, circle)

    def __str__(self):
        return str(self.data)

class Tree():
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.root = None

    def verify_exist_value(self, value):
        for node in self.nodes:
            if value == node.data:
                return True
        return False


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

    # A function to preorder update pos in screen
    def update_pre_order(self, node): 
        if node != None: 
    
            # First print the data of node 
            self.update_sons(node), 
    
            # Then recur on left child 
            self.update_pre_order(node.node_left) 
    
            # Finally recur on right child 
            self.update_pre_order(node.node_right) 

    def search_to_son_right(self, node):
        if self.root.data == node.data or self.root == None:
            return ((WIDTH + self.root.x_position) // 2, self.root.y_position + Y_DISTANCE)
        
        else:
            temp = self.root
            right_side = True
            left_side = True

            while True:
                parent = temp

                if node.data <= temp.data and temp.data != -1:
                    right_side = False
                    temp = temp.node_left

                    if temp.data == node.data:
                        return ((node.x_position + node.parent.x_position) // 2, node.y_position + Y_DISTANCE)
                elif node.data > temp.data and temp.data != -1:
                    left_side = False
                    temp = temp.node_right

                    if temp.data == node.data:
                        if right_side:
                            return ((WIDTH + node.x_position) // 2, node.y_position + Y_DISTANCE)
                        else:
                            return (((node.x_position + node.parent.x_position) // 2) + (node.x_position - node.parent.x_position), node.y_position + Y_DISTANCE)
        
    
    def search_to_son_left(self, node):
        if self.root.data == node.data or self.root == None:
            return (self.root.x_position // 2, self.root.y_position + Y_DISTANCE)
        else:
            temp = self.root
            right_side = True
            left_side = True

            while True:
                parent = temp

                if node.data <= temp.data and temp.data != -1:
                    right_side = False
                    temp = temp.node_left

                    if temp.data == node.data:
                        if left_side:
                            return (node.x_position // 2, node.y_position + Y_DISTANCE)
                        else:
                            return (((node.x_position + node.parent.x_position) // 2) - (node.parent.x_position - node.x_position), node.y_position + Y_DISTANCE)

                elif node.data > temp.data and temp.data != -1:
                    left_side = False
                    temp = temp.node_right

                    if temp.data == node.data:
                        return ((node.x_position + node.parent.x_position) // 2, node.y_position + Y_DISTANCE)

    def update_sons(self, node):
        if node.node_left != None:
            (node.node_left.x_position, node.node_left.y_position) = self.search_to_son_left(node)
        if node.node_right != None:
            (node.node_right.x_position, node.node_right.y_position) = self.search_to_son_right(node)

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
                (node.node_left.x_position, node.node_left.y_position) = self.search_to_son_left(node)
                (node.node_right.x_position, node.node_right.y_position) = self.search_to_son_right(node)

            if node.node_left != None:
                self.append_node(node.node_left)
                self.edges.append(Edge(node, node.node_left))
                node.node_left.parent = node
                (node.node_left.x_position, node.node_left.y_position) = self.search_to_son_left(node)
                (node.node_right.x_position, node.node_right.y_position) = self.search_to_son_right(node)

        else:
            temp = self.root
            right_side = True
            left_side = True
            
            while True:
                parent = temp
                if self.get_level(parent) >= 5:
                    print('Erro, insira outro nó')
                    break
                if node.data <= temp.data:
                    right_side = False
                    temp = temp.node_left

                    if temp != None:
                        if temp.data == -1:
                            self.edges.remove(self.get_edge(parent, temp))
                            self.nodes.remove(temp)
                            temp = None

                    if temp == None:
                        parent.node_left = node
                        node.parent = parent
                        self.append_node(node)

                        self.edges.append(Edge(parent, node))

                        node.y_position = parent.y_position + Y_DISTANCE
                        if left_side:
                            node.x_position = parent.x_position // 2
                        elif node == parent.node_left and parent == parent.parent.node_left:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) - (parent.parent.x_position - parent.x_position)
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                        
                        if node.node_right != None:
                            self.append_node(node.node_right)
                            self.edges.append(Edge(node, node.node_right))
                            node.node_right.parent = node
                            (node.node_right.x_position, node.node_right.y_position) = self.search_to_son_right(node)
                        if node.node_left != None:
                            self.append_node(node.node_left)
                            self.edges.append(Edge(node, node.node_left))
                            node.node_left.parent = node
                            (node.node_left.x_position, node.node_left.y_position) = self.search_to_son_left(node)
                        return
                else:
                    left_side = False
                    temp = temp.node_right

                    if temp != None:
                        if temp.data == -1:
                            self.edges.remove(self.get_edge(parent, temp))
                            self.nodes.remove(temp)
                            temp = None

                    if temp == None:
                        parent.node_right = node
                        node.parent = parent

                        self.append_node(node)

                        self.edges.append(Edge(parent, node))

                        node.y_position = parent.y_position + Y_DISTANCE
                        if right_side:
                            node.x_position = (WIDTH + parent.x_position) // 2
                        elif node == parent.node_right and parent == parent.parent.node_right:
                            node.x_position = ((parent.x_position + parent.parent.x_position) // 2) + (parent.x_position - parent.parent.x_position)
                        else:
                            node.x_position = (parent.x_position + parent.parent.x_position) // 2
                        
                        if node.node_right != None:
                            self.append_node(node.node_right)
                            self.edges.append(Edge(node, node.node_right))
                            node.node_right.parent = node
                            (node.node_right.x_position, node.node_right.y_position) = self.search_to_son_right(node)
                        if node.node_left != None:
                            self.append_node(node.node_left)
                            self.edges.append(Edge(node, node.node_left))
                            node.node_left.parent = node
                            (node.node_left.x_position, node.node_left.y_position) = self.search_to_son_left(node)
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

    def get_node_array(self, value):
        for node in self.nodes:
            if node.data == value:
                return node        
        return None

    def remove_background_node(self, node):
        for n in self.nodes:
            if node.x_position == n.x_position and node.y_position == n.y_position:
                self.nodes.remove(n)

    def insert_in_tree_RB(self, node):
        self.insert_in_tree(node)
        self.insercao_caso1(node)

    def print_node(self, node):
        print(str(node.data) + ' - ' + str(node.x_position) + ' - ' + str(node.y_position) + ' - ' + str(node.color))


    def rotacionar_direita(self, node):
        print('rotacao direita')
        q = node.node_left

        # atualiza o pai de node para o novo filho
        if node.parent != None:
            if node == node.parent.node_left:
                self.edges.remove(self.get_edge(node.parent, node.parent.node_left))
                node.parent.node_left = q
                self.edges.append(Edge(node.parent, q))
            else:
                self.edges.remove(self.get_edge(node.parent, node.parent.node_right))
                node.parent.node_right = q
                self.edges.append(Edge(node.parent, q))
            # fim da atualizacao
        q.parent = node.parent

        self.edges.remove(self.get_edge(q, q.node_right))
        self.edges.remove(self.get_edge(node, q))
        
        node.node_left = q.node_right
        q.node_right.parent = node
        self.edges.append(Edge(node, q.node_right))

        q.node_right = node
        self.edges.append(Edge(q, node))
        node.parent = q

        if q.parent == None:
            self.root = q
            (q.x_position, q.y_position) = (WIDTH // 2, MARGIN)
        else:
            if q == q.parent.node_left:
                (q.x_position, q.y_position) = self.search_to_son_left(q.parent)
            else:
                (q.x_position, q.y_position) = self.search_to_son_right(q.parent)
            
        (node.x_position, node.y_position) = self.search_to_son_right(node.parent)
        (q.node_left.x_position, q.node_left.y_position) = self.search_to_son_left(q.node_left.parent)

        self.update_pre_order(self.root)

    def rotacionar_esquerda(self, node):
        print('rotacao esquerda')
        q = node.node_right

        # atualiza o pai de node para o novo filho
        if node.parent != None:
            if node == node.parent.node_left:
                self.edges.remove(self.get_edge(node.parent, node.parent.node_left))
                node.parent.node_left = q
                self.edges.append(Edge(node.parent, q))
            else:
                self.edges.remove(self.get_edge(node.parent, node.parent.node_right))
                node.parent.node_right = q
                self.edges.append(Edge(node.parent, q))
            # fim da atualizacao
        q.parent = node.parent

        self.edges.remove(self.get_edge(q, q.node_left))
        self.edges.remove(self.get_edge(node, q))

        node.node_right = q.node_left
        q.node_left.parent = node
        self.edges.append(Edge(node, q.node_left))

        q.node_left = node
        self.edges.append(Edge(q, node))
        node.parent = q
        
        if q.parent == None:
            self.root = q
            (q.x_position, q.y_position) = (WIDTH // 2, MARGIN)
        else:
            if q == q.parent.node_left:
                (q.x_position, q.y_position) = self.search_to_son_left(q.parent)
            else:
                (q.x_position, q.y_position) = self.search_to_son_right(q.parent)
            
        (node.x_position, node.y_position) = self.search_to_son_left(node.parent)
        (q.node_right.x_position, q.node_right.y_position) = self.search_to_son_right(q.node_right.parent)

        self.update_pre_order(self.root)

    def insercao_caso1(self, node):
        if node.parent == None:
            print('caso 1')
            node.color = BLACK
        else:
            self.insercao_caso2(node)

    def insercao_caso2(self, node):
        if node.parent.color == BLACK:
            print('caso 2')
            return
        else:
            self.insercao_caso3(node)

    def insercao_caso3(self, node):
        uncle_node = self.uncle(node)

        if uncle_node != None and uncle_node.color == RED:
            print('caso 3')
            node.parent.color = BLACK
            uncle_node.color = BLACK
            g = self.grandpa(node)
            g.color = RED
            self.insercao_caso1(g)
        else:
            self.insercao_caso4(node)

    def insercao_caso4(self, node):
        print('caso 4')
        g = self.grandpa(node)

        if node == node.parent.node_right and node.parent == g.node_left:
            self.rotacionar_esquerda(node.parent)
            node = node.node_left

        elif node == node.parent.node_left and node.parent == g.node_right:
            self.rotacionar_direita(node.parent)
            node = node.node_right

        self.insercao_caso5(node)

    def insercao_caso5(self, node):
        print('caso 5')
        g = self.grandpa(node)

        node.parent.color = BLACK
        g.color = RED
        if node == node.parent.node_left and node.parent == g.node_left:
            self.rotacionar_direita(g)
        else:
            self.rotacionar_esquerda(g)

    def black_height_recursive(node):
        altura = 0
        if node != None:
            if no.color == BLACK:
                altura = 1 + max(self.black_height_recursive(node.node_left), self.black_height_recursive(node.node_right))
            else:
                altura = max(self.black_height_recursive(node.node_left), self.black_height_recursive(node.node_right))
        return altura

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
            print('O modulo pygame não foi iniciado com sucesso!')

        self.background = pygame.display.set_mode(SCREEN_SIZE)
        self.background.fill(SCREEN_BACKGROUND_COLOR)
        pygame.display.set_caption('Tree')
        pygame.display.update()

        self.option = option
        self.tree = Tree()

        self.input_box = InputBox(10, 600, 250, 32, '', 'Digite o valor do nó e aperte Enter para inserir (Valor entre 0 e 999)')

    def render(self):
        self.background.fill(SCREEN_BACKGROUND_COLOR)

        self.input_box.draw(self.background)
        self.input_box.update()
        
        # node_value = input('Digite o valor do nó: ')
        # try:
        #     node_value = int(node_value)

        #     if self.tree.verify_exist_value(node_value):
        #         print('Este valor já foi inserido na arvore!')
        #     elif node_value < 0:
        #         print('Digite valores positivos!')
        #     elif node_value > 999:
        #         print('Digite numeros menores que 1000!')
        #     else:
        #         if self.option == '1':
        #             pass
        #         elif self.option == '2':
        #             nil1 = Node(BLACK, -1, None, None)
        #             nil2 = Node(BLACK, -1, None, None)
        #             node_inser = Node(RED, node_value, nil1, nil2)
        #             self.tree.insert_in_tree_RB(node_inser)
        #         else:
        #             node_inser = Node(RED, node_value, None, None)
        #             self.tree.insert_in_tree(node_inser)
        
        # except ValueError:
        #     print('Isso não é um inteiro!')
        #     print('Não.. o input não é um inteiro. É uma string.')
        
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
                    if event.key == pygame.K_RETURN and len(self.input_box.text) > 0:
                        try:
                            node_value = int(self.input_box.text)
                            if self.tree.verify_exist_value(node_value):
                                print('Este valor já foi inserido na arvore!')
                            elif node_value < 0:
                                print('Digite valores positivos!')
                            elif node_value > 999:
                                print('Digite numeros menores que 1000!')
                            else:
                                if self.option == '1':
                                    pass
                                elif self.option == '2':
                                    nil1 = Node(BLACK, -1, None, None)
                                    nil2 = Node(BLACK, -1, None, None)
                                    node_inser = Node(RED, node_value, nil1, nil2)
                                    self.tree.insert_in_tree_RB(node_inser)
                                else:
                                    node_inser = Node(RED, node_value, None, None)
                                    self.tree.insert_in_tree(node_inser)
                        except ValueError:
                            print('Isso não é um inteiro!')
                            print('Não.. o input não é um inteiro. É uma string.')
                self.input_box.handle_event(event)

            self.render()
            pygame.display.update()

        pygame.quit()
        sys.exit(0)

def menu():
    option = 0
    while(option != '1' and option != '2' and option != '3'):
        if(option != 0):
            print('!!!! Opção Inválida !!!!\n')
        print('\nEscolha o tipo de árvore: \n')
        print('1 - Árvore AVL')
        print('2 - Árvore Vermelho e Preto')
        print('3 - Árvore Binária de Busca\n')
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
        # n_nodes = [30, 20, 15, 10, 5, 12, 18, 19, 17, 25, 23, 24, 21, 28, 27, 29, 40, 45, 50, 55, 35, 33, 38, 43, 31, 34, 36, 39, 42, 44, 48]
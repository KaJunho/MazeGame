import random, os, ctypes
import msvcrt

class Kruskal(object):
    def __init__(self, node, a):
        self.father = None
        self.pos = [node[0], node[1]]
        self.attr = a  # wall==1 route== 0
        self.offspring = []
        self.nodenum = 1

    def add_node(self, tree):
        if not (tree in self.offspring):
            self.offspring.append(tree)
            temp1 = self
            tree.set_father(temp1)
            self.nodenum += tree.nodenum
            self.update_nodenum(tree)
        else:
            print('This node %s is already added.' % (tree.pos))

    def set_father(self, fa):
        self.father = fa

    def update_nodenum(self, tree):
        if self.father != None:
            self.father.nodenum += tree.nodenum
            self.father.update_nodenum(tree)

    def show_offspring(self):
        for i in self.offspring:
            print(i)

    def find_root(self):
        if self.father == None:
            return self
        else:
            return self.father.find_root()

    def __str__(self):
        return '(' + str(self.pos[0]) + ',' + str(self.pos[1]) + ')'


class Map_of_Maze(object):
    def __init__(self, h, w):
        self.height = h
        self.width = w
        self.map = [[0 if j % 2 == 1 and i % 2 == 1 else 1 for j in range(self.width)] for i in range(self.height)]  # initialize the map, 0 refers to route and 1 refers to wall
        self.m_trees = [[None for j in range(self.width)] for i in range(self.height)]
        self.init_trees()

    def init_trees(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.map[i][j] == 0:
                    self.m_trees[i][j] = Kruskal((i, j), 0)
                elif self.map[i][j] == 1:
                    self.m_trees[i][j] = Kruskal((i, j), 1)

    def print_maze(self):

        for i in range(self.height):
            for j in range(self.width):
                if self.m_trees[i][j].attr == 1:
                    goto(i, j)
                    print(wall)
                elif self.m_trees[i][j].attr == 2:  # Start
                    goto(i, j)
                    print(moving_point)
                elif self.m_trees[i][j].attr == 3:  # terminal
                    goto(i, j)
                    print(termin)
                else:
                    goto(i, j)
                    print(road)
                #if j == self.width - 1:
                    #print('\n', sep='', end='')


STD_OUTPUT_HANDLE = -11
hout = ctypes.windll.kernel32.GetStdHandle(ctypes.c_long(STD_OUTPUT_HANDLE))
def goto(y, x):
   value = x + (y << 16)
   ctypes.windll.kernel32.SetConsoleCursorPosition(hout, ctypes.c_ulong(value))


def begin_end(m):
    frame_list_left = [(x, 1) for x in range(1, m.height - 1)]  # beginning must be on leftside
    frame_list_right = [(x, m.height - 2) for x in range(1, m.height - 1)]  # terminal must be on rightside
    beg = random.choice(frame_list_left)
    end = random.choice(frame_list_right)
    return [beg, end]


def SameTree(m, p1, p2):
    p1 = m.m_trees[p1[0]][p1[1]]
    p2 = m.m_trees[p2[0]][p2[1]]
    if p1.find_root() == p2.find_root():
        return True
    else:
        return False


def adjlist(m, point):
    adlist = []
    if point[0] - 2 > 0:
        if not SameTree(m, point, (point[0] - 2, point[1])):  # if not in a same tree, add to adjacent list
            adlist.append((point[0] - 2, point[1]))  # up
    if point[0] + 2 < m.height:
        if not SameTree(m, point, (point[0] + 2, point[1])):
            adlist.append((point[0] + 2, point[1]))  # down
    if point[1] - 2 > 0:
        if not SameTree(m, point, (point[0], point[1] - 2)):
            adlist.append((point[0], point[1] - 2))  # left
    if point[1] + 2 > m.width:
        if not SameTree(m, point, (point[0], point[1] + 2)):
            adlist.append((point[0], point[1] + 2))  # right

    return adlist


def WallBreak(m, p1, p2):
    if p1[0] == p2[0] and p1[1] > p2[1]:
        m.m_trees[p1[0]][p1[1] - 1].attr = 0
    if p1[0] == p2[0] and p1[1] < p2[1]:
        m.m_trees[p1[0]][p1[1] + 1].attr = 0
    if p1[1] == p2[1] and p1[0] < p2[0]:
        m.m_trees[p1[0] + 1][p1[1]].attr = 0
    if p1[1] == p2[1] and p1[0] > p2[0]:
        m.m_trees[p1[0] - 1][p1[1]].attr = 0


def Union(m, p1, p2):
    p1 = m.m_trees[p1[0]][p1[1]]
    p2 = m.m_trees[p2[0]][p2[1]]
    p1_ancestor = p1.find_root()
    p2_ancestor = p2.find_root()
    if p1_ancestor.nodenum >= p2_ancestor.nodenum:
        p1_ancestor.add_node(p2_ancestor)
    else:
        p2_ancestor.add_node(p1_ancestor)


def changeb_e(m, b, e):
    m.m_trees[b[0]][b[1]].attr = 2
    m.m_trees[e[0]][e[1]].attr = 3


def proceed_up(m, b):
    p = (b[0]-1, b[1])
    if m.m_trees[p[0]][p[1]].attr != 1:
        delete(m, b)
        m.m_trees[p[0]][p[1]].attr = 2           #change to plane
        goto(p[0], p[1])
        print(moving_point)
        return p
    else: return b


def proceed_down(m, b):
    p = (b[0]+1, b[1])
    if m.m_trees[p[0]][p[1]].attr != 1:
        delete(m, b)
        m.m_trees[p[0]][p[1]].attr = 2
        goto(p[0], p[1])
        print(moving_point)
        return p
    else: return b


def proceed_left(m, b):
    p = (b[0], b[1]-1)
    if m.m_trees[p[0]][p[1]].attr != 1:
        delete(m, b)
        m.m_trees[p[0]][p[1]].attr = 2
        goto(p[0], p[1])
        print(moving_point)
        return p
    else: return b


def proceed_right(m, b):
    p = (b[0], b[1]+1)
    if m.m_trees[p[0]][p[1]].attr != 1:
        delete(m, b)
        m.m_trees[p[0]][p[1]].attr = 2
        goto(p[0], p[1])
        print(moving_point)
        return p
    else: return b


def delete(m, p):
    m.m_trees[p[0]][p[1]].attr = 0           #change to road
    goto(p[0], p[1])
    print(road)


def check(p1, p2):
    if p1 == p2:
        return 1
    else: return 0

wall = '#'
road = ' '
moving_point = '@'
termin = 'T'

def MazeGame():
    dimension = [2 * a + 1 for a in range(7, 15)]
    score = 0

    for k in dimension:
        maze = Map_of_Maze(k, k)
        beg_point = begin_end(maze)[0]
        end_point = begin_end(maze)[1]
        route_list = [(x, y) for x in range(maze.height) for y in range(maze.width) if x % 2 == 1 and y % 2 == 1]
        wait_list = route_list

        while len(wait_list) != 0:
            p = random.choice(wait_list)
            adj_list = adjlist(maze, p)
            if len(adj_list) != 0:
                p_adja = random.choice(adj_list)
                WallBreak(maze, p, p_adja)
                Union(maze, p, p_adja)
            elif len(adj_list) == 0:
                wait_list.pop(wait_list.index(p))
                if SameTree(maze, beg_point, end_point) == True:
                    break

        changeb_e(maze, beg_point, end_point)
        maze.print_maze()
        goto(3, 32)
        print('Welcome to maze game! Here are some instructions')
        goto(4, 32)
        print('Starting point: %s    Terminal point: %s    '% (beg_point, end_point))
        goto(5, 32)
        print("Controlling the '@' mark using 'w','s','a','d' to reach the terminal point 'T'")
        goto(6, 32)
        print('Press E if you want to exit. Good luck!')
        goto(8, 32)
        print('Your score : %d' % score)
        goto(0, 0)

        t = 1
        t_temp = 1
        while t:
            ch = msvcrt.getch()
            if ch == b'w':
                beg_point = proceed_up(maze, beg_point)
            if ch == b's':
                beg_point = proceed_down(maze, beg_point)
            if ch == b'd':
                beg_point = proceed_right(maze, beg_point)
            if ch == b'a':
                beg_point = proceed_left(maze, beg_point)
            if ch == b'e':
                t = 0
                t_temp = 0
                
            if check(beg_point, end_point) == 1:
                score = score + 100
                t = 0

        if t_temp == 0:
            break

        goto(8, 32)
        print('Your score : %d' % score)

    return score


def StartGame():
    sco = MazeGame()
    goto(10, 32)
    print('Game Finished. Final Score : %d' % sco)
    goto(11, 32)
    os.system('pause')


if __name__ == '__main__':
    StartGame()





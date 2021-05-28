import turtle
import numpy as np
import random

Row = 20
Column = 20
GridSize = 20


#  默认迷宫大小是20个x20个的，每个单元大小为20x20的像素

class Pos:  # pos类的位置是格子的左上角，像素位置
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        # 像素位置


class MatrixPos:  # 矩阵位置
    def __init__(self, ri=None, ci=None):
        self.ri = ri
        self.ci = ci


# ---------------------初始化窗口以及原点位置-------------------------------
Window = turtle.Screen()
Window.delay(1)
Window.bgcolor('lightblue')  # 方便起见，路的颜色为蓝色，即背景色为‘lightblue’
Window.setup(Column * GridSize, Row * GridSize)
Window.colormode(255)  # 颜色调节设置为（255,255,255）式样
InitialPos = Pos(-(Column * GridSize) / 2, (Row * GridSize) / 2)  # 定义初始坐标，原点在最左上角，turtle库默认原点在中心位置
# ---------------------------------------------------------------------------

# -----------------------将绘图指定turtle设为全局变量方便后续使用------------------
Wall = turtle.Turtle()
Wall.hideturtle()

Dot = turtle.Turtle()
Dot.hideturtle()

flag = turtle.Turtle()

Rocket = turtle.Turtle()
RocketImage = "rocket.gif"
Window.addshape(RocketImage)
Rocket.shape(RocketImage)  # 导入图片
Rocket.pensize(3)
Rocket.speed(3)
# ---------------------------------------------------------------------------

Orient = {'Up': (0, 1), 'Right': (1, 0), 'Down': (0, -1), 'Left': (-1, 0)}  # 定义字典方向


# Prim算法生成MazeList
def PrimCreateList(MazeList):
    Start = MatrixPos(1, 1)  # 默认初始起点为（1,1）
    # Flag = MatrixPos(18, 18)  # 终点
    stack = []
    MazeList[Start.ri][Start.ci] = 1
    '''
    为了实现起来方便，将是road的置为100，访问过一次加1，这样可以更方便的完成矩阵的设置'''
    stack.append(Start)
    while len(stack) is not 0:
        RandomChoice = random.choice(stack)  # 栈中随机选取一个wall，让其开通road
        if MazeList[RandomChoice.ri][RandomChoice.ci] == 1:
            # 当这个节点只被访问过一次就让他成为road
            MazeList[RandomChoice.ri][RandomChoice.ci] = 100
            Push(RandomChoice, stack, MazeList)
            stack.remove(RandomChoice)
        elif 1 < MazeList[RandomChoice.ri][RandomChoice.ci] < 100:
            # 如果这个节点访问多次，就在栈中删除他，保留他为wall
            stack.remove(RandomChoice)
    return MazeList


def Push(breakout, stack, MazeList):
    # 把breakout周围是wall的推进stack里面去
    shape = np.shape(MazeList)
    R = shape[0]
    C = shape[1]
    for toward in Orient:
        Direct = Orient[toward]
        NextPosRi = breakout.ri - Direct[1]
        NextPosCi = breakout.ci + Direct[0]
        NextPos = MatrixPos(NextPosRi, NextPosCi)
        if (NextPosCi is not 0 and NextPosCi is not C - 1) and (
                NextPosRi is not 0 and NextPosRi is not R - 1):  # ri or ci 是0的表示在边界，不进栈
            if MazeList[NextPos.ri][NextPosCi] < 100:  # 当这个不是road时才入栈
                IsDuplicate = bool(NextPos in stack)
                if IsDuplicate is False:  # 重复的不再入栈
                    stack.append(NextPos)
                MazeList[NextPos.ri][NextPosCi] = MazeList[NextPos.ri][NextPosCi] + 1
                # 访问过一次就加1


# ---------------------------地图部分函数---------------------------
def DrawWall(pos):  # 为提高运行速度，把画图的指向变量致为全局变量而不在函数中定义
    #  画一个格子的墙体
    x = pos.x
    y = pos.y
    Wall.penup()
    Wall.goto(x, y)
    Wall.pendown()
    v = random.randint(110, 180)
    Wall.color(v, v, v)
    Wall.begin_fill()
    for i in range(4):  # 旋转90度四次，填充围城的格子
        Wall.fd(GridSize)
        Wall.right(90)
    Wall.end_fill()


def DrawFlag(pos):
    x = pos.x + GridSize / 2
    y = pos.y - GridSize / 2
    flag.penup()
    flag.goto(x, y)  # 将flag位置移动至相应地方
    flag.pendown()
    FlagImage = "flag.gif"
    # Insert picture of flag
    Window.addshape(FlagImage)
    flag.shape(FlagImage)  # 导入图片


def DrawMaze(List):
    Window.tracer(0)
    for i in range(Row):
        for j in range(Column):
            x = InitialPos.x + GridSize * j
            y = InitialPos.y - GridSize * i
            location = Pos(x, y)
            Check = List[i][j]
            if Check == 0:
                DrawWall(location)
                #  elif Check is 1: 不处理，就是Road的情况，为简便不再写出DrawRoad函数
            elif Check == 3:  # 终点设为3
                DrawFlag(location)


# ----------------------------搜索--------------------------------
def DrawPath(ri, ci, color='gold'):
    x = InitialPos.x + GridSize * ci + GridSize / 2
    y = InitialPos.y - GridSize * ri - GridSize / 2
    Rocket.color(color)
    Rocket.goto(x, y)


# 采用DFS搜索时，为了动画美观，回溯节点时按原路返回，而不直接跳跃到该点
def DFSRecurse(List, ri, ci):
    if ci > Column or ri > Row:  # 超出索引范围
        return False
    elif List[ri][ci] == 0 or List[ri][ci] == -1:  # 撞墙或已经走过
        return False
    elif List[ri][ci] == 3:
        DrawPath(ri, ci)
        return True
    #  这是三类基本特殊情况，下面进入road开始搜索
    #  如果已经访问了这个格子，将这个值由1->-1做标识
    List[ri][ci] = -1
    DrawPath(ri, ci)
    for toward in Orient:
        Direct = Orient[toward]
        IsFound = DFSRecurse(List, ri - Direct[1], ci + Direct[0])  # 递归搜索
        if IsFound is True:
            return True
        else:
            DrawPath(ri, ci, 'black')
    return False


def DFSUnRecurse(List, ri, ci):
    Stack1 = [MatrixPos(ri, ci)]
    Stack2 = []
    '''
    这里为了回溯路径，1代表road，走过后若在这个点有多个方向可以走，修改成5
    如果只有一个方向，修改为6
    '''
    while Stack1 is not None:
        tem1 = Stack1.pop()
        DrawPath(tem1.ri, tem1.ci, 'gold')
        Stack2.append(tem1)
        cnt = 0
        for toward in Orient:
            Direct = Orient[toward]
            Next = List[tem1.ri - Direct[1]][tem1.ci + Direct[0]]
            if Next == 1:
                Stack1.append(MatrixPos(tem1.ri - Direct[1], tem1.ci + Direct[0]))
                List[tem1.ri - Direct[1]][tem1.ci + Direct[0]] = -1
                cnt = cnt + 1
            if Next == 3:
                DrawPath(tem1.ri - Direct[1], tem1.ci + Direct[0], 'gold')
                return True
        if cnt == 0:  # cnt ==0 表示四个方向都走不通，开始回溯
            List[tem1.ri][tem1.ci] = 6
            value = 6
            while value is 6:
                if not Stack2:
                    return False
                tem2 = Stack2.pop()
                DrawPath(tem2.ri, tem2.ci, 'black')
                value = List[tem2.ri][tem2.ci]
            Stack2.append(tem2)
            List[tem2.ri][tem2.ci] = List[tem2.ri][tem2.ci] - 1
        elif cnt == 1:
            List[tem1.ri][tem1.ci] = 6  # 只有一条路的修改tag=6
        elif cnt > 1:
            List[tem1.ri][tem1.ci] = 5 + cnt
        '''
        cnt大于有2,3两个值，表明路口分别有2，3个
        当cnt=1时，该节点值为6，表示只有一条路可以走
        当cnt=2时，该节点值为7，表示有2两路可以走
        ......
        因此在cnt=0时，回溯遍历已经走过值为6的路，当遇到值不为6的节点时
        让这个节点的值减1，访问另外一边，如此便是DFS的基本思想
        '''


if __name__ == '__main__':
    # -----------------设置迷宫矩阵-----------------------------
    MazeList = np.zeros((Row, Column))
    a = PrimCreateList(MazeList)
    # 采用Prim算法“开凿”road，先指定（1,1）为起点开凿，然后向四周破路，
    '''
    1.让迷宫全是墙.
    2.选一个单元格作为迷宫的通路，然后把它的邻墙放入列表
    3.当列表里还有墙时
    1.从列表里随机选一个墙，如果这面墙分隔的两个单元格只有一个单元格被访问过:
        1.从列表里随机选一个墙，如果这面墙分隔的两个单元格只有一个单元格被访问过
            1.那就从列表里移除这面墙，即把墙打通，让未访问的单元格成为迷宫的通路
            2.把这个格子的墙加入列表
        2.如果墙两面的单元格都已经被访问过，那就从列表里移除这面墙
    典型的递归算法
'''

    shape = np.shape(MazeList)
    R = shape[0]
    C = shape[1]
    for i in range(R):
        for j in range(C):
            if a[i][j] == 100:
                a[i][j] = 1
            else:
                a[i][j] = 0
    a[Row - 2][Column - 2] = 3

    a = a.tolist()  # numpy数据类型与list中的int不兼容，需要把numpy转化成list
    '''
    numpy中是
    a=
    [
    [0 0 0 0 0 0 0]
    [0 0 0 0 0 0 0]
    ]
    而list中
    a=
    [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
    ]
    后续DFS搜索由于函数传参，两个数据类型不兼容，所以需要把numpy转化成list
    '''
    # -----------------设置迷宫矩阵-----------------------------m
    DrawMaze(a)
    Window.tracer(1)  # 启用跟踪动画
    Rocket.penup()
    Rocket.goto(InitialPos.x + GridSize / 2 + 20, InitialPos.y - GridSize / 2 - 20)
    Rocket.pendown()
    #  需先把rocket移动到起始点位置，为方便计算，这里默认起点都是（1,1）
    # IsSuccess = DFSUnRecurse(a, 1, 1)  # 从（1,1）开始出发搜寻,递归搜索，方向为顺时针
    IsSuccess = DFSRecurse(a, 1, 1)  # 非递归搜索，方向为逆时针
    if IsSuccess is True:
        print('Success find flag')
    else:
        print("Fail to find flag")
    turtle.mainloop()

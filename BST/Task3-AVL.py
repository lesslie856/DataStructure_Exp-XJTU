from DrawBT import draw
import csv
import turtle


class TreeNode(object):  # 定义树节点
    def __init__(self, data=None, lch=None, rch=None, BF=0):
        self.data = data
        self.lch = lch
        self.rch = rch
        self.BF = BF
        # self.tag = 0  # 非递归后序遍历中用到的tag


class Traverse(object):
    def __init__(self):
        self.Order = []

    def RecursePreTraverse(self, node):
        if node is None:
            return None
        self.Order.append(node.data)
        self.RecursePreTraverse(node.lch)
        self.RecursePreTraverse(node.rch)
        return self.Order

    def RecurseInTraverse(self, node):
        if node is None:
            return None
        self.RecurseInTraverse(node.lch)
        self.Order.append(node.data)
        self.RecurseInTraverse(node.rch)
        return self.Order

    def RecursePostTraverse(self, node):
        if node is None:
            return None
        self.RecursePostTraverse(node.lch)
        self.RecursePostTraverse(node.rch)
        self.Order.append(node.data)
        return self.Order

    def LevelTraverse(self, node):
        queue = [node]
        while queue:
            cur_node = queue.pop(0)
            self.Order.append(cur_node.data)
            if cur_node.lch is not None:
                queue.append(cur_node.lch)
            if cur_node.rch is not None:
                queue.append(cur_node.rch)
        return self.Order

    def UnRecursePreTraverse(self, node):
        if node is None:
            return None
        s = Stack()
        while s.is_empty() is not True or node is not None:
            if node is not None:
                self.Order.append(node.data)
                s.push(node)
                node = node.lch
            else:
                node = s.pop()
                node = node.rch
        return self.Order

    def UnRecurseInTraverse(self, node):
        if node is None:
            return None
        s = Stack()
        while s.is_empty() is not True or node is not None:
            if node is not None:
                s.push(node)
                node = node.lch
            else:
                node = s.pop()
                self.Order.append(node.data)
                node = node.rch
        return self.Order

    def UnRecursePostTraverse(self, node):
        if node is None:
            return None
        s = Stack()
        while s.is_empty() is not True or node is not None:
            if node is not None:
                s.push(node)
                node.tag = 1
                node = node.lch
            else:
                node = s.pop()
                if node.tag != 2:
                    s.push(node)
                    node.tag = 2
                    node = node.rch
                else:  # 访问两次根节点，则说明左右子树都已访问完毕，访问根节点
                    self.Order.append(node.data)
                    node = None
        return self.Order


class StackNode(object):
    def __init__(self):
        self.data = TreeNode()
        self.rear = None


class Stack(object):  # 栈采用链式存储
    def __init__(self):
        self.top = None

    def is_empty(self):
        if self.top is None:
            return True
        else:
            return False

    def push(self, tree_node):
        p = StackNode()
        p.data = tree_node
        p.rear = None
        if self.is_empty():
            self.top = p
            self.top.rear = None
        else:
            p.rear = self.top
            self.top = p

    def pop(self):  # python 含垃圾回收机制，暂不考虑free节点空间
        if self.is_empty():
            return None
        else:
            cur = self.top
            self.top = cur.rear
            return cur.data


class AVL(object):
    def __init__(self, array):  # 初始化把列表所有值插入
        self.array = array
        self.Root = None
        self.InitAVL()

    '''python class 中,init初始化相当于可共用用地址,init调用函数时，函数中的变量直接会指向self实例属性地址'''

    def InitAVL(self):
        if len(self.array) is 0:
            print("the tree have no element!")
            exit(0)
        self.Root = TreeNode(self.array[0])
        for i in self.array[1:]:
            self.Insert(i)

    def GetNumOfLeaves(self, Root):
        if Root is None:
            return 0
        if Root.lch is None and Root.rch is None:
            return 1
        LeftNum = self.GetNumOfLeaves(Root.lch)
        RightNUm = self.GetNumOfLeaves(Root.rch)
        Num = LeftNum + RightNUm
        return Num

    def GetHeight(self, Root):
        if Root is None:
            return 0
        LHeight = self.GetHeight(Root.lch)
        RHeight = self.GetHeight(Root.rch)
        return max(LHeight, RHeight) + 1

    def UpdateBF(self, Root):
        LeftHeight = self.GetHeight(Root.lch)
        RightHeight = self.GetHeight(Root.rch)
        Root.BF = abs(LeftHeight - RightHeight)

    def Insert(self, data):
        if self.Root is None:
            self.Root = TreeNode(data)
        else:
            self.Root = self._Insert(data, self.Root)

    def _Insert(self, data, Root):  # 私有函数
        if Root is None:
            Root = TreeNode(data)
        elif data > Root.data:
            Root.rch = self._Insert(data, Root.rch)
            self.UpdateBF(Root)
            if Root.BF > 1:
                if data > Root.rch.data:  # RR
                    Root = self.RR(Root)
                else:  # RL
                    Root = self.RL(Root)
        elif data < Root.data:
            Root.lch = self._Insert(data, Root.lch)
            self.UpdateBF(Root)
            if Root.BF > 1:
                if data < Root.lch.data:
                    Root = self.LL(Root)
                else:
                    Root = self.LR(Root)
        return Root

    def GetLevelNodeNum(self, Root, k):
        if Root is None:
            return 0
        if k is 1:
            return 1
        Lnum = self.GetLevelNodeNum(Root.lch, k - 1)
        Rnum = self.GetLevelNodeNum(Root.rch, k - 1)
        return Lnum + Rnum

    #  平均查找长度由 sigma(高度x该高度下的节点数)/总节点个数
    def AvrFindPath(self):
        Height = self.GetHeight(self.Root)
        LevelNodeNum = []
        sigma = 0
        Path = 0
        for i in range(1, Height + 1, 1):
            LevelNodeNum.append(self.GetLevelNodeNum(self.Root, i))
            sigma = sigma + i * self.GetLevelNodeNum(self.Root, i)
        TotalNode = sum(LevelNodeNum)
        Path = sigma / TotalNode
        return Path

    def LL(self, Root):
        R_Root = Root
        tem = Root.lch.rch
        Root = Root.lch
        Root.rch = R_Root
        R_Root.lch = tem
        self.UpdateBF(Root)
        self.UpdateBF(R_Root)  # 只改变了两个结点位置，所以只要更新两个BF
        return Root

    def RR(self, Root):
        L_Root = Root
        tem = Root.rch.lch
        Root = Root.rch
        Root.lch = L_Root
        L_Root.rch = tem
        self.UpdateBF(Root)
        self.UpdateBF(L_Root)
        return Root

    def LR(self, Root):
        Root.lch = self.RR(Root.lch)
        Root = self.LL(Root)
        return Root

    def RL(self, Root):
        Root.rch = self.LL(Root.rch)
        Root = self.RR(Root)
        return Root


#  传入txt文件地址，返回列表，列表中元素类型为储存二叉树的列表
def DataRead(path):
    result = []
    with open(path, 'r') as f:
        for line in f.readlines():
            result.append([line.strip('\n')])
    for array in result:
        array[0] = eval(array[0])
    Datalist = []
    for array in result:
        Datalist.append(array[0])
    for i in range(0, len(Datalist)):
        Datalist[i] = list(Datalist[i])
    return Datalist


if __name__ == '__main__':
    path = 'BST.txt'

    # MyDataList 为导入数据
    MyDataList = DataRead(path)

    # OperateList 为操作数据
    # OperateList = []
    OperateList = MyDataList[3]

    # 创建AVL树
    MyAVL = AVL(OperateList)

    # 引入遍历类，遍历返回值为一列表
    my_traverse = Traverse()

    #  对my_bst进行中序遍历

    print("----------------------------------")
    Root1 = MyAVL.Root
    order1 = my_traverse.RecurseInTraverse(Root1)
    Distance = MyAVL.AvrFindPath()
    Distance = round(Distance, 2)
    print(order1)
    print(Distance)
    if len(OperateList) > 1:
        draw(Root1, 1, order1, Distance)

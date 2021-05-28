from DrawBT import draw


class TreeNode(object):  # 定义树节点
    def __init__(self, data=None, lch=None, rch=None):
        self.data = data
        self.lch = lch
        self.rch = rch
        self.tag = 0  # 非递归后序遍历中用到的tag


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


class BST(object):
    def __init__(self, array):  # 初始化把列表所有值插入
        self.array = array
        self.Root = None
        self.InitBST()

    '''python class 中,init初始化相当于可共用用地址,init调用函数时，函数中的变量直接会指向self实例属性地址'''

    def InitBST(self):
        if len(self.array) is 0:
            print("The Tree is None!")
            exit(0)
        self.Root = TreeNode(self.array[0])
        for i in self.array[1:]:
            self.InsertNode(i)

    def ExchangeNode(self, Root):
        if Root is None:
            return
        tem = Root.lch
        Root.lch = Root.rch
        Root.rch = tem
        self.ExchangeNode(Root.lch)
        self.ExchangeNode(Root.rch)

    # 递归查找data，返回判断值、data对应节点、data的父节点
    def Search(self, node, parent, data):  # parent指向node的父节点
        if node is None:
            return 0, node, parent
        elif data == node.data:
            return 1, node, parent
        elif data < node.data:
            return self.Search(node.lch, node, data)
        else:
            return self.Search(node.rch, node, data)

    #  利用search直接插入
    def InsertNode(self, data):  # 基于Search函数的插入
        gen = self.Root
        flag, p, p_parent = self.Search(gen, gen, data)
        if flag is 0:  # 已经的存在值（flag=1）不再插入
            New_node = TreeNode(data)
            if data < p_parent.data:
                p_parent.lch = New_node
            else:
                p_parent.rch = New_node
        else:
            return None

    ''' # 递归插入
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
       elif data < Root.data:
           Root.lch = self._Insert(data, Root.lch)
       return Root'''

    # 找到前驱的值
    def FindPrevValue(self, data):
        flag, p, p_parent = self.Search(self.Root, self.Root, data)
        if flag is 0:
            return None
        traverse = Traverse()
        InOrder = traverse.RecurseInTraverse(self.Root)
        cur_position = InOrder.index(data)
        if cur_position is 0:  # 首元素返回None
            return None
        PrevValue = InOrder[cur_position - 1]
        return PrevValue

    def FindPostValue(self, data):
        flag, p, p_parent = self.Search(self.Root, self.Root, data)
        if flag is 0:
            return None
        traverse = Traverse()
        InOrder = traverse.RecurseInTraverse(self.Root)
        cur_position = InOrder.index(data)
        if cur_position is len(InOrder) - 1:  # 末尾元素返回None
            return None
        PostValue = InOrder[cur_position + 1]
        return PostValue

    #  移除data的节点，并保持BST的完整性，这里用后继替代
    def Remove(self, data):
        flag, p, p_parent = self.Search(self.Root, self.Root, data)  # p为data的节点
        if flag is 0:
            print("无%f" % data)
            return 0
        if p.lch is None and p.rch is None:
            '''注意，Python语言里不能直接让 p=None，这样只是让p的地址为none，
            而不是让p代表的地址为none，因此需先访问父节点，再让父节点的下一级指向None
            忽略释放p节点的空间，Python自带gc回收机制'''
            if p_parent.lch == p:
                p_parent.lch = None
            else:
                p_parent.rch = None

        elif p.lch is not None and p.rch is None:
            if p_parent.lch == p:
                p_parent.lch = p.lch
            else:
                p_parent.rch = p.lch
        elif p.lch is None and p.rch is not None:
            if p_parent.lch == p:
                p_parent.lch = p.rch
            else:
                p_parent.rch = p.rch
        # 让p的父节点指向p的左儿子
        elif p.rch is not None and p.lch is not None:
            Post = self.FindPostValue(data)
            self.Remove(Post)
            p.data = Post
        return 1
        #  后继顶替
        '''
            Prev = self.FindPrevValue(data)
            self.Remove(Prev)
            p.data = Prev
        '''
        #  前驱顶替

    #  获取包括该节点在内的高度
    def GetHeight(self, Root):
        if Root is None:
            return 0
        LHeight = self.GetHeight(Root.lch)
        RHeight = self.GetHeight(Root.rch)
        return max(LHeight, RHeight) + 1

    #  获取第k层的节点数
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
    OperateList = MyDataList[3]

    # 创建BST树
    my_bst = BST(OperateList)

    # 引入遍历类，遍历返回值为一列表
    my_traverse = Traverse()

    #  对my_bst进行中序遍历
    print("----------------------------------")
    Root1 = my_bst.Root
    order1 = my_traverse.RecurseInTraverse(Root1)
    print(order1)
    if len(order1) > 1:
        draw(Root1, 1, order1, None)

    # my_traverse.Order=[] # Traverse使用后需对类中order置空
    my_traverse.Order = []

    # 查找
    FindData = int(input("Input the data you want search:\n"))  # 默认查找元素是整型的
    # 若存在含x的结点，则删除该结点，若无输出“无x"
    flag = my_bst.Remove(FindData)
    if flag is 1:
        Root2 = my_bst.Root
        order2 = my_traverse.RecurseInTraverse(Root2)
        print("----------------------------------")
        print(order2)
        AverDis = round(my_bst.AvrFindPath(), 2)
        print(AverDis)
        if len(order2) > 1:
            draw(Root2, 2, order2, AverDis)

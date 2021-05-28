class StaticTreeNode:  # lch,rch分别是下标值
    def __init__(self, data=None):
        self.data = data
        self.lch = 0
        self.rch = 0


Maxsize = 200


class Traverse(object):
    def __init__(self):
        self.Order = []

    def RecurseInTraverse(self, BSTList, Root):
        if Root.data is None:
            return
        self.RecurseInTraverse(BSTList, BSTList[Root.lch])
        self.Order.append(Root.data)
        self.RecurseInTraverse(BSTList, BSTList[Root.rch])
        return self.Order


class BST:
    def __init__(self, DataList):  # 静态链表存储，第BSTList[1]为根节点，
        # 后序按顺序表下标存节点
        self.BSTList = []
        i = 0
        while i < Maxsize:
            self.BSTList.append(None)
            i = i + 1
        self.Root = None
        self.DataList = DataList
        self.InitBST()

    def InitBST(self):
        self.BSTList[0] = StaticTreeNode(None)  # 标识
        if len(self.DataList) is 0:
            print("NO ELEMENT!")
            exit(0)
        self.Root = StaticTreeNode(self.DataList[0])
        self.BSTList[1] = self.Root
        for i in self.DataList[1:]:
            self.Insert(i)

    def Insert(self, data):
        if self.Root is None:
            self.Root = StaticTreeNode()
        else:
            self.Root = self._Insert(data, self.Root)

    def _Insert(self, data, Root):  # 私有函数
        if Root is None:
            Root = StaticTreeNode(data)
        elif data > Root.data:
            Root.rch = 2 * self.BSTList.index(Root) + 1
            self.BSTList[Root.rch] = self._Insert(data, self.BSTList[Root.rch])
        elif data < Root.data:
            Root.lch = 2 * self.BSTList.index(Root)
            self.BSTList[Root.lch] = self._Insert(data, self.BSTList[Root.lch])
        return Root

    def GetHeight(self, Root):
        if Root.data is None:
            return 0
        LHeight = self.GetHeight(self.BSTList[Root.lch])
        RHeight = self.GetHeight(self.BSTList[Root.rch])
        return max(LHeight, RHeight) + 1

    #  获取第k层的节点数
    def GetLevelNodeNum(self, root, k):
        if root.data is None:
            return 0
        if k is 1:
            return 1
        Lnum = self.GetLevelNodeNum(self.BSTList[root.lch], k - 1)
        Rnum = self.GetLevelNodeNum(self.BSTList[root.rch], k - 1)
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
        return round(Path, 2)

    def Search(self, node, parent, data):  # parent指向node的父节点
        if node.data is None:
            return 0, node, parent
        elif data == node.data:
            return 1, node, parent
        elif data < node.data:
            return self.Search(self.BSTList[node.lch], node, data)
        else:
            return self.Search(self.BSTList[node.rch], node, data)

    def FindPostValue(self, data):
        flag, p, p_parent = self.Search(self.Root, self.Root, data)
        if flag is 0:
            return None
        traverse = Traverse()
        InOrder = traverse.RecurseInTraverse(self.BSTList, self.Root)
        cur_position = InOrder.index(data)
        if cur_position is len(InOrder) - 1:  # 末尾元素返回None
            return None
        PostValue = InOrder[cur_position + 1]
        return PostValue

    def Remove(self, data):
        flag, p, p_parent = self.Search(self.Root, self.Root, data)  # p为data的节点
        if flag is 0:
            print("无%f" % data)
            return 0
        if p.lch is 0 and p.rch is 0:
            if self.BSTList[p_parent.lch] == p:
                p_parent.lch = 0
            else:
                p_parent.rch = 0

        elif p.lch is not 0 and p.rch is 0:
            if self.BSTList[p_parent.lch] == p:
                p_parent.lch = p.lch
            else:
                p_parent.rch = p.lch
        elif p.lch is 0 and p.rch is not 0:
            if self.BSTList[p_parent.lch] == p:
                p_parent.lch = p.rch
            else:
                p_parent.rch = p.rch
        # 让p的父节点指向p的左儿子
        elif p.rch is not 0 and p.lch is not 0:
            Post = self.FindPostValue(data)
            self.Remove(Post)
            p.data = Post
        return 1
        #  后继顶替


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
    path = 'C:/Users/周海鹏/Desktop/BST.txt'

    # MyDataList 为导入数据
    MyDataList = DataRead(path)

    # OperateList 为操作数据
    OperateList = MyDataList[0]

    # 创建BST树
    my_bst = BST(OperateList)

    # 引入遍历类，遍历返回值为一列表
    my_traverse = Traverse()

    #  对my_bst进行中序遍历
    print("----------------------------------")
    Root1 = my_bst.Root
    BSTList = my_bst.BSTList
    order1 = my_traverse.RecurseInTraverse(BSTList, Root1)
    print(order1)

    # my_traverse.Order=[] # Traverse使用后需对类中order置空
    my_traverse.Order = []

    # 查找
    FindData = int(input("Input the data you want search:\n"))  # 默认查找元素是整型的
    # 若存在含x的结点，则删除该结点，若无输出“无x"
    flag = my_bst.Remove(FindData)
    if flag is 1:
        Root2 = my_bst.Root
        order2 = my_traverse.RecurseInTraverse(BSTList, Root2)
        print("----------------------------------")
        print(order2)
        AverDis = round(my_bst.AvrFindPath(), 2)
        print(AverDis)

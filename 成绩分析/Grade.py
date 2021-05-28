import hashlib
import math
from numpy import *


def Upgrade(Subject):
    GPA_Perfect = 0
    GPA_Good = 0
    GPA_Normal = 0
    GPA_Pass = 0
    GPA_Bad = 0
    for grade in Subject:  # 基于哈夫曼思想设计if-else语句
        if 80 <= grade < 90:
            GPA_Good = GPA_Good + 1
        elif 70 <= grade < 80:
            GPA_Normal = GPA_Normal + 1
        elif grade >= 90:
            GPA_Perfect = GPA_Perfect + 1
        elif 60 <= grade < 70:
            GPA_Pass = GPA_Pass + 1
        elif grade < 60:
            GPA_Bad = GPA_Bad + 1
    return GPA_Perfect, GPA_Good, GPA_Normal, GPA_Pass, GPA_Bad


def Analyse(Stu):
    Math = AnalyseSubject()
    English = AnalyseSubject()
    DataStructure = AnalyseSubject()
    stumath = []
    stuenglish = []
    studatastrcture = []
    for student in Stu:
        stumath.append(student.Math)
        stuenglish.append(student.English)
        studatastrcture.append(student.DataStructure)
    Math.GPA_Perfect, Math.GPA_Good, Math.GPA_Normal, Math.GPA_Pass, Math.GPA_Bad = Upgrade(stumath)
    English.GPA_Perfect, English.GPA_Good, English.GPA_Normal, English.GPA_Pass, English.GPA_Bad = Upgrade(stuenglish)
    DataStructure.GPA_Perfect, DataStructure.GPA_Good, DataStructure.GPA_Normal, DataStructure.GPA_Pass, DataStructure.GPA_Bad = Upgrade(
        studatastrcture)
    Math.Max = max(stumath)
    Math.Min = min(stumath)
    Math.Average = mean(stumath)
    English.Max = max(stuenglish)
    English.Min = min(stuenglish)
    English.Average = mean(stuenglish)
    DataStructure.Max = max(studatastrcture)
    DataStructure.Min = min(studatastrcture)
    DataStructure.Average = mean(studatastrcture)
    file = open('Analyse.txt', 'w')
    file.write('科目  最高分  最低分  平均分 \n')
    file.write('Math  %d  %d  %f \n' % (Math.Max, Math.Min, Math.Average))
    file.write('English  %d  %d  %f \n' % (English.Max, English.Min, English.Average))
    file.write('DataStructure  %d  %d  %f \n' % (DataStructure.Max, DataStructure.Min, DataStructure.Average))
    file.write('--------------------------------------------\n')
    file.write('科目   90-100   80-89   70-79   60-69   不及格\n ')
    file.write('English %d   %d     %d       %d      %d  \n' % (
        English.GPA_Perfect, English.GPA_Good, English.GPA_Normal, English.GPA_Pass, English.GPA_Bad))
    file.write('Math  %d     %d     %d       %d      %d  \n' % (
        Math.GPA_Perfect, Math.GPA_Good, Math.GPA_Normal, Math.GPA_Pass, Math.GPA_Bad))
    file.write('DS    %d     %d      %d      %d      %d  \n' % (
        DataStructure.GPA_Perfect, DataStructure.GPA_Good, DataStructure.GPA_Normal, DataStructure.GPA_Pass,
        DataStructure.GPA_Bad))
    file.close()


class AnalyseSubject:
    def __init__(self):
        self.GPA_Perfect = 0
        self.GPA_Good = 0
        self.GPA_Normal = 0
        self.GPA_Pass = 0
        self.GPA_Bad = 0
        self.Max = 0
        self.Min = 0
        self.Average = 0


class Person:
    def __init__(self, StuNum=None, Name=None, English=None, Math=None, DataStructure=None):
        self.StuNum = StuNum
        self.Name = Name
        self.English = English
        self.Math = Math
        self.DataStructure = DataStructure
        self.AverGrade = round((self.Math + self.English + self.DataStructure) / 3, 2)
        self.Next = None  # 后续哈希查找时需采用的链地址法


def PutInformationToPerson(Sentence):  # 认为键入数据是正确形式
    AfterSplit = Sentence.split(' ')
    for i in range(2, 5):
        AfterSplit[i] = int(AfterSplit[i])
    Stu = Person(AfterSplit[0], AfterSplit[1], AfterSplit[2], AfterSplit[3], AfterSplit[4])
    return Stu


def ReadKey():
    print("请按 学号、姓名、英语成绩、数学成绩、数据结构成绩 的顺序键入学生信息\n"
          "按回车键进行下一个输入，注意：请用空格将不同信息分隔开！\n"
          "输入 exit 以结束输入")
    tem = None
    file = open('学生成绩.txt', 'w', encoding='UTF-8')
    while tem != 'exit':
        tem = str(input('请输入信息：'))
        if tem != 'exit':
            file.write(tem + '\n')
    file.close()


def LoadStu(path):
    result = []
    with open(path, 'r', encoding="UTF-8") as f:
        Lines = f.readlines()
        for line in Lines:
            result.append([line.strip('\n')])
    Stu = []
    for student in result:
        Stu.append(PutInformationToPerson(student[0]))
    return Stu


def PartitionEnglish(Stu, low, high):
    i = (low - 1)  # 最小元素索引
    pivot = Stu[high].English

    for j in range(low, high):

        # 当前元素小于或等于 pivot
        if Stu[j].English >= pivot:
            i = i + 1
            Stu[i], Stu[j] = Stu[j], Stu[i]

    Stu[i + 1], Stu[high] = Stu[high], Stu[i + 1]
    return i + 1


def SortByEnglish(Stu, low, high):
    if low < high:
        pi = PartitionEnglish(Stu, low, high)
        SortByEnglish(Stu, low, pi - 1)
        SortByEnglish(Stu, pi + 1, high)
    file = open('EnglishRank.txt', 'w')
    file.write('学号  姓名  EnglishGrade\n')
    for Rank in Stu:
        file.write('%s  %s  %d\n' % (Rank.StuNum, Rank.Name, Rank.English))
    file.close()


def heapify(Stu, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and Stu[i].Math > Stu[l].Math:
        largest = l
    if r < n and Stu[largest].Math > Stu[r].Math:
        largest = r
    if largest != i:
        Stu[i], Stu[largest] = Stu[largest], Stu[i]  # 交换
        heapify(Stu, n, largest)


def SortByMath(Stu):
    n = len(Stu)
    for i in range(n, -1, -1):
        heapify(Stu, n, i)

        # 一个个交换元素
    for i in range(n - 1, 0, -1):
        Stu[i], Stu[0] = Stu[0], Stu[i]  # 交换
        heapify(Stu, i, 0)
    file = open('MathRank.txt', 'w')
    file.write('学号  姓名  MathGrade\n')
    for Rank in Stu:
        file.write('%s  %s  %d\n' % (Rank.StuNum, Rank.Name, Rank.Math))
    file.close()


def PartitionDataStructure(Stu, low, high):
    i = (low - 1)  # 最小元素索引
    pivot = Stu[high].DataStructure

    for j in range(low, high):

        # 当前元素小于或等于 pivot
        if Stu[j].DataStructure > pivot:
            i = i + 1
            Stu[i], Stu[j] = Stu[j], Stu[i]

    Stu[i + 1], Stu[high] = Stu[high], Stu[i + 1]
    return i + 1


def SortByDataStructure(Stu, low, high):
    if low < high:
        pi = PartitionDataStructure(Stu, low, high)
        SortByDataStructure(Stu, low, pi - 1)
        SortByDataStructure(Stu, pi + 1, high)
    file = open('DataStructureRank.txt', 'w')
    file.write('学号  姓名  DataStructureGrade\n')
    for Rank in Stu:
        file.write('%s  %s  %d\n' % (Rank.StuNum, Rank.Name, Rank.DataStructure))
    file.close()


def heapify2(Stu, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and Stu[i].AverGrade > Stu[l].AverGrade:
        largest = l
    if r < n and Stu[largest].AverGrade > Stu[r].AverGrade:
        largest = r
    if largest != i:
        Stu[i], Stu[largest] = Stu[largest], Stu[i]  # 交换
        heapify2(Stu, n, largest)


def SortByAverGrade(Stu):
    n = len(Stu)
    for i in range(n, -1, -1):
        heapify2(Stu, n, i)

        # 一个个交换元素
    for i in range(n - 1, 0, -1):
        Stu[i], Stu[0] = Stu[0], Stu[i]  # 交换
        heapify2(Stu, i, 0)
    file = open('AverGradeRank.txt', 'w')
    file.write('学号  姓名  AverGrade\n')
    for Rank in Stu:
        file.write('%s  %s  %f\n' % (Rank.StuNum, Rank.Name, Rank.AverGrade))
    file.close()


def ShowGPA(person):
    print("学号    姓名  英语成绩   数学成绩   DS成绩  ")
    print("%s     %s    %d        %d        %d" % (
        person.StuNum, person.Name, person.English, person.Math, person.DataStructure))


# ---------------------基于遍历搜索，效率低，当元素不可比较时查找次数为 N-----------------

def SearchByID(ID, stu):
    Find = []
    for S in stu:
        if S.StuNum == ID:
            Find.append(S)
    if len(Find) is 0:
        print("没有 %s 的信息！" % ID)
    for F in Find:
        print('学号为：%s 的学生，信息和成绩如下：' % F.StuNum)
        ShowGPA(F)


def SearchByName(name, stu):
    Find = []
    for S in stu:
        if S.Name == name:
            Find.append(S)
    if len(Find) is 0:
        print("没有 %s 的信息！" % name)
    else:
        print('姓名为  %s 的学生，信息和成绩如下：' % name)
        for F in Find:
            ShowGPA(F)


# -------------------------Hash搜索-----------------------------------------
def GetPrim(n):
    Prime = []
    for num in range(0, n + 1):
        if num > 1:
            for i in range(2, num):
                if (num % i) == 0:
                    break
            else:
                Prime.append(num)
    return Prime[len(Prime) - 1]


def HashID(Stu, Prime):
    n = len(Stu)
    HashTable = [None] * n  # 开辟相同大小空间的哈希表
    for student in Stu:
        Key = int(student.StuNum) % Prime  # 选取较小的素数做除数,好处是链地址搜索时可以防止越界
        # 默认这里ID是数字型的不带字母，否则int（）会出错
        if HashTable[Key] is None:
            HashTable[Key] = student
        else:
            tem = HashTable[Key]
            while HashTable[Key].Next is not None:
                tem = tem.Next
            tem.Next = student

    return HashTable


def HashSearchID(ID, hashtable, prime):
    Key = int(ID) % prime
    tem = hashtable[Key]
    cnt = 1  # 设置计数器检验搜索次数，以搜索完
    while tem.StuNum != ID:
        tem = tem.Next
        cnt = cnt + 1
        if tem is None:
            return False
    return tem, cnt


if __name__ == '__main__':
    # ReadKey()  # 以'学生成绩.txt'存入当前目录
    stu = LoadStu('成绩.txt')
    Prime = GetPrim(len(stu))  # 临近的素数，用于哈希搜索
    n = len(stu)
    # -------------------堆排序----------------
    SortByMath(stu)
    SortByAverGrade(stu)
    # --------------------快速排序--------------
    SortByEnglish(stu, 0, n - 1)
    SortByDataStructure(stu, 0, n - 1)

    Analyse(stu)

    HashTable = HashID(stu, Prime)  # 哈希表
    while choose != 'exit':
        print("************************************************************")
        print("****请输入 1 表示用姓名查找，输入 2 用学号查找，输入 exit 退出查找***")
        print("************************************************************")
        choose = str(input('请输入：'))
        if choose == '1':
            print('-------------姓名查找--------------')
            name = str(input('请输入姓名：'))
            SearchByName(name, stu)
        elif choose == '2':
            print('-------------学号查找--------------')
            ID = str(input('请输入学号：'))  # 禁止输入除数字外的其他字符，否则会转化失败！
            SearchByID(ID, stu)  # 遍历搜索
            print('-------------学号查找--------------')
            '''ID = str(input('请输入学号：'))  # 禁止输入除数字外的其他字符，否则会转化失败！
            result = HashSearchID(ID, HashTable, Prime)
            if result is not False:
                ShowGPA(result[0])
                print("搜索次数为%d" % result[1])
            else:
                print("查无此人！")
        else:
            print("请输入正确数字！\n")'''

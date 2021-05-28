class Car:
    def __init__(self, licence=None, pos=None):
        self.licence = licence
        self.pos = pos
        self.next = None


class Park:
    def __init__(self):
        self.top = None
        self.ParkNum = 0
        self.BufferRoad = []
        self.PaveNum = 0
        self.check1 = []
        self.check2 = []
        self.Car1Num = []
        self.Car2Num = []

    def IsParkEmpty(self):
        if self.top is None:
            return True
        else:
            return False

    def IsParkFull(self):
        if self.ParkNum is 5:  # 设定最多5个车位
            return True
        else:
            return False

    def Come(self, car):
        print("\n----------------------------------------------")
        if self.IsParkEmpty():
            self.top = car
            self.ParkNum = self.ParkNum + 1
            car.pos = self.ParkNum
            self.Car1Num.append(car.licence)
            print("%s已经移动至停车场的第%d个位置" % (car.licence, car.pos))
        elif not self.IsParkFull():
            car.next = self.top
            self.top = car
            self.ParkNum = self.ParkNum + 1
            car.pos = self.ParkNum
            self.check1.append(car)
            self.Car1Num.append(car.licence)
            car.pos = self.ParkNum
            print("%s已经移动至停车场的第%d个位置" % (car.licence, car.pos))
        else:
            print("停车场车位已满，%s已进入便道等候" % car.licence)
            self.BufferRoad.append(car)
            self.PaveNum = self.PaveNum + 1
            car.pos = self.PaveNum
            self.check2.append(car)
            self.Car2Num.append(car.licence)
            car.pos = self.PaveNum
            print("%s已经移动至临时车道的第%d个位置" % (car.licence, car.pos))

    def Leave(self, car):
        print("\n----------------------------------------------")
        if car.licence in self.Car1Num:
            tem = self.top
            container = []
            if car.licence != tem.licence:
                while car.licence != tem.licence:
                    container.append(tem)
                    tem.pos = tem.pos - 1
                    print("牌照为%s的汽车暂时退出停车位" % tem.licence)
                    tem = tem.next
            print("牌照为%s的汽车从停车场开走" % tem.licence)
            self.Car1Num.remove(car.licence)
            self.ParkNum = self.ParkNum - 1
            if len(container) is not 0:
                replace = container.pop()
                replace.next = tem.next
                print("牌照为%s的汽车停回%d位置" % (replace.licence, replace.pos))
                while len(container) is not 0:
                    replace = container.pop()
                    print("牌照为%s的汽车停回%d位置" % (replace.licence, replace.pos))
                if len(self.BufferRoad) is not 0:
                    new = self.BufferRoad.pop(0)
                    self.Come(new)
            elif len(container) is 0:
                self.top = tem.next
                if len(self.BufferRoad) is not 0:
                    new = self.BufferRoad.pop(0)
                    self.Come(new)


def Display(stack):
    ParkNum = stack.ParkNum
    top = stack.top
    print("-----------------停车场情况-----------------------------")
    if stack.IsParkFull is True:
        for i in range(5):
            print("第%d个位置的车牌号为%s" % (top.pos, top.licence))
            top = top.next
    else:
        for i in range(5, ParkNum, -1):
            print("第%d个位置是空的" % i)
        for i in range(ParkNum):
            print("停车场第%d个位置的车牌号为%s" % (top.pos, top.licence))
            top = top.next
    print("----------------便道情况-------------------------------")
    if len(stack.BufferRoad) is 0:
        print("没有车在便道上")
    else:
        for i in range(len(stack.BufferRoad)):
            print("便道上第%d个位置是车牌号为%s的车辆" % (i + 1, stack.BufferRoad[i].licence))


if __name__ == '__main__':
    MyPark = Park()
    print("-------------------停车场管理系统--------------------")
    print("现在你可以开始进行功能选择操作：")
    k = 0  # 初始化
    while k is not '4':
        print("************************************************")
        print("功能1：车辆进入停车场\n功能2：车辆从停车场内离开\n功能3：展示停车场和便道的情况\n功能4：退出")
        k = str(input("\n请输入选项1,2,3,4："))
        if k == '1':
            tem = str(input("请输入要进入停车场的车牌号:"))
            if tem in MyPark.Car1Num or tem in MyPark.Car2Num:
                print("%s已经在便道或停车场中，请输入正确的车牌号！" % tem)
            else:
                vehicle = Car(tem)
                MyPark.Come(vehicle)
        elif k == '2':
            LeaveNum = str(input("请输入要离开停车场的车牌号:"))
            if LeaveNum not in MyPark.Car1Num:
                print("请输入正确的车牌号！")
            else:
                LeaveCar = Car(LeaveNum)
                MyPark.Leave(LeaveCar)

        elif k == '3':
            Display(MyPark)
        elif k not in ['1', '2', '3', '4']:
            print("------------请输入正确的数字！------------------")

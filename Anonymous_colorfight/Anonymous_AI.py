# You need to import colorfight for all the APIs
import colorfight


class Mainbody:
    aList = []
    before = [[],[],[]]
    goldList = []
    start1 = 0
    start2 = 0
    start3 = 0
    start4 = 0


    def adjacent(self):
        #for x in range((g.width) -1,0,-1): # right
        for x in range(g.width): # left
            #for y in range((g.height) -1,0,-1): # down
            for y in range(g.height): # up
                c = g.GetCell(x,y)
                if c.owner == g.uid:
                    adjacent1 = g.GetCell(x + 1,y)
                    adjacent2 = g.GetCell(x - 1,y)
                    adjacent3 = g.GetCell(x,y + 1)
                    adjacent4 = g.GetCell(x,y - 1)
                    #if c.cellType == "energy":
                        #g.BuildBase(x, y)
                    #if c.isBase == True:
                        #mybase = [x,y]
                        #m.defendbase(mybase)
                    if c.cellType == "gold":
                        g.BuildBase(x, y)
                    if adjacent1 != None and adjacent1.owner != g.uid:
                        self.aList.append([x + 1, y])
                    if adjacent2 != None and adjacent2.owner != g.uid:
                        self.aList.append([x - 1, y])
                    if adjacent3 != None and adjacent3.owner != g.uid:
                        self.aList.append([x, y + 1])
                    if adjacent4 != None and adjacent4.owner != g.uid:
                        self.aList.append([x, y - 1])

    def attack(self):
        for i in self.aList:
            taketime = 0
            c = g.GetCell(i[0], i[1])

            adjacent1 = g.GetCell(i[0] + 1, i[1])
            adjacent2 = g.GetCell(i[0] - 1, i[1])
            adjacent3 = g.GetCell(i[0], i[1] + 1)
            adjacent4 = g.GetCell(i[0], i[1] - 1)
            if adjacent1 != None and adjacent1.owner == g.uid:
                taketime = taketime + 1
            if adjacent2 != None and adjacent2.owner == g.uid:
                taketime = taketime + 1
            if adjacent3 != None and adjacent3.owner == g.uid:
                taketime = taketime + 1
            if adjacent4 != None and adjacent4.owner == g.uid:
                taketime = taketime + 1

            comp = c.takeTime * (1 - (taketime - 1) * 0.25)
            i.append(comp)
        for i in self.aList:
            if i[2] > 0:
                optimal = [i]
                break
        for i in self.aList:
            if i[2] > 0 and int(i[2]) < int(optimal[0][2]) + 10:
                taking = g.GetCell(i[0], i[1])
                if taking.cellType == "gold" or taking.cellType == "energy":
                    optimal = [i]
                    break

            if i[2] > 0 and int(i[2]) < int(optimal[0][2]):
                optimal = [i]
        self.sign = 0
        if self.before != [[], [], []]:
            for i in self.before:
                if i != [] and i[0] == optimal[0][0] and i[1] == optimal[0][1]:
                    self.sign = 1

        print(optimal)
        if self.sign == 0:
            if (g.AttackCell(optimal[0][0], optimal[0][1]))[0] == True:
                self.before.append(optimal[0])
                del self.before[0]
                # g.Refresh()
        self.aList = []
        optimal = []

    def defendbase(self,mybase):
        self.value = 0
        adjacent1 = g.GetCell(mybase[0] + 1, mybase[1])
        adjacent2 = g.GetCell(mybase[0] - 1, mybase[1])
        adjacent3 = g.GetCell(mybase[0], mybase[1] + 1)
        adjacent4 = g.GetCell(mybase[0], mybase[1] - 1)
        if adjacent1 != None and adjacent1.owner != g.uid and adjacent1.owner != 0:
            self.value = self.value + 1
        if adjacent2 != None and adjacent2.owner != g.uid and adjacent2.owner != 0:
            self.value = self.value + 1
        if adjacent3 != None and adjacent3.owner != g.uid and adjacent3.owner != 0:
            self.value = self.value + 1
        if adjacent4 != None and adjacent4.owner != g.uid and adjacent4.owner != 0:
            self.value = self.value + 1
        if self.value >=3:
            g.Boom(mybase[0], mybase[1], "square", "attack")
            while(m.start(mybase)):
                m.start(mybase)


    def start(self,mybase):
        if mybase != None:
            adjacent1 = g.GetCell(mybase[0] + 1, mybase[1])
            adjacent2 = g.GetCell(mybase[0] - 1, mybase[1])
            adjacent3 = g.GetCell(mybase[0], mybase[1] + 1)
            adjacent4 = g.GetCell(mybase[0], mybase[1] - 1)
            if adjacent1 != None and adjacent1.owner != g.uid:
                if (g.AttackCell(mybase[0] + 1,mybase[1]))[0] == True:
                    return True
                    #g.Refresh()
            if adjacent2 != None and adjacent2.owner != g.uid:
                if (g.AttackCell(mybase[0] - 1,mybase[1]))[0] == True:
                    return True
                    #g.Refresh()
            if adjacent3 != None and adjacent3.owner != g.uid:
                if (g.AttackCell(mybase[0],mybase[1] + 1))[0] == True:
                    return True
                    #g.Refresh()
            if adjacent4 != None and adjacent4.owner != g.uid:
                if (g.AttackCell(mybase[0],mybase[1] - 1))[0] == True:
                    return True
                    #g.Refresh()
            return False

g = colorfight.Game()
g.JoinGame('Anonymous')
m = Mainbody()
#g.BuildBase(7,9)
while True:
    #m.start(None)
    m.adjacent()
    m.attack()
    g.Refresh()
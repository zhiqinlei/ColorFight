import colorfight
from time import sleep

class Mainbody:
    def __init__(self):
        self.attackable = []
        self.before = [[]]
        self.energy = []
        self.gold = []
        self.cell = []
        self.ownCell = []
        self.ownEnergy = []

    # detect all gold and energy cells
    def special(self):
        for x in range(g.width):
            for y in range(g.height):
                c = g.GetCell(x, y)
                if c.cellType == "gold":
                    self.gold.append([x, y])
                if c.cellType == "energy":
                    self.energy.append([x, y])

    # detect all gold cells
    def Gold(self):
        self.egold = []
        self.eenergy = []
        #self.mgold = []
        #self.menergy = []
        for i in self.gold:
            c = g.GetCell(i[0], i[1])
            if c.owner != g.uid:
                self.egold.append([i[0], i[1]])
        for i in self.energy:
            c = g.GetCell(i[0], i[1])
            if c.owner != g.uid:
                self.eenergy.append([i[0], i[1]])
            elif g.baseNum < 3 and g.gold > 60:
                g.BuildBase(i[0], i[1])
                self.ownEnergy.append([i[0],i[1]])
            else:
                self.ownEnergy.append([i[0],i[1]])

    # detect all attackable cell
    # detect all bases
    def detect(self):
        self.attackable = []
        self.ebase = []
        self.mybase = []
        self.base = []
        for x in self.cell:
            c = g.GetCell(x[0],x[1])
            # first store all own cell inside the list
            if c.owner == g.uid:
                self.ownCell.append([x[0],x[1]])
                if c.isBase == True:
                    self.mybase.append([x[0], x[1]])
                adjacent1 = g.GetCell(x[0] + 1, x[1])
                adjacent2 = g.GetCell(x[0] - 1, x[1])
                adjacent3 = g.GetCell(x[0], x[1] + 1)
                adjacent4 = g.GetCell(x[0], x[1] - 1)
                if adjacent1 != None and adjacent1.owner != g.uid: # and not ([x[0] + 1, x[1]] in self.before):
                    self.attackable.append([x[0] + 1, x[1]])
                if adjacent2 != None and adjacent2.owner != g.uid: # and not ([x[0] - 1, x[1]] in self.before):
                    self.attackable.append([x[0] - 1, x[1]])
                if adjacent3 != None and adjacent3.owner != g.uid: # and not ([x[0], x[1] + 1] in self.before):
                    self.attackable.append([x[0], x[1] + 1])
                if adjacent4 != None and adjacent4.owner != g.uid: # and not ([x[0], x[1] - 1] in self.before):
                    self.attackable.append([x[0], x[1] - 1])
            elif (c.isBase == True):
                self.ebase.append([x[0] + 1, x[1]])
                self.ebase.append([x[0] - 1, x[1]])
                self.ebase.append([x[0], x[1] + 1])
                self.ebase.append([x[0], x[1] - 1])
                self.base.append([x[0],x[1]])

    # calculate and return a list of attackable cells with value
    # append this for future function updates
    # gold = 10,0.8
    def calculate(self):
        #print (self.base)
        #print(self.ebase)
        #print(self.energy)


        # base defense method, if dont need then change 1000 to 0
        if 1:
            temp = self.basedefense()
            if temp[2]:
                self.attackable.append([temp[0],temp[1],1000])


    def basedefense(self):
        for i in self.mybase:
            adjacent1 = g.GetCell(i[0] + 1, i[1])
            adjacent2 = g.GetCell(i[0] - 1, i[1])
            adjacent3 = g.GetCell(i[0], i[1] + 1)
            adjacent4 = g.GetCell(i[0], i[1] - 1)
            if adjacent1 != None and adjacent1.owner != g.uid:
                print("base1")
                return ([i[0] + 1, i[1], True])
            if adjacent2 != None and adjacent2.owner != g.uid:
                print("base2")
                return ([i[0] - 1, i[1], True])
            if adjacent3 != None and adjacent3.owner != g.uid:
                print("base3")
                return ([i[0], i[1] + 1, True])
            if adjacent4 != None and adjacent4.owner != g.uid:
                print("base4")
                return ([i[0], i[1] - 1, True])
        return ([0,0,False])

    def valueoptimal(self):
        self.optimal = [[0, 0, 0]]
        self.optimal1 = [[0,0,0]]
        for i in self.attackable:
            if i[2] > self.optimal[0][2]:
                self.optimal1 = self.optimal
                self.optimal = [i]

    def attack(self):
        count = 0

        if self.before != [[]]:
            for i in self.before:
                if i != [] and i[0] == self.optimal[0][0] and i[1] == self.optimal[0][1]:
                    print(self.optimal),
                    print("buffer hit")
                    return

        c = g.GetCell(self.optimal[0][0], self.optimal[0][1])
        if ((c.takeTime >= 3 and self.optimal[0][2] > 10) or c.takeTime >= 5) and g.energy > 10:
            while not (g.AttackCell(self.optimal[0][0], self.optimal[0][1], True))[0] and count < 10:
                print("boost"),
                count = count + 1
        else:
            while not (g.AttackCell(self.optimal[0][0], self.optimal[0][1], False))[0] and count < 10:
                count = count + 1
        print (self.optimal),
        print (self.before)
        self.before.append([self.optimal[0][0],self.optimal[0][1]])
        del self.before[0]

    def blast(self):
        for i in self.base:
            x = i[0]
            y = i[1]
            b = g.GetCell(x, y)
            adjacent1 = g.GetCell(x + 1, y)
            adjacent2 = g.GetCell(x - 1, y)
            adjacent3 = g.GetCell(x, y + 1)
            adjacent4 = g.GetCell(x, y - 1)
            a1 = (adjacent1 != None and adjacent1.owner != b.owner)
            a2 = (adjacent2 != None and adjacent2.owner != b.owner)
            a3 = (adjacent3 != None and adjacent3.owner != b.owner)
            a4 = (adjacent4 != None and adjacent4.owner != b.owner)
            if a1 and a2:
                down1 = g.GetCell(x, y - 1)
                if down1 != None and down1.owner == g.uid:
                    g.Blast(x, y - 1, "vertical")
                    return
                down2 = g.GetCell(x, y - 2)
                if down2 != None and down2.owner == g.uid:
                    g.Blast(x, y - 2, "vertical")
                    return
                down3 = g.GetCell(x, y - 3)
                if down3 != None and down3.owner == g.uid:
                    g.Blast(x, y - 3, "vertical")
                    return
                up1 = g.GetCell(x, y + 1)
                if up1 != None and up1.owner == g.uid:
                    g.Blast(x, y + 1, "vertical")
                    return
                up2 = g.GetCell(x, y + 2)
                if up2 != None and up2.owner == g.uid:
                    g.Blast(x, y + 2, "vertical")
                    return
                up3 = g.GetCell(x, y + 3)
                if up3 != None and up3.owner == g.uid:
                    g.Blast(x, y + 3, "vertical")
                    return
            if a3 and a4:
                left1 = g.GetCell(x - 1, y)
                if left1 != None and left1.owner == g.uid:
                    g.Blast(x - 1, y, "horizontal")
                    return
                left2 = g.GetCell(x - 2, y)
                if left2 != None and left2.owner == g.uid:
                    g.Blast(x - 2, y, "horizontal")
                    return
                left3 = g.GetCell(x - 3, y)
                if left3 != None and left3.owner == g.uid:
                    g.Blast(x - 3, y, "horizontal")
                    return
                right1 = g.GetCell(x + 1, y)
                if right1 != None and right1.owner == g.uid:
                    g.Blast(x + 1, y, "horizontal")
                    return
                right2 = g.GetCell(x + 2, y)
                if right2 != None and right2.owner == g.uid:
                    g.Blast(x + 2, y, "horizontal")
                    return
                right3 = g.GetCell(x + 3, y)
                if right3 != None and right3.owner == g.uid:
                    g.Blast(x + 3, y, "horizontal")
                    return
            if a1 and a4:
                upleft = g.GetCell(x - 1, y + 1)
                if upleft!= None and upleft.owner == g.uid:
                    g.Blast(x - 1, y + 1, "square")
                    return
            if a2 and a4:
                upright = g.GetCell(x + 1, y + 1)
                if upright!= None and upright.owner == g.uid:
                    g.Blast(x + 1, y + 1, "square")
                    return
            if a2 and a3:
                downright = g.GetCell(x + 1, y - 1)
                if downright!= None and downright.owner == g.uid:
                    g.Blast(x + 1, y - 1, "square")
                    return
            if a1 and a3:
                downleft = g.GetCell(x - 1, y - 1)
                if downleft!= None and downleft.owner == g.uid:
                    g.Blast(x - 1, y - 1, "square")
                    return

g = colorfight.Game()
g.JoinGame('Anonymous')
m = Mainbody()
#g.BuildBase(0,25)
m.special()
for x in range(g.width):
    for y in range(g.height):
        m.cell.append([x,y])
while True:
    m.Gold()
    m.detect()
    m.calculate()
    if g.energy > 50:
        m.blast()
    m.valueoptimal()
    m.attack()
    g.Refresh()
    print("cycle done")

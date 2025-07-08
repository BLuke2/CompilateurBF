from tableau import tableau
class compilateur:
    def __init__(self,strtoeval="",rqst = None, dotcb = None, lscb = None, rscb = None):
        if rqst == None:
            self.request = self.getvalue
        else:
            self.request = rqst
        if dotcb == None:
            self.dotcb = [self.printtab]
        else:
            self.dotcb = dotcb
        self.lscb =lscb
        self.rscb =rscb
        
        self.validAns = True

        self.wasRun = False
        
        self.reset()
        self.addStr(strtoeval)

    def reset(self):
        self.validAns = True
        self.wasRun = False
        self.tab = tableau()
        self.i = 0
        self.l = 0
        self.program=""

    def addStr(self,s):
        self.l+=len(s)
        self.program += s

    def findOpBr(self,startIndex):
        i=startIndex
        cnt = -1
        while cnt != 0 or self.program[i] != "[":
            if self.program[i]=="]":
                cnt+=1
            elif self.program[i]=="[":
                cnt-=1
            i-=1
        return i

    def findClBr(self,startIndex):
        i=startIndex
        cnt= -1
        while cnt != 0 or self.program[i] != "]":
            if self.program[i]=="[":
                cnt+=1
            elif self.program[i]=="]":
                cnt-=1
            i+=1
        return i

    def printtab(self,t):
        print(t)

    def getvalue(self):
        a = ""
        while not a.isdigit():
            a = input(">>:")
        return int(a)

    def getAns(self,answer):
        self.validAns = True
        self.tab.set(answer)
        if self.wasRun:
            self.run()

    def runChar(self,i):
        c=self.program[i]
        if c == "<":
            self.tab.lshift()
            if self.lscb!=None:
                self.lscb()
        elif c == ">":
            self.tab.rshift()
            if self.rscb!=None:
                self.rscb()
        elif c == "+":
            self.tab.addone()
        elif c == "-":
            self.tab.subone()
        elif c == "[":
            if self.tab.get() == 0:
                return self.findClBr(i)
        elif c == "]":
            if self.tab.get() != 0:
                return self.findOpBr(i)
        elif c == ".":
            for j in self.dotcb:
                j(self.tab)
        elif c == ",":
            self.validAns = False
            self.request()
        return i+1

    def step(self):
        if self.i<self.l and self.validAns:
            self.i = self.runChar(self.i)

    def run(self):
        while self.i<self.l and self.validAns:
            self.i = self.runChar(self.i)
        self.wasRun = not self.validAns #program runs again only when interupted by a ',' and not when finished naturaly and then reintroduced to a ','...

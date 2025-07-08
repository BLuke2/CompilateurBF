class tableau:
    def __init__(self, size=1):
        self.tab =0
        self.i=0
        self.n=size
    def __len__(self):
        return self.n
    def __str__(self):
        a = "|"
        for i in range(self.n):
            a+=(" ","*")[i==self.i]+str(self[i])+" |"
        return a
    def __getitem__(self,i):
        return (self.tab&(255<<(8*(self.n-1-i))))>>(8*(self.n-1-i))
    def __setitem__(self,i,v):
        self.tab += ((v%256)-self[i])<<(8*(self.n-1-i))
    def addone(self):
        if self[self.i]<255:
            self.tab+=1<<(8*(self.n-1-self.i))
        else:
            self.tab-=255<<(8*(self.n-1-self.i))
    def subone(self):
        if self[self.i]>0:
            self.tab-=1<<(8*(self.n-1-self.i))
        else:
            self.tab+=255<<(8*(self.n-1-self.i))
    def lshift(self):
        if self.i>0:
            self.i-=1
        else:
            self.n+=1
    def rshift(self):
        if self.i>=self.n-1:
            self.n+=1
            self.tab<<=8
        self.i+=1
        
    def get(self):
        return self[self.i]
    def set(self,v):
        self[self.i]=v

import tkinter as tk
import os
from Comp import compilateur

windows = []
comp = compilateur()
baseDir = os.getcwd()


#Chargement de la table Ascii depuis le fichier
if not os.path.exists("Ascii.txt"):
    raise OSError("fichier Ascii.txt non trouvé")
else:
    tableAscii=[]
    with open('Ascii.txt','r',encoding="utf-8") as file:
        for i in range(256):
            if i < 8 or (i>15 and i<28 and i!=25):
                tableAscii.append(file.readline()[:3])
            elif i<32:
                tableAscii.append(file.readline()[:2])
            elif i == 32:
                tableAscii.append(" ")
                file.readline()
            elif i == 255:
                tableAscii.append(file.readline()[:4])
            else:
                tableAscii.append(file.readline()[0])


def openHelpWin():
    global windows
    hlpwin = tk.Tk()
    hlpwin.title("Aide")
    with open(baseDir+"\\help.txt",'r',encoding="utf-8") as file:
        for ligne in file:
            tk.Label(hlpwin,text=ligne).pack()
    windows.append(hlpwin)

def openAsciiWin():
    global windows
    ascwin = tk.Tk()
    ascwin.title("Table Ascii")
    for i in range(256):
       tk.Label(ascwin,text=str(i) +" " +tableAscii[i],bg=("#EEEEEE","#BBBBBB")[(i//16)%2]).grid(row=1+(i%16),column=1+2*(i//16),columnspan=2,sticky="nsew")
    windows.append(ascwin)

upAffTab = True 
affTabIndex=0
startTabIndex=0
currentTabIndex=0
minTabIndex=-10
maxTabIndex=10

def UpAffTabIndex(i):
    global affTabIndex,upAffTab
    affTabIndex = int(i)
    upAffTab=True

mainwin = tk.Tk()
mainwin.title("Compilateur de BF")

hbutt = tk.Button(mainwin,text="H",command=openHelpWin)
hbutt.grid(row=0,column=0,sticky="nsew")
ascbutt = tk.Button(mainwin,text="A",command=openAsciiWin)
ascbutt.grid(row=0,column=1,sticky="nsew")

tk.Label(mainwin,text="V",fg="#9A6969").grid(row=0,column=10)


#Tableau
afftab = [tk.Button(mainwin,text="0",state="disabled",bg="#DADADA",width=4) for i in range(21)]
for i in range(21):
    afftab[i].grid(row=1,column=i,sticky="nsew")

affTabScale = tk.Scale(mainwin,from_=minTabIndex,to=maxTabIndex,orient="horizontal",command=UpAffTabIndex)
affTabScale.grid(sticky="nsew",row=2,column=0,columnspan=21)




#Résultats
boiteAResultats = tk.Frame(mainwin,relief="sunken",highlightbackground="#AAAAAA",highlightthickness=2)
text=[tk.Label(boiteAResultats,bg="#DADADA",width=110) for i in range(4)]
for i in range(4):
    text[i].grid(sticky="nsew",row=i,column=0,columnspan=20)

upAffRes = True
affResIndex = 0
maxResIndex = 0

def UpAffResIndex(i):
    global affResIndex,upAffRes
    affResIndex = int(i)
    upAffRes=True

affResScale = tk.Scale(boiteAResultats,from_=0,to=maxResIndex,command=UpAffResIndex)
affResScale.grid(row=0,rowspan=4,column=20)

boiteAResultats.grid(row=3,rowspan=4,column=0,columnspan=21,sticky="nsew")

resultats = [""]
resIndex = 0



#code
boiteACode = tk.Frame(mainwin,relief="sunken",highlightbackground="#AAAAAA",highlightthickness=2)
upAffCode=True
affCodeIndex=0
maxCodeIndex=0

def UpAffCodeIndex(i):
    global upAffCode,affCodeIndex
    affCodeIndex = int(i)
    upAffCode=True

code=[""]


def getCodeStr():
    global code
    S=""
    for ligne in code:
        S+=ligne
    return S

addtext=True

def addToComp():
    global comp,upAffTab
    if addtext:
        comp.addStr(code[currenti])
    else:
        Reset()
        upAffTab=True

currenti=0

codeField = tk.Entry(boiteACode,text="aaaaaaaaa")
codeField.grid(row=17,column=0,columnspan=20,sticky="nsew")

def edit(i):
    global code, currenti, codeField,upAffCode,addtext
    code[currenti] = codeField.get()
    codeField.delete(0,"end")
    codeField.focus()
    if i>=len(code):
        addToComp()
        currenti=len(code)
        code.append("")
        addtext=True
    else:
        addToComp()
        currenti=i
        codeField.insert(0,code[i])
        code[i]=""
        addtext=False
    upAffCode=True

def codeButtonFunc(i):
    def func():
        global affCodeIndex
        edit(i+affCodeIndex)
    return func

affCode=[tk.Button(boiteACode,width=106,relief="flat",command=codeButtonFunc(i)) for i in range(10)]
codeLineNums = [tk.Label(boiteACode,text=str(i),width=4) for i in range(10)]
affCodeScale = tk.Scale(boiteACode,from_=0,to=maxCodeIndex,command=UpAffCodeIndex)

for i in range(10):
    affCode[i].grid(row=i,column=1,columnspan=19,sticky="nsew")
    codeLineNums[i].grid(row=i,column=0,sticky="nsew")
affCodeScale.grid(row=0,column=20,rowspan=10,sticky="nsew")

def newLine(*arg):
    global currenti
    edit(currenti+1)

def dLline(*arg):
    global currenti,codeField
    if currenti>=1 and codeField.get()=="":
        code.pop(currenti)
        currenti-=1
        codeField.insert(0,code[currenti]+" ")
        edit(currenti)

newLineButt=tk.Button(boiteACode,width=4,text="\\n",command=newLine)
newLineButt.grid(row=17,column=20,sticky="nsew")
codeField.bind("<Return>",newLine)
codeField.bind("<BackSpace>",dLline)
boiteACode.grid(row=7,rowspan=10,column=0,columnspan=21,sticky="nsew")



#Controle du compilateur
def Step():
    global upAffTab
    upAffTab=True
    comp.step()

def Run():
    global upAffTab
    upAffTab=True
    comp.run()

def Reset():
    global upAffTab,upAffRes,resultats,resIndex,startTabIndex,currentTabIndex,minTabIndex,maxTabIndex,affTabScale
    upAffTab=True
    upAffRes=True
    minTabIndex=-10
    maxTabIndex=10
    affTabScale.config(to=maxTabIndex,from_=minTabIndex)
    affTabScale.set(0)
    resIndex=0
    resultats=[""]
    startTabIndex=0
    currentTabIndex=0
    comp.reset()
    comp.addStr(getCodeStr())


stepButton = tk.Button(mainwin,text=">",command=Step)
stepButton.grid(row=0,column=19,sticky="nsew")

runButton = tk.Button(mainwin,text=">>",command=Run)
runButton.grid(row=0,column=20,sticky="nsew")

resetButton = tk.Button(mainwin, text="R",command=Reset)
resetButton.grid(row=0,column=18,sticky="nsew")



#input
userApproval = False
validInput = True
upInp = True

def validate(*arg):
    global userApproval,upInp
    userApproval = not userApproval
    upInp = True

inputField = tk.Entry(mainwin)
inputField.grid(row=18,column=0,columnspan=20,sticky="nsew")
inputField.bind("<Return>",validate)

inputButt = tk.Button(mainwin,text="V",command=validate)
inputButt.grid(row=18,column=20,sticky="nsew")


isAnsRqst = False


#Sauvegarde / charge
def Save(fileName=""):
    global code
    if fileName=="":
        if os.path.exists("Unnamed.txt"):
            i=1
            while os.path.exists(f"Unnamed{i}.txt"):
                i+=1
            fileName=f"Unnamed{i}.txt"
        else:
            fileName="Unnamed.txt"
    with open(fileName,'w',encoding='utf-8') as file:
        for i in code:
            file.write(i+"\n")
    openSaveAck(fileName)

def Load(fileName):
    global code, upAffCode,currenti
    if os.path.exists(fileName):
        code = []
        with open(fileName,'r',encoding='utf-8') as file:
            for i in file:
                code.append(i[:-1])
        upAffCode=True
        Reset()
        currenti=len(code)-1
    else:
        raise ValueError("No File "+fileName+" found")

def openSaveAck(fileName):
    global windows
    win = tk.Tk()
    win.geometry("400x100")
    tk.Label(win,text="Sauvegarde de "+fileName+" effectuée !").pack(fill="x",expand=True)
    tk.Button(win,text="Ok",command=lambda: win.destroy()).pack(expand=True)
    windows.append(win)

def yesSaveButtonCommand(fileName,root):
    def a():
        Save(fileName)
        root.destroy()
    return a

def openSaveConfPrompt(fileName):
    global windows
    prompt = tk.Tk()
    prompt.geometry("400x100")
    tk.Label(prompt,text='Êtes vous sûr de vouloir sauvegarder\nsous le nom : '+fileName+' ?').pack(fill="x",expand=True)
    boite=tk.Frame(prompt)
    tk.Button(boite,text='Oui',command=yesSaveButtonCommand(fileName,prompt)).pack(side="left",padx=50)
    tk.Button(boite,text='Non',command=lambda: prompt.destroy()).pack(side="right",padx=50)
    boite.pack(expand=True)
    windows.append(prompt)
    
def yesLoadButtonCommand(fileName,root):
    def a():
        Load(fileName)
        root.destroy()
    return a

def openLoadConfPrompt(fileName):
    global windows
    prompt = tk.Tk()
    prompt.geometry("400x100")
    tk.Label(prompt,text='Êtes vous sûr de vouloir charger le fichier : '+fileName+' ?').pack(fill="x",expand=True)
    boite=tk.Frame(prompt)
    tk.Button(boite,text='Oui',command=yesLoadButtonCommand(fileName,prompt)).pack(side="left",padx=50)
    tk.Button(boite,text='Non',command=lambda: prompt.destroy()).pack(side="right",padx=50)
    boite.pack(expand=True)
    windows.append(prompt)

currentPath = os.getcwd()+"\\Saves\\"
pathLabel = tk.Label(mainwin,text=currentPath)
os.chdir(currentPath)

def modifyPath(newPath,root):
    global currentPath,pathLabel
    currentPath = newPath+"\\"
    os.chdir(currentPath)
    pathLabel.config(text=currentPath)
    root.destroy()

def openPathModWin():
    global windows,currentPath
    win = tk.Tk()
    win.geometry("400x150")
    tk.Label(win,text="Vous allez changer le dossier de travail :").pack(fill="x",expand=True)
    boite = tk.Frame(win)
    field = tk.Entry(boite,width=250)
    a = lambda: modifyPath(field.get(),win)
    field.insert(0,currentPath)
    field.bind("<Return>",a)
    field.pack(side="top",fill="x",padx=5,expand=True)
    tk.Button(boite,text="Ok",command=a).pack(side="bottom",padx=5,expand=True)
    boite.pack(expand=True)
    windows.append(win)
    
    
changePathButton = tk.Button(mainwin,text="P",command=openPathModWin)

changePathButton.grid(row=19,column=0,sticky="nsew")
pathLabel.grid(row=19,column=1,columnspan=10,sticky="nsew")

fileNameField = tk.Entry(mainwin)
fileNameField.grid(row=19,column=12,columnspan=5,sticky="nsew")
tk.Label(mainwin,text=".txt").grid(row=19,column=17,columnspan=2,sticky="nsew")

def SaveButtonFunc():
    global fileNameField,currentPath
    openSaveConfPrompt(currentPath+fileNameField.get()+".txt")

def LoadButtonFunc():
    global fileNameField,currentPath
    openLoadConfPrompt(currentPath+fileNameField.get()+".txt")

saveButt = tk.Button(mainwin,text="S",command=SaveButtonFunc)
loadButt = tk.Button(mainwin,text="L",command=LoadButtonFunc)

saveButt.grid(row=19,column=19,sticky="nsew")
loadButt.grid(row=19,column=20,sticky="nsew")

def dirFunc(root,dirName):
    def a():
        modifyPath(dirName,root)
        openLoadWin()
    return a

def fileFunc(root,fileName):
    global fileNameField
    def a():
        openLoadConfPrompt(fileName)
        fileNameField.delete(0,"end")
        fileNameField.insert(0,fileName[:-4])
        root.destroy()
    return a

def openLoadWin():
    global windows,currentPath
    loadWin = tk.Tk()
    loadWin.geometry("400x300")
    filelist = os.listdir()
    tk.Button(loadWin,width=56,text="<-",command=dirFunc(loadWin,os.path.dirname(currentPath[:-2]))).grid(row=0,column=0,columnspan=10,sticky="nsew")
    for i in range(len(filelist)):
        if os.path.isfile(filelist[i]):
            tk.Button(loadWin,text=filelist[i],command=fileFunc(loadWin,filelist[i])).grid(row=i+1,column=0,columnspan=10,sticky="nsew")
        else:
            tk.Button(loadWin,text=filelist[i],command=dirFunc(loadWin,currentPath+filelist[i])).grid(row=i+1,column=0,columnspan=10,sticky="nsew")
    windows.append(loadWin)

dirLoadButt = tk.Button(mainwin,text="D",command=openLoadWin)
dirLoadButt.grid(row=19,column=11,sticky="nsew")

######### updates #########
def updateAffTab():
    global startTabIndex, affTabIndex,afftab,comp
    n = comp.tab.n
    for delta in range(-10,11):
        i = delta+affTabIndex-startTabIndex
        if i<0 or i>=n:
            s="0"
        else:
            s=str(comp.tab[i])
        afftab[10+delta].config(bg = "#DADADA",text=s)
        if i == comp.tab.i:
            afftab[10+delta].config(bg = "#FFDADA")

def updateAffRes():
    global affResIndex,text,resultats
    i=affResIndex
    while i<len(resultats) and i<affResIndex+4:
        text[i-affResIndex].config(text=resultats[i])
        i+=1
    while i<affResIndex+4:
        text[i-affResIndex].config(text="")
        i+=1


def updateAffCode():
    global affCodeIndex,affCode,codeLineNums,code,currenti
    i = affCodeIndex
    while i<len(code) and i<affCodeIndex+10:
        affCode[i-affCodeIndex].config(text=code[i],bg="#DADADA")
        codeLineNums[i-affCodeIndex].config(text=str(i))
        if i == currenti:
            affCode[i-affCodeIndex].config(bg="#FFDADA")
        i+=1
    while i<affCodeIndex+10:
        affCode[i-affCodeIndex].config(text="",bg="#DADADA")
        codeLineNums[i-affCodeIndex].config(text="")
        i+=1

def updateInput():
    global inputField,inputButt,userApproval,isAnsRqst,validInput
    
    if not validInput:
        inputField.config(bg="#BB5555")
    elif isAnsRqst:
        inputField.config(bg="#BBAA55")
    else:
        inputField.config(bg="#FFF")
    
    if userApproval:
        inputButt.config(bg="#90DF90")
    else:
        inputButt.config(bg="#DFDF90")



#Callbacks
def lscb():
    global currentTabIndex, startTabIndex,upAffTab
    currentTabIndex-=1
    if currentTabIndex<startTabIndex:
        startTabIndex = currentTabIndex
    upAffTab=True

def rscb():
    global currentTabIndex,upAffTab
    currentTabIndex+=1
    upAffTab=True

def dotcb(tab):
    global resultats,resIndex,upAffRes
    v= tab.get()
    if v == 10:
        resIndex+=1
        resultats.append("")
    else:
        resultats[resIndex]+=tableAscii[v]
    upAffRes=True

def request():
    global upInp,isAnsRqst,inputField
    upInp = True
    isAnsRqst = True
    inputField.focus()

comp.lscb =lscb
comp.rscb =rscb
comp.dotcb = [dotcb]
comp.request = request



windows.append(mainwin)

#boucle principale
while windows!=[]:

    if isAnsRqst and userApproval:
        v = inputField.get()
        validInput = v.isdigit()
        if validInput:
            isAnsRqst=False
            inputField.delete(0,"end")
            upAffTab=True
            comp.getAns(int(v))

        userApproval=False
        upInp=True

    if upAffTab:
        updateAffTab()
        if currentTabIndex>maxTabIndex+10:
            maxTabIndex=currentTabIndex-10
            affTabScale.config(to=maxTabIndex)
        elif currentTabIndex<minTabIndex-10:
            minTabIndex=currentTabIndex+10
            affTabScale.config(from_=minTabIndex)
        upAffTab=False

    if upAffRes:
        updateAffRes()
        if len(resultats)>maxResIndex+4:
            maxResIndex = len(resultats)-4
            affResScale.config(to=maxResIndex)
        upAffRes=False

    if upAffCode:
        updateAffCode()
        if len(code)>maxCodeIndex+9:
            maxCodeIndex = len(code)-9
            affCodeScale.config(to=maxCodeIndex)
        upAffCode=False
    
    if upInp:
        updateInput()
        upInp=False

    i=0
    while i < len(windows):
        try:
            windows[i].update()
            i+=1
        except:
            windows.pop(i)


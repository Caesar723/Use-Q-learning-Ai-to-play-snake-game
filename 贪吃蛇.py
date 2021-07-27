import pygame
import random
import time
import numpy as np
import pandas as pd
class Qtable:
    def __init__(self,listaction,a=0.1,y=0.9,precentmove=1):
        self.action=listaction
        self.arf=a
        self.gama=y
        self.precent=precentmove
        #self.q = pd.DataFrame(np.array([[0] * (25 * 25 * 4)]).reshape(625, 4), columns=listaction)
        #self.qT=[]
        #for add in range(0,400):
            #self.qT.append(pd.DataFrame(pd.DataFrame(np.array([[0] * (25 * 25 * 4)]).reshape(625, 4), columns=listaction)))
        #print(self.qT[0])
        self.readcsv()
    def chooseAction(self,s,Fx,Fy,index=None):
        #print()
        if np.random.uniform()<self.precent:
            actionA=ActionOp(a2Action(s[0][2]))
            #print(int(((Fy-25)/25)*20+(Fx/25)),Fx,Fy)
            state=pd.DataFrame(self.qT[int((Fy-25)/25*20+(Fx/25))]).iloc[(int((s[0][1])+(s[0][0]/25)))].copy()
            #print(state)
            punish=punishMatrix(s)
            punish+=chackround(punish)
            try:
                state[0]+=punish[int(s[0][1]/25)][int(s[0][0]/25)-1]
            except:
                state[0] +=0
            try:
                state[1]+=punish[int(s[0][1]/25)][int(s[0][0]/25)+1]
            except:
                state[1] +=0
            try:
                state[2]+=punish[int(s[0][1]/25)-1][int(s[0][0]/25)]
            except:
                state[2] +=0
            try:
                state[3]+=punish[int(s[0][1]/25)+1][int(s[0][0]/25)]
            except:
                state[3] +=0
            if index!=None:
                state[index] += -9999
            #print(state)
            state=state.reindex(np.random.permutation(state.index))
            #state[2]+=9
            act=state.argmax()
            #print(act)
            actionB=pd.DataFrame(state).index[act]
            if actionA==actionB:
                print(actionA)
                return self.chooseAction(s,Fx,Fy,Action2index(actionB))
            else:
                #print("no")
                return actionB
        else:
            return self.action[random.randint(0,len(self.action)-1)]
    def learn(self,s,r,action,s_,Fx,Fy):
        QPre=self.qT[int((Fy-25)/25*20+(Fx/25))].copy()
        if s_!="over":
            #print(QPre.iloc[(int((s_[1])+(s_[0]/25)))].max())
            #print([(int((s_[1])+(s_[0]/25)))],s_)
            QTarget = r + QPre.iloc[(int((s_[1])+(s_[0]/25)))].max()*self.gama
        else:
            QTarget = r

        self.qT[int((Fy-25)/25*20+(Fx/25))][action].iloc[(int((s[1])+(s[0]/25)))]+=round(self.arf*(QTarget-QPre[action].iloc[(int((s[1])+(s[0]/25)))]),3)
        #print(np.array(self.qT[int((Fy-25)/25*20+(Fx/25))]))
    def tocsv(self):
        for to in range(len(self.qT)):
            self.qT[to].to_csv("dataSnack/"+str(to)+".csv",index=False)
        #print(self.qT)
    def readcsv(self):
        self.qT=[]
        for read in range(400):
            self.qT.append(pd.read_csv("dataSnack/"+str(read)+".csv"))
class snack:
    location=[]

    timeLow=time.time()

    head=pygame.image.load("1.png")
    body=pygame.image.load("1.png")
    tail=pygame.image.load("1.png")
    point=0
    direction=9
    S=0
    clock=time.time()

    def __init__(self,arr,fx,fy):
        self.location=arr

        self.FruitX = fx
        self.FruitY = fy
    def upload(self,screen):
        if self.S==0 or self.S==1000:
            for move in range(0,len(self.location)):
                if move==0:
                    self.head=pygame.image.load(str(self.location[move][2])+".png")
                    bodysize = pygame.transform.scale(self.head, (25, 25))
                    #pygame.draw.circle(screen,(255, 0, 0),[self.location[move][0],self.location[move][1]],10)
                elif move==len(self.location)-1:
                    self.tail = pygame.image.load(str(self.location[move-1][2])+str(self.location[move-1][2])+str(self.location[move-1][2]) + ".png")
                    bodysize = pygame.transform.scale(self.tail, (25, 25))
                    #pygame.draw.circle(screen, (100, 0, 0), [self.location[move][0], self.location[move][1]], 10)
                else:
                    self.body = pygame.image.load(str(self.location[move-1][2]) + str(self.location[move][2])+ ".png")
                    bodysize = pygame.transform.scale(self.body, (25, 25))
                    #pygame.draw.circle(screen, (0, 0, 0), [self.location[move][0], self.location[move][1]], 10)
                bodyxy = bodysize.get_rect(center=(self.location[move][0], self.location[move][1]))
                screen.blit(bodysize, bodyxy)
            if self.location[0][0]==self.FruitX and self.location[0][1]==self.FruitY:
                self.point+=1
                self.S=1000
                self.FruitX,self.FruitY=self.findlocation(self.location)
                self.location.append([self.location[len(self.location)-1][0]-20,self.location[len(self.location)-1][1],self.direction])
            for check in  range(len(self.location)-1):
                if self.location[0][0]==self.location[len(self.location)-1-check][0] and self.location[0][1]==self.location[len(self.location)-1-check][1]:
                    self.S=-1

        #fru = pygame.image.load("bb3.png")
        #frusize = pygame.transform.scale(fru, (25, 25))
        #fruxy = frusize.get_rect(center=(self.FruitX, self.FruitY))
        #screen.blit(frusize, fruxy)
            pygame.draw.circle(screen, (0, 255, 0), [self.FruitX, self.FruitY], 10)
            showMessage(str(self.point), 30, (255, 0, 0), [400, 25])
    def findlocation(self,location):
        FruX, FruY = random.randint(1, 18) * 25, random.randint(1, 19) * 25
        for check in range(len(location)):
            if FruX==location[check][0] and FruY==location[check][1]:
                return self.findlocation(location)
        return FruX,FruY
    def move(self):
        if self.S==0 or self.S==1000:
            for m in range(0, len(self.location)-1):
                self.location[len(self.location)-m-1]=list(self.location[len(self.location)-m-2])
            if self.direction==9 :
                self.location[0][0] += 25
            elif self.direction==1:
                self.location[0][1] += -25
            elif self.direction==4:
                self.location[0][1] += 25
            elif self.direction==6:
                self.location[0][0] += -25
            self.location[0][2] = self.direction
            if self.location[0][0]>=500:self.S=-1
            if self.location[0][1] >= 500: self.S = -1
            if self.location[0][0]<=0:self.S=-1
            if self.location[0][1] <=0: self.S =-1
            #print(self.location)
    def left(self):
        if self.direction!=9:
            self.direction=6
    def right(self):
        if self.direction!=6:
            self.direction=9
    def up(self):
        if self.direction!=4:
            self.direction=1
    def down(self):
        if self.direction!=1:
            self.direction=4
def a2Action(a):
    return "up" if a==1 else "down" if a==4 else "left" if a==6 else "right"
def Action2index(act):
    return 2 if act=="up" else 3 if act=="down" else 0 if act=="left" else 1
def ActionOp(act):
    if act=="up":
        return "down"
    elif act=="down":
        return "up"
    elif act=="left":
        return "right"
    else:
        return "left"
def punishMatrix(location):
    arr=np.array([0]*441).reshape(21,21)
    #print(location)
    for reduce in list(location):
        arr[int(reduce[1]/25)][int(reduce[0]/25)]=-20000
    for column in range(21):
        for row in range(21):
            if column==0 or row==20 or column==20 or row==0:
                arr[column][row]=-20000
    #print(arr)
    return arr
def showMessage(text,size,colour,p):
    fon=pygame.font.Font(None,size)
    sur=fon.render(text,True,colour)
    screen.blit(sur,p)
def S_(location,direction,prize):
    #print(location)
    loca=list(location)
    if prize==0:
        if direction == 9:
            loca[0] += 25
        elif direction == 1:
            loca[1] += -25
        elif direction == 4:
            loca[1] += 25
        else:
            loca[0] += -25
        return loca
    else:
        return "over"
a=Qtable(["left","right","up","down"])
#for r in range(10):
    #for locationx in range(18,20):
        #for locationy in range(1,20):
def chackround(a):
    arr=a.copy()
    run=True
    loc=[]
    for i in range(20):
        y=1
        x=i
        if arr[y][x]==0:
            loc=[[x,y]]
            break
    arr=water(arr,loc)
    while run:
        copyloc=loc
        #print(len(loc))
        loc = []
        counter=0
        #print()
        #print(len(copyloc))
        for num in range(len(copyloc)):

            if arr[copyloc[num][1]][copyloc[num][0]+1]==0:
                loc.append([copyloc[num][0]+1,copyloc[num][1]])
                counter+=1
            if arr[copyloc[num][1]][copyloc[num][0]-1]==0:
                loc.append([copyloc[num][0]-1,copyloc[num][1]])
                counter += 1
            if arr[copyloc[num][1]+1][copyloc[num][0]]==0:
                loc.append([copyloc[num][0],copyloc[num][1]+1])
                counter += 1
            if arr[copyloc[num][1]-1][copyloc[num][0]]==0:
                loc.append([copyloc[num][0],copyloc[num][1]-1])
                counter += 1
            arr=water(arr,loc)
        #print(arr)
        if counter==0:
            run=False
    arr[arr==-20000]=1
    arr[arr==0]=-19999
    arr-=1
    return arr


def water(arr,locate):
    co=arr
    for ii in range(len(locate)):
        co[locate[ii][1]][locate[ii][0]]=-20000
    return co
for turn in range(1):
    clock = time.time()
    pygame.init()
    screen=pygame.display.set_mode([475,475])
    #clock=pygame.time.Clock()
    arrsn=[]
    for sn in range(1):
        arrsn.append(snack([[random.randint(1,19)*25,random.randint(1,19)*25,9],[25,0,9],[25,0,9]],random.randint(1,18)*25,random.randint(1,19)*25))

    running=True
    count=0

    #print(S_(list(sn1.location[0]),sn1.direction,sn1.S))
    #print(a.chooseAction(sn1.location[0],sn1.FruitX,sn1.FruitY))
    #a.learn(sn1.location[0],sn1.S,a2Action(sn1.direction),S_(list(sn1.location[0]),sn1.direction,sn1.S),sn1.FruitX,sn1.FruitY)
    while running:
        if time.time()-clock>0.05:

            clock=time.time()
            screen.fill((255, 255, 255))
            for snk in range(1):
                #print(arrsn[snk].S)
                if arrsn[snk].S!=-1:# and arrsn[snk].S!=1000:
                    arrsn[snk].upload(screen)
                    action = a.chooseAction(arrsn[snk].location, arrsn[snk].FruitX, arrsn[snk].FruitY)
                    #print(action)
                    locat=list(arrsn[snk].location[0])
                    #print(locat)
                    if action == "up": arrsn[snk].up()
                    if action == "down": arrsn[snk].down()
                    if action == "left": arrsn[snk].left()
                    if action == "right": arrsn[snk].right()
                    arrsn[snk].move()
                    punishMatrix(arrsn[snk].location)
                    #a.learn(locat, arrsn[snk].S, a2Action(arrsn[snk].direction), arrsn[snk].location[0],
                            #locationx*25, locationy*25)
                #print("kk")
            for i in pygame.event.get():
                pass
            #print(sn1.S)
            c=0
            win=0
            '''
            for check in range(200):
                if arrsn[check].S==-1 or arrsn[check].S==1000:
                    c+=1
                    if arrsn[check].S==1000:
                        win+=1
                if c>=200:
                    running=False
                    a.tocsv()
                    print(win,turn)
                '''
                #a.learn(sn1.location[0], sn1.S, a2Action(sn1.direction),
                        #S_(list(sn1.location[0]), sn1.direction, sn1.S),
                        #sn1.FruitX, sn1.FruitY)
        #sn2.upload(screen)
        #print("oj\k")

        pygame.display.flip()
    pygame.quit()

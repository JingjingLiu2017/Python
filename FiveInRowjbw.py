import sys
from EaselLib import *

green=(0,200,0)
#green goes first
red=(200,0,0)

def init():
    global redMoves
    global greenMoves
    global p
    global I
    redMoves=set()
    greenMoves=set()
    p='green' #Whoes turn
    I=(0,0)
    
#grid:Sprite
#
#draw the board
def grid():
    L=[]
    #invariant:L is the list of every segment drawn in the Go board	
    for i in range(0,19):
        Li=seg((-270+i*30,270),(-270+i*30,-270),(0,0,0))
        LLi=seg((-270,270-i*30),(270,270-i*30),(0,0,0))
        L=L+[Li,LLi]
    return L

def windowDimensions():
    return(1280,800)

# click: Bool
#
# click() means the left mouse button has gone from up to down.
def Click():
    return mouseDown and not oldMouseDown

#Empty:Intersection->Bool
#
#Empty iff I is empty,that means there is no green stone or red stone on this intersection
def Empty(I):
    return I not in redMoves and I not in greenMoves

#stoneImage:player x Intersection -> Sprite
#
#draw the stone for player p on intersection I
def stoneImage(p,I):
    if p=='red':return disc((int(-270+(I[0]-1)*30),int(270-(I[1]-1)*30)),14,red)
    if p=='green':return disc((int(-270+(I[0]-1)*30),int(270-(I[1]-1)*30)),14,green)

#roughlyEqu:float->int
#
#约等于
def roughlyEqu(a):
    if (a-a//1)<0.5: return a//1
    if (a-a//1)>=0.5: return a//1+1
    
def d1(I):
    return (I[0]-1,I[1])
def d2(I):
    return (I[0]+1,I[1]-1)
def d3(I):
    return(I[0]+1,I[1])
def d4(I):
    return (I[0]+1,I[1]+1)
def d5(I):
    return (I[0],[1]+1)
def d6(I):
    return (I[0]-1,I[1]+1)
def d7(I):
    return (I[0]-1,I[1])
def d8(I):
    return (I[0]-1,I[1]-1)

def psset(p):
    if p=='red':return redMoves
    if p=='green':return greenMoves
#win:
#
#
def win(p,I):
    L=[0,0,0,0,0,0,0,0]
    D={1:d1,2:d2,3:d3,4:d4,5:d5,6:d6,7:d7,8:d8}
    for i in range(0,9):
        while(I in psset(p)):
            L[0]=L[0]+1
            I=D.get(i+1)(I)
    for i in (0,5):
        if L[i]+L[i+4]-1>=5:return True
        else:return False

def printtxt():
    if win(p,I):
        return [txt(p,(-100,0),90,(100,100,100))+txt(wins,(0,0),90,(100,100,100))]
    return [disc((25,25),1,(0,0,0))]

#PlaceStone:Sprite
#
#call stoneImage(p,I) 
def PlaceStone():
    global redMoves
    global greenMoves
    global I
    global p
    if Click():I=(roughlyEqu((mouseX+270)/30)+1,roughlyEqu((270-mouseY)/30)+1)
    if  Empty(I)and Click():#差没结束   
        if (len(redMoves)+len(greenMoves))%2==1:
            redMoves=redMoves|{I}
            p='red'
        else: #if (len(redMoves)+len(greenMoves))%2==0:
            greenMoves=greenMoves|{I}
            p='green'
        return [stoneImage(p,I)]
    return [disc((25,25),1,(0,0,0))]

def stone():
    L=[]
    #invariant:L is the list of all the stones on the board
    for i in range(0,19):
        for j in range(0,19):
            if (1+j,1+i) in redMoves:L=L+[disc((-270+j*30,270-i*30),14,red)]
            if (1+j,1+i) in greenMoves: L=L+[disc((-270+j*30,270-i*30),14,green)] 
    return L

def display():
    return grid()+PlaceStone()+stone()+printtxt()

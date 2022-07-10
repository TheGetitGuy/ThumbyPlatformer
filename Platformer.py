import time
import thumby
import math 

thumby.display.setFPS(60)# BITMAP: width: 8, height: 8
maps = {
    'map1': [["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","2l","2","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","1","2","0","0","0","0","0","0"],["0","0","0","0","0","0","p","0","0","0","0","0","0","0","1","1","2","2","2","0","0","0"],["0","0","2","2","2","2","2","2","2","2","2","0","0","0","0","0","1","1","1","2","2","0"],["0","0","1","1","1","1","1","1","1","1","1","0","0","0","0","0","0","0","0","1","1","2"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","1"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","2","1"],["0","0","2","2","2","0","2","2","2","0","0","0","p","0","0","0","0","2l","2","2","1","1"],["0","0","1","1","1","2","1","1","1","0","0","1","1","1","0","0","0","1","1","1","1","1"],["0","0","1","1","1","1","1","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"],["0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"]]}
curmap = 'map1'
bitmap0 = bytearray([32,16,252,126,126,252,16,32])

arrowbitmap = bytearray([0,16,32,126,126,32,16,0])
tile1 = bytearray([255,255,255,255,255,255,255,255])
tilegrassmid = bytearray([253,253,243,251,251,243,249,253])
# BITMAP: width: 8, height: 8
tilegrassr = bytearray([249,251,247,187,93,51,58,0])
# BITMAP: width: 8, height: 8
tilegrassl = bytearray([0,61,115,123,217,51,251,249])

t0 = time.time()

currentplayer = 0
playerarray = []
arrowarray = []

class Camera:
    def __init__(self,x,y):
        self.x = x
        self.y = y
viewport = Camera(30,0)

def Lerp(x,y,per):
    return (x + per*(y - x))

    
class Entity:
    def __init__(self,x,y,xv,yv,sprite):
        self.xv = xv
        self.yv = yv
        self.sprite = thumby.Sprite(8,8,sprite,0,0,0)
        self.sprite.x = x
        self.sprite.y = y
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

class Solid(Entity):
    def __init__(self,x,y,xv,yv,sprite):
        super().__init__(x,y,xv,yv,sprite)
        self.iscollidable = True
        
class Arrow(Entity):
    def __init__(self,x,y,xv,yv,sprite):
        super().__init__(x,y,xv,yv,sprite)
        arrowarray.append(self)
        self.iscollidable = False
    def updateplace(self):
        self.x = Lerp(self.x,playerarray[currentplayer].x,0.7)
        self.y = playerarray[currentplayer].y-10

class Player(Entity):
    def __init__(self,x,y,xv,yv,sprite):
        super().__init__(x,y,xv,yv,sprite)
        playerarray.append(self)
        self.iscollidable = True
def Distance(a,b): #its distance formula bitch
    c = (a.x-b.x)**2 + (a.y-b.y)**2 
    return math.sqrt(c)
        
def Colliding(ent1,ent2):
    data = {'x': ent1.xv,'y': ent1.yv}
    if (ent1.iscollidable == False) or (ent2.iscollidable == False):
        return data
    x1 = ent1.sprite.x
    x2 = ent1.width + x1 
    x3 = ent2.sprite.x 
    x4 = ent2.width + x3 
    y1 = ent1.sprite.y
    y2 = ent1.height + y1 
    y3 = ent2.sprite.y
    y4 = ent2.height + y3


    
    if (x1 + data['x'] < x4 and x2 + data['x'] > x3 and y1 < y4 and y2 > y3):
        data['x'] = data['x']*0.5
        if (x1 + data['x'] < x4 and x2 + data['x'] > x3 and y1  < y4 and y2 > y3):
            data['x'] = 0
        
    if (x1 < x4 and x2 > x3 and y1 + data['y'] < y4 and y2 + data['y'] > y3):
        data['y'] = data['y']*0.5
        if (x1  < x4 and x2 > x3 and y1 + data['y'] < y4 and y2 + data['y'] > y3):
            data['y'] = 0
        

    return data
    
def PrintTiles(curmap):
    cx = 0
    cy = 0
    for row in curmap:
        cy+=1
        for column in row:
            cx+=1
            if column == '1':
               ## print('{}    {}  '.format((cx - (len(row)-1)*8),(cy*8)))
                entities.append(Solid((cx - (len(row))*(cy-1))*8,(cy*8),0,0,tile1))
            if column == '2':
                entities.append(Solid((cx - (len(row))*(cy-1))*8,(cy*8),0,0,tilegrassmid))
            if column == '2l':
                entities.append(Solid((cx - (len(row))*(cy-1))*8,(cy*8),0,0,tilegrassl))
            if column == '2r':
                entities.append(Solid((cx - (len(row))*(cy-1))*8,(cy*8),0,0,tilegrassr))
            
            if column == 'p':
                entities.append(Player((cx - (len(row))*(cy-1))*8,(cy*8),0,0,bitmap0))
                
entities = []            
PrintTiles(maps[curmap])   ##set the map
entities.extend([Arrow(0,0,0,0,arrowbitmap)]) ##spawn the arrow object

while(True):
    thumby.display.fill(0)

    t0 = time.ticks_ms() 
    if (thumby.buttonA.justPressed() == True):
        currentplayer += 1
        if currentplayer >= len(playerarray):
            currentplayer = 0
    if (thumby.buttonL.pressed() == True) and (playerarray[currentplayer].xv >= -3 ):
        playerarray[currentplayer].xv -= 2
        
    if (thumby.buttonR.pressed() == True) and (playerarray[currentplayer].xv <= 3):
        playerarray[currentplayer].xv += 2
    
    
    if (thumby.buttonU.pressed() == True):
        playerarray[currentplayer].yv -= 3
        
    
       ## curr_ent.x += curr_ent.xv
    for curr_ent in arrowarray:
        curr_ent.updateplace()
        curr_ent.yv = math.sin(t0/300)*2
                
    for curr_ent in playerarray:
        if curr_ent.yv < 10:
            curr_ent.yv += 2        
        if (curr_ent.xv >= 1 ):
            curr_ent.xv -= 1
        elif (curr_ent.xv <= -1):    
            curr_ent.xv += 1
    

    for curr_ent in entities:
        if curr_ent.xv != 0 or curr_ent.yv != 0:
            for other_ent in entities:
                if curr_ent != other_ent:
                    if Distance(other_ent, curr_ent) < 17:
                        rdata = Colliding(curr_ent, other_ent)
                        curr_ent.xv = rdata['x'] 
                        curr_ent.yv = rdata['y']
                        
                        
                        
        curr_ent.x += curr_ent.xv
        #print(curr_ent.xv)
        curr_ent.y += curr_ent.yv
                
       # print(viewport.x)
        curr_ent.sprite.y = (curr_ent.y)-viewport.y
        curr_ent.sprite.x = (curr_ent.x)-viewport.x
        thumby.display.drawSprite(curr_ent.sprite)
        
    viewport.x = Lerp(viewport.x,((playerarray[currentplayer].x+4)+(playerarray[currentplayer].xv*18))-(thumby.display.width/2),0.1)
    viewport.y = Lerp(viewport.y,((playerarray[currentplayer].y+4)+(playerarray[currentplayer].yv*8))-(thumby.display.height/2),0.1)
    thumby.display.update()

    
import pygame
import sys
pygame.init()

global init_time
init_time = pygame.time.get_ticks()
print(init_time)

window = pygame.display.set_mode((600,400))
pygame.display.set_caption("Stopwatch - Aleena")
font = pygame.font.SysFont('Arial',20)
font2 = pygame.font.SysFont('Arial',60)

objects = []

global ticks
ticks = 0
global past
past = 0

class Button():
    def __init__ (self, x, y, width, height, buttonText, onclickFunction, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False

        self.fillColors = {
            'normal' : '#ffffff',
            'hover' :  '#f5f2f0',
            'pressed' : '#4f4f4f'
        }

        self.buttonSurface = pygame.Surface((self.width,self.height))
        self.buttonRect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.buttonSurf = font.render(buttonText,True, (0,0,0))

        objects.append(self)

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True 
            else:
                self.alreadyPressed = False
        
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        window.blit(self.buttonSurface, self.buttonRect)

global started
started = False

global reseted
reseted = False

global stopped
stopped = False

def startFunction():
    global started, reseted, stopped, init_time, past
    if not started and reseted and stopped:
        init_time = pygame.time.get_ticks()
    if not started and not reseted and stopped:
        init_time = pygame.time.get_ticks()-past
    started = True
    reseted = False
    stopped = False
    
def pauseFunction():
    global started, reseted, stopped
    started = False
    reseted = False
    stopped = True
    global init_time
    init_time = pygame.time.get_ticks()

def stopFunction():
    global started, stopped, reseted
    started = False
    reseted = True
    stopped = True
    global init_time
    init_time = pygame.time.get_ticks()  

def resetFunction():
    global started, reseted, stopped
    started = True
    reseted = True
    stopped = True
    global init_time
    init_time = pygame.time.get_ticks()
    print(init_time)

Button(170,300,50,40,'Start',startFunction)
Button(240,300,50,40,'Pause',pauseFunction)
Button(310,300,50,40,'Stop',stopFunction)
Button(380,300,50,40,'Reset',resetFunction)

while True:
    window.fill((0,0,0))
    for ev in pygame.event.get():
        if ev.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    for obj in objects:
        obj.process()
    
    #start
    if started and not reseted and not stopped:
        ticks = pygame.time.get_ticks()-init_time
        
    #pause
    if not reseted and stopped:
        ticks = init_time
        past = init_time

    #stop
    if not started and reseted and stopped:
        ticks = init_time

    #reset
    if started and reseted and stopped:
        ticks = 0    

    millis=int(ticks%1000)
    seconds = int(ticks/1000 % 60)
    minutes=int(ticks/60000 % 60)
    hours = int((ticks/3600000) % 24)
    out='{hours:02d} : {minutes:02d} : {seconds:02d} : {millis:03d}'.format(hours=hours, minutes=minutes, seconds=seconds, millis=millis)
    outSurface = font2.render(out,False,pygame.Color('dodgerblue'))

    window.blit(outSurface, (125,95))
    pygame.display.flip()


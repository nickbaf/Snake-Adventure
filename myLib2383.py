#***************************************#
#   Nikolaos Bafatakis, AEM 2383        #
#       nikompaf@csd.auth.gr            #
#    Snake Adventure Beta v1.10.0       #
#                                       #
#          >>Libraries<<                #
#***************************************#






import pygame, sys,time
from pygame.font import SysFont
from random import randint
from collections import deque
from pygame.locals import *
from pygame.sprite import *




def clear_screen(surf):
    '''Method for clearing the screen with white color'''
    surf.fill((255,255,255))
    pygame.display.update()
    

def main_screen(surf):
    '''Method for showing the menu screen on the screen,it loads an image and blits
    it into the screen...The Menu options are handled within the menu screen loop in main.py'''
    rect=pygame.Rect(0,0,1280,720)
    sprite=pygame.image.load('Images/loadscreen.bmp').convert()
    surf.blit(sprite,(0,0))
    pygame.display.update()

def createEngine():
    '''Method that reads the game data from a file and creates the Engine set that
    contains every data for each of the levels of the game'''
    fo = open("data.txt", "r")
    engine=[]
    while True:
        l1=fo.readline()
        if l1=='':
            break
        else:
            l2=str(fo.readline())
            score=str(fo.readline())
        c=[]
        '''Because we read from the file a color in the format(xxx,yyy,zzz)
        readline converts it to string,so this for-loop takes only the 9 numbers given: xxx,yyy,zzz and discards
        the commas and the brackets'''
        for i in range(0,12):
            if i % 4==0:
                continue
            c.append(l2[i])
        e=Engine(l1,c,score)
        #Each engine contains the necessery data for handling each level of the game
        #of course we can expand the engine class to implement more options for each level
        engine.append(e) 
    return engine
        
    
    
class Engine():
    '''This class represents a level in the game,it stores all the necessery info for hadling each level of the game.'''
    def __init__(self,objective,c,s):
        '''Basic constractor that stores:
        i)The Goal of the level(objective)
        ii)The colour of the level(c)
        iii)The number of points required to win the level'''
        self.objective=objective
        self.color=[]
        self.color.append(int(c[0])*100+int(c[1])*10+int(c[2]))
        self.color.append(int(c[3])*100+int(c[4])*10+int(c[5]))
        self.color.append(int(c[6])*100+int(c[7])*10+int(c[8]))
        self.score=s

class Option(Sprite):
    '''This class represents the options for the main menu.With this class a minor animation effect is implemented
    in the main menu of the game.'''
    def __init__(self,Xaxis,Yaxis,txt,step,color,dimX=300,dimY=50,speed=2):
        '''Basic constractor that handles:
        i)the text(e.x Start,Quit)(txt)
        ii)the step, in the animation were the text gets draged from the left we can add a step
        in order to seperate each animation.(Note in the main menu screen the "Quit" tile makes a slight delay)
        iii)the color of the text
        iv)The X axis and the Y axis that the text is shown.'''
        
        self.Xaxis=Xaxis
        self.Yaxis=Yaxis
        Sprite.__init__(self)
        self.rect=pygame.Rect(Xaxis-2000-step,Yaxis,dimX,dimY)
        self.t=text(txt,color,70)
    def move(self,surf):
        '''The animation handler that moves the text into the screen from the outer left to the
        the point specified form the user in the Xaxis and Yaxis.'''  
        flag=True
        if self.rect.x<self.Xaxis:
            self.rect.move_ip(30,0)
            flag=False
        #print(self.rect.x,self.rect.y)
        self.t.render(surf,self.rect.x,self.rect.y)
        return flag
    def pos(self):
        '''Method for returning the position of the option text.This method has been kept only for debug perposes'''
        return (Xaxis,Yaxis)
        
class text():
    '''Class for printing text to screen.'''
    def __init__(self,t,color,size):
        '''Constractor that uses pygame.font.SysFont to build the text'''
        self.t=t
        self.font=pygame.font.SysFont('Calibri',size,True)
        self.text=self.font.render(self.t,True,color)
    def colorChange(self,color):
        '''Method for changing the color of the text'''
        self.text=self.font.render(self.t,True,color)

    def render(self,surf,x,y):
        '''Method for bliting the text into a surface'''
        surf.blit(self.text,(x,y))

class Score():
    '''This class implements a scoreboard that keeps track of time and the player's score'''
    def __init__(self):
        '''Constractor that:
        i)initializes the time,score and total score'''
        self.score=0
        self.level=50 #THE TIME that is used in the game.
        self.time_now=100
        self.start_time=0
        self.totalscore=0
    def start_timer(self):
        '''Method for capturing the current time'''
        self.start_time=time.time()
    def changeScore(self,apple):
        '''Method for changing the score.'''
        if apple == 1: #Standard Aapl
            self.score += 50
            self.totalscore +=50
        elif apple == 2:#Luxury Aalp,NOT used in this game
            self.score +=250
            self.totalscore+=250
        elif apple ==3:#Lives,that isn't used either.Maybe in a later version(!).
            self.lives -=1
      
    def printScore(self, surf):
        '''Method that blits the score and the remaining time into the screen'''
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)   
        score_now=text('Score:   '+str(self.score),(255,200,5),30)
        score_now.render(surf,1050,2)
        self.time_now=int(self.level+self.start_time-time.time())
        t=text('Time:   '+str(self.time_now),(255,200,5),30)
        t.render(surf,12,5)
        
        

class Direction:
    '''Class that represents a direction.
    When a snake's tail is due to turn into a direction it will be the coordinates(x,y)
    that will tell the tail where to turn'''
    def __init__(self,x,y,d):
        self.xAxis=x
        self.yAxis=y
        self.direction=d
class Aapl(Sprite):
    '''Aapl(Apple Inc. stock symbol in NASDAQ), is as you imagined the apple that the snake eats.
    it spawns randomly into the screen in size  30x30 pixels''' 
    def __init__(self,dimX=30, dimY=30):
        '''Basic contstructor for Aapl which handles:
        i)the X and Y cordinates in the screen, which are produced in random order
        ii)image of the Aapl.'''
        Sprite.__init__(self)
        self.createX=randint(30,1250)
        self.createY=randint(30,690)
        self.rect=pygame.Rect(self.createX, self.createY, dimX, dimY)
        self.image=pygame.image.load('Images/aapl.png')
        self.transimage = pygame.transform.scale(self.image, (dimX, dimY))
    def projectAapl(self,surf):
        '''Method for blitting the Aapl in screen'''
        surf.blit(self.transimage, self.rect)
class Snake(Sprite):
    '''This class represents the Snake used in the game'''
    def __init__(self, createX, createY,img,\
                 dimX=30, dimY=30, speedX=1):
        '''Constructor that gives birth to a little tiny snake 30 by 30 pixels.This constructor handles:
        i)X and Y cordinates
        ii)Image of the Snake
        iii)The orientation which the snake moves is represented by boolean variables.
        iv)Speed of the snake which is 1 pixel per frame.Changing this requires further modification of the game code.'''
        Sprite.__init__(self)
        self.rect=pygame.Rect(createX, createY, dimX, dimY)
        self.image=pygame.image.load(img)
        self.transimage = pygame.transform.scale(self.image,(dimX,dimY))
        self.moveLeft=False
        self.moveRight=False
        self.moveUp=False
        self.moveDown=False
        self.speedX=speedX
        self.corners=deque([])
        if(img=='Images/head.png'):#Boolean variable to recognise the head of the snake
            self.head=True
        else:
            self.head=False
    def tailTurn(self,x,y,direction):
        '''Overiding Method for turning the tail of the snake'''
        pass
    def resetMovement(self):
        '''Resets the movement of the snake'''
        self.moveLeft=False
        self.moveRight=False
        self.moveUp=False
        self.moveDown=False
    def getMove(self):
        '''Methof that returns a string representation of the direction of the
        snake that it's currently moving at.'''
        if self.moveRight:
            return 'Right'
        elif self.moveLeft:
            return 'Left'
        elif self.moveUp:
            return 'Up'
        else:
            return 'Down'
    def setMove(self,move):
        '''Method that takes as argument a string representation of a
        direction(e.x Right,Up) and sets this direction to the snake.'''
        if move=='Right':
            self.moveRight=True
        elif move=='Left':
            self.moveLeft=True
        elif move=='Up':
            self.moveUP=True
        else:
            self.moveDown=True
    def move(self, surf, horiz=800):#!!!!!!!!DES HORIZ
        '''Method for moving the snake in the screen.
        After checking to which direction the snake wants to be moved, then it moves the rectangle and applies the right image to the snake
        .We have 4 images for the head representing 4 different directions.Appling this policy, that with the change of movement we
        change the picture instead than rotating the original one;was made in order to make the code faster and more reliable.This solution
        of replacing the picture was applied in the optimization process of the code''' 
        if self.moveLeft:
            self.rect.move_ip(-self.speedX, 0)
            self.transimage = pygame.transform.scale(pygame.image.load('Images/headLeft.png'),(30,30))
        elif self.moveRight:
            self.rect.move_ip(self.speedX, 0)
            self.transimage = pygame.transform.scale(pygame.image.load('Images/headRight.png'),(30,30))
        elif self.moveUp:
            self.rect.move_ip(0,-self.speedX)
            self.transimage = pygame.transform.scale(pygame.image.load('Images/headUp.png'),(30,30))
        elif self.moveDown:
            self.rect.move_ip(0,self.speedX)
            self.transimage = pygame.transform.scale(pygame.image.load('Images/headDown.png'),(30,30))
        surf.blit(self.transimage, self.rect)

class Tail(Snake):
    '''This class represents a tail of the little snake.It inherits from the class Snake, and each snake has
    a couple number of tails.'''
    def __init__(self, createX, createY,img,\
                 dimX=30, dimY=30, speedX=1):
        Snake.__init__(self,createX, createY,img)


    def tailTurn(self,x,y,direction):
        '''Method for appending in the queue a turn in the Snake's tail'''
        a=Direction(x,y,direction)
        self.corners.append(a)
    def setMove(self,move):
        if move=='Right':
            self.moveRight=True
        elif move=='Left':
            self.moveLeft=True
        elif move=='Up':
            self.moveUP=True
        else:
            self.moveDown=True
    def move(self, surf, horiz=800):
        '''Method for moving the tail of the snake.
        Every time the head turns, a direction object is created with attributes: the direction of the snake and the coordinate(x,y)
        in which when the tail reaches, it must turn.'''
        if(len(self.corners)>0): #If the queue isn't empty, meaning that the tails must turn somewhere
            a=self.corners[0] #pop the first direction
            #print(a.xAxis,self.rect.x,a.yAxis,self.rect.y)
            if a.xAxis==self.rect.x and a.yAxis==self.rect.y: #if the current position of the tail matches the position in which the tail must turn
                self.resetMovement() #reset the tail's movement
                movement=a.direction #take the direction from a and set it to the tail
                if movement=='Down':
                    self.moveDown=True
                elif movement=='Up':
                    self.moveUp=True
                elif movement=='Right':
                    self.moveRight=True
                elif movement=='Left':
                    self.moveLeft=True
                self.corners.popleft() #remove the direction from the queue
        if self.moveLeft:
            self.rect.move_ip(-self.speedX, 0)
        elif self.moveRight:
            self.rect.move_ip(self.speedX, 0)
        elif self.moveUp:
            self.rect.move_ip(0,-self.speedX)
        elif self.moveDown:
            self.rect.move_ip(0,self.speedX)
        surf.blit(self.transimage, self.rect)
class OST():
    '''Method that handles the Music of the Game'''
    def __init__(self,filename):
        '''Constructor that builds a Sound file gained from pygame.mixer'''
        self.s=pygame.mixer.Sound(filename)
    def starti(self,i):
        '''Method for starting the playback of the sound'''
        self.channel=self.s.play(i)
    def start(self):
        self.channel=self.s.play()
    def stop(self):
        '''Method for stoping the playback of the sound'''
        self.s.stop()
    def pause(self):
        '''Method for pausing the playback of the sound'''
        pygame.mixer.init()
        self.channel.pause()
    def unpause(self):
        '''Method for unpausing the playback of the sound.This method is not working(yet)!!!!'''
        self.channel.unpause()

        

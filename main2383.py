#***************************************#
#   Nikolaos Bafatakis, AEM 2383        #
#       nikompaf@csd.auth.gr            #
#    Snake Adventure Beta v1.10.0       #
#                                       #
#   >>Intro+Splash Screen+Main Game<<   #
#***************************************#

from myLib2383 import *
from myLib2383 import Snake
from myLib2383 import Engine
import time
import pygame
from multiprocessing import Process,Pipe

HORIZ=1280
VERT=720


def dead_sequence(surf,level,totalpoints):
    '''Method for showing the sequence when the player dies'''
    rect=pygame.Rect(0,0,1920,1000)
    sprite=pygame.image.load('Images/dead snake.bmp').convert()
    lvl=text('Maximum levels played: '+str(level-1),(255,80,100),50)
    pnts=text('Total points Gathered:    '+str(totalpoints),(255,80,100),50)
    surf.blit(sprite,(0,0))
    lvl.render(surf,200,450)
    pnts.render(surf,200,500)
    pygame.display.update

def win_sequence(surf,level,totalpoints):
    '''Method for showing the sequence when the player finishes the game'''
    rect=pygame.Rect(0,0,1920,1000)
    sprite=pygame.image.load('Images/won.bmp').convert()
    pnts=text('Total points Gathered  '+str(totalpoints),(255,70,255),50)
    surf.blit(sprite,(0,0))
    pnts.render(surf,200,520)
    pygame.display.update

def main(args):
    '''The main class of the game that utilises the intro video and the main menu screen logic'''
    #SET THE GAME ENGINE
    pygame.init()
    clock=pygame.time.Clock()
    HORIZ=1280
    VERT=720
    GREEN = (0, 255, 0)
    '''The options buttons are created with tags for starting or quiting the game'''
    o1=Option(200,450,'New Adventure',0,GREEN) #Option Buttons doesn't implement adaptive resolution
    o2=Option(205,550,'Quit',200,GREEN)     #If resolution changes, change these as well
    options=[]
    options.append(o1)
    options.append(o2)
    my_screen = pygame.display.set_mode((HORIZ,VERT),0, 32)
    pygame.display.set_caption('Snake Adventure v1.1')
    pygame.mixer.init()
    #PREPARE THE SOUNDTRACK
    s1=OST('Sound/castle.ogg')
    s=OST('Sound/rest.ogg')
    s2=OST('Sound/rest2.ogg')
    #PREPARE THE INTRO MOVIE
   # m=pygame.movie.Movie('Video/main.mpg') Pygame.Movie Was beend disavowed..........
    '''The main menu consists of 3 different types:
    i)Intro video+Main menu for starting a new game or quit the game.
    ii)Main menu for starting a new game or quit the game(No intro video shown).
    iii)Main menu(or Pause menu) with options to continue the game or quit it(No intro video shown)'''
    if args==1:#Menu type No.1
       '''movie_screen=pygame.Surface((1280,720)).convert()
        m.set_display(movie_screen) #Play the movie
        s1.start()
        m.play()
        pygame.mouse.set_visible(False)
        flag=True #start playing the movie
        flag2=True
        tick=60 #The movie is 60p
        '''
    elif args==2: #Menu type No.2
        flag=False #don't play the movie 
        flag2=True
        s2.start()
        tick=30
    elif args==3: #Menu No.3
        pygame.mixer.init()
        o1=Option(200,450,'Continue Adventure',0,GREEN) #Change the option text
        options[0]=o1
        flag=False #Don't play the movie
        flag2=True
        s2.start()
        tick=30
    optionsFlag=False
    theFLAG=True #Dont change this
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~Main Menu Logic~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    while theFLAG:
        if flag2: #Until all the menu events-animations finishes(intro movie and menu animations)
            if flag and m.get_frame()==452: #if the video is played and it reached the maximum frames
                flag=False #stop the playback loop
                s1.stop() #stop the music
                m.stop() #stop the movie
                main_screen(my_screen) #start the main menu screen
                s.start() #start the main menu music
                pygame.mouse.set_visible(True) #unhide the mouse!
                pygame.event.clear()#if user presses key when video is displayed it will be cleared
                tick=30 #lock the fps to 30p
            elif flag and m.get_frame()<907: #while the video must be played and the video havn't reached the maximum frames yet
                  my_screen.blit(movie_screen,(0,0)) #blit the next frame of the movie
            else: #play the animations
                main_screen(my_screen)
                t1=options[0].move(my_screen)
                t2=options[1].move(my_screen)
                if t1==True and t2==True: #if animations have finished
                    flag2=False # get out from the events-animations branch
        if True: #Open events     
            for ev in pygame.event.get():
                if flag==False:
                    if options[0].rect.collidepoint(pygame.mouse.get_pos()): #if the mouse colledes with the 1st option
                        #Highlight the option
                        optionsFlag=True #set a flag in order to notify the system that the text is highlighted
                        main_screen(my_screen)
                        options[0].t.colorChange((255,190,255))
                        options[0].move(my_screen)
                        options[1].move(my_screen)
                        if pygame.mouse.get_pressed()[0]==True: #if player presses the button
                            if(o1.t.t=='Continue Adventure'): #if we are in menu No.3
                                theFLAG=False
                                s2.stop()
                                #pygame.mixer.quit()
                                return
                           # clear_screen(my_screen)
                            if pygame.mixer.get_init()!=None: #Cut the soundtrack
                                pygame.mixer.stop()
                            p=Process(target=game(),args=(0)) #create a new process
                            p.start() #start the process
                            theFLAG=False
                            break
                    elif options[1].rect.collidepoint(pygame.mouse.get_pos()):#if the mouse colledes with the 2st option(Quit)
                        optionsFlag=True
                        main_screen(my_screen)
                        options[1].t.colorChange((255,190,255))
                        options[1].move(my_screen)
                        options[0].move(my_screen)
                        if pygame.mouse.get_pressed()[0]==True:
                            pygame.quit() #Exit the game engine
                            sys.exit()    #Exit the game
                    elif optionsFlag: #else if the mouse moves away from an option unhightlight the text
                        #This flag is used because in every clock tick the engine redraws the whole screen and the
                        #text seems flickering
                        optionsFlag=False
                        main_screen(my_screen)
                        options[0].t.colorChange(GREEN)
                        options[1].t.colorChange(GREEN)
                        options[0].move(my_screen)
                        options[1].move(my_screen)
        pygame.display.update()
        clock.tick(tick)

def game():
    '''This method is used for the game's logic'''
    #SET THE GAME ENGINE
    clock = pygame.time.Clock()
    obj=createEngine() #Create the game data
    HORIZ=1280
    VERT=720
    screen = pygame.display.set_mode((HORIZ,VERT), 0,32)
    r=pygame.Rect(0,40,HORIZ,VERT-40)
    pygame.mixer.init()
    level_music=OST('Sound/main.ogg')
    level_music.starti(5)
    pygame.display.set_caption('Snake Adventure v1.1')
    BLACK = (0, 0, 0)
    GREEN = (10,170,82) #125,170,84
    screen.fill(GREEN)
    #Create a little tiny snake 
    my_snake=Snake(150,50,'Images/headRight.png')
    my_body=Tail(125,50,'Images/body.png')
    my_body0=Tail(100,50,'Images/body.png')
    my_body1=Tail(75,50,'Images/body.png')
    apple1=Aapl() #Grow an Aapl
    thesnake=[] #Create a list to place the snake's body
    thesnake.append(my_body)
    thesnake.append(my_body0)
    thesnake.append(my_body1)
    #Create the game's scoreboard
    score =Score()
    pygame.display.update()
    my_snake.resetMovement() #Reset the movement of the snake
    my_snake.moveRight=True #set the movement to the right
    for s in thesnake: #set the movement to the right of all the snake's tails
        s.resetMovement()
        s.moveRight=True
    count=1 #The level of the game
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #~~~~~~~~~Game Logic~~~~~~~~#
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #Show the OBJECTIVE
    for objective in obj: #For all the levels in the game
        e=objective
        #DEBUG PERPOSES ONLY#################################
        print('LEVEL ',count)################################
        print('TARGET==',e.score)############################
        print('Color ',(e.color[0],e.color[1],e.color[2]))###
        #####################################################
        count+=1 #Increase the level    
        screen.fill((e.color[0],e.color[1],e.color[2])) #fill the screen with the prefered color
        before=time.time() #capture(!) the time
        score.score=0 #set the score to 0(zero)
        #Print the Objective to the player
        t1=text('Current Objective:',(255,200,40),50) 
        t2=text(e.objective[:len(e.objective)-1],(255,255,255),50)
        #Blit the level's goal to the screen for 6 seconds
        while True:
            screen.fill((e.color[0],e.color[1],e.color[2]))
            pygame.draw.rect(screen,(0,0,0),r,10)
            t2.render(screen,-400+HORIZ/2,-100+VERT/2)
            t1.render(screen,-500+HORIZ/2,-170+VERT/2)
            after=time.time()
            if after-before>6:
                break;
            tme=text(str(5+int(before-after)),(255,200,0),400) #Countdown the time till the start of the level
            tme.render(screen,+260+HORIZ/2,-30+VERT/2)
            pygame.display.update()
            clock.tick(24)
            pygame.event.get()
        tick=120
        screen.fill((int(e.color[0]),int(e.color[1]),int(e.color[2])))
        score.start_timer() #Start game's countdown time
        while True:
            ###SNAKE COLLISION###
            #If the snake collides with the outer rectangle
            if my_snake.rect.colliderect(r)==False:
                #Start the dead snake sequence
                level_music.stop() #Stop the music
                timer=time.time()
                d=OST('Sound/dead snake.ogg') #play the funeral march
                d.start()
                while True: #wait 4 seconds until the screen changes to the death screen(Creative Director's orders)
                    pygame.display.update()
                    if (int(4+timer-time.time()))==0:
                        break
                print('Little Snake Died')
                #clear_screen(screen) Shows blank screen...its bad
                timer=time.time()
                while True:#show the death screen for 9 seconds and then return to main menu
                    pygame.event.clear()
                    if (int(9+timer-time.time()))==0: #if time is up!
                        print('Reseting to Menu')
                        p=Process(target=main(2),args=(0))#Go to menu No.2 (no intro video,just the menu)
                        p.start()
                        return
                    dead_sequence(screen,count,score.totalscore) #show the death screen with the total level's played(count) and the total score(score.totalscore)
                    pygame.display.update()
                
            #WIN || LOOSE
            if score.time_now==0: #if the time is up, return to main menu
                level_music.stop()
                p=Process(target=main(2),args=(2))
                p.start()
                break;
            if score.score >= int(e.score):#if the player reaches the maximum points of the level go to the next one or leave the game
                break
            #Aapl
            if apple1.rect.colliderect(my_snake.rect): #if the player collides with the Aapl
                if score.score+50 >= int(e.score) and count-1==len(obj): #if the player has reached the objective break and proceed to the next level
                    score.changeScore(1)
                    break
                score.changeScore(1)#change the score
                apple1=Aapl()#grow a new Aapl
                x=thesnake[-1].rect.x #get the coordinates of the last tail
                y=thesnake[-1].rect.y
                movement=thesnake[-1].getMove() #get the movement of the last tail
                #grow a new tail to the end of the snake 
                if movement=='Right':
                    n=Tail(x-25,y,'Images/body.png')
                    n.moveRight=True
                elif movement=='Left':
                    n=Tail(x+25,y,'Images/body.png')
                    n.moveLeft=True
                elif movement=='Up':
                    n=Tail(x,y+25,'Images/body.png')
                    n.moveUp=True
                else:
                    n=Tail(x,y-25,'Images/body.png')
                    n.moveDown=True;
                n.corners=deque(thesnake[-1].corners) #attach the corners queue to the new snake in order to continue moving accordingly
                thesnake.append(n) #append the tail
                tick=tick+25 #increase the tick
            for ev in pygame.event.get():
                x=my_snake.rect.x #get the snake's coordinates
                y=my_snake.rect.y
                if pygame.mouse.get_pressed()[0]: #DEBUB:if you press the left mouse btn, the fps gets print
                    print(clock.get_fps())
                if ev.type == QUIT:
                    pygame.quit()                
                    sys.exit()
                '''Moving the snake:
                if the player presses btn X:
                i)if the snake currently moves in X direction nothing will happen
                ii)if not,reset the head's movement and start moving it to direction X
                iii)for every tail: call tail turn in order to turn the tails to direction X'''
                if ev.type == KEYDOWN:
                    if ev.key == K_LEFT:
                        if my_snake.moveLeft:
                            break
                        my_snake.resetMovement()
                        my_snake.moveLeft=True;
                        for s in thesnake:
                            s.tailTurn(x,y,'Left')
                    if ev.key == K_RIGHT:
                       if my_snake.moveRight==True:
                            break
                       my_snake.resetMovement()
                       my_snake.moveRight=True;
                       for s in thesnake:
                           s.tailTurn(x,y,'Right')                 
                    if ev.key == K_UP:
                        if my_snake.moveUp==True:
                            break
                        my_snake.resetMovement()
                        my_snake.moveUp=True;
                        for s in thesnake:
                            s.tailTurn(x,y,'Up')
                    if ev.key == K_DOWN:
                        if my_snake.moveDown==True:
                            break
                        my_snake.resetMovement()
                        my_snake.setMove('Down')
                        my_snake.moveDown=True
                        for s in thesnake:
                            s.tailTurn(x,y,'Down')
                    if ev.key == K_ESCAPE:#WARNING:Time advnaces as player is sitting in the pause menu
                        pygame.mixer.quit()
                        current_time=score.time_now
                        level_music.pause()
                        main(3)
                        score.time_now=current_time
                        level_music.stop()
                        level_music.start()
                        continue
            ###SCREEN DRAWING##
            screen.fill((int(e.color[0]),int(e.color[1]),int(e.color[2]))) #blit the color
            my_snake.move(screen)#blit the little snake
            for s in thesnake:#blit the tails
                s.move(screen)
            apple1.projectAapl(screen)#blit the Aapl
            score.printScore(screen)#blit the scoreboard
            pygame.draw.rect(screen,(0,0,0),r,10)#blit the outer rectangle
            pygame.display.update()#and of course update the screen
            clock.tick(tick)#tick the clock as well


    ###THE GAME HAS ENDED AND THE PLAYER ADVANCED TO ALL LEVELS###
    level_music.stop() #stop the music
    w=OST('Sound/win.ogg') #pay the win triumph
    w.start()
    timer=time.time()
    while True:#freeze the screen for 5 secs
       pygame.event.clear()
       if (int(5+timer-time.time()))==0:
           break
    print('GAME ENDED')
   # clear_screen(screen)
    timer=time.time()
    level_music.stop()
    while True:#show the win sequence for 8 secs
        pygame.event.clear()
        if (int(8+timer-time.time()))==0:
            print('RESETING TO MENU')
            p=Process(target=main(2),args=(0))
            p.start()   
            break
        win_sequence(screen,count,score.totalscore)
        pygame.display.update()   





    
if __name__ == '__main__':
    print(__name__)
    main(2) #Run main No.1
    #main(2)#Run main No.2
    #game() #Run the game only

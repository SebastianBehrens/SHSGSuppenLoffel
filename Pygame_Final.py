import pygame
import os
from dataclasses import dataclass
import random

#size of the game displayed (pixel), as it will be square we only need an x value
auflösung = 800
# Sets the beginning Values of the Game, Size of the Game and amount of Mines
global raster, abstand, anzMinen
raster = 10 #int(input("Please enter the size of your Game: "))
abstand = auflösung // raster
anzMinen = 10 #int(input("Please enter the number of mines: "))
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green= (0, 200, 0)
bright_green= (0, 255, 0)
# Initializes the pyGame engine
pygame.init()
# Defining a screen display
screen = pygame.display.set_mode([auflösung, auflösung])
# Naming the Window
pygame.display.set_caption("Minesweeper by SHSG Summerschool")
clock = pygame.time.Clock()
# Importing all images needed for the programm
#print(os.getcwd())
cell_normal = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","Feld.png")), (abstand,abstand))
cell_marked = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","FeldFlagge.png")), (abstand,abstand))
cell_mine = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","BombeFeld.png")), (abstand,abstand))
cell_explosion = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","Exp.png")), (abstand,abstand))
cell_mine_cross = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","BombCross.png")), (abstand,abstand))
game_over = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","GameOver.png")), (900,900))
you_win = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","YouWin.png")), (592,200))
summerschool = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","summerschool.png")), (600,115))
bombe = pygame.image.load(os.path.join("Minesweeper Graphics","Bombe.png"))
cell_selected = []
for n in range(9):
    cell_selected.append(pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics", f"{n}.png")), (abstand,abstand))) 
#Defining a Matrix that can be filled later, this will help us create the grid for our game
matrix = []
#Defining the fields next to the mine as a criteria that can later be accessed
benachbarteFelder = [(-1,-1),(-1,0),(-1,+1),(0,-1),(0,+1),(+1,-1),(+1,0),(+1,+1)]

# Defining the class for the game which can later be accessed
@dataclass
class Zelle():
    zeile : int
    spalte : int
    mine : bool = False
    selected : bool = False
    flagged : bool = False
    anzMinenDrumrum = int = 0

    def show(self):
        pos=(self.spalte*abstand, self.zeile*abstand)
        if self.selected:
            if self.mine:
                screen.blit(cell_mine, pos)
            else:
                screen.blit(cell_selected[self.anzMinenDrumrum], pos)
        else:
            if self.flagged:
                screen.blit(cell_marked, pos)
            else:
                screen.blit(cell_normal, pos)
    #Counting the amount of mines in the game
    def anzahlMinenErmitteln(self):
        for pos in benachbarteFelder:
            neueZeile = self.zeile + pos[0]
            neueSpalte = self.spalte + pos[1]
            if neueZeile >= 0 and neueZeile < raster and neueSpalte >= 0 and neueSpalte < raster:
                if matrix[neueZeile*raster+neueSpalte].mine:
                    self.anzMinenDrumrum+=1

    # Defining function for making sure that all emty cells are also uncovered when one next to them is empty
def floodFill(zeile, spalte):
    for pos in benachbarteFelder:
        neueZeile = zeile + pos[0]
        neueSpalte = spalte + pos[1]
        if neueZeile >= 0 and neueZeile < raster and neueSpalte >= 0 and neueSpalte < raster:
            cell = matrix[neueZeile*raster+neueSpalte]
            if cell.anzMinenDrumrum == 0 and not cell.selected:
                cell.selected = True
                floodFill(neueZeile, neueSpalte)
            else: 
                cell.selected = True

# defining function for text objects
def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

# defining functions for buttons which can be used
# defines an area of a button which is clickable. therfor an action can be taken
# if you hover over the field of you button, the color changes
def button(msg,x,y,w,h,color,activated_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, activated_color,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, color,(x,y,w,h))
    smallText = pygame.font.Font('freesansbold.ttf', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (((x+(w/2)),(y+(h/2))))
    screen.blit(textSurf, textRect)
    
#the game intro is the introduction to the game
#it makes a screen appear where you can decide to start the game
#it also gives the game a title and can display logos and graphics
def game_intro():

    intro = True
    pygame.mixer.music.load('intro_music.mp3')
    pygame.mixer.music.play(0)
    while intro:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.fill(black)

        screen.blit(bombe, (300,-50))
        screen.blit(summerschool, (100,130))
        largeText = pygame.font.Font('freesansbold.ttf', 100)
        TextSurf, TextRect = text_objects("MINESWEEPER", largeText)
        TextRect.center = ((auflösung/2), (auflösung/2))
        screen.blit(TextSurf, TextRect)
        button("START",200,550,150,50,green,bright_green, game_loop)
        button("START IN RED",450,550,150,50,red,bright_green, game_loop)
        pygame.display.update()
        clock.tick(15)

# game function
def game_loop():
    global anzMinen, raster
    #Creating the grid for the game
    for n in range(raster*raster):
        matrix.append(Zelle(n // raster, n % raster))
    #Randomly placing mines in the grid
    while anzMinen > 0:
        x = random.randrange(raster*raster)
        if not matrix[x].mine:
            matrix[x].mine = True
            anzMinen-=1
    for objekt in matrix:
        objekt.anzahlMinenErmitteln()
    #This is the game engine which also lets the mouse click on the fields
    #In this process we define the actions which are taken by the clicks and how the fields react
    weitermachen = True
    #initiation of the game and starts the music
    pygame.mixer.music.load('Minesweeper.mp3')
    pygame.mixer.music.play(0)
    while weitermachen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                weitermachen = False
            # determination of the mouse button which is pressed and where
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                spalte = mouseX // abstand
                zeile = mouseY // abstand
                i = zeile*raster+spalte
                cell = matrix[i]
                if pygame.mouse.get_pressed()[2]:
                    cell.flagged = not cell.flagged
                if pygame.mouse.get_pressed()[0]:
                    cell.selected = True
                    # if a cell is zero it opens all the cells arount it too
                    if cell.anzMinenDrumrum == 0 and not cell.mine:
                        floodFill(zeile, spalte)
                    # if the clicked cell is a mine, it shows game over and plays an explostion sound previous to ending the game
                    # the time delays are used to make the display more attractive to the user
                    if cell.mine:
                        screen.blit(game_over,(-50,-50))
                        pygame.display.flip()
                        pygame.mixer.music.load('explosion.mp3')
                        pygame.mixer.music.play(-1, 1.0)
                        pygame.time.delay(1000)
                        pygame.display.flip()
                        for objekt in matrix:
                            objekt.selected = True
                        for objekt in matrix:
                            objekt.show()
                        pygame.display.flip()
                        pygame.time.delay(3300)
                        pygame.quit()
                    # This helps to indicate numbers for the determination of the win
                    count = []
                    countA = []
                    countB = []
                    for objekt in matrix:
                        if objekt.selected == True:
                            count.append(1)
                        if objekt.mine == False:
                            countA.append(1)
                       # if objekt.flagged == True:
                        #    countB.append(1)
                    print(len(countB))
                # This determines if you won the game and gives you an image and a melody
                if int(len(count)) == int(len(countA)): #and int(len(count)) == int(len(countB)):
                    pygame.mixer.music.load('win.mp3')
                    pygame.mixer.music.play(-1, 1.0)
                    screen.blit(you_win,(100,300))
                    pygame.display.flip()
                    pygame.time.delay(2300)
                    for objekt in matrix:
                        objekt.selected = True
                    for objekt in matrix:
                        objekt.show()
                    pygame.display.flip()
                    pygame.time.delay(5300)
                    pygame.quit()
      #This makes the game appear on the screen
        for objekt in matrix:
            objekt.show()
        pygame.display.flip()
game_intro()
pygame.quit()






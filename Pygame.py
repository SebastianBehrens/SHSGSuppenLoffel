import pygame as pygame
import os
from dataclasses import dataclass
import random

auflösung = 1000
raster = int(input("Please enter the size of your Game: "))
abstand = auflösung // raster
anzMinen = int(input("Please enter the number of mines: "))

pygame.init()
screen = pygame.display.set_mode([auflösung, auflösung])
#print(os.getcwd())
cell_normal = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","Feld.png")), (abstand,abstand))
cell_marked = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","FeldFlagge.png")), (abstand,abstand))
cell_mine = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","BombeFeld.png")), (abstand,abstand))
cell_explosion = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","Exp.png")), (abstand,abstand))
cell_mine_cross = pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics","BombCross.png")), (abstand,abstand))
cell_selected = []
for n in range(9):
    cell_selected.append(pygame.transform.scale(pygame.image.load(os.path.join("Minesweeper Graphics", f"{n}.png")), (abstand,abstand))) 

#screen.blit(cell_selected[2],(100,100))
#screen.blit(cell_two,(100,200))
#screen.blit(cell_explosion,(200,200))
#while True:
 #   pygame.display.flip()


matrix = []
benachbarteFelder = [(-1,-1),(-1,0),(-1,+1),(0,-1),(0,+1),(+1,-1),(+1,0),(+1,+1)]

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
    
    def anzahlMinenErmitteln(self):
        for pos in benachbarteFelder:
            neueZeile = self.zeile + pos[0]
            neueSpalte = self.spalte + pos[1]
            if neueZeile >= 0 and neueZeile < raster and neueSpalte >= 0 and neueSpalte < raster:
                if matrix[neueZeile*raster+neueSpalte].mine:
                    self.anzMinenDrumrum+=1

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


for n in range(raster*raster):
    matrix.append(Zelle(n // raster, n % raster))

while anzMinen > 0:
    x = random.randrange(raster*raster)
    if not matrix[x].mine:
        matrix[x].mine = True
        anzMinen-=1

for objekt in matrix:
    objekt.anzahlMinenErmitteln()


weitermachen = True
while weitermachen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weitermachen = False
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
                if cell.anzMinenDrumrum == 0 and not cell.mine:
                    floodFill(zeile, spalte)
                if cell.mine:
                    for objekt in matrix:
                        objekt.selected = True

    for objekt in matrix:
        #objekt.selected = True
        objekt.show()
    pygame.display.flip()

pygame.quit()




    
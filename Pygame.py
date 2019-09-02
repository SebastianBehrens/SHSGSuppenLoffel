import pygame as pygame
import os
from dataclasses import dataclass
import random

auflösung = 1000
raster = 10
abstand = auflösung // raster

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

anzMinen = 10
matrix = []

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

for n in range(raster*raster):
    matrix.append(Zelle(n // raster, n % raster))

weitermachen = True
while weitermachen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            weitermachen = False
    for objekt in matrix:
        objekt.show()
    pygame.display.flip()

pygame.quit()




    
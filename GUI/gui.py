import pygame as pg
from gui_objects import *

pg.init()

win = pg.display.set_mode((700, 700))
pg.display.set_caption("Science Fair 2020-2021")

clock = pg.time.Clock()

 
box = CheckBox(243, 252, 10, 10)
def drawMain(): 
    win.fill((255, 255, 255))

    font = pg.font.SysFont("comicsans", 60)
    text = font.render("ARCVision", 1, (0,0,0))
    win.blit(text, ((700 - text.get_width()) /2, 200))
    #print(text.get_height())
    box.draw(win)

    

run, main = True, True
while run:
    if main:
        drawMain()
        pg.display.update()

    for event in pg.event.get():
        pos = pg.mouse.get_pos()

        if event.type == pg.QUIT:
            run = False
            pg.quit()

        if main:
            if event.type == pg.MOUSEBUTTONDOWN and box.isHover(pos):
                print("TOGGLED")
                if box.isToggled:
                    box.isToggled = False
                else:
                    box.isToggled = True
            
            

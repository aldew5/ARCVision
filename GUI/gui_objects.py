import pygame as pg

class Button(object):
    def __init__(self, color, x, y, width, height):
        self.color = color
        self.x, self.y = (x, y)
        self.width, self.height = (width, height)
        
    def draw(self, win, outline=None):
        if outline:
            pg.draw.rect(win, outline, (self.x -2, self.y-2, self.width+4, self.height+4), 0)
        
        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
##        if (self.text != ""):
##            font = pg.font.SysFont("comicsans", 60)
##            text = font.render(self.text, 1, (0,0,0))
##            win.blit(text, (self.x + (self.width /2 - text.get_width() /2), self.y + (self.height /2 - text.get_height() /2)))
            
    def isHover(self, pos) -> bool:
        if (pos[0] > self.x and pos[0] < self.x + self.width):
            if (pos[1] > self.y and pos[1] < self.y + self.height):
                return True
                
        return False
a
class CheckBox(Button):
    def __init__(self, x, y, width, height):
        Button.__init__(self, (255,255,255), x, y, width, height)
        self.isToggled = False

    def draw(self, win):
        rect = pg.Rect(self.x, self.y, self.width, self.height)
        if not self.isToggled:
            #rect.fill((255,255,255), rect)
            pg.draw.rect(win, (0,0,0), rect, 2)
        else:
            rect.fill((255,255,255))
            pg.draw.rect(win, (0,0,0), (self.x, self.y, self.width, self.height), 2)

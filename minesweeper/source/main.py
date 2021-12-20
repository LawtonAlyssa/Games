import pygame as pg
from pygame.locals import *

purple = (85,11,202)

def setup():
    pg.init()
    
def draw_grid(g, tile_size, rows, columns, margin=1, **kwargs):
    for y in range(rows):
        for x in range(columns):
            pg.draw.rect(g,purple,(x*tile_size,y*tile_size,tile_size-margin,tile_size-margin))


def main():
    setup()
    clock = pg.time.Clock()
    
    tile_size = 64
    
    rows = 2
    columns = 16
    
    width, height = columns*tile_size, rows*tile_size
    g = pg.display.set_mode((width, height))

    while True:
        g.fill((0, 0, 0))
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return
    
        # draw here
        
        draw_grid(**locals()) 
        
        # add game logic here
        
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
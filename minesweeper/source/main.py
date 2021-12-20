import pygame as pg
from pygame.locals import *
from difficulty import Difficulty 
from random import randrange

purple = (85,11,202)

def setup():
    pg.init()
    
def draw_grid(g, tile_size, rows, columns, margin=1, **kwargs):
    for y in range(rows):
        for x in range(columns):
            pg.draw.rect(g,purple,(x*tile_size,y*tile_size,tile_size-margin,tile_size-margin))

def find_adjacent_bombs(row, col, bombs_present, rows, columns):
    num_bombs_present = 0
    for y in range(row-1,row+2):
        for x in range(col-1,col+2):
            if x>=0 and x<columns and y>=0 and y<rows and bombs_present[y][x] is True: # handles edges
                num_bombs_present += 1
    return num_bombs_present

def fill_num_bombs(bombs_present, rows, columns):
    for y in range(rows):
        for x in range(columns):
            if bombs_present[y][x] is False:
                bombs_present[y][x] = find_adjacent_bombs(y, x, bombs_present, rows, columns)

def fill_bombs_present(rows, columns, bombs):
    bombs_present = [[False for y in range(rows)] for x in range(columns)]

    bombs_placed = 0

    while bombs_placed < bombs:
        bomb_row = randrange(0,rows)
        bomb_col = randrange(0,columns)
        if not bombs_present[bomb_row][bomb_col]: 
            bombs_present[bomb_row][bomb_col] = True
            bombs_placed += 1
    
    fill_num_bombs(bombs_present, rows, columns)

    return bombs_present

def main():
    setup()
    clock = pg.time.Clock()
    
    mode = Difficulty.hard

    if(mode==Difficulty.easy):
        tile_size = 64
        rows =  9
        columns = 9
        bombs = 10
    elif(mode==Difficulty.medium):
        tile_size = 42
        rows =  16
        columns = 16
        bombs = 40
    elif(mode==Difficulty.hard):
        tile_size = 42
        rows =16
        columns = 30
        bombs = 99
    else:
        print("ERROR!!! Invalid difficulty mode")
        pg.quit()
        return

    bombs_present = fill_bombs_present(rows, columns, bombs)

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
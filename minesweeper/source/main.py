import imp
import pygame as pg
from pygame.locals import *
from difficulty import Difficulty 
from random import randrange
from typing import List, Tuple

purple = (85,11,202)

def setup():
    pg.init()
    pg.font.init() # you have to call this at the start, if you want to use this module.
    
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
    bombs_present = [[False for x in range(columns)] for y in range(rows)]

    bombs_placed = 0

    while bombs_placed < bombs:
        bomb_row = randrange(0,rows)
        bomb_col = randrange(0,columns)
        if not bombs_present[bomb_row][bomb_col]: 
            bombs_present[bomb_row][bomb_col] = True
            bombs_placed += 1
    
    fill_num_bombs(bombs_present, rows, columns)

    return bombs_present

def render_digits(digits_font):
    return [digits_font.render(str(digit), False, (255, 255, 255)) for digit in range(1,9)]

def draw_digits(g, rows, columns, tile_size, bombs_present, digits, digits_font):
    for y in range(rows):
        for x in range(columns):
            if bombs_present[y][x] is not True:
                if bombs_present[y][x] != 0:
                    digit = bombs_present[y][x]
                    g.blit(digits[digit-1],center_text(width=tile_size, height=tile_size, text=str(digit), font=digits_font, x_offset=x*tile_size,y_offset=y*tile_size))
                    
def render_game_over(game_over_font:pg.font.Font, bombs_found:int, **kwargs) -> List[Tuple[pg.Surface,Tuple[int,int]]] : 
    """renders game over text

    Args:
        game_over_font (pg.font.Font): font for game over
        bombs_found (int): number of bombs found
        **kwargs: window_width (int), window_height (int)

    Returns:
        List[Tuple[pg.Surface,Tuple[int,int]]]: blit arguments for each line
    """    
    out = []
    for text, y_offset in [("Game Over", -50), ("Bombs Found: "+str(bombs_found), 50)]:
        rendered = game_over_font.render(text, False, (255, 255, 255))
        offset = center_text(text=text, font=game_over_font, y_offset=y_offset, **kwargs)
        out.append((rendered, offset))
    return out
    
def draw_game_over(g, game_over_rendered):
    for text_tuple in game_over_rendered:
        g.blit(*text_tuple)

def center_text(width, height, text, font, x_offset=0, y_offset=0):
    text_width, text_height = font.size(text) #txt being whatever str you're rendering
    return (width - text_width)//2 + x_offset, (height - text_height)//2 + y_offset
  
def reset_game(rows, columns, bombs):
    bombs_present = fill_bombs_present(rows, columns, bombs) # reset game
    return bombs_present
      
def main():
    setup()
    clock = pg.time.Clock()
    
    digits_font = pg.font.SysFont('Comic Sans MS', 30)
    digits = render_digits(digits_font)
    
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
    bombs_found = 0
    

    window_width, window_height = columns*tile_size, rows*tile_size
    g = pg.display.set_mode((window_width, window_height))

    game_over_font = pg.font.SysFont('Comic Sans MS', 60)
    game_over_rendered = render_game_over(game_over_font, bombs_found, width=window_width, height=window_height)
    
    while True:
        g.fill((0,0,0))
        
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                return
    
        # draw here
        draw_grid(**locals()) 
        draw_digits(g, rows, columns, tile_size, bombs_present, digits, digits_font)
        
        # add game logic here
        # bombs_present = reset_game(rows, columns, bombs)
        # draw_game_over(g, game_over_rendered)
        
        pg.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
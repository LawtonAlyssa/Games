from email.mime import image
import imp
import pygame as pg
from pygame.locals import *
from difficulty import Difficulty 
from random import randrange
from typing import List, Tuple

purple = (85,11,202)
lt_purple = (85+30,11+30,202+30)

class Tile:
    def __init__(self):
        self.is_flag = False
        self.bombs_present = 0
        self.is_bomb = False
        self.is_revealed = False

def setup():
    pg.init()
    pg.font.init() # you have to call this at the start, if you want to use this module.
    
def draw_grid(g, tile_size, rows, columns, margin=1, **kwargs):
    for y in range(rows):
        for x in range(columns):
            pg.draw.rect(g,purple,(x*tile_size,y*tile_size,tile_size-margin,tile_size-margin))

def find_adjacent_bombs(row, col, tiles, rows, columns):
    num_bombs_present = 0
    for y in range(row-1,row+2):
        for x in range(col-1,col+2):
            if x>=0 and x<columns and y>=0 and y<rows and tiles[y][x].is_bomb is True: # handles edges
                num_bombs_present += 1
    return num_bombs_present

def fill_num_bombs(tiles, rows, columns):
    for y in range(rows):
        for x in range(columns):
            if tiles[y][x].is_bomb is False:
                tiles[y][x].bombs_present = find_adjacent_bombs(y, x, tiles, rows, columns)

def generate_tiles(rows, columns, bombs):
    tiles = [[Tile() for x in range(columns)] for y in range(rows)]

    bombs_placed = 0

    while bombs_placed < bombs:
        bomb_row = randrange(0,rows)
        bomb_col = randrange(0,columns)
        if not tiles[bomb_row][bomb_col].is_bomb: 
            tiles[bomb_row][bomb_col].is_bomb = True
            bombs_placed += 1
    
    fill_num_bombs(tiles, rows, columns)

    return tiles

def render_digits(digits_font):
    return [digits_font.render(str(digit), False, (255, 255, 255)) for digit in range(1,9)]

def draw_tiles(g, rows, columns, tile_size, tiles, digits, digits_font, bomb_image, flag_image, no_bomb_image, margin=1):
    for y in range(rows):
        for x in range(columns):
            tile = tiles[y][x]
            pixel_x = x*tile_size
            pixel_y = y*tile_size
            if tile.is_revealed:
                if tile.is_bomb:
                    g.blit(bomb_image, (pixel_x, pixel_y))
                else:
                    if tile.bombs_present != 0:
                        digit = tile.bombs_present
                        g.blit(digits[digit-1],center_text(width=tile_size, height=tile_size, text=str(digit), font=digits_font, x_offset=pixel_x,y_offset=pixel_y))
                    else:
                        pg.draw.rect(g, lt_purple, (pixel_x, pixel_y, tile_size-margin, tile_size-margin))
            elif tile.is_flag:
                g.blit(flag_image, (pixel_x, pixel_y))
            # elif not tile.is_bomb:

                    
def render_game_over(game_over_font:pg.font.Font, bombs_found:int, **kwargs) -> List[Tuple[pg.Surface,Tuple[int,int]]] : 
    """Renders game over text

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
    text_width, text_height = font.size(text) # txt being whatever str you're rendering
    return (width - text_width)//2 + x_offset, (height - text_height)//2 + y_offset
  
def reset_game(rows, columns, bombs):
    tiles = generate_tiles(rows, columns, bombs) # reset game
    return tiles

def convert_pixel_to_tile_coord(tile_size, pixel_x, pixel_y):
    return pixel_x//tile_size, pixel_y//tile_size  

def reveal_tile(tiles, tile_x, tile_y, columns, rows, **kwargs):
    tile = tiles[tile_y][tile_x]
    if tile.is_revealed: return
    tile.is_revealed = True
    if not tile.is_bomb and tile.bombs_present == 0:
        for y in range(tile_y-1,tile_y+2):
            for x in range(tile_x-1,tile_x+2):
                if x>=0 and x<columns and y>=0 and y<rows: # handles edges
                    reveal_tile(tiles, x, y, columns, rows)
def main():
    setup()
    clock = pg.time.Clock()
    
    digits_font = pg.font.SysFont('Comic Sans MS', 30)
    digits = render_digits(digits_font)
    
    mode = Difficulty.easy

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

    tiles = generate_tiles(rows, columns, bombs)
    bombs_found = 0
    

    window_width, window_height = columns*tile_size, rows*tile_size
    g = pg.display.set_mode((window_width, window_height))
    
    # paths = [
    #     "C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\bomb.png", 
    #     "C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\flag.png", 
    #     "C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\no_bomb.png"
    #     ]
    # images = [[pg.image.load(path)] for path in paths]
    
    bomb_image = pg.image.load(r"C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\bomb.png")
    flag_image = pg.image.load(r"C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\flag.png").convert_alpha()
    no_bomb_image = pg.image.load(r"C:\Users\aml05\OneDrive\Documents\GitHub\Games\minesweeper\assets\no_bomb.png")
    
    # scaled_size
    scaled_bomb_image = pg.transform.scale(bomb_image, (tile_size-1,tile_size-1))
    scaled_flag_image = pg.transform.scale(flag_image, (tile_size-1,tile_size-1))
    scaled_no_bomb_image = pg.transform.scale(no_bomb_image, (tile_size,tile_size))

    game_over_font = pg.font.SysFont('Comic Sans MS', 60)
    game_over_rendered = render_game_over(game_over_font, bombs_found, width=window_width, height=window_height)
    
    is_game_over = False
    
    while True:
        g.fill((0,0,0))
        if is_game_over:
            draw_game_over(g, game_over_rendered)
        else:
            draw_grid(**locals()) 
            draw_tiles(g, rows, columns, tile_size, tiles, digits, digits_font, scaled_bomb_image, scaled_flag_image, scaled_no_bomb_image)
            
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONUP:
                mouse = pg.mouse.get_pos() # position
                tile_x, tile_y = convert_pixel_to_tile_coord(tile_size, *mouse)
                # print(tile_x, tile_y, end="    \r")
                tile = tiles[tile_y][tile_x]
                if event.button == 1: # left click
                    reveal_tile(**locals())
                    if tile.is_bomb:
                        is_game_over = True
                elif event.button == 3: # right click
                    if tile.is_flag:
                        tile.is_flag = False
                    else:
                        tile.is_flag = True
            
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    tiles = reset_game(rows, columns, bombs)
                    is_game_over = False
                
            if event.type == QUIT:
                pg.quit()
                return
        
        pg.display.flip()
        clock.tick(60) # controls speed

if __name__ == '__main__':
    main()
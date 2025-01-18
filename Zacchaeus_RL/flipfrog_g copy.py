import math
import os
import pygame as pyg
from typing import Optional, Union
import random as rm
import numpy as np

import gymnasium as gym
from gymnasium import spaces

import random
import time
pass

class FlipFrogGameEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        
        '''self.action_space = spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1., 1.]), dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([-1., -1.]), high=np.array([1., 1.]), dtype=np.float32)
'''
        self.render_mode = render_mode
        #checks to make sure that we are rendering
        if self.render_mode == "human":
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{2000},{20}"
            pyg.init()
            pyg.display.init()
            # pyg.mixer.init()
            # self.noise=pyg.mixer.Sound(r'noises\mouse-click-104737.mp3')
            self.screen = pyg.display.set_mode((600, 800))
        else:
            self.screen = None
        
        self.isopen = True
        self.state = None
        self.steps_beyond_terminated = None
        
        'neccesaries ^'
        'game stuff v'
        self.greenrectangle = pyg.Surface((150,150))
        self.greenrectangle.fill('green')
        self.redrectangle = pyg.Surface((150,150))
        self.redrectangle.fill('red')
        
        self.wrong=False
        self.player_count = 4 #improve this number
        player_list = []
        color_list = ['red', 'green', 'blue', 'pink']
        rm.shuffle(color_list)
        # temp = game_player('red')
        for _ in range(self.player_count):
            player_list.append(self.game_player(color_list[0]))
            del color_list[0]
        # for thisThinkAboutMoreLater in self.player_count:
        #     self.player_list.append('put something here')
        # self.render_stuff = True
        
        # Setup the game's initial state
        draw_pile1 = self.stack_of_tiles(self.tile, self.render_mode)
        self.draw_pile = draw_pile1.tilestack                                              
        self.board = self.game_board(4,4)
        color_list = ['red', 'green', 'blue', 'pink']
        rm.shuffle(color_list)
        self.player_list = []
        for _ in range(self.player_count):
            self.player_list.append(self.game_player(color_list[0]))
            del color_list[0]
        # draw hands
        for game_player in self.player_list:
            # draw 3 tiles
            for _ in range(3):
                game_player.gettile(self.draw_pile)

        player_ai=player_list[0]

        'success'# Fix these to be 19                                                       
        self.action_space = spaces.Box(low=np.array([0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0]), high=np.array([1., 1.,1., 1.,1., 1.,1., 1.,1., 1.,1., 1.,1., 1.,1., 1.,1., 1.,1.]), dtype=np.float32)

        # Fix these to be very long
        self.observation_space = spaces.Box(low=np.array(np.zeros(214)), high=np.array(np.ones(214)), dtype=np.float32)
        self.state = None
        self.terminated = False

        self.steps_beyond_terminated = None

    class tile:
        def __init__(self, color, arrows, snake, graphic_file):
            self._color = color
            self._arrows = arrows
            self._snake = snake
            self._graphic = graphic_file
            
        def _getcolor(self):
            return self._color
        
        def _getarrows(self):
            return self.arrows
        
        def _getsnake(self):
            return self._snake
        
        def _setcolor(self, value):
            self._color=value

        def _setarrows(self, value):
            self._arrows=value

        def _setsnake(self, value):
            self._snake=value

        def _getgraphic(self, value):
            return self._graphic

        def _setgraphic(self, value):
            self._graphic = value

        color = property(
            fget=_getcolor,
            fset=_setcolor,
            # cdel=delcolor
            doc="color thang"
        )
        arrows = property(
            fget=_getarrows,
            fset=_setarrows,
            # adel=delarrows
            doc="arrows thang"
        )

        graphic = property(
            fget=_getgraphic,
            fset=_setgraphic,
            doc="tile graphic file"
        )

        @property
        def snake(self):
            "The snake property."
            return self._snake
        
        @snake.setter
        def snake(self, value):
            self._snake = value

    class game_player:

        def __init__(self, color):
            self.hand = []
            self.color = color

        def gettile(self, tiles):
            if tiles:
                tile = rm.choices(tiles)[0]
                self.hand.append(tile)
                tiles.remove(tile)

        @property
        def color(self):
            "The color property."
            return self._color
        
        @color.setter                                        
        def color(self, value):
            self._color = value

    class game_board:
        def __init__(self, rows, cols):
            self.rows = rows
            self.cols = cols
            game_board_space_dict = {"top": None,
                                    "bottom": None}
            self.gameboard = [[game_board_space_dict.copy() for i in range(self.cols)] for j in range(self.rows)] 

        def update(self, tile, row, col):
            def flip2dict(dictionary,key1,key2):
                dictionary[key1], dictionary[key2] = dictionary[key2], dictionary[key1]
        
            # set top dictionary element to played tile
            # swich top and bottom of appropriate neighbors depending on + or x of played tile    
            # Checks to make sure that played tile is legal 
            if self.gameboard[row][col]["top"] == None and tile._snake != True:
                pass
            elif tile._snake == True:
                print("ha ha you murder person hahahahahaha")
            else:
                return(True)

            self.gameboard[row][col]["top"] = tile
            # snake = tile._snake
            # if snake:
            #     ((self.gameboard[row + 1])[col+1])={"top": None,
            #                                         "bottom":None}
            # self.render()
            arrows = tile._arrows
            
            if arrows == "x":
                #Checks to make sure that the nearby tiles are not offscreen
                if row+1<4 and col+1<4:
                    flip2dict((((self.gameboard[row + 1])[col+1])), "top", "bottom")
                if row-1>=0 and col+1<4:
                    flip2dict((((self.gameboard[row - 1])[col+1])), "top", "bottom")
                if row+1<4 and col-1>=0:
                    flip2dict((((self.gameboard[row + 1])[col-1])), "top", "bottom")
                if row-1>=0 and col-1>=0:
                    flip2dict((((self.gameboard[row - 1])[col-1])), "top", "bottom")
            if arrows == "+":
                #Checks to make sure that the nearby tiles are not offscreen
                if row+1<4:
                    flip2dict((((self.gameboard[row+1])[col])), "top", "bottom")
                if row-1>=0:
                    flip2dict((((self.gameboard[row-1])[col])), "top", "bottom")
                if col+1<4:
                    flip2dict((((self.gameboard[row])[col+1])), "top", "bottom")
                if col-1>=0:
                    flip2dict((((self.gameboard[row])[col-1])), "top", "bottom")
            if arrows == "crap":
                if (((self.gameboard[row])[col])["top"]) == None:
                    if (((self.gameboard[row])[col])["bottom"]) != None:
                        (((self.gameboard[row])[col])["bottom"]) = None
                    else:
                        # print("uhm nah")
                        return()
                else:
                    (((self.gameboard[row])[col])["top"]) = None

            return(False)

    class stack_of_tiles():
        def __init__(self, tile, render_mode: Optional[str] = None):#should render_stuff be here?
            bloop = []
            for _ in range(4):
                if render_mode=="human":
                    red_t = pyg.image.load(r'images\weezard-red.png').convert_alpha()
                    red_t = pyg.transform.scale(red_t, (130,130))
                    bloop.append(tile("red", "+", False, red_t))
                else:
                    bloop.append(tile("red", "+", False, None))
            for _ in range(4):
                if render_mode=="human":
                    red_x = pyg.image.load(r'images\wozard-red.png').convert_alpha()
                    red_x = pyg.transform.scale(red_x, (130,130))
                    bloop.append(tile("red", "x", False, red_x))
                else:
                    bloop.append(tile("red", "x", False, None))
            for _ in range(4):
                if render_mode=="human":
                    blue_t = pyg.image.load(r'images\weezard-blue.png').convert_alpha()
                    blue_t = pyg.transform.scale(blue_t, (130,130))
                    bloop.append(tile("blue", "+", False, blue_t))
                else:
                    bloop.append(tile("blue", "+", False, None))
            for _ in range(4):
                if render_mode=="human":
                    blue_x = pyg.image.load(r'images\wozard-blue.png').convert_alpha()
                    blue_x = pyg.transform.scale(blue_x, (130,130))
                    bloop.append(tile("blue", "x", False, blue_x))
                else:
                    bloop.append(tile("blue", "x", False, None))
            for _ in range(4):
                if render_mode=="human":
                    green_t = pyg.image.load(r'images\weezard-green.png').convert_alpha()
                    green_t = pyg.transform.scale(green_t, (130,130))                              
                    bloop.append(tile("green", "+", False, green_t))
                else:
                    bloop.append(tile("green", "+", False, None))
            for _ in range(4):
                if render_mode=="human":
                    green_x = pyg.image.load(r'images\wozard-green.png').convert_alpha()
                    green_x = pyg.transform.scale(green_x, (130,130))
                    bloop.append(tile("green", "x", False, green_x))
                else:
                    bloop.append(tile("green", "x", False, None))
            for _ in range(4):
                if render_mode=="human":
                    pink_t = pyg.image.load(r'images\weezard-pink.png').convert_alpha()
                    pink_t = pyg.transform.scale(pink_t, (130,130))
                    bloop.append(tile("pink", "+", False, pink_t))
                else:
                    bloop.append(tile("pink", "+", False, None))
            for _ in range(4):
                if render_mode=="human":
                    pink_x = pyg.image.load(r'images\wozard-pink.png').convert_alpha()
                    pink_x = pyg.transform.scale(pink_x, (130,130))
                    bloop.append(tile("pink", "x", False, pink_x))
                else:
                    bloop.append(tile("pink", "x", False, None))
        
            rm.shuffle(bloop)
            self.tilestack=bloop 

    def boardisfullcheck(self):
        boardisfull=True
        for row in range(4):
            for col in range(4):
                if (((self.board.gameboard[row])[col])["top"]) == None:
                    boardisfull=False
                else:
                    pass
        return(boardisfull)

    def flipper(self,played_tile,hidden,x,y):
        row=x
        col=y

        if played_tile._arrows=="x":
            #Checks 
            #⬛⬜⬜
            #⬜🟨⬜                    
            #⬜⬜⬜ Tile and makes sure that it is not offscreen
            if row-1>=0 and col-1>=0:
                if (((self.board.gameboard[row - 1])[col-1])["bottom"]) != None:
                    a1=(((self.board.gameboard[row - 1])[col-1])["bottom"])._graphic
                else:
                    a1=hidden
                if (((self.board.gameboard[row - 1])[col-1])["top"]) != None:
                    b1=(((self.board.gameboard[row - 1])[col-1])["top"])._graphic
                else:
                    b1=hidden
                # a1=(((self.board.gameboard[row + 1])[col+1])["bottom"])._graphic
                # b1=(((self.board.gameboard[row + 1])[col+1])["top"])._graphic
            else:
                a1=None
                b1=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a1==hidden and b1 == hidden:
                a1=None
                b1=None
            #Checks 
            #⬜⬜⬛
            #⬜🟨⬜                    
            #⬜⬜⬜ Tile and makes sure that it is not offscreen
            if row-1>=0 and col+1<4:
                # flip2dict((((self.board.gameboard[row - 1])[col+1])), "top", "bottom")
                if (((self.board.gameboard[row - 1])[col+1])["bottom"]) != None:
                    a2=(((self.board.gameboard[row - 1])[col+1])["bottom"])._graphic
                else:
                    a2=hidden
                if (((self.board.gameboard[row - 1])[col+1])["top"]) != None:
                    b2=(((self.board.gameboard[row - 1])[col+1])["top"])._graphic
                else:
                    b2=hidden
                # a2=(((self.board.gameboard[row - 1])[col+1])["bottom"])._graphic
                # b2=(((self.board.gameboard[row - 1])[col+1])["top"])._graphic
            else:
                a2=None
                b2=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a2==hidden and b2 == hidden:
                a2=None
                b2=None
            #Checks 
            #⬜⬜⬜
            #⬜🟨⬜                    
            #⬛⬜⬜ Tile and makes sure that it is not offscreen
            if row+1<4 and col-1>=0:
                # flip2dict((((self.board.gameboard[row + 1])[col-1])), "top", "bottom")
                if (((self.board.gameboard[row + 1])[col-1])["bottom"]) != None:
                    a3=(((self.board.gameboard[row + 1])[col-1])["bottom"])._graphic
                else:
                    a3=hidden
                if (((self.board.gameboard[row + 1])[col-1])["top"]) != None:
                    b3=(((self.board.gameboard[row + 1])[col-1])["top"])._graphic
                else:
                    b3=hidden
                # a3=(((self.board.gameboard[row + 1])[col-1])["bottom"])._graphic
                # b3=(((self.board.gameboard[row + 1])[col-1])["top"])._graphic
            else:
                a3=None
                b3=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a3==hidden and b3 == hidden:
                a3=None
                b3=None
            #Checks 
            #⬜⬜⬜
            #⬜🟨⬜                    
            #⬜⬜⬛ Tile and makes sure that it is not offscreen
            if row+1<4 and col+1<4:
                # flip2dict((((self.board.gameboard[row - 1])[col-1])), "top", "bottom")
                if (((self.board.gameboard[row + 1])[col+1])["bottom"]) != None:
                    a4=(((self.board.gameboard[row+ 1])[col+1])["bottom"])._graphic
                else:
                    a4=hidden
                if (((self.board.gameboard[row + 1])[col+1])["top"]) != None:
                    b4=(((self.board.gameboard[row + 1])[col+1])["top"])._graphic
                else:
                    b4=hidden
                # a4=(((self.board.gameboard[row - 1])[col-1])["bottom"])._graphic
                # b4=(((self.board.gameboard[row - 1])[col-1])["top"])._graphic
            else:
                a4=None
                b4=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a4==hidden and b4 == hidden:
                a4=None
                b4=None
            row=x-1
            col=y-1
            self.flipx(a1,b1,a2,b2,a3,b3,a4,b4,row,col)

        else:
            #Checks 
            #⬜⬛⬜
            #⬜🟨⬜                    
            #⬜⬜⬜ Tile and makes sure that it is not offscreen
            row_check = row - 1
            column_check = col
            if row_check>=0:
                # flip2dict((((self.board.gameboard[row + 1])[col+1])), "top", "bottom")
                # a1=(((self.board.gameboard[row + 1])[col])["bottom"])._graphic
                if (((self.board.gameboard[row_check])[column_check])["bottom"]) != None:
                    a1=(((self.board.gameboard[row_check])[column_check])["bottom"])._graphic
                else:
                    a1=hidden
                if (((self.board.gameboard[row_check])[column_check])["top"]) != None:
                    b1=(((self.board.gameboard[row_check])[column_check])["top"])._graphic
                else:
                    b1=hidden
            else:
                a1=None
                b1=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a1==hidden and b1 == hidden:
                a1=None
                b1=None
            #Checks 
            #⬜⬜⬜
            #⬛🟨⬜                    
            #⬜⬜⬜ Tile and makes sure that it is not offscreen
            if col-1>=0:
                # flip2dict((((self.board.gameboard[row - 1])[col+1])), "top", "bottom")
                if (((self.board.gameboard[row])[col-1])["bottom"]) != None:
                    a2=(((self.board.gameboard[row])[col-1])["bottom"])._graphic
                else:
                    a2=hidden
                if (((self.board.gameboard[row])[col-1])["top"]) != None:
                    b2=(((self.board.gameboard[row])[col-1])["top"])._graphic
                else:
                    b2=hidden
                # a2=(((self.board.gameboard[row - 1])[col])["bottom"])._graphic
                # b2=(((self.board.gameboard[row - 1])[col])["top"])._graphic
            else:
                a2=None
                b2=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a2==hidden and b2 == hidden:
                a2=None
                b2=None
            #Checks 
            #⬜⬜⬜ 
            #⬜🟨⬛                   
            #⬜⬜⬜ Tile and makes sure that it is not offscreen
            if col+1<4:
                if (((self.board.gameboard[row])[col+1])["bottom"]) != None:
                    a3=(((self.board.gameboard[row])[col+1])["bottom"])._graphic
                else:
                    a3=hidden
                if (((self.board.gameboard[row])[col+1])["top"]) != None:
                    b3=(((self.board.gameboard[row])[col+1])["top"])._graphic
                else:
                    b3=hidden
                # # flip2dict((((self.board.gameboard[row + 1])[col-1])), "top", "bottom")
                # a3=(((self.board.gameboard[row])[col+1])["bottom"])._graphic
                # b3=(((self.board.gameboard[row])[col+1])["top"])._graphic
            else:
                a3=None
                b3=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a3==hidden and b3 == hidden:
                a3=None
                b3=None
            #Checks 
            #⬜⬜⬜
            #⬜🟨⬜                    
            #⬜⬛⬜ Tile and makes sure that it is not offscreen
            if row+1<4:
                if (((self.board.gameboard[row+1])[col])["bottom"]) != None:
                    a4=(((self.board.gameboard[row+1])[col])["bottom"])._graphic
                else:
                    a4=hidden
                if (((self.board.gameboard[row+1])[col])["top"]) != None:
                    b4=(((self.board.gameboard[row+1])[col])["top"])._graphic
                else:
                    b4=hidden
            else:
                a4=None
                b4=None
            #if both the top and bottom of the tile (the tile told above this comment) are empty, it will make them both
            #hidden, but thats not correct, so we turn them both to none.
            if a4==hidden and b4 == hidden:
                a4=None
                b4=None
            row=x-1
            col=y-1

            self.flipt(a1,b1,a2,b2,a3,b3,a4,b4,row,col)

    def enemy_turn(self, player_random):

        # Choose a tile to play
        tile = (self.player_list[player_random]).hand[0]

        # Remove chosen tile from hand
        del((self.player_list[player_random]).hand[0])

        # Draw a new tile
        self.player_list[player_random].gettile(self.draw_pile)

        run = True
        while run:    
            # Choose a random location to play
            x=rm.randint(0,3)
            y=rm.randint(0,3)

            # Check to see if location is valid
            retry=self.board.update(tile,x,y)

            # if retry is true, need to check that board is not full, then try to place in different spot
            if retry:
                boardisfull=self.boardisfullcheck()
                if boardisfull:
                    run=False
            else:
                run=False
                # print('enemy location = ', x, y)

        boardisfull=self.boardisfullcheck()

        return(boardisfull,x,y,tile)
    
    def render(self,x2,y2,blitthing): 
        grid = pyg.image.load(r'images\grid-png-43560.png').convert_alpha()
        grid = pyg.transform.scale(grid, (600,600))
        hidden = pyg.image.load(r'images\hidden.png').convert_alpha()
        hidden = pyg.transform.scale(hidden, (130,130))
        self.screen.fill((217,217,217))
        self.screen.blit(grid,(0,0))
        if blitthing!=None:
            self.screen.blit(blitthing,(x2*150, y2*150))
        pixel_loc_list = [10, 160, 310, 460]
        for x_loc in pixel_loc_list:
            for y_loc in pixel_loc_list:
                x=int((x_loc-10)/150)
                y=int((y_loc-10)/150)
                # darnit = 0
                # grumpy = 0

                #checks to make sure that a spot on the board is not none before it blits it
                if self.board.gameboard[y][x]["bottom"] != None:
                    self.screen.blit(hidden,(y_loc, x_loc))
                    # screen.blit(grid,(x, y))
                if (self.board.gameboard[y][x]["top"]) != None:
                    self.screen.blit(self.board.gameboard[y][x]["top"]._graphic,(y_loc, x_loc))

    def state_make(self):
        indexer = 0
        for torb in ["top", 'bottom']:
            for x in range(4):
                for y in range(4):
                    #makes the state by cheking hte boarrd
                    if (self.board.gameboard[x][y][torb]) != None:
                        if (self.board.gameboard[x][y][torb])._color == "red":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                        if (self.board.gameboard[x][y][torb])._color == "green":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                        if (self.board.gameboard[x][y][torb])._color == "blue":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                        if (self.board.gameboard[x][y][torb])._color == "pink":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                        if (self.board.gameboard[x][y][torb])._arrows == "+":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                        if (self.board.gameboard[x][y][torb])._arrows == "x":
                            self.state[indexer]=1
                        else:
                            self.state[indexer]=0
                        indexer += 1
                    else:
                        indexer+=6

        player_ = self.player_list[0]

        for tile in player_.hand:
            if tile._color == "red":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1
            if tile._color == "green":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1
            if tile._color == "blue":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1
            if tile._color == "pink":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1
            if tile._arrows == "+":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1
            if tile._arrows == "x":
                self.state[indexer]=1
            else:
                self.state[indexer]=0
            indexer += 1

        if player_.color == "red":
            self.state[indexer]=1
        else:
            self.state[indexer]=0
        indexer += 1
        if player_.color == "green":
            self.state[indexer]=1
        else:
            self.state[indexer]=0
        indexer += 1
        if player_.color == "blue":
            self.state[indexer]=1
        else:
            self.state[indexer]=0
        indexer += 1
        if player_.color == "pink":
            self.state[indexer]=1
        else:
            self.state[indexer]=0
    
    def flipx(self,greenrectangle, redrectangle,greenrectangle2, redrectangle2,greenrectangle3, redrectangle3,greenrectangle4, redrectangle4,boardx,boardy):
        # ONLY NECCESARY ONCE v
        x=1
        flip=False
        # greenrectangle = pyg.image.load(r'images\weezard-red.png').convert_alpha()
        # redrectangle = pyg.image.load(r'images\weezard-blue.png').convert_alpha()
        # rectangle = pyg.transform.scale(greenrectangle, ((130-(x*2),130)))
        clock = pyg.time.Clock()
        jflip=None
        rectangle=greenrectangle
        rectangle2=greenrectangle2
        rectangle3=greenrectangle3
        rectangle4=greenrectangle4
        flip2=True
        green=True
        while True:
            for event in pyg.event.get():
                if event.type==pyg.QUIT:
                    pyg.display.quit()
                    pyg.quit()
                    exit()
            if x==65:
                jflip=True
                if flip2==False:
                    flip2=True
                elif flip2==True:
                    flip2=False

            if x==0:
                # if flip2==False:
                #     flip2=True
                # elif flip2==True:
                #     flip2=False
                break
            if jflip!=None:
                if jflip:
                    if green:
                        green=False
                    else:
                        green=True
            # self.screen.fill((217,217,217))
            #ONLY NECCESSARY ONCE ^
            if rectangle != None:
                self.screen.blit(rectangle,(x+10+(boardx*150), 10+(boardy*150)))
            if rectangle2 != None:
                self.screen.blit(rectangle2,(x+310+(boardx*150), 10+(boardy*150)))
            if rectangle3 != None:
                self.screen.blit(rectangle3,(x+10+(boardx*150), 310+(boardy*150)))
            if rectangle4 != None:
                self.screen.blit(rectangle4,(x+310+(boardx*150), 310+(boardy*150)))
            
            pyg.display.update()
            if green:
                if rectangle != None:
                    rectangle = pyg.transform.scale(greenrectangle, ((130-(x*2),130)))
                if rectangle2 != None:
                    rectangle2 = pyg.transform.scale(greenrectangle2, ((130-(x*2),130)))
                if rectangle3 != None:
                    rectangle3 = pyg.transform.scale(greenrectangle3, ((130-(x*2),130)))
                if rectangle4 != None:
                    rectangle4 = pyg.transform.scale(greenrectangle4, ((130-(x*2),130)))
                if flip2==False:
                    x-=1
                if flip2==True:
                    x+=1

            else:
                if rectangle != None:
                    rectangle = pyg.transform.scale(redrectangle, ((130-(x*2),130)))
                if rectangle2 != None:
                    rectangle2 = pyg.transform.scale(redrectangle2, ((130-(x*2),130)))
                if rectangle3 != None:
                    rectangle3 = pyg.transform.scale(redrectangle3, ((130-(x*2),130)))
                if rectangle4 != None:
                    rectangle4 = pyg.transform.scale(redrectangle4, ((130-(x*2),130)))
                if flip2==False:
                    x-=1
                else:
                    x+=1
            jflip=False
            clock.tick(60)

    def flipt(self,greenrectangle, redrectangle,greenrectangle2, redrectangle2,greenrectangle3, redrectangle3,greenrectangle4, redrectangle4,boardx,boardy):
        # ONLY NECCESARY ONCE v
        x=1
        flip=False
        # greenrectangle = pyg.image.load(r'images\weezard-red.png').convert_alpha()
        # redrectangle = pyg.image.load(r'images\weezard-blue.png').convert_alpha()
        
        clock = pyg.time.Clock()
        jflip=None
        rectangle=greenrectangle
        rectangle2=greenrectangle2
        rectangle3=greenrectangle3
        rectangle4=greenrectangle4
        flip2=True
        green=True
        while True:
            for event in pyg.event.get():
                if event.type==pyg.QUIT:
                    pyg.display.quit()
                    pyg.quit()
                    exit()
            if x==65:
                jflip=True
                if flip2==False:
                    flip2=True
                elif flip2==True:
                    flip2=False

            if x==0:
                # if flip2==False:
                #     flip2=True
                # elif flip2==True:
                #     flip2=False
                break
            if jflip!=None:
                if jflip:
                    if green:
                        green=False
                    else:
                        green=True
            # self.screen.fill((217,217,217))
            #ONLY NECCESSARY ONCE ^
            if rectangle != None:
                self.screen.blit(rectangle,(x+160+(boardx*150), 10+(boardy*150)))
            if rectangle2 != None:
                self.screen.blit(rectangle2,(x+10+(boardx*150), 160+(boardy*150)))
            if rectangle3 != None:
                self.screen.blit(rectangle3,(x+310+(boardx*150), 160+(boardy*150)))
            if rectangle4 != None:
                self.screen.blit(rectangle4,(x+160+(boardx*150), 310+(boardy*150)))
            
            pyg.display.update()
            if green:
                if rectangle != None:
                    rectangle = pyg.transform.scale(greenrectangle, ((130-(x*2),130)))
                if rectangle2 != None:
                    rectangle2 = pyg.transform.scale(greenrectangle2, ((130-(x*2),130)))
                if rectangle3 != None:
                    rectangle3 = pyg.transform.scale(greenrectangle3, ((130-(x*2),130)))
                if rectangle4 != None:
                    rectangle4 = pyg.transform.scale(greenrectangle4, ((130-(x*2),130)))
                if flip2==False:
                    x-=1
                if flip2==True:
                    x+=1
 
            else:
                if rectangle != None:
                    rectangle = pyg.transform.scale(redrectangle, ((130-(x*2),130)))
                if rectangle2 != None:
                    rectangle2 = pyg.transform.scale(redrectangle2, ((130-(x*2),130)))
                if rectangle3 != None:
                    rectangle3 = pyg.transform.scale(redrectangle3, ((130-(x*2),130)))
                if rectangle4 != None:
                    rectangle4 = pyg.transform.scale(redrectangle4, ((130-(x*2),130)))
                if flip2==False:
                    x-=1
                else:
                    x+=1
            jflip=False
            clock.tick(60)

    def step(self, action):

        # Decode action, assume each element of action is in [0, 1]
        # Give input to bot about their hand, ask them what tile they'll play
        #self.action_space = spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1., 1.]), dtype=np.float32)
        listofyourhand = [action[0],action[1],action[2]]
        indexofyourhand=listofyourhand.index(max(listofyourhand))
        'success'#Z, get max value of first 3 elements of action =  [.2, .4, .6, 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]

        player_ai = self.player_list[0]

        if player_ai.hand!=[]:

            if indexofyourhand+1>len(player_ai.hand): #has issues make sure check BIGISSUE
                self.wrong=True
            if not self.wrong:
                tile=player_ai.hand[indexofyourhand] #make it so that the game knows that it is actually a specific players turn because otherwise well yeah
        
        else:
            self.terminated = True

        # ask bot where they want to play it
        chosentilelist = []  # SuccessZ, get max value of last 16 elements of action =  [.2, .4, .6, 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
        for values in range(16):
            chosentilelist.append(action[values+3]) # ok wait what
        indexofthelocation = chosentilelist.index(max(chosentilelist))

        'Success'# Turn the tile spot chosen into x and y values
        y = int(np.floor(indexofthelocation/4))
        x = np.mod(indexofthelocation,4)

        reward = 0

        # if playerturn>self.player_count:
        #     playerturn=1
        player_=self.player_list
        # tile = player_.hand[select-1]
        # print("indexofhand: ",indexofyourhand)
        # print(len(player_ai.hand))
        hidden = pyg.image.load(r'images\hidden.png').convert_alpha()
        hidden = pyg.transform.scale(hidden, (130,130))
        if indexofyourhand+1>len(player_ai.hand): #has issues make sure check BIGISSUE
            self.wrong=True

        if player_ai.hand!=[]:
            if self.wrong==False:
                played_tile = player_ai.hand[indexofyourhand]
                del(player_ai.hand[indexofyourhand])
                if not self.wrong:
                    # Update the board with the AI player's action
                    self.wrong=self.board.update(tile, x, y)
                        
                    # Render the AI player's action
                    if self.render_mode == 'human':
                        self.flipper(played_tile,hidden,x,y)

                        self.render(x,y,self.greenrectangle)

                        pyg.display.update()
                        pyg.event.pump()
            else:
               self.terminated = True
        else:
            self.terminated = True
        # self.noise.play()        

        if not self.wrong:
            if self.draw_pile!=[]:
                player_ai.gettile(self.draw_pile)
            else:
                self.terminated = True

        # print(len(self.draw_pile),' tiles left')

        boardisfull=self.boardisfullcheck() #to check if the board is full

        '''Enemy turns'''
        if boardisfull==False:
            for enemyindex in [1,2,3]:
                self.terminated,x,y,played_tile=self.enemy_turn(enemyindex)
                # print(len(self.draw_pile),' tiles left')
                row=x-1
                col=y-1
                
                if self.render_mode == 'human':
                    self.flipper(played_tile,hidden,x,y)
                    # if played_tile._arrows=="x":
                    #     if row+1<4 and col+1<4:
                    #         # flip2dict((((self.board.gameboard[row + 1])[col+1])), "top", "bottom")
                    #         if (((self.board.gameboard[row + 1])[col+1])["bottom"]) != None:
                    #             a1=(((self.board.gameboard[row + 1])[col+1])["bottom"])._graphic
                    #         else:
                    #             a1=hidden
                    #         if (((self.board.gameboard[row + 1])[col+1])["top"]) != None:
                    #             b1=(((self.board.gameboard[row + 1])[col+1])["top"])._graphic
                    #         else:
                    #             b1=hidden
                    #         # a1=(((self.board.gameboard[row + 1])[col+1])["bottom"])._graphic
                    #         # b1=(((self.board.gameboard[row + 1])[col+1])["top"])._graphic
                    #     else:
                    #         a1=None
                    #         b1=None
                    #     if row-1>=0 and col+1<4:
                    #         # flip2dict((((self.board.gameboard[row - 1])[col+1])), "top", "bottom")
                    #         if (((self.board.gameboard[row - 1])[col+1])["bottom"]) != None:
                    #             a2=(((self.board.gameboard[row - 1])[col+1])["bottom"])._graphic
                    #         else:
                    #             a2=hidden
                    #         if (((self.board.gameboard[row - 1])[col+1])["top"]) != None:
                    #             b2=(((self.board.gameboard[row - 1])[col+1])["top"])._graphic
                    #         else:
                    #             b2=hidden
                    #         # a2=(((self.board.gameboard[row - 1])[col+1])["bottom"])._graphic
                    #         # b2=(((self.board.gameboard[row - 1])[col+1])["top"])._graphic
                    #     else:
                    #         a2=None
                    #         b2=None
                    #     if row+1<4 and col-1>=0:
                    #         # flip2dict((((self.board.gameboard[row + 1])[col-1])), "top", "bottom")
                    #         if (((self.board.gameboard[row + 1])[col-1])["bottom"]) != None:
                    #             a3=(((self.board.gameboard[row + 1])[col-1])["bottom"])._graphic
                    #         else:
                    #             a3=hidden
                    #         if (((self.board.gameboard[row + 1])[col-1])["top"]) != None:
                    #             b3=(((self.board.gameboard[row + 1])[col-1])["top"])._graphic
                    #         else:
                    #             b3=hidden
                    #         # a3=(((self.board.gameboard[row + 1])[col-1])["bottom"])._graphic
                    #         # b3=(((self.board.gameboard[row + 1])[col-1])["top"])._graphic
                    #     else:
                    #         a3=None
                    #         b3=None
                    #     if row-1>=0 and col-1>=0:
                    #         # flip2dict((((self.board.gameboard[row - 1])[col-1])), "top", "bottom")
                    #         if (((self.board.gameboard[row - 1])[col-1])["bottom"]) != None:
                    #             a4=(((self.board.gameboard[row- 1])[col-1])["bottom"])._graphic
                    #         else:
                    #             a4=hidden
                    #         if (((self.board.gameboard[row - 1])[col-1])["top"]) != None:
                    #             b4=(((self.board.gameboard[row - 1])[col-1])["top"])._graphic
                    #         else:
                    #             b4=hidden
                    #         # a4=(((self.board.gameboard[row - 1])[col-1])["bottom"])._graphic
                    #         # b4=(((self.board.gameboard[row - 1])[col-1])["top"])._graphic
                    #     else:
                    #         a4=None
                    #         b4=None
                    #     self.flipx(a1,b1,a2,b2,a3,b3,a4,b4,col,row)

                    # else:
                        # if row+1<4:
                        #     # flip2dict((((self.board.gameboard[row + 1])[col+1])), "top", "bottom")
                        #     # a1=(((self.board.gameboard[row + 1])[col])["bottom"])._graphic
                        #     if (((self.board.gameboard[row + 1])[col])["bottom"]) != None:
                        #         a1=(((self.board.gameboard[row + 1])[col])["bottom"])._graphic
                        #     else:
                        #         a1=hidden
                        #     if (((self.board.gameboard[row + 1])[col])["top"]) != None:
                        #         b1=(((self.board.gameboard[row + 1])[col])["top"])._graphic
                        #     else:
                        #         b1=hidden
                        # else:
                        #     a1=None
                        #     b1=None
                        # if row-1>=0:
                        #     # flip2dict((((self.board.gameboard[row - 1])[col+1])), "top", "bottom")
                        #     if (((self.board.gameboard[row - 1])[col])["bottom"]) != None:
                        #         a2=(((self.board.gameboard[row - 1])[col])["bottom"])._graphic
                        #     else:
                        #         a2=hidden
                        #     if (((self.board.gameboard[row - 1])[col])["top"]) != None:
                        #         b2=(((self.board.gameboard[row - 1])[col])["top"])._graphic
                        #     else:
                        #         b2=hidden
                        #     # a2=(((self.board.gameboard[row - 1])[col])["bottom"])._graphic
                        #     # b2=(((self.board.gameboard[row - 1])[col])["top"])._graphic
                        # else:
                        #     a2=None
                        #     b2=None
                        # if col+1<4:
                        #     if (((self.board.gameboard[row])[col+1])["bottom"]) != None:
                        #         a3=(((self.board.gameboard[row])[col+1])["bottom"])._graphic
                        #     else:
                        #         a3=hidden
                        #     if (((self.board.gameboard[row])[col+1])["top"]) != None:
                        #         b3=(((self.board.gameboard[row])[col+1])["top"])._graphic
                        #     else:
                        #         b3=hidden
                        #     # # flip2dict((((self.board.gameboard[row + 1])[col-1])), "top", "bottom")
                        #     # a3=(((self.board.gameboard[row])[col+1])["bottom"])._graphic
                        #     # b3=(((self.board.gameboard[row])[col+1])["top"])._graphic
                        # else:
                        #     a3=None
                        #     b3=None
                        # if col-1>=0:
                        #     if (((self.board.gameboard[row])[col-1])["bottom"]) != None:
                        #         a4=(((self.board.gameboard[row])[col-1])["bottom"])._graphic
                        #     else:
                        #         a4=hidden
                        #     if (((self.board.gameboard[row])[col-1])["top"]) != None:
                        #         b4=(((self.board.gameboard[row])[col-1])["top"])._graphic
                        #     else:
                        #         b4=hidden
                        #     # flip2dict((((self.board.gameboard[row - 1])[col-1])), "top", "bottom")
                        #     # a4=(((self.board.gameboard[row])[col-1])["bottom"])._graphic
                        #     # b4=(((self.board.gameboard[row])[col-1])["top"])._graphic
                        # else:
                        #     a4=None
                        #     b4=None
                        # self.flipt(a1,b1,a2,b2,a3,b3,a4,b4,col,row)
                    pyg.time.delay(1000)
                    # self.noise.play()
                    self.render(x,y,self.redrectangle)
                    pyg.display.update()
                    pyg.event.pump()

                if self.terminated:
                    break
                # check board
        reward = 0

        '''reward each turn for surviving(+2)
        give extra reward at end based on how many of its tiles are on the board'''
        if self.wrong==False:
            reward+=2
        else:
            self.terminated = True

        boardisfull=self.boardisfullcheck() # we need 2 boardisfull checks before and after the enemy turns because we need to tell whether or not to do an enemy turn and wi also need to know boardisfull after enemy turns
        if boardisfull: # Removed the need for self.terminated, it seemed to be causing issues
            for row in range(4):
                for col in range(4):
                    if (((self.board.gameboard[row])[col])["top"])._color == self.player_list[0].color:
                        reward +=2

        self.state_make() # Creates the state for the beggining of the next turn
        
        
        return np.array(self.state, dtype=np.float32), reward, self.terminated, False, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.

        self.steps_beyond_terminated = None

        # Clear game state classes to be reinitialized
        del self.board

        if self.render_mode=="human":
            del self.screen
            os.environ['SDL_VIDEO_WINDOW_POS'] = f"{2000},{20}"
            pyg.quit
            pyg.init()
            pyg.display.init()
            # pyg.mixer.init()
            # self.noise=pyg.mixer.Sound(r'noises\mouse-click-104737.mp3')
            self.screen = pyg.display.set_mode((600, 800))
            pyg.display.update()
            pyg.event.pump()
            
        # Setup the game's initial state
        self.render_stuff = True
        draw_pile1 = self.stack_of_tiles(self.tile, self.render_mode)
        self.draw_pile = draw_pile1.tilestack
        self.board = self.game_board(4,4)
        color_list = ['red', 'green', 'blue', 'pink']
        rm.shuffle(color_list)
        self.player_list = []
        for _ in range(self.player_count):
            self.player_list.append(self.game_player(color_list[0]))
            del color_list[0]
        for _ in range(3):
            for player_ in self.player_list:
                player_.gettile(self.draw_pile)
        self.state = None
        self.state = np.array(np.zeros(214))
        self.state_make()
        self.terminated = False
        self.wrong=False

        return np.array(self.state, dtype=np.float32), {}
        
    def close(self):
        pyg.display.quit()
        pyg.QUIT
        self.isopen = False
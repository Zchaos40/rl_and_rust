import math
import pygame as pyg
from typing import Optional, Union

import numpy as np

import gymnasium as gym
from gymnasium import spaces
import random as rm


class ZGameEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        pyg.init
        pyg.font.init()

        self.skyx = 0
        self.nightx = 1670
        self.y = 140
        self.yvel = 0
        self.obs1x = rm.randint(400,1580)
        self.obs2x = rm.randint(1580, 3160)
        self.font = pyg.font.Font(None, 34)
        self.scorer_int = 0
        self.score_number_str = "0"
        self.score = self.font.render(self.score_number_str, False, 'red')
        self.sonic = pyg.Suraface((110, 180))
        self.sonic.fill('red')
        self.sonic_rect = self.sonic.get_rect(topleft = (20, self.y))
        self.sky = pyg.image.load('sky.png').convert_alpha()
        self.sky = pyg.transform.scale(self.sky, (1670,400))
        self.nightsky = pyg.image.load('nightsky.png').convert_alpha()
        self.nightsky = pyg.transform.scale(self.nightsky , (1670,400))
        self.floor = pyg.image.load('Dark-grey.png').convert_alpha()
        self.floor = pyg.transform.scale(self.floor, (1670,100))
        self.obs1 = pyg.Surface((20,20))
        self.obs1.fill('green')
        self.obs1_rect = self.obs1.get_rect(topleft = (self.obs1x, 280))
        self.obs2 = pyg.Surface((20,20))
        self.obs2.fill('green')
        self.obs2_rect = self.obs2.get_rect(topleft = (self.obs2x, 280))
        self.game_tics = 0


        # self.action_space = spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1., 1.]), dtype=np.float32)
        # self.observation_space = spaces.Box(low=np.array([-1., -1.]), high=np.array([1., 1.]), dtype=np.float32)

        self.render_mode = render_mode

        if self.render_mode == "human":
            self.screen = pyg.display.set_mode((1670, 400))
        else:
            self.screen = None
        self.isopen = True
        self.state = None

        self.steps_beyond_terminated = None

    def step(self, action):
        
        reward = 0
        # if kb.is_pressed(' ') and yvel==0:
        #     yvel = -2.5

        # if y == 40:
        #     yvel = 2.5

        # if y > 120:
        #     y = 120

        # if y == 120 and yvel == 2.5:
        #     yvel = 0

        self.y+=self.yvel

        self.skyx-=4
        self.nightx-=4
        self.obs1x-=4
        self.obs2x-=4

        if self.skyx <= -1670:
            self.skyx = 1670
            self.scorer_int += 1
            self.obs1x = rm.randint(1580, 3160)
        if self.nightx <= -1670:
            self.obs2x = rm.randint(1580, 3160)
            self.scorer_int += 1
            self.nightx = 1670
            
        self.sonic_rect.y = self.y  
        self.obs1_rect.x = self.obs1x
        self.obs2_rect.x = self.obs2x

        self.score_number_str = str(self.scorer_int)


        # if skyx <= -3160:
        #     obs1x = rm.randint(1580, 3160)

        # if nightx <= -3160:
        #     obs2x = rm.randint(1580, 3160)

        self.score = self.font.render(self.score_number_str, False, 'red')



        self.game_tics += 1

        '''work on reward and action space soon!'''


        reward+=0.01
        if self.sonic_rect.colliderect(self.obs1_rect) or self.sonic_rect.colliderect(self.obs2_rect):
            reward-=3 

        '''IMPORTANT! get a working self.state.'''
        # self.state = (np.sign(x_distance), np.sign(y_distance))



        '''Change terminated soon'''
        terminated = bool(self.game_tics > 1000)

        if self.render_mode == "human":
            self.render()

        return np.array(self.state, dtype=np.float32), reward, terminated, False, {}

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.
        '''Get reset soon!!!'''

        # self.state = (np.sign(x_distance), np.sign(y_distance))

        # self.steps_beyond_terminated = None

        if self.render_mode == "human":
            self.render()
        return np.array(self.state, dtype=np.float32), {}

    '''Update render soon!'''
    def render(self):

        pyg.display.update()

    def close(self):
        pyg.display.quit()
        pyg.QUIT
        self.isopen = False
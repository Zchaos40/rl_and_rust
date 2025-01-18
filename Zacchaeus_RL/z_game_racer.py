import math
import pygame as pyg
from typing import Optional, Union

import numpy as np

import gymnasium as gym
from gymnasium import spaces
import random as rm


class RacerEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        pyg.init
        pyg.font.init()
        pyg.display.init()

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
        self.sonic = pyg.Surface((110, 180))
        self.sonic.fill('red')
        self.sonic_rect = self.sonic.get_rect(topleft = (20, self.y))
        self.sky = pyg.image.load('E:/Zacchaeus_Python/sky.png')
        self.sky = pyg.transform.scale(self.sky, (1670,400))
        self.nightsky = pyg.image.load('E:/Zacchaeus_Python/nightsky.png')
        self.nightsky = pyg.transform.scale(self.nightsky , (1670,400))
        self.floor = pyg.image.load('E:/Zacchaeus_Python/Dark-grey.png')
        self.floor = pyg.transform.scale(self.floor, (1670,100))
        self.obs1 = pyg.Surface((20,20))
        self.obs1.fill('green')
        self.obs1_rect = self.obs1.get_rect(topleft = (self.obs1x, 280))
        self.obs2 = pyg.Surface((20,20))
        self.obs2.fill('green')
        self.obs2_rect = self.obs2.get_rect(topleft = (self.obs2x, 280))
        self.game_tics = 0


        self.action_space = spaces.Box(low=np.array([0.]), high=np.array([1.]), dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([0.]), high=np.array([1.]), dtype=np.float32)

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


        if self.skyx <= -3160:
            self.obs1x = rm.randint(1580, 3160)

        if self.nightx <= -3160:
            self.obs2x = rm.randint(1580, 3160)

        self.score = self.font.render(self.score_number_str, False, 'red')



        self.game_tics += 1

        '''work on action space soon!'''#########

        if action >= 0.63 and self.yvel == 0:
            self.yvel = -2.5        
            
        if self.y == 40:
            self.yvel = 2.5

        if self.y > 120:
            self.y = 120

        if self.y == 120 and self. yvel == 2.5:
            self.yvel = 0

        reward+=0.0075
        if self.sonic_rect.colliderect(self.obs1_rect) or self.sonic_rect.colliderect(self.obs2_rect):
            reward-=3
            self.game_tics = 1500
            # print')

        '''IMPORTANT! get a working self.state.'''
        # self.state = (np.sign(x_distance), np.sign(y_distance))
        self.state = (self.get_obs(),)

        print(self.game_tics)

        '''Change terminated soon'''
        terminated = bool(self.game_tics >= 1500)

        if self.render_mode == "human":
            self.render()


        return np.array(self.state, dtype=np.float32), reward, terminated, False, {}

    def get_obs(self):

        dist1 = self.obs1_rect.x - self.sonic_rect.x
        dist2 = self.obs2_rect.x - self.sonic_rect.x

        if dist1 > dist2 and dist2 >0:
            minfrontobs = dist2
        else:
            minfrontobs = dist1

        if minfrontobs > 500:
            minfrontobs = 500
        
        if minfrontobs < 0:
            minfrontobs = 0.01

        obs = minfrontobs / 505

        return obs

    def reset(
        self,
        *,
        seed: Optional[int] = None,
        options: Optional[dict] = None,
    ):
        super().reset(seed=seed)
        # Note that if you use custom reset bounds, it may lead to out-of-bound
        # state/observations.
        #b '''Get reset soon!!!'''
        self.skyx = 0
        self.nightx = 1670
        self.y = 140
        self.yvel = 0
        self.obs1x = rm.randint(400,1580)
        self.obs2x = rm.randint(1580, 3160)
        self.font = pyg.font.Font(None, 34)
        self.scorer_int = 0
        self.score_number_str = "0"
        self.game_tics = 0

        self.state = np.array([.9])

        self.steps_beyond_terminated = None

        if self.render_mode == "human":
            self.render()
        return np.array(self.state, dtype=np.float32), {}

    '''Update render soon!'''
    def render(self):
        self.screen.blit(self.sky, (self.skyx, 0))
        self.screen.blit(self.nightsky, (self.nightx, 0))
        self.screen.blit(self.sonic, self.sonic_rect)
        self.screen.blit(self.obs1, self.obs1_rect)
        self.screen.blit(self.obs2, self.obs2_rect)

        pyg.display.update()

    def close(self):
        pyg.display.quit()
        pyg.QUIT
        self.isopen = False
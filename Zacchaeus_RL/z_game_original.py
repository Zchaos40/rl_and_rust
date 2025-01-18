import math
import pygame as pyg
from typing import Optional, Union

import numpy as np

import gymnasium as gym
from gymnasium import spaces
import random


class ZGameEnv(gym.Env[np.ndarray, Union[int, np.ndarray]]):

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 50,
    }

    def __init__(self, render_mode: Optional[str] = None):
        pyg.init
        pyg.font.init()

        self.x = 300
        self.y = 200
        self.a = 150
        self.x1 = 400
        self.y1 = 200
        self.score = 0
        self.game_tics = 0
        self.rat_timer = 50
        self.clock = pyg.time.Clock()
        self.sonic = pyg.image.load('E:/Zacchaeus_RL/mom_present_graphics/Zifna_Face.png')
        self.sonic = pyg.transform.scale(self.sonic, (100,100))
        self.sky = pyg.image.load('E:/Zacchaeus_RL/mom_present_graphics/sky.png')
        self.sky = pyg.transform.scale(self.sky, (800,400))
        self.rat = pyg.image.load('E:/Zacchaeus_RL/mom_present_graphics/ratty.png')
        self.rat = pyg.transform.scale(self.rat, (100,100))
        self.font = pyg.font.Font(None, 50)
        self.speed = 5
        self.turning_rate = 0.4
        self.direction = 0
        self.scorer = self.font.render('score: ', False, 'red')
        self.sonic_r = self.sonic.get_rect(topleft = (self.x,self.y))
        self.rat_r = self.rat.get_rect(center=(self.x1-50,self.y1-50))
        # self.rat_r = self.rat_r.inflate(-40,-40)

        self.action_space = spaces.Box(low=np.array([-1.0, -1.0]), high=np.array([1., 1.]), dtype=np.float32)
        self.observation_space = spaces.Box(low=np.array([-1., -1.]), high=np.array([1., 1.]), dtype=np.float32)

        self.render_mode = render_mode

        if self.render_mode == "human":
            self.screen = pyg.display.set_mode((800, 400))
        else:
            self.screen = None
        self.isopen = True
        self.state = None

        self.steps_beyond_terminated = None

    def step(self, action):

        reward = 0

        self.game_tics += 1

        x_distance = self.rat_r.x - self.sonic_r.x
        y_distance = self.rat_r.y - self.sonic_r.y

        if self.a >= self.rat_timer:
            self.x1=random.randint(30,700)
            self.y1=random.randint(30, 330)
            self.a=0
            self.rat_r.x = self.x1-50
            self.rat_r.y = self.y1-50
        if action[0] > 0.1:
            self.x+=4
        if action[0] < -0.1:
            self.x-=4
        if action[1] > 0.1:
            self.y+=4
        if action[1] < -0.1:
            self.y-=4
        if self.sonic_r.colliderect(self.rat_r) and self.a<2:
            self.a=self.rat_timer
        if self.sonic_r.colliderect(self.rat_r) and self.a!=self.rat_timer:
            self.a=self.rat_timer
            reward += 1
            self.score+=1

        if self.x > 800:
            self.x = 800
        if self.x < 0:
            self.x = 0
        if self.y > 400:
            self.y = 400
        if self.y < 0:
            self.y = 0

        self.a+=1

        self.sonic_r.x = self.x
        self.sonic_r.y = self.y

        x_distance_new = self.rat_r.x - self.sonic_r.x
        y_distance_new = self.rat_r.y - self.sonic_r.y

        self.state = (np.sign(x_distance), np.sign(y_distance))

        # Rat has just jumped locations, so no penalty or reward this step
        if self.a != 1:
            reward += 0.00005*(np.abs(x_distance - x_distance_new)*np.abs(y_distance - y_distance_new))


        terminated = bool(self.game_tics > 1000)

        if self.render_mode == "human":
            self.render()

        # print(self.x, self.y, self.rat_r.x, self.rat_r.y)

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
        self.x = 300
        self.y = 200
        self.a = 150
        self.x1 = 42
        self.y1 = 234
        self.score = 0
        self.game_tics = 0

        x_distance = self.rat_r.x - self.sonic_r.x
        y_distance = self.rat_r.y - self.sonic_r.y

        self.state = (np.sign(x_distance), np.sign(y_distance))

        self.steps_beyond_terminated = None

        if self.render_mode == "human":
            self.render()
        return np.array(self.state, dtype=np.float32), {}

    def render(self):

        scorey=str(self.score)
        scorer=self.font.render('score: '+scorey, False, 'red')
        
        self.screen.blit(self.sky,(0,0))   
        self.screen.blit(self.sonic,self.sonic_r)
        self.screen.blit(self.rat,self.rat_r)
        self.screen.blit(scorer,(200,30))

        pyg.display.update()

    def close(self):
        pyg.display.quit()
        pyg.QUIT
        self.isopen = False

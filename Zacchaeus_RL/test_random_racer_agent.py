from ray.tune.registry import register_env
from z_game_racer import RacerEnv
import time


def env_creator(env_config):
    return RacerEnv(env_config)

register_env("RacerEnv", env_creator)


env = RacerEnv(render_mode='human')

# returns an initial observation
env.reset()

for i in range(1000):

    env.render()
    #env.action_space.sample() produces either 0 (left) or 1 (right).
    observation, reward, done, trunk_dump, info = env.step(env.action_space.sample())
    print(observation)
    time.sleep(0.0075)

env.close()
from ray.tune.registry import register_env
from z_game_original import ZGameEnv


def env_creator(env_config):
    return ZGameEnv(env_config)

register_env("ZGameEnv", env_creator)


env = ZGameEnv(render_mode='human')

# returns an initial observation
env.reset()

for i in range(1000):

    env.render()
    #env.action_space.sample() produces either 0 (left) or 1 (right).
    observation, reward, done, trunk_dump, info = env.step(env.action_space.sample())

env.close()
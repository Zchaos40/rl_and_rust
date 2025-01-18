import gymnasium as gym
from ray.tune.registry import register_env
from flipfrogstuff.flipfrog_g import FlipFrogGameEnv
import ray
from ray.rllib.algorithms.sac import SAC
from ray.rllib.algorithms import Algorithm
import time

def env_creator(env_config):
    return FlipFrogGameEnv(env_config)

register_env("FlipFrogGameEnv", env_creator)

reloaded_agent = Algorithm.from_checkpoint(r'c:\Users\Leonardo\ray_results\SAC\SAC_FlipFrogGameEnv_0146a_00000_0_2024-07-16_15-57-25\checkpoint_050500')

env = FlipFrogGameEnv(render_mode='human')
done = False
total_reward = 0
observations = env.reset()
observations = observations[0]
print(env.player_list[0].color)
while not done:
    action = reloaded_agent.compute_single_action(observations)
    observations, reward, done, trunk_dump, info = env.step(action)
    total_reward += reward
    print(total_reward)
    print(env.player_list[0].color)

print(f"total reward = {total_reward}")

env.close() 
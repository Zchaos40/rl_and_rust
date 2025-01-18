import gymnasium as gym
from ray.tune.registry import register_env
from z_game_racer import RacerEnv
import ray
from ray.rllib.algorithms.ppo import PPO
from ray.rllib.algorithms import Algorithm
import time

def env_creator(env_config):
    return RacerEnv(env_config)

register_env("RacerEnv", env_creator)

reloaded_agent = Algorithm.from_checkpoint(r'C:\Users\Leonardo\ray_results\PPO\PPO_RacerEnv_77cfe_00000_0_2023-07-23_09-44-46\checkpoint_003450')

env = RacerEnv(render_mode='human')
done = False
total_reward = 0
observations = env.reset()
observations = observations[0]
while not done:
    time.sleep(0.0176)
    action = reloaded_agent.compute_single_action(observations)
    observations, reward, done, trunk_dump, info = env.step(action)
    total_reward += reward

print(f"total reward = {total_reward}")

env.close()
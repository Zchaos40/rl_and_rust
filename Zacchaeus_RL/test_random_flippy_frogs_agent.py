from ray.tune.registry import register_env
from flipfrogstuff.flipfrog_g import FlipFrogGameEnv


def env_creator(env_config):
    return FlipFrogGameEnv(env_config)

register_env("FlipFrogGameEnv", env_creator)

env = FlipFrogGameEnv(render_mode='human')

# returns an initial observation
env.reset()
total_reward = 0
for i in range(1000):

    # env.render()
    #env.action_space.sample() produces either 0 (left) or 1 (right).ws
    observation, reward, done, trunk_dump, info = env.step(env.action_space.sample())
    total_reward += reward
    if env.terminated:
        print("total reward = ", total_reward)

        env.reset()
        total_reward = 0
        for i in range(1000):
            observation, reward, done, trunk_dump, info = env.step(env.action_space.sample())
            total_reward += reward
            print(total_reward)
            if env.terminated:  
                print("total reward = ", total_reward)

                break
        
        break

env.close()
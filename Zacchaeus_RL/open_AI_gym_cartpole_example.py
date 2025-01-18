import gymnasium as gym

env = gym.make("CartPole-v1", render_mode='human')
# env = gym.make("CartPole-v1")


# returns an initial observation
env.reset()

for i in range(100):

    env.render()
    #env.action_space.sample() produces either 0 (left) or 1 (right).
    observation, reward, done, trunk_dump, info = env.step(env.action_space.sample())

# env.close()

import ray
from ray.rllib.algorithms.ppo import PPO

config = {
    "env": "CartPole-v1",
    "framework": "torch",
    "model": {
      "fcnet_hiddens": [32],
      "fcnet_activation": "linear",
    },
}
stop = {"episode_reward_mean": 300}
ray.shutdown()
ray.init(
  num_cpus=3,
  include_dashboard=False,
  ignore_reinit_error=True,
  log_to_driver=False,
)
# execute training 
analysis = ray.tune.run(
  "PPO",
  config=config,
  stop=stop,
  checkpoint_at_end=True,
)


trial = analysis.get_best_logdir("episode_reward_mean", "max")
checkpoint = analysis.get_best_checkpoint(
  trial,
  "training_iteration",
  "max",
)
trainer = PPO(config=config)
trainer.restore(checkpoint)

observation = env.reset()
observation = observation[0]
done = False
while not done:
  env.render()
  action = trainer.compute_single_action(observation)
  observation, reward, done, trunk_dump, info = env.step(action)
env.close()
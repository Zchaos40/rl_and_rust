import ray
from ray.rllib.algorithms.ppo import PPO

# restore a trainer from the last checkpoint

config = {
    "env": "CartPole-v1",
    "framework": "torch",
    "model": {
      "fcnet_hiddens": [32],
      "fcnet_activation": "linear",
    },
    "restore": ""
}

checkpoint = analysis.get_best_checkpoint(
  trial,
  "training_iteration",
  "max",
)
trainer = PPOTrainer(config=config)
trainer.restore(checkpoint)

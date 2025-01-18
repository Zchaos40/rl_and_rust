from ray.tune.registry import register_env
from z_game import ZGameEnv
import ray

def env_creator(env_config):
    return ZGameEnv(env_config)

register_env("ZGameEnv", env_creator)

env = ZGameEnv()

config = {
    "env": "ZGameEnv",
    "framework": "torch",
    "model": {
      "fcnet_hiddens": [32],
      "fcnet_activation": "tanh",
    },
}
stop = {"training_iteration": 10000}
ray.shutdown()
ray.init(
  num_cpus=3,
  num_gpus=1,
  include_dashboard=False,
  ignore_reinit_error=True,
  log_to_driver=False,
)
# execute training 
analysis = ray.tune.run(
  "PPO",
  config=config,
  stop=stop,
  checkpoint_freq=10,
  keep_checkpoints_num = 3,
  checkpoint_at_end=True,
)

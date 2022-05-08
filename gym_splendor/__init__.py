from gym.envs.registration import register

register(
    id='gym_splendor-v0',    
    entry_point='gym_splendor.envs:SplendporEnv',
)
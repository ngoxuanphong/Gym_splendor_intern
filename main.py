
from unicodedata import name
import gym
import gym_splendor
import pandas as pd
import time
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    start_time = time.time()
    while env.turn <1000:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
        env.render()
        # print(env.player[env.turn%env.amount_player])
        if done == True:
            break
    for i in range(4):
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(state = env.state))
    state = env.state
    print(check_winner(state))
    print(time.time()-start_time)
if __name__ == '__main__':
    main()


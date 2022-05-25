import gym
import gym_splendor
import pandas as pd
import time
import warnings
from collections import Counter

warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    start_time = time.time()
    while env.turn < 1000:
        o, a, done, t = env.step(env.player[env.turn % env.amount_player].action(state=env.state))
        # env.render()
        if done == True:
            break
    for i in range(4):
        o, a, done, t = env.step(env.player[env.turn % env.amount_player].action(state=env.state))
        state = env.state
    print(env.turn, env.pVictory.name, env.pVictory.score)
    return env.pVictory.name


#     if __name__ == '__main__':
#         main()
print(Counter(main() for i in range(1000)))
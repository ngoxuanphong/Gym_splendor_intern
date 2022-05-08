import gym
import gym_splendor
import os
import pandas as pd
def main():
    env = gym.make('gym_splendor-v0')
    env.reset()
    while env.turn <150:
        o,a,done,t = env.step(env.player[env.turn%env.amount_player].action(env.state))
        env.render()
        if done == True:
            break

if __name__ == '__main__':
    main()


import gym

import gym
import Azul_game
from gym import spaces
import RandomAzulPlayer
import numpy as np

import random
import numpy as np


class Pygame2D():

    def __init__(self):
        self.game = Azul_game.Azul_game()
        self.opponent_turn = "P2"
        self.opponent = RandomAzulPlayer("P2")
        #self.opponent_turn = "P2"

        self.boh = "P1"

        #  pit_choice, tile_type, column_choice
        self.action_pit_choice = -1
        self.action_tile_type = -1
        self.action_column_choice = -1

    def traduci_azione(self,action):

        #traduce l'azione da 180 a 6,6,5
        self.action_pit_choice = action % 6
        self.action_tile_type = int(action / 6 % 6)
        self.action_column_choice = int(((action / 6) % 5))

    def action(self, action):
        self.traduci_azione(action)
        self.game.play_turn(self.boh, self.action_pit_choice, self.action_tile_type, self.action_column_choice)


    def is_done(self):
        return self.game.gameover

    def observe(self):

        if(self.game.is_turn_done()):
            self.game.create_drawing_pit()

        while self.game.player_turn != self.boh:
            #richiama l'azione del opponent
            self.opponent.set_board(self.game)
            self.opponent.random_action(self)

        #self.game.p1_score
        obs = []
        for elem in self.game.rows_p1:
            obs = obs + elem
        for elem in self.game.penalty_row_p1:
            obs = obs + elem
        for row in self.game.board_p1:
            for elem in row:
                obs = obs +elem
        for pit in self.game.drawing_pit:
            for elem in pit:
                obs = obs + elem

        #obs = 0
        return obs

    def evaluete(self):
        if self.game.valid_move(self.boh, self.action_pit_choice, self.action_tile_type, self.action_column_choice):
            return 1
        else:
            return -1


    def view(self):
        return self.game.print_table()

class CustomEnv(gym.Env):
    def __init__(self):
        self.pygame = Pygame2D()
        self.action_space = spaces.Discrete(180)

        rows_player_obs = [5] * 15
        penality_player_obs = [1] * 7
        board_player_obs = [1] * 25
        normal_pit_obs = [4] * 5
        #al massimo ci possono essere 3*5 tessere nel discard pit per una singola tessera
        discard_pit_obs = [3*5] * 5
        one_player_obs = rows_player_obs + penality_player_obs + board_player_obs + \
                         normal_pit_obs + discard_pit_obs

        self.observation_space = spaces.MultiDiscrete(one_player_obs)

    def reset(self):
        del self.pygame
        self.pygame = Pygame2D()
        obs = self.pygame.observe()
        return obs

    def step(self, action):
        self.pygame.action(action)
        obs = self.pygame.observe()
        reward = self.pygame.evaluete()
        done = self.pygame.is_done()

        return obs,reward,done,{}

    def render(self, mode='human'):
        print(self.pygame.view())

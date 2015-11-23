# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "12:44, Nov. 21th, 2015"
"""This is library for HappyPosion.
This library is responisble for generating game board in the format of a two-dimensional list and also works as a judge in a way similar to the observable pattern."""

import random
from HP.Agents.HappyAgent import *
from HP.Agents.PoisonAgent import *

class GameBoard():
  """ This class manages the whole game board, and, meanwhile, coordinate each agents on the board.
  All the parameter row and col are calculated from top to bottom and left to right, and are calculated from 0."""

  # Sign in the board list
  GOLD_SIGN = 2
  OBSTACLE_SIGN = 1
  EMPTY_SIGN = 0
  # Flag for game state
  GAME_RUNNING = 0
  HAPPY_WIN = 1
  POISON_WIN = -1

  def __init__(self, game_width, game_height, happy_agents, poison_agents, num_gold):
    """Init Function of this class whose responsiblity is to generate the game board and put agents on them.
    :param game_width: the size of game board's width.
    :type game_width: integer.
    :param game_height: the size of game board's height.
    :type game_height: integer.
    :param happy_agents: the list of happy agents.
    :type happy_agents: list.
    :param poison_agents: the list of poison agents.
    :type poison_agents: list.
    :param num_gold: the number of treasures.
    :type num_gold: integer.
    """
    # Check legality
    num_happy = len(happy_agents)
    num_poison = len(poison_agents)
    self.legal_check(game_width, game_height, num_happy, num_poison, num_gold)
    
    # Initialize Game Information variables
    self.game_width = game_width
    self.game_height = game_height
    self.game_state = self.GAME_RUNNING

    # Initialize the bord list
    self.board = self._initialize_board()
    self.gold_list = list()
    self.obstacle_list = list()
    self.happy_agents_list = list()
    self.poison_agents_list = list()
    
    # Prepare putting objects on the board
    board_occupy = [[0 for i in range(self.game_height)], [0 for i in range(self.game_width)]]
    candidate_row = [i for i in range(self.game_height)]
    candidate_col = [i for i in range(self.game_width)]
    
    # Put Happy on the board
    middle_row = self.game_height//2 + 1
    middle_col = self.game_width//2 +1
    self.set_object_position(middle_row, middle_col, happy_agents[0])
    board_occupy[0][middle_row] = 1 # No Need to check. It is the first object on the board whose minimum size is 2x2
    board_occupy[1][middle_col] = 1
    # Put the first happy on the middle of the board
    # Put the others randomly
    for i in range(1, num_happy):
      row = random.choice(candidate_row)
      col = random.choice(candidate_col)
      board_occupy[0][row] += 1
      if board_occupy[0][row] == self.game_height:
        candidate_row.remove(row)
      if board_occupy[1][col] == self.game_width:
        candidate_col.remove(col)
      self.set_object_position(row, col, happy_agents[i])

    # Put Gold on the board Randomly
    for i in range(num_gold):
      row = random.choice(candidate_row)
      col = random.choice(candidate_col)
      board_occupy[0][row] += 1
      if board_occupy[0][row] == self.game_height:
        candidate_row.remove(row)
      if board_occupy[1][col] == self.game_width:
        candidate_col.remove(col)
      self.set_object_position(row, col, self.GOLD_SIGN)

    # Put Poison on the board Randomly 
    for i in range(num_poison):
      row = random.choice(candidate_row)
      col = random.choice(candidate_col)
      board_occupy[0][row] += 1
      if board_occupy[0][row] == self.game_height:
        candidate_row.remove(row)
      if board_occupy[1][col] == self.game_width:
        candidate_col.remove(col)
      self.set_object_position(row, col, poison_agents[i])

    # Put obstacles on the board Randomly if possible
    for i in range(int((self.game_width+self.game_height)/5)):
      if (not candidate_row) or (not candidate_col):
        break
      row = random.choice(candidate_row)
      col = random.choice(candidate_col)
      board_occupy[0][row] += 1
      if board_occupy[0][row] == self.game_height:
        candidate_row.remove(row)
      if board_occupy[1][col] == self.game_width:
        candidate_col.remove(col)
      self.set_object_position(row, col, self.OBSTACLE_SIGN)

  def game_result(self):
    """Return 1 if Happy wins, -1 if Poison wins, 0 otherwise."""
    return self.game_state

  def game_over(self, who_win):
    """ Adjust Game Information and Notify Agents when game over.
    :param who_win: who win
    :type who_win: one of GameBoard.HAPPY_WIN or GameBoard.POISON_WIN"""
    if who_win == self.HAPPY_WIN:
      for i in self.happy_agents_list:
        self.get_obj_from_board(i[0], i[1]).win()
      for i in self.poison_agents_list:
        self.get_obj_from_board(i[0], i[1]).fail()
      print('Happy finds out all treasure chests.\nCongratulations to Happy!')
    else:
      for i in self.poison_agents_list:
        self.get_obj_from_board(i[0], i[1]).win()
      for i in self.happy_agents_list:
        self.get_obj_from_board(i[0], i[1]).fail()
      print('Happy has no chance to happy any more!')
    self.game_state = who_win

  def get_board(self):
    """ Return the board in the format of a two-dimensional list.
    Use list here because we need to identify each happy agent and each poison agent."""
    return self.board

  def get_happy_agents_positions(self):
    """ Return a list composed by tuples each of which is a happy agent's position in wich the first entry is row and the second entry is col."""
    return self.happy_agents_list

  def get_poison_agents_positions(self):
    """ Return a list composed by tuples each of which is a happy agent's position in wich the first entry is row and the second entry is col."""
    return self.poison_agents_list

  def get_obstacles_positions(self):
    """ Return a list composed by tuples each of which is a obstacle's position in wich the first entry is row and the second entry is col."""
    return self.obstacle_list

  def get_golds_positions(self):
    """ Return a list composed by tuples each of which is a treasure's position in wich the first entry is row and the second entry is col."""
    return self.gold_list

  def _initialize_board(self):
    """ Initialize the game board.
    Use list here because we need to identify each happy agent and each poison agent."""
    return [ [self.EMPTY_SIGN for i in range(self.game_width)] for j in range(self.game_height) ]

  def _is_a_board_object(self, obj):
    """ Return True if the input argument obj is a self.XXXX_SIGN"""
    if obj == self.OBSTACLE_SIGN or obj == self.GOLD_SIGN or obj == self.EMPTY_SIGN:
      return True
    return False
    
  def can_set_position(self, row, col, obj):
    """ Return True if the given coordinate is not occupied by other objects.
    Rules: (1) Occupied square cannot be put at, except that a agent tries to occupy the square of another agent whose type is different.
    (2) A square will be cleared up if an EMPTY_SIGN is put at."""
    if row<0 or col<0 or row >= self.game_height or col >= self.game_width:
      return False
    if isinstance(obj, HappyAgent) or isinstance(obj, PoisonAgent):
      now_pos = obj.get_position()
      if now_pos == (row, col):
        # It is not allowed to stay at a same square
        return False
      else:
        if ((abs(now_pos[0] - row) == 1 and now_pos[1] == col) \
        or (abs(now_pos[1] - col) == 1 and now_pos[0] == row)):
          tar_obj = self.get_obj_from_board(row, col)
          if tar_obj != None and ( \
          tar_obj == self.EMPTY_SIGN \
          or (isinstance(obj, HappyAgent) and tar_obj == self.GOLD_SIGN)\
          or (isinstance(obj, HappyAgent) and isinstance(tar_obj, PoisonAgent)) \
          or (isinstance(obj, PoisonAgent) and isinstance(tar_obj, HappyAgent))):
            return True
        return False
    elif self._is_a_board_object(obj):
      if self.get_obj_from_board(row, col) == self.EMPTY_SIGN:
        return True
      return False
    return False
      
  def set_object_position(self, row, col, obj):
    """Put an object on the board. Use self.can_set_position() beforehand.
    Rules: A HappyAgent will be killed if it be put at a squared occupied by a PoisonAgent or if a PoisonAgent is put at a squared by the HappyAgent.
    :param row: the row id, from top to bottom, the most top row is 0.
    :type row: integer.
    :param col: the col id, from left to right, the most left col is 0.
    :type col: integer.
    :param obj: the object needed to be put on the board.
    :type obj: HappyAgent, PoisonAgent or self.XXXX_SIGN"""
    tar_obj = self.get_obj_from_board(row, col)
    murder = False
    harvest = False
    if isinstance(obj, HappyAgent):
      if isinstance(tar_obj, PoisonAgent):
        murder = True
        killer = tar_obj
        dead = obj
        obj.is_killed_by(tar_obj)
      else:
        if tar_obj == self.GOLD_SIGN:
          self.gold_list.remove((row, col))
          harvest = True
          obj.harvest(self.GOLD_SIGN, self)
        obj_pos = obj.get_position()
        if isinstance(obj_pos, tuple):
          self.board[obj_pos[0]][obj_pos[1]] = self.EMPTY_SIGN
          self.happy_agents_list.remove(obj_pos)
          self.show_walking_info(obj, (row, col))
        obj.set_position(row, col)
        self.happy_agents_list.append((row, col))
        self.board[row][col] = obj
    elif isinstance(obj, PoisonAgent):
      if isinstance(tar_obj, HappyAgent):
        murder = True
        killer = obj
        dead = tar_obj
        obj.kills(tar_obj)
      obj_pos = obj.get_position()
      if isinstance(obj_pos, tuple):
        self.board[obj_pos[0]][obj_pos[1]] = self.EMPTY_SIGN
        self.poison_agents_list.remove(obj_pos)
        self.show_walking_info(obj, (row, col))
      obj.set_position(row, col)
      self.poison_agents_list.append((row, col))
      self.board[row][col] = obj
    elif obj == self.GOLD_SIGN:
      self.gold_list.append((row, col))
      self.board[row][col] = obj
    elif obj == self.OBSTACLE_SIGN:
      self.obstacle_list.append((row, col))
      self.board[row][col] = obj
    elif obj == self.EMPTY_SIGN:
      self.board[row][col] = obj
    if murder == True:
      # Clear corpse
      self.happy_agents_list.remove(dead.get_position())
      self.show_murder_info(killer, dead)
      # Check if all Happyagents are killed
      if not self.happy_agents_list:
        # Poison wins
        self.game_over(self.POISON_WIN)
    elif harvest == True:
      self.show_harvest_info(obj)
      # Check if all treasures are obtained already
      if not self.gold_list:
        # Happy wins
        self.game_over(self.HAPPY_WIN)
  
  def get_obj_from_board(self, row, col):
    """ Return the object or SIGN at the given coordinate on the board.
    :param row: the row id.
    :type row: integer.
    :param col: the col id.
    :type col: integer"""
    if row < self.game_height and col < self.game_width and row >= 0 and col>=0:
      return self.board[row][col]
    
  def draw_board(self):
    """ This function will print board to terminal"""
    print('')
    print('╔' + '═'*self.game_width + '╗')
    for i in range(self.game_height):
      output = '║'
      for j in range(self.game_width):
        obj = self.get_obj_from_board(i, j)
        if isinstance(obj, HappyAgent):
          output += '\033[92m@\033[0m'
        elif isinstance(obj, PoisonAgent):
          output += '\033[91m∞\033[0m'
        elif obj == self.EMPTY_SIGN:
          output += '·'
        elif obj == self.GOLD_SIGN:
          output += '\033[93m$\033[0m'
        elif obj == self.OBSTACLE_SIGN:
          output += '\033[96m×\033[0m'
      print(output + '║')
    print('╚' + '═'*self.game_width + '╝')
    print('\033[92m@\033[0m: Happy')
    print('\033[91m∞\033[0m: Poison')
    print('\033[93m$\033[0m: Treasure')
    print('\033[96m×\033[0m: Obstacle')
    print('')

  def show_walking_info(self, obj, from_here):
    if isinstance(obj, PoisonAgent):
      color = '\033[91m'
    else:
      color = '\033[92m'
    print(color + obj.agent_name() + '\033[0m walks from ' + str(obj.get_position()) +' to ' + str(from_here)+'.')

  def show_harvest_info(self, obj):
    print('\033[92m' + obj.agent_name() + '\033[0m picks up a \033[93m$treasure chest$\033[0m at ' + str(obj.get_position()))

  def show_murder_info(self, killer_agent, victim_agent):
    print('\033[91m'+killer_agent.agent_name()+'\033[0m kills \033[92m'+victim_agent.agent_name()+'\033[0m at ' + str(killer_agent.get_position()))

  @staticmethod
  def legal_check(game_width, game_height, num_happy, num_poison, num_gold):
    """ Check if a set of game configure is legal.
    :param game_width: the size of game board's width.
    :type game_width: integer.
    :param game_height: the size of game board's height.
    :type game_height: integer.
    :param num_happy: the number of happy agents.
    :type num_happy: integer.
    :param num_poison: the number of poison agents.
    :type num_poison: integer.
    :param num_gold: the number of treasures.
    :type num_gold: integer.
    """
    game_width = int(game_width)
    game_height = int(game_height)
    num_happy = int(num_happy)
    num_poison = int(num_poison)
    num_gold = int(num_gold)
    if game_width < 2:
      raise GameBoardException('Invaild Game Borad Width', 1)
    if game_height < 2:
      raise GameBoardException('Invaild Game Borad Height', 2)
    if num_happy < 1:
      raise GameBoardException('At Least ONE Happy Is Needed', 3)
    if num_gold < 1:
      raise GameBoardException('At Least ONE Treasure Is Needed', 4)
    if game_width*game_height - num_happy - num_gold - num_poison < 0:
      raise GameBoardException('Game Size is Too Small or Objects are too many', 5)

class GameBoardException(Exception):
  def __init__(self, message, err_code):
    super(GameBoardException, self).__init__(message)
    self.message = message
    self.err_code = err_code


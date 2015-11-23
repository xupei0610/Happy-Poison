# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "02:39, Nov. 21th, 2015"
"""This is the abstract class for all game agent classes in this project."""

from abc import ABCMeta, abstractmethod

class Agent():
  """An Abstract Class defining the basic function and interface for all game agent classes in this project."""
  __metaclass__ = ABCMeta
  
  INF = 10000000   # Used for alpha-beta
  NINF = -10000000
  MIN = -1 # Poison is Min
  MAX = 1  # Happy is MAX

  def __init__(self):
    self.position = None
    self.has_failed = False
    self.has_won = False
    self.goal = None # For Poison, it should be an instance of HappyAgent; For Happy, it should be a coordinate of gold in the format of tuple composed of row id and col id.

  @abstractmethod
  def agent_name(self):
    """ Every Agent should have a unique name. It should be very cool."""
    pass

  @abstractmethod
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    Every agent should make a move unless it cannot move.
    Each move only can help the agent work a step along up, down, left or right.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if self.if_fail() or self.if_win() or self.is_killed():
        return False
    return True

  @abstractmethod
  def is_killed_by(self, killer_agent):
    """The agent is killed by another agent."""
    pass

  @abstractmethod
  def is_killed(self):
    """Return true if the agent has died."""
    pass

  @abstractmethod
  def who_kills_me(self, victim_agent):
    """Return None if the agent is still alive, or the killer agent."""
    pass

  @abstractmethod
  def kills(self, victim_agent):
    """The agent kills another agent."""
    pass

  @abstractmethod
  def deadlist(self):
    """Return a list composed of the agents who are killed by the current agent."""
    pass

  @abstractmethod
  def harvest(self, something):
    """ Give some rewards to the agent, if it harvests something."""
    pass

  def win(self):
    """Tell the agent you win. Win.....LOL.....LOL. """
    self.has_won = True
  
  def if_win(self):
    """Return True if the agent has won."""
    return self.has_won

  def fail(self):
    """Tell the agent you fail. Oh~~~~~ NOOOOOOOOOOO."""
    self.has_failed = True
  
  def if_fail(self):
    """Return True if the agent has failed."""
    return self.has_failed
  
  def get_position(self):
    """Return a tuple composed by the coordinate of the agent, the first is row and the second is col. 0,0 is the most top and left square."""
    return self.position

  @abstractmethod
  def set_position(self, row, col):
    """Set the agent's coordinate. 0, 0 is the most top and left square."""
    self.position = (row, col)
  
  def distance(self, board, from_here, to_there, depth):
    """ Return the distance between two point. The nature of this function is A* search with limited depth
    :param from_here: a point coordinate. The first entry is row id, the second is col id.
    :type from_here: tuple.
    :param to_there: another point coordinate. The first entry is row id, the second is col id.
    :type to_there: tuple.
    :param depth: search depth, the bigger the more accurate
    :type depth: integer."""
    # A* Manhattan Distance
    frontier = [(abs(from_here[0]-to_there[0])+abs(from_here[1]-to_there[1]), from_here)]
    return frontier[0][0]
    candidates = []
    for i in range(depth):
      if not frontier:
        break
      frontier.sort(key=lambda x:x[0], reverse=False)
      c_pos = frontier.pop(0)[1]
      for c in ((c_pos[0]+i[0], c_pos[1]+i[1]) for i in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        if board.get_obj_from_board(c[0], c[1]) == board.EMPTY_SIGN:
          h_val = abs(c[0]-to_there[0]) + abs(c[1]-to_there[1])
          if h_val == 0:
            return i
          if i == depth-1:
            candidates.append(h_val+i)
          else:
            frontier.append((h_val+i, c))
    if candidates:
      return sorted(candidates)[0]
    else:
      return None # unreachable at least in the limited depth

  def set_goal(self, obj):
    """ Goal is used for evaluation function"""
    self.goal = obj

  def get_goal(self):
    """ Return the current agent's goal"""
    return self.goal

  def eval_func(self, aimed_coordinate, board, min_or_max, depth):
    """ Evaluating the game if the current agent moves to the aimed_coordinate.
    Strategy: (1) Set A Goal for the current agent.
    (2) Guess the goal's goal
    (3) Obtain 3 distances. d1 is between the agent and its goal, d2 is between the goal and the goal's goal, and d3 is between the goal's goal and the agent.
    Poison's goal should be Happy. Happy's goal should be gold. Gold's goal here means a poison agent who is most close to the happy agent who is most close to the gold.
    Then:
    evaluation = (board_width + board_height - d1) * 10 + d3 *5 + d2.
    :param aimed_coordinate: the intended coordinate
    :type aimed_coordinate: tuple. The first entry is row id, the second is col id.
    :param board: GameBoard.
    :type board: GameBoard.
    :param min_or_max: min for Poison, max for Happy.
    :type min_or_max: Agent.MAX or Agent.MIN"""
    if min_or_max == self.MAX:
      d1 = self.distance(board, aimed_coordinate, self.get_goal(), depth)
      dis = self.INF
      tar = None
      for i in board.poison_agents_list:
        res = self.distance(board, self.get_goal(), i, depth)
        if res and res < dis:
          dis = res
          tar = i
      if tar:
        d2 = dis
        d3 = self.distance(board, aimed_coordinate, tar, depth)
        if d3:
          c = board.game_width + board.game_height
          return (c-d1)*10 + (c-d3)*6 + c - d2
      return self.INF
    else: 
      d1 = self.distance(board, aimed_coordinate, self.get_goal().get_position(), self.IQ)
      dis = self.INF
      tar = None
      for i in board.gold_list:
        res = self.distance(board, self.get_goal().get_position(), i, depth)
        if res and res < dis:
          dis = res
          tar = i
      if tar:
        d2 = dis
        d3 = self.distance(board, aimed_coordinate, tar, depth)
        if d3:
          c = board.game_width + board.game_height
          return d1
      return self.NINF

  def alpha_beta(self, board, coordinate, depth, min_or_max, _alpha=None, _beta=None, _max_depth=None):
    """ Alpha-Beta Pruning.
    Return the evaluated value for the given coordinate.
    :param board: GameBoard.
    :type board: GameBoard.
    :param coordinate: the coordinate needed to be evaluated.
    :type coordinate: tuple. the first entry is row id and the second entry is col id.
    :param depth: search depth.
    :type depth: integer.
    :param _alpha, _beta, _max_depth: for recursive."""
    if depth == 0:
      return self.eval_func(coordinate, board, min_or_max, _max_depth)

    if _alpha==None:
      _alpha = self.NINF
      _beta = self.INF
      _max_depth = depth

    if min_or_max == self.MAX:
      v = self.NINF
      no_child = True
      cut_off = False
      for i in ((coordinate[0]+j[0], coordinate[1]+j[1]) for j in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        if board.can_set_position(i[0], i[1], self):
          no_child = False
          v = max(v, alpha_beta(board, i, depth-1, min_or_max, _alpha, _beta, _max_depth))
          _alpha = max(_alpha, v)
          if _beta <= _alpha:
            cut_off = True
            break
      if cut_off:
        return v
      if no_child:
        return self.eval_func(coordinate, board, min_or_max, _max_depth) 
    else:
      v = self.INF
      no_child = True
      cut_off = False
      for i in ((coordinate[0]+j[0], coordinate[1]+j[1]) for j in ((1, 0), (-1, 0), (0, 1), (0, -1))):
        if board.can_set_position(i[0], i[1], self):
          v = min(v, alpha_beta(board, i, depth-1, min_or_max, _alpha, _beta, _max_depth))
          _beta = min(_beta, v)
          if _beta <= _alpha:
            cut_off = True
            break
      if no_child:
        return self.eval_func(coordinate, board, min_or_max, _max_depth)
      if cut_off:
        return v





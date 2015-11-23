# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "02:59, Nov. 21th, 2015"
"""This is the implement of a smart poison agent whose action is decided via
min-max algorithm with alpha-beta pruning."""

from HP.Agents.PoisonAgent import *

class PoisonIntel(PoisonAgent):
  """This is an implement for a poison agent whose action pattern is decides via min-max algorithm with alpha-beta pruning."""

  def __init__(self):
    super(PoisonIntel, self).__init__()
    self.IQ = 2

  def agent_name(self):
    """ Return the current agent's name."""
    if not self.my_name:
      self.my_name = super(PoisonIntel, self).agent_name() + 'S'
    return self.my_name
  
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    Return None if there is not any possible path.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if not super(PoisonIntel, self).want_move(board):
      return None

    distances = list()
    for i in range(len(board.happy_agents_list)):
      dis = self.distance(board, self.get_position(), board.happy_agents_list[i], self.IQ)
      if dis == None:
        dis = self.INF
      distances.append((i, dis))
    distances = sorted(distances, key=lambda x: x[1], reverse = False)

    need_to_set_a_goal = True
    if isinstance(self.goal, HappyAgent) and self.goal.is_killed() == False:
      if i < 2:
        rang = range(i+1)
      else:
        rang = range(3)
      for j in rang:
        if board.get_obj_from_board(distances[j][0], distances[j][1]) == self.goal:
          need_to_set_a_goal = False
    if need_to_set_a_goal == True:
      # Need a new goal
      self.set_goal(board.get_obj_from_board(board.happy_agents_list[distances[0][0]][0], board.happy_agents_list[distances[0][0]][1]))

    coordinate = self.get_position()
    cand_coord = ((coordinate[0]+i[0], coordinate[1]+i[1]) for i in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    min_val = self.INF
    candidates = list()
    for i in cand_coord:
      if board.can_set_position(i[0], i[1], self) == False:
        continue
      res = self.alpha_beta(board, i, self.IQ, self.MIN)
      if res < min_val:
        candidates = [i]
        min_val = res
      elif res == min_val:
        candidates.append(i)
    if len(candidates) > 1:
      dis = self.INF
      min_coord = None
      for i in candidates:
        res = self.distance(board, i, self.goal.get_position(), self.IQ)
        if not res:
          res = self.INF/2
        if res < dis:
          dis = res
          min_coord = i
    else:
      min_coord = candidates[0]
    return min_coord



# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "03:02, Nov. 21th, 2015"
"""This is the implement of a computer happy player agent."""

from HP.Agents.HappyAgent import *

class HappyCompu(HappyAgent):
  """This is an implement for a happy agent whose action pattern is decides via min-max algorithm with alpha-beta pruning."""

  def __init__(self):
    super(HappyCompu, self).__init__()
    self.IQ = 5

  def agent_name(self):
    """ Return the current agent's name."""
    if not self.my_name:
      self.my_name = super(HappyCompu, self).agent_name() + 'C'
    return self.my_name
  
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    Return None if there is not any possible path.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if not super(HappyCompu, self).want_move(board):
      return None
    
    distances = list()
    for i in range(len(board.gold_list)):
      dis = self.distance(board, self.get_position(), board.gold_list[i], self.IQ)
      if dis == None:
        dis = self.INF
      distances.append((i, dis))
    distances = sorted(distances, key=lambda x: x[1], reverse = False)

    need_to_set_a_goal = True
    if self.goal in board.gold_list:
      if i < 2:
        rang = range(i+1)
      else:
        rang = range(3)
      for j in rang:
        if board.get_obj_from_board(distances[j][0], distances[j][1]) == self.goal:
          need_to_set_a_goal = False
    if need_to_set_a_goal == True:
      # Need a new goal
      self.set_goal(board.gold_list[distances[0][0]])

    coordinate = self.get_position()
    cand_coord = ((coordinate[0]+i[0], coordinate[1]+i[1]) for i in ((1, 0), (-1, 0), (0, 1), (0, -1)))
    max_val = self.NINF
    candidates = list()
    for i in cand_coord:
      if board.can_set_position(i[0], i[1], self) == False:
        continue
      res = self.alpha_beta(board, i, self.IQ, self.MAX)
      if res > max_val:
        max_val = res
        candidates = [i]
      elif res == max_val:
        candidates.append(i)
    if len(candidates) > 1:
      dis = self.INF
      min_coord = None
      for i in candidates:
        res = self.distance(board, i, self.goal, self.IQ)
        if not res:
          res = self.INF/2
        if res < dis:
          dis = res
          min_coord = i
    else:
      min_coord = candidates[0]
    return min_coord


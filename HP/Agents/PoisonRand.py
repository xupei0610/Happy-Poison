# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "02:59, Nov. 21th, 2015"
"""This is the implement of an idiot poison agent whose action is random."""

from HP.Agents.PoisonAgent import *

import random

class PoisonRand(PoisonAgent):
  """ This is an implement for a poison agent whose action pattern is random."""
  
  def __init__(self):
    super(PoisonRand, self).__init__()

  def agent_name(self):
    """ Return the current agent's name."""
    if not self.my_name:
      self.my_name = super(PoisonRand, self).agent_name() + 'R'
    return self.my_name
  
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    This agent's action pattern is random.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if super(PoisonRand, self).want_move(board):
      pos = self.get_position()
      candidate_targets = list()
      for p in ((pos[0]+1, pos[1]), (pos[0]-1, pos[1]), (pos[0], pos[1]+1), (pos[0], pos[1]-1)):
        if not board.can_set_position(p[0], p[1], self):
          continue
        candidate_targets.append(p)
      if not candidate_targets:
        return None
      return random.choice(candidate_targets)
    return None


 

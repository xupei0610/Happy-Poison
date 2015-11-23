# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "02:59, Nov. 21th, 2015"
"""This is the implement of human player agent whose action is controlled by human player."""

from HP.Agents.HappyAgent import *

class HappyHuman(HappyAgent):

  def __init__(self):
    super(HappyHuman, self).__init__()

    self.direction_want_go = None # The direction the player wants the agent to go along

  def want_move_to(self, direction):
    """Use this beforehand, otherwise want_move() will return False.
    :param direction: the direction the player wants the agent to go along.
    :param string or None: n, s, w, or e if string is given."""
    self.direction_want_go = direction

  def can_move_on(self, board):
    """Return True if it is possible for the agent to make a move; False otherwise.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if not super(HappyAgent, self).want_move(board):
        return False
    c_pos = self.get_position()
    can = False
    for j in ((c_pos[0]+i[0], c_pos[1]+i[1]) for i in ((1,0),(-1,0),(0,1),(0,-1))):
      if board.can_set_position(j[0], j[1], self):
        can = True
        break
    return can

  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    if super(HappyAgent, self).want_move(board):
      if self.direction_want_go == None:
        return None
      c_pos = self.get_position()
      if self.direction_want_go == 'n':
        tar = (c_pos[0]-1, c_pos[1]) 
      if self.direction_want_go == 's':
        tar = (c_pos[0]+1, c_pos[1])
      if self.direction_want_go == 'w':
        tar = (c_pos[0], c_pos[1]-1)
      if self.direction_want_go == 'e':
        tar = (c_pos[0], c_pos[1]+1)
      if board.can_set_position(tar[0], tar[1], self):
        return tar
    return None

  #def set_position(self, row, col):
  #  """ Set Position for the current agent.
  #  The function here will reset the player's control to the agent."""
  #  super(HappyHuman, self).set_position(row, col)
  #  self.direction_want_go = None


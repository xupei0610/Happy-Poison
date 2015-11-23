# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "03:49, Nov. 21th, 2015"
"""This is the abstract class for all happy agent classes in this project."""

from abc import ABCMeta, abstractmethod

from HP.Agents.Agent import *

import random

class HappyAgent(Agent):
  """An Abstract Class defining the basic function and interface for all happy agent classes in this project."""
  __metaclass__ = ABCMeta

  def __init__(self):
    super(HappyAgent, self).__init__()
    self.is_corpse = False
    self.dead_in_the_hand_of = None
    self.my_name = None
    self.score = 0

  @abstractmethod
  def agent_name(self):
    """ Return the name of the agent based on the fact that it is Happy."""
    if not self.my_name:
      self.my_name = 'H#' + str(random.randint(1000, 9999))
    return self.my_name

  @abstractmethod
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    Every agent should make a move unless it cannot move.
    Each move only can help the agent work a step along up, down, left or right.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    return super(HappyAgent, self).want_move(board)

  def is_killed_by(self, killer_agent):
    """ A killed Happy will be removed from the board.
    Maybe a killed HappyAgent instance should be eliminated. I do not know.
    Basically, they should not move."""
    if not self.is_killed:
      self.is_corpse = True
      self.dead_in_the_hand_of = killer_agent

  def is_killed(self):
    """ Return True if the agent is dead."""
    return self.is_corpse

  def kills(self, victim_agent):
    """Happy never kills anyone."""
    return False

  def deadlist(self):
    """Return None since Happy never kills anyone."""
    return None

  def who_kills_me(self):
    """Return the agent who kills the current agent."""
    return self.dead_in_the_hand_of

  def harvest(self, something, board):
    """Gold, Gold, I Love Gold."""
    if something == board.GOLD_SIGN:
      self.score += 1


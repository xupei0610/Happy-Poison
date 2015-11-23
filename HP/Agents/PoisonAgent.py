# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "02:39, Nov. 21th, 2015"
"""This is the abstract class for all poison agent classes in this project."""

from abc import ABCMeta, abstractmethod
from HP.Agents.Agent import *
from HP.Agents.HappyAgent import *

import random

class PoisonAgent(Agent):
  """An Abstract Class defining the basic function and interface for all happy agent classes in this project."""
  __metaclass__ = ABCMeta

  def __init__(self):
    super(PoisonAgent, self).__init__()
    self.dead_note = list()
    self.MURDER_SIGN = 'CORPSE'
    self.score = 0
    self.my_name = None

  def agent_name(self):
    """ Return the name of the agent based on the fact that it is Poison."""
    if not self.my_name:
      self.my_name = 'P#' + str(random.randint(1000, 9999))
    return self.my_name

  @abstractmethod
  def want_move(self, board):
    """Return a turple composed of row and col id the agent wants to move, or None if it cannot move.
    Every agent should make a move unless it cannot move.
    Each move only can help the agent work a step along up, down, left or right.
    :param board: an instance of GameBoard.
    :type board: GameBoard."""
    return super(PoisonAgent, self).want_move(board)

  def is_killed_by(self, killer_agent):
    """ Do nothing. Poison is undead"""
    return False

  def is_killed(self):
    """ Return False, since Poison is undead."""
    return False

  def who_kills_me(self):
    """ Return None, since nothing can kill Poison."""
    return None

  def kills(self, victim_agent):
    """ Kill another agent."""
    if not victim_agent.is_killed:
      if victim_agent.is_killed_by(self):
        self.dead_note.append(victim_agent)
        self.harvest(self.MURDER_SIGN)
        return True
    return False
        
  def deadlist(self):
    """ Return a list of names of Happy agents killed by the agent"""
    return self.dead_note

  def harvest(self, something):
    """ Poison has the instinct of killing."""
    if something == self.MURDER_SIGN:
      self.score += 1


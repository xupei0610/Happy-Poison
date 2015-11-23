# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "17:39:50, Nov. 21th, 2015"
"""This is the main program of the HappyPosion homework with the interface of terminal-line.
Run main.py for the GUI version with full functions"""

import HP.Game as Game

if __name__ == '__main__':
  
  print('\n\033[92m===== Welcome =====\033[0m')
  print('Hi, this is a HappyPoison game developed by Pei Xu')
  print('This is a simpler version with limited functions running at command-line.')
  print('\nHope you love this game.\n')
  print('Version: ' + __version__)
  print('License: ' + __license__)
  print('Copyright: ' + __copyright__)
  print('\033[92m===================\033[0m\n')

  while True:
    print('Please choose a game mode: 1 or 2')
    print('1: Computer v.s. Computer')
    print('2: Human v.s. Computer')
    choose = input('')
    if int(choose) == 1:
      player = 'C'
      break
    elif int(choose) == 2:
      player = 'H'
      break
  print('Game Starts')
  Game.run(player)

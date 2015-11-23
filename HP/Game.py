# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "14:37, Nov. 20th, 2015"
"""This is intrance program of the implement for HappyPosion.
Its responsiblity is to load agents and call GameBoard to prepare the board."""

import random, time, os
import tkinter as tk
import tkinter.font as tkfont

from HP.GameBoard import *
from HP.Agents.HappyAgent import *
from HP.Agents.PoisonAgent import *
from HP.Agents.HappyCompu import *
from HP.Agents.HappyHuman import *
from HP.Agents.PoisonIntel import *
from HP.Agents.PoisonRand import *

SQUARE_SIZE = 40
BASE_TURN = 10        # A new obstacle may appear at the game turns exceeding this value 
OBS_INCREASE_RATE = 1 # The possbility of a new obstacle appearing. Integer, 0-9

def legal_check(game_width, game_height, num_happy, num_poison, num_gold, obs_increase, tk_instance=None, raise_except = False):
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
  :param obs_increase: more obstacles will appear during the game running or not,
  :type obs_increase: boolean.
  :param raise_except: this function will raise an exception or just return false if failure.
  :type raise_except: boolean."""
  try:
    GameBoard.legal_check(game_width, game_height, num_happy, num_poison, num_gold)
    if isinstance(tk_instance, tk.Tk):
      tk_instance.update()
      redundant_area = tk_instance.geometry().split('+')
      game_width = int(game_width)
      game_height = int(game_height)
      screen_width = tk_instance.winfo_screenwidth()-int(redundant_area[1])
      screen_height = tk_instance.winfo_screenheight()-int(redundant_area[2])
      if game_width * SQUARE_SIZE > screen_width:
        raise GameBoardException('Game Width is too huge to display on the screen', 101)
      if game_height * SQUARE_SIZE > screen_height:
        raise GameBoardException('Game height is too huge to display on the screen', 102)
  except Exception as err:
    if raise_except == True:
      raise err
    else:
      return False
  return True

def run(player='C', width=20, height=10, num_happy=1, poisons=['R', 'R'], num_gold=1, obs_increase=False, poison_move_rate=3, tk_canvas = None, tk_toplevel=None, image_happy=None, image_poison=None, image_gold=None, image_obstacle=None):
  """The main function of this game program. It will generate a game according to the given parameters.
  !ATTENTION! Use legal_check() beforehand.
  :param player: the type of player. 'C' means computer, 'H' means human.
  :type player: string, 'C' or 'H'.
  :param width: the game board's width, the number of squares in a row.
  :type width: integer.
  :param height: the game board's height, the number of squares in a col.
  :type height: integer.
  :param num_happy: the number of happys. 1 if player is human.
  :type num_happy: integer.
  :param posions: posions' action pattern. 'I' means intelligent; 'R' means random.
  :type posions: list.
  :param num_gold: the number of gold.
  :type num_gold: integer.
  :param obs_increase: more obstacles will appear during the game running or not,
  :type obs_increase: boolean.
  :param poison_move_rate: the rate of poison making a move. 3 means 30%
  :type poison_move_rate: integer < 10
  :param game_running_flag: a object passed by reference, it will be set None when game is over.
  :type game_running_flag: suggested to be list.
  :param tk_canvas: the instance of a tk canvas, or None if not use GUI
  :type poison_type: tk.Canvas or None.
  :return: None.
  """

  # Set agent for Happy
  if player == 'H':
    happy_agents = [HappyHuman()]
  else:
    happy_agents = [HappyCompu() for i in range(num_happy)]

  # Set agent for each Poison
  poison_agents = list()
  for i in poisons:
    if i == 'I':
      poison_agents.append(PoisonIntel())
    else:
      poison_agents.append(PoisonRand())
   
  # Initialize Game Board
  board = GameBoard(game_width=width, game_height=height,\
      happy_agents=happy_agents, poison_agents=poison_agents,\
      num_gold=num_gold)

  # Draw Board    
  board.draw_board()
  if tk_canvas:
    draw_canvas(tk_canvas, board, image_happy, image_poison, image_gold, image_obstacle)
    if player == 'H':
      def control_happy(event):
        if event.keysym == 'W' or event.keysym == 'w' or event.keysym == 'Up':
          happy_agents[0].want_move_to('n')
        elif event.char == 'S' or event.keysym == 's' or event.keysym == 'Down':
          happy_agents[0].want_move_to('s')
        elif event.char == 'A' or event.keysym == 'a' or event.keysym == 'Left':
          happy_agents[0].want_move_to('w')
        elif event.char == 'D' or event.keysym == 'd' or event.keysym == 'Right':
          happy_agents[0].want_move_to('e')
      tk_canvas.bind('<KeyRelease>', control_happy)
      tk_canvas.focus_set()

  # Game Starts
  turns = 0
  while board.game_result() == board.GAME_RUNNING:
    turns += 1
    if player == 'H' and happy_agents[0].can_move_on(board):
      if tk_canvas:
        print('Use W,A,S,D or arrow keys to control Happy')
        while True:
          target = happy_agents[0].want_move(board)
          if target:
            board.set_object_position(target[0], target[1], happy_agents[0])
            happy_agents[0].want_move_to(None)
            break
      else:
        print('Use W,A,S,D to control Happy. Press Q to exit.')
        while True:
          direction = input('')
          if direction == 'w' or direction == 'W':
            happy_agents[0].want_move_to('n')
            want_move = True
          elif direction == 's' or direction == 'S':
            happy_agents[0].want_move_to('s')
            want_move = True
          elif direction == 'a' or direction == 'A':
            happy_agents[0].want_move_to('w')
            want_move = True
          elif direction == 'd' or direction == 'D':
            happy_agents[0].want_move_to('e')
            want_move = True
          elif direction == 'q' or direction == 'Q':
            print('\n\033[92mBye. Have a happy day.\033[0m\n')
            exit()
          if want_move == True:
            target = happy_agents[0].want_move(board)
            if target:
              board.set_object_position(target[0], target[1], happy_agents[0])
              happy_agents[0].want_move_to(None)
              break
            else:
              print('Happy cannot go that way.')
    else:
      for i in happy_agents:
        target = i.want_move(board)
        if target:
          board.set_object_position(target[0], target[1], i)
    for i in poison_agents:
      #if random.randint(0, 9) < poison_move_rate:
      target = i.want_move(board)
      if target:
        board.set_object_position(target[0], target[1], i)

    if obs_increase == True and turns > BASE_TURN:
      #TODO obs increases
      # possiblility = random.randint(0, 9)
      # if possibiliy < OBS_INCREASE_RATE
      #   col =
      #   row = 
      #   if row and col:
      #     board.set_object_position(row, col, board.OBSTACLE_SIGN)
      pass
    # Output to terminal
    board.draw_board()
    # Output to GUI
    if tk_canvas:
      draw_canvas(tk_canvas, board, image_happy, image_poison, image_gold, image_obstacle)
    if player=='C':
      time.sleep(1) # We donot need 60 fps for this game.


  # Output Game Result
  if tk_canvas:
    new_win = tk.Toplevel(tk_toplevel)
    if board.game_result() == board.HAPPY_WIN:
      title = 'Congralutions!'
      if len(happy_agents) > 1:
        message = 'Happys take away '
      else:
        message = 'Happy takes away '
      if num_gold > 1:
        message += 'all treasures.'
      else:
        message += 'the treasure.'
    else:
      title = 'Oh~~Noooooooo!'
      message = ''
      if len(happy_agents) > 1:
        message = 'All Happys were'
      else:
        message = 'The only Happy was'
      message += ' killed.'
    new_win.title(title)
    new_win.config(padx=0, pady=10)
    new_win.resizable(tk.NO, tk.NO)
    msg = tk.Label(new_win, text=message)
    msg.config(highlightcolor='white', borderwidth=0, width=40, height=5, padx=5, pady=5,relief=tk.FLAT)
    msg.pack(fill=tk.BOTH)
    tk.Button(new_win, text="Got It", command=new_win.destroy).pack()
    

def draw_canvas(tk_canvas, board, image_happy=None, image_poison=None, image_gold=None, image_obstacle=None):
  """ Initialize Canvas. Draw Grid and Put Objects on the Canvas.
  :param tk_canvas: canvas.
  :type tk_canvas: tkinter.Canvas.
  :param board: GameBoard.
  :type board: GameBoard.
  :param image_happy: handle for Happy's image. I will draw a sign if it is None.
  :type image_happy: PhotoImage or None.
  :param image_poison: handle for Poison's image. I will draw a sign if it is None.
  :type image_poison: PhotoImage or None.
  :param image_gold: handle for gold's image. I will draw a sign if it is None.
  :type image_gold: PhotoImage or None.
  :param image_obstacle: handle for obstacle's image. I will draw a sign if it is None.
  :type image_obstacle: PhotoImage or None."""
  tk_canvas.delete()
  tk_canvas.config(width=board.game_width*SQUARE_SIZE, height=board.game_height*SQUARE_SIZE)
  asset_path = os.path.split(os.path.realpath(__file__))[0] + os.sep + 'asset' + os.sep
  for i in range(board.game_height):
    for j in range(board.game_width):
      tk_canvas.create_rectangle((j*SQUARE_SIZE, i*SQUARE_SIZE, (j+1)*SQUARE_SIZE, (i+1)*SQUARE_SIZE), fill='white', outline="black")
      obj = board.get_obj_from_board(i, j)
      imag = None
      if obj == board.GOLD_SIGN:
        if image_gold:
          tk_canvas.create_image(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), image=image_gold)
        else:
          tk_canvas.create_text(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), state=tk.DISABLED, text='$',fill='yellow', font='Monospace '+ str(SQUARE_SIZE) + ' bold')
      elif obj == board.OBSTACLE_SIGN:
        if image_obstacle:
          tk_canvas.create_image(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), image=image_obstacle)
        else:
          #tk_canvas.create_oval(j*SQUARE_SIZE, i*SQUARE_SIZE, (j+1)*SQUARE_SIZE, (i+1)*SQUARE_SIZE, fill='black')
          tk_canvas.create_text(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), state=tk.DISABLED, text='X', fill='cyan', font='Monospace '+ str(SQUARE_SIZE) + ' bold')
      elif isinstance(obj, HappyAgent):
        if image_happy:
          tk_canvas.create_image(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), image=image_happy)
        else:
          tk_canvas.create_text(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), state=tk.DISABLED, text='@', fill='green', font='Monospace '+ str(SQUARE_SIZE) + ' bold')
      elif isinstance(obj, PoisonAgent):
        if image_poison:
          tk_canvas.create_image(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), image=image_poison)
        else:
          tk_canvas.create_text(j*SQUARE_SIZE + int(SQUARE_SIZE/2), i*SQUARE_SIZE+int(SQUARE_SIZE/2), state=tk.DISABLED, text='∞',fill='red', font='Monospace '+ str(SQUARE_SIZE) + ' bold')
  tk_canvas.create_line(3, 3, 3, board.game_height*SQUARE_SIZE)
  tk_canvas.create_line(0, 3, board.game_width*SQUARE_SIZE, 3)


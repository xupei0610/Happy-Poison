# -*- coding:utf-8 -*-
__author__ = "Pei Xu, #5186611, xuxx0884@umn.edu"
__copyright__ = "Copyright 2015-, Pei Xu"
__license__ = "MIT"
__version__ = "1.0.1"
__date__ = "14.34:50, Nov. 20th, 2015"
"""This is the main program of the HappyPosion homework.
It is responsible for the management of windows and loading the game function."""

# GUI libraries
import tkinter as tk
from tkinter import messagebox
# For os.path
import os
# For ceil
import math
# MultiThread library
from threading import Thread
# Game libraries
import HP.Game as Game
import HP.GameBoard as Board

class AppGUI(tk.Frame):
  """ Management for the windows of HappyPoison"""

  def __init__(self, master):
    tk.Frame.__init__(self, master)
    self.master = master
    self.master.config(bg='white')
    print('\n\033[92m===== Welcome =====\033[0m')
    print('Hi, this is a HappyPoison game developed by Pei Xu')
    print('\nHope you love this game.\n')
    print('Version: ' + __version__)
    print('License: ' + __license__)
    print('Copyright: ' + __copyright__)
    print('\033[92m===================\033[0m\n')

    # Initialize Game information
    self.game_width = 20
    self.game_height = 10
    self.obs_increase = False
    self.num_happy = 1
    self.num_poison = 2
    self.num_gold = 1
    self.game_pattern = "C"
    self.game_thread = None
    self.idiot_poison = 0
    self.poison_move_rate = 3

    asset_path = os.path.split(os.path.realpath(__file__))[0][0:-2] + os.sep + 'asset' + os.sep
    # Initialize Image Widget for Canvas
    # Use this for the sake of preventing Python CC these pic
    try:
      self.poison_pic = tk.PhotoImage(file = asset_path + 'poison.gif')
      self.poison_pic = self.poison_pic.subsample(math.ceil(self.poison_pic.width()/Game.SQUARE_SIZE), math.ceil(self.poison_pic.height()/Game.SQUARE_SIZE))
      self.happy_pic = tk.PhotoImage(file = asset_path + 'happy.gif')
      self.happy_pic = self.happy_pic.subsample(math.ceil(self.happy_pic.width()/Game.SQUARE_SIZE), math.ceil(self.happy_pic.height()/Game.SQUARE_SIZE))
      self.gold_pic = tk.PhotoImage(file = asset_path + 'gold.gif')
      self.gold_pic = self.gold_pic.subsample(math.ceil(self.gold_pic.width()/Game.SQUARE_SIZE), math.ceil(self.gold_pic.height()/Game.SQUARE_SIZE))
      self.obstacle_pic = None
    except Exception as err:
      #raise err
      self.poison_pic = None
      self.happy_pic = None
      self.gold_pic = None
      self.obstacle_pic = None

    # Initialize PopUp Window
    self.new_game_window = None
    self.help_window = None
    self.about_window = None

    # Window Title
    self.master.title('HappyPoison -- Powered by PeiXu')

    # Minsize
    #self.master.minsize(480, 360)
    self.master.resizable(width=False, height=False)

    # Load Menu Bar
    self.master.config(menu=self.menubar())

    self.master.rowconfigure(0, weight=3)
    self.master.rowconfigure(1, weight=0)
    self.master.columnconfigure(0, weight=1)
    # Layout the window
    self.content = tk.Frame(self.master, padx=3, pady=12)
    #self.content.pack(fill=tk.BOTH, side=tk.TOP, expand=1)
    self.content.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.W, tk.E))
    self.status_frame = tk.Frame(self.master, padx=0, pady=0, height=1)
    #self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, anchor=tk.S, expand=1)
    self.status_frame.grid(row=1, column=0, sticky=(tk.S, tk.W, tk.E))

    # Status Bar
    self.status_bar = tk.Text(self.status_frame, height=1)
    self.status_bar.config(highlightcolor='white')
    self.status_bar.pack(fill=tk.X, expand=1, side=tk.BOTTOM, anchor=tk.S)

    # Put a START GAME button on the start window
    tk.Label(self.content, text='\nWhat are you waitting for?\n').pack()
    tk.Button(self.content, text='Start A New Game Now', command=self.new_game).pack()

  def menubar(self):
    """Set Up the menu bar for the window"""
    menubar = tk.Menu(self.master)

    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="New Game", command=self.new_game)
    filemenu.add_command(label="Restart", command=self.restart)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=self.exit)
    menubar.add_cascade(label="File", menu=filemenu)

    helpmenu = tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Help", command=self.helpme)
    helpmenu.add_separator()
    helpmenu.add_command(label="About", command=self.about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    return menubar

  def new_game(self):
    """Show Options for Seting Up A New Game"""
    if self.game_running():
      a = self.comfirm_open_a_new_game()
      if a != True:
        return
    print('Opening The Game Config Window...')
    if self.new_game_window != None:
      self.new_game_window.destroy()
    self.new_game_window = tk.Toplevel(self.master)
    self.new_game_window.title('Start A New Game')
    self.new_game_window.resizable(tk.NO, tk.NO)
    self.new_game_window.config(padx=12, pady=12)

    # Label Widgets
    tk.Label(self.new_game_window, text='Game Pattern').grid(row=0, column=0, sticky=tk.E)
    tk.Label(self.new_game_window, text='Game Width').grid(row=1, column=0, sticky=tk.E)
    tk.Label(self.new_game_window, text='Game Height').grid(row=1, column=2, sticky=tk.E)
    tk.Label(self.new_game_window, text='Happy x').grid(row=2, column=0, sticky=tk.E)
    tk.Label(self.new_game_window, text='Poison x').grid(row=2, column=2, sticky=tk.E)
    tk.Label(self.new_game_window, text='Treasure x').grid(row=2, column=4, sticky=tk.E)
    tk.Label(self.new_game_window, text='Obstacle').grid(row=3, column=0, sticky=tk.E)

    # Variables for Entry Widgets
    game_pattern = tk.StringVar()
    def game_pattern_callback(*args):
      if game_pattern.get() == 'C':
        num_happy_entry.config(state=tk.NORMAL)
      else:
        num_happy.set(1)
        num_happy_entry.config(state=tk.DISABLED)
    game_pattern.trace('w', game_pattern_callback)
    game_width = tk.StringVar()
    game_height = tk.StringVar()
    num_happy = tk.StringVar()
    num_poison = tk.StringVar()
    num_gold = tk.StringVar()
    obs_increase = tk.BooleanVar()

    # Entry Widgets
    radiobutton_frame = tk.Frame(self.new_game_window, bg='red')
    radiobutton_frame.grid(row=0, column=1, columnspan=5)
    tk.Radiobutton(radiobutton_frame, text="Computer vs Computer", variable=game_pattern, value='C').grid(row=0, column=0)
    tk.Radiobutton(radiobutton_frame, text="Human vs Computer", variable=game_pattern, value='H').grid(row=0,column=1)
    game_width_entry = tk.Entry(self.new_game_window, width=3, textvariable=game_width)
    game_width_entry.grid(row=1, column=1, sticky=tk.W)
    game_height_entry = tk.Entry(self.new_game_window, width=3, textvariable=game_height)
    game_height_entry.grid(row=1, column=3, sticky=tk.W)
    num_happy_entry = tk.Entry(self.new_game_window, width=3, textvariable=num_happy)
    num_happy_entry.grid(row=2, column=1, sticky=tk.W)
    tk.Entry(self.new_game_window, width=3, textvariable=num_poison).grid(row=2, column=3, sticky=tk.W)
    num_gold_entry = tk.Entry(self.new_game_window, width=3, textvariable=num_gold)
    num_gold_entry.grid(row=2, column=5, sticky=tk.W)
    tk.Checkbutton(self.new_game_window, text='increases in the game', variable=obs_increase).grid(row=3, column=1, columnspan=5, sticky=tk.W)

    # Function for checking the legality of input information
    def _go_go_go():
      print('Checking The Input...')
      game_width_entry.config(highlightbackground='white')
      game_height_entry.config(highlightbackground='white')
      num_happy_entry.config(highlightbackground='white')
      num_gold_entry.config(highlightbackground='white')
      try:
        Game.legal_check(game_width=game_width.get(), game_height=game_height.get(),num_happy=num_happy.get(), num_poison=num_poison.get(), num_gold=num_gold.get(),obs_increase=obs_increase.get(), tk_instance=self.master, raise_except = True)
      except ValueError:
        self.display_error_info('A wrong value is input!')
      except Board.GameBoardException as err:
        if err.err_code == 1 or err.err_code == 101:
          game_width_entry.config(highlightbackground='red')
        elif err.err_code == 2 or err.err_code == 102:
          game_height_entry.config(highlightbackground='red')
        elif err.err_code == 3:
          num_happy_entry.config(highlightbackground='red')
        elif err.err_code == 4:
          num_gold_entry.config(highlightbackground='red')
        self.display_error_info(err.message)
      else:
        self.game_width = int(game_width.get())
        self.game_height = int(game_height.get())
        self.num_happy = int(num_happy.get())
        self.num_poison = int(num_poison.get())
        self.num_gold = int(num_gold.get())
        self.obs_increase = bool(obs_increase.get())
        self.game_pattern = game_pattern.get()
        self.idiot_poison = self.num_poison//2
        self.new_game_window.destroy()
        self.start_game()

    # Game Start Button
    tk.Button(self.new_game_window, text="GO GO GO", command=_go_go_go).grid(row=4, column=0, columnspan=6)

    # Default Values of widgets
    game_pattern.set(self.game_pattern)
    game_width.set(self.game_width)
    game_height.set(self.game_height)
    num_happy.set(self.num_happy)
    num_poison.set(self.num_poison)
    num_gold.set(self.num_gold)
    obs_increase.set(self.obs_increase)

  def comfirm_open_a_new_game(self):
    """Show a dialog to inquire client"""
    msg = 'Are you sure to discard the current game and start a new?'
    print(msg)
    a = tk.messagebox.askyesno('Really?', message = msg)
    if a == True:
      print('Yes')
    else:
      print('No')
    return a

  def restart(self):
    """Start A New Game according to the current config"""
    if self.game_running():
      a = self.comfirm_open_a_new_game()
      if a == True:
        print('Starting A New Game...')
        return self.start_game()
    else:
      return self.new_game()

  def start_game(self):
    """Start A Game"""
    print('\n\033[92m===== Game Configure Information =====\033[0m')
    print('Bord Width: '+str(self.game_width))
    print('Bord Height: '+str(self.game_height))
    print('Number of Happys: '+str(self.num_happy))
    print('Number of Poisons: '+str(self.num_poison))
    print('Number of Treasures: '+str(self.num_gold))
    if self.obs_increase == True:
      print('Obstacle: Increasing' )
    else:
      print('Obstacle: Permanent')
    print('\033[92m======================================\033[0m\n')
    self.update_status_bar()
    print('Stopping Current Game...')
    self.stop_current_game()
    print('Starting Game Application...')
    # Load Poisons' Type
    poisons_pattern = list()
    for i in range(self.num_poison):
      if i < self.idiot_poison:
        poisons_pattern.append('R')
      else:
        poisons_pattern.append('I')
    # Generate Canvas
    for w in self.content.winfo_children():
      w.destroy()
    canvas = tk.Canvas(self.content)
    canvas.pack(fill=tk.BOTH, expand=1)
    # Use Multithread for the sake of preventing GUI from crashing
    try:
      self.game_thread = Thread(target=Game.run, args=(self.game_pattern, self.game_width, self.game_height, self.num_happy, poisons_pattern, self.num_gold, self.obs_increase, self.poison_move_rate, canvas, self.master, self.happy_pic, self.poison_pic, self.gold_pic, self.obstacle_pic))
      self.game_thread.setDaemon(True)
      self.game_thread.start()
    except Exception as err:
      self.stop_current_game()
      self.display_error_info(str(err))

  def update_status_bar(self):
    if self.game_pattern == 'C':
      status_text = 'Computer vs Computer'
    else:
      status_text = 'Human vs Computer'
    status_text += ' - Happy x ' + str(self.num_happy) + ' - Idiot Poison x ' + str(self.idiot_poison) + ' - Smart Poison: ' + str(self.num_poison-self.idiot_poison) + ' - Treasure x ' + str(self.num_gold) + ' - Game Size: ' + str(self.game_width) + 'x' + str(self.game_height)
    print('Update Status Bar: ' + status_text)
    self.status_bar.delete(1.0, tk.END)
    self.status_bar.insert(tk.END, status_text)

  def helpme(self):
    """Show Help Information"""
    print('Opening Help Window...')
    # TODO help information
    help_text = "TODO help information"
    if self.help_window != None:
      self.help_window.destroy()
    self.help_window = tk.Toplevel(self.master)
    self.help_window.title('Help')
    self.help_window.resizable(tk.NO, tk.NO)
    msg = tk.Text(self.help_window)
    msg.insert(tk.END, help_text)
    msg.config(highlightcolor='white', borderwidth=0, width=40, height=5, padx=5, pady=5,relief=tk.FLAT, insertborderwidth=0, selectborderwidth=0, state=tk.DISABLED)
    msg.pack(fill=tk.BOTH)
    msg.bind("<1>", lambda event: msg.focus_set())
    tk.Button(self.help_window, text="Got It", command=self.help_window.destroy).pack()
    tk.Button(self.help_window)
    print('\n\033[92m===== Help =====\033[0m' + help_text + '\n\033[92m================\033[0m\n')

  def about(self):
    """Show About Information"""
    print('Opening About Window...')
    source_add = "https://github.umn.edu/xuxx0884"
    about_text = "Version: "+__version__+ "\nDeveloped by: Pei Xu\nfor CSCI4511W\nSource at:\n" + source_add
    if self.about_window != None:
      self.about_window.destroy()
    self.about_window = tk.Toplevel(self.master)
    self.about_window.title('About...')
    self.about_window.resizable(tk.NO, tk.NO)
    msg = tk.Text(self.about_window)
    msg.insert(tk.END, about_text)
    msg.config(highlightcolor='white', borderwidth=0, width=40, height=5, padx=5, pady=5,relief=tk.FLAT, state=tk.DISABLED)
    msg.pack(fill=tk.BOTH)
    msg.bind("<1>", lambda event: msg.focus_set())
    tk.Button(self.about_window, text="Got It", command=self.about_window.destroy).pack()
    print('\n\033[92m===== About The Application =====\033[0m\n' + about_text + '\n]\033[92m=================================\033[0m\n')

  def exit(self):
    """Exit the app"""
    print('\n\033[92mBye. Have a happy day.\033[0m\n')
    self.stop_current_game()
    self.quit()

  def destroy(self):
    """Exit the app via directly pressing x"""
    print('\n\033[92mBye. Have a happy day.\033[0m\n')
    self.stop_current_game()

  def display_error_info(self, msg):
    """Display error information"""
    print('\033[91m'+msg+'\033[0m')
    tk.messagebox.showinfo('Something Wrong', message = msg)

  def game_running(self):
    if self.game_thread == None:
      return False
    if self.game_thread.is_alive():
      return True
    return False

  def stop_current_game(self):
    if self.game_thread != None:
      if self.game_thread.is_alive():
        self.game_thread.stopped = True
      self.game_thread = None


if __name__ == '__main__':
  AppGUI(master=tk.Tk()).mainloop()

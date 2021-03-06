# HappyPoison
An implement for HappyPoison game.

# Version
v. 1.0.2

# License
MIT

# Feature
This game uses Tcl/Tk as the GUI library and, meanwhile, provides a command-line version.

The game supports Computer v.s. Computer and Human v.s. Computer.

Multi-Happy-Players v.s. Multi-Poison-Players is supported in Computer v.s. Computer mode.

This program uses a more efficient evaluation system compared to the implement offered in CS4511's repository.

# Evaluation System
The evaluation system of this game is based on min-max algorithm with alpha-beta pruning.

It considers the distance between an agent and its possible goal. This distance has a weight of 10.

For each Happy agent, it also considers the distance between the Happy agent, the distance who has a weight of 5, and the distance between itself and the Poison agent who may set the Happy agent as the goal.

Defaultly, each Happy agent will set the gold who is the most close to it as its goal, and each Poison agent will set the Happy agent who is the most close to it as its goal.

Agents will not change their goal, except they are too far away from their goals as the game goes on.

Each agent has their own name and own IQ. Their IQ decides the depth of min-max algorithm's searching.

# Agents
Four kinds of agents are developed.

   Intelligent Happy agent,
   Intelligent Poison agent,
   Poison agent whose action pattern is random completely, and
   Happy agent, for human player, the agent who can response to the control signs from the outside.

# Usage
Environment: Python 3.4 with support to TK.

Run _*main.py*_ .

# Thanks
Have a good day.

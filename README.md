# PythonBattleShip

# Game Instructions

This project allows a user to play a game of Battleship against a CPU with the use of a GUI powered by pygame.
The user is presented with two game boards; the user's on the left and the CPU's on the right.
Instructions are given to the user through the console.
A user must first place 5 ships: Aircraft carrier (5), Battleship (4), Cruiser (4), Destroyer (3), and Submarine (2).
To do this, the user can click the squares on their board (left) in a vertical or horizontal pattern.
The CPU will than randomly generate placement for their ships.
The user will then be prompted through the console to begin firing at the CPU's board (left).
A white X will appear if the shot is a miss and if a shot is a hit then the intiial of the ship hit will appear.
The CPU will fire on alternating turns. The CPU will initially randomly fire until it hits a ship.
When the CPU hits a ship, their shots will switch from random fire to proximity fire until the ship is sunk.
This game will continue until either the user or CPU sink all the oponents ships.

# Game design

This project was designed in an object oriented fashion. The gameboard, squares, and pieces are some examples of 
objects I used to build this game. The project is setup into 3 files. The main game mechanics are found
in BoardModel.py. The design I chose was of a Model View Controller. The view and controller can be found
in Main.py. The GUI is powered by pygame. One of the hardest features was the proximity fire of the CPU.
To accomplish this, I constantly feed the CPU a report of the lattest shot and if it was a hit or miss.
The recent hit shots are stored on a stack. The CPU moves along the stack shooting left, right, up, and down
until the ship and all surrounding ships are sunk.

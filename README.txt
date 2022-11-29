
BackgammonAI

Requires pygame package: pip install pygame

Run command: python3 BackgammonAI.py
Requires python3 interpreter

Note: This will not run on a virtual machine. Pygame uses local window functionality to display.

The BackgammonAI.py program runs backgammon, either with 2 AI's against each other or with a player against the AI.

The user_playing booleon at the top of the file dictates whether the user will play or the program will run two AI's against each other. Only set this to false if using the attached file RunXTimes.py. Otherwise, it will crash when trying to open the file that does not exist

RunXTimes.py is a python program that plays the backgammon program X times, entered by the user when first starting the file. I used this to test utility functions against each other, running the two AI's against each other a thousand times.
Run command: python3 RunXTimes.py

Pygame was used to create the game visuals

User will always play as black. Utility_best will always play as white.
Utility_experiment will play as black if user is not playing.

Game is internally represented as a python list with 26 spots: 24 for the board and one for each end final bin. Two more variables, black_bar and white_bar, are used to represent how many pieces are on the bar.

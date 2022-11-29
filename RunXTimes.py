import os

#BlackWins.txt is a temporary file created to keep track of wins over multiple runs
#The file is removed after it's no longer needed

f = open("BlackWins.txt", "w")
f.write("0") # no wins yet
f.close()

x_str = input("Enter number of games: ")

x = int(x_str)

for i in range(x):
    exec(open("BackgammonAI.py").read())
    print("Game " + str(i + 1) + " complete")


f = open("BlackWins.txt", "r")
wins = f.read()
f.close()

os.remove("BlackWins.txt")

print("Black Win Percentage: " + str(round(float(wins) /(x) * 100, 2)) + "%")

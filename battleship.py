import random
import re
import time
from random import randint
class game:
    def __init__(self):
        self.cross = "X"
        self.water = "≈"
        self.question = "?"
        self.boat = "*"
        self.boat_lengths = [2, 2, 3, 3]
        self.lettersToNumbers = {"A" : 1, "B" : 2, "C" : 3, "D" : 4, "E" : 5, "F" : 6}
        self.gridPlayer = """      A    B    C    D    E    F
    +----+----+----+----+----+----+
  1 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  2 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  3 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  4 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  5 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  6 |    |    |    |    |    |    |
    +----+----+----+----+----+----+"""
        self.gridBot = self.gridPlayer
        self.gridBotVisible = self.gridPlayer
        self.xPosIndex = {"A" : 7, "B" : 12, "C" : 17, "D" : 22, "E" : 27, "F" : 32}
    def updateGrid(self, gridIdentifier, position, insert_type):
        xPos = int(self.xPosIndex[position[0]])
        yPos = int(position[1])*2
        if gridIdentifier == 0:
            temp_grid = self.gridPlayer
        elif gridIdentifier == 1:
            temp_grid = self.gridBot
        elif gridIdentifier == 2:
            temp_grid = self.gridBotVisible
        temp_grid = temp_grid.splitlines()
        temp_grid_line = list(temp_grid[yPos])
        # del temp_grid_line[xPos]
        if insert_type == 0:
            temp_grid_line[xPos] = self.question
        elif insert_type == 1:
            temp_grid_line[xPos] = self.water
        elif insert_type == 2:
            temp_grid_line[xPos] = self.cross
        elif insert_type == 3:
            temp_grid_line[xPos] = self.boat
        temp_grid[yPos] = ''.join(temp_grid_line)
        temp_grid = '\n'.join(temp_grid)
        if gridIdentifier == 0:
            self.gridPlayer = temp_grid
        elif gridIdentifier == 1:
            self.gridBot = temp_grid
        elif gridIdentifier == 2:
            self.gridBotVisible = temp_grid 
    
    def viewLocationData(self, position):
        xPos = int(self.xPosIndex[position[0]])
        yPos = int(position[1])*2
        temp_grid = self.gridBot
        temp_grid = temp_grid.splitlines()
        temp_grid_line = list(temp_grid[yPos])
        return temp_grid_line[xPos]

    def viewLocationDataBot(self, position):
        xPos = int(self.xPosIndex[position[0]])
        yPos = int(position[1])*2
        temp_grid = self.gridPlayer
        temp_grid = temp_grid.splitlines()
        temp_grid_line = list(temp_grid[yPos])
        return temp_grid_line[xPos]

    def startGame(self):
        user_choices = []
        boat_lengths = self.boat_lengths
        for i in range(len(boat_lengths)):
            first_pos_valid = False
            while first_pos_valid == False:
                first_pos = chr(65+randint(0, 5)) + str(randint(1, 6))
                locations, first_pos_valid = self.directionChoose(user_choices, first_pos, boat_lengths[i])
            user_choices.append(locations)
        self.user_choices = user_choices
        
        bot_choices = []
        boat_lengths = self.boat_lengths
        for i in range(len(boat_lengths)):
            first_pos_valid = False
            while first_pos_valid == False:
                first_pos = chr(65+randint(0, 5)) + str(randint(1, 6))
                locations, first_pos_valid = self.directionChoose(bot_choices, first_pos, boat_lengths[i])
            bot_choices.append(locations)
        self.bot_choices = bot_choices
        # print(bot_choices)

    def directionChoose(self, locations, currentChoice, boatLength):
        if (any(currentChoice in i for i in locations)):
            return [], False
        current_pos_y = int(currentChoice[1])
        current_pos_x = int(self.lettersToNumbers[currentChoice[0]])
        direction1 = [currentChoice]
        direction2 = [currentChoice]
        direction3 = [currentChoice]
        direction4 = [currentChoice]
        directions = [direction1, direction2, direction3, direction4]
        valids = [False, False, False, False]
        if current_pos_y-boatLength+1>0:
            valids[0] = True
        if current_pos_x+boatLength-1<=6:
            valids[1] = True
        if current_pos_y+boatLength-1<=6:
            valids[2] = True
        if current_pos_x-boatLength+1>0:
            valids[3] = True
        for k in range(boatLength-1):
            if valids[0] == True:
                currentLocation = directions[0][len(directions[0])-1]
                currentLocationX = int(self.lettersToNumbers[currentLocation[0]])
                currentLocationY = int(currentLocation[1])
                newLocation = chr(64+currentLocationX) + str(currentLocationY-1)
                if (any(newLocation in i for i in locations)):
                    valids[0] = False
                else: 
                    directions[0].append(newLocation)
            if valids[1] == True:
                currentLocation = directions[1][len(directions[1])-1]
                currentLocationX = int(self.lettersToNumbers[currentLocation[0]])
                currentLocationY = int(currentLocation[1])
                newLocation = chr(64+currentLocationX+1) + str(currentLocationY)
                if (any(newLocation in i for i in locations)):
                    valids[1] = False
                else:
                    directions[1].append(newLocation)
            if valids[2] == True:
                currentLocation = directions[2][len(directions[2])-1]
                currentLocationX = int(self.lettersToNumbers[currentLocation[0]])
                currentLocationY = int(currentLocation[1])
                newLocation = chr(64+currentLocationX) + str(currentLocationY+1)
                if (any(newLocation in i for i in locations)):
                    valids[2] = False
                else:
                    directions[2].append(newLocation)
            if valids[3] == True:
                currentLocation = directions[3][len(directions[3])-1]
                currentLocationX = int(self.lettersToNumbers[currentLocation[0]])
                currentLocationY = int(currentLocation[1])
                newLocation = chr(64+currentLocationX-1) + str(currentLocationY)
                if (any(newLocation in i for i in locations)):
                    valids[3] = False
                else:
                    directions[3].append(newLocation)
        options = []
        if valids[0] == True:
            options.append(0)
        if valids[1] == True:
            options.append(1)
        if valids[2] == True:
            options.append(2)
        if valids[3] == True:
            options.append(3)
        if options == []:
            return [], False
        random_direction = random.choice(options)
        direction = directions[random_direction]
        return direction, True

    def resetGrids(self):
        self.gridPlayer = """      A    B    C    D    E    F
    +----+----+----+----+----+----+
  1 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  2 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  3 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  4 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  5 |    |    |    |    |    |    |
    +----+----+----+----+----+----+
  6 |    |    |    |    |    |    |
    +----+----+----+----+----+----+"""
        self.gridBot = self.gridPlayer

    def takeShot(self, location):
        data = self.viewLocationData(location)
        if data == "*" and data != "X":
            self.updateGrid(2, location, 2)
            self.updateGrid(1, location, 2)
            return True
        else:
            self.updateGrid(2, location, 1)
            return False
    
    def takeShotBot(self, location):
        data = self.viewLocationDataBot(location)
        if data == "*" and data != "X":
            self.updateGrid(0, location, 2)
            return True
        else:
            self.updateGrid(0, location, 1)
            return False

print("Welcome to battlefield! There are 4 ships of lengths 2, 2, 3 and 3. You need to sink the opponents ships before they sink yours to win!\n\n")
print("* represents a boat, X marks a hit, ≈ marks a miss\n\n")
ch = False
x = game()
gameOngoing = True
while ch == False:
    x.resetGrids()
    x.startGame()
    for a in range(len(x.user_choices)):
        for b in range(len(x.user_choices[a])):
            x.updateGrid(0, x.user_choices[a][b], 3)
    print(x.gridPlayer)
    correct_input = False
    while correct_input == False:
        user_ch = input("Do you want to continue with this layout? y/n: ")
        if user_ch == "y" or user_ch == "Y":
            correct_input = True
            ch = True
        elif user_ch == "n" or user_ch == "N":
            correct_input = True
            ch = False
        else:
            correct_input = False
# test = x.gridPlayer
# test = test.splitlines()
for a in range(len(x.bot_choices)):
    for b in range(len(x.bot_choices[a])):
        x.updateGrid(1, x.bot_choices[a][b], 3)
#print(x.gridBot)
print(x.gridPlayer)
print("You will get 3 shots every turn")
bot_guesses = []
users_turn = True
bot_turn = True
while gameOngoing == True:
    num_turns = 0
    while users_turn == True:
        try:
            game_choice = int(input("""Enter-
    1: Take  chance
    2: View your board
    3: view your hits on opponents board
    Choice: """))
        except ValueError:
            print('Please enter a correct value!')
            continue
        if game_choice == 1:
            print("Here are your shots on opponents board:")
            print(x.gridBotVisible)
            pattern = re.compile("[A-F]+[1-6]")
            correct_input = False
            while correct_input == False:
                shot_location = input("Please enter location on board such as A1, B2 etc: ")
                if bool(pattern.match(shot_location)):
                    hit = x.takeShot(shot_location)
                    num_turns += 1
                    correct_input = True
            print(x.gridBotVisible)
            if hit:
                print("You successfully hit a boat!")
            else:
                print("You missed! Better luck next time!")
            print("Turn " + str(num_turns) + " of 3")
        elif game_choice == 2:
            print(x.gridPlayer)
        elif game_choice == 3:
            print(x.gridBotVisible)
        if num_turns == 3:
            users_turn = False
            bot_turn = True
        if "*" not in x.gridBot:
            print("Game over! You win!")
            gameOngoing = False
            break
    if gameOngoing == True:
        print("Bot's turn now!")
    num_turns = 0
    while bot_turn == True:
        time.sleep(1.5)
        bot_guess_unique = False
        while bot_guess_unique == False:
            guess = chr(65+randint(0, 5)) + str(randint(1, 6))
            if guess not in bot_guesses:
                bot_guesses.append(guess)
                bot_guess_unique = True
        hit = x.takeShotBot(guess)
        if hit:
            print("Bot shot at " + guess + " and hit your ship!")
        else:
            print("Bot shot at " + guess + " and missed!")
        num_turns += 1
        if num_turns == 3:
            bot_turn = False
            users_turn = True
    print(x.gridPlayer)
    if "*" not in x.gridPlayer:
        print("Game over! You lose :( Here is the bot's map:")
        print(x.gridBot)
        gameOngoing = False

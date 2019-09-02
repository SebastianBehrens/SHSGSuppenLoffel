# Minesweeper group project

'''
1. Create playground
1.1 Create a grid (user input)
1.2 Define number of bombs (user input // maybe: with limits)
1.3 Randomly distrubute bombs over the grid

2. Define the rules
2.1 Game ends as soon as you hit a mine
2.2 Game proceeds if you hit an empty field
2.3 A number in a field describes the number of mines which are in the 8 surrounding fields

3. Beeing able to play the game (maybe by putting in the number)

4. Make it looking fancy (add syntactic sugar)
'''

import random

#Code to start the game by user input
def play_game():
    print ('Hello to Minecraft by the Suppenloffels.')
    play_game = input('When you are ready to start the game type "P"')
    if play_game == 'P':
        print("Perfect, let's start playing!")
        empty_grid = create_grid(int(input('How large do you prefer your field to be?')))
        ready_grid = add_mines(empty_grid,int(input('How many bombs do you want to place in your field?')))
        print_game(ready_grid)
    else:
        print ('Your input is invalid. Please type "P" to start the game.')
        play_game()
        return



#create a row of cells
def create_row(number_of_cells):
    new_row = []
    for i in range(number_of_cells):
        new_row.append('0')
    return new_row

#create a list of rows
def create_grid(a_size):
    a_grid = []
    for i in range(a_size):
        new_row = create_row(a_size)
        a_grid.append(new_row)
    return a_grid

# Add mines randomized over the grid
# maybe define it, so that it checks if there is already a bomb in the field (not done yet)
def add_mines(a_grid,max_number_of_mines):
     count = 0
     max_count = max_number_of_mines
     if count < max_count:
        for i in range(max_number_of_mines):
            a_grid[random.randint(0,len(a_grid[0])-1)][random.randint(0,len(a_grid[0])-1)] = '*'
            count +=1
        return a_grid

# Function for printing the grid
def print_game (a_grid):
    for some_list in a_grid:
        for element in some_list:
            print(element, end=' | ')
        print("")


play_game()
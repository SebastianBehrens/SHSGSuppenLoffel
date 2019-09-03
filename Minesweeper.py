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
#create a row of empty cells
def create_empty_row(number_of_cells):
    new_empty_row = []
    for i in range(number_of_cells):
        new_empty_row.append('-')
    return new_empty_row

#create an empty list of rows
def create_empty_grid(a_size):
    a_empty_grid = []
    for i in range(a_size):
        new_empty_row = create_empty_row(a_size)
        a_empty_grid.append(new_empty_row)
    return a_empty_grid

def print_empty_game (a_empty_grid):
    for some_list in a_empty_grid:
        for element in some_list:
            print(element, end=' | ')
        print("")

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


# Define the list of bombs

# def list_bombs (a_grid):
#     for rows in range(len(a_grid)-1):
#         for colums in rows:
#             if colums == '*':
#                 position_of_bombs = []
#                 position_of_bombs.append(a_grid.index('*'))


# play_game()

def position_of_bombs(a_grid):
    pos_bombs = []
    for rowInd, rowItem in enumerate(a_grid):
        [pos_bombs.append([rowInd, colInd]) for colInd, colItem in enumerate(rowItem) if colItem == '*']
    return pos_bombs

# Define the numbers surrounding the bombs
def compute_numbers_in_grid(grid):
    nRow = len(grid)
    nCol = len(grid[0])
    createMatrix = []
    for i in range(nRow):
        for j in range(nCol):
            currentState = grid[i][j]
            neighbourCells = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i,j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
            toBeDeleted = []
            for ind, pair in enumerate(neighbourCells):
                if pair[0] < 0 or pair[0] > nRow - 1:
                    toBeDeleted.append(ind)
                if pair[1] < 0 or pair[1] > nCol -1:
                    toBeDeleted.append(ind)
            neighbourCellsToCheck = [i for j, i in enumerate(neighbourCells) if j not in toBeDeleted]
            neighbourCount = 0
            for pair in neighbourCellsToCheck:
                if grid[pair[0]][pair[1]] == '*':
                    neighbourCount += 1
            createMatrix.append([i, j, neighbourCount, currentState])
    return createMatrix





def create_neighbour_count_grid(neighbourCountMatrix):
    neighbourCountGrid = create_empty_grid(int(len(neighbourCountMatrix)**.5))
    for neighbourquadruplet in neighbourCountMatrix:
        indRow = neighbourquadruplet[0]
        indCol = neighbourquadruplet[1]
        neighbours = neighbourquadruplet[2]

        neighbourCountGrid[indRow][indCol] = neighbours

    return neighbourCountGrid

def play_round(display_grid, numbers_in_grid, bomb_grid):
    print(display_grid)
    a = input('Where do you want to klick?')
    i, j = a.split(' ')
    compute_reveal(numbers_in_grid, display_grid, bomb_grid, int(i), int(j))


#Code to start the game by user input
def look_in_neighbours(i, j):
    neighbourCells = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j-1], [i,j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
    return neighbourCells

def compute_reveal(numbers_in_grid, display_grid, bomb_grid, i, j ):
    if bomb_grid[i][j] == '*':
        print_game('You lost.')
        # exit() to break the course of the game
    else:
        if numbers_in_grid[i][j] == 0:
            for i in look_in_neighbours(i, j):
                if numbers_in_grid[i] == 0:
                    compute_reveal(numbers_in_grid, display_grid, bomb_grid, i, j)
        else:
            display_grid[i][j] = numbers_in_grid[i][j]
        print_game(display_grid)













def play_game():
    print ('Hello to Minecraft by the Suppenloffels.')
    play_game = input('When you are ready to start the game type "P"')
    if play_game == 'P':
        print("Perfect, let's start playing!")
        size = int(input('How large do you prefer your field to be?'))
        difficulty = str(input('At which level of difficulty do you want to play (l=low,m=medium,h=high)'))
        if difficulty == "l":
            severity = 0.2
        if difficulty == "m":
            severity = 0.4
        if difficulty == "h":
            severity = 0.7
        empty_grid = create_grid(size)
        ready_grid = add_mines(empty_grid,int(severity*size*size))
        print_game(ready_grid)
        empty_grid = create_empty_grid(size)
        print_empty_game(empty_grid)
        print(position_of_bombs(ready_grid))
        compute_numbers_in_grid(ready_grid)

        play_round(empty_grid,
        create_neighbour_count_grid(compute_numbers_in_grid(ready_grid)),
        ready_grid)


    else:
        print ('Your input is invalid. Please type "P" to start the game.')
        play_game()
        return



play_game()

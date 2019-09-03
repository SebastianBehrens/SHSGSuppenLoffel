import random
#create a row of empty cells
def print_game (a_grid):
    header_indices = ['   ', ] + list(range(len(a_grid)))
    row_indices = list(range(len(a_grid)))
    for head_index in header_indices:
        print(head_index, end = ' | ')
    print('\n')
    row_count = 0
    for some_list in a_grid:

        print(row_indices[row_count], end = ' |   ')
        row_count += 1
        for element in some_list:
            print(element, end=' | ')
        print("")

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

#  for the bombs
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


def add_mines(a_grid,max_number_of_mines):
     count = 0
     if count < max_number_of_mines:
        for i in range(max_number_of_mines):
            bomb_i_ind = random.randint(0,len(a_grid[0])-1)
            bomb_j_ind = random.randint(0,len(a_grid[0])-1)
            a_grid[bomb_i_ind][bomb_j_ind] = '*'
            count +=1
        return a_grid

#
# def position_of_bombs(a_grid):
#     pos_bombs = []
#     for rowInd, rowItem in enumerate(a_grid):
#         [pos_bombs.append([rowInd, colInd]) for colInd, colItem in enumerate(rowItem) if colItem == '*']
#     return pos_bombs

# unsure about use


def compute_numbers_grid(grid):
    nRow = len(grid)
    nCol = len(grid[0])
    list_of_neighbour_numbers = []
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
            list_of_neighbour_numbers.append([i, j, neighbourCount, currentState])

    numbers_grid = create_empty_grid(int(len(list_of_neighbour_numbers)**.5))
    for neighbourquadruplet in list_of_neighbour_numbers:
        indRow = neighbourquadruplet[0]
        indCol = neighbourquadruplet[1]
        neighbours = neighbourquadruplet[2]

        numbers_grid[indRow][indCol] = neighbours

    return numbers_grid


def startGame():
    print ('Hello to Minecraft by the Suppenloffels.')
    if True: # once asked for P now executes regardless.
        print("Perfect, let's start playing!")
        size = int(input('How large do you prefer your field to be?'))
        difficulty = str(input('At which level of difficulty do you want to play (l=low,m=medium,h=high)'))
        if difficulty == "l":
            severity = 0.2
        if difficulty == "m":
            severity = 0.4
        if difficulty == "h":
            severity = 0.7
        display_grid = create_empty_grid(size)
        bomb_grid = add_mines(create_empty_grid(size), int(severity*(size**2)))
        numbers_grid = compute_numbers_grid(bomb_grid)


    return display_grid, bomb_grid, numbers_grid

opened_up_zeros = []
def reveal(i, j, number_grid, display_grid):
    nRow = len(number_grid)
    nCol = len(number_grid[1])

    neighbourCells = [[i-1, j-1], [i-1, j], [i-1, j+1], [i, j], [i, j-1], [i,j+1], [i+1, j-1], [i+1, j], [i+1, j+1]]
    toBeDeleted = []
    for ind, pair in enumerate(neighbourCells):
        if pair[0] < 0 or pair[0] > nRow - 1 or pair[1] < 0 or pair[1] > nCol -1:
            toBeDeleted.append(ind)
        else:
            continue
        # if pair[1] < 0 or pair[1] > nCol -1:
        #     toBeDeleted.append(ind)


    to_be_revealed = [i for j, i in enumerate(neighbourCells) if j not in toBeDeleted]
    for reveal_pair in to_be_revealed:
        display_grid[reveal_pair[0]][reveal_pair[1]] = number_grid[reveal_pair[0]][reveal_pair[1]]
        if display_grid[reveal_pair[0]][reveal_pair[1]] == 0:
            if reveal_pair in opened_up_zeros:
                continue
            else:
                opened_up_zeros.append(reveal_pair)

                ### the recursive problem
                reveal(reveal_pair[0], reveal_pair[1], number_grid, display_grid)





def playRound(display_grid, bomb_grid, number_grid):
    print_game(number_grid)
    print_game(display_grid)
    # print('next bomb grid\n_____')
    # print_game(bomb_grid)
    # print('next bomb \n_____')
    # print_game(number_grid)
    # print('next numb \n_____')
    # exit()

    klick_input = input('Where do you want to klick?')
    i, j = klick_input.strip().split(' ')
    # i, j = a.split(' ')
    i = int(i)
    j = int(j)

    if bomb_grid[i][j] == '*':
        print('You lost. Game Over.')
        exit()  # to be determined (tested with and without)

    else:
        if number_grid[i][j] == 0:
            # print('The clicked field would trigger the expansion reveal')
            print_game(number_grid)
            reveal(i, j, number_grid, display_grid)
            # for reveal_pair in revealed:
            #     display_grid[reveal_pair[0]][reveal_pair[1]] = number_grid[reveal_pair[0]][reveal_pair[1]]
            print_game(display_grid)

        else:
            display_grid[i][j] = number_grid[i][j]
            # print_game(display_grid)






        # display_grid = # overwritten grid to display (with reveaal)

# my_disp, my_bomb, my_numb = startGame()
#
# playRound(my_disp, my_bomb, my_numb)

def playGame(round):
    if round == 1:
        round += 1
        my_disp, my_bomb, my_numb = startGame()
        playRound(my_disp, my_bomb, my_numb)

    while round > 1:
        playRound(my_disp, my_bomb, my_numb)


playGame(1)

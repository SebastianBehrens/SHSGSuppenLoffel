def play_game():
    print ('Hello to Minecraft by the Suppenloffels.')
    play_game = input('When you are ready to start the game type "P"')
    if play_game == 'P':
        print("Perfect, let's start playing!")
        empty_grid = create_empty_grid(int(input('How large do you prefer your field to be?')))

        print_empty_game(empty_grid)
        
    else:
        print ('Your input is invalid. Please type "P" to start the game.')
        play_game()
        return
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

play_game()


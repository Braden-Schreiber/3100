import random
import time
import tkinter


""" 
Legend: 
"." = empty space 
"0" = part of ship 
"X" = part of ship hit with bullet, a hit
"#" = empty space shot with bullet, a miss
"""

# 2D array for gird 
grid = [[]]

grid_size = 10 

num_of_ships = 5 

bullets_left = 50 

game_over = False 

num_of_ships_sunk = 0 

ship_positions = [[]] 

alphabet = "ABCDEFGHIJKLMNOPQRSTUVXYZ" 

def validate_grid_and_place_ship(start_row, end_row, start_col, end_col): 
    #check row or column to see if it is safe for ship to be placed
    #return true or false
    global grid 
    global ship_positions 

    #check that all positions are empty space
    all_valid = True
    for r in range(start_row, end_row):
        for c in range(start_col, end_col):
            if grid[r][c] != ".":
                all_valid = False
                break
    
    #if all positions are valid, add a ship 
    if all_valid:
        ship_positions.append([start_row, end_row, start_col, end_col])
        for r in range(start_row, end_row):
            for c in range(start_col, end_col):
                grid[r][c] = "O"
    return all_valid

def try_to_place_ship_on_grid(row, col, direction, length): 
    #based on direction will call helper method to try and place a ship on the grid
    #returns validate_grid_and_place_ship which will be true or false
    global grid_size 

    start_row, end_row, start_col, end_col = row, row + 1, col, col + 1
    
    #check to make sure the ship does not go out on the left side of the grid 
    if direction == "left":
        if col - length < 0:
            return False
        start_col = col - length + 1

    #check to make sure the ship does not go out on the right side of the grid
    elif direction == "right":
        if col + length >= grid_size:
            return False
        end_col = col + length

    #check to make sure the ship does not go out on the top side of the grid
    elif direction == "up":
        if row - length < 0:
            return False
        start_row = row - length + 1

    #check to make sure the ship does not go out on the bottom side of the grid
    elif direction == "down":
        if row + length >= grid_size:
            return False
        end_row = row + length

    return validate_grid_and_place_ship(start_row, end_row, start_col, end_col)

def create_grid(): 
    #create 10x10 grid and randomly pace down ships of different sizes in different directions 
    #does not return but will use try_to_place_ship_on_grid

    global grid 
    global grid_size 
    global num_of_ships 
    global ship_positions 
    
    #make randomness based on when you run the program
    random.seed(time.time())

    rows, cols = (grid_size, grid_size)

    #create the 2D array
    grid = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(".")
        grid.append(row)

    num_of_ships_placed = 0

    ship_positions = []

    #place ship anywhere on the grid 
    while num_of_ships_placed != num_of_ships:
        random_row = random.randint(0, rows - 1)
        random_col = random.randint(0, cols - 1)
        direction = random.choice(["left", "right", "up", "down"])
        ship_size = random.randint(3, 5)
        if try_to_place_ship_on_grid(random_row, random_col, direction, ship_size):
            num_of_ships_placed += 1

def print_grid(): 
    #will print the grid with rows A-J and columns 0-9 
    #no return

    global grid 
    global alphabet 

    debug_mode = True

    #slice the alphabet based on num of rows
    alphabet = alphabet[0: len(grid) + 1]

    #print 2D array
    for row in range(len(grid)):
        print(alphabet[row], end=") ")
        for col in range(len(grid[row])):
            if grid[row][col] == "O":
                if debug_mode:
                    print("O", end=" ")
                else:
                    print(".", end=" ")
            else:
                print(grid[row][col], end=" ")
        print("")

    #print numbers for each column 
    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end=" ")
    print("")

def accept_valid_bullet_placement(): 
    #will get valid row and column to place bullet shot 
    #return integers row, col 

    global alphabet 
    global grid 

    #input sanitization: 
    is_valid_placement = False
    row = -1
    col = -1
    while is_valid_placement is False:
        placement = input("Enter row (A-J) and column (0-9) such as A3: ")
        placement = placement.upper()

        #user should only enter 2 characters 
        if len(placement) <= 0 or len(placement) > 2:
            print("Error: Please enter only one row and column such as A3")
            continue #reset back to the start of the loop
       
        #set row to the letter and the column to the number
        row = placement[0]
        col = placement[1]
        if not row.isalpha() or not col.isnumeric():
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue
        row = alphabet.find(row)
        if not (-1 < row < grid_size):
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue
        col = int(col)
        if not (-1 < col < grid_size):
            print("Error: Please enter letter (A-J) for row and (0-9) for column")
            continue

        #bullet was already shot in that place
        if grid[row][col] == "#" or grid[row][col] == "X":
            print("You have already shot a bullet here, pick somewhere else")
            continue

        #valid input
        if grid[row][col] == "." or grid[row][col] == "O":
            is_valid_placement = True

    return row, col

def check_for_ship_sunk(row, col): 
    #if entire ship is sunk, incrememnt ships sunk
    #returns true or false 

    global ship_positions 
    global grid 

    #based where bullet was last shot 
    for position in ship_positions:
        start_row = position[0]
        end_row = position[1]
        start_col = position[2]
        end_col = position[3]
        if start_row <= row <= end_row and start_col <= col <= end_col:
            # Ship found, now check if its all sunk
            for r in range(start_row, end_row):
                #if all "X", then ship is sunk 
                for c in range(start_col, end_col):
                    if grid[r][c] != "X":
                        return False
    return True

def shoot_bullet(): 
    #updates grid and ships based on wherer the bullet was shot 
    #uses accept_valid_bullet_placement
    #no return

    global grid 
    global num_of_ships_sunk 
    global bullets_left 

    row, col = accept_valid_bullet_placement()
    print("")
    print("----------------------------")

    #determine what the user hit
    if grid[row][col] == ".":
        print("You missed, no ship was shot")
        grid[row][col] = "#"
    elif grid[row][col] == "O":
        print("You hit!", end=" ")
        grid[row][col] = "X"
        if check_for_ship_sunk(row, col):
            print("A ship was completely sunk!")
            num_of_ships_sunk += 1
        else:
            print("A ship was shot")

    #decrement bullets by 1 every time
    bullets_left -= 1

def check_for_game_over(): 
    #if all ships have been sunk or you run out of bullets its game over
    #no return 

    global num_of_ships_sunk 
    global num_of_ships 
    global bullets_left 
    global game_over 

    #user wins
    if num_of_ships == num_of_ships_sunk:
        print("Congrats you won!")
        game_over = True

    #user loses, ran out of bullets
    elif bullets_left <= 0:
        print("Sorry, you lost! You ran out of bullets, try again next time!")
        game_over = True 

def main(): 
    #main entry point of application that runs game loop 
    #uses create_grid, print_grid, shoot_bullet, and check_for_game_over
    #no return 

    global game_over

    print("-----Welcome to Battleships-----")
    print("You have 50 bullets to take down 8 ships, may the battle begin!")

    create_grid()

    while game_over is False:
        print_grid()
        print("Number of ships remaining: " + str(num_of_ships - num_of_ships_sunk))
        print("Number of bullets left: " + str(bullets_left))
        shoot_bullet()
        print("----------------------------")
        print("")
        check_for_game_over()

if __name__ == '__main__': 
    #will only be called when the program is run from terminal or IDE like PyCharm
    main()

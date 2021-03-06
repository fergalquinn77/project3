import random
import gspread
from google.oauth2.service_account import Credentials
from art import *
from colored import fg, bg, attr

"""
    Battleships

    How it works:

    1. User inputs the grid size (min-max of 10 & 15)
    2. There will be 5 types of ships (10 ships in total)
        - Carrier (Size 5 squares) x 1 [C1]
        - Battleship (Size 4 squares) x 2 [B1, B2]
        - Destroyer (Size 3 squares) x 3 [D1, D2, D3]
        - Patrol Boat (Size 2 squares) x 4 [P1, P2, P3, P4]
    3. Fixed number of bombs - 50.
    4. User gives grid co-ordinates to drop bomb
    5. Object of game is to destroy all ships before running out of bombs

    Legend
    '~' = Water
    'S' = Part of ship
    '#' = Water hit by bomb
    'X' = Part of ship hit by bomb

"""

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("project-3-battleships")

num_ships = 10
bombs_left = 50
grid = []
num_ships_sunk = 0
grid_size = 10
ship_sizes = {
    'c1': 5, 'b1': 4, 'b2': 4, 'd1': 3, 'd2': 3,
    'd3': 3, 'p1': 2, 'p2': 2, 'p3': 2, 'p4': 2}

ship_lives_remaining = {
    'c1': 5, 'b1': 4, 'b2': 4, 'd1': 3,
    'd2': 3, 'd3': 3, 'p1': 2, 'p2': 2,
    'p3': 2, 'p4': 2}

ships_remaining = 10
game_over = False
USER_NAME = ""
ship_names = {
    'c1': 'Carrier USS Langley',
    'b1': 'Battleship USS Texas',
    'b2': 'Battleship USS Iowa',
    'd1': 'Destroyer USS Manley',
    'd2': 'Destroyer USS Wickes',
    'd3': 'Destroyer USS Philip',
    'p1': 'Patrol Ship USS Cyclone',
    'p2': 'Patrol Ship USS Hurricane',
    'p3': 'Patrol Ship USS Monsoon',
    'p4': 'Patrol Ship USS Sirocco'}
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
test_mode = False


def get_grid_size():
    """
    This function gets the grid size from the user.
    """
    global grid_size
    global USER_NAME
    USER_NAME = input("Please enter your name: \n")
    while True:
        grid_size = input("Please enter the grid size between 8 & 15: \n")
        if not grid_size.isnumeric():
            print("You did not enter a valid integer")
            continue
        if int(grid_size) < 8 or int(grid_size) > 15:
            print("Grid size needs to be between 8 & 15")
            continue
        grid_size = int(grid_size)
        break


def create_initial_grid():
    """
    Create the initial grid that contains water '~'
    throughout.
    """
    for r in range(grid_size):
        row = []
        for c in range(grid_size):
            row.append("~")
        grid.append(row)


def spacing(col):
    """
    Adjusts the space between colums on grid.
    """
    two_spaces = "  "
    three_spaces = "   "
    if col < 10:
        return two_spaces
    else:
        return three_spaces


def print_grid_display(grid):
    """
    Display/print the grid. Option to show ships for
    testing purposes
    """
    global alphabet
    alphabet = alphabet[0: grid_size]

    for row in range(grid_size):
        print(alphabet[row], end=") ")
        color = fg('blue')
        color_miss = fg('yellow')
        color_hit = fg('red')
        reset = attr('reset')
        for col in range(len(grid[row])):
            if len(grid[row][col]) > 1:
                if test_mode:
                    print(grid[row][col], end=" ")
                else:
                    print(color + "~" + reset, end=spacing(col))
            else:
                if(grid[row][col] == '#'):
                    print(
                        color_miss + grid[row][col] + reset, end=spacing(col))
                    reset = attr('reset')
                elif(grid[row][col] == 'X'):
                    print(color_hit + grid[row][col] + reset, end=spacing(col))
                    reset = attr('reset')
                else:
                    print(color + grid[row][col] + reset, end=spacing(col))
                    reset = attr('reset')

        print("")

    print("  ", end=" ")
    for i in range(len(grid[0])):
        print(str(i), end="  ")
    print("")


def check_ship_fits(length, start_row, start_col, direction):
    """
    When positioning ships in grid - check to see if the ship fits on grid.
    Ships are positioned randomly - they cannot be positioned if they are
    off the grid. Once the ship fits - it then checks whether there is clear
    water to position the ship.
    """
    if direction == 'north':
        if(start_row-(length-1) >= 0):
            return check_clear_water(length, start_row, start_col, direction)
        else:
            return False

    if direction == 'south':
        if(start_row+(length-1) <= grid_size-1):
            return check_clear_water(length, start_row, start_col, direction)
        else:
            return False

    if direction == 'east':
        if(start_col+(length-1) <= grid_size-1):
            return check_clear_water(length, start_row, start_col, direction)
        else:
            return False

    if direction == 'west':
        if(start_col-(length-1) >= 0):
            return check_clear_water(length, start_row, start_col, direction)
        else:
            return False


def check_clear_water(length, start_row, start_col, direction):
    """
    Check when positioning ships, that there are no other ships in the way.
    This function is used in the check_ship_fits function once it determines
    that the ship can fit.
    """
    if direction == 'north':
        non_water = 0
        for position in range(length):
            if grid[start_row-position][start_col] != '~':
                non_water += 1
        if non_water == 0:
            return True
        else:
            return False

    if direction == 'south':
        non_water = 0
        for position in range(length):
            if grid[start_row+position][start_col] != '~':
                non_water += 1
        if non_water == 0:
            return True
        else:
            return False

    if direction == 'west':
        non_water = 0
        for position in range(length):
            if grid[start_row][start_col-position] != '~':
                non_water += 1
        if non_water == 0:
            return True
        else:
            return False

    if direction == 'east':
        non_water = 0
        for position in range(length):
            if grid[start_row][start_col+position] != '~':
                non_water += 1
        if non_water == 0:
            return True
        else:
            return False


def position_ships(length, boat):
    """
    Used to position an individual ship on grid. Choose the position randomly.
    Then check it fits using the check_ship_fits and that there is clear water
    using check_clear_water. Once it passes both these - the ships can be
    positioned and the grid is updated using the place_ship function.
    """
    position_ship_possible = False

    while position_ship_possible is False:
        direction = random.choice(('north', 'south', 'east', 'west'))
        start_row = random.randint(0, grid_size-1)
        start_col = random.randint(0, grid_size-1)
        position_ship_possible = check_ship_fits(
            length, start_row, start_col, direction)

    place_ship(length, start_row, start_col, direction, boat)


def position_ships_on_grid():
    """
    Loop through all ships to position on grid.
    """
    for key, value in ship_sizes.items():
        position_ships(value, key)


def place_ship(length, start_row, start_col, direction, boat):
    """
    Once passed tests - place the ship i.e. update the grid.
    """
    if(direction == 'north'):
        for position in range(length):
            grid[start_row-position][start_col] = boat
    elif(direction == 'south'):
        for position in range(length):
            grid[start_row+position][start_col] = boat
    elif(direction == 'east'):
        for position in range(length):
            grid[start_row][start_col+position] = boat
    elif(direction == 'west'):
        for position in range(length):
            grid[start_row][start_col-position] = boat


def get_bomb():
    """
    Get co-ordinates from user for positioning bomb. Run validity checks
    and then pass the co-ordinates on the position_bomb function.
    """
    global alphabet
    msg_get_position = (
        f'Enter row (A-{alphabet[grid_size-1]}) and column (0-{grid_size})'
        f' such as G7: '
        )
    alphabet = alphabet[0: grid_size]
    within_grid = False
    while within_grid is False:
        msg_bombs_left = (
            f'You have {bombs_left} bombs left and '
            f'have sunk {num_ships_sunk} ships so far'
            )
        print(msg_bombs_left)
        position_bomb = input(msg_get_position)
        position_bomb = position_bomb.upper()
        if len(position_bomb) == 2:
            row = position_bomb[0]
            col = position_bomb[1]
        elif len(position_bomb) == 3:
            row = position_bomb[0]
            col = position_bomb[-2:]
        else:
            print("Error: Please enter only one row and column such as A3")
            continue
        if (not col.isnumeric()):
            print("Error: Invalid entry")
            continue
        if (not row.isalpha()):
            print("Error: Invalid entry")
            continue
        col = int(col)
        if (row not in alphabet) or (not 0 <= col <= grid_size-1):
            print("Error: Your choice was off the grid")
            continue
        row = alphabet.find(row)
        if (grid[row][col] == "#" or grid[row][col] == "X"):
            print("Error: You have already thrown a bomb here")
            continue
        if (grid[row][col] == "~" or len(grid[row][col]) == 2):
            within_grid = True

    return row, col


def check_ship_sunk(ship):
    """
    Check if a ship is sunk after a hit. This function is called
    in the place_bomb function.
    """
    global ships_remaining
    global num_ships_sunk
    if ship_lives_remaining[ship] == 0:
        ships_remaining -= 1
        num_ships_sunk += 1
        color_ship_sunk = fg('red')
        reset = attr('reset')
        print(color_ship_sunk + 'You sunk the', ship_names[ship] + reset)
        reset = attr('reset')


def place_bomb():
    """
    Once valid co-ordinates are entered by user in get_bomb function, this
    function checks whether it's a hit or miss. Updates the grid accordingly.
    """
    global bombs_left
    row, col = get_bomb()
    if (grid[row][col] == "~"):
        grid[row][col] = "#"
        message = text2art("YOU  MISSED")
        print(message)
    else:
        ship_hit = grid[row][col]
        ship_lives_remaining[ship_hit] -= 1
        grid[row][col] = "X"
        message = text2art("YOU  HIT  A  SHIP")
        print(message)
        check_ship_sunk(ship_hit)
    bombs_left -= 1


def check_game_over():
    """
    Checks if game is over (either bombs have run out or all ships have#
    been sunk).
    """
    global game_over
    if bombs_left == 0 or num_ships_sunk == 10:
        game_over = True
        game_over_message = text2art("GAME  OVER")
        print(game_over_message)
        record_game_stats()


def reset_grid():
    """
    Resets the grid to be all water before positioning ships
    """
    for r in range(grid_size):
        for c in range(grid_size):
            grid[r][c] = "~"


def reset_game():
    """
    If user chooses to restart game at end, this resets the grid and resets
    the stats
    """
    global num_ships_sunk
    global bombs_left
    game_over = False
    reset_grid()
    bombs_left = 50
    num_ships_sunk = 0
    position_ships_on_grid()
    print_grid_display(grid)
    while game_over is False:
        place_bomb()
        print_grid_display(grid)
        check_game_over()


def start_new_game():
    """
    Executes at end of game. Asks user if they'd like to start a new game.
    """
    while True:
        start_game_inp = input("Would you like to start again? Enter [Y/N]: ")
        start_game_inp = start_game_inp.upper()
        if(start_game_inp == "Y"):
            reset_game()
            break
        elif(start_game_inp == "N"):
                print("Thank you for playing Battleships!")
                break
        else:
            print("Invalid entry - please try again")


def record_game_stats():
    """
    Record game stats to google spreadsheet when game is over.
    Provide feedback to user on how they did.
    """
    player_score = num_ships_sunk*grid_size
    user_stats = [bombs_left, num_ships_sunk, USER_NAME, player_score]
    print("Let's see how you did...\n")
    battleships_worksheet = SHEET.worksheet("battleships")
    all_user_stats = SHEET.worksheet("battleships").get_all_values()
    number_players = len(all_user_stats)-1
    best_score = 0
    for i in range(1, len(all_user_stats)):
        if int(all_user_stats[i][3]) > best_score:
            best_score = int(all_user_stats[i][3])
            best_score_user = all_user_stats[i][2]
    print(
        "The top score to date out of",
        number_players, "players to date is", best_score,
        "by", best_score_user
        )
    print("You scored ", player_score)
    if(player_score > best_score):
        print("Congrats, you are the new leader")
        battleships_worksheet.append_row(user_stats)
        start_new_game()
    else:
        print("Maybe try again to get the top score!")
        battleships_worksheet.append_row(user_stats)
        start_new_game()


def main():
    """
    Main function for program
    """
    global game_over
    intro = text2art("Battleships")
    print(intro)
    msg = 'You get the choose the grid size - the higher, the more difficult.'\
        + ' You get 50 bombs'
    print(msg)
    print("There are 10 ships in ranging in size from 2 to 5")
    get_grid_size()
    create_initial_grid()
    position_ships_on_grid()
    print_grid_display(grid)
    while game_over is False:
        place_bomb()
        print_grid_display(grid)
        check_game_over()

main()

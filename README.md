# PORTFOLIO PROJECT - 3

# BATTLESHIPS

## PURPOSE

'Battleships' is the well known game which is strategy type guessing game. It is played on ruled grids (paper or board) on which each player's fleet of warships are marked. The locations of the fleets are concealed from the other player. Players alternate turns calling "shots" at the other player's ships, and the objective of the game is to destroy the opposing player's fleet.

The project has been developed using the Python programming language.

* Here is a link to the [final project](https://battleshipscifq.herokuapp.com/)
.

#  


## USER STORIES

* As a User, I want the game that I can set the difficulty
* As a User, I want the option to see how many bombs I've left and how many ships are sunk
* As a User, I want to see how I performed compared to other users
* As a User, I want the option to play again

## FEATURES

* The game features are:
    * The user plays against a computer. The computer has 10 ships that are positioned randomly on the grid
    * The user has 50 bombs to use in the game
    * The user can set the level of difficulty by the size of the grid system. This is inputted at the start of game. The lower the grid-size, the easier the game.
    * The ship names are actual USS ship names
    * The game is over when the user runs out of bombs or all ships are sunk (whichever is first)
    * The users score is recorded and they get feedback on whether they got the top score or not

### Gameplay components:
#### User vs Computer

* A terminal with the title `Battleships` and `Enter your name:`

![Enter Name](docs/images/name_input.jpg)

* Once the User name has been entered, the User is then asked `Please enter the grid size between 8 & 15:`

![Grid Size](docs/images/enter_name.jpg)

* Once the user enters the grid size - they are presented with the grid with ships hidden.

![Grid Display](docs/images/grid_display.jpg)


* The game starts with by the user entering the co-ordinates of where they want to drop the first bomb. There are various checks on the inputted co-ordinates like whether the row is a [letter and column is a number](docs/images/invalid_entry.jpg). It also checks whether a bomb has been thrown at that co-ordinate before and [prompts user for another position](docs/images/already_thrown_a_bomb.JPG) if it has. 

* If the user [hits a ship](docs/images/ship_hit.jpg), a message is displayed and the co-ordinate is marked with an 'X' in red font. If the user [misses a ship](docs/images/missed-ship.jpg), a message is displayed and the co-ordinate is marked with an '#' in yellow font.

* If the User sinks a ships, the ship name is displayed. 

![Ship name](docs/images/you_sunk_a_ship.JPG)

* The game finishes when the user either runs out of bombs or sinks all ships (whichever comes first). Then the user is provided feedback on how they did compared to users to date.

![game over](docs/images/game_over_message.jpg)


### Future features:

* Let the user choose the number of ships - this can increase the level of difficulty further.
* Introduce a 'super bomb' that can wipe out one cell and all surrounding cells at a time (up to 9 cells). The user will have one 'super bomb'
* At present, the user is advised at game end as to whether they got top score or not. I would like to have a leader-board of the top ten scores


### Images

* There is one background image, for aesthetics only
    [Ultra Board Games](https://www.ultraboardgames.com/battleship/gfx/banner.jpg)

### Typography

* The project uses the [Art](https://pypi.org/project/art/) and [Colored](https://pypi.org/project/colored/) libraries for the ascii art and font color
* Otherwise, Standard terminal font, cannot be changed
# 

# TESTING

## User story testing

* `As a User, I want the game that I can set the difficulty`:
    *  On starting the game, the user is asked to provide a grid size with the note that `You get the choose the grid size - the higher, the more difficult.`. 
* `As a User, I want the option to see how many bombs I've left and how many ships are sunk`:
    * The user is displayed with the following message at the start of game - `You have 50 and have sunk 0 ships so far`. The message is updated after each bomb is used 
* `As a User, I want to see how I performed compared to other users`:
    * At the end of the game, the user scores is calculated using the following formula - score = number of ships sunk x grid size. This adjusts the users score for difficulty
    * The users score is then compared to all previous users and they are informed whether they got the top score or not 
* `As a User, I want the option to play again`:
    * I have provided an option at the end of the game that asks 
        `Would you like to start a new game? Enter [Y/N]:`
        * If the User inputs `Y`, the game restarts and the grid is 
        the User vs AI with the original input difficulty. 
        * If the User inputs `N` the game ends with a message 
        `Thank you for playing Battleships!`.

## Validation
### PEP8 Online Validation

<details>
<summary>PEP8 Screenshot Results for game run file</summary>
<br>

![PEP8 Results - run.py](docs/images/pep8check.jpg)
</details>

## Manual testing

- Upon loading the game screen terminal and entering their name:
    - The user is asked for the grid-size
        
        ![Grid Size](docs/images/grid_size.jpg)
    
    - If the using enters a non-numeric entry, the following message displays

        ![Non-Integer](docs/images/non_integer.jpg)

    - If the user enters a number less than 8 or greater than 15 - the following message displays

        ![Grid Entry Error](docs/images/grid_entry_error.jpg)
    
    - Once the game begins, the user is prompted for the co-ordinates for where a bomb is to be placed. There are a number of data entry checks to cover invalid data:
    
        - If incorrect data is entered, a `Error: Invalid Entry` message is displayed
          ![Coordinate incorrect data](docs/images/coordinate_incorrect_entry.jpg)

        - If coordinates are provided off the grid, an `Error: Your choice was off the grid`
            ![Off the grid](docs/images/off_the_grid.jpg)

        - If the user positions a bomb where a bomb has already been placed, a message saying `Error: You have already thrown a bomb here`
            ![bomb already](docs/images/bomb_already_thrown.jpg)
        
    - Once the game is over, the user is asked whether, they'd like to start another game of not - `Would you like to start again? Enter [Y/N]:`
        - If the user enters invalid data - the user will be prompted to enter data again and a message is displayed with `Invalid entry - please try again`
           ![invalid data game end](docs/images/start_game_again_invalid_entry.jpg) 
    
    
## Solved bugs and errors

* Throughout the development of this project, several automated (flake8) errors have been fixed i.e.
    - Indentation errors
    - Undefined variable name
    - Not enough whitespace between functions
    - No new line at end of file
    - Invalid syntax errors
    - Imported but unused errors
    

* Found an issue with entering bomb co-ordinates for grid size greater than 10. This issue was solved by using a split on the list for co-ordinates with length 3 e.g. A10. The split was `col = position_bomb[-2:]`
    
* There were a number of errors showing the on PEP8 validation report that related to the number of characters on a row. These were solved with help from Ed on the Tutor support team and some articles on [codeingem](https://www.codingem.com/formatted-string-in-python/) and [flake8rules](https://www.flake8rules.com/rules/E131.html). 

## Unsolved bugs and errors

* All previously known errors during the development process have been resolved


#
# TECHNOLOGIES

## DEVELOPMENT

* The project was written and tested using [Gitpod](https://gitpod.io/)
* The project uses [Github](https://github.com/) for utilising git version control
* The project was deployed via [Heroku](https://heroku.com/)


## LANGUAGES USED

* The project was written using [PYTHON3](https://en.wikipedia.org/wiki/Python_(programming_language))

## LIBRARIES USED

* Colored
    - This is used to color some of the text. This makes the grid more readable to the user
        
* Art
    - This library was used to create the ASCII art for the title upon loading the game

#
# DEPLOYMENT

## How to fork a repository:

If you need to `FORK` a repository:

1. If you have not already, login in to [GitHub](www.github.com) and go to https://github.com/fergalquinn77/project3.git
2. In the top right corner, click `Fork`
3. The next page will be the forked version of https://github.com/fergalquinn77/project3.git but in your own repository

## How to clone a repository:

If you need to make a clone of this repository:

1. Fork the repository https://github.com/fergalquinn77/project3.git using the steps above
2. Above the file list, click `Code` (Usually green at the top right of the code window)
3. Choose if you want to clone using HTTPS, SSH or GitHub CLI, then click the copy button to the right
4. Open Git Bash
5. Change the directory to where you want your clone to go (your own github)
6. Type `git clone` and then paste the URL you copied in step 4
7. Press `Enter` to create your clone

## Local depolyment:

This project was constructed in Gitpod. These steps will explain how to clone this in your local envirnment. Assuming you have forked or cloned this depository, If you need to make a local clone:

1. Go to Gitpod.io and create and free account
2. Download the chrome or firefox extension
3. Come back to depository and click on green button on top right - this will launch the code in a new workspace, from which you can make any desired edits. Note - you will have exectute the command `pip3 install -r requirements.txt`

## Remote depolyment

### Heroku

* This Game was deployed using [Heroku](https://heroku.com/) with the following the steps:

1. Navigate to [Heroku.com](https://www.heroku.com/) and log-in or create a new account.
2. On the top right hand side, click the 'New' button.
3. Inside the dropdown menu, select 'Create new app'.
4. Create a new name for your app (making sure the name chosen is available) in this case it is `battleshipscifq`.
    App names can only be in lower-case letters, numbers and dashes.
5. Select your region, in this case, `Europe`.
6. Click on the `Create App` button.  
7. This will create your app in Heroku and take you to the [Heroku](https://heroku.com/) dashboard.
8. Navigate to the settings tab and scroll down to the button `Reveal Config vars`.
9. Replace the word `KEY` and enter `PORT` and then replace the word `VALUE` and enter `8000` then click on the `Add` button.
10. Below `Config vars` is `Buildpacks`. Click the `Add Buildpack` button.
11. In the pop up window, select `python` and save changes.
12. Repeat this again but this time selecting `node.js` and save the changes.
13. It is `important` to make sure the buildpacks are in the correct order 
    with `Python` being at the top and `node.js` bottom. If they are not in the correct order, you can drag them into the right order.
14. Next, navigate to the `Deploy` tab at the top left side.
15. Select `Github, 'connect to github'` as the deployment method.
16. Search for the Github Repository in the search field (in this case `Python_PP3`) and click `Search`.
17. When the search is complete, click `connect`.
18. Once your repository is connected to [Heroku](https://heroku.com/), Click the `Enable Automatic Deploys` button for automatic deployment.
19. Alternatively you can manually deploy by selecting a branch to deploy from and clicking `Deploy Branch`.
20. If you choose to `Enable Automatic Deploys`, [Heroku](https://heroku.com/) will build a new version of the app when a change to 
    `gitpod` is pushed to `Github`.  
21. Manual deployment allows you to update the app whenever you click `Deploy Branch`.
    In the case of this project, I chose to `Enable Automatic Deploys` to ensure the code was deployed straight away at each push from `Gitpod`.
22. Once the build process is complete (this can take a few seconds) you will then be able to view the live app by clicking on the button `View`
    below `Your app was successfully deployed`.


#
## CREDITS AND REFERENCES

### IMAGE

* Background image of Battleships - from [Ultra Board Games](https://www.ultraboardgames.com/battleship/gfx/banner.jpg)


#
## ACKNOWLEDGEMENTS:

- I once again made use of the great help from the Code institute Tutor team (Ed and Ger). 
- My tutor Chris Quinn for his continued advice and guideance throughout.


#### RETURN TO THE [TOP](#battleships)
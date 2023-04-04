# Settler-Project

This project is a version of the Settlers "Catan" game written in Python for the team15 Software Engineering Project. The game itself is turn based similar in parts to monopoly but mainly more focused on resources and building roads across the world map. For a detailed explanation of the game rules and concepts please refer to [this](https://www.catan.com/understand-catan/game-rules) document.
# Getting Started
In order to run this on your personal machine be sure to download the repository as a zip file and save on your own machine. Then unzip the folder and open using an IDE of your choice, for example VSCode. Finally run main.py to start the game and display the pygame window from which you can play the game.
# Installing
If you receive 'module not found errors' for modules such as hexgrid and Color etc. when running main.py ensure to run these commands in your terminal (pip is interchangeable with whichever package manager you happen to be using).
```
pip install pygame
pip install Color
pip install pygame
```
# Testing
There are several unit tests that have been written for this project stored inside the testing folder. The tests in the aforementioned files are unit tests that test all functionality of the relevant classes , in order to run these tests follow this instruction:
-  Write the command 
```
pytest 'test_file.py'
```
The terminal will then output the test results detailing how many tests have passed/failed and any accompanying error messages. But if you wish to run all tests at once enter this command into the terminal:
```
pytest
```
## Built using
* [Pygame](https://pypi.org/project/pygame/)- GUI Implementation
* [Hexgrid](https://pypi.org/project/hexgrid/)- Used in the hexagonal board implementation

## Authors
* Morgan Plant
* Eddie Jones
* Yash Magane
* Noah Davy
* Ryan Moss
* Wai Hang Nelson Chan


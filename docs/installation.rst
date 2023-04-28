Getting Started
===============

Pre-Requisites
--------------

Firstly you must ensure that on the system you are using, whether you use a virtual environment or intend to do everything globally, you must not use a python version that is 3.10 or lower as these are the versions that the game has been been tested to work optimally with and if not some packages will not install such as 'rembg'; versions between 3.8 and 3.10 should run with no issues, preferably install version 3.10 in a virtual environment. 

Secondly, from the github repository https://github.com/sussex-Team15/Settler-Project/tree/main, you must download the repository as a zip file to your machine and save in an appropriate location. Alternatively you can just clone the repository and input the link in the appropriate section within your IDE to clone it directly.

Then, in order to install the correct modules run this code in the terminal, however if you use a different package manager than pip, change accordingly.

.. code-block:: text

    pip install -r requirements.txt

Just for reference, this project is structured as a python package,as per convention, where the src folder is the package and therefore the main.py file is a module and needs to be run accordingly, as seen below.

Run Game
--------

To run the game open the terminal inside your IDE or globally on your system and enter the following command to run the main file as a module. For example within VSCode, open a terminal window from the toolbar and enter the below command. Use the first or second line of code depending on your version of python installed.

.. code-block:: text

    python3 -m src.main
    python -m src.main


Gameplay instructions
---------------------

Once the game window has opened, first enter the player names and/or choose to include an AI player(s). Next read the rules then press start game. The game will prompt you to choose two places for your starting settlement and to consequently build your starting road. You must then press the 'space bar' once you are done to allow the next person to choose.

When you have all completed this steps you will be in the normal game state and can continue as a normal game of catan. It is worth noting that in the trading screen the green and red buttons above the resource images allow you to choose how many of a particular resource you wish to trade after which you must press submit to confirm the trade.


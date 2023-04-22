Getting Started
===============

Pre-Requisites
--------------

Firstly you must ensure that on the system that you are using, and whether you are using a virtual environment or intend to do everything globally, you must not use a python version higher than 3.10 as this is the version that the game has been been tested to work optimally with and if not some packages will not install such as 'rembg', versions between 3.8 and 3.10 should also run with no issues.

In order to install the correct modules run this code in the terminal, however if you use a different package manager than pip, change accordingly

.. code-block:: text

    pip install -r requirements.txt

Just as some background information, this project is structured as a python package where the src folder is the package and therefore the main.py file is a module and needs to be run as such, as seen below.

Run Game
--------

To run the game open the terminal inside your IDE or globally on your system and enter the following command to run the main file as a module. For example within VSCode, open a terminal window from the toolbar and enter the below command. Use the first or second line of code depending on your version of python installed.

.. code-block:: text

    python3 -m src.main
    python -m src.main


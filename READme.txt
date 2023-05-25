Sudoku game
To run this game just run sudoku_gui.py 
Features: 

Enter - you have to click enter to enter your value/ number into the board. In case it is right answer it stays in board and you can’t change that tile further. If the answer  is not right it will count as a mistake under the board and gets deleted automatically. You only have 3 mistake opportunities, if you made 3 mistakes you will loose. 

H key - gives you hints in a form of random correct answers 

SPACE key - serves as a SUDOKU SOLVER button ( I didn’t have time to do actual button but made a backtracking logic to solve sudoku) 

Del/Backspace - deletes number 

Difficulty levels: 
I managed difficulty levels through dokusan library, it relates its difficulty level on several features such as quantity of missing numbers in a board, techniques needed to solve it, arrangement of shown numbers in a board etc (full explanation can be found in dokusan library ).

Game status : in the right you can see game status which shows in which stage you are .

Due to time limit this is all I could do, there was no time left for button for solve sudoku and further improvements.
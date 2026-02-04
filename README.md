This was written in a bit of a time crunch, so sorry for any confusion that is caused. in case of any questions, email: nikasha.datiashvili@gmail.com
to use it simply put all three attached files into a program with a recent python interpreter installed.
this is a pretty simple program, that serves to imitate Karel, Stanford University's robot, which makes learning python fun and easy. 
the program reads the .csv file named "world.csv" and exctracts information about the starting world from there. more about editing the starting world later.

to look at the starting world, run the Karel.py file and the 2d world will be printed.

Karel has 4 default functions built into her: move(), turn_left(), put_beeper(), and pick_beeper(). in Stanford's course, this is enough to get students accustomed to solving complex problems using only these four functions.

currently, in world.csv, Karel starts out facing East (right), which can be edited in the metadata by changing the E to N,S, or W. (the program contains all necessary metadata in the first line of the .csv file)

Karel is indicated on the grid with the letter K, while beepers are indicated with numbers. beepers are just an object Karel can place that helps her solve more complex tasks.

to use the program, simply input the functions you want Karel to use into the "user_program.py" file and press run on the "Karel.py" file.

an example of the problems Stanford's course asks you to solve is "Midpoint Karel". they task you with making a program that can find the middle point of the bottom row of any world. it tests you by giving you strange edge cases (like a 1x1 world) and giving you worlds with an even number tile width, meaning you need to fit your program for any possible scenario, and realize how to use your resources appropriately.

to edit the starting world, there are a few specifics to the csv file. the current one has three grids. the first one serves to indicate Karel's position, the second indicates which tile has wall(s) (here each tile can have no value, or a 4 character long string of digits 0000, 0100, 0001 ,0111, and so on. flipping the first 0 to a 1 indicates a north wall on that tile, the second one indicates a west wall, the third - south, and the fourth - east). the third grid corresponds to the amount of beepers on the grid, indicated by integers. because of the way the program is displayed in print, it is recommended to not go past 99 beepers, because, if the program had to print Karel and 100 beepers together (K100) that is a 4 character long string that wouldnt fit within the walls.

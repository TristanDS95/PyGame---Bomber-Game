# PyGame---Bomber-Game
just a small game, trying out the pygame library and it's function. 


See below for detailed description on how it works.


There are three main objects in the game: the plane, the bomb, and the buildings. The features of the plane and bomb are defined in dictionaries at the top of the code
(as well as the world, which keeps track of the game state - paused/not paused/game over). The buildings are set up after initializing the Pygame. Their heights are randomly generated
in increments of the TILE size (which is set to 40 pixels). This TILE size is used in many places through the code to keep elements of the game consistent. For example, I made sure to make the 
number of columns (buildings) divisible by the TILE size so that the buildings would fit neatly on the screen without extra space or partial buildings. 

The buildings are drawn using the draw_buildings function which uses a surface parameter. Basic rectangles are used. This type of function was initially also
used to draw the plane but I later changed this because I needed to add a tail to match the reference image. So instead I made a predrawn image using a surface then used blit to just move the static image 
of the plane around the screen. Blit is a Pygame function that I was not aware of. It essentially allows you to copy the exact pixels from a predrawn image and move it around the screen without basically redrawing
the image anytime you want the object to move.

Main Game Loop Explanation: Firstly, the game runs by setting 'running' to True, then the game runs while testing for certain events that will change running to False
(ending the game) or pause the game. These events will change the default values (paused/game_over) in the world dictionary from False to True.

The game timing is controlled by the clock.tick which is a Pygame function that takes FPS as a parameter. This is another variable that is defined and set at the top of the program so it can easily be editted/tuned.
While the game is running a few inputs are checked for; pausing with 'p' keypress and dropping a bomb with the spacebar. 

At the same time, collision detection is happening for the plane and the bomb. The bomb collision causes the building diretly below it to be reduced in height
and the plane collision causes the game to end (collision with building or ground/bottom of screen). The collision with the buildings is based on the coordinates of the front right end of the plane because
the plane moves left to right. 

There are also two helper functions to assist with this collision detection (col_index_from_x and column_top_y). These basically just get the column/building that the plane/bomb is above and the height of the building at that column (y-coordinate) 
Another important note is that the coordinates in Pygame go from top left to bottom right. So when checking for collisions, the <> sign will be opposite of the natural intuition (i.e. greater value means lower on the screen)

import pygame
import sys
import random


#Game settings
WIDTH, HEIGHT = 900,800
FPS = 60
TILE = 40

#Colors of objects
BG = (15,18,25)
PLANE_COLOR = (230, 230, 230)
BOMB_COLOR = (255,0,0)

plane = {
    "width": 60, #length of plane going left to right
    "height": 20, #distance down from top of plane to bottom
    "x": TILE, #x,y are the top-left corner of the plane
    "y": 40,
    "speed_x": 8,      # may need to tune speed
    "drop_dy": TILE,    #how far plane descends after each pass
}

bomb = {
    "active": False,
    "x": 0,
    "y": 0,
    "speed_y": 10,   # may need to tune speed
}

world = {
    "paused": False,
    "game_over": False,
}
#---------------
#INITIALIZE PYGAME
#---------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomber")
clock = pygame.time.Clock()


# --- build the plane as a single pre-drawn image 
TAIL_W = 15  # left margin for the tail
plane["img_w"] = plane["width"] + TAIL_W
plane["img_h"] = max(plane["height"], 30)

plane_surface = pygame.Surface((plane["img_w"], plane["img_h"]), pygame.SRCALPHA)

# body rectangle shifted right so tail fits on the left
body_rect = pygame.Rect(TAIL_W, (plane["img_h"] - plane["height"])//2, plane["width"], plane["height"])
pygame.draw.rect(plane_surface, PLANE_COLOR, body_rect)

# tail triangle centered on the body's vertical middle
mid_y = body_rect.centery
tail_points = [(TAIL_W, mid_y), (0, mid_y - plane["height"]//3), (0, mid_y + plane["height"]//3)]
pygame.draw.polygon(plane_surface, PLANE_COLOR, tail_points)

#BUILDING SETUP

NUM_COLS = 13    
COL_WIDTH = WIDTH // NUM_COLS

#Generate random building heights and random building colors
heights = [random.randint(4, 14) * TILE for _ in range(NUM_COLS)]

PINK = (240,0, 180)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

color_choices = [PINK, GREEN, BLUE, YELLOW]
colors = [random.choice(color_choices) for _ in range(NUM_COLS)]


def draw_buildings(surface):
    base_y = HEIGHT - TILE
    for i,h in enumerate(heights):
        x = i * COL_WIDTH
        y = base_y - h
        color = colors[i] #different colors for buildings
        pygame.draw.rect(surface,color, (x, y, COL_WIDTH -12, h))

#HELPER FUNCTIONS FOR COLLISIONS
GROUND_Y = HEIGHT - TILE  # same as your draw_buildings baseline

def col_index_from_x(x):
    """Return which column an x-coordinate is in (clamped to valid range)."""
    c = int(x // COL_WIDTH)
    return max(0, min(NUM_COLS - 1, c))

def column_top_y(col):
    """Y-coordinate of the top surface of a column."""
    return GROUND_Y - heights[col]


def draw_plane(surface):
    surface.blit(plane_surface, (plane["x"], plane["y"]))



running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN: #pause/unpause game with 'p' key
            if event.key == pygame.K_p:
                world["paused"] = not world["paused"]
            #drop bomb on spacebar if one isn't active
            elif event.key == pygame.K_SPACE and not world["paused"] and not bomb["active"]:
                bomb["active"] = True
                bomb["x"] = plane["x"] + plane["width"] // 2
                bomb["y"] = plane["y"] + plane["height"]



#screen coordinates start at top-left corner (0,0) and moves bottom-right

#bomb movement and plane movement
    if not world["paused"]:

        plane["x"] += plane["speed_x"]
        if bomb["active"]:
            bomb["y"] += bomb["speed_y"]

            #Collision check w building/column under bomb
            bcol = col_index_from_x(bomb["x"])
            btop = column_top_y(bcol)
            bomb_radius = 5  #bomb radius for collision detection

            if bomb["y"] + bomb_radius >= btop:
                #bomb hit building
                DAMAGE = TILE * 3
                #reduce building height
                heights[bcol] = max(0, heights[bcol] - DAMAGE)
                bomb['active']=False
            elif bomb["y"] + bomb_radius >= GROUND_Y:
                #bomb off bottom of screen
                bomb['active']=False
        front_plane = plane["x"] + plane["img_w"]-1  #front of plane for collision detection
        pcol = col_index_from_x(front_plane)
        ptop = column_top_y(pcol)

        if plane["y"] + plane["height"] >= ptop:
            #plane hit building - end game
            world["game_over"] = True
            world["paused"] = True
            print("Game Over! The plane has crashed.")
        elif plane["y"] + plane["height"] >= GROUND_Y:
            #plane hit ground - end game
            world["game_over"] = True
            world["paused"] = True
            print("Game Over! The plane has crashed.")


        if plane["x"] > WIDTH:  #wrap around and descend after each pass
            plane["x"] = -plane["width"]
            plane["y"] += plane["drop_dy"]

    screen.fill(BG)
    draw_buildings(screen)
    draw_plane(screen)
    if bomb["active"]:
        bomb_rect = pygame.Rect(int(bomb["x"]-4), int(bomb["y"]-4), 10, 10)
        pygame.draw.rect(screen, BOMB_COLOR, bomb_rect)
    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
sys.exit()



'''
Description:

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



'''
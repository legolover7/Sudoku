# Built in modules
import subprocess
import sys
import os

# Custom modules
import modules.draw as draw
import modules.gen_board as gen

#  Attempt to import modules, if they're not found, install them
try:
    import pygame as pyg
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "pygame"], stdout=subprocess.DEVNULL)
    import pygame as pyg
try:
    from screeninfo import get_monitors
except:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', "screeninfo"], stdout=subprocess.DEVNULL)
    from screeninfo import get_monitors

# Get screen size based on primary monitor
for m in get_monitors():
    if m.is_primary:
        WIDTH, HEIGHT = m.width, m.height

# Initialize window
pyg.init()
WINDOW = pyg.display.set_mode((WIDTH, HEIGHT))
pyg.display.set_caption("Classic Soduko")

os.system("cls")

FPS = 60

# Color maps:
# 0 = Gray/normal, 1 = Green

# Difficulty thresholds:
# 0.5 = Easy
difficulty = 0.4
base = 3
square_size = 60

# Main control function
def Main():
    # Global variables
    global WINDOW, WIDTH, HEIGHT, FPS
    
    game_board, solved_board, counts = Generate_Board()
    submit = False

    # Local variables
    mouse_pos = (0, 0)
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(base ** 2):
        for y in range(base ** 2):
            if game_board[x][y][0] != "":
                val = int(game_board[x][y][0])
                if 1 <= val <= 9:
                    counts[val-1] += 1

    clock = pyg.time.Clock()
    while True:
        for event in pyg.event.get():
            mouse_pos = pyg.mouse.get_pos()
            mods = pyg.key.get_mods()
            shift = mods & pyg.KMOD_SHIFT
            ctrl = mods & pyg.KMOD_CTRL

            # Window closed
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            # Key pressed
            elif event.type == pyg.KEYDOWN:
                key = event.key
                # Exit key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

                # Reset
                elif key == pyg.K_F5:
                    game_board, solved_board, counts = Generate_Board()
                    submit = False

                # Clear selected cells
                elif key == pyg.K_BACKSPACE and not submit:
                    for x in range(base**2):
                        for y in range(base**2):
                            if game_board[x][y][0] != "":
                                val = int(game_board[x][y][0])
                            if game_board[x][y][1] and type(game_board[x][y][0]) != int:
                                game_board[x][y][0] = ""
                                counts[int(val)-1] -= 1
                            if game_board[x][y][1] and shift:
                                game_board[x][y][3] = []
                            


                # Num keys
                elif 49 <= key <= 57 and not submit:
                    num = "123456789"[key-49]
                    if not ctrl and not shift:
                        for x in range(base**2):
                            for y in range(base**2):
                                if game_board[x][y][1] and type(game_board[x][y][0]) != int:
                                    game_board[x][y][0] = num
                                    counts[int(num)-1] += 1

                    # Notes
                    elif shift:
                        for x in range(base**2):
                            for y in range(base**2):
                                if game_board[x][y][1] and num not in game_board[x][y][3]:
                                    game_board[x][y][3] += [num]
                                elif game_board[x][y][1] and num in game_board[x][y][3]:
                                    game_board[x][y][3].remove(num)
                    
            
            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                if 22 + (square_size * base ** 2) / 2 - 150 <= mouse_pos[0] <= 22 + (square_size * base ** 2) / 2 + 150 and square_size * (base ** 2 + 2) <= mouse_pos[1] <= square_size * (base ** 2 + 2) + 30:
                    if submit:
                        game_board, solved_board, counts = Generate_Board()
                        submit = False
                    else:
                        submit = True

                elif mouse_pos[0] > 20 and mouse_pos[1] > 20:
                    # Calculate tile
                    tile_x = (mouse_pos[0] - 20) // square_size
                    tile_y = (mouse_pos[1] - 20) // square_size

                    color = -1
                    
                    # Select tiles in game board
                    if tile_x < base ** 2 and tile_y < base ** 2:
                        tile_value = str(game_board[tile_x][tile_y][0])
                        for x in range(base**2):
                            for y in range(base ** 2):
                                if not ctrl:
                                    game_board[x][y][1] = False
                                if shift and str(game_board[x][y][0]) == tile_value and tile_value != "":
                                    game_board[x][y][1] = True

                        game_board[tile_x][tile_y][1] = True
                    
                    # Clear all
                    elif tile_x == base ** 2 + 1 and tile_y == 0:
                        for x in range(base**2):
                            for y in range(base**2):
                                game_board[x][y][2] = 0
                        
                    # Calculate color square
                    elif base ** 2 + 2 <= tile_x <= base ** 2 + 5 and tile_y == 0:
                        color = tile_x - (base ** 2 + 2)                        

                    if color != -1:
                        for x in range(base**2):
                            for y in range(base**2):
                                if game_board[x][y][1]:
                                    game_board[x][y][2] = color

        
            draw.draw(WINDOW, (WIDTH, HEIGHT), mouse_pos, game_board, solved_board, square_size, base, counts, submit)
        clock.tick(FPS)



def Generate_Board():
    game_board, solved_board = gen.generate(3, difficulty)

    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for x in range(base ** 2):
        for y in range(base ** 2):
            if game_board[x][y][0] != "":
                val = int(game_board[x][y][0])
                if 1 <= val <= 9:
                    counts[val-1] += 1

    return game_board, solved_board, counts
Main()
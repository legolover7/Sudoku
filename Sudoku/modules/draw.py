# Import statements
import pygame as pyg

# Draw function
def draw(WINDOW, size, mouse, board, s_board, square_size, base, counts, submit):
    # Unpack variables
    WIDTH, HEIGHT = size

    # Local variables
    black = (25, 25, 25)
    dark_gray = (40, 40, 40)
    gray = (60, 60, 60)
    white = (255, 255, 255)
    blue = (100, 150, 255)
    light_green = (0, 140, 0)

    green = (0, 60, 0)
    magenta = (139, 0, 139)
    red = (80, 0, 0)
    light_red = (140, 0, 0)
    mapped_colors = [gray, green, magenta, red]

    num_font = pyg.font.SysFont("consolas", 30)
    note_font = pyg.font.SysFont("consolas", 18)
    text_font = pyg.font.SysFont("consolas", 18)

    WINDOW.fill(black)

    x_offset = 1
    pyg.draw.rect(WINDOW, dark_gray, (20, 20, square_size * base ** 2 + 10, square_size * base ** 2 + 10))

    # Draw tiles
    for x in range(base ** 2):
        y_offset = 1
        if x % 3 == 0:
            x_offset += 2
        for y in range(base ** 2):
            tile = board[x][y]
            if y % 3 == 0:
                y_offset += 2

            pyg.draw.rect(WINDOW, dark_gray, (20 + x_offset + x*square_size, 20 + y_offset + y*square_size, square_size, square_size))
            
            if submit:
                pyg.draw.rect(WINDOW, gray, (21 + x_offset + x*square_size, 21 + y_offset + y*square_size, square_size-2, square_size-2))
                if type(tile[0]) == int or tile[0] == "":
                    color = white
                elif int(tile[0]) == int(s_board[x][y][0]):
                    color = light_green
                else:
                    color = red
                text_w, text_h = num_font.size(str(tile[0]))
                WINDOW.blit(num_font.render(str(tile[0]), True, color), (20 + x_offset + x*square_size + (square_size-text_w)/2, 20 + y_offset + y*square_size + (square_size-text_h)/2))

            else:
                tile_color = mapped_colors[tile[2]]

                if tile[1]:
                    pyg.draw.rect(WINDOW, blue, (20 + x_offset + x*square_size, 20 + y_offset + y*square_size, square_size, square_size))
                    pyg.draw.rect(WINDOW, tile_color, (27 + x_offset + x*square_size, 27 + y_offset + y*square_size, square_size-14, square_size-14))
                else:
                    pyg.draw.rect(WINDOW, tile_color, (21 + x_offset + x*square_size, 21 + y_offset + y*square_size, square_size-2, square_size-2))
                
                if tile[0] != "":
                    if type(tile[0]) == int:
                        color = white
                    else:
                        color = blue
                    text_w, text_h = num_font.size(str(tile[0]))
                    WINDOW.blit(num_font.render(str(tile[0]), True, color), (20 + x_offset + x*square_size + (square_size-text_w)/2, 20 + y_offset + y*square_size + (square_size-text_h)/2))

                else:
                    note_len = len(tile[3])
                    for i in range(note_len):
                        note = tile[3][i]
                        text_w, text_h = note_font.size(note)
                        note_offset = (square_size-text_w * note_len)/2
                        WINDOW.blit(note_font.render(str(note), True, blue), (20 + x_offset + note_offset + x*square_size + i * text_w, 20 + y_offset + y*square_size + (square_size-text_h)/2))

    # Num tracking
    for i in range(len(counts)):
        color = gray
        if counts[i] < 9:
            color = white
        
        WINDOW.blit(num_font.render(str(i+1), True, color), (22 + square_size / 2 + i * square_size, (base ** 2 + 1) * square_size))

    # Submit button
    if not submit:
        color = light_green
        if 22 + (square_size * base ** 2) / 2 - 150 <= mouse[0] <= 22 + (square_size * base ** 2) / 2 + 150 and square_size * (base ** 2 + 2) <= mouse[1] <= square_size * (base ** 2 + 2) + 30:
            color = green
        pyg.draw.rect(WINDOW, color, (22 + (square_size * base ** 2) / 2 - 150, square_size * (base ** 2 + 2), 300, 30))
        text_w, text_h = text_font.size("Submit board")
        WINDOW.blit(text_font.render("Submit board", True, white), (22 + (square_size * base ** 2 - text_w) / 2, square_size * (base ** 2 + 2) + text_h / 2 - 2))
    
    # Reset
    else:
        color = light_red
        if 22 + (square_size * base ** 2) / 2 - 150 <= mouse[0] <= 22 + (square_size * base ** 2) / 2 + 150 and square_size * (base ** 2 + 2) <= mouse[1] <= square_size * (base ** 2 + 2) + 30:
            color = red
        pyg.draw.rect(WINDOW, color, (22 + (square_size * base ** 2) / 2 - 150, square_size * (base ** 2 + 2), 300, 30))
        text_w, text_h = text_font.size("Reset")
        WINDOW.blit(text_font.render("Reset", True, white), (22 + (square_size * base ** 2 - text_w) / 2, square_size * (base ** 2 + 2) + text_h / 2 - 2))

    # Draw tile color choices
    pyg.draw.rect(WINDOW, gray, (20 + x_offset + (base ** 2 + 1) * square_size, 20, square_size, square_size))
    pyg.draw.rect(WINDOW, dark_gray, (22 + x_offset + (base ** 2 + 1) * square_size, 22, square_size-4, square_size-4))
    pyg.draw.line(WINDOW, white, (22 + x_offset + (base ** 2 + 1) * square_size, 22), (22 + x_offset + (base ** 2 + 1) * square_size + square_size-6, 20 + square_size-4), 2)
    pyg.draw.line(WINDOW, white, (22 + x_offset + (base ** 2 + 1) * square_size + square_size-6, 22), (22 + x_offset + (base ** 2 + 1) * square_size, 20 + square_size-4), 2)
    
    x_offset += 4
    for i in range(len(mapped_colors)):
        pyg.draw.rect(WINDOW, dark_gray, (20 + x_offset + (base ** 2 + 2 + i) * square_size, 20, square_size, square_size))
        pyg.draw.rect(WINDOW, mapped_colors[i], (22 + x_offset + (base ** 2 + 2 + i) * square_size, 22, square_size-4, square_size-4))


    # Controls text
    WINDOW.blit(text_font.render("Controls:", True, white), (22 + (base ** 2 + 1) * square_size, 120))
    WINDOW.blit(text_font.render("Clicking on a tile with the LMB will select that tile. If the ctrl key is held, it will not deselect all other tiles,", True, white), (22 + (base ** 2 + 1) * square_size, 145))
    WINDOW.blit(text_font.render("and if the shift key is pressed, it will select all tiles with the same value as the tile you have selected, excluding blanks.", True, white), (22 + (base ** 2 + 1) * square_size, 170))
    WINDOW.blit(text_font.render("Clicking on any of the color boxes above will color all selected tiles, with the leftmost box resetting all colors.", True, white), (22 + (base ** 2 + 1) * square_size, 210))
    WINDOW.blit(text_font.render("You can enter in numbers using the keyboard, and if you are holding shift while doing so, you will add a note to that cell.", True, white), (22 + (base ** 2 + 1) * square_size, 250))
    WINDOW.blit(text_font.render("Pressing backspace will remove any inserted numbers, with backspace+shift removing the notes as well.", True, white), (22 + (base ** 2 + 1) * square_size, 275))
    WINDOW.blit(text_font.render("Below the board is a list of the numbers and these will be grayed out if you have 9 (or more)", True, white), (22 + (base ** 2 + 1) * square_size, 315))
    WINDOW.blit(text_font.render("instances of that number in the board.", True, white), (22 + (base ** 2 + 1) * square_size, 340))
    WINDOW.blit(text_font.render("Once you are satisfied with your solution, click the green \"Submit\" button to check if your board is correct.", True, white), (22 + (base ** 2 + 1) * square_size, 380))
    WINDOW.blit(text_font.render("Any cells with green numbers were correct, any with white were what you were given, and any that are red were incorrect.", True, white), (22 + (base ** 2 + 1) * square_size, 405))
    WINDOW.blit(text_font.render("Happy Sudoko-ing!", True, white), (22 + (base ** 2 + 1) * square_size, 440))

    pyg.display.update()
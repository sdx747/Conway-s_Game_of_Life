from tkinter import *
from tkinter import messagebox
import random
import threading


# Creating the functions


def random_grid():
    global keep_simulating
    keep_simulating = True
    values = [0, 0, 0, 0, 1]
    return [[values[random.randint(0, 4)] for _ in range(columns)] for _ in range(rows)]


def fill_grid():
    global keep_simulating
    keep_simulating = True
    if grid_sum() != rows * columns:
        return [[1 for _ in range(columns)] for _ in range(rows)]


def toggle(i, j):
    if button_grid[i][j]['bg'] == "yellow":
        button_grid[i][j]['bg'] = "black"
    else:
        button_grid[i][j]['bg'] = "yellow"


def reset():
    global keep_simulating
    keep_simulating = True
    for i in range(rows):
        for j in range(columns):
            button_grid[i][j].config(bg="black")


def grid_sum():
    grid = get_grid()
    return sum(sum(grid[r]) for r in range(rows))


def enable_controls():
    reset_button['state'] = NORMAL
    start_button['state'] = NORMAL
    random_button['state'] = NORMAL
    next_button['state'] = NORMAL
    fill_button['state'] = NORMAL
    pause_button['state'] = DISABLED
    for i in range(rows):
        for j in range(columns):
            button_grid[i][j]['state'] = NORMAL


def disable_controls():
    reset_button['state'] = DISABLED
    start_button['state'] = DISABLED
    random_button['state'] = DISABLED
    next_button['state'] = DISABLED
    fill_button['state'] = DISABLED
    pause_button['state'] = NORMAL
    for i in range(rows):
        for j in range(columns):
            button_grid[i][j]['state'] = DISABLED


def visualise_grid(grid):
    if grid is None:
        return
    for i in range(rows):
        for j in range(columns):
            if grid[i][j] == 1:
                button_grid[i][j].config(bg="yellow")
            if grid[i][j] == 0:
                button_grid[i][j].config(bg="black")


def get_grid():
    current_grid = [[0 for _ in range(columns)] for _ in range(rows)]
    for i in range(rows):
        for j in range(columns):
            if button_grid[i][j]['bg'] == "yellow":
                current_grid[i][j] = 1
    return current_grid


def updating_grid():
    if grid_sum() > 0:
        current_grid = get_grid()
        new_grid = [[0 for _ in range(columns)] for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                neighbours = 0
                # North-East neighbour
                neighbours += current_grid[i - 1][j - 1]
                # North neighbour
                neighbours += current_grid[i - 1][j]
                # North-West neighbour
                if j < columns - 1:
                    neighbours += current_grid[i - 1][j + 1]
                else:
                    neighbours += current_grid[i - 1][0]
                # East neighbour
                neighbours += current_grid[i][j - 1]
                # West neighbour
                if j < columns - 1:
                    neighbours += current_grid[i][j + 1]
                else:
                    neighbours += current_grid[i][0]
                # South-East neighbour
                if i < rows - 1:
                    neighbours += current_grid[i + 1][j - 1]
                else:
                    neighbours += current_grid[0][j - 1]
                # South neighbour
                if i < rows - 1:
                    neighbours += current_grid[i + 1][j]
                else:
                    neighbours += current_grid[0][j]
                # South-West neighbour
                if i < rows - 1 and j < columns - 1:
                    neighbours += current_grid[i + 1][j + 1]
                elif i == rows - 1 and j == columns - 1:
                    neighbours += current_grid[0][0]
                elif i == rows - 1:
                    neighbours += current_grid[0][j + 1]
                else:
                    neighbours += current_grid[i + 1][0]

                if current_grid[i][j] == 1:
                    if neighbours == 2 or neighbours == 3:
                        new_grid[i][j] = 1
                if current_grid[i][j] == 0:
                    if neighbours == 3:
                        new_grid[i][j] = 1

        visualise_grid(new_grid)


def start_simulation():
    global keep_simulating
    if grid_sum() == 0:
        enable_controls()
        return
    if keep_simulating:
        disable_controls()
        updating_grid()
        threading.Timer(0, start_simulation).start()
    else:
        keep_simulating = True
        enable_controls()
        return


def pause():
    global keep_simulating
    keep_simulating = False


def instruction_message():
    messagebox.showinfo("Instructions", text)


def exit_app():
    root.destroy()


# Creating the window

root = Tk()
root.title("Conway's Game of Life")
root.geometry("1320x720")
window = Frame(root, padx=0, pady=10, borderwidth=1, relief=SUNKEN)
window.grid(row=0, column=0, columnspan=25, padx=25)

# Instructions text
f = open('instructions.txt', 'r')
text = f.read()

# Creating buttons grid

rows = 25
columns = 53
keep_simulating = True

button_grid = [
    [Button(window, height=1, width=2, bg="black", command=lambda i=i, j=j: toggle(i, j)) for j in range(columns)] for i
    in range(rows)]

for i in range(rows):
    for j in range(columns):
        button_grid[i][j].grid(row=i, column=j)

# Adding control buttons

button_bg = "#16E1A4"
active_bg = "#70D8B9"

start_button = Button(root, text="START", bg=button_bg, activebackground=active_bg, height=1, width=7,
                      command=start_simulation)
next_button = Button(root, text="NEXT", bg=button_bg, activebackground=active_bg, height=1, width=7,
                     command=updating_grid)
random_button = Button(root, text="RANDOM", bg=button_bg, activebackground=active_bg, height=1, width=7,
                       command=lambda: visualise_grid(random_grid()))
pause_button = Button(root, text="PAUSE", bg=button_bg, activebackground=active_bg, height=1, width=7, state=DISABLED,
                      command=pause)
fill_button = Button(root, text="FILL", bg=button_bg, activebackground=active_bg, height=1, width=7,
                     command=lambda: visualise_grid(fill_grid()))
reset_button = Button(root, text="RESET", bg=button_bg, activebackground=active_bg, height=1, width=7, command=reset)
exit_button = Button(root, text="EXIT", bg=button_bg, activebackground=active_bg, height=1, width=7, command=exit_app)

instruct_button = Button(root, text="Instructions", bg='#16E1D4', activebackground=active_bg, height=1, width=9,
                         command=instruction_message)
instruct_button.grid(row=1, column=1)

start_button.grid(row=1, column=8, pady=10)
next_button.grid(row=1, column=9)
random_button.grid(row=1, column=10)
pause_button.grid(row=1, column=11)
fill_button.grid(row=1, column=12)
reset_button.grid(row=1, column=13)
exit_button.grid(row=1, column=14)

root.mainloop()

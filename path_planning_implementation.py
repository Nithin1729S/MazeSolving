# %%
import numpy as np
from graphics import *
import tkinter as tk
import time
# %%

# R, C = 5, 7
# # m = [['S', '.', '.', '#', '.', '.', '.'],
# #      ['.', '#', '.', '.', '.', '#', '.'],
# #      ['.', '#', '.', '#', '.', '.', '#'],
# #      ['.', '.', '#', '.', '#', '.', '.'],
# #      ['#', '.', '#', 'E', '.', '.', '#']]

# m = [['S', '.', '.', '#', '.', '.', '.'],
#      ['.', '#', '.', '.', '.', '#', '.'],
#      ['.', '-', '.', '#', '.', '.', '#'],
#      ['.', '#', '#', '.', '#', '.', '.'],
#      ['#', '.', '#', 'E', '.', '.', '#']]

# R,C=3,3;

# m=[['S', '#', '-'], ['-', '#', '-'], ['-', '-', 'E']]
# print(m)
# %%

class MazeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Generator")

        self.label = tk.Label(root, text="Enter dimensions of the maze (rows x columns):")
        self.label.pack()

        self.rows_entry = tk.Entry(root)
        self.rows_entry.pack()

        self.generate_button = tk.Button(root, text="Generate Maze", command=self.generate_maze)
        self.generate_button.pack()

        self.maze = None

    def generate_maze(self):
        dimensions = self.rows_entry.get().split('x')
        if len(dimensions) != 2:
            self.label.config(text="Invalid input. Please enter dimensions in the format 'rows x columns'.")
            return

        try:
            rows = int(dimensions[0])
            columns = int(dimensions[1])
        except ValueError:
            self.label.config(text="Invalid input. Please enter valid integer dimensions.")
            return

        if rows <= 0 or columns <= 0:
            self.label.config(text="Invalid dimensions. Please enter positive integers.")
            return

        self.label.config(text="Click on each cell to set S, E, #, or - (default).")
        self.generate_button.config(state=tk.DISABLED)

        self.maze = [['-' for _ in range(columns)] for _ in range(rows)]
        self.display_maze()

    def display_maze(self):
        self.root.destroy()
        root = tk.Tk()
        root.title("Maze Creator")

        def on_click(row, col):
            def set_symbol(symbol):
                self.maze[row][col] = symbol
                button.config(text=symbol)

            button = buttons[row][col]
            menu = tk.Menu(root, tearoff=0)
            menu.add_command(label="S", command=lambda: set_symbol('S'))
            menu.add_command(label="E", command=lambda: set_symbol('E'))
            menu.add_command(label="#", command=lambda: set_symbol('#'))
            menu.add_command(label="-", command=lambda: set_symbol('-'))
            menu.tk_popup(root.winfo_pointerx(), root.winfo_pointery())

        buttons = []
        for i in range(len(self.maze)):
            row_buttons = []
            for j in range(len(self.maze[0])):
                button = tk.Button(root, text='-', width=4, height=2, command=lambda row=i, col=j: on_click(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            buttons.append(row_buttons)

        def submit_maze():
            print("Submitted Maze:")
            for row in self.maze:
                print(' '.join(row))
            # root.destroy()
            root.quit()

        submit_button = tk.Button(root, text="Submit", command=submit_maze)
        submit_button.grid(row=len(self.maze)+1, columnspan=len(self.maze[0]))

        root.mainloop()

    def get_maze(self):
        return self.maze
    
    
root = tk.Tk()
generator = MazeGenerator(root)
print("Hi")

root.mainloop()
print("Hi3")
m= generator.get_maze()
R=len(m)
C=len(m[0])
print(m)


class queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)


# %%
sr, sc = 0, 0
s = (sr, sc)
e = (0,0)
rq, cq = queue(), queue()

# %%
move_count = 0
nodes_left_in_layer = 1
nodes_in_next_layer = 0
# %%
reach_end = False
# %%
# visited = np.zeros((5, 7))
# # prev = np.empty((5, 7))
# # prev.fill(0)
# prev = [[0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 0, 0]]

visited = np.zeros((R, C))
prev = np.empty((R, C), dtype=object)
# %%
dr = [-1, +1, 0, 0]
dc = [0, 0, +1, -1]

#%%
def rectangle(rr,cc):
    rr *=100
    cc *=100
    rect = Rectangle(Point(cc,rr), Point(100+cc, 100+rr))
    rect.draw(win)

def circle(rr,cc):
    rr *=100
    cc *=100
    c = Circle(Point(cc+50,rr+50), 25)
    c.draw(win)

def text(rr,cc,text_input):
    rr *=100
    cc *=100
    text = Text(Point(cc+50,rr+50),text_input)
    text.setSize(30)
    text.draw(win)

class agent:
    def __init__(self,cr,cc):
        self.cr=cr*100
        self.cc=cc*100
        self.text = Text(Point(self.cc+50,self.cr+50),'X')
        self.text.draw(win)
    def movement(self,mr,mc):
        mr *=100
        mc *=100
        self.text.move((mc-self.cc),(mr-self.cr))
        self.cc= mc
        self.cr= mr

# %%
def draw_grid(R,C):
    for i in range(R):
        for j in range(C):
            rectangle(i,j)


#%%


def explore_neighbours(r, c):
    global nodes_in_next_layer, prev
    for i in range(0, 4):
        rr = r + dr[i]
        cc = c + dc[i]

        
        
        if rr < 0 or cc < 0:
            continue
        if rr >= R or cc >= C:
            continue

        if visited[rr][cc]:
            continue
        if m[rr][cc] == '#':
            circle(rr,cc)
            continue
        rq.enqueue(rr)
        cq.enqueue(cc)
        visited[rr][cc] = True
        prev[rr][cc] = (r, c)
        nodes_in_next_layer += 1

# %%


def solve():
    global reach_end, e,move_count, nodes_left_in_layer, nodes_in_next_layer
    rq.enqueue(sr)
    cq.enqueue(sc)
    visited[sr][sc] = True
    while rq.size() > 0:
        r = rq.dequeue()
        c = cq.dequeue()
        if m[r][c] == 'E':
            e = (r, c)
            text(r,c,"E")
            reach_end = True
            break
        explore_neighbours(r, c)
        nodes_left_in_layer -= 1
        if nodes_left_in_layer == 0:
            nodes_left_in_layer = nodes_in_next_layer
            nodes_in_next_layer = 0
            move_count += 1

    if reach_end:
        return move_count
    return -1

# %%


def reconstructPath(prev):
    global e, s
    path = []
    at = e
    while(at != s):
        path.append(at)
        at = prev[at[0]][at[1]]
    path.append(s)  # Append the starting position as well
    path.reverse()

    return path
    
# %%
print("Hi")
win = GraphWin("My Grid", 1000, 600)
draw_grid(R,C)
text(sc,sr,"S")
print(solve())
agent_0 = agent(sc,sr)
path_0 = reconstructPath(prev)
for i in path_0:
    agent_0.movement(i[0],i[1])
    time.sleep(1)
    line = Line(Point(agent_0.cc+100,agent_0.cr+100),Point((i[1])*100,(i[0])*100))
    line.draw(win)
    time.sleep(1)
win.getMouse() # Pause to view result
win.close()
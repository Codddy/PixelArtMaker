from tkinter import *
from tkinter import colorchooser, filedialog, simpledialog, messagebox
from PIL import Image, ImageGrab

# Set up constants
cell_size = 20
num_cells = 32
width = cell_size * num_cells
height = cell_size * num_cells

# Initialize the grid to represent the pixel art canvas
grid = [[0] * num_cells for _ in range(num_cells)]

# Default drawing settings
outline_disabled = False
color = ("black", "black")

# Function to handle painting on the canvas when the left mouse button is pressed
def paint(event):
    x, y = event.x // cell_size, event.y // cell_size
    grid[x][y] = 1
    x1, y1 = x * cell_size, y * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color[0], outline="" if outline_disabled else color[1])

# Function to handle continuous painting while dragging the mouse
def drag_paint(event):
    x, y = event.x // cell_size, event.y // cell_size
    grid[x][y] = 1
    x1, y1 = x * cell_size, y * cell_size
    x2, y2 = x1 + cell_size, y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill=color[0], outline="" if outline_disabled else color[1])

# Function to disable or enable outline on existing pixels
def disable_outline():
    global outline_disabled
    if not outline_disabled:
        for item in canvas.find_all():
            canvas.itemconfig(item, outline="")
        outline_disabled = True
    else:
        for item in canvas.find_all():
            canvas.itemconfig(item, outline=color[1])
        outline_disabled = False

# Function to choose a fill color using a color chooser dialog
def choose_color():
    global color
    fill_color = colorchooser.askcolor()[1]
    color = (fill_color, color[1])

# Function to erase pixels on the canvas
def erase(event):
    x, y = event.x // cell_size, event.y // cell_size
    if grid[x][y] == 1:
        grid[x][y] = 0
        x1, y1 = x * cell_size, y * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline=color[1])

# Function to erase pixels while dragging the mouse
def drag_erase(event):
    x, y = event.x // cell_size, event.y // cell_size
    if grid[x][y] == 1:
        grid[x][y] = 0
        x1, y1 = x * cell_size, y * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline=color[1])

# Function to save the canvas as an image
def save_button():
    disable_outline()
    filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG", "*.png")])
    if filename:
        img = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))
        img.save(filename, "png")
        messagebox.showinfo(title="Image Saved", message="The image has been saved as {}".format(filename))

# Function to clear the canvas
def clear_canvas():
    global grid
    grid = [[0] * num_cells for _ in range(num_cells)]
    canvas.delete("all")
    for i in range(num_cells):
        for j in range(num_cells):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

# Function to resize the canvas
def resize_canvas():
    global num_cells, cell_size, width, height, grid
    size = simpledialog.askinteger("Resize Canvas", "Enter canvas size (between 8 and 128):", minvalue=8, maxvalue=128)
    if size is None:
        return
    num_cells = size
    cell_size = 640 // num_cells
    width = cell_size * num_cells
    height = cell_size * num_cells
    grid = [[0] * num_cells for _ in range(num_cells)]
    canvas.config(width=width, height=height)
    canvas.delete("all")
    for i in range(num_cells):
        for j in range(num_cells):
            x1, y1 = i * cell_size, j * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, outline="black")

# Create the main Tkinter window
master = Tk()
master.title("Pixel Art")

# Create the canvas widget for drawing
canvas = Canvas(master, width=width, height=height, bg='white')
canvas.pack()
canvas.bind("<B1-Motion>", drag_paint)

# Draw the initial grid on the canvas
for i in range(num_cells):
    for j in range(num_cells):
        x1, y1 = i * cell_size, j * cell_size
        x2, y2 = x1 + cell_size, y1 + cell_size
        canvas.create_rectangle(x1, y1, x2, y2, outline="black")

# Bind mouse events to their respective functions
canvas.bind("<Button-1>", paint)
canvas.bind("<Button-3>", erase)
canvas.bind("<B3-Motion>", drag_erase)

# Create buttons for various actions
disable_button = Button(master, text="Disable/Enable Outline", command=disable_outline)
disable_button.pack(side=LEFT, padx=5)

color_button = Button(master, text="Choose Color", command=choose_color)
color_button.pack(side=LEFT, padx=5)

save_button = Button(master, text="Save", command=save_button)
save_button.pack(side=LEFT, padx=5)

clear_button = Button(master, text="Clear Canvas", command=clear_canvas)
clear_button.pack(side=LEFT, padx=5)

resize_button = Button(master, text="Resize Canvas", command=resize_canvas)
resize_button.pack(side=LEFT, padx=5)

# Start the Tkinter event loop
mainloop()

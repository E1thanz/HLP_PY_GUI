import tkinter as tk
from tkinter import ttk
from NewLayer import Layer


# warning this program is very junky and if you spam stuff it will lag/slow down and I cannot insure it won't crash
# low-end computers, if you do not spam anything it should be fine :)
root = tk.Tk()  # the tkinter window
padding = 10  # a small value I use to pad the layer dots from the edges of the screen, and also use for other spacing
inside_padding = 80  # value between each layer
size = 30  # size of a layer value's dot
layers = 2  # amount of layers CHANGE THIS IF YOU WANT MORE OR LESS LAYERS
side_bar_size = 250  # pixel size of the sidebar
root_x = 16 * (size + padding) + padding + side_bar_size
root_y = (layers + 1) * (size + inside_padding) - inside_padding + 10 * padding + size
max_y = 8 * (size + inside_padding) - inside_padding + 10 * padding + size
root.geometry(f"{root_x}x{root_y if root_y < max_y else max_y}")  # setting window size
root.resizable(False, False)  # making sure people cant screw with it
root.update_idletasks()  # updating the window because why not
# canvas to draw the dots and lines of the layers
canvas = tk.Canvas(master=root, width=root_x - side_bar_size, height=(root_y if root_y < max_y else max_y) - 7 * padding, background="#aaaaaa", bd=0, highlightthickness=0)
# a canvas for holding the sidebar's layer's inputs
side_bar = tk.Canvas(master=root, width=side_bar_size, height=(root_y if root_y < max_y else max_y) - 10 * padding, bd=0, highlightthickness=0)
# print(((root_y if root_y < max_y else max_y) - 4 * padding - 2 * (size + padding)) // (size + inside_padding))
hex_layer = Layer()  # the object for simulating the hex layers
iter_layer = hex_layer  # like iterating on a linked list, so I don't lose the head I store it here
for _ in range(layers - 1):
    iter_layer.next_layer = Layer()
    iter_layer = iter_layer.next_layer
value_scales = []  # holds all the tkinter scale widgets for the A and B inputs for each layer
boolean_variables = []  # holds all the tkinter boolean variables that hold the comparator's mode for each layer
input_circles = []  # location of each input circle (bottom number layer), treats like a rectangle not a circle
input_frames = []  # all frames that hold each layers input widgets, scales and checkButtons
text_load = tk.Entry(root, width=143, background="#bbbbbb")  # used for input and output of a text representation of the layer
text_load.delete(0, tk.END)  # make sure its empty
text_load.insert(0, hex_layer.get_text_representation())  # load the current (default) text representation of the layer
y_offset = 0  # for scrolling


# updates the actual widget inputs does not update any values
def update_inputs(offset):
    side_bar.delete("all")
    for layer, frame in enumerate(input_frames):
        side_bar.create_window(padding, (2 * (padding + size)) + (inside_padding // 2) + layer * (size + inside_padding) + y_offset - 3 * padding, anchor="w", window=frame)
    text_load.delete(0, tk.END)
    text_load.insert(0, hex_layer.get_text_representation())
    render_layers()
    render_active_path(input_slider.get())


# updates only values and the layer does not touch input widgets location
def update_input_values(*args):
    text_repr = text_load.get()
    # side_bar.delete("all")
    for layer in range(layers - 1, -1, -1):
        boolean_variables[layer][0].set(text_repr.startswith("*"))
        value_scales[layer][0].set(int(text_repr[1:2], 16))
        text_repr = text_repr[3:]
        boolean_variables[layer][1].set(text_repr.startswith("*"))
        value_scales[layer][1].set(int(text_repr[1:2], 16))
        text_repr = text_repr[3:]
    change()


# when scrolling it adjusts the y_offset based on limits and stuff
def on_mouse_wheel(event):
    global y_offset
    if (event.num == 4 or event.delta == 120) and y_offset < 0:  # Scroll up
        y_offset += (inside_padding + size) // 2
        update_inputs((inside_padding + size) // 2)
        change()
    elif (event.num == 5 or event.delta == -120) and y_offset > -max(layers - (((root_y if root_y < max_y else max_y) - 4 * padding - 2 * (size + padding)) // (size + inside_padding)), 0) * (inside_padding + size):  # Scroll down
        y_offset -= (inside_padding + size) // 2
        update_inputs(-(inside_padding + size) // 2)
        change()


root.bind('<MouseWheel>', on_mouse_wheel)  # binds the mouse wheel action to the function on_mouse_wheel
unused_lines_var = tk.BooleanVar(value=False)  # boolean variable for the unused lines check button which toggles showing unused layer lines
# the check button for toggling showing unused lines
unused_lines_mode = tk.Checkbutton(master=root, text="unused lines", variable=unused_lines_var, command=update_input_values)
# boolean variable for the binary output check button which toggles showing the output as 0 if the value is 0 and 1 otherwise
binary_output_var = tk.BooleanVar(value=False)
# the check button for toggling switching to binary output (made this for Powsii)
binary_output_mode = tk.Checkbutton(master=root, text="1 if > 15 ", variable=binary_output_var, command=update_input_values)
text_load_button = tk.Button(root, text="Enter", command=update_input_values)  # enter button for entering a text input
root.bind('<Return>', update_input_values)  # binding the enter key to the update_input_values function


# activates when input slider changes value
def on_scale_change(index):
    index = int(index)
    canvas.delete("all")
    input_slider.set(index)
    render_layers()
    render_active_path(index)


# input slider, slider for input :)
input_slider = tk.Scale(root, from_=0, to=15, orient=tk.HORIZONTAL, length=635, command=on_scale_change)


# function for incrementing the value of the input_slider
def change_slider_value():
    if input_slider_button['text'] == "⏸":
        incremented_value = input_slider.get() + 1
        input_slider.set(incremented_value if incremented_value < 16 else 0)
        input_slider.update()
        root.after(500, change_slider_value)


# function for switching the state of the animation play/pause button
def animate_slider():
    if input_slider_button['text'] == "⏵":
        input_slider_button.configure(text="⏸")
        root.after(500, change_slider_value())
    else:
        input_slider_button.configure(text="⏵")


# animation play/pause button
input_slider_button = tk.Button(root, text="⏵", command=animate_slider)


# function activates when you left-click (used for input)
def on_left_click(event):
    x, y = event.x, event.y
    for index, circle in enumerate(input_circles):
        if circle[0] <= x <= circle[2] and circle[1] <= y <= circle[3]:
            canvas.delete("all")
            input_slider.set(index)
            render_layers()
            render_active_path(index)


# function that changes the layer's object parameter values while also updating everything
def change(*args):
    canvas.delete("all")
    iter_layer_ = hex_layer
    for layer in range(layers - 1, -1, -1):
        iter_layer_.set_a(int(value_scales[layer][0].get()))
        iter_layer_.set_b(int(value_scales[layer][1].get()))
        iter_layer_.set_mode_a(boolean_variables[layer][0].get())
        iter_layer_.set_mode_b(boolean_variables[layer][1].get())
        iter_layer_ = iter_layer_.next_layer
    text_load.delete(0, tk.END)
    text_load.insert(0, hex_layer.get_text_representation())
    render_layers()
    render_active_path(input_slider.get())


# function for painting on the main canvas the layer's dots and lines
def render_layers():
    global input_circles
    input_circles = []

    input_vector = [index for index in range(16)]
    iter_layer_ = hex_layer
    for layer in range(layers, 0, -1):
        next_vector = []
        for index in range(16):
            if index in input_vector or unused_lines_var.get():
                x = padding + index * (size + padding)
                y = 2 * padding + size + layer * (size + inside_padding) + y_offset

                new_x = padding + iter_layer_.map[index] * (size + padding)
                new_y = 2 * padding + size + (layer - 1) * (size + inside_padding) + y_offset

                if index in input_vector:
                    next_vector.append(iter_layer_.map[index])

                canvas.create_line((x + size // 2, y + size // 2,
                                    x + size // 2, y + (size // 2) - (inside_padding // 2),
                                    new_x + size // 2, new_y + (size // 2) + (inside_padding // 2),
                                    new_x + size // 2, new_y + size // 2), width=5, fill="#000000" if index in input_vector or not unused_lines_var.get() else '#FFFFFF', smooth=True)
        input_vector = next_vector
        iter_layer_ = iter_layer_.next_layer

    for index in range(16):
        x = padding + index * (size + padding)
        y = 2 * padding + size + layers * (size + inside_padding) + y_offset
        x2 = x + size
        y2 = y + size
        input_circles.append((x, y, x2, y2))
        canvas.create_oval(x, y, x2, y2, fill="#000000")
        canvas.create_text(x + size // 2, y + size // 2, text=str(index), font=("Arial", 12), fill="#FFFFFF")

    for layer in range(layers):
        for index in range(16):
            x = padding + index * (size + padding)
            y = 2 * padding + size + layer * (size + inside_padding) + y_offset
            x2 = x + size
            y2 = y + size

            canvas.create_oval(x, y, x2, y2, fill="#000000")
            canvas.create_text(x + size // 2, y + size // 2, text=str(index), font=("Arial", 12), fill="#FFFFFF")

    for index in range(16):
        x = padding + index * (size + padding)
        y = padding + y_offset
        x2 = x + size
        y2 = y + size
        output = hex_layer.output_single(index)
        if binary_output_var.get():
            canvas.create_oval(x, y, x2, y2, fill="#000000" if int(output == 0) else '#FFFFFF')
            continue
        canvas.create_oval(x, y, x2, y2, fill="#000000")
        canvas.create_text(x + size // 2, y + size // 2, text=output, font=("Arial", 12), fill="#FFFFFF")


def render_active_path(index):
    iter_layer_ = hex_layer
    last_input = index
    last_coordinate = None
    for layer in range(layers, -1, -1):
        if layer == layers:
            x = padding + index * (size + padding)
        else:
            last_input = iter_layer_.map[last_input]
            x = padding + last_input * (size + padding)
            iter_layer_ = iter_layer_.next_layer
        y = 2 * padding + size + layer * (size + inside_padding) + y_offset
        x2 = x + size
        y2 = y + size

        if layer != layers:
            canvas.create_line((last_coordinate[0] + size // 2, last_coordinate[1] + size // 2,
                               last_coordinate[0] + size // 2, last_coordinate[1] + (size // 2) - (inside_padding // 2),
                               x + size // 2, y + (size // 2) + (inside_padding // 2),
                               x + size // 2, y + size // 2), width=5, fill="#FF0000", smooth=True)
            canvas.create_oval(last_coordinate[0], last_coordinate[1], last_coordinate[2], last_coordinate[3], fill="#FF0000")
            canvas.create_text(last_coordinate[0] + size // 2, last_coordinate[1] + size // 2, text=str(last_coordinate[4]), font=("Arial", 12), fill="#FFFFFF")
        last_coordinate = (x, y, x2, y2, last_input)
    canvas.create_oval(last_coordinate[0], last_coordinate[1], last_coordinate[2], last_coordinate[3], fill="#FF0000")
    canvas.create_text(last_coordinate[0] + size // 2, last_coordinate[1] + size // 2, text=str(last_coordinate[4]), font=("Arial", 12), fill="#FFFFFF")


# used for rendering the inputs of each layer's parameters
def render_inputs():
    for layer in range(layers):
        input_frame = tk.Frame(side_bar)

        a_label = tk.Label(input_frame, text="A:")
        a_entry = tk.Scale(input_frame, from_=0, to=15, orient=tk.HORIZONTAL, length=100, command=change)

        b_label = tk.Label(input_frame, text="B:")
        b_entry = tk.Scale(input_frame, from_=0, to=15, orient=tk.HORIZONTAL, length=100, command=change)

        value_scales.append((a_entry, b_entry))

        a_mode_bool = tk.BooleanVar()
        a_mode = tk.Checkbutton(input_frame, text="A Comp/Sub", variable=a_mode_bool, command=change)

        b_mode_bool = tk.BooleanVar()
        b_mode = tk.Checkbutton(input_frame, text="B Comp/Sub", variable=b_mode_bool, command=change)

        boolean_variables.append((a_mode_bool, b_mode_bool))

        a_label.grid(column=0, row=0)
        a_entry.grid(column=1, row=0)
        b_label.grid(column=0, row=1)
        b_entry.grid(column=1, row=1)
        a_mode.grid(column=0, row=2)
        b_mode.grid(column=1, row=2)
        input_frames.append(input_frame)
        side_bar.create_window(padding, 2 * (padding + size) + (inside_padding // 2) + layer * (size + inside_padding) + y_offset - 3 * padding, anchor="w", window=input_frame)


# line_frame = tk.Canvas(master=root, width=16 * (size + padding) + padding, height=(layers + 1) * (size + inside_padding) - inside_padding + 2 * padding, bd=0, highlightthickness=0)
canvas.bind("<Button-1>", on_left_click)

render_layers()

render_inputs()

render_active_path(input_slider.get())

# line_frame.place(x=0, y=0, anchor="nw")

# canvas.pack(side="left", fill="both", expand=True)

# just placing everything dw about it ;]
root.update_idletasks()

canvas.place(x=0, y=0, anchor="nw")
side_bar.place(x=canvas.winfo_reqwidth(), y=4 * padding, anchor="nw")

input_slider.place(x=padding // 2, y=canvas.winfo_reqheight())
input_slider_button.place(x=input_slider.winfo_reqwidth() + padding, y=canvas.winfo_reqheight() + 3 * padding, anchor="w")

text_load.place(x=0, y=canvas.winfo_reqheight() + 5 * padding)
text_load_button.place(x=text_load.winfo_reqwidth(), y=canvas.winfo_reqheight() + 5 * padding - 5)

binary_output_mode.place(x=canvas.winfo_reqwidth() + 3 * padding, y=0)
unused_lines_mode.place(x=canvas.winfo_reqwidth() + 3 * padding + binary_output_mode.winfo_reqwidth(), y=0)

root.mainloop()

import tkinter as tk
import numpy as np
from matplotlib import cm, pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from utils.eval_math_fn import eval_math_fn_at
from hooke_jeeves import hooke_jeeves


def calculate():
    # get values from input
    fun = fn.get()
    eps = float(epsilon.get())
    iter_c = int(iteration_count.get())

    # Clear the figure
    fig.clear()

    # calculate plot points
    x_values = np.arange(-50, 50, 1)
    y_values = np.arange(-50, 50, 1)
    X, Y = np.meshgrid(x_values, y_values)
    Z = eval_math_fn_at(fun, (X, Y))

    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.RdBu, antialiased=False)
    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # hooke_jeeves(lambda point: eval_math_fn_at(fun, point), [-2, 2], [0.5, 0.5], 0.01)

    plt.draw()
    canvas.draw()


# GUI SETUP

# the main Tkinter window
master = tk.Tk()

# setting the title
master.title('Hooke-Jeeves Optimization')

# dimensions of the main window
master.geometry('800x800')

# labels
fn_input_label = tk.Label(master, text='f(x,y) = ')
epsilon_label = tk.Label(master, text='Minimalna długość kroku')
initial_step_label = tk.Label(master, text='Początkowa długość kroku')
iter_count = tk.Label(master, text='Maksymalna ilość iteracji')

# entry list
fn = tk.Entry(master)
epsilon = tk.Entry(master)
initial_step = tk.Entry(master)
iteration_count = tk.Entry(master)

# place labels and entry in main window
fn_input_label.pack()
fn.pack()

epsilon_label.pack()
epsilon.pack()

initial_step_label.pack()
initial_step.pack()

iter_count.pack()
iteration_count.pack()

# method choice buttons
buttons = tk.Frame(master)
tk.Button(buttons, command=calculate, height=2, width=20, text='Znajdź minimum').pack()
buttons.pack(pady=10)

# PLOT SETUP

# the figure that will contain the plot
fig = Figure(figsize=(5, 4), dpi=100)

# adding the subplot
plot = fig.add_subplot(111, projection='3d')

# creating the Tkinter canvas containing the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master)
canvas.draw()

# placing the canvas on the Tkinter window
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# creating the Matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, master)
toolbar.update()

# placing the toolbar on the Tkinter window
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# run the gui
master.mainloop()

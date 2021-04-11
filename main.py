import tkinter as tk
import numpy as np
from matplotlib import cm, pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.ticker import LinearLocator, FormatStrFormatter

from utils.plot.marker import mark_point
from utils.eval_math_fn import eval_math_fn_at
from hooke_jeeves import hooke_jeeves

max_size = 50

def calculate():
    # get values from input
    fun = fn.get()
    initial_approx = eval(initial_approximation.get())
    init_step = float(initial_step.get())
    eps_step = float(epsilon_step.get())
    eps_abs = float(epsilon_abs.get())
    iter_c = int(iteration_count.get())

    # Clear the figure
    fig.clear()

    # calculate plot points
    x_values = np.arange(-max_size, max_size, 1)
    y_values = np.arange(-max_size, max_size, 1)
    X, Y = np.meshgrid(x_values, y_values)
    Z = eval_math_fn_at(fun, (X, Y))

    # 3d visualization
    # ax = fig.gca(projection='3d')
    # ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.RdBu, antialiased=False)
    # ax.zaxis.set_major_locator(LinearLocator(10))
    # ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    # 2d contour visualization
    ax = fig.gca()
    CS = ax.contour(X, Y, Z)
    ax.clabel(CS, inline=True)

    f = lambda point: eval_math_fn_at(fun, point)
    point, value = hooke_jeeves(fun=f, u=initial_approx, h=init_step, eps_step=eps_step, eps_abs=eps_abs, max_iterations=iter_c)

    print(f'Wynik: punkt: {point}, wartość: {value}')

    mark_point(ax, point)
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
initial_approximation_label = tk.Label(master, text='Początkowe minimum: [x, y]')
initial_step_label = tk.Label(master, text='Początkowa długość kroku')
epsilon_step_label = tk.Label(master, text='Minimalna długość kroku')
epsilon_abs_label = tk.Label(master, text='Dokładność')
iteration_count_label = tk.Label(master, text='Maksymalna ilość iteracji')

# entry list
fn = tk.Entry(master)
fn.insert(index=tk.END, string='x*y')
initial_approximation = tk.Entry(master)
initial_approximation.insert(index=tk.END, string='[1, 3]')
initial_step = tk.Entry(master)
initial_step.insert(index=tk.END, string='1')
epsilon_step = tk.Entry(master)
epsilon_step.insert(index=tk.END, string='0.1')
epsilon_abs = tk.Entry(master)
epsilon_abs.insert(index=tk.END, string='0.1')
iteration_count = tk.Entry(master)
iteration_count.insert(index=tk.END, string='20')

# place labels and entry in main window
fn_input_label.pack()
fn.pack()

initial_approximation_label.pack()
initial_approximation.pack()

initial_step_label.pack()
initial_step.pack()

epsilon_step_label.pack()
epsilon_step.pack()

epsilon_abs_label.pack()
epsilon_abs.pack()

iteration_count_label.pack()
iteration_count.pack()

# method choice buttons
buttons = tk.Frame(master)
tk.Button(buttons, command=calculate, height=2, width=20, text='Znajdź minimum').pack()
buttons.pack(pady=10)

# PLOT SETUP

# the figure that will contain the plot
fig = Figure(figsize=(5, 4), dpi=100)

# 3d plot
# plot = fig.add_subplot(111, projection='3d')
# 2d contour plot
plot = fig.add_subplot(111)

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

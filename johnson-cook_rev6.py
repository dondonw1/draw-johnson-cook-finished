import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox

def johnson_cook_stress(eps, eps_dot, A, B, C, n, eps_dot_0):
    term1 = A + B * eps**n
    term2 = 1 + C * np.log(eps_dot / eps_dot_0)
    return term1 * term2 

def validate_input(value, name):
    try:
        return float(value)
    except ValueError:
        messagebox.showerror("Invalid Input", f"Please enter a valid number for {name}.")
        return None

def plot_curve():
    # Get the parameters from the input fields and validate them
    A = validate_input(entry_A.get(), "A")
    B = validate_input(entry_B.get(), "B")
    C = validate_input(entry_C.get(), "C")
    n = validate_input(entry_n.get(), "n")
    eps_dot = validate_input(entry_eps_dot.get(), "Strain rate")
    eps_dot_0 = validate_input(entry_eps_dot_0.get(), "Reference strain rate")
    curve_name = entry_curve_name.get()

    # If any input is invalid, return without plotting
    if None in (A, B, C, n, eps_dot, eps_dot_0):
        return

    # Define the strain range
    eps = np.linspace(0, 1, 500)

    # Calculate stress using Johnson-Cook model
    stress = johnson_cook_stress(eps, eps_dot, A, B, C, n, eps_dot_0)

    # Plot the stress-strain curve
    ax.plot(eps, stress, label=curve_name if curve_name else 'Johnson-Cook Model')
    ax.set_xlabel('Equivalent Plastic Strain')
    ax.set_ylabel('Equivalent Flow Stress (MPa)')
    ax.set_title('Johnson-Cook Material Law Curve')
    ax.legend()
    ax.grid(True)

    # Draw the new plot
    canvas.draw()

def create_input_field(root, text, row, default_value, variable):
    tk.Label(root, text=text).grid(row=row, column=0)
    entry = tk.Entry(root, textvariable=variable)
    variable.set(default_value)
    entry.grid(row=row, column=1)
    return entry

# Create the main window
root = tk.Tk()
root.title("Johnson-Cook Material Law Curve")

# Create StringVar variables for parameters with default values
A_var = tk.StringVar()
B_var = tk.StringVar()
C_var = tk.StringVar()
n_var = tk.StringVar()
eps_dot_var = tk.StringVar()
eps_dot_0_var = tk.StringVar()
curve_name_var = tk.StringVar()

# Create input fields for parameters with default values
entry_A = create_input_field(root, "A (MPa)", 0, "792", A_var)
entry_B = create_input_field(root, "B (MPa)", 1, "510", B_var)
entry_C = create_input_field(root, "C", 2, "0.014", C_var)
entry_n = create_input_field(root, "n", 3, "0.26", n_var)
entry_eps_dot = create_input_field(root, "Strain rate (eps_dot)", 4, "1", eps_dot_var)
entry_eps_dot_0 = create_input_field(root, "Reference strain rate (eps_dot_0)", 5, "1", eps_dot_0_var)
entry_curve_name = create_input_field(root, "Curve Name", 6, "", curve_name_var)

# Create a figure for the plot
fig, ax = plt.subplots()

# Create a canvas to display the plot in the tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=8, column=0, columnspan=2)

# Create a button to plot the curve
tk.Button(root, text="Plot Curve", command=plot_curve).grid(row=7, column=0, columnspan=2)

# Run the tkinter main loop
root.mainloop()

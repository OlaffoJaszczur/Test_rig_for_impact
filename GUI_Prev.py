import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv
import math

# Constants
GRAVITY = 9.81  # m/s^2, acceleration due to gravity

# Global variables
current_energy = 0  # In joules
mass = 2.0  # Default mass in kg

def calculate_height(energy):
    """Calculate the height from energy."""
    return energy / (mass * GRAVITY)

def calculate_drop_time(height):
    """Calculate the time it takes for the ball to drop from the given height."""
    if height <= 0:
        return 0
    return math.sqrt(2 * height / GRAVITY)

def update_plot(accelerometer_data):
    """Update the plot with accelerometer data only."""
    ax.clear()
    ax.plot(accelerometer_data, label="Accelerometer Data")
    ax.set_title("Accelerometer Data")
    ax.set_xlabel("Time (arbitrary units)")
    ax.set_ylabel("Acceleration (m/s^2)")
    ax.legend()
    canvas.draw()

def update_display():
    """Update the force and height display in the app."""
    global current_energy
    height = calculate_height(current_energy)
    force_label.config(text=f"Energy: {current_energy:.2f} J\nMass: {mass:.2f} kg\nHeight: {height:.2f} m")

def slider_changed(event=None):
    """Handle slider value changes."""
    selected_energy = slider.get()
    energy_var.set(f"{selected_energy:.2f}")  # Update the entry box with the slider value

def manual_energy_entered(event=None):
    """Handle manual energy entry."""
    try:
        selected_energy = float(energy_var.get())
        if 0 <= selected_energy <= 100:  # Energy range (adjust as needed)
            slider.set(selected_energy)  # Update the slider to match the manual entry
        else:
            energy_var.set("Invalid")  # Indicate invalid input
    except ValueError:
        energy_var.set("Invalid")  # Indicate invalid input

def change_mass(event=None):
    """Update the mass value."""
    global mass
    try:
        new_mass = float(mass_var.get())
        if new_mass > 0:
            mass = new_mass
            update_display()  # Update the display to reflect the new mass
        else:
            mass_var.set("Invalid")  # Indicate invalid input
    except ValueError:
        mass_var.set("Invalid")  # Indicate invalid input

def raise_ball():
    """Set the ball's energy and calculate the height."""
    global current_energy
    current_energy = slider.get()
    update_display()
    drop_button.config(state="normal")  # Enable the drop button

def drop_ball():
    """Reset the energy to 0 and recalculate the height."""
    global current_energy
    global drop_time, accelerometer_data
    height = calculate_height(current_energy)
    drop_time = calculate_drop_time(height)
    print("drop time:",drop_time)
    current_energy = 0  # Reset energy to 0
    update_display()
    drop_button.config(state="disabled")  # Disable the drop button

    # Simulate accelerometer data
    total_time = drop_time + 1  # Add 1 second after the drop
    print("total time:",total_time)
    sample_rate = 100  # Samples per second
    time_points = np.linspace(0, total_time, int(total_time * sample_rate))
    accelerometer_data = GRAVITY * np.ones_like(time_points)  # Constant acceleration for simplicity
    export_button.config(state="normal")  # Enable export button

def export_data():
    """Export the drop data to a CSV file."""
    global drop_time, accelerometer_data
    total_time = drop_time + 1  # Total duration
    sample_rate = 100  # Samples per second
    time_points = np.linspace(0, total_time, int(total_time * sample_rate))

    with open("drop_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Time (s)", "Acceleration (m/s^2)"])
        for t, a in zip(time_points, accelerometer_data):
            writer.writerow([t, a])

    export_button.config(state="disabled")  # Disable the export button after saving

# Simulated accelerometer data
accelerometer_data = np.array([])  # Placeholder for accelerometer data
drop_time = 0  # Placeholder for drop time

# GUI Setup
root = tk.Tk()
root.title("Raise and Drop Ball: Energy to Height Viewer")

# Configure dynamic resizing
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)  # Give the plot row the highest weight

# Main Frame
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky="ew")
main_frame.columnconfigure(1, weight=1)

slider_label = ttk.Label(main_frame, text="Set Energy (J):")
slider_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

slider = ttk.Scale(main_frame, from_=0, to=100, orient="horizontal", command=slider_changed)
slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

energy_var = tk.StringVar()
energy_entry = ttk.Entry(main_frame, textvariable=energy_var, width=10)
energy_entry.grid(row=0, column=2, padx=5, pady=5, sticky="e")
energy_entry.bind("<Return>", manual_energy_entered)  # Trigger manual input on Enter key

energy_label = ttk.Label(main_frame, text="Manual Energy Entry:")
energy_label.grid(row=0, column=3, padx=5, pady=5, sticky="e")

mass_label = ttk.Label(main_frame, text="Set Mass (kg):")
mass_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

mass_var = tk.StringVar(value=str(mass))
mass_entry = ttk.Entry(main_frame, textvariable=mass_var, width=10)
mass_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")
mass_entry.bind("<Return>", change_mass)  # Trigger mass change on Enter key

# Buttons for Raising, Dropping, and Exporting
button_frame = ttk.Frame(root, padding="10")
button_frame.grid(row=1, column=0, sticky="ew")
raise_button = ttk.Button(button_frame, text="Raise Ball", command=raise_ball)
raise_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
drop_button = ttk.Button(button_frame, text="Drop Ball", command=drop_ball, state="disabled")
drop_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
export_button = ttk.Button(button_frame, text="Export Data", command=export_data, state="disabled")
export_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

# Force and Height Display Section
force_frame = ttk.LabelFrame(root, text="Energy, Mass, and Height Calculation", padding="10")
force_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
force_frame.columnconfigure(0, weight=1)

force_label = ttk.Label(force_frame, text="Energy: 0.00 J\nMass: 1.00 kg\nHeight: 0.00 m", font=("Arial", 12))
force_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

# Configure plot row for maximum space
root.rowconfigure(3, weight=5)  # Make the plot row the largest component

# Initial plot
update_plot(accelerometer_data)

# Run the application
root.mainloop()

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
photocell_velocity = None  # Placeholder for photocell velocity data

def calculate_height(energy):
    """Calculate the height from energy."""
    return (energy / (mass * GRAVITY))

def calculate_drop_time(height):
    """Calculate the time it takes for the impactor to drop from the given height."""
    if height <= 0:
        return 0
    return math.sqrt(2 * height / GRAVITY)

def simulate_deformation_acceleration(total_time, sample_rate):
    """Simulate deformation acceleration as a damped exponential decay."""
    time_points = np.linspace(0, total_time, int(total_time * sample_rate))
    A = 200  # Initial peak acceleration (arbitrary units)
    b = 10   # Damping coefficient
    deformation_acceleration = A * np.exp(-b * time_points)
    return time_points, deformation_acceleration

def simulate_photocell_velocity(max_velocity, total_time, sample_rate):
    """Simulate photocell velocity as an exponentially decaying function."""
    time_points = np.linspace(0, total_time, int(total_time * sample_rate))
    b = 5  # Damping coefficient
    velocity = max_velocity * np.exp(-b * time_points)
    return velocity

def update_plot(time_points, deformation_acceleration):
    """Update the plot with simulated deformation acceleration."""
    ax.clear()
    ax.plot(time_points, deformation_acceleration, label="Deformation Acceleration")
    ax.set_title("Deformation Acceleration on Steel Plate")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Acceleration (arbitrary units)")
    ax.legend()
    canvas.draw()

def update_display():
    """Update the energy, mass, height, and photocell velocity display in the app."""
    global current_energy, photocell_velocity
    height = calculate_height(current_energy)
    force = mass * GRAVITY * height
    if photocell_velocity is not None:
        peak_velocity = np.max(photocell_velocity)
    else:
        peak_velocity = 0
    force_label.config(
        text=f"Energy: {current_energy:.2f} J\nMass: {mass:.2f} kg\n"
             f"Height: {height:.2f} m\nForce: {force:.2f} N\n"
             f"Photocell Peak Velocity: {peak_velocity:.2f} m/s"
    )

def slider_changed(event=None):
    """Handle slider value changes."""
    selected_energy = slider.get()
    energy_var.set(f"{selected_energy:.2f}")  # Update the entry box with the slider value

def manual_energy_entered(event=None):
    """Handle manual energy entry."""
    try:
        selected_energy = float(energy_var.get())
        if 0 <= selected_energy <= 10:  # Energy range (adjust as needed)
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

def raise_impactor():
    """Set the impactor's energy and calculate the height."""
    global current_energy
    current_energy = slider.get()
    update_display()
    drop_button.config(state="normal")  # Enable the drop button

def drop_impactor():
    """Simulate the drop and calculate the deformation and photocell velocity."""
    global current_energy, time_points, deformation_acceleration, photocell_velocity, height_before_drop, force, export_energy
    height = calculate_height(current_energy)
    height_before_drop = height
    drop_time = calculate_drop_time(height)
    force = mass * GRAVITY
    export_energy = current_energy
    current_energy = 0  # Reset energy to 0
    update_display()
    drop_button.config(state="disabled")  # Disable the drop button

    # Simulate accelerations and velocity
    total_time = drop_time + 1  # Total time for deformation (drop time + 1 second for simplicity)
    sample_rate = 100  # Samples per second
    time_points, deformation_acceleration = simulate_deformation_acceleration(total_time, sample_rate)
    max_velocity = math.sqrt(2 * GRAVITY * height)  # Maximum velocity before impact
    photocell_velocity = simulate_photocell_velocity(max_velocity, total_time, sample_rate)

    # Update the plot
    update_plot(time_points, deformation_acceleration)
    export_button.config(state="normal")  # Enable export button


def export_data():
    """Export the deformation and photocell velocity data to a CSV file."""
    global time_points, deformation_acceleration

    with open("output_data.csv", "w", newline="") as file:
        writer = csv.writer(file)
        # Write metadata as headers
        writer.writerow(["Energy (J)", "Height (m)", "Force (N)", "Mass (kg)", "Photocell Impact Velocity (m/s)"])
        writer.writerow([export_energy, height_before_drop, force, mass, np.max(photocell_velocity)])
        writer.writerow([])  # Empty row
        writer.writerow(["Time (s)", "Deformation Acceleration (arbitrary units)"])
        # Write data points
        for t, d in zip(time_points, deformation_acceleration):
            writer.writerow([t, d])

    export_button.config(state="disabled")  # Disable the export button after saving

# GUI Setup
root = tk.Tk()
root.title("Raise and Drop Impactor: Velocity Viewer")

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

slider = ttk.Scale(main_frame, from_=0, to=10, orient="horizontal", command=slider_changed)
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
raise_button = ttk.Button(button_frame, text="Raise Impactor", command=raise_impactor)
raise_button.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
drop_button = ttk.Button(button_frame, text="Drop Impactor", command=drop_impactor, state="disabled")
drop_button.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
export_button = ttk.Button(button_frame, text="Export Data", command=export_data, state="disabled")
export_button.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

# Force and Height Display Section
force_frame = ttk.LabelFrame(root, text="Energy, Mass, Height, Force, and Photocell Velocity", padding="10")
force_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
force_frame.columnconfigure(0, weight=1)

force_label = ttk.Label(force_frame, text="Energy: 0.00 J\nMass: 1.00 kg\nHeight: 0.00 m\nForce: 0.00 N\nPhotocell Peak Velocity: 0.00 m/s", font=("Arial", 12))
force_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Matplotlib Figure
fig, ax = plt.subplots(figsize=(10, 8))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

# Configure plot row for maximum space
root.rowconfigure(3, weight=5) # Make the plot row the largest component

# Run the application
root.mainloop()

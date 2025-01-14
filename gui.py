import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import csv
import numpy as np

class ImpactorSimulatorGUI:
    def __init__(self, root, simulator):
        self.simulator = simulator
        self.root = root
        self.root.title("Raise and Drop Impactor: Velocity Viewer")
        self._setup_gui()

        self.main_frame.bind("<<raise_impactor>>", self.impactor_risen)
        self.main_frame.bind("<<drop_impactor>>", self.impactor_dropped)

    def _setup_gui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="ew")
        self.main_frame.columnconfigure(1, weight=1)

        ttk.Label(self.main_frame, text="Set Energy (J):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.slider = ttk.Scale(self.main_frame, from_=0, to=10, orient="horizontal", command=self.on_slider_change)
        self.slider.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.energy_var = tk.StringVar()
        energy_entry = ttk.Entry(self.main_frame, textvariable=self.energy_var, width=10)
        energy_entry.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        energy_entry.bind("<Return>", self.on_manual_energy_entry)

        ttk.Label(self.main_frame, text="Set Mass (kg):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.mass_var = tk.StringVar(value=str(self.simulator.mass))
        mass_entry = ttk.Entry(self.main_frame, textvariable=self.mass_var, width=10)
        mass_entry.grid(row=1, column=1, padx=5, pady=5, sticky="e")
        mass_entry.bind("<Return>", self.on_mass_change)

        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, sticky="ew")
        ttk.Button(button_frame, text="Raise Impactor", command=self.raise_impactor).grid(row=0, column=0, padx=10, pady=5)
        self.drop_button = ttk.Button(button_frame, text="Drop Impactor", command=self.drop_impactor, state="disabled")
        self.drop_button.grid(row=0, column=1, padx=10, pady=5)
        self.export_button = ttk.Button(button_frame, text="Export Data", command=self.export_data, state="disabled")
        self.export_button.grid(row=0, column=2, padx=10, pady=5)

        energy_frame = ttk.LabelFrame(self.root, text="Energy, Mass, Height, Photocell Velocity and Impact Velocity", padding="10")
        energy_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.energy_label = ttk.Label(energy_frame, text="", font=("Arial", 12))
        self.energy_label.grid(row=0, column=0, padx=10, pady=10)

        fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)

    def update_plot(self):
        self.ax.clear()
        self.simulator.time_points = np.arange(1, 101)  # only for testing !
        self.ax.plot(self.simulator.time_points, self.simulator.acceleration_filtered, label="Deformation Acceleration")
        self.ax.set_title("Deformation Acceleration on Steel Plate")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Acceleration (arbitrary units)")
        self.ax.legend()
        self.canvas.draw()

    def update_display(self):
        height = self.simulator.calculations.calculate_height(self.simulator.current_energy)
        drop_time = self.simulator.calculations.calculated_drop_time(height)
        calculated_impact_velocity = self.simulator.calculations.calculated_impact_velocity(drop_time)
        peak_velocity = self.simulator.calculations.red_photocell_velocity(self.simulator.photocell_time_data) if self.simulator.photocell_velocity is not None else 0
        self.energy_label.config(
            text=f"Energy: {self.simulator.current_energy:.2f} J\nMass: {self.simulator.mass:.2f} kg\n"
                 f"Height: {height:.2f} m\n"
                 f"Photocell Peak Velocity: {peak_velocity:.2f} m/s\n"
                 f"Predicted Impact Velocity: {calculated_impact_velocity:.2f} m/s"
        )

    def on_slider_change(self, event=None):
        selected_energy = self.slider.get()
        self.energy_var.set(f"{selected_energy:.2f}")
        self.simulator.current_energy = selected_energy
        self.update_display()

    def on_manual_energy_entry(self, event=None):
        try:
            selected_energy = float(self.energy_var.get())
            if 0 <= selected_energy <= 10:
                self.slider.set(selected_energy)
                self.simulator.current_energy = selected_energy
                self.update_display()
            else:
                self.energy_var.set("Invalid")
        except ValueError:
            self.energy_var.set("Invalid")

    def on_mass_change(self, event=None):
        try:
            new_mass = float(self.mass_var.get())
            if new_mass > 0:
                self.simulator.mass = new_mass
                self.simulator.calculations.mass = new_mass  # Update the mass in calculations
                self.update_display()
            else:
                self.mass_var.set("Invalid")
        except ValueError:
            self.mass_var.set("Invalid")

    def raise_impactor(self):
        self.simulator.STM.rasie_impactor(lambda: self.main_frame.event_generate("<<raise_impactor>>"))

    def impactor_risen(self, event):
        self.drop_button.config(state="normal")

    def drop_impactor(self):
        height = self.simulator.calculations.calculate_height(self.simulator.current_energy)
        self.simulator.height_before_drop = height
        self.simulator.export_energy = self.simulator.current_energy
        self.simulator.current_energy = 0

        def data_received(photocell_time_data, time_table, acceleration_table):
            self.simulator.photocell_time_data = photocell_time_data
            self.simulator.time_points = time_table
            self.simulator.acceleration = acceleration_table
            self.main_frame.event_generate("<<drop_impactor>>")

        self.simulator.STM.drop_impactor(data_received)

    def impactor_dropped(self, event):
        # print(self.simulator.time_points)
        # print(self.simulator.acceleration)
        # print(self.simulator.photocell_time_data)

        self.drop_button.config(state="disabled")
        self.export_button.config(state="normal")

        self.simulator.photocell_velocity = self.simulator.calculations.red_photocell_velocity(self.simulator.photocell_time_data)

        self.update_display()

        self.simulator.acceleration_filtered = self.simulator.calculations.lowpass_filter(self.simulator.acceleration, 0.3, 16000, 5)
        print(self.simulator.acceleration_filtered)

        self.update_plot()

    def export_data(self):
        file_path = os.path.join("data", "output_data.csv")
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Energy (J)", "Height (m)", "Mass (kg)", "Photocell Impact Velocity (m/s)", "Predicted Impact Velocity (m/s)"])
            writer.writerow([self.simulator.export_energy, self.simulator.height_before_drop, self.simulator.mass, self.simulator.calculations.calculated_impact_velocity(self.simulator.calculations.calculated_drop_time(self.simulator.height_before_drop)), self.simulator.calculations.calculated_impact_velocity(self.simulator.calculated_drop_time(self.simulator.height_before_drop))])
            writer.writerow([])
            writer.writerow(["Time (s)", "Deformation Acceleration (arbitrary units)", "Filtered Acceleration (arbitrary units)"])
            for t, ra, fa in zip(self.simulator.time_points, self.simulator.acceleration, self.simulator.acceleration_filtered):
                writer.writerow([t, ra, fa])
        self.export_button.config(state="disabled")
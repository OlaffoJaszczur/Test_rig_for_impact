import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import csv
import time

class ImpactorSimulatorGUI:
    def __init__(self, root, simulator):
        self.simulator = simulator
        self.root = root
        self.root.title("Raise and Drop Impactor: Velocity Viewer")
        self._setup_gui()

        self.main_frame.bind("<<raise_impactor>>", self.impactor_risen)
        self.main_frame.bind("<<drop_impactor>>", self.impactor_dropped)

        self.file_path = os.path.join(os.path.dirname(__file__), 'only_for_testing', 'data_from_simulation',
                                      'acc_sim_1_m.csv')

    def _setup_gui(self):
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

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

        button_frame = ttk.Frame(self.main_frame, padding="10")
        button_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        ttk.Button(button_frame, text="Raise Impactor", command=self.raise_impactor).grid(row=0, column=0, padx=10, pady=5)
        self.drop_button = ttk.Button(button_frame, text="Drop Impactor", command=self.drop_impactor, state="disabled")
        self.drop_button.grid(row=0, column=1, padx=10, pady=5)
        self.export_button = ttk.Button(button_frame, text="Export Data", command=self.export_data, state="disabled")
        self.export_button.grid(row=0, column=2, padx=10, pady=5)

        energy_frame = ttk.LabelFrame(self.main_frame, text="Energy, Mass, Height, Photocell Velocity and Predicted Impact Velocity", padding="10")
        energy_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
        energy_frame.columnconfigure(0, weight=1)
        energy_frame.rowconfigure(0, weight=1)
        self.energy_label = ttk.Label(energy_frame, text="", font=("Arial", 12))
        self.energy_label.grid(row=0, column=0, padx=10, pady=10)

        fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=10, pady=10)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.root.rowconfigure(2, weight=3)
        self.root.rowconfigure(3, weight=2)

    def update_plot(self):
        self.ax.clear()
        self.ax.plot(self.test_time, 2*self.simulator.acceleration_filtered, label="Deformation Acceleration")
        self.ax.set_title("Deformation Acceleration on Steel Plate")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Acceleration (m/s²)")
        self.ax.legend()
        self.canvas.draw()

    def update_display(self):
        height = self.simulator.calculations.calculate_height(self.simulator.current_energy)
        drop_time = self.simulator.calculations.calculated_drop_time(height)
        calculated_impact_velocity = self.simulator.calculations.calculated_impact_velocity(drop_time)
        peak_velocity = self.simulator.photocell_velocity if self.simulator.photocell_velocity is not None else 0
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
        height = self.simulator.calculations.calculate_height(self.simulator.current_energy)
        self.simulator.STM.rasie_impactor(lambda: self.main_frame.event_generate("<<raise_impactor>>"), height)

    def impactor_risen(self, event):
        # time.sleep(3)
        self.drop_button.config(state="normal")

    def drop_impactor(self):
        height = self.simulator.calculations.calculate_height(self.simulator.current_energy)
        self.simulator.height_before_drop = height
        self.simulator.export_energy = self.simulator.current_energy
        self.simulator.current_energy = 0

        def data_received(photocell_time_data, time_table):
            self.simulator.photocell_time_data = photocell_time_data
            self.simulator.time_points = time_table
            self.main_frame.event_generate("<<drop_impactor>>")

        self.simulator.STM.drop_impactor(data_received)

    def impactor_dropped(self, event):
        # print(self.simulator.time_points)
        # print(self.simulator.acceleration)
        # print(self.simulator.photocell_time_data)

        self.drop_button.config(state="disabled")
        self.export_button.config(state="normal")

        self.simulator.photocell_velocity = self.simulator.photocell_time_data
        # print(self.simulator.photocell_velocity)

        [self.test_time, self.test_acceleration] = self.simulator.calculations.read_csv(self.file_path)
        # print(self.test_time)
        # print(self.test_acceleration)

        self.update_display()

        self.simulator.acceleration_filtered = self.simulator.calculations.bandpass_filter(self.test_acceleration, 100, 2000, 2) # (data, lowcut, highcut, order), simulation (data, 0.001, 2, 20000, 2)
        # print(self.simulator.acceleration_filtered)

        time.sleep(2)
        self.update_plot()

    def export_data(self):
        file_path = os.path.join(os.path.dirname(__file__), 'data', "output_data.csv")
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Energy (J)", "Height (m)", "Mass (kg)", "Photocell Impact Velocity (m/s)", "Predicted Impact Velocity (m/s)"])
            # writer.writerow([round(self.simulator.export_energy, 3), round(self.simulator.height_before_drop, 3), self.simulator.mass, round(self.simulator.calculations.red_photocell_velocity(self.simulator.photocell_time_data), 3), round(self.simulator.calculations.calculated_impact_velocity(self.simulator.calculated_drop_time(self.simulator.height_before_drop)), 3)])
            writer.writerow([round(self.simulator.export_energy, 3), round(self.simulator.height_before_drop, 3), self.simulator.mass, round(self.simulator.photocell_velocity, 3), round(self.simulator.calculations.calculated_impact_velocity(self.simulator.calculated_drop_time(self.simulator.height_before_drop)), 3)])
            writer.writerow([])
            writer.writerow(["Time (s)", "Deformation Acceleration (m/s^2)", "Filtered Acceleration (m/s^2)"])
            for t, ra, fa in zip(self.test_time, self.test_acceleration, self.simulator.acceleration_filtered):
                writer.writerow([t, ra, fa])
        self.export_button.config(state="disabled")
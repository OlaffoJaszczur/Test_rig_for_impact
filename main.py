import tkinter as tk
from calculations import ImpactorSimulatorCalculations
from gui import ImpactorSimulatorGUI
from STM_Interaction_no_acceleration import STMDataInteraction



class ImpactorSimulator:
    def __init__(self):
        self.GRAVITY = 9.81  # m/s^2, acceleration due to gravity
        self.current_energy = 0
        self.mass = 1.0
        self.photocell_velocity = None
        self.height_before_drop = 0
        self.export_energy = 0

        self.calculations = ImpactorSimulatorCalculations(self.mass, self.GRAVITY)
        self.STM = STMDataInteraction()

        # Initialize GUI components
        self.root = tk.Tk()
        self.gui = ImpactorSimulatorGUI(self.root, self)

    def calculate_height(self, energy):
        return self.calculations.calculate_height(energy)

    def calculated_drop_time(self, height):
        return self.calculations.calculated_drop_time(height)

    def calculated_impact_velocity(self, calculated_drop_time):
        return self.calculations.calculated_impact_velocity(calculated_drop_time)



    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ImpactorSimulator()
    app.run()
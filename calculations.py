import math
import numpy as np

class ImpactorSimulatorCalculations:
    GRAVITY = 9.81  # m/s^2, acceleration due to gravity

    def __init__(self, mass):
        self.mass = mass

    def calculate_height(self, energy):
        return energy / (self.mass * self.GRAVITY)

    def calculate_drop_time(self, height):
        return math.sqrt(2 * height / self.GRAVITY) if height > 0 else 0

    def simulate_deformation_acceleration(self, total_time, sample_rate):
        time_points = np.linspace(0, total_time, int(total_time * sample_rate))
        A, b = 200, 10  # Peak acceleration and damping coefficient
        return time_points, A * np.exp(-b * time_points)

    def simulate_photocell_velocity(self, max_velocity, total_time, sample_rate):
        time_points = np.linspace(0, total_time, int(total_time * sample_rate))
        b = 5  # Damping coefficient
        return max_velocity * np.exp(-b * time_points)
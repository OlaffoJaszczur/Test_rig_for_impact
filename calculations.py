import math
import numpy as np

class ImpactorSimulatorCalculations:

    def __init__(self, mass, GRAVITY):
        self.mass = mass
        self.GRAVITY = GRAVITY

    def calculate_height(self, energy):
        return energy / (self.mass * self.GRAVITY)

    def calculated_drop_time(self, height): # h = 1/2gt^2
        return math.sqrt(2 * height / self.GRAVITY) if height > 0 else 0

    def calculated_impact_velocity(self, calculated_drop_time):
        return self.GRAVITY * calculated_drop_time

    def red_photocell_velocity(self, photocell_time_data):
        return self.GRAVITY * photocell_time_data  # probably will have to change as time will be provided in milisecons

 #   def low_pass_filter(self, ):

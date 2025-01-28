import numpy as np
from numpy.fft import fft
from scipy.signal import butter, lfilter

class ImpactorSimulatorCalculations:

    def __init__(self, mass, GRAVITY):
        self.mass = mass
        self.GRAVITY = GRAVITY

        self.fs = 1 / (self.time_data[1] - self.time_data[0])
        self.lowcut = 100.0
        self.highcut = 2000.0

    def calculate_height(self, energy):
        return energy / (self.mass * self.GRAVITY)

    def calculated_drop_time(self, height): # h = 1/2gt^2
        return np.sqrt(2 * height / self.GRAVITY) if height > 0 else 0

    def calculated_impact_velocity(self, calculated_drop_time):
        return self.GRAVITY * calculated_drop_time

    def red_photocell_velocity(self, photocell_time_data):
        return self.GRAVITY * photocell_time_data  # probably will have to change as time will be provided in milisecons

    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        b, a = butter(order, [lowcut, highcut], fs=fs, btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut, order=2):
        fs = self.fs
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        self.filtered_data = lfilter(b, a, data)
        return self.filtered_data

    # zrobic band pass 100Hz to 200kHz
    # pasmo można wiziąc z symulacji od grzesia
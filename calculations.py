import numpy as np
from scipy.signal import butter, filtfilt

class ImpactorSimulatorCalculations:

    def __init__(self, mass, GRAVITY):
        self.mass = mass
        self.GRAVITY = GRAVITY

    def calculate_height(self, energy):
        return energy / (self.mass * self.GRAVITY)

    def calculated_drop_time(self, height): # h = 1/2gt^2
        return np.sqrt(2 * height / self.GRAVITY) if height > 0 else 0

    def calculated_impact_velocity(self, calculated_drop_time):
        return self.GRAVITY * calculated_drop_time

    def red_photocell_velocity(self, photocell_time_data):
        return self.GRAVITY * photocell_time_data  # probably will have to change as time will be provided in milisecons

    # def butter_lowpass(self, lowcut, highcut, fs, order):
    #     nyq = 0.5 * fs  # Nyquist Frequency
    #     low = lowcut / nyq
    #     high = highcut / nyq
    #     b, a = butter(order, [low, high], btype='band', analog=False)
    #     return b, a
    #
    # def lowpass_filter(self, data, cutoff, fs, order):
    #     print(data, cutoff, fs, order)
    #     data = np.arange(1,101) # only for testing !
    #     print(data)
    #     self.b, self.a = self.butter_lowpass(cutoff, fs, order)
    #     self.filtered_data = filtfilt(self.b, self.a, data)
    #     return np.abs(self.filtered_data)
    #
    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        nyq = 0.5 * fs  # Nyquist Frequency
        low = lowcut / nyq
        high = highcut / nyq
        b, a = butter(order, [low, high], btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut, fs, order=2):
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        self.filtered_data = filtfilt(b, a, data)
        return np.abs(self.filtered_data)

    # zrobic band pass 100Hz to 200kHz
    # pasmo można wiziąc z symulacji od grzesia

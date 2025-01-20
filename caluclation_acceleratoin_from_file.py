import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy.signal import butter, lfilter

class ImpactorSimulatorCalculations:

    def __init__(self, mass, GRAVITY):
        self.mass = mass
        self.GRAVITY = GRAVITY
        self.file_path = os.path.join(os.path.dirname(__file__), 'only_for_testing', 'data_from_simulation', 'tabelkaAcceleration.csv')
        self.time_data, self.acceleration_data = self.read_csv(self.file_path)

        # Sampling frequency (fs)
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

    def read_csv(self, file_path):
        self.time_data = []
        self.acceleration_data = []

        with open(self.file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                self.time_data.append(float(row['Time']))
                self.acceleration_data.append(float(row['Acceleration']))

        return np.array(self.time_data), np.array(self.acceleration_data)

    def butter_bandpass(self, lowcut, highcut, fs, order=2):
        b, a = butter(order, [lowcut, highcut], fs=fs, btype='band')
        return b, a

    def bandpass_filter(self, data, lowcut, highcut, order=2):
        fs = self.fs
        b, a = self.butter_bandpass(lowcut, highcut, fs, order=order)
        self.filtered_data = lfilter(b, a, data)
        return self.filtered_data

# def plot_time_vs_acceleration(time_data, acceleration_data, filtered_data):
#     plt.figure(figsize=(12, 6))
#     plt.subplot(2, 1, 1)
#     plt.plot(time_data, acceleration_data, label='Original Acceleration Data')
#     plt.title('Time vs. Acceleration')
#     plt.xlabel('Time (s)')
#     plt.ylabel('Acceleration (m/s²)')
#     plt.legend()
#
#     plt.subplot(2, 1, 2)
#     plt.plot(time_data, 2*filtered_data, label='Filtered Acceleration Data')
#     plt.title('Time vs. Filtered Acceleration')
#     plt.xlabel('Time (s)')
#     plt.ylabel('Acceleration (m/s²)')
#     plt.legend()
#
#     plt.tight_layout()
#     plt.show()
#
# def plot_frequency_spectrum(time_data, acceleration_data, fs):
#     N = len(acceleration_data)
#     T = time_data[1] - time_data[0]  # Assuming uniform sampling
#     fft_values = np.fft.fft(acceleration_data)
#     fft_freq = np.fft.fftfreq(N, T)
#
#
#     plt.figure(figsize=(12, 6))
#     plt.plot(fft_freq[:N//2], np.abs(fft_values)[:N//2], label='FFT Amplitude')
#     plt.title('Frequency Spectrum')
#     plt.xlabel('Frequency (Hz)')
#     plt.ylabel('Amplitude')
#     plt.legend()
#
#     plt.tight_layout()
#     plt.show()

# Read the data from the CSV file
# file_path = os.path.join(os.path.dirname(__file__), '..', 'data_from_simulation', 'tabelkaAcceleration.csv')
# time_data, acceleration_data = read_csv(file_path)
#
# # Sampling frequency (fs)
# fs = 1 / (time_data[1] - time_data[0])
# print(fs)
#
# lowcut = 100.0
# highcut = 2000.0
#
# # Plot the time vs. acceleration data and the filtered data
# filtered_data = bandpass_filter(acceleration_data, lowcut, highcut, fs)
# plot_time_vs_acceleration(time_data, acceleration_data, filtered_data)
#
# # Plot the frequency spectrum and the IFFT of the filtered data
# plot_frequency_spectrum(time_data, acceleration_data, fs)
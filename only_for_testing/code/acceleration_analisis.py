import numpy as np
import matplotlib.pyplot as plt
import csv
import os

def read_csv(file_path):
    time_data = []
    acceleration_data = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time_data.append(float(row['Time']))
            acceleration_data.append(float(row['Acceleration']))

    return np.array(time_data), np.array(acceleration_data)

def plot_time_vs_acceleration(time_data, acceleration_data):
    plt.figure(figsize=(12, 6))
    plt.plot(time_data, acceleration_data, label='Acceleration Data')
    plt.title('Time vs. Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()
    plt.show()

def plot_frequency_spectrum(time_data, acceleration_data):
    N = len(acceleration_data)
    T = time_data[1] - time_data[0]  # Assuming uniform sampling
    fft_values = np.fft.fft(acceleration_data)
    fft_freq = np.fft.fftfreq(N, T)

    plt.figure(figsize=(12, 6))
    plt.plot(fft_freq[:N//2], np.abs(fft_values)[:N//2], label='FFT Amplitude')
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

# Read the data from the CSV file
file_path = os.path.join(os.path.dirname(__file__), '..', 'data_from_simulation', 'tabelkaAcceleration.csv')
time_data, acceleration_data = read_csv(file_path)

# Plot the time vs. acceleration data
plot_time_vs_acceleration(time_data, acceleration_data)

# Plot the frequency spectrum
plot_frequency_spectrum(time_data, acceleration_data)


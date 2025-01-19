import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from scipy.signal import butter, lfilter
from scipy.fftpack import rfft, irfft, fftfreq

def read_csv(file_path):
    time_data = []
    acceleration_data = []

    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            time_data.append(float(row['Time']))
            acceleration_data.append(float(row['Acceleration']))

    return np.array(time_data), np.array(acceleration_data)

def butter_bandpass(lowcut, highcut, fs, order=2):
    b, a = butter(order, [lowcut, highcut], fs=fs, btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=2):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def plot_time_vs_acceleration(time_data, acceleration_data, filtered_data):
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time_data, acceleration_data, label='Original Acceleration Data')
    plt.title('Time vs. Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time_data, 2*filtered_data, label='Filtered Acceleration Data')
    plt.title('Time vs. Filtered Acceleration')
    plt.xlabel('Time (s)')
    plt.ylabel('Acceleration (m/s²)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_frequency_spectrum(time_data, acceleration_data, fs):
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

    plt.tight_layout()
    plt.show()

# Read the data from the CSV file
file_path = os.path.join(os.path.dirname(__file__), '..', 'data_from_simulation', 'tabelkaAcceleration.csv')
time_data, acceleration_data = read_csv(file_path)

# Sampling frequency (fs)
fs = 1 / (time_data[1] - time_data[0])
print(fs)

lowcut = 100.0
highcut = 2000.0

# Plot the time vs. acceleration data and the filtered data
filtered_data = bandpass_filter(acceleration_data, lowcut, highcut, fs)
plot_time_vs_acceleration(time_data, acceleration_data, filtered_data)

# Plot the frequency spectrum and the IFFT of the filtered data
plot_frequency_spectrum(time_data, acceleration_data, fs)
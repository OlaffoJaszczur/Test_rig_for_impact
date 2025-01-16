import serial
import keyboard
import time

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 38400)

# try:
#     print("Press any key to stop...")
#     while not keyboard.is_pressed(hotkey='esc'):
#         if ser.in_waiting > 0:
#             data = ser.read(ser.in_waiting)
#             print(data.decode('utf-8'), end='')
# finally:
#     ser.close()
#     print("\nSerial connection closed.")

start_time = time.time()
elapsed_time = 0

try:
    print("Reading data for 5 seconds...")
    while elapsed_time < 5:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(data.decode('US-ASCII'), end='')
        elapsed_time = time.time() - start_time
finally:
    ser.close()
    print(f"\nSerial connection closed. Elapsed time: {elapsed_time:.2f} seconds.")
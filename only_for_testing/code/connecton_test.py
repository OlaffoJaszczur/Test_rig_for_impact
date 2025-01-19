import serial
import time

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)

try:
    # Read data from the serial port for the first 3 seconds
    start_time = time.time()
    elapsed_time = 0
    print("Reading data for the first 3 seconds...")
    while elapsed_time < 3:
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(data.decode('utf-8'), end='')
        elapsed_time = time.time() - start_time


    start_time = time.time()
    elapsed_time = 0
    print("Sending 1 to the serial port for 3 seconds...")
    while elapsed_time < 3:
        ser.write(int(1).to_bytes(8, 'big'))
        elapsed_time = time.time() - start_time


    # Read data from the serial port for the next 3 seconds
    start_time = time.time()
    elapsed_time = 0
    print("\nReading data for the next 3 seconds...")
    while elapsed_time < 3:
        if ser.in_waiting > 0:
            data = int.from_bytes(ser.read(ser.in_waiting), 'big')
            print(data)
        elapsed_time = time.time() - start_time
finally:
    ser.close()
    print("\nSerial connection closed.")
import serial
import keyboard

# Initialize the serial connection
ser = serial.Serial('USART2', 38400)

try:
    print("Press any key to stop...")
    while not keyboard.is_pressed():
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(data.decode('utf-8'), end='')
finally:
    ser.close()
    print("\nSerial connection closed.")
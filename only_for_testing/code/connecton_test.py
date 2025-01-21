import serial

# Initialize the serial connection
ser = serial.Serial('/dev/ttyUSB0', 115200)
# ser = serial.Serial('/dev/ttyACM0', 115200)
try:

    byte_length = 4

    print("red data")
    aaa_bytes = ser.read(byte_length)
    print(aaa_bytes)
    aaa= int.from_bytes(aaa_bytes, 'little')
    print(aaa)
    float_value = aaa / 1000
    print(float_value)

finally:
    ser.close()
    print("\nSerial connection closed.")
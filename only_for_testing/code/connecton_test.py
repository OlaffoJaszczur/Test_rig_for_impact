import serial

# Initialize the serial connection
# ser = serial.Serial('/dev/ttyUSB0', 115200)
ser = serial.Serial('/dev/ttyACM0', 115200)
try:
    data = 1234
    byte_length = 4
    serial_write = ser.write(int(data).to_bytes(byte_length, 'big'))
    print(data)
    print(int(data).to_bytes(byte_length, 'big'))
    print('writen data over serial')

    print("red data")
    aaa = ser.read(byte_length)
    print(aaa)
    aaa_bytes = int.from_bytes(aaa, 'big')
    print(aaa_bytes)

finally:
    ser.close()
    print("\nSerial connection closed.")
import threading
import serial

# This is a mock class for the serial connection, to be used for debugging
class Mock_serial:
    def write(self, data):
        print(data)

    def read(self, size):
        value = int(input())

        return value.to_bytes(size, 'big')

    def close(self):
        pass

class STMDataInteraction:
    def __init__(self):
        #self.serial = serial.Serial('/dev/ttyUSB0', 38400) # need to later change this, for naw using mock serial for debugging
        self.serial = Mock_serial() # to be replaced !!!
        self.thread = None

    def _wait_for_data(self, experiment_ended):
        self.serial.write(int(5678).to_bytes(8, 'big'))
        self.serial.read(8)
        acceleration_table = []

        while True:
            last_acceleration_sample = int.from_bytes(self.serial.read(4), 'big')

            if last_acceleration_sample == 000:
                end_time = int.from_bytes(self.serial.read(4), 'big')
                photocell_time_data = int.from_bytes(self.serial.read(4), 'big')
                experiment_ended(photocell_time_data, end_time, acceleration_table)
                break

            acceleration_table.append(last_acceleration_sample)


    def _do_raise_impactor(self, on_raised, height):
        self.serial.write(int(1234).to_bytes(8, 'big'))
        self.serial.read(8)
        height = int(height * 1000)
        print(height)
        self.serial.write(height.to_bytes(8, 'big'))
        self.serial.read(8)
        on_raised()

    def rasie_impactor(self, on_raised, height):
        if self.thread is not None:
            self.thread.join()
        self.thread = threading.Thread(target=self._do_raise_impactor, args=(on_raised, height))
        self.thread.start()

    def drop_impactor(self, experiment_ended):
        if self.thread is not None:
            self.thread.join()
        self.thread = threading.Thread(target=self._wait_for_data, args=(experiment_ended,))
        self.thread.start()

    def __del__(self):
        self.serial.close()
        if self.thread is not None:
            self.thread.join()
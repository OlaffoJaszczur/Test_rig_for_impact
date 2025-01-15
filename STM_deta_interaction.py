import threading
import serial

class Mock_serial:
    def write(self, data):
        print(data)

    def read(self, size):
        value = int(input())

        return value.to_bytes(size, 'big')

class STMDataInteraction:
    def __init__(self):
        #self.serial = serial.Serial('COM3', 9600) nee to later change this, for naw using mock fo rdebuging
        self.serial = Mock_serial()
        self.thread = None

    def _wait_for_data(self, experiment_ended):
        self.serial.write(b'2')
        time_table = []
        acceleration_table = []

        while True:
            last_time_sample = int.from_bytes(self.serial.read(4), 'big')
            last_acceleration_sample = int.from_bytes(self.serial.read(4), 'big')

            if last_time_sample == 000 and last_acceleration_sample == 000:
                photocell_time_data = int.from_bytes(self.serial.read(4), 'big')
                experiment_ended(photocell_time_data, time_table, acceleration_table)
                break

            time_table.append(last_time_sample)
            acceleration_table.append(last_acceleration_sample)


    def _do_raise_impactor(self, on_raised):
        self.serial.write(b'1')
        self.serial.read(1)
        on_raised()

    def rasie_impactor(self, on_raised):
        if self.thread is not None:
            self.thread.join()
        self.thread = threading.Thread(target=self._do_raise_impactor, args=(on_raised,))
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
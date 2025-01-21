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

class Even_Worse_Mock_serial:
    def write(self, data):
        pass

    def read(self, size):
        pass

    def close(self):
        pass


class STMDataInteraction:
    def __init__(self):
        self.serial = serial.Serial('/dev/ttyUSB0', 115200) # need to later change this, for naw using mock serial for debugging
        self.serial_mock = Mock_serial() # to be replaced !!!
        self.serial_mock_worse = Even_Worse_Mock_serial() # to be replaced even more !!!
        # self.serial = serial.Serial('/dev/ttyACM0', 115200)
        self.thread = None

    def _wait_for_data(self, experiment_ended):
        # self.serial.write(int(456).to_bytes(4, 'big'))
        # self.serial.read(8)
        # flaga_eksperimet_start = self.serial.read(4)
        # flaga_eksperimet_start = int.from_bytes(flaga_eksperimet_start, 'big')
        # print(flaga_eksperimet_start)

        # aaa
        photocell_time_data = int.from_bytes(self.serial.read(4), 'little')
        photocell_time_data = photocell_time_data/1000
        # photocell_time_data = 4467 / 1000
        print(photocell_time_data)
        # end_time = int.from_bytes(self.serial.read(4), 'big')
        end_time = 2
        print(end_time)

        experiment_ended(photocell_time_data, end_time)

        # flaga_eksperimet_end = self.serial.read(8)
        # flaga_eksperimet_end = int.from_bytes(flaga_eksperimet_end, 'big')
        # print(flaga_eksperimet_end)


    def _do_raise_impactor(self, on_raised, height):
        self.serial_mock_worse.write(int(1234).to_bytes(4, 'big'))
        # self.serial.read(8)

        # debug
        # flaga_odioracza_1234 = self.serial.read(4)
        # print(flaga_odioracza_1234)
        # flaga_odioracza_1234 = int.from_bytes(flaga_odioracza_1234, 'big')
        # print(flaga_odioracza_1234)

        height = int(height * 1000)
        print(height)
        self.serial_mock_worse.write(height.to_bytes(4, 'big'))
        # self.serial.read(8)
        # flaga_odioracza_inpacktor_rased = self.serial.read(4)
        # flaga_odioracza_inpacktor_rased = int.from_bytes(flaga_odioracza_inpacktor_rased, 'big')
        # print(flaga_odioracza_inpacktor_rased)
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
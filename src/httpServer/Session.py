import time


class Session:
    def __init__(self, name, value, time_size=30):
        self.__name = name
        self.__value = value
        self.__time = time_size
        self.__lost_time = time.time()

    def get_value(self):
        return self.__value

from color import Color
from error import InputError


class Roll:
    def __init__(self, value):
        self.value = value
        if value == 0:
            self.color = Color.green
        elif 0 < value < 8:
            self.color = Color.red
        elif 7 < value < 15:
            self.color = Color.black
        else:
            raise InputError('Invalid roll value provided.')

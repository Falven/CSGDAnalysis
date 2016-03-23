from html.parser import HTMLParser
import datetime


def valid_date(date_str):
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


class DateParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.dates = []

    def handle_data(self, data):
        if self.lasttag == 'td' and valid_date(data):
            self.dates.append(data)

from html.parser import HTMLParser
from roll import Roll


class RollParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.inResult = False
        self.rolls = []

    def handle_starttag(self, tag, attrs):
        if tag == 'td':
            for attr in attrs:
                if attr[1] and 'td-val' in attr[1]:
                    self.inResult = True

    def handle_endtag(self, tag):
        if tag == 'td':
            self.inResult = False

    def handle_data(self, data):
        if self.lasttag == 'td' and self.inResult:
            self.rolls.append(Roll(int(data)))

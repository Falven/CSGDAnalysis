import urllib.request
import dateparser
from rollparser import RollParser
from rollanalyzer import RollAnalyzer


domain = 'http://www.csgodouble.com/rolls.php?date='
default_charset = 'utf-8'


class AlgorithmResults:
    def __init__(self, max_balance):
        self.max_balance = 0


date = input('Enter date to analyze in YYYY-MM-DD format: ')
while not dateparser.valid_date(date):
    date = input('Invalid date. Please enter a date to analyze in YYYY-MM-DD format: ')
with urllib.request.urlopen(domain + date) as resource:
    charset = resource.headers.get_content_charset()
    if charset is None:
        charset = default_charset
    content = resource.read().decode(charset)
    parser = RollParser()
    parser.feed(content)
    analyzer = RollAnalyzer(parser.rolls)
    if 'y' in input('Run basic stats? '):
        analyzer.print_basic_stats()
    verbose = False
    if 'y' in input('Verbose? '):
        verbose = True
    martingale = False
    if 'y' in input('Experimental martingale? '):
        martingale = True
    consecutives = int(input('Enter number of consecutives before bet: '))
    initial_balance = int(input('Enter initial balance: '))
    initial_bet = int(input('Enter initial bet: '))
    total_max_balance = 0
    average_max_balance = 0
    max_max_balance = 0
    total_games = 0
    min_balance_count = 0
    while analyzer.rolls:
        analysis_result = analyzer.run_falv_alg(verbose, martingale, initial_balance, initial_bet, consecutives)
        total_games += 1
        analyzer.rolls = analyzer.rolls[analysis_result.rolls_processed:]
        total_max_balance += analysis_result.max_balance
        if analysis_result.max_balance == initial_balance:
            min_balance_count += 1
        max_max_balance = max(max_max_balance, analysis_result.max_balance)
        print('rolls = ' + str(analysis_result.rolls_processed) +
              ', max_balance = ' + str(analysis_result.max_balance))
    parser.close()

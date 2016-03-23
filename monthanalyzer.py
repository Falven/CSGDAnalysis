import urllib.request
import datetime
import dateparser
from rollparser import RollParser
from rollanalyzer import RollAnalyzer


base_domain = 'http://www.csgodouble.com/rolls.php'
date_domain = base_domain + '?date='
default_charset = 'utf-8'

initial_balance = int(input('Enter initial balance: '))
initial_bet = int(input('Enter initial bet: '))
consecutives = int(input('Enter number of consecutives before bet: '))
martingale = False
if 'y' in input('\nExperimental martingale? '):
    martingale = True
with urllib.request.urlopen(base_domain) as dates_resource:
    charset = dates_resource.headers.get_content_charset()
    if charset is None:
        charset = default_charset
    content = dates_resource.read().decode(charset)
    date_parser = dateparser.DateParser()
    date_parser.feed(content)
    total_max_balance = 0
    average_max_balance = 0
    max_max_balance = 0
    total_games = 0
    min_balance_count = 0
    for date in date_parser.dates:
        with urllib.request.urlopen(date_domain + date) as resource:
            charset = resource.headers.get_content_charset()
            if charset is None:
                charset = default_charset
            content = resource.read().decode(charset)
            roll_parser = RollParser()
            roll_parser.feed(content)
            analyzer = RollAnalyzer(roll_parser.rolls)
            while analyzer.rolls:
                analysis_result = analyzer.run_falv_alg(False, martingale, initial_balance, initial_bet, consecutives)
                total_games += 1
                analyzer.rolls = analyzer.rolls[analysis_result.rolls_processed:]
                total_max_balance += analysis_result.max_balance
                if analysis_result.max_balance == initial_balance:
                    min_balance_count += 1
                max_max_balance = max(max_max_balance, analysis_result.max_balance)
                print(date + ': rolls = ' + str(analysis_result.rolls_processed) +
                      ', max_balance = ' + str(analysis_result.max_balance))
            roll_parser.close()
    average_max_balance = total_max_balance / total_games
    print('Average max_balance = ', average_max_balance)
    print('Max max_balance = ', max_max_balance)
    print('Number of times ended with initial_balance = ' + str(min_balance_count) +
          ' / ' + str(total_games) + ' = ' + str(min_balance_count/total_games))
    date_parser.close()

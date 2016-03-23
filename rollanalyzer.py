from color import Color
from analysisresult import AnalysisResult


class RollAnalyzer:
    def __init__(self, rolls):
        self.rolls = rolls

    @staticmethod
    def __lookup_increment(lookup, value):
        if value not in lookup.keys():
            lookup[value] = 0
        lookup[value] += 1

    def print_basic_stats(self):
        # Number of repetitive times there were each color.
        # ex: 0 reds in a row, 1 reds in a row, 2...
        red_repetition_lookup = {}
        green_repetition_lookup = {}
        black_repetition_lookup = {}
        red_count = 0
        green_count = 0
        black_count = 0
        repeated_reds = 0
        repeated_greens = 0
        repeated_blacks = 0
        for roll in self.rolls:
            if roll.color is Color.green:
                green_count += 1
                repeated_greens += 1
                if repeated_reds > 0:
                    self.__lookup_increment(red_repetition_lookup, repeated_reds)
                    repeated_reds = 0
                if repeated_blacks > 0:
                    self.__lookup_increment(black_repetition_lookup, repeated_blacks)
                    repeated_blacks = 0
            elif roll.color is Color.red:
                red_count += 1
                repeated_reds += 1
                if repeated_greens > 0:
                    self.__lookup_increment(green_repetition_lookup, repeated_greens)
                    repeated_greens = 0
                if repeated_blacks > 0:
                    self.__lookup_increment(black_repetition_lookup, repeated_blacks)
                    repeated_blacks = 0
            else:
                if roll.color is Color.black:
                    black_count += 1
                    repeated_blacks += 1
                    if repeated_reds > 0:
                        self.__lookup_increment(red_repetition_lookup, repeated_reds)
                        repeated_reds = 0
                    if repeated_greens > 0:
                        self.__lookup_increment(green_repetition_lookup, repeated_greens)
                        repeated_greens = 0

        print('Total number of Reds: ', red_count)
        print('Total number of Greens: ', green_count)
        print('Total number of Blacks: ', black_count)
        print('Total recorded Rolls: ', len(self.rolls), end='\n\n')
        print('Red repetition: ')
        for key, value in red_repetition_lookup.items():
            print('There were ' + str(key) + ' reds in a row ' + str(value) + ' times.')
        print('\nGreen repetition: ')
        for key, value in green_repetition_lookup.items():
            print('There were ' + str(key) + ' greens in a row ' + str(value) + ' times.')
        print('\nBlack repetition: ')
        for key, value in black_repetition_lookup.items():
            print('There were ' + str(key) + ' blacks in a row ' + str(value) + ' times.')

    def run_falv_alg(self, verbose, martingale, initial_balance, initial_bet, consecutives):
        if verbose:
            print('\nRunning falv algorithm...')
        balance = initial_balance
        max_balance = initial_balance
        bet = initial_bet
        consecutive_reds = 0
        consecutive_greens = 0
        consecutive_blacks = 0
        bet_red = False
        bet_green = False
        bet_black = False
        rolls_processed = 0
        for roll in self.rolls:
            rolls_processed += 1
            if roll.color is Color.red:
                if verbose:
                    print('Rolled red # ' + str(roll.value))
                consecutive_reds += 1
                consecutive_greens = 0
                consecutive_blacks = 0
                if bet_red:
                    balance += (bet * 2)
                    if martingale:
                        bet = int(max(bet / 2, initial_bet))
                    max_balance = max(balance, max_balance)
                    if verbose:
                        print('Won our bet on red.')
                        print('Balance: ' + str(balance))
                elif bet_green:
                    if verbose:
                        print('Lost our bet on green.')
                        print('Balance: ' + str(balance))
                    if martingale:
                        bet = int(min(bet * 2, balance))
                else:
                    if bet_black:
                        if verbose:
                            print('Lost our bet on black.')
                            print('Balance: ' + str(balance))
                        if martingale:
                            bet = int(min(bet * 2, balance))
                if balance > 0:
                    if consecutive_reds >= consecutives:
                        bet = int(min(initial_bet, balance))
                        if verbose:
                            print('Gotten ' + str(consecutive_reds) +
                                  ' reds in a row, betting ' + str(bet) + ' on red.')
                        bet_red = True
                        balance -= bet
                else:
                    if verbose:
                        print('Balance reached 0. Stopping scenario...', end='\n\n')
                        print('Max balance achieved: ', max_balance)
                    return AnalysisResult(rolls_processed, max_balance)
                bet_black = False
                bet_green = False
            elif roll.color is Color.green:
                if verbose:
                    print('Rolled green # ' + str(roll.value))
                consecutive_reds = 0
                consecutive_greens += 1
                consecutive_blacks = 0
                if bet_red:
                    if verbose:
                        print('Lost our bet on red.')
                        print('Balance: ' + str(balance))
                    if martingale:
                        bet = int(min(bet * 2, balance))
                elif bet_green:
                    if verbose:
                        print('Won our bet on green.')
                    balance += (bet * 2)
                    if martingale:
                        bet = int(max(bet / 2, initial_bet))
                else:
                    if bet_black:
                        if verbose:
                            print('Lost our bet on black.')
                            print('Balance: ' + str(balance))
                        if martingale:
                            bet = int(min(bet * 2, balance))
                bet_red = False
                bet_green = False
                bet_black = False
            else:
                if roll.color is Color.black:
                    if verbose:
                        print('Rolled black # ' + str(roll.value))
                    consecutive_reds = 0
                    consecutive_greens = 0
                    consecutive_blacks += 1
                    if bet_red:
                        if verbose:
                            print('Lost our bet on red.')
                            print('Balance: ' + str(balance))
                        if martingale:
                            bet = int(min(bet * 2, balance))
                    elif bet_green:
                        if verbose:
                            print('Lost our bet on green.')
                            print('Balance: ' + str(balance))
                        if martingale:
                            bet = int(min(bet * 2, balance))
                    else:
                        if bet_black:
                            balance += (bet * 2)
                            max_balance = max(balance, max_balance)
                            if verbose:
                                print('Won our bet on black.')
                                print('Balance: ' + str(balance))
                            if martingale:
                                bet = int(max(bet / 2, initial_bet))
                    if balance > 0:
                        if consecutive_blacks >= consecutives:
                            bet = int(min(initial_bet, balance))
                            if verbose:
                                print('Gotten ' + str(consecutive_blacks) + ' blacks in a row, betting ' + str(bet) + ' on black.')
                            bet_black = True
                            balance -= bet
                    else:
                        if verbose:
                            print('Balance reached 0. Stopping scenario...', end='\n\n')
                            print('Max balance achieved: ', max_balance)
                        return AnalysisResult(rolls_processed, max_balance)
                    bet_red = False
                    bet_green = False
        return AnalysisResult(rolls_processed, max_balance)
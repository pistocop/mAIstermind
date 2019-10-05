"""
# Overview
This script will create a .CSV with the history of the selected player for each password.
The process submit each password to the player in a wheel-mode for each cycle:
    1st lap: AAAA - AAAB - AAAC ... - FFFF
    2nd lap: AAAA - AAAB - AAAC ... - FFFF
    3rd lap: ...

Moreover, another CSV will contain how many possible psw the guess had cutted:
    1st lap: 1132 - 72 - 3 ... - FFFF


# Usage
strategy        = strategy of the player [hopeful / knuth / knuth_fast]
output_path     = the match CSV path [string]
cut_history_path = the history with cut stat CSV path [string]
saving_lap      = system save the CSV each saving_lap matches [int]
cycles          = how many cycle of all passwords test [int]
optimal_start   = use optimal start AABB or not [if present--> use optimal start]


# Example
python db_creator.py --strategy knuth
                    --output_path ./db_csv/test.csv
                    --cut_history_path ./db_csv/test_cuts.csv
                    --saving_lap 1
                    --cycles 5
                    --optimal_start
"""

import player
import argparse
import pandas as pd
import sys
from itertools import product
from string import ascii_uppercase

COLUMNS_HEADER = ['Guess 1', 'Guess 2', 'Guess 3', 'Guess 4', 'Guess 5',
                  'Guess 6', 'Guess 7', 'Guess 8', 'Guess 9', 'Guess 10',
                  'PASSWORD']

MATCH_LOST_PAD = 'XXXX'

# Classic Mastermind rules
PSW_CARDINALITY = 6
PSW_LEN = 4
PSW_POOL_COMPLETE = [''.join(p) for p in product(ascii_uppercase[0:PSW_CARDINALITY], repeat=PSW_LEN)]


def save_to_csv(df, f, add_header=False):
    df.to_csv(f, sep=',', encoding='utf-8', index=False, header=add_header, float_format="%.0f")


def save_system(path, info_list, header=False):
    df = pd.DataFrame(data=info_list, columns=COLUMNS_HEADER) if header else pd.DataFrame(data=info_list)
    with open(path, 'a') as f:
        save_to_csv(df, f, header)


def run(arg_dict):
    plays_history = []
    cuts_history = []
    save_lap_counter = 0

    save_system(arg_dict.output_path, plays_history, True)  # write header
    save_system(arg_dict.cut_history_path, cuts_history, True)  # write header

    for cycle in range(arg_dict.cycles):
        for psw_goal, index in zip(PSW_POOL_COMPLETE, range(len(PSW_POOL_COMPLETE))):
            save_lap_counter += 1

            if arg_dict.optimal_start:
                play_history, cut_history = player.main(['--strategy={}'.format(arg_dict.strategy),
                                                         '--goal={}'.format(psw_goal),
                                                         '--optimal_start',
                                                         '--silent'])
            else:
                play_history, cut_history = player.main(['--strategy={}'.format(arg_dict.strategy),
                                                         '--goal={}'.format(psw_goal),
                                                         '--silent'])

            # Match is lost
            if len(play_history) > 10:
                play_history = play_history[:9]
                play_history.append(MATCH_LOST_PAD)
                cut_history = cut_history[:10]

            # Match is won before 10 attempts
            if len(play_history) < 10:
                to_add = 10 - len(play_history)
                for _ in range(to_add):
                    play_history.append("<pad>")
                    cut_history.append(0)
            play_history.append(psw_goal)
            cut_history.append(psw_goal)

            plays_history.append(play_history)
            cuts_history.append(cut_history)

            # Save the CSV each saving_lap laps
            if save_lap_counter >= arg_dict.saving_lap:
                save_lap_counter = 0
                save_system(arg_dict.output_path, plays_history)
                save_system(arg_dict.cut_history_path, cuts_history)
                plays_history = []
                cuts_history = []

            if not arg_dict.silent:
                print('Cycle = {}, psw{}/{}'.format(cycle, index, len(PSW_POOL_COMPLETE)))
                sys.stdout.flush()

    save_system(arg_dict.output_path, plays_history)
    save_system(arg_dict.cut_history_path, cuts_history)
    print('Database created!')


def default_args(argv):
    """Provides default values for player match."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--strategy',
        required=True,
        choices=['knuth', 'hopeful', 'knuth_fast'])
    parser.add_argument(
        '--output_path',
        required=True
    )
    parser.add_argument(
        '--cut_history_path',
        required=False,
        default='new_run_cuts.csv'
    )
    parser.add_argument(
        '--saving_lap',
        required=False,
        type=int,
        default=1)
    parser.add_argument(
        '--cycles',
        required=False,
        type=int,
        default=1)
    parser.add_argument(
        '--optimal_start',
        action='store_true')
    parser.add_argument(
        '--silent',
        action='store_true')

    parsed_args, _ = parser.parse_known_args(argv)
    return parsed_args


def main(argv):
    arg_dict = default_args(argv)
    run(arg_dict)


if __name__ == '__main__':
    main(sys.argv[1:])

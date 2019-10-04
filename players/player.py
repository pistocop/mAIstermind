"""
# Usage example
	./player.py --strategy hopeful --forced=ABCD CDEF ABAB --goal=ABCD --print


# Mastermind classic rules
	passwords length = 4 (ABCD)
	password cardinality = 6 (A B C D E F)


# Some snippets are taken from bin Wellner
	https://gist.github.com/gvx/975276 


# Info
- KNUTH_SMART_START: all the opens Knuth find if the 1st guess is not forced to AABB.
					Provided as a list form in order to improve the performance.
- knuth_guess:      official knuth algorithm (match won in max 5 try)
- knuth_guess_fast: count the cut amount considering all the tips, even if some tips are
                    impossible to obtain in the data situation. Sometimes (very uncommon)
                    the match use 6 try, but complexity is reduced of *len(psw_pool)
                    (the differences between knuth and knuth_fast are indicated by "[!]")
- list(psw_pool):   python set structure is more efficient that list, but isn'r real "shuffled"
"""


import sys
import argparse
import random
from itertools import product
from string import ascii_uppercase


# Classic Mastermind rules
PSW_CARDINALITY = 6
PSW_LEN = 4


# The start choices Knuth Algorithm calculate if not AABB start is forced
KNUTH_SMART_START = ["BFAF","FCFE","EFFC","EFAF","FAEA","CACE","CFCA","CBBD","EEAD","BABD",
               		"DDAC","CAEC","EBFB","DCEC","BECC","CCFD","FBDB","BACB","ADAB","DFCF",
               		"CECE","AADD","BBAA","BCBC","CDDC","FAAF","CCAA","FDFD","AAEE","EDDE",
               		"CCEE","EAEA","DCCD","AFAF","AACC","FFEE","AABB","CAAC","EEDD","ACAC",
               		"CBCB","AAFF","EECC","CCBB","FBFB","FEFE","FFAA","BEBE","EBEB","BBCC",
               		"ACCA","CFCF","DFFD","FFBB","AEAE","DDFF","BAAB","AEEA","FCCF","BFBF",
               		"EAAE","EFFE","FBBF","CCDD","BFFB","CBBC","DBDB","FDDF","DEED","CFFC",
               		"DFDF","ECCE","CEEC","FAFA","CACA","DAAD","BDDB","DEDE","ADDA","DADA",
               		"BBEE","FFDD","DBBD","EDED","BEEB","ABAB","AFFA","BDBD","CDCD","ECEC",
               		"CCFF","EBBE","FFCC","FEEF","BABA","DDEE","EEFF","EEAA","DDBB","DDAA",
               		"EFEF","BBDD","BCCB","BBFF","EEBB","DCDC","ADAD","ABBA","FCFC","DDCC"]


# Hopeful strategy
def hopeful_guess(psw_pool):
  next_guess = random.sample(psw_pool, 1)[0]  
  return next_guess


# Knuth-Fast strategy
def knuth_guess_fast(psw_pool, hints_pool):
  if len(psw_pool) == 1:
      next_guess = psw_pool.pop()
      return next_guess
  else:
      psw_pool_complete = list([''.join(p) for p in product(ascii_uppercase[0:PSW_CARDINALITY], repeat=PSW_LEN)]) 
      random.shuffle(psw_pool_complete) 
      max_cut_found = -1

      for possible_next_guess in psw_pool_complete:
        min_cut_found = None

        for hint in hints_pool:
          cut_counter = 0

          for psw_survived in psw_pool: # [!]
            if hints_calculator(psw_survived, possible_next_guess) != hint:
              cut_counter += 1
          if min_cut_found is None or cut_counter < min_cut_found:
            min_cut_found = cut_counter
        
        if (min_cut_found > max_cut_found) or ((min_cut_found == max_cut_found) and possible_next_guess in psw_pool): 
          max_cut_found = min_cut_found
          next_guess = possible_next_guess

      return next_guess


# Knuth strategy
def knuth_guess(psw_pool, hints_pool):
  if len(psw_pool) == 1:
      next_guess = psw_pool.pop()
      return next_guess
  else:
      psw_pool_complete = list([''.join(p) for p in product(ascii_uppercase[0:PSW_CARDINALITY], repeat=PSW_LEN)])
      random.shuffle(psw_pool_complete)
      
      max_cut_found = -1
      for possible_next_guess in psw_pool_complete:
        min_cut_found = None

        for psw_survived in psw_pool:
          cut_counter = 0
          possible_hint = hints_calculator(psw_survived, possible_next_guess) # [!]
          
          for psw_to_cut in psw_pool:
            if hints_calculator(psw_to_cut, possible_next_guess) != possible_hint:
              cut_counter += 1

          if min_cut_found is None or cut_counter < min_cut_found:
            min_cut_found = cut_counter

        if (min_cut_found > max_cut_found) or ((min_cut_found == max_cut_found) and possible_next_guess in psw_pool): 
          max_cut_found = min_cut_found
          next_guess = possible_next_guess

      return next_guess


# Utils
def guess_pool_pruning(psw_pool, next_guess, hints):
  to_remove = []
  for psw in psw_pool:
      if hints != hints_calculator(psw, next_guess):
          to_remove.append(psw)
  len_psw_pool = len(psw_pool)
  psw_pool.difference_update(to_remove)
  return int(len_psw_pool - len(psw_pool))


def hints_calculator(psw_goal, psw_guess):
  black_pegs = len([goal_element for goal_element, guess_element in zip(psw_goal, psw_guess) if goal_element == guess_element])
  white_pegs = sum([min(psw_goal.count(element), psw_guess.count(element)) for element in set('ABCDEF')]) - black_pegs
  return black_pegs, white_pegs


def play(match_info):

  # Pool of all passwords allowed
  psw_pool_complete = set([''.join(p) for p in product(ascii_uppercase[0:PSW_CARDINALITY], repeat=PSW_LEN)])

  # Pool of passwords will be refined step by step
  psw_pool = set(list(psw_pool_complete))

  # List of all combinations of hints (black and white pegs) allowed
  hints_pool = set([(black_pegs, white_pegs) \
              for black_pegs in range(PSW_LEN) \
              for white_pegs in range(PSW_LEN - black_pegs) \
              if not (black_pegs == 3 and white_pegs == 1)])
  
  # Forced attempts list creator
  forced_attempts_list = match_info.forced.split()
  
  # Match start
  match_history = []
  cut_history = []

  black_pegs = 0

  while black_pegs != PSW_LEN:
    next_guess = []
    cut_stat = 0

    # Next guess
    if forced_attempts_list != []:
      next_guess = forced_attempts_list.pop()

    elif len(match_history) == 0 and match_info.optimal_start:
      next_guess = 'AABB'

    elif len(match_history) == 0 and match_info.strategy == 'knuth':
      next_guess = random.choice(KNUTH_SMART_START)

    elif len(match_history) == 0 and match_info.strategy == 'knuth_fast':
      next_guess = random.choice(KNUTH_SMART_START)

    elif match_info.strategy == 'knuth':
      next_guess = knuth_guess(psw_pool, hints_pool)

    elif match_info.strategy == 'knuth_fast':
      next_guess = knuth_guess_fast(psw_pool, hints_pool)

    else:
      next_guess = hopeful_guess(psw_pool)

    # Use the guess
    black_pegs, white_pegs = hints_calculator(match_info.goal, next_guess)

    # Refine the psw pool
    if black_pegs != PSW_LEN:
      cut_stat = guess_pool_pruning(psw_pool, next_guess, (black_pegs,white_pegs))

    # Register the guess
    match_history.append(next_guess + str(black_pegs) + str(white_pegs))
    cut_history.append(cut_stat)

  # Print the match
  if not match_info.silent:
  	print('Match history: {}'.format(match_history))
  	print('Cuts history: {}'.format(cut_history))
  
  return match_history, cut_history


def default_args(argv):
  parser = argparse.ArgumentParser()
  
  parser.add_argument(
    '--strategy',
    required=True,
    choices=['knuth','hopeful','knuth_fast'])
  parser.add_argument(
    '--forced',
    required=False,
    default="")
  parser.add_argument(
    '--goal',
    required=True)
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
  match_history = play(arg_dict)
  return match_history


if __name__ == '__main__':
  main(sys.argv[1:])
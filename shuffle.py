#!/usr/bin/env python3
""" Perform 'perfect' interleave shuffles of a standard deck of cards.
    What do the hands look like?
    $Revision: 1.12 $    $Locker:  $
"""

from terminalcolors import TerminalColors
from card import Card
from evaluate import evaluate

def shuffle_halves(lst):
    """ Splits a list in two halves and returns a new list
        consisting of the halves regularly interleaved.
        (AI assisted creation of this function, simple as it is.)
    """
    half_len = len(lst) // 2
    first_half = lst[:half_len]
    second_half = lst[half_len:]
    shuffled = []
    for i in range(half_len):
        shuffled.append(first_half[i])
        shuffled.append(second_half[i])

    if len(lst) % 2 != 0:  # If the original list was odd, add the middle element separately
        shuffled.append(lst[half_len])

    return shuffled

## main

import argparse
from sys import argv, stderr

SUITS = ("spades", "hearts", "diamonds", "clubs")

# Usage
parser = argparse.ArgumentParser(description='Shuffles a deck of cards and displays the hands')
mutex = parser.add_mutually_exclusive_group()
parser.add_argument('--shuffles', '-n', type=int, default=1, help="Number of shuffles to perform")
parser.add_argument('--hands', '-p', type=int, default=4, help="Number of hands to deal (# players)")
parser.add_argument('--cards', '-c', type=int, default=5, help="Number of cards per hand")
parser.add_argument('--suit', '-S', action='store_true', help="Sort results by suit first")
mutex.add_argument('--color', action='store_true', help="Colored output (good for light backgrounds)")
mutex.add_argument('--red', action='store_true', help="Color red cards only; may work with dark backgrounds")
parser.add_argument('--verbose', '-v', action='store_true', help="Verbose; show the whole deck")
args=parser.parse_args()

hands = int(args.hands)
cardcount = int(args.cards)
shuffles = int(args.shuffles)
Card.set_usecolor(1 if args.color else (2 if args.red else 0) )


# create the deck -- a list of cards
deck = list()
for suit in SUITS :
    for face in range (2,11):
        deck.append(Card(suit, str(face)))
    for face in ("J", "Q", "K", "A") :
        deck.append(Card(suit, str(face)))

# shuffle the number of times requested
for n in range(shuffles) :
    deck = shuffle_halves(deck)

# print the shuffled deck if being verbose
if args.verbose :
    print (f"Size of deck: {len(deck)} cards")
    print (f"After {shuffles} shuffle{'s' if shuffles > 1 else ''}:")
    for card in deck :
        print ("", card)


# initialize deal as a list of empty hands
deal = []
for hand in range(hands) :
    deal.append([])

# fill the hands in the deal in the proper order
topcard = 0
for count in range (cardcount) :
    for hand in range(hands) :
        deal[hand].append(deck[topcard])
        topcard += 1

# show the hands dealt from the shuffled deck
if args.suit :
    Card.set_compareby(Card.by_suit)
else :
    Card.set_compareby(Card.by_face_value)
print (f"\n{hands} hands of {cardcount} cards after {shuffles} interleave shuffle{'s' if shuffles > 1 else ''}:\n")
high_score = max([evaluate.poker_hand(hnd)[0] for hnd in deal])
hx = 0 # hand count
for hand in range(hands) :
    hx += 1
    print (f"Hand #{hx}: ", end="")
    deal[hand] = sorted(deal[hand])
    for crd in deal[hand] :
        print (crd, end=" ")
    (score, name, high_card) = evaluate.poker_hand(deal[hand])
    print (f"  {name}  {'Winner!' if score==high_score else ''}", end="\n")
print()

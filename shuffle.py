#!/usr/bin/env python3
""" Perform 'perfect' interleave shuffles of a standard deck of cards.
    What do the hands look like?
    $Revision: 1.5 $    $Locker:  $
"""

from terminalcolors import TerminalColors

tc = TerminalColors()

def suit_str(suit) :
    if suit == "hearts":
        return f"{tc.set_color('red')}♥"
    elif suit == "diamonds":
        return f"{tc.set_color('red')}♦"
    elif suit == "clubs":
        return f"{tc.set_color('black')}♣"
    elif suit == "spades":
        return f"{tc.set_color('black')}♠"
    else :
        return "?"

class card :
    use_color = True # use color coding in string representation
    by_face_value = 1 # compare by face value setting
    by_suit = 2  # compare by suit then face value setting
    compare_mode = by_face_value # 1=by value; 2=by suit then value
    suit_value = {  # for sorting by suit then face value
        "♥": 100, "hearts": 100,
        "♣": 200, "clubs": 200,
        "♦": 300,  "diamonds":300,
        "♠": 400, "spades": 400
    }
    face_value = { # for sorting by face value (not any gin game value)
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }
    def __init__ (self, suit:str, face_value) :
        #self.cardface = suit_str(suit) + str(value) + tc.reset()
        if suit == "hearts":
            self.color=tc.set_color('red')
            self.suit="♥"
        elif suit == "diamonds":
            self.color=tc.set_color('red')
            self.suit="♦"
        elif suit == "clubs":
            self.color=tc.set_color('black')
            self.suit="♣"
        elif suit == "spades":
            self.color=tc.set_color('black')
            self.suit="♠"
        self.face = str(face_value)

    def __str__(self) :
        if card.use_color :
            return f"{self.color}{self.face}{self.suit}{tc.reset()}"
        else :
            return f"{self.face}{self.suit}"

    @classmethod
    def set_nocolor(cls) :
        cls.use_color = False ;

    @classmethod
    def set_compareby(cls, setting) :
        if setting == cls.by_face_value or setting == cls.by_suit :
            cls.compare_mode = setting
        else :
            raise ValueError

    @classmethod
    def compare_cards(cls, card1, operator, card2) :
        val1 = cls.face_value[card1.face]
        val2 = cls.face_value[card2.face]
        if cls.compare_mode == cls.by_suit :
            val1 += cls.suit_value[card1.suit]
            val2 += cls.suit_value[card2.suit]

        if operator == "gt" :
            return val1 > val2
        elif operator == "ge" :
            return val1 >= val2
        elif operator == "lt" :
            return val1 < val2
        elif operator == "le" :
            return val1 <= val2
        elif operator == "eq" :
            return val1 == val2
        elif operator == "ne" :
            return val1 != val2
        else :
            raise ValueError

    def __gt__(self, other) :
        return card.compare_cards(self, "gt", other)
    def __ge__(self, other) :
        return card.compare_cards(self, "ge", other)
    def __lt__(self, other) :
        return card.compare_cards(self, "lt", other)
    def __le__(self, other) :
        return card.compare_cards(self, "le", other)
    def __eq__(self, other) :
        return card.compare_cards(self, "eq", other)
    def __ne__(self, other) :
        return card.compare_cards(self, "ne", other)

def shuffle_halves(lst):
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

SUITS = ("hearts", "diamonds", "clubs", "spades")

# Usage
parser = argparse.ArgumentParser(description='Shuffles a deck of cards and displays the hands')
parser.add_argument('--shuffles', '-n', type=int, default=1, help="Number of shuffles to perform")
parser.add_argument('--hands', '-p', type=int, default=4, help="Number of hands to deal (# players)")
parser.add_argument('--cards', '-c', type=int, default=5, help="Number of cards per hand")
parser.add_argument('--suit', '-S', action='store_true', help="Sort results by suit first")
parser.add_argument('--bw', '-b', action='store_true', help="Black and white, i.e., native screen color only")
parser.add_argument('--verbose', '-v', action='store_true', help="Verbose; show the whole deck")
args=parser.parse_args()

hands = int(args.hands)
cardcount = int(args.cards)
shuffles = int(args.shuffles)
if args.bw :
    card.set_nocolor()

# create the deck
deck = list()
for suit in SUITS :
    for face in range (2,11):
        deck.append(card(suit, str(face)))
    for face in ("J", "Q", "K", "A") :
        deck.append(card(suit, str(face)))

# shuffle the number of times requested
for n in range(shuffles) :
    deck = shuffle_halves(deck)

# print the shuffled deck
if args.verbose :
    print (f"Size of deck: {len(deck)} cards")
    print (f"After {shuffles} shuffles:")
    for card in deck :
        print ("", card)


# init deal of number of hands
deal = []
for hand in range(hands) :
    deal.append([])

# fill the hands in the deal
topcard = 0
for count in range (cardcount) :
    for hand in range(hands) :
        deal[hand].append(deck[topcard])
        topcard += 1

# show the hands
if args.suit :
    card.set_compareby(card.by_suit)
else :
    card.set_compareby(card.by_face_value)
print (f"\n{hands} hands of {cardcount} cards after {shuffles} interleave shuffle{'s' if shuffles > 1 else ''}:\n")
for hand in range(hands) :
    deal[hand] = sorted(deal[hand])
    for count in range (cardcount) :
        print (f"{deal[hand][count]}", end=" ")
    print ()

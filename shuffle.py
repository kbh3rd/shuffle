#!/usr/bin/env python3
""" Perform 'perfect' interleave shuffles of a standard deck of cards.
    What do the hands look like?
    $Revision: 1.9 $    $Locker:  $
"""

from terminalcolors import TerminalColors

tc = TerminalColors()

class card :
    """ One card. A deck is a list of these objects.
    """
    use_color = 0 # --color set 1; --red set 2; none set 0
    by_face_value = 1 # compare by face value setting
    by_suit = 2  # compare by suit then face value setting
    compare_mode = by_face_value # 1=by value; 2=by suit then value
    suit_value = {  # for sorting by suit
        "♥": 100, "hearts": 100,
        "♣": 200, "clubs": 200,
        "♦": 300,  "diamonds":300,
        "♠": 400, "spades": 400
    }
    face_value = { # for sorting by face value (not a card value in any gin game)
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
        """ create one card.
            'suit' is name or symbol of one of the 4 standard suits
            'face_value' is number or first letter of face card
        """
        if suit.lower() == "hearts" or suit == "♥" :
            self.color=tc.set_color('red')
            self.suit="♥"
        elif suit.lower() == "diamonds" or suit == "♦" :
            self.color=tc.set_color('red')
            self.suit="♦"
        elif suit.lower() == "clubs" or suit == "♣" :
            self.color=tc.set_color('black')
            self.suit="♣"
        elif suit.lower() == "spades" or suit == "♠" :
            self.color=tc.set_color('black')
            self.suit="♠"
        self.face = str(face_value).upper()

    def __str__(self) :
        """ class variable determines if color is used or not """
        if card.use_color == 1 :
            return f"{self.color}{self.face}{self.suit}{tc.reset()}"
        elif card.use_color == 2 and (self.suit == "♥" or self.suit == "♦") :
            return f"{self.color}{self.face}{self.suit}{tc.reset()}"
        else :
            return f"{self.face}{self.suit}"

    @classmethod
    def set_usecolor(cls, val:int) :
        """ Sets class variable for whether/how to use color in __str__() """
        if 0 <= val <= 2 :
            cls.use_color = val ;
        else :
            raise ValueError

    @classmethod
    def set_compareby(cls, setting) :
        """ Sets class variable for card comparison methods used to sort a hand or deck """
        if setting == cls.by_face_value or setting == cls.by_suit :
            cls.compare_mode = setting
        else :
            raise ValueError

    @classmethod
    def compare_cards(cls, card1, operator, card2) :
        """ Compare two cards with the given operator considering the class comparison mode.
            If comparing by suit, add suite value (large) and face value (small) to effect
            comparing by suit then face.
        """
        val1 = cls.face_value[card1.face]
        val2 = cls.face_value[card2.face]
        if cls.compare_mode == cls.by_suit :
            val1 += cls.suit_value[card1.suit]
            val2 += cls.suit_value[card2.suit]

        if operator == "gt" or operator == ">" :
            return val1 > val2
        elif operator == "ge" or operator == ">=" :
            return val1 >= val2
        elif operator == "lt" or operator == "<" :
            return val1 < val2
        elif operator == "le" or operator == "<=" :
            return val1 <= val2
        elif operator == "eq" or operator == "==" :
            return val1 == val2
        elif operator == "ne" or operator == "!=" :
            return val1 != val2
        else :
            raise ValueError

    # Methods used to compare two cards, either directly
    # by the coder; "if card1 < card2:"
    # or implicitly by sorted()
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

SUITS = ("hearts", "diamonds", "clubs", "spades")

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
card.set_usecolor(1 if args.color else (2 if args.red else 0) )


# create the deck -- a list of cards
deck = list()
for suit in SUITS :
    for face in range (2,11):
        deck.append(card(suit, str(face)))
    for face in ("J", "Q", "K", "A") :
        deck.append(card(suit, str(face)))

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
    card.set_compareby(card.by_suit)
else :
    card.set_compareby(card.by_face_value)
print (f"\n{hands} hands of {cardcount} cards after {shuffles} interleave shuffle{'s' if shuffles > 1 else ''}:\n")
for hand in range(hands) :
    deal[hand] = sorted(deal[hand])
    for crd in deal[hand] :
        print (crd, end=" ")
    print ()

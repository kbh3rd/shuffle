#!/usr/bin/env python3

from card import Card

class evaluate :
    """ Evaluate a hand (list) of Cards by various rules (poker initially) """

    __poker_hands = {
        # For comparing hands add the high card face value to the hand score
        "high_card": {"score": 100, "name": "Nothing Burger"}, 
        "one_pair": {"score": 200, "name": "One Pair"}, 
        "two_pair": {"score": 300, "name": "Two Pair"}, 
        "three_of_a_kind": {"score": 400, "name": "Three of a Kind"}, 
        "straight": {"score": 500, "name": "Straight"}, 
        "flush": {"score": 600, "name": "Flush"}, 
        "full_house": {"score": 700, "name": "Full House"}, 
        "four_of_a_kind": {"score": 800, "name": "Four of a Kind"}, 
        "straight_flush": {"score": 900, "name": "Straight Flush"}, 
        "royal_flush": {"score": 900, "name": "Royal Flush"}, # 'Just' a straight flush with Ace high
    }

    @staticmethod
    def __dups (hand:list) :
        face_counts = dict()
        for card in hand :
            face_counts[card.face] = 1 if not card.face in face_counts else face_counts[card.face]+1
        return face_counts

    @staticmethod
    def high_card (hand:list) :
        Card.set_compareby(Card.by_face_value)
        return Card.face_value[sorted(hand)[-1].face] # face value of the last card when sorted

    @staticmethod
    def one_pair (hand:list) :
        face_counts = evaluate.__dups(hand)
        pairs = [face for face, count in face_counts.items() if count == 2]
        if pairs :
            return max([Card.face_value[face] for face in pairs])
        else :
            return 0

    @staticmethod
    def two_pair (hand:list) :
        face_counts = evaluate.__dups(hand)
        pairs = [face for face, count in face_counts.items() if count == 2]
        if len(pairs) > 1 :
            # this isn't right for hands > 5 cards where there could be >2 pairs
            return max(Card.face_value[pairs[0]], Card.face_value[pairs[1]])
        else :
            return 0

    @staticmethod
    def three_of_a_kind (hand:list) :
        face_counts = evaluate.__dups(hand)
        triples = [face for face, count in face_counts.items() if count == 3]
        if triples :
            return max([Card.face_value[face] for face in triples])
        return 0 # if no triple found

    @staticmethod
    def four_of_a_kind (hand:list) :
        face_counts = evaluate.__dups(hand)
        fours = [face for face, count in face_counts.items() if count == 4]
        if fours :
            return max([Card.face_value[face] for face in fours])
        return 0 # if no triple found

    @staticmethod
    def straight (hand:list) :
        Card.set_compareby(Card.by_face_value)
        ordered = sorted(hand)
        for cx in range(len(hand)-1) :
            if Card.face_value[ordered[cx].face]+1 != Card.face_value[ordered[cx+1].face] :
                # next card doesn't follow; no straight
                return 0
        # It's a straight, return value of high card
        return Card.face_value[ordered[-1].face]

    @staticmethod
    def flush (hand:list) :
        for cx in range(len(hand)-1) :
            if hand[cx].suit != hand[cx+1].suit :
                return 0 # no flush
        return max([Card.face_value[card.face] for card in hand])

    @staticmethod
    def straight_flush (hand:list) :
        straight = evaluate.straight(hand)
        if not straight :
            return 0
        flush = evaluate.flush(hand)
        if not flush :
            return 0
        return flush # high card same in straight and flush vars

    @staticmethod
    def full_house (hand:list) :
        pair = evaluate.one_pair(hand)
        three = evaluate.three_of_a_kind(hand)
        if pair and three and pair != three :
            return three
        else :
            return 0

    @staticmethod
    def royal_flush (hand:list): # simply an ace-high straight flush
        val = evaluate.straight_flush(hand)
        if val == Card.face_value["A"] :
            return val
        else :
            return 0

    @classmethod
    def poker_hand (cls, hand:list) :
        """ Evaluate the hand of cards for Poker
            Input: a hand of Cards
            Output: tuple (score, name, high_card)
            Score based on high qualifying card, not high card in hand
        """
        Card.set_compareby(Card.by_face_value)
        high_card = sorted(hand)[-1]

        score = evaluate.royal_flush(hand)
        if score :
            this_hand = cls.__poker_hands['royal_flush']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.straight_flush(hand)
        if score :
            this_hand = cls.__poker_hands['straight_flush']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.full_house(hand)
        if score :
            this_hand = cls.__poker_hands['full_house']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.four_of_a_kind(hand)
        if score :
            this_hand = cls.__poker_hands['four_of_a_kind']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.flush(hand)
        if score :
            this_hand = cls.__poker_hands['flush']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.straight(hand)
        if score :
            this_hand = cls.__poker_hands['straight']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.three_of_a_kind(hand)
        if score :
            this_hand = cls.__poker_hands['three_of_a_kind']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.two_pair(hand)
        if score :
            this_hand = cls.__poker_hands['two_pair']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.one_pair(hand)
        if score :
            this_hand = cls.__poker_hands['one_pair']
            return(score + this_hand['score'], this_hand['name'], high_card)

        score = evaluate.high_card(hand)
        this_hand = cls.__poker_hands["high_card"]
        return(score + this_hand['score'], this_hand['name'], high_card)


if __name__ == "__main__" :

    def make_hand_of_spades(cards:list) -> list : # for when suite doesn't matter
        hand = list()
        for c in cards :
            hand.append(Card("spades", c))
        return hand

    def make_mixed_hand(cards:list) :
        """ Input: list of lists or tuples like ("spades", "A")
            Output: corresponding list of Card objects
        """
        hand = list()
        for suit, face in cards :
            hand.append(Card(suit, face))
        return hand

    def show_hand(hand:list, newline:bool=True) :
        for c in hand :
            print(c, end=" ")
        if newline :
            print()

    def evaluate_all(hand:list) :
        print ("\tHigh card:", evaluate.high_card(hand))
        print ("\tPair:", evaluate.one_pair(hand))
        print ("\tTwo pair:", evaluate.two_pair(hand))
        print ("\tThree of a kind:", evaluate.three_of_a_kind(hand))
        print ("\tStraight:", evaluate.straight(hand))
        print ("\tFlush:", evaluate.flush(hand))
        print ("\tFull house:", evaluate.full_house(hand))
        print ("\tFour of a kind:", evaluate.four_of_a_kind(hand))
        print ("\tStraight flush:", evaluate.straight_flush(hand))
        print ("\tRoyal flush:", evaluate.royal_flush(hand))


    print ("Nothing burger")
    nothing_hand = make_mixed_hand([ ("hearts",3), ("spades",2), ("clubs",9),
                                        ("clubs", "Q"), ("diamonds","7")
                                      ])
    show_hand(nothing_hand)
    evaluate_all(nothing_hand)

    print ("One Pair")
    one_pair_hand = make_mixed_hand([ ("hearts",3), ("spades",2), ("clubs",9),
                                        ("clubs", 3), ("diamonds",6)
                                      ])
    show_hand(one_pair_hand)
    evaluate_all(one_pair_hand)

    print("\nTwo Pair")
    two_pair_hand = make_mixed_hand([ ("hearts",2), ("spades",3), ("clubs",4),
                                        ("clubs", 3), ("diamonds",2)
                                      ])
    show_hand(two_pair_hand)
    evaluate_all(two_pair_hand)

    print("\nThree of a kind")
    triple_hand = make_mixed_hand([ ("hearts",3), ("spades",3), ("clubs",4),
                                        ("clubs", 3), ("diamonds",2)
                                      ])
    show_hand(triple_hand)
    evaluate_all(triple_hand)

    print("\nStraight")
    straight_hand = make_mixed_hand([ ("hearts",6), ("spades",5), ("clubs",4),
                                        ("clubs", 7), ("diamonds",3)
                                      ])
    straight_hand[2].suit="♣"
    show_hand(straight_hand)
    evaluate_all(straight_hand)

    print ("\nStraight flush")
    straight_flush_hand = make_hand_of_spades([6, 5, 4, 7, 3]) 
    show_hand(straight_flush_hand)
    evaluate_all(straight_flush_hand)

    print ("\nFull House")
    full_house_hand = make_mixed_hand([ ("hearts",7), ("spades",7), ("clubs",3),
                                        ("clubs", 7), ("diamonds",3)
                                      ])
    show_hand(full_house_hand)
    evaluate_all(full_house_hand)

    print ("\nFour of a kind")
    four_of_a_kind_hand = make_mixed_hand([ ("hearts",7), ("spades",7), ("clubs","K"),
                                        ("clubs", 7), ("diamonds","7")
                                      ])
    show_hand(four_of_a_kind_hand)
    evaluate_all(four_of_a_kind_hand)

    print ("\nRoyal Flush")
    royal_flush_hand = make_hand_of_spades(["A","K","Q","J","10"])
    show_hand(royal_flush_hand)
    evaluate_all(royal_flush_hand)

    print()
    for hand in [nothing_hand,
                 one_pair_hand,
                 two_pair_hand,
                 triple_hand,
                 straight_hand,
                 full_house_hand,
                 four_of_a_kind_hand,
                 straight_flush_hand,
                 royal_flush_hand,
                ] :
        (score, name, high_card) = evaluate.poker_hand(hand)
        show_hand(hand)
        print (f"  {name} {high_card.face} high, score={score}", end="\n\n")

    exit (0)

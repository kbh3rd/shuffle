## shuffle

Simlulate "perfect" interleaved shuffling of a standard deck of playing cards that has
an initial state of being fully unshuffled: 2 through Ace in order for each of the suits.
This is to demonstrate that standard interleaved shuffling alone does a *very* poor job
of randomizing a deck of cards.

The Python script shuffle.py is meant to be run on a terminal or in a terminal window that
is color-capable. It uses the TERM environment variable to identify the type of display and
defaults to "xterm-256color". It also relies on the terminal being Unicode-capable in order
to show the suit characters.

### Example

Poker, anyone?

```bash
$ ./shuffle.py --shuffles 5 --hands 4 --cards 5 

4 hands of 5 cards after 5 interleave shuffles:

2♥ 2♦ 2♣ 8♣ 8♠ 
3♠ 4♥ 10♥ 10♦ 10♣ 
5♦ 5♣ 5♠ J♠ Q♥ 
7♥ 7♦ K♦ K♣ K♠ 
```

### Bugs

There are no bugs. ;-)

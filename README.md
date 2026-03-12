## shuffle

Simulate "perfect" interleaved riffle shuffling of a standard deck of playing
cards that has an initial state of being fully unshuffled: 2 through Ace
in order for each of the suits (no Jokers).  This is to demonstrate that standard
interleaved shuffling alone does a *very* poor job of randomizing a deck
of cards. In fact, it is not at all random.

The ```evaluate.py``` module is used to evaluate each dealt hand using standard
stud poker rules.

The Python script shuffle.py can be run on a terminal or in a terminal
window that is color-capable. If ```--color``` is in the arguement
list the suits are shown in red and black; this only works well on light backgrounds
so that the black suits are visible. if ```--red``` is given, then
it only colors the red suits, and the black suits are shown in native color;
this might work well on dark backgrounds with light fonts.

It uses the ```terminalcolors.py``` module which uses the TERM
environment variable to identify the type of display and defaults
to "xterm-256color".

It relies on the terminal being Unicode-capable in order to show the
suit characters: ♥ ♦ ♣ ♠

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

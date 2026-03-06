## shuffle

Simlulate "perfect" interleaved shuffling of a standard deck of playing cards that has
an initial state of being fully unshuffled: 2 through Ace in order for each of the suites.
This is to demonstrate that standard interleaved shuffling alone does a very poor job
of randomizing a deck of cards.

The Python script shuffle.py is meant to be run on a terminal or in a terminal window that
is color-capable. It uses the TERM environment variable to identify the type of display and
defaults to "xterm-256color". It also relies on the terminal being Unicode-capable in order
to show the suite characters.

### Bugs

Throughout the code the word "suite" is misspelled as "suit". There are no other bugs. ;-)

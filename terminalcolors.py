#!/usr/bin/env python3

import os
import curses
from typing import Dict

class TerminalColors:
    """
    Generate control‑code strings that change the colour of subsequent
    stdout output.  The class looks up the appropriate escape sequences
    from the terminfo database (via ``curses.tigetstr``).  If the TERM
    variable is missing or not found, it falls back to ``xterm-256color``.

    Created with aid of GPT-OSS 120B
    $Revision: 1.1 $    $Locker:  $
    """

    # Mapping of colour names to the corresponding ANSI colour numbers
    _ansi_map: Dict[str, int] = {
        "black":   0,
        "red":     1,
        "green":   2,
        "yellow":  3,
        "blue":    4,
        "magenta": 5,
        "cyan":    6,
        "white":   7,
        # bright variants
        "bright_black":   8,
        "bright_red":     9,
        "bright_green":  10,
        "bright_yellow": 11,
        "bright_blue":   12,
        "bright_magenta":13,
        "bright_cyan":   14,
        "bright_white":  15,
    }

    def __init__(self, darkbg: bool = False):
        # Determine the terminal type
        term = os.getenv("TERM") or "xterm-256color"
        try:
            curses.setupterm(term)
        except Exception:
            # If the supplied TERM is unknown, fall back to xterm‑256color
            curses.setupterm("xterm-256color")

        # Cache the generic reset sequence
        self._reset_seq = self._tigetstr("sgr0") or b"\x1b[0m"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------
    def _tigetstr(self, cap: str) -> bytes:
        """Return the raw bytes for a terminfo capability, or ``b''``."""
        seq = curses.tigetstr(cap)
        return seq if seq else b""

    def _ansi_escape(self, code: str) -> bytes:
        """Build a simple ANSI escape sequence (e.g. ``\\x1b[31m``)."""
        return f"\x1b[{code}m".encode()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def set_color(self, name: str, bright: bool = False) -> str:
        """
        Return the control‑code string that sets the foreground colour.

        Parameters
        ----------
        name: str
            One of the keys in ``_ansi_map`` (e.g. ``'red'`` or ``'bright_blue'``).
        bright: bool, optional
            If ``True`` and the terminal supports 256‑color mode, the bright
            variant is used even if the name does not contain ``'bright_'``.

        Returns
        -------
        str
            The bytes decoded as UTF‑8 ready to be written to ``stdout``.
        """
        # Normalise the colour name
        key = name.lower()
        if bright and not key.startswith("bright_"):
            key = f"bright_{key}"

        if key not in self._ansi_map:
            raise ValueError(f"Unsupported colour name: {name}")

        # Try to use the terminfo ``setaf`` capability (set ANSI foreground)
        # ``setaf`` expects a colour number (0‑255).  If the capability is missing,
        # fall back to a raw ANSI escape.
        setaf = self._tigetstr("setaf")
        if setaf:
            # ``curses.tparm`` expands the capability with the colour index.
            seq = curses.tparm(setaf, self._ansi_map[key])
        else:
            # Simple fallback – 30‑37 for normal, 90‑97 for bright
            base = 90 if key.startswith("bright_") else 30
            seq = self._ansi_escape(str(base + self._ansi_map[key] % 8))

        return seq.decode()

    def reset(self) -> str:
        """
        Return the control‑code string that resets all attributes
        (colour, bold, underline, etc.) to the terminal defaults.
        """
        return self._reset_seq.decode()


if "__main__" == __name__ :

    import sys
    #from terminalcolors import TerminalColors

    tc = TerminalColors()

    print(tc.set_color("red") + "This text is red" + tc.reset())
    print(tc.set_color("bright_green") + "Bright green text" + tc.reset())

    suits = {
        "hearts": f"{tc.set_color('red')}♥",
        "diamonds": f"{tc.set_color('red')}♦",
        "clubs": f"{tc.set_color('black')}♣",
        "spades": f"{tc.set_color('black')}♠",
    }

    for suit in suits :
        print (f"{suits[suit]} {suit}")



"""All the key sequences"""
# If you add a binding, add something about your setup
# if you can figure out why it's different

# Special names are for multi-character keys, or key names
# that would be hard to write in a config file

# TODO add PAD keys hack as in bpython.cli

# fmt: off
_CURTSIES_NAMES = {
    b'\x1b ':      '<Esc+SPACE>',
    b'\t':         '<TAB>',
    b'\x1b[Z':     '<Shift-TAB>',
    b'\x1b[A':     '<UP>',
    b'\x1b[B':     '<DOWN>',
    b'\x1b[C':     '<RIGHT>',
    b'\x1b[D':     '<LEFT>',
    b'\x1bOA':     '<UP>',         # in issue 92 its shown these should be normal arrows,
    b'\x1bOB':     '<DOWN>',       # not ctrl-arrows as we previously had them.
    b'\x1bOC':     '<RIGHT>',
    b'\x1bOD':     '<LEFT>',

    b'\x1b[1;5A':  '<Ctrl-UP>',
    b'\x1b[1;5B':  '<Ctrl-DOWN>',
    b'\x1b[1;5C':  '<Ctrl-RIGHT>', # reported by myint
    b'\x1b[1;5D':  '<Ctrl-LEFT>',  # reported by myint

    b'\x1b[5A':    '<Ctrl-UP>',    # not sure about these, someone wanted them for bpython
    b'\x1b[5B':    '<Ctrl-DOWN>',
    b'\x1b[5C':    '<Ctrl-RIGHT>',
    b'\x1b[5D':    '<Ctrl-LEFT>',

    b'\x1b[1;9A':  '<Esc+UP>',
    b'\x1b[1;9B':  '<Esc+DOWN>',
    b'\x1b[1;9C':  '<Esc+RIGHT>',
    b'\x1b[1;9D':  '<Esc+LEFT>',

    b'\x1b[1;10A': '<Esc+Shift-UP>',
    b'\x1b[1;10B': '<Esc+Shift-DOWN>',
    b'\x1b[1;10C': '<Esc+Shift-RIGHT>',
    b'\x1b[1;10D': '<Esc+Shift-LEFT>',

    b'\x1bOP':     '<F1>',
    b'\x1bOQ':     '<F2>',
    b'\x1bOR':     '<F3>',
    b'\x1bOS':     '<F4>',

    # see bpython #626
    b'\x1b[11~':   '<F1>',
    b'\x1b[12~':   '<F2>',
    b'\x1b[13~':   '<F3>',
    b'\x1b[14~':   '<F4>',

    b'\x1b[15~':   '<F5>',
    b'\x1b[17~':   '<F6>',
    b'\x1b[18~':   '<F7>',
    b'\x1b[19~':   '<F8>',
    b'\x1b[20~':   '<F9>',
    b'\x1b[21~':   '<F10>',
    b'\x1b[23~':   '<F11>',
    b'\x1b[24~':   '<F12>',
    b'\x00':       '<Ctrl-SPACE>',
    b'\x1c':       '<Ctrl-\\>',
    b'\x1d':       '<Ctrl-]>',
    b'\x1e':       '<Ctrl-6>',
    b'\x1f':       '<Ctrl-/>',
    b'\x7f':       '<BACKSPACE>',    # for some folks this is ctrl-backspace apparently
    b'\x1b\x7f':   '<Esc+BACKSPACE>',
    b'\xff':       '<Meta-BACKSPACE>',
    b'\x1b\x1b[A': '<Esc+UP>',    # uncertain about these four
    b'\x1b\x1b[B': '<Esc+DOWN>',
    b'\x1b\x1b[C': '<Esc+RIGHT>',
    b'\x1b\x1b[D': '<Esc+LEFT>',
    b'\x1b':       '<ESC>',
    b'\x1b[1~':    '<HOME>',
    b'\x1b[4~':    '<END>',
    b'\x1b\x1b[5~':'<Esc+PAGEUP>',
    b'\x1b\x1b[6~':'<Esc+PAGEDOWN>',

    b'\x1b[H':     '<HOME>',    # reported by amorozov in bpython #490
    b'\x1b[F':     '<END>',     # reported by amorozov in bpython #490

    b'\x1bOH':     '<HOME>',    # reported by mixmastamyk in curtsies #78
    b'\x1bOF':     '<END>',     # reported by mixmastamyk in curtsies #78

    # not fixing for back compat.
    # (b"\x1b[1~": u'<FIND>',       # find

    b"\x1b[2~": '<INSERT>',       # insert (0)
    b"\x1b[3~": '<DELETE>',       # delete (.), "Execute"
    b"\x1b[3;5~": '<Ctrl-DELETE>',

    # st (simple terminal) see issue #169
    b"\x1b[4h": '<INSERT>',
    b"\x1b[P": '<DELETE>',

    # not fixing for back compat.
    # (b"\x1b[4~": u'<SELECT>',       # select

    b"\x1b[5~": '<PAGEUP>',       # pgup   (9)
    b"\x1b[6~": '<PAGEDOWN>',     # pgdown (3)
    b"\x1b[7~": '<HOME>',         # home
    b"\x1b[8~": '<END>',          # end
    b"\x1b[OA": '<UP>',           # up     (8)
    b"\x1b[OB": '<DOWN>',         # down   (2)
    b"\x1b[OC": '<RIGHT>',        # right  (6)
    b"\x1b[OD": '<LEFT>',         # left   (4)
    b"\x1b[OF": '<END>',          # end    (1)
    b"\x1b[OH": '<HOME>',         # home   (7)

    # reported by cool-RR
    b"\x1b[[A": '<F1>',
    b"\x1b[[B": '<F2>',
    b"\x1b[[C": '<F3>',
    b"\x1b[[D": '<F4>',
    b"\x1b[[E": '<F5>',
    # cool-RR says the rest were good: see issue #99

    # reported by alethiophile see issue #119
    b"\x1b[1;3C": '<Meta-RIGHT>',      # alt-right
    b"\x1b[1;3B": '<Meta-DOWN>',       # alt-down
    b"\x1b[1;3D": '<Meta-LEFT>',       # alt-left
    b"\x1b[1;3A": '<Meta-UP>',         # alt-up
    b"\x1b[5;3~": '<Meta-PAGEUP>',     # alt-pageup
    b"\x1b[6;3~": '<Meta-PAGEDOWN>',   # alt-pagedown
    b"\x1b[1;3H": '<Meta-HOME>',       # alt-home
    b"\x1b[1;3F": '<Meta-END>',        # alt-end
    b"\x1b[1;2C": '<Shift-RIGHT>',
    b"\x1b[1;2B": '<Shift-RIGHT>',
    b"\x1b[1;2D": '<Shift-RIGHT>',
    b"\x1b[1;2A": '<Shift-RIGHT>',
    b"\x1b[3;2~": '<Shift-DELETE>',
    b"\x1b[5;2~": '<Shift-PAGEUP>',
    b"\x1b[6;2~": '<Shift-PAGEDOWN>',
    b"\x1b[1;2H": '<Shift-HOME>',
    b"\x1b[1;2F": '<Shift-END>',
    # end of keys reported by alethiophile
}
# fmt: on
import itertools
import codecs
chr_byte = lambda i: chr(i).encode("latin-1")
chr_uni = chr

CURTSIES_NAMES = {chr_byte(i): "<Ctrl-%s>" % chr(i + 0x60) for i in range(0x00, 0x1B)}
for i in range(0x00, 0x80):
    CURTSIES_NAMES[b"\x1b" + chr_byte(i)] = "<Esc+%s>" % chr(i)
for i in range(0x00, 0x1B):  # Overwrite the control keys with better labels
    CURTSIES_NAMES[b"\x1b" + chr_byte(i)] = "<Esc+Ctrl-%s>" % chr(i + 0x40)
for i in range(0x00, 0x80):
    CURTSIES_NAMES[chr_byte(i + 0x80)] = "<Meta-%s>" % chr(i)
for i in range(0x00, 0x1B):  # Overwrite the control keys with better labels
    CURTSIES_NAMES[chr_byte(i + 0x80)] = "<Meta-Ctrl-%s>" % chr(i + 0x40)

CURTSIES_NAMES.update(_CURTSIES_NAMES)

CURSES_NAMES = {
    b' ': "SPACE",
    b'\x1b': "ESC",
    b'\t': "TAB",
    b'\x7f': "BACKSPACE",
    b'\n': "ENTER",
    b"\x1bOP": "KEY_F(1)",
    b"\x1bOQ": "KEY_F(2)",
    b"\x1bOR": "KEY_F(3)",
    b"\x1bOS": "KEY_F(4)",
    b"\x1b[15~": "KEY_F(5)",
    b"\x1b[17~": "KEY_F(6)",
    b"\x1b[18~": "KEY_F(7)",
    b"\x1b[19~": "KEY_F(8)",
    b"\x1b[20~": "KEY_F(9)",
    b"\x1b[21~": "KEY_F(10)",
    b"\x1b[23~": "KEY_F(11)",
    b"\x1b[24~": "KEY_F(12)",
    # see bpython #626
    b"\x1b[11~": "KEY_F(1)",
    b"\x1b[12~": "KEY_F(2)",
    b"\x1b[13~": "KEY_F(3)",
    b"\x1b[14~": "KEY_F(4)",
    b"\x1b[A": "KEY_UP",
    b"\x1b[B": "KEY_DOWN",
    b"\x1b[C": "KEY_RIGHT",
    b"\x1b[D": "KEY_LEFT",
    b"\x1b[F": "KEY_END",  # https://github.com/bpython/bpython/issues/490
    b"\x1b[H": "KEY_HOME",  # https://github.com/bpython/bpython/issues/490
    b"\x08": "KEY_BACKSPACE",
    b"\x1b[Z": "KEY_BTAB",
    # see curtsies #78 - taken from https://github.com/jquast/blessed/blob/e9ad7b85dfcbbba49010ab8c13e3a5920d81b010/blessed/keyboard.py#L409
    b"\x1b[1~": "KEY_FIND",  # find
    b"\x1b[2~": "KEY_IC",  # insert (0)
    b"\x1b[3~": "KEY_DC",  # delete (.), "Execute"
    b"\x1b[4~": "KEY_SELECT",  # select
    b"\x1b[5~": "KEY_PPAGE",  # pgup   (9)
    b"\x1b[6~": "KEY_NPAGE",  # pgdown (3)
    b"\x1b[7~": "KEY_HOME",  # home
    b"\x1b[8~": "KEY_END",  # end
    b"\x1b[OA": "KEY_UP",  # up     (8)
    b"\x1b[OB": "KEY_DOWN",  # down   (2)
    b"\x1b[OC": "KEY_RIGHT",  # right  (6)
    b"\x1b[OD": "KEY_LEFT",  # left   (4)
    b"\x1b[OF": "KEY_END",  # end    (1)
    b"\x1b[OH": "KEY_HOME",  # home   (7)
}

KEYMAP_PREFIXES = set()
for table in (CURSES_NAMES, CURTSIES_NAMES):
    for k in table:
        if k.startswith(b"\x1b"):
            for i in range(1, len(k)):
                KEYMAP_PREFIXES.add(k[:i])

MAX_KEYPRESS_SIZE = max(
    len(seq) for seq in itertools.chain(CURSES_NAMES.keys(), CURTSIES_NAMES.keys())
)

def decodable(seq: bytes, encoding: str) -> bool:
    try:
        u = seq.decode(encoding)
    except UnicodeDecodeError:
        return False
    else:
        return True

def could_be_unfinished_utf8(seq: bytes) -> bool:
    # http://en.wikipedia.org/wiki/UTF-8#Description
    o = ord(seq[0:1])
    return (
        (o & 0b11100000 == 0b11000000 and len(seq) < 2)
        or (o & 0b11110000 == 0b11100000 and len(seq) < 3)
        or (o & 0b11111000 == 0b11110000 and len(seq) < 4)
        or (o & 0b11111100 == 0b11111000 and len(seq) < 5)
        or (o & 0b11111110 == 0b11111100 and len(seq) < 6)
    )

def could_be_unfinished_char(seq: bytes, encoding: str) -> bool:
    """Whether seq bytes might create a char in encoding if more bytes were added"""
    if decodable(seq, encoding):
        return False  # any sensible encoding surely doesn't require lookahead (right?)
        # (if seq bytes encoding a character, adding another byte shouldn't also encode something)

    if codecs.getdecoder("utf8") is codecs.getdecoder(encoding):
        return could_be_unfinished_utf8(seq)
    elif codecs.getdecoder("ascii") is codecs.getdecoder(encoding):
        return False
    else:
        return True  # We don't know, it could be


def get_key(
    bytes_,
    encoding: str,
    full: bool = False):
    if not all(isinstance(c, bytes) for c in bytes_):
        raise TypeError("get key expects bytes, got %r" % bytes_)  # expects raw bytes
    seq = b"".join(bytes_)
    if len(seq) > MAX_KEYPRESS_SIZE:
        raise ValueError("unable to decode bytes %r" % seq)

    key_known = seq in CURTSIES_NAMES or seq in CURSES_NAMES or decodable(seq, encoding)

    if full and key_known:
        return _key_name(seq, encoding)
    elif seq in KEYMAP_PREFIXES or could_be_unfinished_char(seq, encoding):
        return None  # need more input to make up a full keypress
    elif key_known:
        return _key_name(seq, encoding)
    else:
        # this will raise a unicode error (they're annoying to raise ourselves)
        seq.decode(encoding)
        assert False, "should have raised an unicode decode error"


def _key_name(seq: bytes, encoding: str) -> str:
    # may not be here (and still not decodable) curses names incomplete
    if seq in CURSES_NAMES:
        return CURSES_NAMES[seq]
    if seq in CURTSIES_NAMES:
        return CURTSIES_NAMES[seq]
    # Otherwise, there's no special curses name for this
    try:
        
        # for normal decodable text or a special curtsies sequence with bytes that can be decoded
        return seq.decode(encoding)
    except UnicodeDecodeError:
        # this sequence can't be decoded with this encoding, so we need to represent the bytes
        if len(seq) == 1:
            return "x%02X" % ord(seq)
            # TODO figure out a better thing to return here
        else:
            raise NotImplementedError(
                "are multibyte unnameable sequences possible?"
            )
            return "bytes: " + "-".join(
                "x%02X" % ord(seq[i : i + 1]) for i in range(len(seq))
            )
            # TODO if this isn't possible, return multiple meta keys as a paste event if paste events enabled
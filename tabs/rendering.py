import collections
import re

StringTabulature = collections.namedtuple(
    'StringTabulature',
    (
        'tuning',
        'frets',
    ),
)

Tabulature = collections.namedtuple(
    'Tabulature',
    (
        'strings',
    ),
)

Row = collections.namedtuple(
    'Row',
    (
        'rhythm',
        'tabulature',
        'chords',
        'lyrics',
    ),
)

Tab = collections.namedtuple(
    'Tab',
    (
        'rows',
    ),
)

def whitespace_row_parser(index, lines):
    failure = (False, index, None)

    if lines[index].strip() == '':
        return True, index + 1, lines[index]

    return failure

RHYTHM_LINE_MATCHER = re.compile(r'R(\s*[WHQEST]\.?)*\s*').fullmatch
def rhythm_parser(index, lines):
    return False, index, None

TABULATURE_LINE_MATCHER = re.compile(r'([A-Ga-g][b#]?)\s*\|(-*\d+)*-*').fullmatch
def tabulature_parser(index, lines):
    failure = (False, index, None)
    return failure

CHORDS_LINE_MATCHER = re.compile(r'CH(\s*[A-G][b#]?(add|dim|maj|min|sus)?(\d)?)*').fullmatch
def chords_parser(index, lines):
    failure = (False, index, None)
    return failure

LYRICS_MATCHER = re.compile(r'((\d+)\.)?(.*)').fullmatch
def lyrics_parser(index, lines):
    failure = (False, index, None)

    lyrics_lines = []

    match = LYRICS_MATCHER(lines[index])
    while match:
        lyrics_lines.append(lines[index])
        index += 1

        if index == len(lines):
            break

        match = LYRICS_MATCHER(lines[index])

    if len(lyrics_lines) == 0:
        return failure

    return True, index, tuple(lyrics_lines)

def row_parser(index, lines):
    whitespace_row_success = True
    while whitespace_row_success:
        whitespace_row_success, index, _ = whitespace_row_parser(index, lines)

    rhythm_success, index, rhythm = rhythm_parser(index, lines)

    tabulature_success, index, tabulature = tabulature_parser(index, lines)

    chords_success, index, chords = chords_parser(index, lines)

    lyrics_success, index, lyrics = lyrics_parser(index, lines)

    return (
        rhythm_success or tabulature_success or chords_success or lyrics_success,
        index,
        Row(
            rhythm=rhythm if rhythm_success else None,
            tabulature=tabulature if tabulature_success else None,
            chords=chords if chords_success else None,
            lyrics=lyrics if lyrics_success else None,
        ),
    )



def tab_parser(index, lines):
    rows = []

    while index < len(lines):
        success, index, result = row_parser(index, lines)

        if success:
            rows.append(result)

        else:
            break

    return success, index, Tab(rows=tuple(rows))

def render(source):
    lines = source.splitlines()
    success, index, result = tab_parser(0, lines)
    assert success
    assert index == len(lines)
    return result

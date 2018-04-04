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

TabulatureString = collections.namedtuple(
    'TabulatureString',
    (
        'length',
        'tuning',
        'notes',
    ),
)

TabulatureStringNote = collections.namedtuple(
    'TabulatureStringNote',
    (
        'offset',
        'width',
        'fret',
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

RhythmNote = collections.namedtuple(
    'RhythmNote',
    (
        'prespace',
        'note',
        'dotted',
    ),
)

RHYTHM_LINE_MATCHER = re.compile(r'R(\s*[WHQEST]\.?)*\s*').fullmatch
RHYTHM_NOTE_MATCHER = re.compile(r'(R?\s*)([WHQEST])(\.?)').finditer
def rhythm_parser(index, lines):
    failure = (False, index, None)

    match = RHYTHM_LINE_MATCHER(lines[index])

    if match:
        notes = []
        for match in RHYTHM_NOTE_MATCHER(lines[index]):
            notes.append(RhythmNote(
                prespace=len(match.group(1)) * ' ',
                note=match.group(2),
                dotted=len(match.group(3)) > 0,
            ))

        return True, index + 1, notes

    return failure

TABULATURE_LINE_MATCHER = re.compile(r'([A-Ga-g][b#]?)\s*\|(-*\d+)*-*').fullmatch
TABULATURE_NOTE_MATCHER = re.compile(r'\d+').finditer
def tabulature_parser(index, lines):
    failure = (False, index, None)

    tabulature_lines = []

    match = TABULATURE_LINE_MATCHER(lines[index])

    while match:
        notes = tuple(
            TabulatureStringNote(
                offset=(m.start() - 2) * 8,
                width=len(m.group()) * 8,
                fret=int(m.group()),
            ) for m in TABULATURE_NOTE_MATCHER(lines[index])
        )
        tabulature_lines.append(TabulatureString(
            length=(len(lines[index]) - len(match.group(1)) - 1) * 8,
            tuning=match.group(1),
            notes=notes,
        ))
        index += 1

        if index == len(lines):
            break

        match = TABULATURE_LINE_MATCHER(lines[index])

    if len(tabulature_lines) == 0:
        return failure

    return True, index, Tabulature(
        strings=tuple(tabulature_lines),
    )

CHORDS_LINE_MATCHER = re.compile(r'CH(\s*[A-G][b#]?(add|dim|maj|min|sus)?(\d)?)*').fullmatch
def chords_parser(index, lines):
    failure = (False, index, None)
    return failure

LYRICS_MATCHER = re.compile(r'((\d+)\.)?(.*)').fullmatch
def lyrics_parser(index, lines):
    failure = (False, index, None)

    lyrics_lines = []

    match = LYRICS_MATCHER(lines[index])
    while match and lines[index].strip() != '':
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

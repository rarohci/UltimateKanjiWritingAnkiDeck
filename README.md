# Ultimate Kanji Writing Anki Deck

An Anki deck for learning kanji and practicing handwriting, with interactive stroke practice, vocabulary examples, and multilingual reference information.

## Deck contents

| Item | Included |
| --- | --- |
| Kanji entries | 6,396 unique characters |
| Cards | 12,792 — two per character |
| Note type | `japanese+` |
| Card types | `learningCard` and `writingCard` |
| Organization | Main deck and 60 WaniKani-level subdecks |
| Vocabulary | 56,089 entries across 5,390 kanji notes |
| Package | `ultimateKanjiWritingAnkiDeck.apkg` |

Vocabulary totals count entries across notes. A word containing several kanji can appear in more than one note. Some characters remain in the main deck rather than a level subdeck.

## Card types

### Learning card

The front displays the kanji alongside Sino-Vietnamese, Korean, and Mandarin readings where available.

The back provides stroke diagrams, Japanese readings, definitions, Vietnamese explanations, radicals, components, related characters, and vocabulary.

### Writing card

Practice drawing the kanji with interactive stroke checking.

- **Undo:** remove the last accepted stroke.
- **Redo:** restore an undone stroke.
- **Restart:** clear the drawing and its stroke history.
- **Show reading / Show meaning:** switch between the two prompts.

Each time the writing front renders, it independently chooses readings or meaning with a 50% chance for each. The multilingual reference section stays visible when switching prompts.

Undo and Redo affect handwriting strokes, not Anki review history. Rejected strokes do not enter the undo history.

## Random vocabulary hints

A random word from the note's `vocab` field appears with the current kanji replaced by an outlined square.

For example, when practicing **歓**:

- 歓声 → □声
- 歓迎 → □迎
- 大歓迎 → 大□迎
- 歓迎会 → □迎会

Only words containing the current character are selected. If no matching entry is available, the hint is hidden.

## Vocabulary popups

Tap or click a vocabulary word on the back to display its reading and meaning directly below the word. The popup stays attached while scrolling, and long definitions scroll inside it.

Tap the same word again to close the popup. Desktop users can also hover over a word or press Escape to dismiss the popup.

## Installation

1. Download `ultimateKanjiWritingAnkiDeck.apkg` from this repository or its Releases page.
2. Import the package into Anki or AnkiDroid.
3. Sync if you use Anki on multiple devices.

The package includes the note type, card templates, and shared styling. Separate template installation is not required.

## AnkiDroid writing setup

To reduce accidental answer reveals while drawing:

1. Open **Settings → Gestures**.
2. Set conflicting tap, double-tap, and swipe actions to **No action**.
3. Check gestures assigned to **Answer button 1–4** as well; these may reveal the answer on the front.
4. Use the explicit **Show Answer** button.
5. Leave AnkiDroid's built-in whiteboard off while using the card's handwriting area.

Gesture options can vary by AnkiDroid version. See the [AnkiDroid manual](https://docs.ankidroid.org/manual.html#_gestures).

## Editing vocabulary

The vocabulary field is named `vocab`. Entries use this format:

```text
歓声|かんせい|cheer, shout of joy
歓迎|かんげい|welcome, warm reception
歓喜|かんき|delight, great joy
```

Separate entries with newlines or `<br>`. Each entry contains the word, reading, and meaning, separated by `|`.

## Changes since v1.0

- Consolidated the deck into learning and writing card types.
- Added handwriting Undo, Redo, and Restart controls.
- Added random reading/meaning prompts and a switch button.
- Added vocabulary hints with a square masking the target kanji.
- Improved responsive buttons and shared card styling.
- Added touch handling for writing and vocabulary interaction.
- Anchored vocabulary popups to the selected word.
- Merged vocabulary lists and removed duplicate words within each note.
- Standardized vocabulary templates on the `vocab` field.
- Removed unused scripts and simplified vocabulary rendering.

## Notes

Supporting information varies by character; some fields are empty. The package contains new cards and no review history.

Handwriting controls use the bundled customized Hanzi Writer library. Replacing that library may require changes to the controls. Rendering and touch behavior can vary between Anki clients.

## Credits

Interactive handwriting uses [Hanzi Writer](https://hanziwriter.org/).

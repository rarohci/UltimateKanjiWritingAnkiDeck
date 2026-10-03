# How to use the deck

## First installation

1. Install Anki Desktop or AnkiDroid.
2. Import `ultimateKanjiWritingAnkiDeck.apkg`.
3. Open the `ultimateKanjiWritingAnkiDeck` deck.
4. Start with a learning card to review the character, then use the writing
   card to practice its stroke order.

The package already includes the note type, templates, SVG files, font, and
subdecks. You do not need to install the template files separately for normal
use.

## What appears on each card

Learning cards present reference information. Writing cards present a prompt,
an interactive drawing area, and the current character's multilingual
reference information.

The writing front randomly starts with either the readings or meaning prompt.
Use the prompt button to switch at any time.

## Writing practice

Draw one stroke at a time in the square. The card accepts a stroke when its
position, direction, shape, endpoints, and length are close enough to the
reference data.

The buttons work as follows:

- **Undo:** go back one accepted stroke.
- **Redo:** restore a stroke removed by Undo.
- **Restart:** clear all accepted strokes and reset the quiz. It also refreshes
  the vocabulary hint.

Only accepted strokes are stored in the card's temporary history. Press Anki's
normal **Show Answer** button when you finish or want to reveal the answer.

## Vocabulary hint popup

When a matching vocabulary word exists, the writing card replaces the current
kanji with an outlined square. Tap or click that hint to see:

- the word's reading;
- the word's meaning.

Tap the hint again to close the popup. You can also press **Escape** or click
outside it. A long meaning scrolls inside the popup. Restart closes the popup
before selecting the next hint.

If no matching vocabulary entry exists, the hint stays hidden.

## Decks

Use the WaniKani level subdecks when you want level-based study. Characters with
no vocabulary entry are grouped in:

```text
ultimateKanjiWritingAnkiDeck::noVocabsKanji
```

Moving cards between subdecks changes organization only; it does not change the
note fields or writing data.

## Gesture settings on AnkiDroid

Drawing can conflict with device gestures. In AnkiDroid:

1. Open **Settings → Gestures**.
2. Set tap, double-tap, and swipe actions that could reveal an answer to
   **No action**.
3. Check gestures assigned to **Answer button 1–4**.
4. Use the explicit **Show Answer** button.
5. Disable AnkiDroid's built-in whiteboard while using this card.

The names of gesture settings vary between AnkiDroid versions.

## Updating the templates

Changing files in this repository does not update a deck already imported into
Anki. Copy each complete front/back template into the matching card type and
copy `templates/style.css` into Styling. Save copies of your current templates
before replacing them.

The source templates are provided for developers who want to customize the
cards. In Anki, open **Tools → Manage Note Types**, select `japanese+`, and
edit the card templates or styling. Keep the field names unchanged unless you
also update every template reference.

The writing front depends on the customized Hanzi Writer code embedded in its
template. Changes to that bundled code can affect stroke recognition,
Undo/Redo, touch input, or the SVG data loader.

## Troubleshooting

- **The font looks different:** confirm that
  `NotoSerifJP-VariableFont_wght.ttf` is present in Anki's media collection.
- **The writing hint is missing:** the note has no vocabulary word containing
  the current character.
- **A stroke is rejected:** draw from the correct starting point in the correct
  direction, follow the bend, and finish near the reference endpoint.
- **A gesture reveals the answer:** review AnkiDroid's gesture assignments.
- **The popup does not close:** tap the hint again, press **Escape**, or click
  outside the popup.

## Vocabulary format

The `vocab` field accepts entries separated by new lines or `<br>`:

```text
歓迎|かんげい|welcome, warm reception
歓喜|かんき|delight, great joy
```

The format is `word|reading|meaning`. The writing hint selects only entries
whose word contains the current kanji.

## Updating an existing deck

1. Back up your collection, including media, and save any custom templates.
2. Download the `.apkg` from the release you intend to install and read its notes.
3. If you have customized notes or templates, first try the import in a separate
   profile. Check the import summary and inspect representative cards.
4. Confirm that your edits, review history, media, and both card types behave as
   expected before continuing normal study and synchronization.

Do not delete your existing deck merely to install an update. Import behavior
depends on note identity, your client version, and import options; preservation
of every local customization is not guaranteed.

## Appearance and writing limitations

The templates select light/dark colors through the client's system-color-scheme
signal. This can differ from an app's own theme setting. The writing grid scales
with the viewport; font rendering, gestures, and spacing can vary by client.

Short bends and hooks can be rejected even when they look close to the reference.
Compare stroke order, direction, and endpoints with the answer. A thicker pen
changes the visible line and does not guarantee greater acceptance tolerance.
Use your own recall to choose a review grade. Drawing history is temporary and
is not a saved handwriting record.

For problems, include the kanji, stroke number, card side, app/version, device,
and a screenshot in a
[GitHub issue](https://github.com/rarohci/UltimateKanjiWritingAnkiDeck/issues).
See [DISCLAIMER.md](DISCLAIMER.md) for data and compatibility limitations.

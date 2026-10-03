# Unreleased — Documentation

- Replaced mockups with actual front-template screenshots.
- Added download/support links, backup guidance, and compatibility limitations.
- Added handwriting and data-accuracy disclaimers.
- Added Hanzi Writer attribution and clarified unresolved text-data provenance.
- Corrected the FSRS learning-step example and daily card-limit explanation.

# v1.1.0 — Changes since v1.0

- Added stroke Undo, Redo, and Restart controls.
- Added random reading or meaning prompts with a switch button.
- Kept multilingual readings visible.
- Added random vocabulary hints with a square masking the kanji.
- Improved responsive buttons and shared styling.
- Improved touch handling while writing.
- Anchored vocabulary popups beside the selected word.
- Merged vocabulary lists and removed duplicates.
- Updated templates to use the vocab field.
- Removed unused scripts.

# v1.2.0 — Changes since v1.1.0

- Added precise SVG curve sampling to generate denser handwriting medians.
- Converted all 6,396 kanji SVG sources into validated stroke and median data.
- Added kanji-named SVG media copies and updated image mappings.
- Added a separate package with the `noVocabsKanji` subdeck for 1,006 notes.
- Included the Noto Serif JP font and its license in the updated package.
- Removed unused note-type metadata from the updated package.
- Added random vocabulary hint changes when Restart is pressed.
- Added a separate writing-card variant with tappable vocabulary reading and meaning popups.
- Added SVG conversion documentation, validation tests, and package audit reports.
- Verified media integrity, card relationships, templates, layouts, and handwriting controls.
- Kept the original Anki package unchanged.
- Added system light/dark theme colors across all card templates.
- Softened reference strokes so user-drawn strokes remain easier to see.
- Made the writing grid responsive, centered, and better spaced around the vocabulary hint.
- Added SRS and Anki review-setting guidance to the README.

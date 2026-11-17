# REVIEW: The Incredible Story of the Cartel Olympics

## Creative calls
- Built storyline **A: The Evidence Board**: a single 3 x 3 cardboard board, filmed in one continuous take. Act one pins up Mau Morales's legend. Act two stamps each claim and pins the record over it. The film ends on a pull-back to the whole board, then a push-in to the movie clapperboard.
- Not built: **B: One Date, Two Stories** and **C: The Trailer That Never Was** (see STORYLINES.md).
- Narration uses Kokoro `am_michael`, generated locally for free. Captions are burned in, 4 to 6 words per group, timed to whisper word timings.
- **No music.** HeyGen isn't signed in, so the catalog is unavailable (sound.md §3). The film has narration and sound effects only.
- Every claim is attributed: Mau's story is told as "he says", and the findings are what The Atlantic reported (RESEARCH.md). Real people appear only as text. The only faces are generic silhouettes.

## Measured vs looked at
- `check`: 0 errors. Warnings kept on purpose:
  - `text_below_floor`: only during the pull-back to the whole board (87-90 s), where the board is shown at 1/3 scale as an overview. The stamps stay large enough to read there.
  - `composition_file_too_large` and `timeline_track_too_dense`: the board is one continuous take, so it is a single composition.
- Looked at 15 QA stills plus the review/phone sheets. Fixed the following:
  - stamps unreadable over the drawings (they now sit on paper labels);
  - the clapper arm poking into the cell above;
  - the NEVER HAPPENED stamp spilling into the next cell;
  - the arm reading like a finger (now a forearm and fist);
  - an empty tournament cell from 26 to 30 s (the header now lands on "Mexico's biggest cartels").
- The sound was **measured, not heard**: effect placement and peaks were computed, and the rendered file was checked with `hyperframes audio`.

## Weakest shot / with more time
- The S6 believers chain is text-heavy (email, clapper, Peña strip, sticky note). It would read better with fewer words and one more drawn object.
- Kokoro's read is flat compared with a real Vox narrator. A HeyGen voice, or the person's own recording, would lift it most. A music bed would be the next biggest gain.
- The source facts come from secondary write-ups of the paywalled Atlantic article. Verify against the article before publishing.

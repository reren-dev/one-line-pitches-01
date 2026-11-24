#!/usr/bin/env python3
"""Write the one-line pitch for make.fun's "A Day of One-Line Pitches".

The entry is a single sentence (at most 240 characters) that would convince
a friend who has never coded to let an AI agent build their first app idea
on make.fun. This program writes that sentence, exactly, to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).
"""

import os
import tempfile

# The pitch: one sentence, 219 characters.
# It speaks to the friend directly ("that app idea you've been carrying
# around"), names make.fun and the AI agent, gives a concrete reason to say
# yes now (a working first version today, your idea finally real) and makes
# handing the idea over feel easy and low risk (no code to learn, nothing
# to install). Plain words, no jargon, no promise it cannot keep.
LINE = (
    "That app idea you've been carrying around for years \u2014 describe it "
    "in plain words and let an AI agent on make.fun build a working first "
    "version today, no code to learn and nothing to install, just your "
    "idea finally real."
)

MAX_CHARS = 240


def main() -> None:
    if not 1 <= len(LINE) <= MAX_CHARS:
        raise SystemExit(
            f"pitch must be 1-{MAX_CHARS} characters, got {len(LINE)}"
        )
    if not LINE.strip():
        raise SystemExit("pitch must not be only whitespace")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")
    os.makedirs(out_dir, exist_ok=True)
    # Atomic write: write to a temp file in the same directory, verify the
    # bytes round-trip as the exact pitch, then move it into place, so a
    # reader never sees a half-written entry.txt.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as handle:
            handle.write(LINE)
        with open(tmp_path, "r", encoding="utf-8", newline="") as handle:
            if handle.read() != LINE:
                raise SystemExit("round-trip check failed: entry.txt mismatch")
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()

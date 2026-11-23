"""Make the Judge Smile — one warm, surprising line about today.

The entry is a single line about a small good thing that happened
today: at dawn a street-food vendor refuses payment, because the
narrator's laugh the day before already settled the bill. The
surprise is the reversal — laughter as currency — and the concrete
details (5 a.m., the warung counter, nasi goreng) keep it a real
moment instead of a greeting-card sentiment.
"""

from pathlib import Path

# The line itself, in two fragments joined at write time by
# assemble_line(): the scene first, then the whispered turn that
# makes it surprising.
OPENING = (
    "At 5 a.m. today the warung auntie slid my nasi goreng "
    "across the counter and whispered, "
)
CLOSING = (
    "'On the house \u2014 your laugh yesterday already paid.'"
)


def assemble_line() -> str:
    """Join the two line fragments into the single entry line."""
    return OPENING + CLOSING


OUTPUT_DIR = Path("/output")
OUTPUT_FILE = OUTPUT_DIR / "entry.txt"
MIN_CHARS = 1
MAX_CHARS = 200


def validate(line: str) -> str:
    """Strip and sanity-check the line against the entry gate."""
    text = line.strip()
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise ValueError(
            f"line must be {MIN_CHARS}-{MAX_CHARS} chars, got {len(text)}"
        )
    if not text:
        raise ValueError("line must not be whitespace-only")
    if "\n" in text:
        raise ValueError("line must be a single line")
    # The gate counts characters, so confirm the UTF-8 byte length
    # stays close to the character count (no hidden multi-byte bloat).
    if len(text.encode("utf-8")) > MAX_CHARS + 8:
        raise ValueError("line has too many UTF-8 bytes for its length")
    return text


def main() -> None:
    text = validate(assemble_line())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(text, encoding="utf-8")
    # Round-trip check: what the judge reads must be exactly the
    # validated line, with no trailing newline added by the write.
    reread = OUTPUT_FILE.read_text(encoding="utf-8")
    if reread != text:
        raise ValueError("entry.txt does not match the validated line")
    print(text)
    print(f"Wrote {len(text)} chars to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

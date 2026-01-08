from pathlib import Path

CONTENT_ROOT = Path("content")

def has_front_matter(text: str) -> bool:
    stripped = text.lstrip()
    return stripped.startswith(("---", "+++", "{"))

def make_title(path: Path) -> str:
    return path.stem.replace("-", " ").replace("_", " ").title()

for md_file in CONTENT_ROOT.rglob("*.md"):
    raw = md_file.read_bytes()

    # Skip empty files
    if not raw:
        continue

    # Only act if FIRST BYTE is literal hyphen "-"
    if raw[:1] != b"-":
        continue

    text = raw.decode("utf-8", errors="replace")

    # If it already has front matter, leave it alone
    if has_front_matter(text):
        continue

    title = make_title(md_file)

    front_matter = (
        "---\n"
        f'title: "{title}"\n'
        "---\n\n"
    )

    md_file.write_text(front_matter + text, encoding="utf-8")
    print(f"Fixed leading-hyphen file → {md_file}")

import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path("content")

# Build an index of all .md files by stem
md_index = {}
for path in ROOT.rglob("*.md"):
    md_index.setdefault(path.stem, []).append(path)

wikilink_re = re.compile(r"\[\[([^\[\]]+)\]\]")

def replace_links(text: str) -> str:
    def repl(match):
        name = match.group(1)

        # Only resolve filename.md
        if name not in md_index:
            return match.group(0)

        target = md_index[name][0]

        # Path relative to content/
        rel_path = target.relative_to(ROOT).as_posix()

        # URL encode path (spaces → %20, etc.)
        # encoded_path = quote(rel_path)
        # only encode spaces
        encoded_path = rel_path.replace(" ", "%20")

        display = name.replace("_", " ")

        return f"[{display}]({encoded_path})"

    return wikilink_re.sub(repl, text)

for md_file in ROOT.rglob("*.md"):
    original = md_file.read_text(encoding="utf-8")
    updated = replace_links(original)

    if updated != original:
        md_file.write_text(updated, encoding="utf-8")
        print(f"Updated: {md_file}")

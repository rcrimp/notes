import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path("content")

# Index markdown by stem (for [[Note Name]])
md_index: dict[str, list[Path]] = {}
for p in ROOT.rglob("*.md"):
    md_index.setdefault(p.stem, []).append(p)

# Index png by:
#  - content-relative path (for ![[path/to/img.png]])
#  - filename only (for ![[img.png]])
png_by_rel: dict[str, Path] = {}
png_by_name: dict[str, list[Path]] = {}
for p in ROOT.rglob("*.png"):
    rel = p.relative_to(ROOT).as_posix()
    png_by_rel[rel] = p
    png_by_name.setdefault(p.name, []).append(p)

# Matches both [[...]] and ![[...]]
wikilink_re = re.compile(r"(!?)\[\[([^\[\]]+)\]\]")

def encode_url_path(path: str) -> str:
    # URL-encode, but keep slashes so directories stay readable
    path = path.replace("'", "").replace('’', "")
    return quote(path, safe="/")

def replace_links(text: str) -> str:
    def repl(match: re.Match) -> str:
        bang = match.group(1)           # "" or "!"
        inner = match.group(2).strip()  # content inside [[...]]
        inner_lower = inner.lower()

        # ---- Embedded PNG images: ![[...png]] ----
        if bang == "!" and inner_lower.endswith(".png"):
            # Prefer treating it as a content-relative path if it contains '/'
            target = None
            if "/" in inner:
                target = png_by_rel.get(inner)
            else:
                hits = png_by_name.get(inner)
                target = hits[0] if hits else None

            if not target:
                return match.group(0)

            rel_path = target.relative_to(ROOT).as_posix()
            return f"![](/{encode_url_path(rel_path)})"

        # ---- Regular links: [[name]] -> resolve to name.md only ----
        # If someone writes [[something.png]] without '!', leave it alone.
        if inner_lower.endswith(".png"):
            return match.group(0)

        hits = md_index.get(inner)
        if not hits:
            return match.group(0)

        target = hits[0]
        rel_path = target.relative_to(ROOT).as_posix()
        display = inner.replace("_", " ")
        return f"[{display}]({encode_url_path(rel_path)})"

    return wikilink_re.sub(repl, text)

for md_file in ROOT.rglob("*.md"):
    original = md_file.read_text(encoding="utf-8")
    updated = replace_links(original)

    if updated != original:
        md_file.write_text(updated, encoding="utf-8")
        print(f"Updated: {md_file}")

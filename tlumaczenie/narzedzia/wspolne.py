"""Wspólne funkcje skryptów tłumaczenia."""
import re
import subprocess
from pathlib import Path

from markdown_it import MarkdownIt

REPO = Path(__file__).resolve().parents[2]

_md = MarkdownIt("commonmark")

HEADING_ID_RE = re.compile(r"\s*\{\s*#([^\s}]+)\s*\}\s*$")


def parse(text: str):
    return _md.parse(text)


def naglowki_md(text: str) -> list[tuple[int, int, str]]:
    """Nagłówki ATX poza kodem: (numer linii od 0, poziom, surowa linia)."""
    lines = text.split("\n")
    out = []
    for tok in parse(text):
        if tok.type == "heading_open" and tok.map:
            lineno = tok.map[0]
            raw = lines[lineno]
            if "#" not in raw.lstrip("> ")[:7]:
                continue  # setext
            out.append((lineno, int(tok.tag[1]), raw))
    return out


def git_show(rev: str, path: str) -> str:
    return subprocess.run(
        ["git", "show", f"{rev}:{path}"],
        cwd=REPO,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def rel(path) -> str:
    p = Path(path).resolve()
    try:
        return str(p.relative_to(REPO))
    except ValueError:
        return str(path)

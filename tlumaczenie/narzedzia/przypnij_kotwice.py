#!/usr/bin/env python3
"""Przypina kotwice nagłówków w src/*.md do id wygenerowanych przez mdBook (D3).

Użycie: przypnij_kotwice.py [--tryb=attr|a-id] [--book tmp/book-base] [--src src]
"""
import argparse
import sys
from pathlib import Path

from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wspolne import naglowki_md  # noqa: E402


def id_z_html(html_path: Path) -> list[str]:
    soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    if main is None:
        return []
    return [h["id"] for h in main.select(":is(h1,h2,h3,h4,h5,h6)[id]")]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tryb", choices=["attr", "a-id"], default="attr")
    ap.add_argument("--book", default="tmp/book-base")
    ap.add_argument("--src", default="src")
    args = ap.parse_args()

    src = Path(args.src)
    book = Path(args.book)
    piny = 0
    pominiete = []
    for md in sorted(src.glob("*.md")):
        if md.name == "SUMMARY.md":
            continue
        text = md.read_text(encoding="utf-8")
        lines = text.split("\n")
        heads = naglowki_md(text)
        html = book / (md.stem + ".html")
        ids = id_z_html(html) if html.exists() else None
        if ids is None or len(ids) != len(heads):
            pominiete.append(md.name)
            print(
                f"POMINIĘTO {md.name}: nagłówki md={len(heads)}, "
                f"html={'brak pliku' if ids is None else len(ids)}",
                file=sys.stderr,
            )
            continue
        # od końca, żeby wstawianie linii nie przesuwało numerów
        for (lineno, _level, _title), hid in reversed(list(zip(heads, ids))):
            line = lines[lineno].rstrip()
            if args.tryb == "attr":
                lines[lineno] = f"{line} {{#{hid}}}"
            else:
                prefix = "> " if line.lstrip().startswith(">") else ""
                lines[lineno : lineno + 1] = [
                    f'{prefix}<a id="{hid}"></a>',
                    prefix.rstrip(),
                    line,
                ]
            piny += 1
        md.write_text("\n".join(lines), encoding="utf-8")
    print(f"piny: {piny}, pominięte pliki: {len(pominiete)}")
    return 1 if pominiete else 0


if __name__ == "__main__":
    sys.exit(main())

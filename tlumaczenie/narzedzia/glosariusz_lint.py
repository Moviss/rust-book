#!/usr/bin/env python3
"""Bramka G6: zakazane warianty terminów z GLOSARIUSZ.md (kolumna „Zakazane”).

Użycie: glosariusz_lint.py [--glosariusz PLIK] [--wyjatki PLIK] [pliki...]
Bez plików sprawdza src/*.md i quizzes/*.toml. Kod wyjścia 1, jeśli są trafienia.
"""
import argparse
import re
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wspolne import REPO, rel  # noqa: E402

TU = Path(__file__).resolve().parent
FENCE_RE = re.compile(r"(?ms)^[ >]{0,6}(`{3,}|~{3,}).*?^[ >]{0,6}\1[`~]*[ \t]*$")
INLINE_CODE_RE = re.compile(r"(`+)(?:(?!\1).)+?\1", re.S)
LINK_DEF_RE = re.compile(r"(?m)^\s*\[[^\]]+\]:\s*\S+.*$")
URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
# angielski odpowiednik w nawiasie przy pierwszym wystąpieniu (D4): (*ownership*)
GLOSS_RE = re.compile(r"\((?:\*[^*\n]+\*|_[^_\n]+_)\)")
TOML_CODE_RE = re.compile(r'(?ms)^(prompt\.program|answer\.stdout)\s*=\s*""".*?"""')
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")


def blank(m):
    return re.sub(r"[^\n]", " ", m.group(0))


def proza(text: str, toml: bool) -> str:
    """Tekst z wyczyszczonym kodem (z zachowaniem numerów linii i kolumn)."""
    if toml:
        text = TOML_CODE_RE.sub(blank, text)
    for rx in (FENCE_RE, COMMENT_RE, INLINE_CODE_RE, LINK_DEF_RE, URL_RE, GLOSS_RE):
        text = rx.sub(blank, text)
    return text


def wczytaj_glosariusz(path: Path):
    reguly = []
    kol = None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("|"):
            kol = None if not line.strip() else kol
            continue
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line.strip().strip("|"))]
        if kol is None:
            low = [c.lower() for c in cells]
            idx = [i for i, c in enumerate(low) if c.startswith("zakazane")]
            if idx:
                kol = idx[0]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if kol >= len(cells):
            continue
        cell = cells[kol].strip()
        if not cell:
            continue
        if cell.startswith("`") and cell.endswith("`"):
            cell = cell[1:-1]
        cell = cell.replace("\\|", "|")
        reguly.append((cells[0], re.compile(cell, re.I)))
    return reguly


def wczytaj_wyjatki(path: Path):
    if not path.exists():
        return {}
    return tomllib.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--glosariusz", default=str(TU.parent / "GLOSARIUSZ.md"))
    ap.add_argument("--wyjatki", default=str(TU / "wyjatki.toml"))
    ap.add_argument("pliki", nargs="*")
    args = ap.parse_args()

    reguly = wczytaj_glosariusz(Path(args.glosariusz))
    wyj = wczytaj_wyjatki(Path(args.wyjatki))
    pliki = args.pliki or sorted(
        [str(p) for p in (REPO / "src").glob("*.md")]
        + [str(p) for p in (REPO / "quizzes").glob("*.toml")]
    )
    trafienia = 0
    for f in pliki:
        sciezka = rel(f)
        akcept = [
            e.get("tekst", "").casefold()
            for sekcja in (wyj.get(sciezka, {}), wyj.get("*", {}))
            for e in sekcja.get("glosariusz", [])
        ]
        raw = Path(f).read_text(encoding="utf-8")
        text = proza(raw, f.endswith(".toml"))
        lines = text.split("\n")
        raw_lines = raw.split("\n")
        for n, line in enumerate(lines, 1):
            for termin, rx in reguly:
                for m in rx.finditer(line):
                    if m.group(0).casefold() in akcept:
                        continue
                    trafienia += 1
                    ctx = raw_lines[n - 1].strip()
                    print(f"{sciezka}:{n}: [{termin}] „{m.group(0)}”: {ctx[:120]}")
    print(f"Podsumowanie: reguł {len(reguly)}, trafień {trafienia}")
    return 1 if trafienia else 0


if __name__ == "__main__":
    sys.exit(main())

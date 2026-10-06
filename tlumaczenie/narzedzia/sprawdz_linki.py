#!/usr/bin/env python3
"""Bramka G4: zepsute kotwice w zbudowanej książce.

Użycie: sprawdz_linki.py <katalog_book> [--zapisz-baseline] [--raport-tekstow]
"""
import argparse
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup

BASELINE = Path(__file__).resolve().parent / "linki-baseline.txt"
POMIJANE = {"print.html", "toc.html", "404.html"}


def wczytaj(book: Path):
    strony = {}
    for p in sorted(book.glob("*.html")):
        if p.name in POMIJANE:
            continue
        strony[p.name] = BeautifulSoup(p.read_text(encoding="utf-8"), "html.parser")
    return strony


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("book")
    ap.add_argument("--zapisz-baseline", action="store_true")
    ap.add_argument("--raport-tekstow", action="store_true")
    ap.add_argument("--baseline", default=str(BASELINE))
    args = ap.parse_args()

    strony = wczytaj(Path(args.book))
    ids = {
        n: {el["id"] for el in s.find_all(id=True)} | {el["name"] for el in s.find_all(attrs={"name": True})}
        for n, s in strony.items()
    }
    zepsute = set()
    raport = []
    for nazwa, soup in strony.items():
        main_el = soup.find("main") or soup
        for a in main_el.find_all("a", href=True):
            href = a["href"]
            u = urlsplit(href)
            if u.scheme or u.netloc or not u.fragment:
                continue
            cel = Path(u.path).name if u.path else nazwa
            if u.path and not u.path.endswith(".html"):
                continue
            frag = unquote(u.fragment)
            if cel not in ids:
                zepsute.add(f"{nazwa} -> {href} (brak pliku)")
                continue
            if frag not in ids[cel]:
                zepsute.add(f"{nazwa} -> {href}")
                continue
            if args.raport_tekstow and "header" not in (a.get("class") or []):
                el = strony[cel].find(id=frag)
                if el is not None and el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
                    tekst = " ".join(a.get_text().split())
                    tytul = " ".join(el.get_text().split())
                    znak = "=" if tekst.casefold() == tytul.casefold() else "≠"
                    raport.append(f"{znak} {nazwa} | {tekst} | {cel}#{frag} | {tytul}")

    if args.raport_tekstow:
        for line in raport:
            print(line)
        return 0

    if args.zapisz_baseline:
        Path(args.baseline).write_text(
            "".join(f"{z}\n" for z in sorted(zepsute)), encoding="utf-8"
        )
        print(f"zapisano baseline: {len(zepsute)} zepsutych linków")
        return 0

    base = set()
    if Path(args.baseline).exists():
        base = {l for l in Path(args.baseline).read_text(encoding="utf-8").splitlines() if l}
    nowe = sorted(zepsute - base)
    for z in nowe:
        print(f"BŁĄD [G4] nowy zepsuty link: {z}")
    print(f"Podsumowanie: zepsute {len(zepsute)}, w baseline {len(zepsute & base)}, nowe {len(nowe)}")
    return 1 if nowe else 0


if __name__ == "__main__":
    sys.exit(main())

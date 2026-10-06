#!/usr/bin/env python3
"""Tabela postępu i porównanie tytułów.

  postep.py --init      dopisuje tabelę plików do tlumaczenie/POSTEP.md
  postep.py --summary   wypisuje pary (tytuł w SUMMARY.md, H1 pliku)
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from wspolne import HEADING_ID_RE, REPO, git_show  # noqa: E402

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+\.md)\)")
QUIZ_RE = re.compile(r"\{\{#quiz \.\./quizzes/([^}\s]+)\}\}")
FENCE_RE = re.compile(r"(?ms)^ {0,3}(`{3,}|~{3,}).*?^ {0,3}\1[`~]*\s*$")
POSTEP = REPO / "tlumaczenie" / "POSTEP.md"


def summary():
    text = (REPO / "src" / "SUMMARY.md").read_text(encoding="utf-8")
    return [(t, f) for t, f in LINK_RE.findall(text)]


def rozdzial(f):
    m = re.match(r"ch(\d+)-", f)
    if m:
        return str(int(m.group(1)))
    if f.startswith("appendix"):
        return "dod."
    return "0"


def init():
    tekst = POSTEP.read_text(encoding="utf-8")
    if "## Pliki" in tekst:
        print("POSTEP.md ma już tabelę plików", file=sys.stderr)
        return 1
    wiersze = [
        "## Pliki",
        "",
        "| plik | rozdz. | słowa EN | quizy | status | agent | próby | G5 | uwagi |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    suma = 0
    for _, f in summary():
        src = git_show("pl-source", f"src/{f}")
        slowa = len(FENCE_RE.sub("", src).split())
        suma += slowa
        quizy = ", ".join(q.removesuffix(".toml") for q in QUIZ_RE.findall(src)) or "—"
        wiersze.append(f"| {f} | {rozdzial(f)} | {slowa} | {quizy} | do zrobienia | | 0 | | |")
    wiersze.append("")
    blok = "\n".join(wiersze) + "\n"
    if "## Decyzje orkiestratora" in tekst:
        tekst = tekst.replace("## Decyzje orkiestratora", blok + "\n## Decyzje orkiestratora", 1)
    else:
        tekst += "\n" + blok
    POSTEP.write_text(tekst, encoding="utf-8")
    print(f"dopisano {len(summary())} plików, {suma} słów EN (bez bloków kodu)")
    return 0


def h1(f):
    for line in (REPO / "src" / f).read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return HEADING_ID_RE.sub("", line[2:]).strip()
    return None


def tytuly():
    for t, f in summary():
        h = h1(f)
        znak = "=" if h == t else "≠"
        print(f"{znak} {f} | SUMMARY: {t} | H1: {h}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", action="store_true")
    g.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    sys.exit(init() if a.init else tytuly())

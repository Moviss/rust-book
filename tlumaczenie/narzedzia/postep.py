#!/usr/bin/env python3
"""Tabela postępu i porównanie tytułów.

  postep.py --init      dopisuje tabelę plików do tlumaczenie/POSTEP.md
  postep.py --summary   wypisuje pary (tytuł w SUMMARY.md, H1 pliku)
  postep.py --ustaw STATUS [--agent ID] [--proba] [--g5 N] [--uwagi TXT] PLIK...
                        zmienia wiersze tabeli (PLIK bez src/)
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
    """Pierwszy nagłówek pliku poza blokami kodu (Brown używa często `##`)."""
    from wspolne import naglowki_md

    heads = naglowki_md((REPO / "src" / f).read_text(encoding="utf-8"))
    if not heads:
        return None
    raw = heads[0][2].lstrip("> ").lstrip("#").strip()
    return HEADING_ID_RE.sub("", raw).strip()


def tytuly():
    for t, f in summary():
        h = h1(f)
        znak = "=" if h == t else "≠"
        print(f"{znak} {f} | SUMMARY: {t} | H1: {h}")
    return 0


def ustaw(a):
    lines = POSTEP.read_text(encoding="utf-8").split("\n")
    cele = {Path(f).name for f in a.pliki}
    znalezione = set()
    for i, line in enumerate(lines):
        if not line.startswith("| "):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) != 9 or c[0] not in cele:
            continue
        c[4] = a.ustaw
        if a.agent is not None:
            c[5] = a.agent
        if a.proba:
            c[6] = str(int(c[6] or 0) + 1)
        if a.g5 is not None:
            c[7] = a.g5
        if a.uwagi is not None:
            c[8] = a.uwagi
        lines[i] = "| " + " | ".join(c) + " |"
        znalezione.add(c[0])
    POSTEP.write_text("\n".join(lines), encoding="utf-8")
    brak = cele - znalezione
    if brak:
        print("nie znaleziono: " + ", ".join(sorted(brak)), file=sys.stderr)
        return 1
    return 0


def stan():
    from collections import Counter
    cnt = Counter()
    for line in POSTEP.read_text(encoding="utf-8").splitlines():
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if line.startswith("| ") and len(c) == 9 and c[0].endswith(".md"):
            cnt[c[4]] += 1
            if c[4] not in ("gotowe", "do zrobienia"):
                print(f"{c[0]}: {c[4]} (agent {c[5]}, próby {c[6]})")
    print(dict(cnt))
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--init", action="store_true")
    g.add_argument("--summary", action="store_true")
    g.add_argument("--stan", action="store_true")
    g.add_argument("--ustaw", metavar="STATUS")
    ap.add_argument("--agent")
    ap.add_argument("--proba", action="store_true")
    ap.add_argument("--g5")
    ap.add_argument("--uwagi")
    ap.add_argument("pliki", nargs="*")
    a = ap.parse_args()
    if a.init:
        sys.exit(init())
    if a.summary:
        sys.exit(tytuly())
    if a.stan:
        sys.exit(stan())
    sys.exit(ustaw(a))

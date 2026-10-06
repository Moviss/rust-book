#!/usr/bin/env python3
"""Autotesty skryptów tłumaczenia. Uruchomienie: python3 tlumaczenie/narzedzia/testy/uruchom.py"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

TU = Path(__file__).resolve().parent
NARZ = TU.parent
REPO = NARZ.parents[1]
PY = sys.executable
wyniki = []


def run(*args):
    return subprocess.run([PY, *map(str, args)], cwd=REPO, capture_output=True, text=True)


def test(nazwa, ok, out=""):
    wyniki.append(ok)
    print(f"{'OK  ' if ok else 'FAIL'} {nazwa}")
    if not ok:
        print("     " + out.strip().replace("\n", "\n     ")[:1500])


def git_show(path):
    return subprocess.run(
        ["git", "show", f"pl-source:{path}"], cwd=REPO, capture_output=True, text=True, check=True
    ).stdout


def uszkodzenie(nazwa, plik, funkcja, oczekiwany_fragment):
    oryg = git_show(plik)
    zepsuty = funkcja(oryg)
    assert zepsuty != oryg, f"uszkodzenie '{nazwa}' nic nie zmieniło"
    with tempfile.TemporaryDirectory(dir=REPO / "tmp") as d:
        en = Path(d) / ("en" + Path(plik).suffix)
        pl = Path(d) / ("pl" + Path(plik).suffix)
        en.write_text(oryg, encoding="utf-8")
        pl.write_text(zepsuty, encoding="utf-8")
        r = run(NARZ / "sprawdz.py", "--orig", en, pl)
    ok = r.returncode != 0 and oczekiwany_fragment in r.stdout
    test(f"sprawdz.py wykrywa: {nazwa}", ok, r.stdout)


def bez_uszkodzenia(nazwa, plik, funkcja):
    oryg = git_show(plik)
    zmieniony = funkcja(oryg)
    with tempfile.TemporaryDirectory(dir=REPO / "tmp") as d:
        en = Path(d) / ("en" + Path(plik).suffix)
        pl = Path(d) / ("pl" + Path(plik).suffix)
        en.write_text(oryg, encoding="utf-8")
        pl.write_text(zmieniony, encoding="utf-8")
        r = run(NARZ / "sprawdz.py", "--orig", en, pl)
    test(f"sprawdz.py akceptuje: {nazwa}", r.returncode == 0, r.stdout)


def zamien_pierwsze(rx, repl, flags=0):
    return lambda s: re.sub(rx, repl, s, count=1, flags=flags)


def main():
    (REPO / "tmp").mkdir(exist_ok=True)

    # 1. Nietknięte pliki względem pl-source: zero błędów.
    pliki = sorted(str(p.relative_to(REPO)) for p in (REPO / "src").glob("*.md")) + sorted(
        str(p.relative_to(REPO)) for p in (REPO / "quizzes").glob("*.toml")
    )
    r = subprocess.run(
        [PY, NARZ / "sprawdz.py", "--ref", "pl-source", "--cicho", *pliki],
        cwd=REPO, capture_output=True, text=True,
    )
    test("sprawdz.py --ref pl-source na nietkniętych plikach: zero błędów",
         r.returncode == 0 and "BŁĘDY 0" in r.stdout, r.stdout)

    # 2. Uszkodzenia wykrywane.
    md = "src/ch01-01-installation.md"
    uszkodzenie("zmieniony blok kodu", md,
                zamien_pierwsze(r"(?m)^\$ rustc --version$", "$ rustc --wersja"), "szkielet")
    uszkodzenie("zmieniony kod inline", md,
                zamien_pierwsze(r"`rustup`", "`rustupx`"), "kod inline nie istnieje")
    uszkodzenie("usunięty {#id}", md,
                zamien_pierwsze(r" \{#[^}]+\}", ""), "nagłówek bez {#id}")
    uszkodzenie("zmieniony {#id}", md,
                zamien_pierwsze(r"\{#([^}]+)\}", r"{#\1-x}"), "szkielet")
    uszkodzenie("zepsuty link referencyjny", md,
                zamien_pierwsze(r"\]\[otherinstall\]", "][inna-etykieta]"), "URL-e")
    uszkodzenie("zmieniony URL definicji", md,
                zamien_pierwsze(r"(?m)^(\[otherinstall\]: \S+)", r"\1-x"), "URL-e")
    uszkodzenie("usunięty <a id>", md,
                zamien_pierwsze(r'(?m)^<a id="[^"]*"></a>\n', ""), "atrybuty id")
    uszkodzenie("utracona notatka", md,
                zamien_pierwsze(r"(?m)^> Note: ", "> "), "notatki")
    uszkodzenie("zmieniony @Perm", "src/ch04-02-references-and-borrowing.md",
                zamien_pierwsze(r"@Perm\{read\}", "@Perm{czytanie}"), "@Perm")
    uszkodzenie("zmieniony atrybut <Listing>", "src/ch02-00-guessing-game-tutorial.md",
                zamien_pierwsze(r'number="2-1"', 'number="2-9"'), "szkielet")
    uszkodzenie("złamana linia <Listing>", "src/ch02-00-guessing-game-tutorial.md",
                zamien_pierwsze(r'(<Listing number="2-1") ', "\\1\n"), "szkielet")
    uszkodzenie("usunięta dyrektywa quizu", "src/ch04-01-what-is-ownership.md",
                zamien_pierwsze(r"\{\{#quiz [^}]*\}\}", ""), "dyrektywy")

    q = "quizzes/ch04-01-ownership-sec2-moves.toml"
    uszkodzenie("zmienione id quizu", q,
                zamien_pierwsze(r'id = "889ca9ac', 'id = "889ca9ad'), "pole id")
    uszkodzenie("zmienione answer.doesCompile", q,
                zamien_pierwsze(r"doesCompile = (true|false)",
                                lambda m: "doesCompile = " + ("false" if m.group(1) == "true" else "true")),
                "doesCompile")
    uszkodzenie("zepsuty TOML", q, zamien_pierwsze(r'"""', '"'), "nie parsuje")
    uszkodzenie("kod inline w dystraktorze", q,
                zamien_pierwsze(r"`if`", "`jeśli`"), "kod inline nie istnieje")
    mp = "quizzes/ch17-05-design-challenge-references.toml"
    uszkodzenie("zmieniony multipart", mp, zamien_pierwsze(r'multipart = "q"', 'multipart = "r"'),
                "multipart")
    uszkodzenie("zmieniony kod w [multipart]", mp,
                zamien_pierwsze(r"-> &Asset;", "-> &Zasob;"), "bloki kodu")
    uszkodzenie("zmieniona opcja z kodu", mp, zamien_pierwsze(r'\["2"\]', '["dwa"]'), "z kodu")
    uszkodzenie("powtórzona opcja", "quizzes/ch04-01-ownership-sec2-moves.toml",
                zamien_pierwsze(r'"Freeing the same memory a second time"',
                                '"Using a pointer that points to freed memory"'),
                "wzajemnie różne")

    # 3. Dozwolone zmiany przechodzą.
    bez_uszkodzenia("przetłumaczona notatka i caption", "src/ch02-00-guessing-game-tutorial.md",
                    lambda s: s.replace("> Note: ", "> Uwaga: ").replace(
                        'caption="Code that gets a guess from the user and prints it"',
                        'caption="Kod, który pobiera odpowiedź użytkownika i ją wypisuje"'))
    bez_uszkodzenia("przetłumaczony tekst linku referencyjnego", md,
                    zamien_pierwsze(r"\[Other Rust Installation Methods page\]\[otherinstall\]",
                                    "[stronie Inne metody instalacji Rusta][otherinstall]"))
    bez_uszkodzenia("Filename → Plik", "src/ch01-02-hello-world.md",
                    lambda s: s.replace('<span class="filename">Filename: ', '<span class="filename">Plik: '))

    # 4. glosariusz_lint.py na fixture.
    r = run(NARZ / "glosariusz_lint.py", "--glosariusz", TU / "fixture-glosariusz.md",
            "--wyjatki", TU / "fixture-wyjatki.toml", TU / "fixture-tekst.md")
    out = r.stdout
    test("glosariusz_lint.py znajduje zakazany wariant",
         r.returncode != 0 and "„Posiadanie”" in out and "„kopiec”" in out, out)
    test("glosariusz_lint.py respektuje wyjątek i ignoruje kod",
         "„kopca”" not in out and "posiadaniem" not in out and "skrzynia" not in out, out)
    test("glosariusz_lint.py obsługuje \\| w regexie", "„kopiec”" in out, out)

    # 5. sprawdz_linki.py na sztucznej książce.
    with tempfile.TemporaryDirectory(dir=REPO / "tmp") as d:
        dd = Path(d)
        (dd / "a.html").write_text('<main><h2 id="x">X</h2><a href="b.html#y">ok</a>'
                                   '<a href="b.html#z">zły</a><a href="#x">ok</a></main>')
        (dd / "b.html").write_text('<main><h2 id="y">Y</h2></main>')
        (dd / "base.txt").write_text("")
        r = run(NARZ / "sprawdz_linki.py", dd, "--baseline", dd / "base.txt")
        test("sprawdz_linki.py wykrywa zepsutą kotwicę",
             r.returncode != 0 and "b.html#z" in r.stdout and "nowe 1" in r.stdout, r.stdout)

    n_ok = sum(wyniki)
    print(f"\n{n_ok}/{len(wyniki)} testów zaliczonych")
    return 0 if all(wyniki) else 1


if __name__ == "__main__":
    sys.exit(main())

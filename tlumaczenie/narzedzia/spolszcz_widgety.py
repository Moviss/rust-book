#!/usr/bin/env python3
"""Spolszcza napisy interfejsu w zbudowanej książce (po `mdbook build`).

Napisy widżetu quizów (mdbook-quiz) i szablonu mdBooka są wkompilowane w ich
binarki, więc nie da się ich przetłumaczyć w `src/`. Skrypt podmienia je w
wygenerowanych plikach. Każda podmiana ma oczekiwaną liczbę wystąpień: jeśli po
aktualizacji mdbook-quiz lub mdBooka napis zniknie albo się zmieni, skrypt
kończy się błędem (CI czerwone) zamiast po cichu zostawić angielski tekst.

Użycie: spolszcz_widgety.py [KATALOG_KSIĄŻKI]   (domyślnie: book)
"""
import sys
from pathlib import Path

# Odmiana „pytanie” po liczebniku (1 pytanie, 2–4 pytania, 5+ pytań).
PYTANIA = (
    '(c=>c==1?"pytanie":c%10>=2&&c%10<=4&&(c%100<10||c%100>=20)'
    '?"pytania":"pytań")(n.questions.length)'
)

# (stary, nowy, oczekiwana liczba wystąpień)
QUIZ_JS = [
    ('"Why is this quiz fullscreen?"', '"Dlaczego quiz zajmuje cały ekran?"', 1),
    (
        '"We want to know how much you are learning that can be recalled'
        " without assistance. Please complete the quiz without re-reading the"
        ' text, e.g. by opening it in another tab."',
        '"Quiz sprawdza, ile zapamiętujesz bez pomocy. Rozwiąż go, nie'
        ' zaglądając ponownie do tekstu (np. w innej karcie)."',
        1,
    ),
    ('"Question"," ",(e.attempt', '"Pytanie"," ",(e.attempt', 1),
    ('," question",n.questions.length>1&&"s"', '," ",' + PYTANIA, 1),
    ('"You can either"', '"Możesz"', 1),
    ('"retry the quiz")," ","or"," "', '"rozwiązać quiz ponownie")," ","albo"," "', 1),
    ('"see the correct answers"', '"zobaczyć poprawne odpowiedzi"', 1),
    ('"Answer Review"', '"Przegląd odpowiedzi"', 1),
    ('"You answered"," "', '"Poprawne odpowiedzi:"," "', 1),
    ('," ","questions correctly."', ',"."', 1),
    ('},"Start")', '},"Rozpocznij")', 1),
    ('"Write your answer here..."', '"Wpisz tutaj odpowiedź…"', 2),
    (
        '"Determine whether the program will pass the compiler. If it passes,'
        ' write the expected output of the program if it were executed."',
        '"Ustal, czy program się skompiluje. Jeśli tak, wpisz, co wypisze po'
        ' uruchomieniu."',
        1,
    ),
    ('"This program:"', '"Ten program:"', 1),
    ('"DOES compile"', '"SIĘ kompiluje"', 1),
    ('"option-separator"},"OR"', '"option-separator"},"ALBO"', 1),
    ('"does NOT compile"', '"NIE kompiluje się"', 1),
    ('"The output of this program will be:"', '"Ten program wypisze:"', 2),
    ('"Write the program\'s stdout here..."', '"Wpisz tutaj standardowe wyjście programu…"', 1),
    (
        '"This program"," ",Z.createElement("strong",null,e.doesCompile?"does":"does not")," compile."',
        '"Ten program"," ",Z.createElement("strong",null,e.doesCompile?"kompiluje się":"nie kompiluje się"),"."',
        1,
    ),
    ('"Report a bug in this question"', '"Zgłoś błąd w tym pytaniu"', 1),
    ('"Report a bug"', '"Zgłoś błąd"', 1),
    (
        '"If you found an issue in this question (e.g. a typo or an incorrect'
        ' answer), please describe the issue and report it:"',
        '"Jeśli w tym pytaniu jest błąd (np. literówka lub zła odpowiedź),'
        ' opisz go i wyślij zgłoszenie:"',
        1,
    ),
    ('"Bug feedback"', '"Opis błędu"', 1),
    ('"Submit bug feedback"', '"Wyślij zgłoszenie"', 1),
    ('"Question ",e.substring(0,1)," has multiple parts."', '"Pytanie ",e.substring(0,1)," składa się z kilku części."', 1),
    ('" The box below contains the shared context for each part."', '" Poniższa ramka zawiera wspólny kontekst wszystkich części."', 1),
    ('"h4",null,"Question ",r)', '"h4",null,"Pytanie ",r)', 2),
    ('"h4",null,"Response")', '"h4",null,"Odpowiedź")', 1),
    (
        '"In 1-2 sentences, please explain why you picked this answer. \xa0\xa0"',
        '"W 1–2 zdaniach wyjaśnij, dlaczego wybierasz tę odpowiedź. \xa0\xa0"',
        1,
    ),
    (
        "Normally, we only observe *whether* readers get a question correct or incorrect. \n"
        "This explanation helps us understand *why* a reader answers a particular way, so \n"
        "we can better improve the surrounding text.",
        "Zwykle widać tylko, *czy* odpowiedź jest poprawna. To wyjaśnienie pokazuje, \n"
        "*dlaczego* ktoś odpowiada w określony sposób, co pomaga ulepszyć tekst.",
        1,
    ),
    ('title:"Explanation"', 'title:"Wyjaśnienie"', 1),
    ('onClick:()=>T(!0)},"Submit")', 'onClick:()=>T(!0)},"Wyślij")', 1),
    ('Z.createElement("input",{type:"submit"})', 'Z.createElement("input",{type:"submit",value:"Wyślij"})', 1),
    ('"Return to question context "', '"Wróć do kontekstu pytania "', 1),
    ('"You answered:"', '"Twoja odpowiedź:"', 1),
    ('"The correct answer is:"', '"Poprawna odpowiedź:"', 1),
    ("`**Context**:", "`**Kontekst**:", 1),
]

QUIZ_CSS = [
    ('content:"✓ Correct"', 'content:"✓ Poprawnie"', 1),
    ('content:"✗ Incorrect"', 'content:"✗ Niepoprawnie"', 1),
]

# Szablon mdBooka: liczba wystąpień na stronę z pełnym szablonem.
HTML = [
    ('<h2 class="mdbook-help-title">Keyboard shortcuts</h2>', '<h2 class="mdbook-help-title">Skróty klawiszowe</h2>', 1),
    (
        "<p>Press <kbd>←</kbd> or <kbd>→</kbd> to navigate between chapters</p>",
        "<p>Naciśnij <kbd>←</kbd> lub <kbd>→</kbd>, aby przejść do poprzedniego lub następnego rozdziału</p>",
        1,
    ),
    (
        "<p>Press <kbd>S</kbd> or <kbd>/</kbd> to search in the book</p>",
        "<p>Naciśnij <kbd>S</kbd> lub <kbd>/</kbd>, aby przeszukać książkę</p>",
        1,
    ),
    ("<p>Press <kbd>?</kbd> to show this help</p>", "<p>Naciśnij <kbd>?</kbd>, aby wyświetlić tę pomoc</p>", 1),
    ("<p>Press <kbd>Esc</kbd> to hide this help</p>", "<p>Naciśnij <kbd>Esc</kbd>, aby ukryć tę pomoc</p>", 1),
    ('title="Toggle Table of Contents"', 'title="Pokaż/ukryj spis treści"', 1),
    ('aria-label="Toggle Table of Contents"', 'aria-label="Pokaż/ukryj spis treści"', 1),
    ('aria-label="Table of contents"', 'aria-label="Spis treści"', 1),
    ('title="Change theme"', 'title="Zmień motyw"', 1),
    ('aria-label="Change theme"', 'aria-label="Zmień motyw"', 1),
    ('aria-label="Themes"', 'aria-label="Motywy"', 1),
    ('id="mdbook-theme-default_theme">Auto<', 'id="mdbook-theme-default_theme">Automatyczny<', 1),
    ('id="mdbook-theme-light">Light<', 'id="mdbook-theme-light">Jasny<', 1),
    ('id="mdbook-theme-coal">Coal<', 'id="mdbook-theme-coal">Grafitowy<', 1),
    ('id="mdbook-theme-navy">Navy<', 'id="mdbook-theme-navy">Granatowy<', 1),
    ('title="Search (`/`)"', 'title="Szukaj (`/`)"', 1),
    ('aria-label="Toggle Searchbar"', 'aria-label="Pokaż/ukryj wyszukiwarkę"', 1),
    ('placeholder="Search this book ..."', 'placeholder="Szukaj w książce…"', 1),
    ('title="Print this book"', 'title="Drukuj książkę"', 1),
    ('aria-label="Print this book"', 'aria-label="Drukuj książkę"', 1),
    ('title="Git repository"', 'title="Repozytorium Git"', 1),
    ('aria-label="Git repository"', 'aria-label="Repozytorium Git"', 1),
]
# Nawigacja: na stronie pierwszej/ostatniej brak jednego z linków.
HTML_NAV = [
    ('title="Previous chapter"', 'title="Poprzedni rozdział"'),
    ('aria-label="Previous chapter"', 'aria-label="Poprzedni rozdział"'),
    ('title="Next chapter"', 'title="Następny rozdział"'),
    ('aria-label="Next chapter"', 'aria-label="Następny rozdział"'),
    ('aria-label="Page navigation"', 'aria-label="Nawigacja między stronami"'),
]

SEARCHER_JS = [
    (
        "return count + ' search result for \\'' + searchterm + '\\':';",
        "return count + ' wynik dla „' + searchterm + '”:';",
        1,
    ),
    (
        "return 'No search results for \\'' + searchterm + '\\'.';",
        "return 'Brak wyników dla „' + searchterm + '”.';",
        1,
    ),
    (
        "return count + ' search results for \\'' + searchterm + '\\':';",
        "return 'Liczba wyników dla „' + searchterm + '”: ' + count;",
        1,
    ),
]

BOOK_JS = [
    ("'No output'", "'Brak wyjścia'", 1),
    ("'Show hidden lines'", "'Pokaż ukryte wiersze'", 2),
    ('title="Show hidden lines"', 'title="Pokaż ukryte wiersze"', 1),
    ('aria-label="Show hidden lines"', 'aria-label="Pokaż ukryte wiersze"', 1),
    ("'Hide lines'", "'Ukryj wiersze'", 2),
    ("'Copy to clipboard'", "'Kopiuj do schowka'", 2),
    ("'Copied!'", "'Skopiowano!'", 1),
]

bledy = []


def podmien(path: Path, reguly, opis=None):
    s = path.read_text(encoding="utf-8")
    for stary, nowy, ile in reguly:
        n = s.count(stary)
        if n != ile:
            bledy.append(f"{opis or path}: {stary[:70]!r}: oczekiwano {ile}, jest {n}")
            continue
        s = s.replace(stary, nowy)
    path.write_text(s, encoding="utf-8")


def jeden(book: Path, wzorzec: str) -> Path | None:
    pliki = sorted(book.glob(wzorzec))
    if len(pliki) != 1:
        bledy.append(f"{wzorzec}: oczekiwano 1 pliku, jest {len(pliki)}")
        return None
    return pliki[0]


def main() -> int:
    book = Path(sys.argv[1] if len(sys.argv) > 1 else "book")
    for wzorzec, reguly in (
        ("quiz/quiz-embed.iife.js", QUIZ_JS),
        ("quiz/style.css", QUIZ_CSS),
        ("searcher-*.js", SEARCHER_JS),
        ("book-*.js", BOOK_JS),
    ):
        p = jeden(book, wzorzec)
        if p:
            podmien(p, reguly)

    strony = 0
    for p in sorted(book.rglob("*.html")):
        s = p.read_text(encoding="utf-8")
        if 'id="mdbook-help-popup"' not in s:
            continue  # przekierowania i inne strony bez szablonu
        strony += 1
        podmien(p, HTML, rel := str(p.relative_to(book)))
        s = p.read_text(encoding="utf-8")
        for stary, nowy in HTML_NAV:
            s = s.replace(stary, nowy)
        p.write_text(s, encoding="utf-8")
        for stary, _ in HTML_NAV:
            if stary in p.read_text(encoding="utf-8"):
                bledy.append(f"{rel}: pozostało {stary!r}")
    if strony < 100:
        bledy.append(f"za mało stron z szablonem mdBooka: {strony}")

    for b in bledy[:50]:
        print("BŁĄD", b)
    print(f"Spolszczono interfejs: stron {strony}, błędów {len(bledy)}")
    return 1 if bledy else 0


if __name__ == "__main__":
    sys.exit(main())

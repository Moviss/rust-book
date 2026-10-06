# Plan tłumaczenia książki na język polski

Roadmapa przetłumaczenia forka `Moviss/rust-book` (wersja Brown University z quizami
i wizualizacjami aquascope) na polski. Plan jest napisany tak, żeby nowa sesja Claude
Code mogła go wykonać autonomicznie od Fazy 0 do Fazy 5. Wersja 2, po autoreview
(sekcja 11).

---

## 0. Jak uruchomić

### 0.1. Przygotowanie ręczne (użytkownik, przed startem sesji)

```bash
# Rust; mdbook-quiz kompiluje programy z quizów domyślnym toolchainem rustup,
# dlatego ustawiamy 1.90 jako domyślny (tak jak w CI)
# --no-modify-path: ~/.bash_profile należy do roota, więc instalator nie może go
# edytować; PATH dla zsh dopisujemy sami do ~/.zshenv
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --no-modify-path --default-toolchain 1.90
grep -qs 'cargo/env' ~/.zshenv || echo '. "$HOME/.cargo/env"' >> ~/.zshenv
source "$HOME/.cargo/env"

# mdBook 0.5.2 i mdbook-quiz 0.5.0 (binarki macOS arm64, te same wersje co w CI)
curl -sSL https://github.com/rust-lang/mdBook/releases/download/v0.5.2/mdbook-v0.5.2-aarch64-apple-darwin.tar.gz | tar -xz -C "$HOME/.cargo/bin"
curl -sSL https://github.com/cognitive-engineering-lab/mdbook-quiz/releases/download/v0.5.0/mdbook-quiz_aarch64-apple-darwin_bare.tar.gz | tar -xz -C "$HOME/.cargo/bin"

# Kontrola
cd ~/private-projects/rust-book && rustc --version && mdbook --version && mdbook-quiz --version
```

Aquascope nie ma binarki na macOS i **nie jest potrzebny lokalnie**. Lokalne buildy
oznaczają go jako opcjonalny, a pełny build z aquascope robi CI. Ochronę składni
aquascope zapewniają bramki G1 i G2.

### 0.2. Prompt startowy dla nowej sesji

```
Zrealizuj plan z tlumaczenie/PLAN.md od Fazy 0 do Fazy 5, autonomicznie.
Stan prowadź w tlumaczenie/POSTEP.md. Masz zgodę na: commity i push do origin/main
oraz push tagów pl-base i pl-source; edycję CLAUDE.md, book.toml, ferris.js,
README.md i packages/mdbook-trpl zgodnie z planem. Commity po angielsku, bez stopek
AI (bez Co-Authored-By). Zatrzymaj się tylko w sytuacjach z sekcji 7.3.
```

Opcjonalnie dopisz na końcu `Zatrzymaj się po pilocie (Faza 2).`, jeśli chcesz
przejrzeć próbkę stylu przed tłumaczeniem całości.

### 0.3. Wznowienie po kompaktowaniu kontekstu

Długa sesja na pewno przejdzie kompaktowanie. Po nim orkiestrator:
1. Ponownie czyta **cały** `tlumaczenie/PLAN.md`, a od Fazy 1 także
   `tlumaczenie/KONWENCJE.md`.
2. Czyta `tlumaczenie/POSTEP.md` (lista kroków faz i tabela plików).
3. Dla plików w stanie `tłumaczenie` lub `przegląd` stosuje regułę wznowienia z
   sekcji 4.3. **Nigdy** nie uruchamia drugiego agenta na plik, którego agent może
   jeszcze pracować.
4. Kontynuuje od pierwszego niezamkniętego kroku.

---

## 1. Cel i zakres

**Cel:** polska wersja książki do nauki Rusta, opublikowana na
https://moviss.github.io/rust-book/. Tłumaczenie techniczne: ważne pojęcia zostają
w oryginale (przy pierwszym użyciu w nawiasie) albo po angielsku, jeśli tak mówią
polscy programiści.

**Skala (zmierzona 2026-10-06, commit `88250e03`):**

| Element | Liczba |
|---|---|
| Pliki `src/*.md` | 121: 120 jednostek tłumaczenia (wszystkie w `SUMMARY.md`) + sam `SUMMARY.md` (Faza 4); ok. 195 tys. słów łącznie z kodem |
| Nagłówki w `src/*.md` | 590 (bez setext; 12 wewnątrz cytatów, zawsze w pierwszej linii cytatu) |
| Quizy `quizzes/*.toml` | 93 pliki, 222 pytania (141 MultipleChoice, 64 Tracing, 17 ShortAnswer); 4 pliki mają tabelę `[multipart]` |
| Pliki `.md` z quizami | 72; każdy quiz jest podpięty dokładnie raz przez `{{#quiz ...}}` |
| Największy plik / rozdział | `ch02-00` ok. 6 tys. słów; rozdział 17 ok. 15,4 tys. słów |
| Rozdziały z ponad 6 plikami | 12, 15, 17 (po 7), dodatki (8) |
| Kotwice i odnośniki | 108 + 10 linków z `#` w `src/`, linki w 12 plikach quizów, 181 linii `<a id>` |
| Znaczniki `@Perm` aquascope w prozie | 68 w `src/`, 2 w quizach |

**W zakresie:**
- cała treść `src/*.md`: rozdziały, dodatki i strony Brown (`experiment-intro.md`,
  `end-of-experiment.md`, `title-page.md`, `foreword.md`);
- `src/SUMMARY.md` i wszystkie quizy, w tym tabele `[multipart]`;
- teksty `alt`, podpisy listingów, tabel i rysunków;
- etykiety „Note”/„Filename” w preprocesorach i podpowiedzi Ferrisa w `ferris.js`;
- `book.toml` (tytuł, język) i notka o nieoficjalnym tłumaczeniu.

**Poza zakresem:**
- kod w każdej postaci: bloki kodu, kod inline, `<pre>`/`<code>` w HTML,
  `listings/`, `output.txt`, bloki `aquascope`, znaczniki `@Perm`, także komentarze
  w kodzie (D2);
- interfejs mdBook (wyszukiwarka, przyciski), widżetów quizu i aquascope: to
  zewnętrzne narzędzia, więc etykiety zostają po angielsku;
- wyszukiwarka działa, ale bez polskiej odmiany: „własność” nie znajdzie
  „własności” inaczej niż przez prefiks;
- grafiki SVG z angielskim tekstem w `src/img/` (tłumaczymy tylko `alt`);
- `nostarch/`, `first-edition/`, `second-edition/`, `2018-edition/`, `redirects/`,
  widżet feedbacku (`js-extensions/`).

---

## 2. Decyzje

Przed startem możesz zmienić dowolną z nich. W trakcie wykonania orkiestrator ich
nie zmienia (sekcja 7.3).

| # | Decyzja | Uzasadnienie |
|---|---|---|
| D1 | Tłumaczymy **w miejscu** (`src/`, `quizzes/`). Nazwy plików i URL-e bez zmian. | Fork jest publiczny, ale służy do własnej nauki. Stałe URL-e zachowują przekierowania i linki z quizów. |
| D2 | **Kod nietknięty bajt po bajcie**, łącznie z komentarzami, napisami w `println!`, kodem inline i znacznikami `@Perm`. | `output.txt` cytuje linie źródła, bloki aquascope są kompilowane, a `@Perm` z nieznaną nazwą wywraca build CI. Zmiany z upstream w `listings/` scalają się bez konfliktów. |
| D3 | **Kotwice nagłówków przypięte do angielskich id** przez `{#id}` (np. `## Stos i sterta {#the-stack-and-the-heap}`). | Linki wewnętrzne, linki z quizów i zakładki działają bez przepisywania. |
| D4 | Termin z glosariusza przy **pierwszym wystąpieniu w prozie pliku**: „polski (*english*)”, potem sam polski. Termin zostawiony po angielsku: „*crate* (objaśnienie)”, potem bez kursywy. **Nagłówki bez objaśnień**: objaśnienie trafia do pierwszego zdania prozy. | Prośba użytkownika. Nagłówki zasilają menu, wyszukiwarkę i raport odwołań. |
| D5 | **Nie odmieniamy kodu inline.** Piszemy „typ `String`”, „metoda `push`”, a nie „`String`a”. | Czytelność i zgodność z kodem (G1 sprawdza kod inline). |
| D6 | Do czytelnika zwracamy się w 2. os. l.poj. bez zaimka („możesz”). Autorzy mówią „my” („napiszemy”). | Naturalny rejestr polskich książek technicznych. |
| D7 | Typografia: „…”, wewnętrzne ‚…’, półpauza ze spacjami „ – ”, nagłówki zdaniowe. W odmianie angielskich terminów apostrof typograficzny: crate’a, future’a. | Polska typografia. Prosty `'` i `"` łamią atrybuty `caption`. |
| D8 | W quizach **bez zmian** zostają: `id`, `type`, klucz `multipart` w pytaniu, `prompt.program`, `answer.doesCompile`, `answer.lineNumber`, `answer.stdout`, `prompt.answerIndex`, `prompt.sortAnswers`, `answer.answer` i `answer.alternatives` pytań ShortAnswer, opcje MultipleChoice składające się wyłącznie z kodu, kod w każdym polu. | `id` są kluczem zapisanych odpowiedzi. Wszystkie 17 odpowiedzi ShortAnswer to kod lub liczby, wpisywane i porównywane dosłownie. |
| D9 | Łatka w `packages/mdbook-trpl`: notatki rozpoznają też `> Uwaga: `, a etykieta pliku to „Plik:”. Podpis „Listing N-M” zostaje. Podpisy: „Tabela N-M”, „Rysunek N-M”. W prozie: „listing 4-1” (odmieniany), „rozdział 4”, „dodatek A”. | Preprocesor rozpoznaje dosłownie `Note: ` (`note/mod.rs:63`), a „Filename:” jest wpisane na sztywno (`listing/mod.rs:234`). |
| D10 | Tytuł: „Język programowania Rust”; `language = "pl"` w `book.toml`. | Ustawia `<html lang="pl">` (sprawdzone). |
| D11 | Commity po angielsku, **bez stopek AI**. Jeden commit na rozdział, push co 2–3 rozdziały. W commitach tylko jawne ścieżki (`git add src quizzes tlumaczenie ...`), nigdy `git add -A`. | Preferencja użytkownika. Push to ok. 15 min CI. Lokalny `pnpm` brudzi `js-extensions/pnpm-lock.yaml`. |
| D12 | Notka „nieoficjalne tłumaczenie” z linkiem do oryginału na **`experiment-intro.md`** (strona startowa, `index.html`) i `title-page.md`, plus sekcja w `README.md` (po angielsku). Dodatkowe linki są dozwolone przez `wyjatki.toml`. | Warunek Apache-2.0 §4(b) przy publikacji zmienionych plików. Notka musi być na stronie, którą czytelnik widzi pierwszą. |

---

## 3. Fakty techniczne

**Zweryfikowane:**
- mdBook 0.5.2:
  - `## Tytuł {#id}` daje `<h2 id="id">`; postać ` { #id }`, którą zapisuje
    pulldown-cmark-to-cmark, też działa, także wewnątrz notatki;
  - `language = "pl"` daje `<html lang="pl">`.
- **Brak preprocesora to błąd**, chyba że `optional = true`. Nadpisanie bez edycji
  `book.toml`: `MDBOOK_PREPROCESSOR__AQUASCOPE__OPTIONAL=true`. Bloki aquascope
  renderują się wtedy jako zwykły kod.
- Każda strona mdBook ma dodatkowe `<h1 class="menu-title">` i
  `<h2 class="mdbook-help-title">` bez id, poza `<main>`. **Nagłówki treści są tylko
  w `<main>`**: 590 w markdownie = 590 id w HTML.
- `packages/mdbook-trpl`:
  - parsuje z `ENABLE_HEADING_ATTRIBUTES` (`lib.rs:34`);
  - `trpl-note` serializuje cały rozdział z powrotem (`note/mod.rs:130`), ale
    zachowuje id nagłówków;
  - mdbook-quiz i mdbook-aquascope podmieniają tylko fragmenty tekstu.
- **mdbook-quiz 0.5.0 zawsze waliduje quizy**; klucz `validate` w `book.toml` jest
  ignorowany. Walidacja kompiluje i uruchamia 64 programy Tracing `rustc` z
  domyślnego toolchaina rustup. `MDBOOK_PREPROCESSOR__QUIZ__OPTIONAL` nie pomaga,
  gdy binarka jest, ale się wywraca.
- `mdbook-aquascope` 0.4.0 akceptuje w `@Perm` tylko nazwy
  read/write/own/flow i modyfikatory gained/lost/missing.
- Build wymaga `js-extensions/packages/feedback/dist/*`, więc raz uruchamiamy
  `pnpm init-repo`. Lokalny pnpm 10 przepisuje `pnpm-lock.yaml` (CI używa pnpm 6).
- Pierwszy deploy na Pages przeszedł (run `37487147336`). Fork jest **publiczny**.
- Lokalnie są Python 3.12 z `tomllib`, `markdown_it` 2.2 i `bs4`.

**Do potwierdzenia w Fazie 0 (z planem awaryjnym):**
- **R1:** przypięte `{#id}` przetrwają cały lokalny pipeline. Bramka G0; fallback
  to idiom repo `<a id="..."></a>` nad nagłówkiem.
- **R2:** lokalna walidacja quizów przechodzi. Jeśli mdbook-quiz zawodzi z
  przyczyn środowiskowych, lokalnie zastępujemy go przelotowym preprocesorem
  `MDBOOK_PREPROCESSOR__QUIZ__COMMAND="python3 tlumaczenie/narzedzia/przelot.py"`.
  Quizy pilnuje wtedy G2, a pełną walidację robi CI.

---

## 4. Architektura wykonania

### 4.1. Role i zasady

- **Orkiestrator** (główna sesja): planuje paczki, uruchamia subagentów, odpala
  skrypty bramek, scala glosariusz, prowadzi `POSTEP.md`, robi commity i pushe.
  **Sam nie tłumaczy rozdziałów** i nie czyta ich w całości, poza autoreview pilota
  i naprawami.
- **Tłumacz** (subagent, jeden na plik `.md` razem z jego quizami): tłumaczy w
  miejscu i uruchamia `sprawdz.py` aż do zera błędów.
- **Recenzent** (subagent, jeden na grupę plików do ok. 8 tys. słów EN): porównuje
  EN z PL, nanosi poprawki, uruchamia `sprawdz.py`.

**Zasady twarde:**
- Subagenci nie używają gita poza `git show`. Edytują tylko przydzielone pliki.
- Tylko orkiestrator edytuje `GLOSARIUSZ.md`, `KONWENCJE.md`, `POSTEP.md`,
  `wyjatki.toml`, `src/SUMMARY.md`, `book.toml`, `CLAUDE.md` i robi commity.
- Najwyżej **6 subagentów naraz**.
- Subagenci zgłaszają nowe terminy w raporcie, a orkiestrator scala je między
  paczkami.
- `KONWENCJE.md` ma pierwszeństwo przed `style-guide.md` i odpowiednimi
  fragmentami `CLAUDE.md` (Title Case, twarde zawijanie).

### 4.2. `POSTEP.md`

Plik powstaje **jako pierwsza czynność Fazy 0**: na początku to sama lista kroków
faz. Tabelę plików dopisuje `postep.py --init` w Fazie 1.

```
## Kroki
- [x] F0.1 Weryfikacja narzędzi
- [ ] F0.2 ...
## Pliki
| plik | rozdz. | słowa EN | quizy | status | agent | próby | G5 | uwagi |
```

Statusy: `do zrobienia` → `tłumaczenie` → `przetłumaczone` → `przegląd` → `gotowe`.
W kolumnie `agent` zapisuj nazwę/id subagenta, a w `próby` licznik prób.
Orkiestrator aktualizuje plik po każdej zmianie stanu. Zmiana jest commitowana
razem z rozdziałem.

### 4.3. Reguła wznowienia

Dla pliku w stanie `tłumaczenie` lub `przegląd`:
- jeśli agent z kolumny `agent` wciąż działa (ListAgents lub oczekujące
  powiadomienie), **czekaj**;
- jeśli agent się zakończył, uruchom `sprawdz.py`:
  - zielony: przejdź do następnego statusu;
  - czerwony: uruchom nowego agenta z dopiskiem „plik może być częściowo
    przetłumaczony, dokończ go” i zwiększ licznik `próby`.

### 4.4. Pętla orkiestratora (Faza 3)

1. Z `POSTEP.md` wybierz następny rozdział. Jeśli ma więcej niż 6 plików, podziel
   go na fale po najwyżej 6 tłumaczy. Kolejną falę uruchamiaj, gdy zwalniają się
   miejsca. Mały rozdział możesz połączyć z następnym, łącznie do 6 plików.
2. Uruchom tłumaczy (szablon 6.1) i ustaw status `tłumaczenie`, zapisując agenta.
3. Po powrocie tłumacza uruchom `sprawdz.py` na jego plikach. Nie ufaj samemu
   raportowi.
   - **Zielony:** ustaw status `przetłumaczone`.
   - **Czerwony:** odeślij do tego samego agenta (SendMessage) z wynikiem
     skryptu, najwyżej 2 razy. Potem popraw sam. Jeśli i to nie pomaga,
     przejdź do sekcji 7.3.
4. Gdy cały rozdział jest `przetłumaczone`, uruchom recenzentów (szablon 6.2): po
   jednym na grupę plików do ok. 8 tys. słów EN. Ustaw status `przegląd`, a po
   powrocie ponownie uruchom `sprawdz.py`.
5. **Build i linki:**
   `MDBOOK_PREPROCESSOR__AQUASCOPE__OPTIONAL=true mdbook build -d tmp/book-pl`,
   potem `python3 tlumaczenie/narzedzia/sprawdz_linki.py tmp/book-pl`.
   Build potrwa kilka minut, bo walidacja quizów kompiluje programy. Jeśli G3
   lub G4 zawiedzie, wskaż plik z komunikatu, napraw sam albo odeślij do
   recenzenta. **Bez zielonego G3 i G4 nie ma commitu.**
6. Scal zgłoszone terminy do `GLOSARIUSZ.md`. Gdy nowy termin koliduje z
   istniejącym, zostaje istniejący. Wyjątek: oczywisty błąd. Wtedy popraw
   glosariusz i uruchom `glosariusz_lint.py` na przetłumaczonych plikach.
7. Ustaw status `gotowe`. Zrób commit z jawnymi ścieżkami:
   `Translate chapter N into Polish`.
8. **CI co 2–3 rozdziały:**
   - `git push origin main`;
   - pobierz id runu:
     `gh run list --workflow pages.yml --commit $(git rev-parse HEAD) --json databaseId -q '.[0].databaseId'`.
     Jeśli wynik jest pusty, ponów przy kolejnym kroku pętli; nie używaj `sleep`
     na pierwszym planie;
   - `gh run watch <id> --exit-status` uruchom **w tle** (run_in_background).
     Powiadomienie przyjdzie samo.
   - **Wynik:** run `cancelled` (nadpisany przez nowszy push) nie jest błędem.
     Run `failure` blokuje kolejne pushe do czasu naprawy.

Alternatywa: jeśli prompt startowy zawiera „użyj workflow”, pętlę z Fazy 3 można
zrealizować narzędziem Workflow. Zasady i bramki zostają te same.

---

## 5. Fazy

### Faza 0: infrastruktura

0. Utwórz `tlumaczenie/POSTEP.md` z listą kroków F0–F5 (sekcja 4.2).
1. **Narzędzia:** `rustc --version` (1.90; `rustup default` też 1.90),
   `mdbook --version` (0.5.2), `mdbook-quiz --version`. Jeśli czegoś brakuje,
   przerwij i podaj użytkownikowi komendy z 0.1.
2. **Tag bazowy:** `git tag pl-base 88250e03` (stan upstream) i
   `git push origin pl-base`.
3. **JS i build bazowy:**
   - `(cd js-extensions && pnpm init-repo)`, koniecznie w subshellu;
   - `git checkout -- js-extensions/pnpm-lock.yaml`;
   - `MDBOOK_PREPROCESSOR__AQUASCOPE__OPTIONAL=true mdbook build -d tmp/book-base`.
     Jeśli zawiedzie mdbook-quiz, zastosuj fallback z R2: najpierw napisz
     `przelot.py` (sekcja 8).
4. **Łatka preprocesorów (D9):**
   - `note/mod.rs`: warunek `starts_with("Note: ") || starts_with("Uwaga: ")`,
     plus test dla `Uwaga:`;
   - `listing/mod.rs`: `Filename:` → `Plik:`, plus aktualizacja 3 oczekiwań w
     `listing/tests.rs`;
   - `(cd packages/mdbook-trpl && cargo test)`: wszystko zielone.
5. **Przypięcie kotwic (D3):** napisz i uruchom `przypnij_kotwice.py` (sekcja 8).
   **Bramka G0:**
   - zapisano tyle pinów, ile jest nagłówków (590 w `88250e03`); pominięto 0
     plików;
   - przebuduj do `tmp/book-pinned`. Dla każdego pliku lista id nagłówków w
     `<main>` jest identyczna z `tmp/book-base`.
   Jeśli G0 nie przechodzi: `git checkout -- src` i ponów w trybie
   `--tryb=a-id`. Jeśli oba tryby zawodzą, przerwij (7.3).
6. **Commit i tag źródła:** commit z jawnymi ścieżkami (`src`,
   `packages/mdbook-trpl`) `Pin heading anchors and localize trpl labels`, potem
   `git tag pl-source` i `git push origin main pl-source`. **`pl-source` to
   angielskie źródło z przypiętymi kotwicami. Wszystkie bramki porównują do
   niego.**
7. **Skrypty i autotesty** (`tlumaczenie/narzedzia/`, sekcja 8): `sprawdz.py`,
   `sprawdz_linki.py`, `glosariusz_lint.py`, `postep.py`, a także `przelot.py`,
   jeśli nie powstał wcześniej.
   - **Autotesty** (`tlumaczenie/narzedzia/testy/`, uruchamiane jednym poleceniem):
     - `sprawdz.py --ref pl-source` na nietkniętych plikach: zero błędów;
     - `sprawdz.py --orig <plik EN> <zepsuta kopia>` na kopiach w `tmp/` wykrywa
       każde z uszkodzeń: zmieniony blok kodu, zmieniony kod inline, usunięty
       `{#id}`, zepsuty link referencyjny, zmieniony `@Perm`, zmienione `id`
       quizu, zmieniony `multipart`, usunięty `<a id>`;
     - `glosariusz_lint.py` na własnym glosariuszu testowym (fixture) znajduje
       zakazany wariant i respektuje wyjątek.
8. **Baseline linków:**
   `sprawdz_linki.py tmp/book-base --zapisz-baseline` zapisuje do
   `tlumaczenie/narzedzia/linki-baseline.txt` linki zepsute już w oryginale.
9. **`CLAUDE.md`:** dodaj sekcję „Polish translation” (po angielsku):
   - odnośnik do `tlumaczenie/`;
   - D2, D3, D8 i D11 (w tym brak stopek AI);
   - zakaz gita u subagentów;
   - `KONWENCJE.md` ma pierwszeństwo przed `style-guide.md` i regułą Title Case;
   - **nie synchronizujemy `nostarch/book.toml`**, mimo komentarza w `book.toml`.
10. Commit `Add translation tooling`, push, zielony CI.

**Warunki wyjścia:** G0, `cargo test` i autotesty zielone, CI zielone.

### Faza 1: konwencje, glosariusz, postęp

1. Utwórz `tlumaczenie/KONWENCJE.md` z sekcji 9.1.
2. Utwórz `tlumaczenie/GLOSARIUSZ.md` z sekcji 9.2.
3. Utwórz `tlumaczenie/narzedzia/wyjatki.toml` z wpisami dla `experiment-intro.md`
   i `title-page.md` (dozwolone dodatkowe linki i blok notki z D12).
4. `postep.py --init` dopisuje do `POSTEP.md` tabelę 120 plików w kolejności
   `SUMMARY.md`, ze słowami i przypisanymi quizami.
5. `glosariusz_lint.py` na prawdziwym glosariuszu: skrypt się parsuje i działa.
6. Commit `Add Polish translation conventions and glossary`.

### Faza 2: pilot

1. Paczka: `ch01-00..03` (4 pliki, 3 quizy, notatki, listingi) oraz
   `ch04-01-what-is-ownership.md` (aquascope, `@Perm`, quizy Tracing, przypisy).
2. Pełna ścieżka z 4.4, kroki 2–7.
3. **Autoreview pilota przez orkiestratora:**
   - przeczytaj w całości `ch01-01` i `ch04-01` oraz ich quizy;
   - oceń naturalność (kalki), spójność terminów, D4–D7 i działanie reguł
     glosariusza;
   - popraw `KONWENCJE.md` i `GLOSARIUSZ.md` (to ostatni moment na zmianę
     propozycji oznaczonych „?”) i nanieś zmiany na pilota.
4. Push i weryfikacja wdrożonej strony. `curl` z parametrem `?v=<sha>` i do 3 prób,
   bo CDN Pages może podać starą wersję:
   - `ch01-01-installation.html` zawiera `<section class="note"` z „Uwaga:”;
   - `ch04-01-what-is-ownership.html` zawiera elementy aquascope i quizu.
5. Jeśli prompt startowy kazał zatrzymać się po pilocie, zakończ podsumowaniem i
   linkiem do strony.

### Faza 3: tłumaczenie właściwe

Pętla 4.4 po kolejnych paczkach:
1. Strony otwierające: `experiment-intro.md`, `title-page.md`, `foreword.md`,
   `ch00-00-introduction.md`, `end-of-experiment.md`.
   - Notkę z D12 dodaje orkiestrator w Fazie 4, nie tłumacz.
   - W `title-page.md` tłumacz przepisuje zdanie o tym, że wersja eksperymentalna
     jest dostępna tylko po angielsku: informuje, że to polskie tłumaczenie tej
     wersji.
2. Rozdziały 2, 3, reszta 4 (`ch04-00`, `ch04-02..05`), potem 5 … 21 po kolei.
3. Dodatki (`appendix-*`, 8 plików: dwie fale tłumaczy).

Odwołania do tytułów sekcji z innych rozdziałów tłumacz naturalnie. Ujednolica je
Faza 5.

### Faza 4: elementy całej książki

1. `src/SUMMARY.md`: tytuły w menu zgodne z przetłumaczonymi H1 plików.
   `postep.py --summary` wypisuje pary (tytuł SUMMARY, H1). Tytuły, które w
   oryginale różnią się od H1, tłumacz osobno.
2. `book.toml`: `title = "Język programowania Rust"`, `language = "pl"`.
   Nadpisanie `git-repository-url` i `site-url` zostaje.
3. `ferris.js`: przetłumacz 3 podpowiedzi (`title`), zgodnie z tabelą Ferrisa w
   `ch00-00`.
4. **Notka z D12** na górze `experiment-intro.md` i `title-page.md`, po polsku:
   nieoficjalne tłumaczenie, link do oryginału Brown i do rust-lang/book, licencja
   MIT/Apache-2.0. Sekcja na górze `README.md` po angielsku. Sprawdź, że
   `sprawdz.py` przechodzi dzięki `wyjatki.toml`.
5. Commit `Translate book chrome and add translation notice`.

### Faza 5: przegląd globalny i odbiór

1. `glosariusz_lint.py` na całej książce. Każde trafienie poprawiasz albo, jeśli
   jest uzasadnione, wpisujesz do `wyjatki.toml` z uzasadnieniem. Po tym kroku:
   zero trafień spoza wyjątków.
2. **Spójność odwołań:** `sprawdz_linki.py tmp/book-pl --raport-tekstow` wypisuje
   pary (tekst linku, tytuł docelowego nagłówka). Orkiestrator dzieli raport
   między recenzentów (najwyżej 6 naraz, po zakresie rozdziałów). Ujednolicają
   cytowane tytuły sekcji z nagłówkami.
3. **Nieprzetłumaczone:** zbiorczy raport G5 dla całej książki. Każde trafienie
   jest przetłumaczone albo uzasadnione.
4. Pełny build (G3), linki (G4: nic nowego względem baseline), `sprawdz.py` na
   wszystkich plikach: zero błędów.
5. Opcjonalnie:
   `(cd packages/trpl && cargo build) && mdbook test --library-path packages/trpl/target/debug/deps`.
6. Push, zielony CI, `curl` z `?v=<sha>`: `lang="pl"`, polski tytuł; 3 losowe
   rozdziały renderują notatki, listingi i quizy.
7. Aktualizacja `CLAUDE.md` (stan: przetłumaczone) i commit końcowy.
8. **Raport końcowy dla użytkownika:** liczby, nierozstrzygnięte wątpliwości
   terminologiczne, lista wyjątków z uzasadnieniem, link do strony.

### Faza 6: utrzymanie (poza autonomicznym przebiegiem)

Synchronizacja ze zmianami w oryginale Brown:
1. `git fetch upstream`, potem `git diff pl-base upstream/main --stat`.
2. `git merge --no-commit upstream/main`, potem
   `git checkout HEAD -- src quizzes`. Bez tego merge po cichu wplata angielskie
   zdania obok identycznych linii (kod, dyrektywy) w polskie pliki. Nowe pliki z
   upstream zostają (do przetłumaczenia).
3. Dla przetłumaczonych plików `git diff pl-base upstream/main -- src quizzes`
   to lista angielskich zmian. Przetłumacz i nanieś je ręcznie. Do nowych
   nagłówków dopisz `{#id}`, potem uruchom bramki.
4. Jeśli merge przywrócił `.github/workflows/main.yml`, usuń go.
5. Zakończ merge commitem. Potem `git tag -f pl-base upstream/main` i
   `git push -f origin pl-base`. Odtwórz `pl-source`: `przypnij_kotwice.py` na
   wersji upstream w osobnym worktree, commit tam, `git tag -f pl-source` na tym
   commicie.

---

## 6. Szablony promptów subagentów

### 6.1. Tłumacz

```
Tłumaczysz na polski część książki "The Rust Programming Language" (wersja Brown)
w repo /Users/marcinlubowicz/private-projects/rust-book.

Twoje pliki: {PLIK_MD} oraz quizy: {LISTA_QUIZÓW lub "brak"}.
{Jeśli wznowienie: "Plik może być częściowo przetłumaczony; dokończ go."}

1. Przeczytaj tlumaczenie/KONWENCJE.md i tlumaczenie/GLOSARIUSZ.md. Obowiązują
   bezwzględnie i mają pierwszeństwo przed style-guide.md i CLAUDE.md.
2. Przetłumacz pliki w miejscu (Edit/Write). Oryginał: `git show pl-source:<ścieżka>`.
3. Nie używaj gita poza `git show`. Nie edytuj innych plików (zwłaszcza
   GLOSARIUSZ.md, POSTEP.md, SUMMARY.md, plików innych rozdziałów).
4. Na koniec: python3 tlumaczenie/narzedzia/sprawdz.py {PLIKI}
   Poprawiaj, aż nie ma BŁĘDÓW. OSTRZEŻENIA przejrzyj: przetłumacz albo uzasadnij.

Raport końcowy (dokładnie ten format):
STATUS: ok | problemy
NOWE_TERMINY: tabela | EN | PL | uzasadnienie | (tylko terminy spoza glosariusza)
WĄTPLIWOŚCI: lista (miejsce, problem, przyjęte rozwiązanie)
OSTRZEŻENIA: liczba i uzasadnienia pozostawionych
```

### 6.2. Recenzent

```
Jesteś recenzentem polskiego tłumaczenia części książki o Rust w repo
/Users/marcinlubowicz/private-projects/rust-book. Pliki: {LISTA (.md i quizy)}.
Oryginał każdego pliku: `git show pl-source:<ścieżka>`.

Przeczytaj tlumaczenie/KONWENCJE.md i tlumaczenie/GLOSARIUSZ.md. Porównaj EN z PL
akapit po akapicie i sprawdź:
1. Wierność: pominięcia, dopiski, błędy merytoryczne (odwrócony sens, zła liczba,
   pomylone pojęcia).
2. Terminologię wg glosariusza; regułę pierwszego wystąpienia (D4); brak objaśnień
   w nagłówkach.
3. Naturalność polszczyzny: kalki, szyk, zbyt dosłowne idiomy.
4. Spójność w obrębie plików (te same pojęcia tak samo).
5. Quizy: poprawna odpowiedź nadal jednoznacznie poprawna, dystraktory nadal
   błędne i wzajemnie różne; `context` i `multipart` wyjaśniają to samo co
   oryginał.
6. Notatki: `> Uwaga: ` w tej samej formie co `> Note: ` w oryginale (pierwsza
   linia nie złamana, bez dodatkowej kursywy lub pogrubienia).
Poprawki nanoś bezpośrednio. Nie używaj gita poza `git show`.
Na koniec: python3 tlumaczenie/narzedzia/sprawdz.py {PLIKI} bez BŁĘDÓW.

Raport: POPRAWKI (liczba wg kategorii 1–6 + 3 najpoważniejsze przykłady),
NOWE_TERMINY (jak u tłumacza), WĄTPLIWOŚCI.
```

---

## 7. Bramki jakości, ryzyka, kiedy przerwać

### 7.1. Bramki

| # | Co sprawdza | Narzędzie | Typ |
|---|---|---|---|
| G0 | 590 pinów, 0 pominiętych plików, id w `<main>` bez zmian | build + porównanie | twarda, jednorazowa |
| G1 | Szkielet i niezmienniki `.md` zgodne z `pl-source` | `sprawdz.py` | twarda |
| G2 | Quiz poprawny, pola z D8 i kod niezmienione | `sprawdz.py` | twarda |
| G3 | Lokalny build bez błędów, w tym walidacja quizów | `mdbook build` | twarda |
| G4 | Brak nowych zepsutych kotwic względem baseline | `sprawdz_linki.py` | twarda |
| G5 | Fragmenty prawdopodobnie nieprzetłumaczone | `sprawdz.py` (ostrzeżenia) | miękka; rozstrzyga recenzent |
| G6 | Zakazane warianty terminów | `glosariusz_lint.py` | miękka; w F5 każde trafienie poprawione lub w `wyjatki.toml` |
| G7 | Przegląd semantyczny | recenzent (6.2) | obowiązkowa |
| G8 | Build i deploy CI | GitHub Actions | twarda przed kolejnym pushem |

### 7.2. Ryzyka

| Ryzyko | Mitygacja |
|---|---|
| `{#id}` gubione w pipeline (R1) | G0 i fallback `<a id>` |
| Zmieniony kod, kod inline lub `@Perm` (aquascope lokalnie wyłączony, więc wyszłoby dopiero w CI) | G1/G2: identyczność bloków, multizbiór kodu inline i `@Perm` |
| Zepsuty TOML lub `multipart` | G2 (`tomllib`, klucze) + walidacja mdbook-quiz w G3 i CI |
| Tłumaczenie zmienia poprawność odpowiedzi w quizie | punkt 5 recenzenta |
| Notatka traci styl („Uwaga” złamana lub sformatowana) | G1: liczba `> Uwaga: ` = liczba `> Note: `; punkt 6 recenzenta |
| Złamana linia `<Listing ...>` psuje build | KONWENCJE: bez zawijania; G1 (szkielet) i G3 |
| Dryf terminologii | glosariusz, scalanie tylko przez orkiestratora, G6, Faza 5 |
| Kalki i „angielska” polszczyzna | KONWENCJE (styl), recenzent pkt 3, autoreview pilota |
| Przepełnienie kontekstu orkiestratora | orkiestrator nie czyta rozdziałów; `POSTEP.md` od F0; sekcje 0.3 i 4.3 |
| Dwóch agentów na jednym pliku | kolumna `agent` + reguła wznowienia 4.3 |
| Konflikty przy pracy równoległej | jeden plik = jeden agent; pliki wspólne tylko u orkiestratora |
| Przypadkowy commit `pnpm-lock.yaml` lub `dist/` | D11: jawne ścieżki, przywrócenie lockfile w F0.3 |
| Zmiany w upstream w trakcie | baza przypięta tagiem `pl-base`; synchronizacja w Fazie 6 |
| Długi CI, nakładające się runy, cache CDN | push co 2–3 rozdziały; `cancelled` ≠ błąd; `curl ?v=<sha>` z ponowieniem |

### 7.3. Kiedy przerwać i zapytać użytkownika

- brakuje narzędzi z 0.1 albo instalacja wymaga uprawnień;
- G0 nie przechodzi w żadnym trybie;
- CI pada dwa razy z tego samego powodu, a lokalny build przechodzi;
- konieczna byłaby zmiana którejś decyzji D1–D12;
- plik nie przechodzi `sprawdz.py` po 2 poprawkach agenta i własnej próbie
  orkiestratora.

W pozostałych przypadkach orkiestrator decyduje sam i zapisuje decyzję w raporcie
końcowym.

---

## 8. Specyfikacja skryptów (`tlumaczenie/narzedzia/`)

Wszystkie skrypty: Python 3.12, tylko `tomllib`, `markdown_it`, `bs4` i biblioteka
standardowa. Kod wyjścia różny od 0 oznacza błąd twardy.

- **`przypnij_kotwice.py [--tryb=attr|a-id] [--book tmp/book-base]`:**
  - dla każdego `src/*.md` bez `SUMMARY.md` wyciąga nagłówki ATX poza blokami
    kodu, także w pierwszej linii cytatu (`> ### ...`);
  - z `<main>` w `<book>/<plik>.html` pobiera id nagłówków `h1`–`h6` w kolejności
    (selektor `main :is(h1,h2,h3,h4,h5,h6)[id]`);
  - liczba się nie zgadza: zgłasza plik i go pomija (G0 wymaga 0 pominięć);
  - tryb `attr` dopisuje ` {#id}`, tryb `a-id` wstawia `<a id="id"></a>` i pustą
    linię nad nagłówkiem;
  - na końcu wypisuje liczbę pinów i pominiętych plików.
- **`sprawdz.py [--ref REV | --orig PLIK] <pliki...>`:** porównuje z
  `git show REV:<ścieżka>` (domyślnie `pl-source`) albo z jawnie podanym
  oryginałem. Stosuje `wyjatki.toml`. Wynik: BŁĘDY (exit ≠ 0) i OSTRZEŻENIA.
  - **G1 dla `.md`**, uporządkowany szkielet identyczny z oryginałem:
    - nagłówek: poziom + id;
    - blok kodu: info string + treść;
    - dyrektywa `{{#...}}`;
    - otwarcie i zamknięcie `<Listing>` z atrybutami poza `caption`;
    - początek cytatu i tabeli; liczba wierszy i kolumn tabel;
    - blok `<pre>...</pre>` dosłownie.
  - **G1, multizbiory identyczne z oryginałem:**
    - docelowe URL-e linków po rozwiązaniu referencji;
    - `src` obrazków;
    - atrybuty `id\s*=\s*"..."`;
    - znaczniki `@Perm(\[[^\]]*\])?\{[^}]*\}`;
    - komentarze HTML;
    - zawartość `<code>...</code>` w HTML;
    - etykiety przypisów `[^...]` (szukane regexem, bo markdown_it w trybie
      commonmark ich nie widzi);
    - znaczniki inline HTML (nazwa i atrybuty poza `alt`/`title`).
  - **G1, liczniki:**
    - liczba `^> Uwaga: ` = liczba `^> Note: ` w oryginale;
    - liczba `<span class="filename">Plik: ` = liczba `Filename: ` w oryginale.
  - **G1, kod inline:**
    - każdy span kodu inline w PL musi istnieć w EN (inaczej BŁĄD);
    - różnica liczności to OSTRZEŻENIE.
  - **G2 dla `.toml`:**
    - `tomllib` parsuje plik;
    - ta sama liczba i kolejność pytań;
    - pola z D8 identyczne;
    - te same klucze tabeli `[multipart]`;
    - w każdym polu tekstowym (także `multipart.*`): identyczne bloki kodu,
      multizbiór URL-i i `@Perm`, kod inline jak w G1;
    - ta sama liczba dystraktorów; dystraktory i odpowiedź wzajemnie różne;
    - ten sam typ `answer.answer` (napis/lista) i długość listy;
    - opcje złożone wyłącznie z kodu: identyczne.
  - **G5 (ostrzeżenia), dla `.md` i pól tekstowych `.toml`:**
    - linie prozy identyczne z oryginałem, z pominięciem `<pre>`, kodu, wierszy
      tabel z samym kodem, `</Listing>`, `[etykieta]: url` i `{{#...}}`;
    - akapity z dużym udziałem angielskich słów funkcyjnych (the, and, of, is,
      that, with, this, which, are, you; **bez** „to”, które jest polskim
      słowem).
- **`sprawdz_linki.py <katalog_book> [--zapisz-baseline] [--raport-tekstow]`:**
  - dla każdego `href` do lokalnego `.html` z `#fragment` (oraz samego
    `#fragment`) sprawdza, czy plik docelowy ma taki `id`;
  - porównuje wynik z `linki-baseline.txt`; zgłasza tylko nowe zepsute linki;
  - `--raport-tekstow` wypisuje pary (tekst linku, tekst docelowego nagłówka).
- **`glosariusz_lint.py [pliki...]`:**
  - kolumna „Zakazane” w `GLOSARIUSZ.md` zawiera **regexy** (Python,
    bez rozróżniania wielkości liter), dopasowywane tylko w prozie, poza kodem;
  - przed kompilacją regexu zdejmij otaczające backticki i zamień `\|` na `|`
    (escape wymagany w komórce tabeli Markdown);
  - wyjątki per plik bierze z `wyjatki.toml`;
  - wypisuje trafienia z kontekstem.
- **`postep.py --init | --summary`:**
  - `--init` dopisuje do `POSTEP.md` tabelę plików w kolejności `SUMMARY.md`, ze
    słowami EN i quizami z `{{#quiz}}`;
  - `--summary` wypisuje pary (tytuł w SUMMARY, H1 pliku).
- **`przelot.py`** (fallback R2): przelotowy preprocesor mdBook.
  - wywołany z argumentem `supports <renderer>` kończy się kodem 0;
  - w przeciwnym razie czyta ze stdin `[context, book]` i wypisuje `book` bez
    zmian.
- **`wyjatki.toml`:** sekcja na plik:
  - `dodatkowe_urle`: lista URL-i;
  - `dodatkowe_bloki`: liczba dodatkowych elementów szkieletu, np. cytat z notką;
  - `glosariusz`: lista zaakceptowanych trafień G6, każde z uzasadnieniem.

---

## 9. Treść startowa konwencji i glosariusza

### 9.1. KONWENCJE (przenieść do `tlumaczenie/KONWENCJE.md`)

**Pierwszeństwo:** te zasady wygrywają z `style-guide.md` i `CLAUDE.md`, np. w
kwestii Title Case i zawijania.

**Bez zmian (bajt po bajcie):**
- bloki kodu (w tym `aquascope`) i dyrektywy `{{#...}}`;
- **kod inline** i znaczniki `@Perm...{...}`;
- `{#id}` w nagłówkach;
- komentarze HTML (w tym `<!-- ignore -->` i „Old headings”) oraz linie
  `<a id="..."></a>`;
- `<pre>`/`<code>` w HTML;
- adresy linków i etykiety referencji (`[tekst][etykieta]`, `[etykieta]: url`);
- `src` obrazków i atrybuty `<Listing>` poza `caption`;
- etykiety przypisów `[^...]`;
- pola quizów z D8.

**Tłumaczymy:**
- prozę i nagłówki (z zachowaniem `{#id}`, bez objaśnień terminów);
- tekst linków;
- `caption` listingów, `alt` obrazków, komórki tabel (poza kodem);
- treść notatek i przypisów;
- podpisy: „Table” → „Tabela”, „Figure” → „Rysunek”, „Listing” zostaje;
- pola quizów `prompt.prompt`, `prompt.distractors`, `answer.answer`
  (MultipleChoice, z wyjątkiem opcji z samego kodu), `context` i tabele
  `[multipart]`.

**Linki:** link skrótowy `[etykieta]` po przetłumaczeniu tekstu zamień na
`[polski tekst][etykieta]`. `<!-- ignore -->` zostaje bezpośrednio za linkiem. Nie
dodawaj nowych linków.

**Terminologia:**
- zgodnie z `GLOSARIUSZ.md` i D4;
- pierwsze wystąpienie w prozie pliku: termin tłumaczony „własność
  (*ownership*)”, termin zostawiony po angielsku „*crate* (objaśnienie)”;
- kolumna „Pierwsze wystąpienie” podaje gotową formę;
- termin spoza glosariusza: przyjmij rozwiązanie najbliższe polskiej praktyce
  programistycznej i zgłoś go w raporcie;
- w quizach wystarczy sam polski termin.

**Styl:**
- tłumacz sens, nie słowa; dziel i łącz zdania, jeśli tak jest naturalniej;
- unikaj zbędnej strony biernej i kalk („robi sens”, „aplikować” w znaczeniu
  „stosować”, „w tym przypadku” na każde „here”);
- „you” → 2. os. l.poj. bez zaimka; „we” → „my” w formie czasownika;
- nie dodawaj własnych wyjaśnień. Wyjątek: nieprzekładalna gra słów, wtedy
  „(przyp. tłum.: …)” w jednym zdaniu;
- elementy UI widżetów (quiz, aquascope, mdBook) cytuj po angielsku w
  cudzysłowie, np. przycisk „Submit”;
- litery uprawnień aquascope (R, W, O, F) zostają; przy pierwszym wystąpieniu w
  pliku: „R (*read*, odczyt)”, „W (*write*, zapis)”, „O (*own*, własność)”,
  „F (*flow*, przepływ)”;
- odwołania: „rozdział 4”, „listing 4-1” (odmiana: listingu, listingiem),
  „dodatek A”;
- odmiana nazw: Rust, Rusta, Rustowi, w Ruście; Cargo i rustup nieodmienne;
  Ferris, Ferrisa;
- typografia (D7): „…”, ‚…’, „ – ”, nagłówki zdaniowe, apostrof w odmianie ’
  (crate’a).

**Łamanie linii:**
- prozę zawijaj w okolicach 80 znaków;
- **nigdy** nie łam: linii `<Listing ...>` (złamana przestaje być blokiem HTML i
  psuje build), nagłówków, wierszy tabel, definicji `[etykieta]: url`, pierwszej
  linii notatki (`> Uwaga: ...`), linków i kodu inline.

**Notatki i etykiety:**
- `> Note: ` → `> Uwaga: ` dokładnie w tej formie;
- inne warianty (`> **Note:**`, `*Note:*`, `_Note_:`) mają zachować formatowanie,
  zmienia się tylko słowo;
- cytat zaczyna się tak samo jak w oryginale; nie przestawiaj kodu na początek
  cytatu;
- `<span class="filename">Filename: X</span>` →
  `<span class="filename">Plik: X</span>`.

**Atrybuty HTML:** w `caption="..."` nie używaj prostego `"`, a w `caption='...'`
prostego `'`. Polskie „” i ’ są bezpieczne.

**Quizy (TOML):**
- zachowaj format stringów (`"""` wielolinijkowe);
- nie zmieniaj kolejności pól ani pytań;
- w `"..."` nie używaj prostego `"`;
- opcje odpowiedzi muszą pozostać wzajemnie różne.

### 9.2. GLOSARIUSZ (start, przenieść do `tlumaczenie/GLOSARIUSZ.md`)

Kolumny: **EN | PL | Pierwsze wystąpienie | Zakazane (regex) | Uwagi**. Znak „?”
oznacza propozycję do potwierdzenia w pilocie (Faza 2); później już się jej nie
zmienia. Regexy dopasowuje `glosariusz_lint.py`. Słowa wieloznaczne celowo nie są
zakazane (np. „zakres”, „zamknięcie”, „odwołanie”, „zmienny”); pilnuje ich
recenzent.

| EN | PL | Pierwsze wystąpienie | Zakazane (regex) | Uwagi |
|---|---|---|---|---|
| ownership | własność | własność (*ownership*) | `\bposiadani\w*` | owner → właściciel |
| borrowing / to borrow | pożyczanie / pożyczyć | pożyczanie (*borrowing*) | `\bzapożycz\w*` | a borrow → pożyczenie |
| borrow checker | borrow checker | *borrow checker* (mechanizm sprawdzania pożyczeń) | `\bsprawdzacz\w*` | odmiana: borrow checkera |
| reference | referencja | referencja (*reference*) | `\bodnośnik\w*` | |
| mutable / immutable | mutowalny / niemutowalny | mutowalny (*mutable*) | `\bmodyfikowaln\w*` | mutability → mutowalność; nie „zmienny” (koliduje ze „zmienna”) |
| variable | zmienna | — | | |
| shadowing | przesłanianie | przesłanianie (*shadowing*) | `\bcieniowani\w*` | |
| scope | zasięg | zasięg (*scope*) | | „zakres” zarezerwowany dla *range* |
| range | zakres | — | | |
| move | przeniesienie / przenieść | przeniesienie (*move*) | | |
| copy / clone | kopiowanie / klonowanie | — | | traity `Copy`/`Clone` jako kod |
| drop | zwolnienie / zwolnić | zwolnienie (*drop*) | `\bupuszcz\w*` | „wartość zostaje zwolniona” |
| stack / heap | stos / sterta | stos (*stack*), sterta (*heap*) | `\bkop(iec\|c\w+)\b` | |
| pointer | wskaźnik | — | | |
| smart pointer | inteligentny wskaźnik | inteligentny wskaźnik (*smart pointer*) | | |
| raw pointer | surowy wskaźnik | surowy wskaźnik (*raw pointer*) | | |
| dangling reference | wisząca referencja | wisząca referencja (*dangling reference*) | | |
| dereference | dereferencja | dereferencja (*dereference*) | `\bwyłuskani\w*` | ? czasownik: „wykonać dereferencję” |
| deref coercion | deref coercion | *deref coercion* (automatyczna konwersja przez dereferencję) | | |
| undefined behavior | niezdefiniowane zachowanie | niezdefiniowane zachowanie (*undefined behavior*) | | |
| permission (Brown) | uprawnienie | uprawnienie (*permission*) | | litery R/W/O/F zostają |
| lifetime | czas życia | czas życia (*lifetime*) | `\bżywotnoś\w*` | lifetime elision → pomijanie czasów życia (*lifetime elision*) |
| slice | wycinek | wycinek (*slice*) | `\bplast(er\|r)\w*` | ? string slice → wycinek łańcucha (*string slice*) |
| string | łańcuch znaków | łańcuch znaków (*string*) | | skrótowo „łańcuch”; typ `String` jako kod |
| struct | struktura | struktura (*struct*) | | |
| enum | enum | *enum* (typ wyliczeniowy) | | ? odmiana: enuma, enumy |
| variant / field | wariant / pole | — | | |
| method | metoda | — | | |
| associated function | funkcja powiązana | funkcja powiązana (*associated function*) | `\bstowarzyszon\w*` | |
| associated type | typ powiązany | typ powiązany (*associated type*) | | |
| trait | trait | *trait* (cecha typu, zbliżona do interfejsu) | | ? odmiana: traitu, traity; alternatywa „cecha” |
| trait object | obiekt traitu | obiekt traitu (*trait object*) | | |
| trait bound | ograniczenie traitu | ograniczenie traitu (*trait bound*) | | |
| generics | typy generyczne | typy generyczne (*generics*) | `\btyp\w* ogóln\w*` | type parameter → parametr typu |
| pattern / pattern matching | wzorzec / dopasowywanie wzorców | dopasowywanie wzorców (*pattern matching*) | | match arm → ramię (*arm*) |
| refutable / irrefutable | odrzucalny / nieodrzucalny | wzorzec odrzucalny (*refutable*) | | ? |
| closure | domknięcie | domknięcie (*closure*) | | nie „zamknięcie” (zarezerwowane m.in. dla zamykania kanału) |
| iterator / iterator adapter | iterator / adapter iteratora | adapter iteratora (*iterator adapter*) | | consuming adapter → adapter konsumujący |
| crate | crate | *crate* (jednostka kompilacji w Ruście) | `\bskrzyn\w*` | ? odmiana: crate’a, crate’y, crate’ów |
| package | pakiet | pakiet (*package*) | | |
| module / module tree | moduł / drzewo modułów | — | | |
| path | ścieżka | — | | |
| workspace | przestrzeń robocza | przestrzeń robocza (*workspace*) | | |
| dependency | zależność | — | | |
| release profile | profil wydania | profil wydania (*release profile*) | | |
| panic | panika / panikować | panika (*panic*) | | „program panikuje” |
| recoverable / unrecoverable error | błąd odwracalny / nieodwracalny | błąd odwracalny (*recoverable error*) | | ? |
| error propagation | propagowanie błędów | — | | |
| unit / integration test | test jednostkowy / integracyjny | — | | assertion → asercja |
| thread | wątek | — | | |
| concurrency / parallelism | współbieżność / równoległość | współbieżność (*concurrency*) | | |
| message passing | przekazywanie komunikatów | przekazywanie komunikatów (*message passing*) | | channel → kanał |
| mutex / lock | mutex / blokada | — | | „uzyskać blokadę” |
| deadlock | zakleszczenie | zakleszczenie (*deadlock*) | | |
| race condition / data race | wyścig / wyścig danych | sytuacja wyścigu (*race condition*) | | |
| reference counting | zliczanie referencji | zliczanie referencji (*reference counting*) | | |
| interior mutability | wewnętrzna mutowalność | wewnętrzna mutowalność (*interior mutability*) | | |
| future | future | *future* (wartość, która będzie gotowa później) | | ? odmiana: future’a |
| async runtime | środowisko uruchomieniowe | środowisko uruchomieniowe (*runtime*) | | |
| stream | strumień | strumień (*stream*) | | |
| graceful shutdown | łagodne zamykanie | łagodne zamykanie (*graceful shutdown*) | | ? rozdział 21 |
| macro | makro | — | | l.mn. makra; deklaratywne / proceduralne |
| unsafe Rust | niebezpieczny Rust | niebezpieczny Rust (*unsafe Rust*) | | słowo kluczowe `unsafe` jako kod |
| statement / expression | instrukcja / wyrażenie | instrukcja (*statement*), wyrażenie (*expression*) | | |
| tuple / array / vector | krotka / tablica / wektor | krotka (*tuple*) | | |
| hash map | mapa haszująca | mapa haszująca (*hash map*) | `\btablic\w* mieszając\w*` | ? |
| type inference | wnioskowanie typów | wnioskowanie typów (*type inference*) | | type annotation → adnotacja typu |
| zero-cost abstraction | abstrakcja o zerowym koszcie | abstrakcja o zerowym koszcie (*zero-cost abstraction*) | | |
| toolchain | zestaw narzędzi | zestaw narzędzi (*toolchain*) | | |
| standard library / prelude | biblioteka standardowa / prelude | *prelude* (zestaw elementów importowanych automatycznie) | | |
| attribute / derive | atrybut / derive | — | | `#[derive]` jako kod |
| Ownership Inventory (Brown) | Inwentaryzacja własności | — | | ? tytuł sekcji quizów |

---

## 10. Definicja ukończenia

- [ ] wszystkie pozycje w `POSTEP.md` (kroki i pliki) zamknięte, status `gotowe`;
- [ ] `sprawdz.py` na wszystkich `src/*.md` i `quizzes/*.toml`: zero BŁĘDÓW;
      ostrzeżenia G5 rozstrzygnięte;
- [ ] `glosariusz_lint.py`: zero trafień spoza `wyjatki.toml`;
- [ ] lokalny build i linki (G3, G4) zielone; brak nowych zepsutych kotwic;
- [ ] CI zielone; strona https://moviss.github.io/rust-book/ ma `lang="pl"`,
      polski tytuł, notkę o tłumaczeniu na stronie startowej oraz działające
      quizy i aquascope;
- [ ] `CLAUDE.md`, `README.md`, `experiment-intro.md` i `title-page.md`
      zawierają informacje o tłumaczeniu;
- [ ] raport końcowy przekazany użytkownikowi.

---

## 11. Autoreview

Plan przeszedł dwie rundy przeglądu (2026-10-06).

**Runda 1 (autor):**
- jednolity zapis terminów zostawionych po angielsku;
- sprawdzanie URL-i w quizach (linki w quizach renderuje JS, więc G4 ich nie
  widzi);
- uprawnienie F (flow) w aquascope;
- odmiana „Rust” i „Cargo”;
- liczba jednostek tłumaczenia (120 + `SUMMARY.md`).

**Runda 2 (niezależny agent bez kontekstu rozmowy, weryfikacja na repo, scratch
build mdBook 0.5.2 i źródłach mdbook-quiz 0.5.0, aquascope 0.4.0,
pulldown-cmark-to-cmark 19).** Wynik: 0 blokerów, 8 poważnych, 12 drobnych
problemów. Wszystkie zostały wprowadzone.

| # | Waga | Problem | Poprawka |
|---|---|---|---|
| 1 | poważny | G0 mogło przejść bez przypięcia czegokolwiek: dodatkowe `h1`/`h2` poza `<main>` | selektor `<main>`; G0 wymaga 590 pinów i 0 pominięć |
| 2 | poważny | Autotesty skryptów przed utworzeniem `pl-source` i glosariusza | `pl-source` w F0.6 przed skryptami; `--ref`/`--orig`; fixture glosariusza |
| 3 | poważny | `@Perm` w prozie niechronione; błąd wyszedłby dopiero w CI | `@Perm` w „bez zmian”; multizbiór w G1/G2 |
| 4 | poważny | G1/G2 nie sprawdzały kodu inline | PL ⊆ EN = błąd; opcje kodowe identyczne |
| 5 | poważny | „Zakazane” sprzeczne z resztą glosariusza (zakres, przyszłość, rdzenie) | regexy, wyjątki w `wyjatki.toml`, G6 miękka |
| 6 | poważny | Notka o tłumaczeniu łamała G1; strona startowa to `experiment-intro.md` | `wyjatki.toml`; notka na `experiment-intro.md` i `title-page.md` |
| 7 | poważny | Wznowienie po kompaktowaniu: brak stanu w F0, ryzyko dwóch agentów na plik | `POSTEP.md` od F0.0, kolumny agent/próby, reguła 4.3, czytanie całego planu |
| 8 | poważny | Pominięte pola quizów: `[multipart]`, `answer.alternatives` | dodane do D8, 9.1 i G2 |
| 9 | drobny | Liczba pytań MultipleChoice | 141 (sprawdzone `tomllib`) |
| 10 | drobny | mdbook-quiz zawsze waliduje i kompiluje domyślnym `rustc`; fallback nie działał | `rustup default 1.90`; `przelot.py` jako fallback |
| 11 | drobny | `pnpm init-repo` brudzi lockfile i zmienia katalog roboczy | subshell, przywrócenie lockfile, jawne ścieżki w commitach |
| 12 | drobny | Notatki mogły po cichu stracić styl | liczniki w G1, reguły w 9.1, pkt 6 recenzenta |
| 13 | drobny | Brak reguł dla podpisów Table/Figure, `ferris.js` i cudzysłowów w `caption` | D9, 9.1, F4.3 |
| 14 | drobny | Zawijanie mogło złamać `<Listing>`; objaśnienia w nagłówkach | wyjątki zawijania; D4 bez objaśnień w nagłówkach |
| 15 | drobny | Luki G1: `<pre>`, przypisy, inline HTML, `id =`, kolejność elementów | uporządkowany szkielet + multizbiory |
| 16 | drobny | G5 hałaśliwe („to” jest polskim słowem) | lista bez „to”, wykluczenia, także TOML |
| 17 | drobny | Sprzeczne reguły ponowień; rozdziały ponad 6 plików; kolumna commit | ujednolicone (4.4 i 7.3); fale; recenzent na ok. 8 tys. słów |
| 18 | drobny | Mechanika CI: id runu, `cancelled`, cache CDN | 4.4 pkt 8, `curl ?v=<sha>` |
| 19 | drobny | Konflikty instrukcji (`style-guide.md`, nostarch, stopki AI, zgody) | F0.9, 4.1, prompt startowy 0.2 |
| 20 | drobny | „Fork prywatny” (jest publiczny); merge z upstream wplata angielski tekst | D1; Faza 6: `merge --no-commit` + `checkout HEAD -- src quizzes`, `push -f` tagu |

Potwierdzone przez recenzenta jako poprawne:
- R1 powinno przejść, bo pulldown-cmark-to-cmark zachowuje id w postaci
  ` { #id }`;
- `print.html` nie daje fałszywych alarmów G4;
- brak nagłówków setext i duplikatów id (poza „Ownership Inventory #1–#4”);
- wszystkie 93 quizy podpięte dokładnie raz;
- wszystkie 17 odpowiedzi ShortAnswer to kod lub liczby;
- każdy `<Listing>` mieści się w jednej linii;
- wyszukiwarka działa z `language = "pl"`.

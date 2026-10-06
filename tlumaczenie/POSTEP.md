# Postęp tłumaczenia

Stan wykonania planu z `PLAN.md`. Aktualizuje wyłącznie orkiestrator.

## Kroki

- [x] F0.1 Weryfikacja narzędzi
- [x] F0.2 Tag bazowy `pl-base`
- [x] F0.3 JS i build bazowy
- [x] F0.4 Łatka preprocesorów (D9)
- [x] F0.5 Przypięcie kotwic, bramka G0
- [x] F0.6 Commit i tag `pl-source`
- [x] F0.7 Skrypty i autotesty
- [x] F0.8 Baseline linków
- [x] F0.9 `CLAUDE.md`
- [x] F0.10 Commit narzędzi, push, CI
- [x] F1.1 `KONWENCJE.md`
- [x] F1.2 `GLOSARIUSZ.md`
- [x] F1.3 `wyjatki.toml`
- [x] F1.4 `postep.py --init`
- [x] F1.5 `glosariusz_lint.py` na glosariuszu
- [x] F1.6 Commit konwencji
- [x] F2.1 Pilot: tłumaczenie
- [x] F2.2 Pilot: przegląd, bramki
- [x] F2.3 Autoreview pilota
- [x] F2.4 Push i weryfikacja strony
- [x] F3.1 Strony otwierające
- [ ] F3.2 Rozdziały 2–21
- [ ] F3.3 Dodatki
- [ ] F4.1 `SUMMARY.md`
- [ ] F4.2 `book.toml`
- [ ] F4.3 `ferris.js`
- [ ] F4.4 Notka D12
- [ ] F4.5 Commit
- [ ] F5.1 Glosariusz na całej książce
- [ ] F5.2 Spójność odwołań
- [ ] F5.3 Raport G5
- [ ] F5.4 Pełny build, linki, `sprawdz.py`
- [ ] F5.5 `mdbook test` (opcjonalnie)
- [ ] F5.6 Push, CI, weryfikacja strony
- [ ] F5.7 `CLAUDE.md` końcowy
- [ ] F5.8 Raport końcowy

## Pliki

| plik | rozdz. | słowa EN | quizy | status | agent | próby | G5 | uwagi |
|---|---|---|---|---|---|---|---|---|
| experiment-intro.md | 0 | 550 | example-quiz | gotowe | afe257bc | 1 |  |  |
| title-page.md | 0 | 145 | — | gotowe | afe257bc | 1 |  |  |
| foreword.md | 0 | 448 | — | gotowe | afe257bc | 1 |  |  |
| ch00-00-introduction.md | 0 | 1611 | — | gotowe | afe257bc | 1 |  |  |
| ch01-00-getting-started.md | 1 | 49 | — | gotowe | a26173e7 | 1 |  |  |
| ch01-01-installation.md | 1 | 926 | ch01-01-installation | gotowe | a26173e7 | 1 |  |  |
| ch01-02-hello-world.md | 1 | 1137 | ch01-02-hello-world | gotowe | a26173e7 | 1 |  |  |
| ch01-03-hello-cargo.md | 1 | 1612 | ch01-03-hello-cargo | gotowe | a26173e7 | 1 | 1 (tytuł Hello, Cargo!) |  |
| ch02-00-guessing-game-tutorial.md | 2 | 5469 | — | gotowe | a538c911 | 1 |  |  |
| ch03-00-common-programming-concepts.md | 3 | 201 | — | gotowe | a654ea8f | 1 |  |  |
| ch03-01-variables-and-mutability.md | 3 | 1337 | ch03-01-variables-and-mutability-sec1-variables, ch03-01-variables-and-mutability-sec2-constants, ch03-01-variables-and-mutability-sec3-shadowing | gotowe | a654ea8f | 1 |  |  |
| ch03-02-data-types.md | 3 | 2535 | ch03-02-data-types-sec1-scalar, ch03-02-data-types-sec2-compound | gotowe | a654ea8f | 1 |  |  |
| ch03-03-how-functions-work.md | 3 | 1412 | ch03-03-functions-sec1-parameters, ch03-03-functions-sec2-expressions | gotowe | ab69c60f | 1 |  |  |
| ch03-04-comments.md | 3 | 167 | — | gotowe | ab69c60f | 0 |  |  |
| ch03-05-control-flow.md | 3 | 2436 | ch03-05-control-flow-sec1-if, ch03-05-control-flow-sec2-loops | gotowe | ab69c60f | 1 |  |  |
| ch04-00-understanding-ownership.md | 4 | 64 | — | gotowe | a54f221e | 0 |  |  |
| ch04-01-what-is-ownership.md | 4 | 2764 | ch04-01-ownership-sec1-stackheap, ch04-01-ownership-sec2-moves | gotowe | a172b206 | 1 |  |  |
| ch04-02-references-and-borrowing.md | 4 | 3293 | ch04-02-references-sec1-basics, ch04-02-references-sec2-perms, ch04-02-references-sec3-safety | gotowe | a54f221e | 1 | 1 (`x` scalone, uzasadnione) |  |
| ch04-03-fixing-ownership-errors.md | 4 | 2480 | ch04-03-fixing-ownership-errors-sec1-idioms, ch04-03-fixing-ownership-errors-sec2-safety | gotowe | a54f221e | 1 |  |  |
| ch04-04-slices.md | 4 | 1832 | ch04-04-slices | gotowe | a9daf518 | 1 |  |  |
| ch04-05-ownership-recap.md | 4 | 1470 | ch04-05-ownership-recap | gotowe | a9daf518 | 0 |  |  |
| ch05-00-structs.md | 5 | 135 | — | gotowe | ab2fdd3d | 1 |  |  |
| ch05-01-defining-structs.md | 5 | 2092 | ch05-01-structs | gotowe | ab2fdd3d | 1 |  |  |
| ch05-02-example-structs.md | 5 | 1578 | ch05-02-example-structs | gotowe | ab2fdd3d | 1 |  |  |
| ch05-03-method-syntax.md | 5 | 2491 | ch05-03-method-syntax-sec1, ch05-03-method-syntax-sec2 | gotowe | ab2fdd3d | 1 |  |  |
| ch06-00-enums.md | 6 | 113 | — | gotowe | ac18a18c | 1 |  |  |
| ch06-01-defining-an-enum.md | 6 | 2381 | ch06-01-defining-an-enum | gotowe | ac18a18c | 1 |  |  |
| ch06-02-match.md | 6 | 2072 | ch06-02-match | gotowe | ac18a18c | 1 | 2 (`match` jako kod, uzasadnione) |  |
| ch06-03-if-let.md | 6 | 1006 | ch06-03-if-let | gotowe | ac18a18c | 1 |  |  |
| ch06-04-inventory.md | 6 | 312 | ch06-04-inventory | gotowe | ac18a18c | 1 |  |  |
| ch07-00-managing-growing-projects-with-packages-crates-and-modules.md | 7 | 477 | — | gotowe | a854e603 | 1 |  |  |
| ch07-01-packages-and-crates.md | 7 | 589 | ch07-01-packages-and-crates | gotowe | a854e603 | 1 |  |  |
| ch07-02-defining-modules-to-control-scope-and-privacy.md | 7 | 1124 | ch07-02-modules | gotowe | a854e603 | 1 |  |  |
| ch07-03-paths-for-referring-to-an-item-in-the-module-tree.md | 7 | 2291 | ch07-03-paths-sec1, ch07-03-paths-sec2 | gotowe | a854e603 | 1 |  |  |
| ch07-04-bringing-paths-into-scope-with-the-use-keyword.md | 7 | 1826 | ch07-04-use | gotowe | a854e603 | 1 |  |  |
| ch07-05-separating-modules-into-different-files.md | 7 | 882 | ch07-05-files | gotowe | a854e603 | 1 |  |  |
| ch08-00-common-collections.md | 8 | 218 | — | gotowe | aadc4d0e | 1 |  |  |
| ch08-01-vectors.md | 8 | 2030 | ch08-01-vec-sec1, ch08-01-vec-sec2 | gotowe | aadc4d0e | 1 |  |  |
| ch08-02-strings.md | 8 | 2578 | ch08-02-string-sec1, ch08-02-string-sec2 | gotowe | aadc4d0e | 1 |  |  |
| ch08-03-hash-maps.md | 8 | 1844 | ch08-03-hashmap | gotowe | aadc4d0e | 1 |  |  |
| ch08-04-inventory.md | 8 | 34 | ch08-04-inventory | gotowe | aadc4d0e | 1 |  |  |
| ch09-00-error-handling.md | 9 | 221 | — | gotowe | aba68c9b | 1 |  |  |
| ch09-01-unrecoverable-errors-with-panic.md | 9 | 1152 | ch09-01-panic | gotowe | aba68c9b | 1 |  |  |
| ch09-02-recoverable-errors-with-result.md | 9 | 3996 | ch09-02-recoverable-errors-sec1, ch09-02-recoverable-errors-sec2 | gotowe | aba68c9b | 1 |  |  |
| ch09-03-to-panic-or-not-to-panic.md | 9 | 2213 | ch09-03-panic-or-not | gotowe | aba68c9b | 1 |  |  |
| ch10-00-generics.md | 10 | 898 | — | gotowe | a7841011 | 1 |  |  |
| ch10-01-syntax.md | 10 | 2324 | ch10-01-generics | gotowe | a7841011 | 1 |  |  |
| ch10-02-traits.md | 10 | 2577 | ch10-02-traits-sec1, ch10-02-traits-sec2 | gotowe | a7841011 | 1 |  |  |
| ch10-03-lifetime-syntax.md | 10 | 4540 | ch10-03-lifetimes-sec1, ch10-03-lifetimes-sec2 | gotowe | a03441c0 | 1 |  |  |
| ch10-04-inventory.md | 10 | 34 | ch10-04-inventory | gotowe | a03441c0 | 1 |  |  |
| ch11-00-testing.md | 11 | 340 | — | gotowe | a0133458 | 1 |  |  |
| ch11-01-writing-tests.md | 11 | 3461 | ch11-01-writing-tests | gotowe | a0133458 | 1 |  |  |
| ch11-02-running-tests.md | 11 | 1201 | ch11-02-running-tests | gotowe | a0133458 | 1 |  |  |
| ch11-03-test-organization.md | 11 | 1808 | ch11-03-test-organization | gotowe | a0133458 | 1 |  |  |
| ch12-00-an-io-project.md | 12 | 386 | — | gotowe | aaf838c8 | 1 |  |  |
| ch12-01-accepting-command-line-arguments.md | 12 | 906 | — | gotowe | aaf838c8 | 1 |  |  |
| ch12-02-reading-a-file.md | 12 | 342 | — | gotowe | aaf838c8 | 1 |  |  |
| ch12-03-improving-error-handling-and-modularity.md | 12 | 3777 | — | gotowe | aaf838c8 | 1 |  |  |
| ch12-04-testing-the-librarys-functionality.md | 12 | 1363 | — | gotowe | ad855890 | 1 |  |  |
| ch12-05-working-with-environment-variables.md | 12 | 1302 | — | gotowe | ad855890 | 1 |  |  |
| ch12-06-writing-to-stderr-instead-of-stdout.md | 12 | 639 | — | gotowe | ad855890 | 1 |  |  |
| ch13-00-functional-features.md | 13 | 191 | — | gotowe | a877a99a | 1 |  |  |
| ch13-01-closures.md | 13 | 3006 | ch13-01-closures-sec1, ch13-01-closures-sec2 | gotowe | a877a99a | 1 |  |  |
| ch13-02-iterators.md | 13 | 1473 | ch13-02-iterators | gotowe | a877a99a | 1 |  |  |
| ch13-03-improving-our-io-project.md | 13 | 1271 | — | gotowe | a877a99a | 1 |  |  |
| ch13-04-performance.md | 13 | 427 | — | gotowe | a877a99a | 1 |  |  |
| ch14-00-more-about-cargo.md | 14 | 110 | — | gotowe | a0b6c247 | 1 |  |  |
| ch14-01-release-profiles.md | 14 | 413 | ch14-01-release-profiles | gotowe | a0b6c247 | 1 |  |  |
| ch14-02-publishing-to-crates-io.md | 14 | 2926 | ch14-02-publishing-to-crates-io-sec1, ch14-02-publishing-to-crates-io-sec2 | gotowe | a0b6c247 | 1 |  |  |
| ch14-03-cargo-workspaces.md | 14 | 1574 | ch14-03-cargo-workspaces | gotowe | a0b6c247 | 1 |  |  |
| ch14-04-installing-binaries.md | 14 | 282 | — | gotowe | a0b6c247 | 1 |  |  |
| ch14-05-extending-cargo.md | 14 | 161 | — | gotowe | a0b6c247 | 1 |  |  |
| ch15-00-smart-pointers.md | 15 | 438 | — | gotowe | a10bc024 | 1 |  |  |
| ch15-01-box.md | 15 | 2097 | ch15-01-box | gotowe | a10bc024 | 1 |  |  |
| ch15-02-deref.md | 15 | 2107 | ch15-02-deref | gotowe | a10bc024 | 1 |  |  |
| ch15-03-drop.md | 15 | 1071 | ch15-03-drop | gotowe | a10bc024 | 1 |  |  |
| ch15-04-rc.md | 15 | 1416 | ch15-04-rc | gotowe | af1b9fd3 | 1 |  |  |
| ch15-05-interior-mutability.md | 15 | 2790 | ch15-05-interior-mutability | gotowe | af1b9fd3 | 1 |  |  |
| ch15-06-reference-cycles.md | 15 | 2501 | ch15-06-reference-cycles | gotowe | af1b9fd3 | 1 |  |  |
| ch16-00-concurrency.md | 16 | 451 | — | przegląd | a5977de1 | 1 |  |  |
| ch16-01-threads.md | 16 | 1657 | ch16-01-threads | przegląd | a5977de1 | 1 |  |  |
| ch16-02-message-passing.md | 16 | 1747 | ch16-02-message-passing | przegląd | a5977de1 | 1 |  |  |
| ch16-03-shared-state.md | 16 | 1957 | ch16-03-shared-state | przegląd | a5977de1 | 1 |  |  |
| ch16-04-extensible-concurrency-sync-and-send.md | 16 | 892 | ch16-04-extensible-concurrency-send-and-sync | przegląd | a5977de1 | 1 |  |  |
| ch17-00-async-await.md | 17 | 1644 | — | przetłumaczone | a38a4454 | 1 |  |  |
| ch17-01-futures-and-syntax.md | 17 | 2979 | async-01-futures-and-syntax | tłumaczenie | ab1a0d8c | 1 |  |  |
| ch17-02-concurrency-with-async.md | 17 | 2805 | async-02-concurrency-with-async | tłumaczenie | a69798ab | 1 |  |  |
| ch17-03-more-futures.md | 17 | 1473 | async-03-more-futures | tłumaczenie | ab6bd790 | 1 |  |  |
| ch17-04-streams.md | 17 | 631 | async-04-streams | tłumaczenie | a0b11b51 | 1 |  |  |
| ch17-05-traits-for-async.md | 17 | 4099 | async-05-traits-for-async | do zrobienia | | 0 | | |
| ch17-06-futures-tasks-threads.md | 17 | 873 | — | tłumaczenie | a0b11b51 | 1 |  |  |
| ch18-00-oop.md | 18 | 143 | — | do zrobienia | | 0 | | |
| ch18-01-what-is-oo.md | 18 | 1257 | ch17-01-what-is-oo | do zrobienia | | 0 | | |
| ch18-02-trait-objects.md | 18 | 2203 | ch17-02-trait-objects | do zrobienia | | 0 | | |
| ch18-03-oo-design-patterns.md | 18 | 4285 | ch17-03-oo-design-patterns | do zrobienia | | 0 | | |
| ch18-04-inventory.md | 18 | 34 | ch17-04-inventory | do zrobienia | | 0 | | |
| ch18-05-design-challenge.md | 18 | 598 | ch17-05-design-challenge-references, ch17-05-design-challenge-trait-trees, ch17-05-design-challenge-dispatch, ch17-05-design-challenge-intermediates | do zrobienia | | 0 | | |
| ch19-00-patterns.md | 19 | 239 | — | do zrobienia | | 0 | | |
| ch19-01-all-the-places-for-patterns.md | 19 | 1657 | ch18-01-all-the-places-for-patterns | do zrobienia | | 0 | | |
| ch19-02-refutability.md | 19 | 650 | ch18-02-refutability | do zrobienia | | 0 | | |
| ch19-03-pattern-syntax.md | 19 | 4266 | ch18-03-pattern-syntax | do zrobienia | | 0 | | |
| ch20-00-advanced-features.md | 20 | 198 | — | do zrobienia | | 0 | | |
| ch20-01-unsafe-rust.md | 20 | 4284 | ch19-01-unsafe-rust | do zrobienia | | 0 | | |
| ch20-02-advanced-traits.md | 20 | 2996 | ch19-03-advanced-traits | do zrobienia | | 0 | | |
| ch20-03-advanced-types.md | 20 | 2024 | ch19-04-advanced-types | do zrobienia | | 0 | | |
| ch20-04-advanced-functions-and-closures.md | 20 | 1151 | ch19-05-advanced-functions-and-closures | do zrobienia | | 0 | | |
| ch20-05-macros.md | 20 | 3550 | ch19-06-macros | do zrobienia | | 0 | | |
| ch21-00-final-project-a-web-server.md | 21 | 356 | — | do zrobienia | | 0 | | |
| ch21-01-single-threaded.md | 21 | 3273 | — | do zrobienia | | 0 | | |
| ch21-02-multithreaded.md | 21 | 4855 | — | do zrobienia | | 0 | | |
| ch21-03-graceful-shutdown-and-cleanup.md | 21 | 1497 | — | do zrobienia | | 0 | | |
| end-of-experiment.md | 0 | 47 | — | gotowe | afe257bc | 1 |  |  |
| appendix-00.md | dod. | 17 | — | do zrobienia | | 0 | | |
| appendix-01-keywords.md | dod. | 743 | — | do zrobienia | | 0 | | |
| appendix-02-operators.md | dod. | 1779 | — | do zrobienia | | 0 | | |
| appendix-03-derivable-traits.md | dod. | 1495 | — | do zrobienia | | 0 | | |
| appendix-04-useful-development-tools.md | dod. | 567 | — | do zrobienia | | 0 | | |
| appendix-05-editions.md | dod. | 496 | — | do zrobienia | | 0 | | |
| appendix-06-translation.md | dod. | 97 | — | do zrobienia | | 0 | | |
| appendix-07-nightly-rust.md | dod. | 1376 | — | do zrobienia | | 0 | | |


## Decyzje orkiestratora

- F0.3: `pnpm init-repo` zgłasza błędy typów w `@types/node` (TS1005), ale `dist/` powstaje i build przechodzi; mdbook-quiz działa lokalnie, fallback R2 (`przelot.py`) niepotrzebny (skrypt istnieje).
- F0.5: G0 zielona w trybie `attr`: 590 pinów, 0 pominiętych, id w `<main>` identyczne dla 120 plików.
- F0.7: G1 dla notatek/etykiet plików: błąd, gdy suma `Uwaga:`+`Note:` ≠ liczbie `Note:` w oryginale; pozostawione `Note:`/`Filename:` to ostrzeżenie G5 (inaczej nietknięte pliki nie przeszłyby autotestu „zero błędów”). `SUMMARY.md` nie wymaga `{#id}`.
- F0.8: baseline linków pusty (0 zepsutych kotwic w oryginale).
- F1.1: KONWENCJE uzupełnione o zasadę zachowania łamania linii oryginału (rozdziały Brown mają akapity w jednej linii) i o zakaz linii zaczynających się od znaków Markdownu po zawinięciu.
- F2: glosariusz uzupełniony o terminy z raportów pilota przed recenzją (rustowcy, box, ramka stosu, wartość wskazywana, …); KONWENCJE: listy, rodzaj gramatyczny, „Hello, world!”. `glosariusz_lint.py` pomija angielskie odpowiedniki w nawiasie `(*...*)` (forma D4). G5 ignoruje `{#id}` i dyrektywy.
- F2.3 autoreview pilota: jakość dobra (bez błędów merytorycznych); poprawiono listy w ch04-01 (fragmenty zdań małą literą ze średnikami), „dokumentacja API” w ch01-01. Wszystkie propozycje „?” w glosariuszu zatwierdzone bez zmian. Dodano: zwalnianie (*freeing* lub *dropping*), modyfikować (*mutate*), endpoint, błąd segmentacji.
- F2.4: wdrożony pilot (9113fa4a) zweryfikowany: notatka „Uwaga:” w `<section class="note">`, aquascope i quizy na ch04-01.
- F3: nazwa serwisu w prozie „crates.io” (wielka litera tylko na początku zdania i w cytowanych tytułach); nagłówek ch14-00 „Więcej o Cargo i crates.io” do ujednolicenia w F5.

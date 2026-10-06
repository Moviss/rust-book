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
- [ ] F0.10 Commit narzędzi, push, CI
- [ ] F1.1 `KONWENCJE.md`
- [ ] F1.2 `GLOSARIUSZ.md`
- [ ] F1.3 `wyjatki.toml`
- [ ] F1.4 `postep.py --init`
- [ ] F1.5 `glosariusz_lint.py` na glosariuszu
- [ ] F1.6 Commit konwencji
- [ ] F2.1 Pilot: tłumaczenie
- [ ] F2.2 Pilot: przegląd, bramki
- [ ] F2.3 Autoreview pilota
- [ ] F2.4 Push i weryfikacja strony
- [ ] F3.1 Strony otwierające
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

## Decyzje orkiestratora

- F0.3: `pnpm init-repo` zgłasza błędy typów w `@types/node` (TS1005), ale `dist/` powstaje i build przechodzi; mdbook-quiz działa lokalnie, fallback R2 (`przelot.py`) niepotrzebny (skrypt istnieje).
- F0.5: G0 zielona w trybie `attr`: 590 pinów, 0 pominiętych, id w `<main>` identyczne dla 120 plików.
- F0.7: G1 dla notatek/etykiet plików: błąd, gdy suma `Uwaga:`+`Note:` ≠ liczbie `Note:` w oryginale; pozostawione `Note:`/`Filename:` to ostrzeżenie G5 (inaczej nietknięte pliki nie przeszłyby autotestu „zero błędów”). `SUMMARY.md` nie wymaga `{#id}`.
- F0.8: baseline linków pusty (0 zepsutych kotwic w oryginale).

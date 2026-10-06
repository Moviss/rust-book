# Konwencje tłumaczenia

Obowiązują tłumaczy i recenzentów. Źródło: `PLAN.md`, sekcje 2 i 9.1. Zmienia je
wyłącznie orkiestrator.

**Decyzje z planu (skrót):** D2 kod bez zmian bajt po bajcie; D3 nagłówki z
`{#id}`; D4 pierwsze wystąpienie terminu w prozie pliku „polski (*english*)” lub
„*crate* (objaśnienie)”, bez objaśnień w nagłówkach; D5 nie odmieniamy kodu
inline; D6 „możesz”, „napiszemy”; D7 typografia „…”, ‚…’, „ – ”, nagłówki
zdaniowe, crate’a; D8 pola quizów bez zmian; D9 „Uwaga:”, „Plik:”, „Listing N-M”,
„Tabela N-M”, „Rysunek N-M”.

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
- zachowaj sposób łamania oryginału: akapit zapisany w oryginale w jednej linii
  zostaje w jednej linii (tak jest w rozdziałach Brown); akapit zawinięty
  zawijaj w okolicach 80 znaków;
- przy zawijaniu żadna linia nie może zaczynać się od znaku, który zmienia jej
  znaczenie w Markdownie (`#`, `>`, `-`, `+`, `*`, `1.`), a każda linia w
  cytacie zaczyna się od `> `;
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

**Zakres pliku:** tłumacz cały plik od początku do końca, łącznie z treścią
notatek, przypisów, podpisów i tabel. Nie skracaj i nie streszczaj.

**Teksty Brown o quizach i eksperymencie:** nazwy elementów interfejsu (np.
„Submit”, „Next”) zostają po angielsku w cudzysłowie; opisy wokół nich
tłumaczymy.

**Listy:** punkty będące fragmentami zdania wprowadzonego dwukropkiem zaczynają
się małą literą i kończą średnikiem (ostatni kropką); punkty będące pełnymi
zdaniami zaczynają się wielką literą i kończą kropką.

**Rodzaj gramatyczny:** tam, gdzie to łatwe, unikaj form rodzajowych w zwrotach
do czytelnika („udało ci się napisać” zamiast „napisałeś”); jeśli się nie da,
używaj formy męskiej.

**Tytuły programów i nazwy własne:** „Hello, world!” i „Hello, Cargo!” zostają po
angielsku (nazwa programu); nagłówek „Hello, World!” zapisujemy „Hello, world!”.

**Odwołania do podrozdziałów:** „Chapter 4.1” → „podrozdział 4.1” (odmiana: w podrozdziale 4.1); „Chapter 4” → „rozdział 4”.

**Odwołania do sekcji:** cytowany nagłówek z innego pliku zapowiadamy jako „podrozdział „Tytuł”” (nie „sekcja”), niezależnie od poziomu nagłówka.

**Po „Uwaga:”** piszemy małą literą (polska reguła po dwukropku), chyba że dalej jest nazwa własna lub kod.

**unsafe w prozie:** *unsafe code* bez kodu inline w oryginale → „niebezpieczny kod”.

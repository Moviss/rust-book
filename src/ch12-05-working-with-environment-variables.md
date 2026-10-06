## Praca ze zmiennymi środowiskowymi {#working-with-environment-variables}

Ulepszymy plik binarny `minigrep`, dodając do niego dodatkową funkcjonalność:
opcję wyszukiwania bez rozróżniania wielkości liter, którą użytkownik może
włączyć za pomocą zmiennej środowiskowej. Moglibyśmy zrobić z tej
funkcjonalności opcję wiersza poleceń i wymagać od użytkowników, by podawali ją
za każdym razem, gdy chcą z niej skorzystać. Jeśli jednak zrobimy z niej zmienną
środowiskową, użytkownicy będą mogli ustawić ją raz i w danej sesji terminala
wszystkie ich wyszukiwania będą ignorować wielkość liter.

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-a-failing-test-for-the-case-insensitive-search-function"></a>

### Pisanie testu wyszukiwania bez rozróżniania wielkości liter, który kończy się niepowodzeniem {#writing-a-failing-test-for-case-insensitive-search}

Najpierw dodajemy do biblioteki `minigrep` nową funkcję
`search_case_insensitive`, która będzie wywoływana, gdy zmienna środowiskowa ma
jakąś wartość. Nadal postępujemy zgodnie z procesem TDD, więc pierwszym krokiem
znów jest napisanie testu, który kończy się niepowodzeniem. Dodamy nowy test dla
nowej funkcji `search_case_insensitive` i zmienimy nazwę starego testu z
`one_result` na `case_sensitive`, aby wyraźniej pokazać różnicę między tymi
dwoma testami, jak w listingu 12-20.

<Listing number="12-20" file-name="src/lib.rs" caption="Dodanie nowego testu kończącego się niepowodzeniem dla funkcji ignorującej wielkość liter, którą zaraz dodamy">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-20/src/lib.rs:here}}
```

</Listing>

Zwróć uwagę, że zmieniliśmy też `contents` w starym teście. Dodaliśmy nowy wiersz
z tekstem `"Duct tape."`, zaczynającym się wielką literą _D_, która nie powinna
pasować do zapytania `"duct"`, gdy wyszukujemy z rozróżnianiem wielkości liter.
Taka zmiana starego testu pomaga upewnić się, że przypadkiem nie zepsujemy już
zaimplementowanej funkcjonalności wyszukiwania z rozróżnianiem wielkości liter.
Ten test powinien teraz przechodzić i powinien przechodzić nadal, gdy będziemy
pracować nad wyszukiwaniem ignorującym wielkość liter.

Nowy test wyszukiwania _bez_ rozróżniania wielkości liter używa zapytania
`"rUsT"`. W funkcji `search_case_insensitive`, którą zaraz dodamy, zapytanie
`"rUsT"` powinno pasować do wiersza zawierającego `"Rust:"` z wielką literą _R_
oraz do wiersza `"Trust me."`, mimo że oba mają inną wielkość liter niż
zapytanie. To nasz test kończący się niepowodzeniem – nawet się nie skompiluje,
bo nie zdefiniowaliśmy jeszcze funkcji `search_case_insensitive`. Możesz dodać
szkieletową implementację, która zawsze zwraca pusty wektor (*vector*),
podobnie jak zrobiliśmy to z funkcją `search` w listingu 12-16, aby zobaczyć,
jak test się kompiluje i kończy niepowodzeniem.

### Implementacja funkcji `search_case_insensitive` {#implementing-the-search_case_insensitive-function}

Funkcja `search_case_insensitive`, pokazana w listingu 12-21, będzie niemal
taka sama jak funkcja `search`. Jedyna różnica polega na tym, że zamienimy
`query` i każdą `line` na małe litery, dzięki czemu niezależnie od wielkości
liter w argumentach wejściowych podczas sprawdzania, czy wiersz zawiera
zapytanie, będą one miały tę samą wielkość liter.

<Listing number="12-21" file-name="src/lib.rs" caption="Zdefiniowanie funkcji `search_case_insensitive`, która przed porównaniem zamienia zapytanie i wiersz na małe litery">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-21/src/lib.rs:here}}
```

</Listing>

Najpierw zamieniamy łańcuch znaków (*string*) `query` na małe litery i
zapisujemy go w nowej zmiennej o tej samej nazwie. To przesłanianie
(*shadowing*) oryginalnej zmiennej `query`. Wywołanie `to_lowercase` na
zapytaniu jest konieczne, aby niezależnie od tego, czy użytkownik wpisze
`"rust"`, `"RUST"`, `"Rust"` czy `"rUsT"`, traktować zapytanie tak, jakby
brzmiało `"rust"`, i ignorować wielkość liter. Choć `to_lowercase` obsługuje
podstawowy Unicode, nie działa w 100 procentach dokładnie. Gdybyśmy pisali
prawdziwą aplikację, trzeba by tu włożyć nieco więcej pracy, ale ten
podrozdział dotyczy zmiennych środowiskowych, a nie Unicode, więc na tym
poprzestaniemy.

Zwróć uwagę, że `query` jest teraz typu `String`, a nie wycinkiem łańcucha
(*string slice*), ponieważ wywołanie `to_lowercase` tworzy nowe dane, zamiast
odwoływać się do istniejących. Załóżmy na przykład, że zapytanie to `"rUsT"`:
ten wycinek łańcucha nie zawiera małej litery `u` ani `t`, której moglibyśmy
użyć, więc musimy zaalokować nowy `String` zawierający `"rust"`. Przekazując
teraz `query` jako argument do metody `contains`, musimy dodać znak ampersand,
ponieważ sygnatura `contains` jest zdefiniowana tak, że przyjmuje wycinek
łańcucha.

Następnie dodajemy wywołanie `to_lowercase` na każdej `line`, aby zamienić
wszystkie jej znaki na małe litery. Skoro `line` i `query` są już zamienione na
małe litery, znajdziemy dopasowania niezależnie od wielkości liter w zapytaniu.

Sprawdźmy, czy ta implementacja przechodzi testy:

```console
{{#include ../listings/ch12-an-io-project/listing-12-21/output.txt}}
```

Świetnie! Przeszły. Teraz wywołajmy nową funkcję `search_case_insensitive` z
funkcji `run`. Najpierw dodamy do struktury (*struct*) `Config` opcję
konfiguracyjną, która pozwoli przełączać się między wyszukiwaniem z
rozróżnianiem wielkości liter a wyszukiwaniem bez niego. Dodanie tego pola
spowoduje błędy kompilatora, ponieważ jeszcze nigdzie go nie inicjalizujemy:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:here}}
```

Dodaliśmy pole `ignore_case`, które przechowuje wartość logiczną. Następnie
funkcja `run` musi sprawdzać wartość pola `ignore_case` i na jej podstawie
decydować, czy wywołać funkcję `search`, czy funkcję
`search_case_insensitive`, jak pokazano w listingu 12-22. To nadal się nie
skompiluje.

<Listing number="12-22" file-name="src/main.rs" caption="Wywołanie `search` albo `search_case_insensitive` w zależności od wartości `config.ignore_case`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-22/src/main.rs:there}}
```

</Listing>

Na koniec musimy sprawdzić zmienną środowiskową. Funkcje do pracy ze zmiennymi
środowiskowymi znajdują się w module `env` biblioteki standardowej, który jest
już w zasięgu (*scope*) na początku pliku _src/main.rs_. Użyjemy funkcji `var`
z modułu `env`, aby sprawdzić, czy ustawiono jakąkolwiek wartość dla zmiennej
środowiskowej o nazwie `IGNORE_CASE`, jak pokazano w listingu 12-23.

<Listing number="12-23" file-name="src/main.rs" caption="Sprawdzanie, czy zmienna środowiskowa o nazwie `IGNORE_CASE` ma jakąkolwiek wartość">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-23/src/main.rs:here}}
```

</Listing>

Tworzymy tu nową zmienną `ignore_case`. Aby ustawić jej wartość, wywołujemy
funkcję `env::var` i przekazujemy jej nazwę zmiennej środowiskowej
`IGNORE_CASE`. Funkcja `env::var` zwraca `Result`, który będzie wariantem
sukcesu `Ok` zawierającym wartość zmiennej środowiskowej, jeśli ta zmienna ma
ustawioną jakąkolwiek wartość. Jeśli zmienna środowiskowa nie jest ustawiona,
funkcja zwróci wariant `Err`.

Używamy metody `is_ok` na `Result`, aby sprawdzić, czy zmienna środowiskowa jest
ustawiona, co oznacza, że program powinien wyszukiwać bez rozróżniania wielkości
liter. Jeśli zmienna środowiskowa `IGNORE_CASE` nie ma żadnej wartości, `is_ok`
zwróci `false`, a program wykona wyszukiwanie z rozróżnianiem wielkości liter.
Nie interesuje nas _wartość_ zmiennej środowiskowej, tylko to, czy jest
ustawiona, czy nie, więc sprawdzamy `is_ok`, zamiast używać `unwrap`, `expect`
czy którejkolwiek z pozostałych poznanych metod typu `Result`.

Wartość zmiennej `ignore_case` przekazujemy do instancji `Config`, aby funkcja
`run` mogła ją odczytać i zdecydować, czy wywołać `search_case_insensitive`,
czy `search`, tak jak zaimplementowaliśmy to w listingu 12-22.

Wypróbujmy to! Najpierw uruchomimy program bez ustawionej zmiennej
środowiskowej, z zapytaniem `to`, które powinno pasować do każdego wiersza
zawierającej słowo _to_ zapisane małymi literami:

```console
{{#include ../listings/ch12-an-io-project/listing-12-23/output.txt}}
```

Wygląda na to, że nadal działa! Teraz uruchommy program z `IGNORE_CASE`
ustawionym na `1`, ale z tym samym zapytaniem `to`:

```console
$ IGNORE_CASE=1 cargo run -- to poem.txt
```

Jeśli używasz PowerShella, musisz ustawić zmienną środowiskową i uruchomić
program jako osobne polecenia:

```console
PS> $Env:IGNORE_CASE=1; cargo run -- to poem.txt
```

Dzięki temu `IGNORE_CASE` pozostanie ustawiona do końca sesji powłoki. Można ją
usunąć za pomocą cmdletu `Remove-Item`:

```console
PS> Remove-Item Env:IGNORE_CASE
```

Powinniśmy dostać wiersze zawierające _to_, w których mogą występować wielkie
litery:

<!-- manual-regeneration
cd listings/ch12-an-io-project/listing-12-23
IGNORE_CASE=1 cargo run -- to poem.txt
can't extract because of the environment variable
-->

```console
Are you nobody, too?
How dreary to be somebody!
To tell your name the livelong day
To an admiring bog!
```

Doskonale, dostaliśmy też wiersze zawierające _To_! Nasz program `minigrep`
potrafi teraz wyszukiwać bez rozróżniania wielkości liter, a sterujemy tym za
pomocą zmiennej środowiskowej. Wiesz już, jak obsługiwać opcje ustawiane za
pomocą argumentów wiersza poleceń albo zmiennych środowiskowych.

Niektóre programy pozwalają na ustawienie tej samej opcji konfiguracji zarówno
argumentem, _jak i_ zmienną środowiskową. W takich przypadkach program
rozstrzyga, które z nich ma pierwszeństwo. W ramach kolejnego samodzielnego
ćwiczenia spróbuj sterować rozróżnianiem wielkości liter za pomocą argumentu
wiersza poleceń albo zmiennej środowiskowej. Zdecyduj, czy pierwszeństwo
powinien mieć argument wiersza poleceń, czy zmienna środowiskowa, jeśli program
zostanie uruchomiony z jednym ustawionym na rozróżnianie wielkości liter, a
drugim na jej ignorowanie.

Moduł `std::env` zawiera wiele innych przydatnych funkcjonalności do pracy ze
zmiennymi środowiskowymi: zajrzyj do jego dokumentacji, aby zobaczyć, co jest
dostępne.

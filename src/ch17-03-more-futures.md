<!-- Old headings. Do not remove or links may break. -->

<a id="yielding"></a>

### Oddawanie sterowania środowisku uruchomieniowemu {#yielding-control-to-the-runtime}

Przypomnij sobie z podrozdziału
[„Nasz pierwszy program asynchroniczny”][async-program]<!-- ignore -->, że w
każdym punkcie oczekiwania (*await point*) Rust daje środowisku
uruchomieniowemu (*runtime*) szansę wstrzymać zadanie i przełączyć się na inne,
jeśli *future* (wartość, która będzie gotowa później), na który czekamy, nie
jest jeszcze gotowy. Działa to też w drugą stronę: Rust wstrzymuje bloki async
i oddaje sterowanie środowisku uruchomieniowemu _wyłącznie_ w punktach
oczekiwania. Wszystko pomiędzy punktami oczekiwania wykonuje się synchronicznie.

Oznacza to, że jeśli wykonasz w bloku async dużo pracy bez żadnego punktu
oczekiwania, ten future zablokuje postęp wszystkich innych future’ów. Czasem
można usłyszeć, że jeden future _zagładza_ inne future’y. W niektórych
przypadkach może to nie mieć większego znaczenia. Jeśli jednak wykonujesz jakąś
kosztowną konfigurację lub długotrwałą pracę albo masz future, który ma bez
końca wykonywać jakieś zadanie, musisz zastanowić się, kiedy i gdzie oddawać
sterowanie środowisku uruchomieniowemu.

Zasymulujmy długotrwałą operację, aby zilustrować problem zagłodzenia, a potem
zastanówmy się, jak go rozwiązać. Listing 17-14 wprowadza funkcję `slow`.

<Listing number="17-14" caption="Użycie `thread::sleep` do symulowania wolnych operacji" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-14/src/main.rs:slow}}
```

</Listing>

Ten kod używa `std::thread::sleep` zamiast `trpl::sleep`, dzięki czemu
wywołanie `slow` zablokuje bieżący wątek na określoną liczbę milisekund.
Możemy użyć `slow` w zastępstwie rzeczywistych operacji, które są zarówno
długotrwałe, jak i blokujące.

W listingu 17-15 używamy `slow`, aby zasymulować wykonywanie tego rodzaju pracy
ograniczonej przez procesor w parze future’ów.

<Listing number="17-15" caption="Wywoływanie funkcji `slow` do symulowania wolnych operacji" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-15/src/main.rs:slow-futures}}
```

</Listing>

Każdy future oddaje sterowanie środowisku uruchomieniowemu dopiero _po_
wykonaniu szeregu wolnych operacji. Jeśli uruchomisz ten kod, zobaczysz taki
wynik:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-15/
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'a' ran for 10ms
'a' ran for 20ms
'b' started.
'b' ran for 75ms
'b' ran for 10ms
'b' ran for 15ms
'b' ran for 350ms
'a' finished.
```

Podobnie jak w listingu 17-5, w którym użyliśmy `trpl::select`, aby future’y
pobierające dwa adresy URL ścigały się ze sobą, `select` nadal kończy się, gdy
tylko `a` skończy pracę. Wywołania `slow` w obu future’ach jednak się nie
przeplatają. Future `a` wykonuje całą swoją pracę, aż do oczekiwania na
wywołanie `trpl::sleep`, następnie future `b` wykonuje całą swoją pracę, aż do
oczekiwania na własne wywołanie `trpl::sleep`, a na końcu kończy się future
`a`. Aby oba future’y mogły robić postępy między swoimi wolnymi zadaniami,
potrzebujemy punktów oczekiwania, w których oddamy sterowanie środowisku
uruchomieniowemu. A to znaczy, że potrzebujemy czegoś, na co możemy czekać!

Takie przekazywanie sterowania widać już w listingu 17-15: gdybyśmy usunęli
`trpl::sleep` na końcu future’a `a`, zakończyłby się on, zanim future `b`
_w ogóle_ by się uruchomił. Spróbujmy użyć funkcji `trpl::sleep` jako punktu
wyjścia, aby operacje mogły na zmianę robić postępy, jak pokazano w
listingu 17-16.

<Listing number="17-16" caption="Użycie `trpl::sleep`, aby operacje mogły na zmianę robić postępy" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-16/src/main.rs:here}}
```

</Listing>

Między kolejnymi wywołaniami `slow` dodaliśmy wywołania `trpl::sleep` z
punktami oczekiwania. Teraz praca obu future’ów się przeplata:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-16
cargo run
copy just the output
-->

```text
'a' started.
'a' ran for 30ms
'b' started.
'b' ran for 75ms
'a' ran for 10ms
'b' ran for 10ms
'a' ran for 20ms
'b' ran for 15ms
'a' finished.
```

Future `a` nadal działa przez chwilę, zanim przekaże sterowanie do `b`, bo
wywołuje `slow`, zanim w ogóle wywoła `trpl::sleep`, ale potem future’y
zamieniają się za każdym razem, gdy któryś z nich dotrze do punktu
oczekiwania.
Zrobiliśmy to po każdym wywołaniu `slow`, ale moglibyśmy podzielić pracę w
dowolny sposób, który najbardziej nam odpowiada.

Tak naprawdę nie chcemy tu jednak _spać_: chcemy robić postępy tak szybko, jak
to możliwe. Musimy jedynie oddać sterowanie środowisku uruchomieniowemu. Możemy
to zrobić bezpośrednio za pomocą funkcji `trpl::yield_now`. W listingu 17-17
zastępujemy wszystkie wywołania `trpl::sleep` wywołaniami `trpl::yield_now`.

<Listing number="17-17" caption="Użycie `yield_now`, aby operacje mogły na zmianę robić postępy" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-17/src/main.rs:yields}}
```

</Listing>

Ten kod lepiej wyraża faktyczny zamiar i może być znacznie szybszy niż użycie
`sleep`, ponieważ timery, takie jak ten używany przez `sleep`, często mają
ograniczoną rozdzielczość. Wersja `sleep`, której używamy, zawsze śpi na
przykład przez co najmniej milisekundę, nawet jeśli przekażemy jej `Duration`
równe jednej nanosekundzie. Przypomnijmy raz jeszcze: współczesne komputery są
_szybkie_ – w ciągu jednej milisekundy potrafią zrobić bardzo dużo!

Oznacza to, że async może się przydać nawet w zadaniach ograniczonych przez
obliczenia, zależnie od tego, co jeszcze robi twój program, bo daje użyteczne
narzędzie do strukturyzowania relacji między różnymi częściami programu
(kosztem narzutu asynchronicznej maszyny stanów). Jest to forma
_wielozadaniowości kooperacyjnej_ (*cooperative multitasking*), w której każdy
future może sam decydować, kiedy oddaje sterowanie, za pomocą punktów
oczekiwania.
Dlatego każdy future odpowiada też za to, by nie blokować zbyt długo. W
niektórych wbudowanych systemach operacyjnych opartych na Ruście jest to
_jedyny_ rodzaj wielozadaniowości!

W rzeczywistym kodzie zwykle nie będziesz oczywiście przeplatać wywołań funkcji
z punktami oczekiwania w każdym wierszu. Choć oddawanie sterowania w ten sposób
jest stosunkowo tanie, nie jest darmowe. W wielu przypadkach próba podzielenia
zadania ograniczonego przez obliczenia może je znacznie spowolnić, więc czasem
dla wydajności _całości_ lepiej pozwolić operacji na krótkie zablokowanie.
Zawsze mierz, aby ustalić, gdzie leżą faktyczne wąskie gardła wydajności twojego
kodu. Warto jednak pamiętać o tej mechanice, jeśli _widzisz_, że wiele pracy
wykonuje się sekwencyjnie, choć oczekiwano współbieżności (*concurrency*)!

### Budowanie własnych abstrakcji asynchronicznych {#building-our-own-async-abstractions}

Future’y możemy też składać ze sobą, tworząc nowe wzorce. Możemy na przykład
zbudować funkcję `timeout` z asynchronicznych klocków, które już mamy. Gdy
skończymy, wynik będzie kolejnym klockiem, którego moglibyśmy użyć do
tworzenia kolejnych abstrakcji asynchronicznych.

Listing 17-18 pokazuje, jak spodziewalibyśmy się, że `timeout` będzie działać z
wolnym future’em.

<Listing number="17-18" caption="Użycie wyobrażonej funkcji `timeout` do wykonania wolnej operacji z limitem czasu" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-18/src/main.rs:here}}
```

</Listing>

Zaimplementujmy to! Na początek zastanówmy się nad API funkcji `timeout`:

- Sama musi być funkcją asynchroniczną, abyśmy mogli na nią czekać.
- Jej pierwszym parametrem powinien być future do uruchomienia. Możemy użyć
  typów generycznych (*generics*), aby działała z dowolnym future’em.
- Jej drugim parametrem będzie maksymalny czas oczekiwania. Jeśli użyjemy
  `Duration`, łatwo będzie go przekazać dalej do `trpl::sleep`.
- Powinna zwracać `Result`. Jeśli future zakończy się powodzeniem, `Result`
  będzie wariantem `Ok` z wartością wytworzoną przez future. Jeśli najpierw
  upłynie limit czasu, `Result` będzie wariantem `Err` z czasem, przez jaki
  czekaliśmy.

Listing 17-19 pokazuje tę deklarację.

<!-- This is not tested because it intentionally does not compile. -->

<Listing number="17-19" caption="Definicja sygnatury funkcji `timeout`" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-19/src/main.rs:declaration}}
```

</Listing>

To spełnia nasze cele dotyczące typów. Zastanówmy się teraz nad potrzebnym
_zachowaniem_: chcemy, aby przekazany future ścigał się z czasem trwania.
Możemy użyć `trpl::sleep`, aby utworzyć z czasu trwania future’a-timer, oraz
`trpl::select`, aby uruchomić ten timer razem z future’em przekazanym przez
kod wywołujący.

W listingu 17-20 implementujemy `timeout`, dopasowując wynik oczekiwania na
`trpl::select`.

<Listing number="17-20" caption="Definicja funkcji `timeout` za pomocą `select` i `sleep`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-20/src/main.rs:implementation}}
```

</Listing>

Implementacja `trpl::select` nie jest sprawiedliwa: zawsze odpytuje (*polls*)
argumenty w kolejności, w jakiej zostały przekazane (inne implementacje `select`
losowo wybierają, który argument odpytać najpierw). Dlatego przekazujemy
`future_to_try` do `select` jako pierwszy, aby miał szansę się zakończyć, nawet
jeśli `max_time` jest bardzo krótkim czasem. Jeśli `future_to_try` zakończy się
pierwszy, `select` zwróci `Left` z wynikiem `future_to_try`. Jeśli pierwszy
zakończy się `timer`, `select` zwróci `Right` z wynikiem timera, czyli `()`.

Jeśli `future_to_try` zakończy się powodzeniem i otrzymamy `Left(output)`,
zwracamy `Ok(output)`. Jeśli zamiast tego upłynie czas timera i otrzymamy
`Right(())`, ignorujemy `()` za pomocą `_` i zwracamy `Err(max_time)`.

W ten sposób mamy działającą funkcję `timeout` zbudowaną z dwóch innych
asynchronicznych funkcji pomocniczych. Jeśli uruchomimy nasz kod, po upływie
limitu czasu wypisze on komunikat o niepowodzeniu:

```text
Failed after 2 seconds
```

Ponieważ future’y można składać z innymi future’ami, z mniejszych
asynchronicznych klocków możesz budować naprawdę potężne narzędzia. Możesz na
przykład użyć tego samego podejścia, aby połączyć limity czasu z ponownymi
próbami, a następnie stosować je w operacjach takich jak wywołania sieciowe
(jak te z listingu 17-5).

W praktyce zwykle będziesz pracować bezpośrednio z `async` i `await`, a w
drugiej kolejności z funkcjami takimi jak `select` i makrami takimi jak makro
`join!`, aby kontrolować, jak wykonują się najbardziej zewnętrzne future’y.

Poznaliśmy już kilka sposobów pracy z wieloma future’ami jednocześnie. Dalej
przyjrzymy się, jak pracować z wieloma future’ami po kolei w czasie za pomocą
_strumieni_ (*streams*).

{{#quiz ../quizzes/async-03-more-futures.toml}}

[async-program]: ch17-01-futures-and-syntax.html#our-first-async-program

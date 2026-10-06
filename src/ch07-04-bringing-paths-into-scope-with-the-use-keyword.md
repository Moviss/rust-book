## Wprowadzanie ścieżek do zasięgu za pomocą słowa kluczowego `use` {#bringing-paths-into-scope-with-the-use-keyword}

Wypisywanie pełnych ścieżek przy każdym wywołaniu funkcji bywa niewygodne
i monotonne. W listingu 7-7, niezależnie od tego, czy wybraliśmy ścieżkę
bezwzględną, czy względną do funkcji `add_to_waitlist`, przy każdym wywołaniu
`add_to_waitlist` musieliśmy podawać także `front_of_house` i `hosting`.
Na szczęście da się to uprościć: możemy raz utworzyć skrót do ścieżki za pomocą
słowa kluczowego (*keyword*) `use`, a potem w całym zasięgu (*scope*) używać
krótszej nazwy.

W listingu 7-11 wprowadzamy moduł `crate::front_of_house::hosting` do zasięgu
funkcji `eat_at_restaurant`, dzięki czemu, aby wywołać funkcję
`add_to_waitlist` w `eat_at_restaurant`, wystarczy podać
`hosting::add_to_waitlist`.

<Listing number="7-11" file-name="src/lib.rs" caption="Wprowadzanie modułu do zasięgu za pomocą `use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-11/src/lib.rs}}
```

</Listing>

Dodanie `use` i ścieżki w zasięgu przypomina utworzenie dowiązania
symbolicznego w systemie plików. Po dodaniu `use crate::front_of_house::hosting`
w korzeniu crate’a (*crate root*; *crate* to jednostka kompilacji w Ruście)
`hosting` staje się w tym zasięgu poprawną nazwą, tak jakby moduł `hosting` był
zdefiniowany w korzeniu crate’a. Ścieżki wprowadzone do zasięgu za pomocą `use`
podlegają też sprawdzaniu prywatności, jak wszystkie inne ścieżki.

Zwróć uwagę, że `use` tworzy skrót tylko dla konkretnego zasięgu, w którym
znajduje się to `use`. Listing 7-12 przenosi funkcję `eat_at_restaurant` do
nowego modułu podrzędnego o nazwie `customer`, który stanowi już inny zasięg
niż instrukcja (*statement*) `use`, więc ciało funkcji się nie skompiluje.

<Listing number="7-12" file-name="src/lib.rs" caption="Instrukcja `use` obowiązuje tylko w zasięgu, w którym się znajduje.">

```rust,noplayground,test_harness,does_not_compile,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-12/src/lib.rs}}
```

</Listing>

Błąd kompilatora pokazuje, że skrót nie obowiązuje już w module `customer`:

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-12/output.txt}}
```

Zauważ, że pojawia się też ostrzeżenie, że `use` nie jest już używane w swoim
zasięgu! Aby rozwiązać ten problem, przenieś `use` również do modułu
`customer` albo odwołaj się do skrótu w module nadrzędnym za pomocą
`super::hosting` wewnątrz modułu podrzędnego `customer`.

### Tworzenie idiomatycznych ścieżek `use` {#creating-idiomatic-use-paths}

Być może przy listingu 7-11 zastanawiało cię, dlaczego podaliśmy
`use crate::front_of_house::hosting`, a potem wywołaliśmy
`hosting::add_to_waitlist` w `eat_at_restaurant`, zamiast poprowadzić ścieżkę
`use` aż do funkcji `add_to_waitlist`, co dałoby ten sam efekt, jak
w listingu 7-13.

<Listing number="7-13" file-name="src/lib.rs" caption="Wprowadzanie funkcji `add_to_waitlist` do zasięgu za pomocą `use`, co nie jest idiomatyczne">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-13/src/lib.rs}}
```

</Listing>

Choć listing 7-11 i listing 7-13 robią to samo, listing 7-11 pokazuje
idiomatyczny sposób wprowadzania funkcji do zasięgu za pomocą `use`.
Wprowadzenie do zasięgu modułu nadrzędnego funkcji za pomocą `use` oznacza, że
przy wywołaniu funkcji musimy podać ten moduł nadrzędny. Dzięki temu widać, że
funkcja nie jest zdefiniowana lokalnie, a jednocześnie ograniczamy powtarzanie
pełnej ścieżki. Z kodu w listingu 7-13 nie wynika jasno, gdzie zdefiniowano
`add_to_waitlist`.

Z kolei przy wprowadzaniu za pomocą `use` struktur (*struct*), enumów (*enum*,
typ wyliczeniowy) i innych elementów idiomatyczne jest podawanie pełnej ścieżki.
Listing 7-14 pokazuje idiomatyczny sposób wprowadzenia struktury `HashMap`
z biblioteki standardowej do zasięgu crate’a binarnego.

<Listing number="7-14" file-name="src/main.rs" caption="Idiomatyczne wprowadzanie `HashMap` do zasięgu">

```rust
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-14/src/main.rs}}
```

</Listing>

Za tym idiomem nie stoi żaden ważny powód: po prostu taka konwencja się
wykształciła i ludzie przyzwyczaili się do czytania i pisania kodu w Ruście
w ten sposób.

Wyjątkiem od tego idiomu jest sytuacja, w której za pomocą instrukcji `use`
wprowadzamy do zasięgu dwa elementy o tej samej nazwie, bo Rust na to nie
pozwala. Listing 7-15 pokazuje, jak wprowadzić do zasięgu dwa typy `Result`
o tej samej nazwie, ale z różnych modułów nadrzędnych, i jak się do nich
odwoływać.

<Listing number="7-15" file-name="src/lib.rs" caption="Wprowadzenie dwóch typów o tej samej nazwie do jednego zasięgu wymaga użycia ich modułów nadrzędnych.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-15/src/lib.rs:here}}
```

</Listing>

Jak widać, użycie modułów nadrzędnych pozwala odróżnić od siebie oba typy
`Result`. Gdybyśmy zamiast tego napisali `use std::fmt::Result`
i `use std::io::Result`, mielibyśmy w jednym zasięgu dwa typy `Result` i Rust
nie wiedziałby, o który chodzi nam przy użyciu `Result`.

### Nadawanie nowych nazw za pomocą słowa kluczowego `as` {#providing-new-names-with-the-as-keyword}

Problem wprowadzania za pomocą `use` dwóch typów o tej samej nazwie do jednego
zasięgu można rozwiązać jeszcze inaczej: po ścieżce możemy podać `as` i nową
lokalną nazwę, czyli _alias_, dla tego typu. Listing 7-16 pokazuje inny sposób
zapisania kodu z listingu 7-15 – zmieniamy w nim nazwę jednego z dwóch typów
`Result` za pomocą `as`.

<Listing number="7-16" file-name="src/lib.rs" caption="Zmiana nazwy typu przy wprowadzaniu go do zasięgu za pomocą słowa kluczowego `as`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-16/src/lib.rs:here}}
```

</Listing>

W drugiej instrukcji `use` wybraliśmy dla typu `std::io::Result` nową nazwę
`IoResult`, która nie koliduje z `Result` z `std::fmt`, wprowadzonym również do
zasięgu. Zarówno listing 7-15, jak i listing 7-16 uchodzą za idiomatyczne,
więc wybór należy do ciebie!

### Reeksportowanie nazw za pomocą `pub use` {#re-exporting-names-with-pub-use}

Gdy wprowadzamy nazwę do zasięgu słowem kluczowym `use`, jest ona prywatna dla
zasięgu, do którego ją zaimportowaliśmy. Aby kod spoza tego zasięgu mógł
odwoływać się do tej nazwy tak, jakby była zdefiniowana w tym zasięgu, możemy
połączyć `pub` i `use`. Technika ta nazywa się _reeksportowaniem_
(*re-exporting*), ponieważ wprowadzamy element do zasięgu, a przy tym
udostępniamy go innym, aby mogli wprowadzić go do swojego zasięgu.

Listing 7-17 pokazuje kod z listingu 7-11, w którym `use` w module głównym
zmieniono na `pub use`.

<Listing number="7-17" file-name="src/lib.rs" caption="Udostępnienie nazwy dowolnemu kodowi w nowym zasięgu za pomocą `pub use`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-17/src/lib.rs}}
```

</Listing>

Przed tą zmianą kod zewnętrzny musiałby wywoływać funkcję `add_to_waitlist`
przez ścieżkę `restaurant::front_of_house::hosting::add_to_waitlist()`, co
wymagałoby też oznaczenia modułu `front_of_house` jako `pub`. Teraz, gdy to
`pub use` reeksportowało moduł `hosting` z modułu głównego, kod zewnętrzny może
zamiast tego używać ścieżki `restaurant::hosting::add_to_waitlist()`.

Reeksportowanie przydaje się, gdy wewnętrzna struktura twojego kodu różni się
od tego, jak o danej dziedzinie myślą programiści wywołujący twój kod.
Na przykład w naszej metaforze restauracji osoby prowadzące restaurację myślą
w kategoriach „sali” i „zaplecza”. Klienci odwiedzający restaurację raczej nie
myślą jednak o jej częściach w ten sposób. Dzięki `pub use` możemy napisać kod
o jednej strukturze, a udostępnić na zewnątrz inną. Dzięki temu nasza
biblioteka jest dobrze zorganizowana zarówno dla programistów, którzy nad nią
pracują, jak i dla tych, którzy ją wywołują. Kolejnemu przykładowi `pub use`
i jego wpływowi na dokumentację crate’a przyjrzymy się w podrozdziale
[„Eksportowanie wygodnego publicznego API”][ch14-pub-use]<!-- ignore -->
w rozdziale 14.

### Korzystanie z pakietów zewnętrznych {#using-external-packages}

W rozdziale 2 napisaliśmy grę w zgadywanie, która do generowania liczb losowych
używała zewnętrznego pakietu (*package*) o nazwie `rand`. Aby użyć `rand`
w naszym projekcie, dodaliśmy do pliku _Cargo.toml_ taki wiersz:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch14-03-cargo-workspaces.md
-->

<Listing file-name="Cargo.toml">

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:9:}}
```

</Listing>

Dodanie `rand` jako zależności w _Cargo.toml_ sprawia, że Cargo pobiera pakiet
`rand` wraz z jego zależnościami z [crates.io](https://crates.io/)
i udostępnia `rand` naszemu projektowi.

Następnie, aby wprowadzić definicje z `rand` do zasięgu naszego pakietu,
dodaliśmy wiersz `use` zaczynający się od nazwy crate’a, `rand`, i wymieniliśmy
elementy, które chcieliśmy wprowadzić do zasięgu. Jak pamiętasz, w podrozdziale
[„Generowanie liczby losowej”][rand]<!-- ignore --> w rozdziale 2
wprowadziliśmy do zasięgu trait (*trait*, cecha typu, zbliżona do interfejsu)
`Rng` i wywołaliśmy funkcję `rand::thread_rng`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:ch07-04}}
```

Członkowie społeczności Rusta udostępnili wiele pakietów w serwisie
[crates.io](https://crates.io/), a dołączenie dowolnego z nich do twojego
pakietu wymaga tych samych kroków: wpisania go w pliku _Cargo.toml_ twojego
pakietu i wprowadzenia elementów z jego crate’ów do zasięgu za pomocą `use`.

Zwróć uwagę, że biblioteka standardowa `std` również jest crate’em zewnętrznym
względem naszego pakietu. Ponieważ biblioteka standardowa jest dostarczana
razem z językiem Rust, nie musimy zmieniać _Cargo.toml_, aby dołączyć `std`.
Musimy jednak odwołać się do niej za pomocą `use`, aby wprowadzić jej elementy
do zasięgu naszego pakietu. Na przykład dla `HashMap` użylibyśmy takiego wiersza:

```rust
use std::collections::HashMap;
```

Jest to ścieżka bezwzględna zaczynająca się od `std`, czyli nazwy crate’a
biblioteki standardowej.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-nested-paths-to-clean-up-large-use-lists"></a>

### Porządkowanie list `use` za pomocą ścieżek zagnieżdżonych {#using-nested-paths-to-clean-up-use-lists}

Jeśli używamy wielu elementów zdefiniowanych w tym samym crate’cie lub tym
samym module, wypisywanie każdego z nich w osobnym wierszu może zająć w plikach
sporo miejsca w pionie. Na przykład te dwie instrukcje `use` z gry
w zgadywanie z listingu 2-4 wprowadzają do zasięgu elementy z `std`:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-01-use-std-unnested/src/main.rs:here}}
```

</Listing>

Zamiast tego możemy użyć ścieżek zagnieżdżonych, aby wprowadzić te same
elementy do zasięgu w jednym wierszu. Podajemy wtedy wspólną część ścieżki, po
niej dwa dwukropki, a następnie w nawiasach klamrowych listę tych części
ścieżek, które się różnią, jak pokazano w listingu 7-18.

<Listing number="7-18" file-name="src/main.rs" caption="Podanie ścieżki zagnieżdżonej, aby wprowadzić do zasięgu wiele elementów o tym samym prefiksie">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-18/src/main.rs:here}}
```

</Listing>

W większych programach wprowadzanie wielu elementów z tego samego crate’a lub
modułu za pomocą ścieżek zagnieżdżonych może znacznie zmniejszyć liczbę
potrzebnych osobnych instrukcji `use`!

Ścieżki zagnieżdżonej możemy użyć na dowolnym poziomie ścieżki, co przydaje się
przy łączeniu dwóch instrukcji `use` o wspólnej podścieżce. Na przykład
listing 7-19 pokazuje dwie instrukcje `use`: jedną, która wprowadza do zasięgu
`std::io`, i drugą, która wprowadza do zasięgu `std::io::Write`.

<Listing number="7-19" file-name="src/lib.rs" caption="Dwie instrukcje `use`, z których jedna jest podścieżką drugiej">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-19/src/lib.rs}}
```

</Listing>

Wspólną częścią tych dwóch ścieżek jest `std::io` i jest to zarazem cała
pierwsza ścieżka. Aby połączyć te dwie ścieżki w jedną instrukcję `use`, możemy
użyć `self` w ścieżce zagnieżdżonej, jak pokazano w listingu 7-20.

<Listing number="7-20" file-name="src/lib.rs" caption="Połączenie ścieżek z listingu 7-19 w jedną instrukcję `use`">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-20/src/lib.rs}}
```

</Listing>

Ten wiersz wprowadza do zasięgu `std::io` i `std::io::Write`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-glob-operator"></a>

### Importowanie elementów za pomocą operatora glob {#importing-items-with-the-glob-operator}

Jeśli chcemy wprowadzić do zasięgu _wszystkie_ publiczne elementy zdefiniowane
w danej ścieżce, możemy podać tę ścieżkę, a po niej operator glob `*`:

```rust
use std::collections::*;
```

Ta instrukcja `use` wprowadza do bieżącego zasięgu wszystkie publiczne elementy
zdefiniowane w `std::collections`. Uważaj przy korzystaniu z operatora glob!
Glob może utrudnić ustalenie, jakie nazwy są w zasięgu i gdzie zdefiniowano
nazwę używaną w programie. Co więcej, jeśli zależność zmieni swoje definicje,
zmieni się też to, co zaimportowano. Może to na przykład prowadzić do błędów
kompilacji po aktualizacji zależności, jeśli doda ona definicję o tej samej
nazwie co twoja definicja w tym samym zasięgu.

Operatora glob często używa się w testach, aby wprowadzić wszystko, co jest
testowane, do modułu `tests`; omówimy to w podrozdziale
[„Jak pisać testy”][writing-tests]<!-- ignore --> w rozdziale 11. Operatora glob
używa się też czasem w ramach wzorca *prelude* (zestaw elementów importowanych
automatycznie): więcej informacji o tym wzorcu znajdziesz w
[dokumentacji biblioteki standardowej](https://doc.rust-lang.org/std/prelude/index.html#other-preludes)<!-- ignore -->.

{{#quiz ../quizzes/ch07-04-use.toml}}

[ch14-pub-use]: ch14-02-publishing-to-crates-io.html#exporting-a-convenient-public-api-with-pub-use
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number
[writing-tests]: ch11-01-writing-tests.html#how-to-write-tests

## Przestrzenie robocze Cargo {#cargo-workspaces}

W rozdziale 12 zbudowaliśmy pakiet (*package*) zawierający binarny *crate*
(jednostka kompilacji w Ruście) i crate biblioteczny. W miarę rozwoju projektu
może się okazać, że crate biblioteczny wciąż rośnie i chcesz dalej podzielić
pakiet na kilka crate’ów bibliotecznych. Cargo oferuje mechanizm zwany
przestrzenią roboczą (*workspace*), który pomaga zarządzać wieloma powiązanymi
pakietami rozwijanymi równolegle.

### Tworzenie przestrzeni roboczej {#creating-a-workspace}

_Przestrzeń robocza_ to zbiór pakietów, które współdzielą ten sam plik
_Cargo.lock_ i katalog wyjściowy. Utwórzmy projekt korzystający z przestrzeni
roboczej – użyjemy trywialnego kodu, żeby skupić się na jej strukturze.
Przestrzeń roboczą można zorganizować na wiele sposobów, więc pokażemy tylko
jeden, często spotykany. Nasza przestrzeń robocza będzie zawierać plik binarny
i dwie biblioteki. Plik binarny, który zapewni główną funkcjonalność, będzie
zależał od obu bibliotek. Jedna biblioteka udostępni funkcję `add_one`, a druga
funkcję `add_two`. Te trzy crate’y będą częścią tej samej przestrzeni roboczej.
Zaczniemy od utworzenia nowego katalogu dla przestrzeni roboczej:

```console
$ mkdir add
$ cd add
```

Następnie w katalogu _add_ tworzymy plik _Cargo.toml_, który skonfiguruje całą
przestrzeń roboczą. Ten plik nie będzie miał sekcji `[package]`. Zamiast tego
zacznie się od sekcji `[workspace]`, która pozwoli nam dodawać członków do
przestrzeni roboczej. Dbamy też o to, by nasza przestrzeń robocza korzystała z
najnowszej i najlepszej wersji algorytmu rozwiązywania zależności Cargo
(*resolver*), ustawiając wartość `resolver` na `"3"`:

<span class="filename">Plik: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-01-workspace/add/Cargo.toml}}
```

Następnie utworzymy crate binarny `adder`, uruchamiając `cargo new` w katalogu
_add_:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-01-adder-crate/add
remove `members = ["adder"]` from Cargo.toml
rm -rf adder
cargo new adder
copy output below
-->

```console
$ cargo new adder
     Created binary (application) `adder` package
      Adding `adder` as member of workspace at `file:///projects/add`
```

Uruchomienie `cargo new` wewnątrz przestrzeni roboczej automatycznie dodaje też
nowo utworzony pakiet do klucza `members` w definicji `[workspace]` w pliku
_Cargo.toml_ przestrzeni roboczej, w ten sposób:

```toml
{{#include ../listings/ch14-more-about-cargo/output-only-01-adder-crate/add/Cargo.toml}}
```

Na tym etapie możemy zbudować przestrzeń roboczą, uruchamiając `cargo build`.
Pliki w katalogu _add_ powinny wyglądać tak:

```text
├── Cargo.lock
├── Cargo.toml
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Przestrzeń robocza ma na najwyższym poziomie jeden katalog _target_, do którego
trafią skompilowane artefakty; pakiet `adder` nie ma własnego katalogu
_target_. Nawet gdybyśmy uruchomili `cargo build` z wnętrza katalogu _adder_,
skompilowane artefakty i tak trafiłyby do _add/target_, a nie do
_add/adder/target_. Cargo organizuje katalog _target_ w przestrzeni roboczej w
ten sposób, ponieważ crate’y w przestrzeni roboczej mają od siebie zależeć.
Gdyby każdy crate miał własny katalog _target_, musiałby ponownie kompilować
każdy z pozostałych crate’ów przestrzeni roboczej, żeby umieścić artefakty we
własnym katalogu _target_. Dzięki współdzieleniu jednego katalogu _target_
crate’y unikają zbędnego ponownego budowania.

### Tworzenie drugiego pakietu w przestrzeni roboczej {#creating-the-second-package-in-the-workspace}

Utwórzmy teraz kolejny pakiet należący do przestrzeni roboczej i nazwijmy go
`add_one`. Wygeneruj nowy crate biblioteczny o nazwie `add_one`:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-02-add-one/add
remove `"add_one"` from `members` list in Cargo.toml
rm -rf add_one
cargo new add_one --lib
copy output below
-->

```console
$ cargo new add_one --lib
     Created library `add_one` package
      Adding `add_one` as member of workspace at `file:///projects/add`
```

Plik _Cargo.toml_ najwyższego poziomu będzie teraz zawierał ścieżkę _add_one_
na liście `members`:

<span class="filename">Plik: Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/Cargo.toml}}
```

Katalog _add_ powinien teraz zawierać następujące katalogi i pliki:

```text
├── Cargo.lock
├── Cargo.toml
├── add_one
│   ├── Cargo.toml
│   └── src
│       └── lib.rs
├── adder
│   ├── Cargo.toml
│   └── src
│       └── main.rs
└── target
```

Dodajmy funkcję `add_one` w pliku _add_one/src/lib.rs_:

<span class="filename">Plik: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/add_one/src/lib.rs}}
```

Teraz pakiet `adder` z naszym plikiem binarnym może zależeć od pakietu
`add_one` z naszą biblioteką. Najpierw musimy dodać do _adder/Cargo.toml_
zależność od `add_one` określoną ścieżką.

<span class="filename">Plik: adder/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-02-workspace-with-two-crates/add/adder/Cargo.toml:6:7}}
```

Cargo nie zakłada, że crate’y w przestrzeni roboczej będą od siebie zależeć,
więc relacje zależności musimy określić jawnie.

Następnie użyjmy funkcji `add_one` (z crate’a `add_one`) w crate’cie `adder`.
Otwórz plik _adder/src/main.rs_ i zmień funkcję `main` tak, by wywoływała
funkcję `add_one`, jak w listingu 14-7.

<Listing number="14-7" file-name="adder/src/main.rs" caption="Użycie crate’a bibliotecznego `add_one` w crate’cie `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-07/add/adder/src/main.rs}}
```

</Listing>

Zbudujmy przestrzeń roboczą, uruchamiając `cargo build` w katalogu _add_
najwyższego poziomu!

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.22s
```

Aby uruchomić crate binarny z katalogu _add_, możemy wskazać, który pakiet
przestrzeni roboczej chcemy uruchomić, podając w `cargo run` argument `-p` i
nazwę pakietu:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-07/add
cargo run -p adder
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo run -p adder
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running `target/debug/adder`
Hello, world! 10 plus one is 11!
```

W ten sposób uruchamiamy kod z _adder/src/main.rs_, który zależy od crate’a `add_one`.

<!-- Old headings. Do not remove or links may break. -->

<a id="depending-on-an-external-package-in-a-workspace"></a>

### Zależność od zewnętrznego pakietu {#depending-on-an-external-package}

Zauważ, że przestrzeń robocza ma tylko jeden plik _Cargo.lock_ na najwyższym
poziomie, zamiast osobnego _Cargo.lock_ w katalogu każdego crate’a. Dzięki temu
wszystkie crate’y używają tych samych wersji wszystkich zależności. Jeśli
dodamy pakiet `rand` do plików _adder/Cargo.toml_ i _add_one/Cargo.toml_, Cargo
rozwiąże obie zależności do jednej wersji `rand` i zapisze ją w jedynym pliku
_Cargo.lock_. To, że wszystkie crate’y w przestrzeni roboczej używają tych
samych zależności, oznacza, że zawsze będą ze sobą zgodne. Dodajmy crate `rand`
do sekcji `[dependencies]` w pliku _add_one/Cargo.toml_, żeby móc używać crate’a
`rand` w crate’cie `add_one`:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch02-00-guessing-game-tutorial.md
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
-->

<span class="filename">Plik: add_one/Cargo.toml</span>

```toml
{{#include ../listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add/add_one/Cargo.toml:6:7}}
```

Możemy teraz dodać `use rand;` do pliku _add_one/src/lib.rs_, a zbudowanie
całej przestrzeni roboczej przez uruchomienie `cargo build` w katalogu _add_
pobierze i skompiluje crate `rand`. Otrzymamy jedno ostrzeżenie, ponieważ nie
odwołujemy się do `rand`, które wprowadziliśmy do zasięgu (*scope*):

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-03-workspace-with-external-dependency/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
    Updating crates.io index
  Downloaded rand v0.8.5
   --snip--
   Compiling rand v0.8.5
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
warning: unused import: `rand`
 --> add_one/src/lib.rs:1:5
  |
1 | use rand;
  |     ^^^^
  |
  = note: `#[warn(unused_imports)]` on by default

warning: `add_one` (lib) generated 1 warning (run `cargo fix --lib -p add_one` to apply 1 suggestion)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.95s
```

Plik _Cargo.lock_ najwyższego poziomu zawiera teraz informację o zależności
`add_one` od `rand`. Jednak choć `rand` jest używany gdzieś w przestrzeni
roboczej, nie możemy go używać w innych crate’ach przestrzeni roboczej, dopóki
nie dodamy `rand` także do ich plików _Cargo.toml_. Jeśli na przykład dodamy
`use rand;` do pliku _adder/src/main.rs_ pakietu `adder`, otrzymamy błąd:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/output-only-03-use-rand/add
cargo build
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo build
  --snip--
   Compiling adder v0.1.0 (file:///projects/add/adder)
error[E0432]: unresolved import `rand`
 --> adder/src/main.rs:2:5
  |
2 | use rand;
  |     ^^^^ no external crate `rand`
```

Aby to naprawić, zmodyfikuj plik _Cargo.toml_ pakietu `adder` i wskaż, że
`rand` jest także jego zależnością. Zbudowanie pakietu `adder` doda `rand` do
listy zależności `adder` w _Cargo.lock_, ale żadne dodatkowe kopie `rand` nie
zostaną pobrane. Cargo zadba o to, by każdy crate w każdym pakiecie przestrzeni
roboczej, który używa pakietu `rand`, korzystał z tej samej wersji, o ile
określają one zgodne wersje `rand`. Oszczędza to miejsce i gwarantuje, że
crate’y w przestrzeni roboczej będą ze sobą zgodne.

Jeśli crate’y w przestrzeni roboczej określają niezgodne wersje tej samej
zależności, Cargo rozwiąże każdą z nich, ale i tak będzie się starać, by wersji
było jak najmniej.

Pamiętaj, że Cargo zapewnia zgodność tylko w ramach reguł
[wersjonowania semantycznego][Semantic Versioning]. Załóżmy na przykład, że
przestrzeń robocza ma jeden crate zależny od `rand` 0.8.0 i drugi zależny od
`rand` 0.8.1. Według reguł semver wersja 0.8.1 jest zgodna z 0.8.0, więc oba
crate’y będą zależeć od 0.8.1 (lub ewentualnie od nowszej poprawki, np. 0.8.2).
Jeśli jednak jeden crate zależy od `rand` 0.7.0, a drugi od `rand` 0.8.0, te
wersje są niezgodne według semver. Dlatego Cargo użyje dla każdego crate’a innej
wersji `rand`.

### Dodawanie testu do przestrzeni roboczej {#adding-a-test-to-a-workspace}

Kolejnym usprawnieniem będzie dodanie testu funkcji `add_one::add_one` w
crate’cie `add_one`:

<span class="filename">Plik: add_one/src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add/add_one/src/lib.rs}}
```

Teraz uruchom `cargo test` w katalogu _add_ najwyższego poziomu. Uruchomienie
`cargo test` w przestrzeni roboczej o takiej strukturze wykona testy wszystkich
crate’ów przestrzeni roboczej:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test
copy output below; the output updating script doesn't handle subdirectories in
paths properly
-->

```console
$ cargo test
   Compiling add_one v0.1.0 (file:///projects/add/add_one)
   Compiling adder v0.1.0 (file:///projects/add/adder)
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.20s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

     Running unittests src/main.rs (target/debug/deps/adder-3a47283c568d2b6a)

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

Pierwsza sekcja wyjścia pokazuje, że test `it_works` w crate’cie `add_one`
przeszedł. Następna sekcja pokazuje, że w crate’cie `adder` nie znaleziono
żadnych testów, a ostatnia – że w crate’cie `add_one` nie znaleziono żadnych
testów dokumentacyjnych.

Z katalogu najwyższego poziomu możemy też uruchomić testy jednego konkretnego
crate’a w przestrzeni roboczej, używając flagi `-p` i podając nazwę crate’a,
który chcemy przetestować:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/no-listing-04-workspace-with-tests/add
cargo test -p add_one
copy output below; the output updating script doesn't handle subdirectories in paths properly
-->

```console
$ cargo test -p add_one
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.00s
     Running unittests src/lib.rs (target/debug/deps/add_one-93c49ee75dc46543)

running 1 test
test tests::it_works ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s

   Doc-tests add_one

running 0 tests

test result: ok. 0 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
```

To wyjście pokazuje, że `cargo test` uruchomiło tylko testy crate’a `add_one`,
a testów crate’a `adder` nie uruchomiło.

Jeśli opublikujesz crate’y z przestrzeni roboczej w
[crates.io](https://crates.io/)<!-- ignore -->, każdy crate przestrzeni
roboczej trzeba będzie opublikować osobno. Podobnie jak w przypadku
`cargo test`, możemy opublikować konkretny crate z naszej przestrzeni roboczej,
używając flagi `-p` i podając nazwę crate’a, który chcemy opublikować.

Aby nabrać wprawy, dodaj do tej przestrzeni roboczej crate `add_two` w podobny
sposób jak crate `add_one`!

Gdy projekt się rozrasta, rozważ użycie przestrzeni roboczej: pozwala ona
pracować z mniejszymi, łatwiejszymi do zrozumienia komponentami zamiast z jedną
wielką bryłą kodu. Co więcej, trzymanie crate’ów w przestrzeni roboczej może
ułatwić ich koordynację, jeśli często są zmieniane jednocześnie.

{{#quiz ../quizzes/ch14-03-cargo-workspaces.toml}}

[Semantic Versioning]: https://semver.org/

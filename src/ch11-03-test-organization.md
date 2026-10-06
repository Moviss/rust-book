## Organizacja testów {#test-organization}

Jak wspomnieliśmy na początku rozdziału, testowanie to złożona dziedzina, a
różni ludzie używają różnej terminologii i różnie organizują testy. Społeczność
Rusta dzieli testy na dwie główne kategorie: testy jednostkowe i testy
integracyjne. _Testy jednostkowe_ są małe i bardziej skupione, sprawdzają
naraz jeden moduł w izolacji i mogą testować prywatne interfejsy. _Testy
integracyjne_ są całkowicie zewnętrzne względem twojej biblioteki i korzystają z
twojego kodu tak samo jak każdy inny kod zewnętrzny – używają wyłącznie
publicznego interfejsu i potencjalnie sprawdzają wiele modułów w jednym teście.

Pisanie obu rodzajów testów jest ważne, aby upewnić się, że poszczególne części
twojej biblioteki robią to, czego od nich oczekujesz, zarówno osobno, jak i
razem.

### Testy jednostkowe {#unit-tests}

Celem testów jednostkowych jest testowanie każdej jednostki kodu w izolacji od
reszty kodu, aby szybko wskazać, gdzie kod działa zgodnie z oczekiwaniami, a
gdzie nie. Testy jednostkowe umieszczasz w katalogu _src_, w każdym pliku razem z
kodem, który testują. Przyjęło się tworzyć w każdym pliku moduł o nazwie `tests`,
który zawiera funkcje testowe, i oznaczać ten moduł adnotacją `cfg(test)`.

#### Moduł `tests` i `#[cfg(test)]` {#the-tests-module-and-cfgtest}

Adnotacja `#[cfg(test)]` przy module `tests` mówi Rustowi, żeby kompilował i
uruchamiał kod testowy tylko wtedy, gdy uruchamiasz `cargo test`, a nie gdy
uruchamiasz `cargo build`. Oszczędza to czas kompilacji, gdy chcesz tylko
zbudować bibliotekę, i miejsce w wynikowym skompilowanym artefakcie, ponieważ
testy nie są do niego dołączane. Zobaczysz, że testy integracyjne, które trafiają
do innego katalogu, nie potrzebują adnotacji `#[cfg(test)]`. Ponieważ jednak
testy jednostkowe znajdują się w tych samych plikach co kod, używasz
`#[cfg(test)]`, aby określić, że nie powinny trafić do skompilowanego wyniku.

Przypomnij sobie, że gdy w pierwszym podrozdziale tego rozdziału
wygenerowaliśmy nowy projekt `adder`, Cargo wygenerowało dla nas taki kod:

<span class="filename">Plik: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

W automatycznie wygenerowanym module `tests` atrybut `cfg` oznacza
_konfigurację_ (*configuration*) i mówi Rustowi, że następny element powinien
zostać dołączony tylko przy określonej opcji konfiguracji. W tym przypadku
opcją konfiguracji jest `test`, którą Rust dostarcza do kompilowania i
uruchamiania testów. Dzięki atrybutowi `cfg` Cargo kompiluje nasz kod testowy
tylko wtedy, gdy faktycznie uruchamiamy testy za pomocą `cargo test`. Dotyczy to
także wszelkich funkcji pomocniczych, które mogą znajdować się w tym module,
oprócz funkcji oznaczonych `#[test]`.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-private-functions"></a>

#### Testowanie funkcji prywatnych {#private-function-tests}

W środowisku testerów toczy się debata, czy funkcje prywatne należy testować
bezpośrednio, a inne języki utrudniają lub wręcz uniemożliwiają testowanie
funkcji prywatnych. Niezależnie od tego, jakiej ideologii testowania się
trzymasz, zasady prywatności (*privacy*) w Ruście pozwalają testować funkcje
prywatne. Przyjrzyj się kodowi z listingu 11-12 z prywatną funkcją
`internal_adder`.

<Listing number="11-12" file-name="src/lib.rs" caption="Testowanie funkcji prywatnej">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-12/src/lib.rs}}
```

</Listing>

Zwróć uwagę, że funkcja `internal_adder` nie jest oznaczona jako `pub`. Testy
to po prostu kod w Ruście, a moduł `tests` to po prostu kolejny moduł. Jak
omówiliśmy w podrozdziale
[„Ścieżki do elementów w drzewie modułów”][paths]<!-- ignore -->,
elementy w modułach podrzędnych mogą używać elementów ze swoich przodków. W tym
teście za pomocą `use super::*` wprowadzamy do zasięgu (*scope*) wszystkie
elementy należące do rodzica modułu `tests`, dzięki czemu test może wywołać
`internal_adder`. Jeśli uważasz, że funkcji prywatnych nie należy testować, nic w
Ruście cię do tego nie zmusi.

### Testy integracyjne {#integration-tests}

W Ruście testy integracyjne są całkowicie zewnętrzne względem twojej biblioteki.
Korzystają z niej tak samo jak każdy inny kod, co oznacza, że mogą wywoływać
tylko funkcje należące do publicznego API twojej biblioteki. Ich celem jest
sprawdzenie, czy wiele części biblioteki poprawnie ze sobą współpracuje.
Jednostki kodu, które działają poprawnie samodzielnie, mogą mieć problemy po
zintegrowaniu, dlatego ważne jest też pokrycie testami zintegrowanego kodu. Aby
utworzyć testy integracyjne, potrzebujesz najpierw katalogu _tests_.

#### Katalog _tests_ {#the-tests-directory}

Tworzymy katalog _tests_ na najwyższym poziomie katalogu projektu, obok _src_.
Cargo wie, że w tym katalogu należy szukać plików z testami integracyjnymi.
Możemy w nim utworzyć dowolnie wiele plików testowych, a Cargo skompiluje każdy z
nich jako osobny *crate* (jednostka kompilacji w Ruście).

Utwórzmy test integracyjny. Mając nadal kod z listingu 11-12 w pliku
_src/lib.rs_, utwórz katalog _tests_, a w nim nowy plik o nazwie
_tests/integration_test.rs_. Struktura katalogów powinna wyglądać tak:

```text
adder
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    └── integration_test.rs
```

Wpisz kod z listingu 11-13 do pliku _tests/integration_test.rs_.

<Listing number="11-13" file-name="tests/integration_test.rs" caption="Test integracyjny funkcji z crate’a `adder`">

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-13/tests/integration_test.rs}}
```

</Listing>

Każdy plik w katalogu _tests_ jest osobnym crate’em, więc musimy wprowadzić naszą
bibliotekę do zasięgu każdego crate’a testowego. Dlatego na początku kodu
dodajemy `use adder::add_two;`, czego nie potrzebowaliśmy w testach
jednostkowych.

Nie musimy oznaczać żadnego kodu w _tests/integration_test.rs_ adnotacją
`#[cfg(test)]`. Cargo traktuje katalog _tests_ w szczególny sposób i kompiluje
pliki z tego katalogu tylko wtedy, gdy uruchamiamy `cargo test`. Uruchom teraz
`cargo test`:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-13/output.txt}}
```

Trzy sekcje wyjścia obejmują testy jednostkowe, test integracyjny i testy
dokumentacyjne. Zwróć uwagę, że jeśli któryś test w danej sekcji nie przejdzie,
kolejne sekcje nie zostaną uruchomione. Jeśli na przykład nie przejdzie test
jednostkowy, nie będzie żadnego wyjścia dla testów integracyjnych i testów
dokumentacyjnych, ponieważ są one uruchamiane tylko wtedy, gdy przechodzą wszystkie
testy jednostkowe.

Pierwsza sekcja, z testami jednostkowymi, wygląda tak samo jak dotychczas: jedna
linia dla każdego testu jednostkowego (jednego o nazwie `internal`, który
dodaliśmy w listingu 11-12), a następnie linia z podsumowaniem testów
jednostkowych.

Sekcja testów integracyjnych zaczyna się od linii
`Running tests/integration_test.rs`. Dalej jest linia dla każdej funkcji testowej w tym teście integracyjnym i
linia z podsumowaniem wyników testu integracyjnego, tuż przed początkiem sekcji
`Doc-tests adder`.

Każdy plik z testami integracyjnymi ma własną sekcję, więc jeśli dodamy więcej
plików w katalogu _tests_, pojawi się więcej sekcji testów integracyjnych.

Nadal możemy uruchomić konkretną funkcję testu integracyjnego, podając jej nazwę
jako argument `cargo test`. Aby uruchomić wszystkie testy z określonego pliku z
testami integracyjnymi, użyj argumentu `--test` polecenia `cargo test`, a po nim
podaj nazwę pliku:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-05-single-integration/output.txt}}
```

To polecenie uruchamia tylko testy z pliku _tests/integration_test.rs_.

#### Podmoduły w testach integracyjnych {#submodules-in-integration-tests}

W miarę dodawania kolejnych testów integracyjnych możesz chcieć utworzyć więcej
plików w katalogu _tests_, aby je uporządkować; możesz na przykład pogrupować
funkcje testowe według funkcjonalności, którą testują. Jak wspomnieliśmy
wcześniej, każdy plik w katalogu _tests_ jest kompilowany jako osobny crate, co
przydaje się do tworzenia oddzielnych zasięgów, wierniej naśladujących sposób,
w jaki użytkownicy końcowi będą korzystać z twojego crate’a. Oznacza to jednak,
że pliki w katalogu _tests_ nie zachowują się tak samo jak pliki w _src_, które
poznaliśmy w rozdziale 7 przy okazji rozdzielania kodu na moduły i pliki.

Odmienne zachowanie plików z katalogu _tests_ jest najbardziej widoczne, gdy
masz zestaw funkcji pomocniczych do użycia w wielu plikach z testami
integracyjnymi i próbujesz wykonać kroki z podrozdziału
[„Rozdzielanie modułów na osobne pliki”][separating-modules-into-files]<!-- ignore -->
z rozdziału 7, aby wyodrębnić je do wspólnego modułu. Jeśli na przykład
utworzymy plik _tests/common.rs_ i umieścimy w nim funkcję o nazwie `setup`,
możemy dodać do `setup` kod, który chcemy wywoływać z wielu funkcji testowych w
wielu plikach testowych:

<span class="filename">Plik: tests/common.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/tests/common.rs}}
```

Gdy ponownie uruchomimy testy, zobaczymy w wyjściu testów nową sekcję dla pliku
_common.rs_, mimo że ten plik nie zawiera żadnych funkcji testowych ani nigdzie
nie wywołaliśmy funkcji `setup`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-12-shared-test-code-problem/output.txt}}
```

Pojawienie się `common` w wynikach testów z komunikatem `running 0 tests` to nie
to, czego chcieliśmy. Chcieliśmy jedynie współdzielić trochę kodu z innymi
plikami testów integracyjnych. Aby `common` nie pojawiał się w wyjściu testów,
zamiast pliku _tests/common.rs_ utworzymy plik _tests/common/mod.rs_. Katalog
projektu wygląda teraz tak:

```text
├── Cargo.lock
├── Cargo.toml
├── src
│   └── lib.rs
└── tests
    ├── common
    │   └── mod.rs
    └── integration_test.rs
```

To starsza konwencja nazewnictwa, którą Rust również rozumie i o której
wspomnieliśmy w podrozdziale
[„Alternatywne ścieżki plików”][alt-paths]<!-- ignore --> w rozdziale 7. Taka
nazwa pliku mówi Rustowi, żeby nie traktował modułu `common` jako pliku z testami
integracyjnymi. Gdy przeniesiemy kod funkcji `setup` do _tests/common/mod.rs_ i
usuniemy plik _tests/common.rs_, sekcja w wyjściu testów przestanie się
pojawiać. Pliki w podkatalogach katalogu _tests_ nie są kompilowane jako osobne
crate’y i nie mają własnych sekcji w wyjściu testów.

Po utworzeniu _tests/common/mod.rs_ możemy używać go jako modułu w dowolnym
pliku z testami integracyjnymi. Oto przykład wywołania funkcji `setup` z testu
`it_adds_two` w _tests/integration_test.rs_:

<span class="filename">Plik: tests/integration_test.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-13-fix-shared-test-code-problem/tests/integration_test.rs}}
```

Zwróć uwagę, że deklaracja `mod common;` jest taka sama jak deklaracja modułu,
którą pokazaliśmy w listingu 7-21. Następnie w funkcji testowej możemy wywołać
funkcję `common::setup()`.

#### Testy integracyjne dla crate’ów binarnych {#integration-tests-for-binary-crates}

Jeśli nasz projekt jest crate’em binarnym, który zawiera tylko plik
_src/main.rs_ i nie ma pliku _src/lib.rs_, nie możemy utworzyć testów
integracyjnych w katalogu _tests_ i wprowadzić do zasięgu funkcji
zdefiniowanych w pliku _src/main.rs_ za pomocą instrukcji (*statement*) `use`.
Tylko crate’y biblioteczne udostępniają funkcje, których mogą używać inne
crate’y; crate’y binarne są przeznaczone do samodzielnego uruchamiania.

To jeden z powodów, dla których projekty w Ruście, które dostarczają plik
binarny, mają prosty plik _src/main.rs_ wywołujący logikę znajdującą się w pliku
_src/lib.rs_. Przy takiej strukturze testy integracyjne _mogą_ testować crate
biblioteczny, używając `use`, aby udostępnić ważną funkcjonalność. Jeśli ważna
funkcjonalność działa, to niewielka ilość kodu w pliku _src/main.rs_ również
będzie działać i nie trzeba jej testować.

## Podsumowanie {#summary}

Mechanizmy testowania w Ruście pozwalają określić, jak kod powinien działać, aby
mieć pewność, że nadal działa zgodnie z oczekiwaniami, nawet gdy wprowadzasz
zmiany. Testy jednostkowe sprawdzają osobno różne części biblioteki i mogą
testować prywatne szczegóły implementacji. Testy integracyjne sprawdzają, czy
wiele części biblioteki poprawnie ze sobą współpracuje, i testują kod za pomocą
publicznego API biblioteki w taki sam sposób, w jaki będzie go używał kod
zewnętrzny. Choć system typów i zasady własności (*ownership*) w Ruście pomagają
zapobiegać niektórym rodzajom błędów, testy nadal są ważne, aby ograniczyć błędy
logiczne związane z tym, jak twój kod ma się zachowywać.

Połączmy wiedzę zdobytą w tym i w poprzednich rozdziałach i zabierzmy się do
pracy nad projektem!

{{#quiz ../quizzes/ch11-03-test-organization.toml}}

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html
[separating-modules-into-files]: ch07-05-separating-modules-into-different-files.html
[alt-paths]: ch07-05-separating-modules-into-different-files.html#alternate-file-paths

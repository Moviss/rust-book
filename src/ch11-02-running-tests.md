## Sterowanie sposobem uruchamiania testów {#controlling-how-tests-are-run}

Tak jak `cargo run` kompiluje kod, a potem uruchamia powstały plik binarny,
tak `cargo test` kompiluje kod w trybie testowym i uruchamia powstały testowy
plik binarny. Domyślnie plik binarny utworzony przez `cargo test` uruchamia
wszystkie testy równolegle i przechwytuje wyjście generowane podczas ich
działania. Dzięki temu wyjście nie jest wyświetlane, a wyniki testów łatwiej
odczytać. Możesz jednak zmienić to domyślne zachowanie opcjami wiersza poleceń.

Część opcji wiersza poleceń trafia do `cargo test`, a część do powstałego
testowego pliku binarnego. Aby rozdzielić te dwa rodzaje argumentów, podajesz
najpierw argumenty dla `cargo test`, potem separator `--`, a po nim argumenty
dla testowego pliku binarnego. Polecenie `cargo test --help` wyświetla opcje,
których możesz użyć z `cargo test`, a `cargo test -- --help` – opcje, których
możesz użyć po separatorze. Opisano je także w
[podrozdziale „Tests” w _The `rustc` Book_][tests].

[tests]: https://doc.rust-lang.org/rustc/tests/index.html

### Uruchamianie testów równolegle lub po kolei {#running-tests-in-parallel-or-consecutively}

Gdy uruchamiasz wiele testów, domyślnie działają one równolegle w osobnych
wątkach. Dzięki temu kończą się szybciej, a ty szybciej dostajesz informację
zwrotną. Ponieważ testy działają jednocześnie, musisz zadbać o to, by nie
zależały od siebie nawzajem ani od żadnego współdzielonego stanu, w tym od
współdzielonego środowiska, takiego jak bieżący katalog roboczy czy zmienne
środowiskowe.

Załóżmy na przykład, że każdy z twoich testów uruchamia kod, który tworzy na
dysku plik o nazwie _test-output.txt_ i zapisuje w nim jakieś dane. Następnie
każdy test odczytuje dane z tego pliku i sprawdza za pomocą asercji, że plik zawiera
określoną wartość, inną w każdym teście. Ponieważ testy działają jednocześnie,
jeden test może nadpisać plik w czasie między zapisem a odczytem pliku przez
inny test. Ten drugi test zakończy się wtedy niepowodzeniem – nie dlatego, że
kod jest błędny, ale dlatego, że testy przeszkadzały sobie nawzajem, działając
równolegle. Jednym z rozwiązań jest dopilnowanie, by każdy test zapisywał do
innego pliku; innym – uruchamianie testów pojedynczo.

Jeśli nie chcesz uruchamiać testów równolegle albo chcesz dokładniej kontrolować
liczbę używanych wątków, możesz przekazać testowemu plikowi binarnemu flagę
`--test-threads` wraz z liczbą wątków, których chcesz użyć. Spójrz na
następujący przykład:

```console
$ cargo test -- --test-threads=1
```

Ustawiamy liczbę wątków testowych na `1`, co oznacza, że program ma nie
korzystać z żadnej równoległości. Uruchamianie testów w jednym wątku potrwa
dłużej niż uruchamianie ich równolegle, ale testy nie będą sobie przeszkadzać,
jeśli współdzielą stan.

### Wyświetlanie wyjścia funkcji {#showing-function-output}

Domyślnie, jeśli test przechodzi, biblioteka testowa Rusta przechwytuje
wszystko, co zostało wypisane na standardowe wyjście. Jeśli na przykład
wywołamy `println!` w teście, a test przejdzie, nie zobaczymy w terminalu
wyjścia `println!`; zobaczymy tylko linię informującą, że test przeszedł. Jeśli
test zakończy się niepowodzeniem, zobaczymy wszystko, co zostało wypisane na
standardowe wyjście, razem z resztą komunikatu o niepowodzeniu.

Na przykład w listingu 11-10 jest niemądra funkcja, która wypisuje wartość
swojego parametru i zwraca 10, a także test, który przechodzi, i test, który
kończy się niepowodzeniem.

<Listing number="11-10" file-name="src/lib.rs" caption="Testy funkcji, która wywołuje `println!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-10/src/lib.rs}}
```

</Listing>

Gdy uruchomimy te testy poleceniem `cargo test`, zobaczymy następujące wyjście:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-10/output.txt}}
```

Zauważ, że nigdzie w tym wyjściu nie widać `I got the value 4`, co jest
wypisywane podczas działania testu, który przechodzi. To wyjście zostało
przechwycone. Wyjście testu, który zakończył się niepowodzeniem,
`I got the value 8`, pojawia się w części podsumowania testów, która pokazuje
też przyczynę niepowodzenia testu.

Jeśli chcemy widzieć wypisywane wartości także dla testów, które przechodzą,
możemy kazać Rustowi pokazywać również wyjście udanych testów za pomocą
`--show-output`:

```console
$ cargo test -- --show-output
```

Gdy ponownie uruchomimy testy z listingu 11-10 z flagą `--show-output`,
zobaczymy następujące wyjście:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-01-show-output/output.txt}}
```

### Uruchamianie podzbioru testów według nazwy {#running-a-subset-of-tests-by-name}

Uruchomienie pełnego zestawu testów może czasem trwać długo. Jeśli pracujesz
nad kodem w określonym obszarze, możesz chcieć uruchomić tylko testy dotyczące
tego kodu. Możesz wybrać, które testy uruchomić, przekazując `cargo test` jako
argument nazwę lub nazwy testów, które chcesz uruchomić.

Aby pokazać, jak uruchomić podzbiór testów, najpierw utworzymy trzy testy dla
naszej funkcji `add_two`, jak w listingu 11-11, a potem wybierzemy, które z nich
uruchomić.

<Listing number="11-11" file-name="src/lib.rs" caption="Trzy testy o trzech różnych nazwach">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-11/src/lib.rs}}
```

</Listing>

Jeśli uruchomimy testy bez przekazywania argumentów, to – jak widzieliśmy
wcześniej – wszystkie testy zostaną uruchomione równolegle:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-11/output.txt}}
```

#### Uruchamianie pojedynczych testów {#running-single-tests}

Możemy przekazać `cargo test` nazwę dowolnej funkcji testowej, aby uruchomić
tylko ten test:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-02-single-test/output.txt}}
```

Uruchomiony został tylko test o nazwie `one_hundred`; pozostałe dwa testy nie
pasowały do tej nazwy. Wyjście testów informuje nas, że mieliśmy więcej testów,
które nie zostały uruchomione, wyświetlając na końcu `2 filtered out`.

W ten sposób nie da się podać nazw kilku testów; użyta zostanie tylko pierwsza
wartość przekazana do `cargo test`. Istnieje jednak sposób na uruchomienie
wielu testów.

#### Filtrowanie w celu uruchomienia wielu testów {#filtering-to-run-multiple-tests}

Możemy podać część nazwy testu, a uruchomiony zostanie każdy test, którego
nazwa pasuje do tej wartości. Ponieważ na przykład nazwy dwóch naszych testów
zawierają `add`, możemy uruchomić te dwa testy poleceniem `cargo test add`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-03-multiple-tests/output.txt}}
```

To polecenie uruchomiło wszystkie testy z `add` w nazwie i odfiltrowało test o
nazwie `one_hundred`. Zauważ też, że moduł, w którym znajduje się test, staje
się częścią nazwy testu, więc możemy uruchomić wszystkie testy w module,
filtrując po nazwie modułu.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-some-tests-unless-specifically-requested"></a>

### Ignorowanie testów, chyba że wyraźnie o nie poproszono {#ignoring-tests-unless-specifically-requested}

Czasem kilka konkretnych testów wykonuje się bardzo długo, więc możesz chcieć
wykluczyć je przy większości uruchomień `cargo test`. Zamiast wymieniać jako
argumenty wszystkie testy, które chcesz uruchomić, możesz oznaczyć
czasochłonne testy atrybutem `ignore`, aby je wykluczyć, jak tutaj:

<span class="filename">Plik: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/src/lib.rs:here}}
```

Po `#[test]` dodajemy wiersz `#[ignore]` do testu, który chcemy wykluczyć.
Teraz, gdy uruchomimy testy, `it_works` zostanie uruchomiony, ale
`expensive_test` już nie:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-11-ignore-a-test/output.txt}}
```

Funkcja `expensive_test` jest oznaczona jako `ignored`. Jeśli chcemy uruchomić
tylko zignorowane testy, możemy użyć `cargo test -- --ignored`:

```console
{{#include ../listings/ch11-writing-automated-tests/output-only-04-running-ignored/output.txt}}
```

Kontrolując, które testy są uruchamiane, możesz zadbać o to, by wyniki
`cargo test` pojawiały się szybko. Gdy dojdziesz do momentu, w którym warto
sprawdzić wyniki testów `ignored` i masz czas, by na nie poczekać, możesz
zamiast tego uruchomić `cargo test -- --ignored`. Jeśli chcesz uruchomić
wszystkie testy, niezależnie od tego, czy są zignorowane, czy nie, możesz
uruchomić `cargo test -- --include-ignored`.

{{#quiz ../quizzes/ch11-02-running-tests.toml}}

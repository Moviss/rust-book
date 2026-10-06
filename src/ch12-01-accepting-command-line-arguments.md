## Przyjmowanie argumentów wiersza poleceń {#accepting-command-line-arguments}

Jak zawsze utwórzmy nowy projekt za pomocą `cargo new`. Nazwiemy go
`minigrep`, żeby odróżnić go od narzędzia `grep`, które być może masz już w
swoim systemie:

```console
$ cargo new minigrep
     Created binary (application) `minigrep` project
$ cd minigrep
```

Pierwsze zadanie polega na tym, żeby `minigrep` przyjmował dwa argumenty
wiersza poleceń: ścieżkę do pliku i szukany łańcuch znaków (*string*). Chcemy
więc móc uruchomić nasz program poleceniem `cargo run`, po którym następują dwa
myślniki (oznaczające, że kolejne argumenty są przeznaczone dla naszego
programu, a nie dla `cargo`), szukany łańcuch i ścieżka do przeszukiwanego
pliku, na przykład tak:

```console
$ cargo run -- searchstring example-filename.txt
```

Program wygenerowany przez `cargo new` nie potrafi na razie przetwarzać
przekazywanych mu argumentów. Niektóre istniejące biblioteki w serwisie
[crates.io](https://crates.io/) mogą pomóc w pisaniu programu, który przyjmuje
argumenty wiersza poleceń, ale ponieważ dopiero poznajesz tę koncepcję,
zaimplementujmy tę możliwość samodzielnie.

### Odczytywanie wartości argumentów {#reading-the-argument-values}

Żeby `minigrep` mógł odczytać wartości przekazanych mu argumentów wiersza
poleceń, potrzebujemy funkcji `std::env::args` z biblioteki standardowej Rusta.
Funkcja ta zwraca iterator po argumentach wiersza poleceń przekazanych do
`minigrep`. Iteratory omówimy w pełni w [rozdziale 13][ch13]<!-- ignore
-->. Na razie wystarczy ci wiedza o dwóch szczegółach: iteratory wytwarzają
ciąg wartości, a na iteratorze możemy wywołać metodę `collect`, żeby zamienić
go w kolekcję, na przykład wektor (*vector*), zawierającą wszystkie elementy
wytworzone przez iterator.

Kod z listingu 12-1 pozwala programowi `minigrep` odczytać dowolne przekazane
mu argumenty wiersza poleceń, a następnie zebrać ich wartości w wektorze.

<Listing number="12-1" file-name="src/main.rs" caption="Zbieranie argumentów wiersza poleceń w wektorze i wypisywanie ich">

```rust
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-01/src/main.rs}}
```

</Listing>

Najpierw wprowadzamy moduł `std::env` do zasięgu (*scope*) za pomocą instrukcji
(*statement*) `use`, żeby móc korzystać z jego funkcji `args`. Zauważ, że
funkcja `std::env::args` jest zagnieżdżona w dwóch poziomach modułów. Jak
wspomnieliśmy w [rozdziale 7][ch7-idiomatic-use]<!-- ignore -->, gdy potrzebna
funkcja jest zagnieżdżona w więcej niż jednym module, zdecydowaliśmy się
wprowadzać do zasięgu moduł nadrzędny, a nie samą funkcję. Dzięki temu możemy
łatwo korzystać z innych funkcji z `std::env`. Jest to też mniej niejednoznaczne niż dodanie
`use std::env::args` i wywoływanie funkcji samym `args`, ponieważ `args` łatwo
pomylić z funkcją zdefiniowaną w bieżącym module.

> ### Funkcja `args` i niepoprawny Unicode {#the-args-function-and-invalid-unicode}
>
> Zwróć uwagę, że `std::env::args` wywoła panikę (*panic*), jeśli któryś z
> argumentów zawiera niepoprawny Unicode. Jeśli twój program musi przyjmować
> argumenty zawierające niepoprawny Unicode, użyj zamiast niej
> `std::env::args_os`. Ta funkcja zwraca iterator, który wytwarza wartości
> `OsString` zamiast wartości `String`. Dla uproszczenia użyliśmy tutaj
> `std::env::args`, ponieważ wartości `OsString` różnią się w zależności od
> platformy i praca z nimi jest bardziej skomplikowana niż z wartościami
> `String`.

W pierwszym wierszu `main` wywołujemy `env::args` i od razu używamy `collect`,
żeby zamienić iterator w wektor zawierający wszystkie wytworzone przez niego
wartości. Funkcji `collect` możemy użyć do tworzenia wielu rodzajów kolekcji,
dlatego jawnie podajemy typ `args`, żeby określić, że chcemy otrzymać wektor
łańcuchów. Choć w Ruście bardzo rzadko trzeba dodawać adnotacje typów,
`collect` jest jedną z funkcji, przy których często jest to konieczne, ponieważ
Rust nie potrafi wywnioskować, jakiego rodzaju kolekcji oczekujesz.

Na koniec wypisujemy wektor za pomocą makra debugującego. Uruchommy kod
najpierw bez argumentów, a potem z dwoma argumentami:

```console
{{#include ../listings/ch12-an-io-project/listing-12-01/output.txt}}
```

```console
{{#include ../listings/ch12-an-io-project/output-only-01-with-args/output.txt}}
```

Zauważ, że pierwszą wartością w wektorze jest `"target/debug/minigrep"`, czyli
nazwa naszego pliku binarnego. Odpowiada to zachowaniu listy argumentów w
języku C i pozwala programom korzystać podczas działania z nazwy, pod którą
zostały wywołane. Dostęp do nazwy programu bywa wygodny, gdy chcesz ją wypisać
w komunikatach albo zmienić działanie programu w zależności od tego, jakiego
aliasu wiersza poleceń użyto do jego wywołania. Na potrzeby tego rozdziału
zignorujemy ją jednak i zapiszemy tylko dwa potrzebne nam argumenty.

### Zapisywanie wartości argumentów w zmiennych {#saving-the-argument-values-in-variables}

Program ma już dostęp do wartości podanych jako argumenty wiersza poleceń.
Teraz musimy zapisać wartości obu argumentów w zmiennych, żeby móc ich używać
w dalszej części programu. Robimy to w listingu 12-2.

<Listing number="12-2" file-name="src/main.rs" caption="Tworzenie zmiennych przechowujących argument z zapytaniem i argument ze ścieżką do pliku">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-02/src/main.rs}}
```

</Listing>

Jak widzieliśmy przy wypisywaniu wektora, nazwa programu zajmuje pierwszą
wartość w wektorze, `args[0]`, dlatego argumenty zaczynamy od indeksu 1.
Pierwszym argumentem, który przyjmuje `minigrep`, jest szukany łańcuch, więc
referencję (*reference*) do pierwszego argumentu umieszczamy w zmiennej
`query`. Drugim argumentem będzie ścieżka do pliku, więc referencję do drugiego
argumentu umieszczamy w zmiennej `file_path`.

Tymczasowo wypisujemy wartości tych zmiennych, żeby sprawdzić, czy kod działa
zgodnie z naszymi zamiarami. Uruchommy program ponownie z argumentami `test` i
`sample.txt`:

```console
{{#include ../listings/ch12-an-io-project/listing-12-02/output.txt}}
```

Świetnie, program działa! Wartości potrzebnych nam argumentów trafiają do
właściwych zmiennych. Później dodamy obsługę błędów, żeby poradzić sobie z
pewnymi potencjalnie błędnymi sytuacjami, na przykład gdy użytkownik nie poda
żadnych argumentów. Na razie zignorujemy ten przypadek i zajmiemy się dodaniem
możliwości odczytu pliku.

[ch13]: ch13-00-functional-features.html
[ch7-idiomatic-use]: ch07-04-bringing-paths-into-scope-with-the-use-keyword.html#creating-idiomatic-use-paths

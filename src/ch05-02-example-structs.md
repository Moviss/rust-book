## Przykładowy program wykorzystujący struktury {#an-example-program-using-structs}

Aby zrozumieć, kiedy warto używać struktur (*struct*), napiszmy program, który
oblicza pole prostokąta. Zaczniemy od pojedynczych zmiennych, a potem będziemy
refaktoryzować program, aż zamiast nich będzie używał struktur.

Utwórzmy za pomocą Cargo nowy projekt binarny o nazwie _rectangles_, który
przyjmie szerokość i wysokość prostokąta podane w pikselach i obliczy jego pole.
Listing 5-8 pokazuje krótki program, który robi dokładnie to w pliku
_src/main.rs_ naszego projektu.

<Listing number="5-8" file-name="src/main.rs" caption="Obliczanie pola prostokąta o szerokości i wysokości zapisanych w osobnych zmiennych">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:all}}
```

</Listing>

Teraz uruchom ten program poleceniem `cargo run`:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/output.txt}}
```

Ten kod poprawnie oblicza pole prostokąta, wywołując funkcję `area` z każdym z
wymiarów, ale możemy zrobić więcej, aby był jasny i czytelny.

Problem z tym kodem widać w sygnaturze funkcji `area`:

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-08/src/main.rs:here}}
```

Funkcja `area` ma obliczać pole jednego prostokąta, ale napisana przez nas
funkcja ma dwa parametry i nigdzie w programie nie widać, że są one ze sobą
powiązane. Bardziej czytelne i łatwiejsze w utrzymaniu byłoby zgrupowanie
szerokości i wysokości razem. Jeden sposób, by to zrobić, omówiliśmy już w
podrozdziale [„Typ krotki”][the-tuple-type]<!-- ignore --> w rozdziale 3: użycie
krotek (*tuple*).

### Refaktoryzacja z użyciem krotek {#refactoring-with-tuples}

Listing 5-9 pokazuje inną wersję naszego programu, która korzysta z krotek.

<Listing number="5-9" file-name="src/main.rs" caption="Określenie szerokości i wysokości prostokąta za pomocą krotki">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-09/src/main.rs}}
```

</Listing>

Pod jednym względem ten program jest lepszy. Krotki pozwalają dodać trochę
struktury, a teraz przekazujemy tylko jeden argument. Pod innym względem ta
wersja jest jednak mniej jasna: krotki nie nazywają swoich elementów, więc
musimy odwoływać się do ich części przez indeksy, przez co obliczenie jest mniej
oczywiste.

Pomylenie szerokości z wysokością nie miałoby znaczenia przy obliczaniu pola,
ale gdybyśmy chcieli narysować prostokąt na ekranie, już by miało! Musielibyśmy
pamiętać, że `width` to indeks krotki `0`, a `height` to indeks krotki `1`.
Komuś innemu, kto korzystałby z naszego kodu, jeszcze trudniej byłoby to
odgadnąć i zapamiętać. Ponieważ nie wyraziliśmy w kodzie znaczenia naszych
danych, łatwiej teraz o błędy.

<!-- Old headings. Do not remove or links may break. -->

<a id="refactoring-with-structs-adding-more-meaning"></a>

### Refaktoryzacja z użyciem struktur {#refactoring-with-structs}

Struktur używamy, aby nadać danym znaczenie przez ich nazwanie. Możemy
przekształcić używaną krotkę w strukturę z nazwą dla całości oraz nazwami dla
poszczególnych części, jak pokazuje listing 5-10.

<Listing number="5-10" file-name="src/main.rs" caption="Definicja struktury `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-10/src/main.rs}}
```

</Listing>

Zdefiniowaliśmy tu strukturę i nazwaliśmy ją `Rectangle`. Wewnątrz nawiasów
klamrowych zdefiniowaliśmy pola `width` i `height`, oba typu `u32`. Następnie w
`main` utworzyliśmy konkretną instancję `Rectangle` o szerokości `30` i
wysokości `50`.

Nasza funkcja `area` ma teraz jeden parametr, który nazwaliśmy `rectangle`, a
jego typem jest niemutowalne (*immutable*) pożyczenie instancji struktury
`Rectangle`. Jak wspomnieliśmy w rozdziale 4, chcemy pożyczyć strukturę, a nie
przejąć jej na własność (*ownership*). Dzięki temu `main` zachowuje własność i
może dalej używać `rect1` – dlatego używamy `&` w sygnaturze funkcji i w
miejscu jej wywołania.

Funkcja `area` odczytuje pola `width` i `height` instancji `Rectangle` (zwróć
uwagę, że dostęp do pól pożyczonej instancji struktury nie przenosi wartości
tych pól, dlatego często spotyka się pożyczenia struktur). Sygnatura funkcji
`area` mówi teraz dokładnie to, co mamy na myśli: oblicz pole `Rectangle`,
używając jego pól `width` i `height`. Wyraża to, że szerokość i wysokość są ze
sobą powiązane, i nadaje wartościom opisowe nazwy zamiast indeksów krotki `0` i
`1`. To wygrana pod względem przejrzystości.

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-useful-functionality-with-derived-traits"></a>

### Dodawanie funkcjonalności za pomocą traitów wyprowadzonych {#adding-functionality-with-derived-traits}

Przydałaby się możliwość wypisania instancji `Rectangle` podczas debugowania
programu, aby zobaczyć wartości wszystkich jej pól. Listing 5-11 próbuje użyć
[makra `println!`][println]<!-- ignore -->, tak jak robiliśmy to w poprzednich
rozdziałach. To jednak nie zadziała.

<Listing number="5-11" file-name="src/main.rs" caption="Próba wypisania instancji `Rectangle`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/src/main.rs}}
```

</Listing>

Gdy skompilujemy ten kod, otrzymamy błąd z następującym głównym komunikatem:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:3}}
```

Makro `println!` potrafi formatować na wiele sposobów, a domyślnie nawiasy
klamrowe każą `println!` użyć formatowania zwanego `Display`: wyjścia
przeznaczonego bezpośrednio dla użytkownika końcowego. Typy prymitywne, które
dotąd poznaliśmy, domyślnie implementują `Display`, ponieważ istnieje tylko
jeden sposób, w jaki chcielibyśmy pokazać użytkownikowi `1` czy dowolną inną
wartość typu prymitywnego. W przypadku struktur sposób, w jaki `println!` ma
sformatować wyjście, jest mniej oczywisty, bo możliwości wyświetlenia jest
więcej: czy chcesz przecinki, czy nie? Czy wypisać nawiasy klamrowe? Czy pokazać
wszystkie pola? Z powodu tej niejednoznaczności Rust nie próbuje zgadywać, czego
chcemy, a struktury nie mają gotowej implementacji `Display`, której można by
użyć z `println!` i symbolem zastępczym (*placeholder*) `{}`.

Jeśli przeczytamy dalej komunikaty błędów, znajdziemy pomocną wskazówkę:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-11/output.txt:9:10}}
```

Spróbujmy! Wywołanie makra `println!` będzie teraz wyglądać tak:
`println!("rect1 is {rect1:?}");`. Umieszczenie specyfikatora `:?` w nawiasach
klamrowych mówi `println!`, że chcemy użyć formatu wyjścia zwanego `Debug`.
*Trait* (cecha typu, zbliżona do interfejsu) `Debug` pozwala wypisać strukturę w
sposób przydatny dla programistów, dzięki czemu możemy zobaczyć jej wartość
podczas debugowania kodu.

Skompiluj kod z tą zmianą. Pech! Nadal dostajemy błąd:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:3}}
```

Ale znowu kompilator daje nam pomocną wskazówkę:

```text
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-01-debug/output.txt:9:10}}
```

Rust _zawiera_ funkcjonalność wypisywania informacji diagnostycznych, ale musimy
jawnie ją włączyć, aby była dostępna dla naszej struktury. W tym celu dodajemy
atrybut zewnętrzny `#[derive(Debug)]` tuż przed definicją struktury, jak
pokazuje listing 5-12.

<Listing number="5-12" file-name="src/main.rs" caption="Dodanie atrybutu wyprowadzającego (*derive*) trait `Debug` i wypisanie instancji `Rectangle` z formatowaniem debugowania">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/src/main.rs}}
```

</Listing>

Teraz, gdy uruchomimy program, nie dostaniemy żadnych błędów i zobaczymy
następujące wyjście:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/listing-05-12/output.txt}}
```

Świetnie! Nie jest to najładniejsze wyjście, ale pokazuje wartości wszystkich
pól tej instancji, co z pewnością pomoże w debugowaniu. Przy większych
strukturach przydaje się wyjście nieco łatwiejsze do czytania; w takich
przypadkach możemy użyć w łańcuchu `println!` zapisu `{:#?}` zamiast `{:?}`. W
tym przykładzie styl `{:#?}` da następujące wyjście:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/output-only-02-pretty-debug/output.txt}}
```

Innym sposobem wypisania wartości w formacie `Debug` jest użycie
[makra `dbg!`][dbg]<!-- ignore -->. W przeciwieństwie do `println!`, które
przyjmuje referencję (*reference*), makro to przejmuje własność wyrażenia
(*expression*), wypisuje nazwę pliku i numer linii, w której w kodzie występuje
wywołanie `dbg!`, wraz z wynikową wartością tego wyrażenia, a następnie oddaje
własność tej wartości.

> Uwaga: Wywołanie makra `dbg!` wypisuje dane do standardowego strumienia błędów
> konsoli (`stderr`), w przeciwieństwie do `println!`, które wypisuje do
> standardowego strumienia wyjścia konsoli (`stdout`). Więcej o `stderr` i
> `stdout` powiemy w podrozdziale
> [„Przekierowywanie błędów na standardowe wyjście błędów” w rozdziale 12][err]<!-- ignore -->.

Oto przykład, w którym interesuje nas wartość przypisywana polu `width`, a także
wartość całej struktury w `rect1`:

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/src/main.rs}}
```

Możemy otoczyć `dbg!` wyrażenie `30 * scale`, a ponieważ `dbg!` oddaje własność
wartości wyrażenia, pole `width` otrzyma taką samą wartość, jak gdyby wywołania
`dbg!` tam nie było. Nie chcemy, aby `dbg!` przejmowało własność `rect1`, więc
w kolejnym wywołaniu używamy referencji do `rect1`. Oto jak wygląda wyjście
tego przykładu:

```console
{{#include ../listings/ch05-using-structs-to-structure-related-data/no-listing-05-dbg-macro/output.txt}}
```

Widzimy, że pierwsza część wyjścia pochodzi z linii 10 pliku _src/main.rs_, w
której debugujemy wyrażenie `30 * scale`, a jego wynikowa wartość to `60`
(formatowanie `Debug` zaimplementowane dla liczb całkowitych wypisuje tylko ich
wartość). Wywołanie `dbg!` w linii 14 pliku _src/main.rs_ wypisuje wartość
`&rect1`, czyli strukturę `Rectangle`. To wyjście korzysta z czytelnego
formatowania `Debug` typu `Rectangle`. Makro `dbg!` potrafi bardzo pomóc, gdy
próbujesz ustalić, co robi twój kod!

Oprócz traitu `Debug` Rust udostępnia szereg traitów, których możemy używać z
atrybutem `derive` i które mogą dodać przydatne zachowania do naszych własnych
typów. Te traity i ich zachowania wymienia [dodatek C][app-c]<!--
ignore -->. W rozdziale 10 omówimy, jak implementować te traity z własnym
zachowaniem oraz jak tworzyć własne traity. Istnieje też wiele atrybutów innych
niż `derive`; więcej informacji znajdziesz w
[sekcji „Attributes” w dokumentacji Rust Reference][attributes].

Nasza funkcja `area` jest bardzo wyspecjalizowana: oblicza tylko pola
prostokątów. Przydałoby się ściślej powiązać to zachowanie ze strukturą
`Rectangle`, ponieważ nie zadziała ono z żadnym innym typem. Zobaczmy, jak
możemy dalej refaktoryzować ten kod, zamieniając funkcję `area` w metodę `area`
zdefiniowaną dla typu `Rectangle`.

{{#quiz ../quizzes/ch05-02-example-structs.toml}}

[the-tuple-type]: ch03-02-data-types.html#the-tuple-type
[app-c]: appendix-03-derivable-traits.md
[println]: https://doc.rust-lang.org/std/macro.println.html
[dbg]: https://doc.rust-lang.org/std/macro.dbg.html
[err]: ch12-06-writing-to-stderr-instead-of-stdout.html
[attributes]: https://doc.rust-lang.org/reference/attributes.html

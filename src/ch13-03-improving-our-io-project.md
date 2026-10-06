## Ulepszanie naszego projektu wejścia/wyjścia {#improving-our-io-project}

Dzięki nowej wiedzy o iteratorach możemy ulepszyć projekt wejścia/wyjścia z
rozdziału 12: użyjemy iteratorów, aby fragmenty kodu stały się czytelniejsze i
bardziej zwięzłe. Zobaczmy, jak iteratory mogą ulepszyć naszą implementację
funkcji `Config::build` i funkcji `search`.

### Usuwanie `clone` za pomocą iteratora {#removing-a-clone-using-an-iterator}

W listingu 12-6 dodaliśmy kod, który przyjmował wycinek (*slice*) wartości
`String` i tworzył instancję struktury (*struct*) `Config`, indeksując wycinek i
klonując wartości, tak aby struktura `Config` była właścicielem tych wartości.
W listingu 13-17 odtworzyliśmy implementację funkcji `Config::build` w postaci
z listingu 12-23.

<Listing number="13-17" file-name="src/main.rs" caption="Odtworzenie funkcji `Config::build` z listingu 12-23">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-23-reproduced/src/main.rs:ch13}}
```

</Listing>

Wtedy napisaliśmy, żeby nie przejmować się nieefektywnymi wywołaniami `clone`,
bo w przyszłości je usuniemy. Cóż, ten moment właśnie nadszedł!

Potrzebowaliśmy tu `clone`, ponieważ w parametrze `args` mamy wycinek z
elementami `String`, a funkcja `build` nie jest właścicielem `args`. Aby zwrócić
własność (*ownership*) instancji `Config`, musieliśmy sklonować wartości z pól
`query` i `file_path` struktury `Config`, tak aby instancja `Config` mogła być
właścicielem swoich wartości.

Dzięki nowej wiedzy o iteratorach możemy zmienić funkcję `build` tak, aby
zamiast pożyczania (*borrowing*) wycinka przejmowała jako argument własność
iteratora. Zamiast kodu, który sprawdza długość wycinka i odwołuje się do
konkretnych pozycji przez indeks, użyjemy możliwości iteratora. Dzięki temu
będzie jaśniejsze, co robi funkcja `Config::build`, bo dostęp do wartości
zapewni iterator.

Gdy `Config::build` przejmie własność iteratora i przestanie używać operacji
indeksowania, które pożyczają wartości, będziemy mogli przenieść (*move*)
wartości `String` z iteratora do `Config`, zamiast wywoływać `clone` i
wykonywać nową alokację.

#### Bezpośrednie używanie zwróconego iteratora {#using-the-returned-iterator-directly}

Otwórz plik _src/main.rs_ swojego projektu wejścia/wyjścia. Powinien wyglądać
tak:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-12-24-reproduced/src/main.rs:ch13}}
```

Najpierw zmienimy początek funkcji `main` z listingu 12-24 na kod z listingu
13-18, który tym razem używa iteratora. Nie skompiluje się on, dopóki nie
zaktualizujemy również `Config::build`.

<Listing number="13-18" file-name="src/main.rs" caption="Przekazywanie wartości zwracanej przez `env::args` do `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-18/src/main.rs:here}}
```

</Listing>

Funkcja `env::args` zwraca iterator! Zamiast zbierać wartości iteratora do
wektora (*vector*), a potem przekazywać wycinek do `Config::build`, przekazujemy
teraz własność iteratora zwróconego przez `env::args` bezpośrednio do
`Config::build`.

Następnie musimy zaktualizować definicję `Config::build`. Zmieńmy sygnaturę
`Config::build` tak, aby wyglądała jak w listingu 13-19. Kod nadal się nie
skompiluje, bo musimy jeszcze zaktualizować ciało funkcji.

<Listing number="13-19" file-name="src/main.rs" caption="Aktualizowanie sygnatury `Config::build` tak, aby oczekiwała iteratora">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-19/src/main.rs:here}}
```

</Listing>

Dokumentacja biblioteki standardowej dla funkcji `env::args` pokazuje, że typem
zwracanego przez nią iteratora jest `std::env::Args` i że ten typ implementuje
*trait* (cecha typu, zbliżona do interfejsu) `Iterator` oraz zwraca wartości
`String`.

Zaktualizowaliśmy sygnaturę funkcji `Config::build` tak, że parametr `args` ma
typ generyczny (*generic type*) z ograniczeniami traitu (*trait bounds*)
`impl Iterator<Item = String>` zamiast `&[String]`. To użycie składni
`impl Trait`, którą omówiliśmy w podrozdziale
[„Używanie traitów jako parametrów”][impl-trait]<!-- ignore --> w rozdziale 10,
oznacza, że `args` może być dowolnym typem, który implementuje
trait `Iterator` i zwraca elementy typu `String`.

Ponieważ przejmujemy własność `args` i będziemy modyfikować `args`, iterując po
nim, możemy dodać słowo kluczowe (*keyword*) `mut` do specyfikacji parametru
`args`, aby uczynić go mutowalnym (*mutable*).

<!-- Old headings. Do not remove or links may break. -->

<a id="using-iterator-trait-methods-instead-of-indexing"></a>

#### Używanie metod traitu `Iterator` {#using-iterator-trait-methods}

Teraz poprawimy ciało `Config::build`. Ponieważ `args` implementuje trait
`Iterator`, wiemy, że możemy wywołać na nim metodę `next`! Listing 13-20
aktualizuje kod z listingu 12-23 tak, aby używał metody `next`.

<Listing number="13-20" file-name="src/main.rs" caption="Zmiana ciała `Config::build` tak, aby używało metod iteratora">

```rust,ignore,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-20/src/main.rs:here}}
```

</Listing>

Pamiętaj, że pierwszą wartością w wyniku `env::args` jest nazwa programu.
Chcemy ją pominąć i przejść do następnej wartości, więc najpierw wywołujemy
`next` i nic nie robimy z wartością zwracaną. Potem wywołujemy `next`, aby
uzyskać wartość, którą chcemy umieścić w polu `query` struktury `Config`. Jeśli
`next` zwróci `Some`, używamy `match`, aby wydobyć wartość. Jeśli zwróci
`None`, oznacza to, że podano za mało argumentów, i wykonujemy wczesny powrót z
wartością `Err`. To samo robimy dla wartości `file_path`.

<!-- Old headings. Do not remove or links may break. -->

<a id="making-code-clearer-with-iterator-adapters"></a>

### Poprawianie czytelności kodu za pomocą adapterów iteratora {#clarifying-code-with-iterator-adapters}

Iteratory możemy wykorzystać także w funkcji `search` naszego projektu
wejścia/wyjścia. Odtworzyliśmy ją tutaj w listingu 13-21 w postaci z listingu
12-19.

<Listing number="13-21" file-name="src/lib.rs" caption="Implementacja funkcji `search` z listingu 12-19">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:ch13}}
```

</Listing>

Ten kod możemy napisać zwięźlej, używając metod będących adapterami iteratora
(*iterator adapters*). Pozwala to też uniknąć mutowalnego wektora pośredniego
`results`. Styl programowania funkcyjnego preferuje minimalizowanie ilości
mutowalnego stanu, aby kod był czytelniejszy. Usunięcie mutowalnego stanu może
w przyszłości umożliwić ulepszenie polegające na równoległym wyszukiwaniu, bo
nie musielibyśmy zarządzać współbieżnym dostępem do wektora `results`. Listing
13-22 pokazuje tę zmianę.

<Listing number="13-22" file-name="src/lib.rs" caption="Używanie metod będących adapterami iteratora w implementacji funkcji `search`">

```rust,ignore
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-22/src/lib.rs:here}}
```

</Listing>

Przypomnij sobie, że celem funkcji `search` jest zwrócenie wszystkich wierszy z
`contents`, które zawierają `query`. Podobnie jak przykład z `filter` w
listingu 13-16, ten kod używa adaptera `filter`, aby zachować tylko te wiersze,
dla których `line.contains(query)` zwraca `true`. Następnie za pomocą `collect`
zbieramy pasujące wiersze do innego wektora. Znacznie prościej! Możesz
wprowadzić analogiczną zmianę, aby używać metod iteratora również w funkcji
`search_case_insensitive`.

Jako dalsze ulepszenie zwracaj iterator z funkcji `search`: usuń wywołanie
`collect` i zmień typ zwracany na `impl Iterator<Item = &'a str>`, tak aby
funkcja stała się adapterem iteratora. Pamiętaj, że trzeba będzie też
zaktualizować testy! Przeszukaj duży plik za pomocą narzędzia `minigrep` przed
tą zmianą i po niej, aby zaobserwować różnicę w zachowaniu. Przed zmianą
program nie wypisze żadnych wyników, dopóki nie zbierze ich wszystkich, ale po
zmianie wyniki będą wypisywane w miarę znajdowania kolejnych pasujących
wierszy, bo pętla `for` w funkcji `run` może skorzystać z leniwości iteratora.

<!-- Old headings. Do not remove or links may break. -->

<a id="choosing-between-loops-or-iterators"></a>

### Wybór między pętlami a iteratorami {#choosing-between-loops-and-iterators}

Następne logiczne pytanie brzmi: który styl wybrać we własnym kodzie i
dlaczego – oryginalną implementację z listingu 13-21 czy wersję z iteratorami z
listingu 13-22 (zakładając, że zbieramy wszystkie wyniki przed ich zwróceniem,
a nie zwracamy iteratora)? Większość programistów Rusta woli styl
iteratorowy. Na początku trochę trudniej go opanować, ale gdy już wyczujesz
różne adaptery iteratora i to, co robią, iteratory mogą okazać się łatwiejsze
do zrozumienia. Zamiast majstrować przy różnych elementach pętli i budowaniu
nowych wektorów, kod skupia się na wysokopoziomowym celu pętli. Pozwala to
ukryć część rutynowego kodu, dzięki czemu łatwiej dostrzec koncepcje
charakterystyczne dla tego kodu, takie jak warunek filtrowania, który musi
spełnić każdy element iteratora.

Czy jednak obie implementacje są naprawdę równoważne? Intuicja może
podpowiadać, że niskopoziomowa pętla będzie szybsza. Porozmawiajmy o
wydajności.

[impl-trait]: ch10-02-traits.html#traits-as-parameters

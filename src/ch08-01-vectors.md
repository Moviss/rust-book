## Przechowywanie list wartości w wektorach {#storing-lists-of-values-with-vectors}

Pierwszym typem kolekcji, któremu się przyjrzymy, jest `Vec<T>`, czyli wektor
(*vector*). Wektory pozwalają przechowywać więcej niż jedną wartość w jednej
strukturze danych, która umieszcza wszystkie wartości w pamięci obok siebie.
Wektory mogą przechowywać wyłącznie wartości tego samego typu. Przydają się, gdy
masz listę elementów, na przykład wiersze tekstu w pliku albo ceny produktów w
koszyku sklepowym.

### Tworzenie nowego wektora {#creating-a-new-vector}

Żeby utworzyć nowy, pusty wektor, wywołujemy funkcję `Vec::new`, jak pokazuje
listing 8-1.

<Listing number="8-1" caption="Tworzenie nowego, pustego wektora na wartości typu `i32`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-01/src/main.rs:here}}
```

</Listing>

Zwróć uwagę, że dodaliśmy tu adnotację typu. Ponieważ nie wstawiamy do tego
wektora żadnych wartości, Rust nie wie, jakiego rodzaju elementy zamierzamy w nim
przechowywać. To ważna kwestia. Wektory są zaimplementowane za pomocą typów
generycznych (*generics*); jak używać typów generycznych z własnymi typami,
omówimy w rozdziale 10. Na razie wystarczy wiedzieć, że typ `Vec<T>`
udostępniany przez bibliotekę standardową może przechowywać dowolny typ. Gdy
tworzymy wektor do przechowywania określonego typu, możemy podać ten typ w
nawiasach ostrych. W listingu 8-1 poinformowaliśmy Rusta, że `Vec<T>` w `v`
będzie przechowywać elementy typu `i32`.

Częściej będziesz tworzyć `Vec<T>` z wartościami początkowymi, a Rust sam
wywnioskuje typ wartości, które chcesz przechowywać, więc ta adnotacja typu
rzadko jest potrzebna. Rust wygodnie udostępnia makro `vec!`, które tworzy nowy
wektor zawierający podane mu wartości. Listing 8-2 tworzy nowy `Vec<i32>`
zawierający wartości `1`, `2` i `3`. Typ całkowity to `i32`, ponieważ jest to
domyślny typ liczb całkowitych, o czym mówiliśmy w podrozdziale
[„Typy danych”][data-types]<!-- ignore --> w rozdziale 3.

<Listing number="8-2" caption="Tworzenie nowego wektora zawierającego wartości">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-02/src/main.rs:here}}
```

</Listing>

Ponieważ podaliśmy początkowe wartości typu `i32`, Rust może wywnioskować, że
typem `v` jest `Vec<i32>`, i adnotacja typu nie jest potrzebna. Teraz
przyjrzymy się temu, jak modyfikować wektor.

### Aktualizowanie wektora {#updating-a-vector}

Żeby utworzyć wektor, a potem dodać do niego elementy, możemy użyć metody
`push`, jak pokazuje listing 8-3.

<Listing number="8-3" caption="Dodawanie wartości do wektora za pomocą metody `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-03/src/main.rs:here}}
```

</Listing>

Jak w przypadku każdej zmiennej, jeśli chcemy mieć możliwość zmiany jej
wartości, musimy uczynić ją mutowalną (*mutable*) za pomocą słowa kluczowego
(*keyword*) `mut`, jak omówiliśmy w rozdziale 3. Wszystkie liczby, które w nim
umieszczamy, są typu `i32`, a Rust wnioskuje to z danych, więc nie potrzebujemy
adnotacji `Vec<i32>`.

### Odczytywanie elementów wektorów {#reading-elements-of-vectors}

Do wartości przechowywanej w wektorze można odwołać się na dwa sposoby: przez
indeksowanie albo za pomocą metody `get`. W poniższych przykładach dla większej
przejrzystości dodaliśmy adnotacje typów wartości zwracanych przez te funkcje.

Listing 8-4 pokazuje oba sposoby dostępu do wartości w wektorze: składnię
indeksowania i metodę `get`.

<Listing number="8-4" caption="Dostęp do elementu wektora za pomocą składni indeksowania i za pomocą metody `get`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-04/src/main.rs:here}}
```

</Listing>

Zwróć tu uwagę na kilka szczegółów. Używamy indeksu `2`, żeby pobrać trzeci
element, ponieważ wektory są indeksowane liczbami, zaczynając od zera. Użycie
`&` i `[]` daje nam referencję (*reference*) do elementu o danym indeksie. Gdy
używamy metody `get` z indeksem przekazanym jako argument, otrzymujemy
`Option<&T>`, którego możemy użyć z `match`.

Rust udostępnia te dwa sposoby odwoływania się do elementu, żeby można było
wybrać, jak program ma się zachować przy próbie użycia indeksu spoza zakresu
istniejących elementów. Zobaczmy na przykład, co się stanie, gdy mamy wektor
pięciu elementów i spróbujemy każdą z tych technik odczytać element o indeksie
100, jak pokazuje listing 8-5.

<Listing number="8-5" caption="Próba dostępu do elementu o indeksie 100 w wektorze zawierającym pięć elementów">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-05/src/main.rs:here}}
```

</Listing>

Gdy uruchomimy ten kod, pierwszy sposób, z `[]`, wywoła panikę (*panic*)
programu, ponieważ odwołuje się do nieistniejącego elementu. Tego sposobu
najlepiej używać wtedy, gdy program ma się zakończyć awarią przy próbie dostępu
do elementu poza końcem wektora.

Gdy metodzie `get` przekażemy indeks spoza wektora, zwraca ona `None` bez
panikowania. Tej metody użyjesz, jeśli dostęp do elementu spoza zakresu wektora
może się od czasu do czasu zdarzyć w normalnych warunkach. Twój kod będzie
wtedy zawierał logikę obsługującą zarówno `Some(&element)`, jak i `None`, jak
omówiliśmy w rozdziale 6. Indeks może na przykład pochodzić od osoby, która
wpisuje liczbę. Jeśli przypadkiem wpisze zbyt dużą liczbę, a program otrzyma
wartość `None`, możesz poinformować użytkownika, ile elementów jest w bieżącym
wektorze, i dać mu kolejną szansę na wpisanie poprawnej wartości. Byłoby to
bardziej przyjazne dla użytkownika niż zakończenie programu awarią z powodu
literówki!

Gdy program ma poprawną referencję, *borrow checker* (mechanizm sprawdzania
pożyczeń) egzekwuje zasady własności (*ownership*) i pożyczania (*borrowing*),
omówione w rozdziale 4, żeby zapewnić, że ta referencja i wszelkie inne
referencje do zawartości wektora pozostaną poprawne. Przypomnij sobie zasadę,
zgodnie z którą w tym samym zasięgu (*scope*) nie można mieć jednocześnie
referencji mutowalnych i niemutowalnych. Ta zasada ma zastosowanie w listingu
8-6, gdzie trzymamy niemutowalną referencję do pierwszego elementu wektora i
próbujemy dodać element na jego koniec. Ten program nie zadziała, jeśli dalej w
funkcji spróbujemy jeszcze odwołać się do tego elementu.

<Listing number="8-6" caption="Próba dodania elementu do wektora przy jednoczesnym trzymaniu referencji do jednego z jego elementów">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-06/src/main.rs:here}}
```

</Listing>

Kompilacja tego kodu zakończy się takim błędem:

```console
{{#include ../listings/ch08-common-collections/listing-08-06/output.txt}}
```

Kod z listingu 8-6 może wyglądać tak, jakby powinien działać: dlaczego
referencję do pierwszego elementu miałyby obchodzić zmiany na końcu wektora? Ten
błąd wynika ze sposobu działania wektorów. Ponieważ wektory umieszczają wartości
w pamięci obok siebie, dodanie nowego elementu na koniec wektora może wymagać
zaalokowania nowej pamięci i skopiowania starych elementów w nowe miejsce, jeśli
tam, gdzie wektor jest obecnie przechowywany, nie ma dość miejsca, by umieścić
wszystkie elementy obok siebie. W takim przypadku referencja do pierwszego
elementu wskazywałaby na zdealokowaną pamięć. Zasady pożyczania nie pozwalają,
by program znalazł się w takiej sytuacji.

> Uwaga: więcej o szczegółach implementacji typu `Vec<T>` znajdziesz w
> [„The Rustonomicon”][nomicon].

### Iterowanie po wartościach w wektorze {#iterating-over-the-values-in-a-vector}

Żeby po kolei uzyskać dostęp do każdego elementu wektora, iterujemy po
wszystkich elementach, zamiast używać indeksów, by sięgać do nich pojedynczo.
Listing 8-7 pokazuje, jak za pomocą pętli `for` uzyskać niemutowalne referencje
do każdego elementu wektora wartości `i32` i je wypisać.

<Listing number="8-7" caption="Wypisywanie każdego elementu wektora przez iterowanie po elementach w pętli `for`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-07/src/main.rs:here}}
```

</Listing>

Żeby odczytać liczbę, na którą wskazuje `i`, musimy użyć operatora dereferencji (*dereference*) `*`, by dostać się do wartości w `i`, zanim dodamy do niej 1, jak omówiliśmy w podrozdziale [„Dereferencja wskaźnika daje dostęp do jego danych”][deref].

Możemy też iterować po mutowalnych referencjach do każdego elementu
mutowalnego wektora, żeby zmienić wszystkie elementy. Pętla `for` w listingu
8-8 doda `50` do każdego elementu.

<Listing number="8-8" caption="Iterowanie po mutowalnych referencjach do elementów wektora">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-08/src/main.rs:here}}
```

</Listing>

Żeby zmienić wartość, na którą wskazuje mutowalna referencja, znowu używamy operatora dereferencji `*`, by dostać się do wartości w `i`, zanim użyjemy operatora `+=`. 

{{#quiz ../quizzes/ch08-01-vec-sec1.toml}}

### Bezpieczne używanie iteratorów {#safely-using-iterators}

Więcej o tym, jak działają iteratory, powiemy w podrozdziale 13.2 [„Przetwarzanie serii elementów za pomocą iteratorów”](ch13-02-iterators.html).
Na razie ważne jest to, że iteratory zawierają wskaźnik do danych wewnątrz wektora. Działanie
iteratorów zobaczymy, rozpisując pętlę for na odpowiadające jej wywołania metod [`Vec::iter`] i [`Iterator::next`]:

```aquascope,interpreter,horizontal
#fn main() {
#use std::slice::Iter;  
let mut v: Vec<i32>         = vec![1, 2];
let mut iter: Iter<'_, i32> = v.iter();`[]`
let n1: &i32                = iter.next().unwrap();`[]`
let n2: &i32                = iter.next().unwrap();`[]`
let end: Option<&i32>       = iter.next();`[]`
#}
```

Zauważ, że iterator `iter` jest wskaźnikiem, który przesuwa się po kolejnych elementach wektora. Metoda `next` przesuwa
iterator i zwraca opcjonalną referencję do poprzedniego elementu: albo `Some` (które rozpakowujemy), albo `None` na końcu wektora.

Ten szczegół ma znaczenie dla bezpiecznego używania wektorów. Załóżmy na przykład, że chcemy zduplikować wektor w miejscu, tak by `[1, 2]` zmienił się w `[1, 2, 1, 2]`.
Naiwna implementacja mogłaby wyglądać tak; adnotacje pokazują uprawnienia (*permission*) wywnioskowane przez kompilator:

```aquascope,permissions,stepper,boundaries,shouldFail
fn dup_in_place(v: &mut Vec<i32>) {
    for n_ref in v.iter() {`(focus,paths:*v)`
        v.push(*n_ref);`{}`
    }
}
```

Zauważ, że `v.iter()` odbiera `*v` uprawnienie @Perm{write}. W związku z tym operacji `v.push(..)` brakuje oczekiwanego uprawnienia @Perm{write}. Kompilator Rusta odrzuci ten program z odpowiednim komunikatem o błędzie:

```text
error[E0502]: cannot borrow `*v` as mutable because it is also borrowed as immutable
 --> test.rs:3:9
  |
2 |     for n_ref in v.iter() {
  |                  --------
  |                  |
  |                  immutable borrow occurs here
  |                  immutable borrow later used here
3 |         v.push(*n_ref);
  |         ^^^^^^^^^^^^^^ mutable borrow occurs here
```

Jak omówiliśmy w rozdziale 4, problemem bezpieczeństwa kryjącym się za tym błędem jest odczyt zdealokowanej pamięci. Gdy tylko wykona się `v.push(1)`, wektor realokuje swoją zawartość i unieważni wskaźnik iteratora. Dlatego, żeby iteratory dało się używać bezpiecznie, Rust nie pozwala dodawać elementów do wektora ani ich z niego usuwać w trakcie iteracji.

<!-- TODO: add loop support and make this diagram look reasonable -->
<!-- ```aquascope,interpreter,shouldFail,horizontal
fn dup_in_place(v: &mut Vec<i32>) {`[]`
    for n_ref in v.iter() {
        v.push(*n_ref);
    }`[]`
}
fn main() {
    let mut v = vec![1, 2, 3];
    dup_in_place(&mut v);
}
``` -->

Jednym ze sposobów iterowania po wektorze bez użycia wskaźnika jest zakres (*range*), podobnie jak przy wycinkach łańcucha (*string slice*) w [podrozdziale 4.4](ch04-04-slices.html#range-syntax). Na przykład zakres `0 .. v.len()` jest iteratorem po wszystkich indeksach wektora `v`, jak widać tutaj:

```aquascope,interpreter,horizontal
#fn main() {
#use std::ops::Range; 
let mut v: Vec<i32>        = vec![1, 2];
let mut iter: Range<usize> = 0 .. v.len();`[]`
let i1: usize              = iter.next().unwrap();
let n1: &i32               = &v[i1];`[]`
#}
```

### Przechowywanie wielu typów za pomocą enuma {#using-an-enum-to-store-multiple-types}

Wektory mogą przechowywać wyłącznie wartości tego samego typu. Bywa to
niewygodne; z pewnością zdarzają się sytuacje, w których trzeba przechowywać
listę elementów różnych typów. Na szczęście warianty *enuma* (typu
wyliczeniowego) są zdefiniowane w ramach tego samego typu enuma, więc gdy
potrzebujemy jednego typu do reprezentowania elementów różnych typów, możemy
zdefiniować enum i go użyć!

Załóżmy na przykład, że chcemy pobrać wartości z wiersza arkusza
kalkulacyjnego, w którym niektóre kolumny zawierają liczby całkowite, inne
liczby zmiennoprzecinkowe, a jeszcze inne łańcuchy znaków (*string*). Możemy
zdefiniować enum, którego warianty będą przechowywać wartości różnych typów, a
wszystkie warianty enuma będą traktowane jako ten sam typ: typ enuma. Następnie
możemy utworzyć wektor przechowujący ten enum, a więc ostatecznie przechowujący
różne typy. Pokazaliśmy to w listingu 8-9.

<Listing number="8-9" caption="Definiowanie enuma do przechowywania wartości różnych typów w jednym wektorze">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-09/src/main.rs:here}}
```

</Listing>

Rust musi wiedzieć w czasie kompilacji (*compile-time*), jakie typy znajdą się w
wektorze, żeby wiedzieć dokładnie, ile pamięci na stercie (*heap*) będzie
potrzebne do przechowania każdego elementu. Musimy też jawnie określić, jakie
typy są dozwolone w tym wektorze. Gdyby Rust pozwalał wektorowi przechowywać
dowolny typ, mogłoby się zdarzyć, że jeden lub więcej typów spowoduje błędy w
operacjach wykonywanych na elementach wektora. Użycie enuma wraz z wyrażeniem
(*expression*) `match` oznacza, że Rust w czasie kompilacji upewni się, że
obsłużono każdy możliwy przypadek, jak omówiliśmy w rozdziale 6.

Jeśli nie znasz wyczerpującego (*exhaustive*) zbioru typów, które program
otrzyma w czasie działania i będzie przechowywać w wektorze, technika z enumem
nie zadziała. Zamiast niej możesz użyć obiektu traitu (*trait object*), który
omówimy w rozdziale 18.

Skoro omówiliśmy już kilka najczęstszych sposobów używania wektorów, koniecznie
przejrzyj [dokumentację API][vec-api]<!-- ignore -->, w której znajdziesz
wszystkie liczne przydatne metody zdefiniowane dla `Vec<T>` w bibliotece
standardowej. Na przykład oprócz `push` istnieje metoda `pop`, która usuwa i
zwraca ostatni element.

### Zwolnienie wektora zwalnia jego elementy {#dropping-a-vector-drops-its-elements}

Jak każda inna `struct`, wektor zostaje zwolniony, gdy wychodzi poza zasięg, co
zaznaczyliśmy w listingu 8-10.

<Listing number="8-10" caption="Miejsca, w których zwalniany jest wektor i jego elementy">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-10/src/main.rs:here}}
```

</Listing>

Gdy wektor zostaje zwolniony (*drop*), zwolniona zostaje też cała jego
zawartość, co oznacza, że przechowywane w nim liczby całkowite zostaną
uprzątnięte. *Borrow checker* dba o to, by wszelkie referencje do zawartości
wektora były używane tylko wtedy, gdy sam wektor jest poprawny.

Przejdźmy do następnego typu kolekcji: `String`!

{{#quiz ../quizzes/ch08-01-vec-sec2.toml}}

[data-types]: ch03-02-data-types.html#data-types
[nomicon]: https://doc.rust-lang.org/nomicon/vec/vec.html
[vec-api]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[deref]: ch04-02-references-and-borrowing.html#dereferencing-a-pointer-accesses-its-data
[`Vec::iter`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.iter
[`Iterator::next`]: https://doc.rust-lang.org/std/iter/trait.Iterator.html#tymethod.next

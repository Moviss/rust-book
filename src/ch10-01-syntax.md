## Generyczne typy danych {#generic-data-types}

Typów generycznych (*generics*) używamy do tworzenia definicji elementów, takich
jak sygnatury funkcji czy struktury (*struct*), których możemy potem używać z
wieloma różnymi konkretnymi typami danych. Najpierw zobaczymy, jak definiować
funkcje, struktury, *enumy* (typy wyliczeniowe) i metody z użyciem typów
generycznych. Potem omówimy, jak typy generyczne wpływają na wydajność kodu.

### W definicjach funkcji {#in-function-definitions}

Definiując funkcję korzystającą z typów generycznych, umieszczamy je w
sygnaturze funkcji tam, gdzie zwykle podalibyśmy typy danych parametrów i
wartości zwracanej. Dzięki temu nasz kod jest bardziej elastyczny i daje więcej
możliwości kodowi wywołującemu naszą funkcję, a jednocześnie unikamy powielania
kodu.

Kontynuując przykład z funkcją `largest`, listing 10-4 pokazuje dwie funkcje,
które znajdują największą wartość w wycinku (*slice*). Następnie połączymy je w
jedną funkcję korzystającą z typów generycznych.

<Listing number="10-4" file-name="src/main.rs" caption="Dwie funkcje, które różnią się tylko nazwami i typami w sygnaturach">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-04/src/main.rs:here}}
```

</Listing>

Funkcja `largest_i32` to ta, którą wyodrębniliśmy w listingu 10-3; znajduje
największą wartość `i32` w wycinku. Funkcja `largest_char` znajduje największą
wartość `char` w wycinku. Ciała obu funkcji zawierają ten sam kod, więc
usuńmy powielenie, wprowadzając generyczny parametr typu w jednej funkcji.

Aby sparametryzować typy w nowej, pojedynczej funkcji, musimy nazwać parametr
typu, tak jak nazywamy parametry wartości funkcji. Jako nazwy parametru typu
możesz użyć dowolnego identyfikatora. My użyjemy jednak `T`, ponieważ zgodnie z
konwencją nazwy parametrów typu w Ruście są krótkie, często jednoliterowe, a
konwencja nazewnictwa typów w Ruście to UpperCamelCase. `T`, skrót od _type_
(typ), to domyślny wybór większości programistów Rusta.

Gdy używamy parametru w ciele funkcji, musimy zadeklarować jego nazwę w
sygnaturze, aby kompilator wiedział, co ta nazwa oznacza. Podobnie, gdy używamy
nazwy parametru typu w sygnaturze funkcji, musimy ją zadeklarować, zanim jej
użyjemy. Aby zdefiniować generyczną funkcję `largest`, umieszczamy deklaracje
nazw typów w nawiasach ostrych, `<>`, między nazwą funkcji a listą parametrów,
w ten sposób:

```rust,ignore
fn largest<T>(list: &[T]) -> &T {
```

Tę definicję czytamy tak: „Funkcja `largest` jest generyczna względem pewnego
typu `T`”. Funkcja ma jeden parametr o nazwie `list`, który jest wycinkiem
wartości typu `T`. Funkcja `largest` zwróci referencję (*reference*) do wartości
tego samego typu `T`.

Listing 10-5 pokazuje połączoną definicję funkcji `largest`, która używa w
sygnaturze generycznego typu danych. Listing pokazuje też, jak możemy wywołać tę
funkcję z wycinkiem wartości `i32` albo wartości `char`. Zwróć uwagę, że ten kod
jeszcze się nie skompiluje.

<Listing number="10-5" file-name="src/main.rs" caption="Funkcja `largest` z generycznymi parametrami typu; jeszcze się nie kompiluje">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/src/main.rs}}
```

</Listing>

Jeśli teraz skompilujemy ten kod, otrzymamy taki błąd:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-05/output.txt}}
```

<!-- BEGIN INTERVENTION: 0aad53ff-89d7-4d14-8e3d-c17809220252 -->
Problem polega na tym, że gdy `largest` przyjmuje na wejściu wycinek `&[T]`, funkcja nie może zakładać *niczego* o typie `T`. Może to być `i32`, może to być `String`, może to być [`File`](https://doc.rust-lang.org/std/fs/struct.File.html). Tymczasem `largest` wymaga, aby `T` dało się porównywać za pomocą `>` (tzn. aby `T` implementował `PartialOrd`, *trait* (cecha typu, zbliżona do interfejsu), który omówimy w następnym podrozdziale). Niektóre typy, takie jak `i32` i `String`, są porównywalne, ale inne, takie jak `File`, nie są.

W języku takim jak C++ z [szablonami](https://en.cppreference.com/w/cpp/language/templates) kompilator nie miałby zastrzeżeń do implementacji `largest`, ale zgłosiłby błąd przy próbie wywołania `largest` np. na wycinku plików `&[File]`. Rust wymaga natomiast, aby oczekiwane możliwości typów generycznych określić z góry. Jeśli `T` musi być porównywalny, to `largest` musi to wyrazić. Dlatego ten błąd kompilatora mówi, że `largest` się nie skompiluje, dopóki `T` nie zostanie ograniczony.

Ponadto, w odróżnieniu od języków takich jak Java, w których wszystkie obiekty mają zestaw podstawowych metod, takich jak [`Object.toString()`](https://docs.oracle.com/javase/7/docs/api/java/lang/Object.html#toString()), w Ruście nie ma podstawowych metod. Bez ograniczeń typ generyczny `T` nie ma żadnych możliwości: nie można go wypisać, sklonować ani zmodyfikować (choć można go zwolnić (*drop*)).
<!-- END INTERVENTION -->

### W definicjach struktur {#in-struct-definitions}

Struktury również możemy zdefiniować tak, aby w jednym lub kilku polach używały
generycznego parametru typu, korzystając ze składni `<>`. Listing 10-6
definiuje strukturę `Point<T>` przechowującą współrzędne `x` i `y` dowolnego
typu.

<Listing number="10-6" file-name="src/main.rs" caption="Struktura `Point<T>` przechowująca wartości `x` i `y` typu `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-06/src/main.rs}}
```

</Listing>

Składnia użycia typów generycznych w definicjach struktur jest podobna do tej w
definicjach funkcji. Najpierw deklarujemy nazwę parametru typu w nawiasach
ostrych zaraz po nazwie struktury. Następnie używamy typu generycznego w
definicji struktury tam, gdzie w przeciwnym razie podalibyśmy konkretne typy
danych.

Zwróć uwagę, że ponieważ do zdefiniowania `Point<T>` użyliśmy tylko jednego typu
generycznego, ta definicja mówi, że struktura `Point<T>` jest generyczna
względem pewnego typu `T`, a pola `x` i `y` są _obydwa_ tego samego typu,
jakikolwiek by on był. Jeśli utworzymy instancję `Point<T>` z wartościami
różnych typów, jak w listingu 10-7, nasz kod się nie skompiluje.

<Listing number="10-7" file-name="src/main.rs" caption="Pola `x` i `y` muszą być tego samego typu, ponieważ oba mają ten sam generyczny typ danych `T`.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/src/main.rs}}
```

</Listing>

Gdy w tym przykładzie przypisujemy do `x` wartość całkowitą `5`, informujemy
kompilator, że typ generyczny `T` będzie dla tej instancji `Point<T>` liczbą
całkowitą. Następnie, gdy podajemy `4.0` dla `y`, które zdefiniowaliśmy jako
pole tego samego typu co `x`, otrzymamy błąd niezgodności typów taki jak ten:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-07/output.txt}}
```

Aby zdefiniować strukturę `Point`, w której `x` i `y` są typami generycznymi,
ale mogą mieć różne typy, możemy użyć wielu generycznych parametrów typu. Na
przykład w listingu 10-8 zmieniamy definicję `Point` tak, aby była generyczna
względem typów `T` i `U`, gdzie `x` jest typu `T`, a `y` typu `U`.

<Listing number="10-8" file-name="src/main.rs" caption="Struktura `Point<T, U>` generyczna względem dwóch typów, dzięki czemu `x` i `y` mogą być wartościami różnych typów">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-08/src/main.rs}}
```

</Listing>

Teraz wszystkie pokazane instancje `Point` są dozwolone! W definicji możesz użyć
dowolnie wielu generycznych parametrów typu, ale więcej niż kilka sprawia, że
kod staje się trudny do czytania. Jeśli okazuje się, że potrzebujesz w kodzie
wielu typów generycznych, może to oznaczać, że kod wymaga podzielenia na
mniejsze części.

### W definicjach enumów {#in-enum-definitions}

Podobnie jak w przypadku struktur, możemy definiować enumy, które przechowują w
swoich wariantach generyczne typy danych. Spójrzmy jeszcze raz na enum
`Option<T>` dostarczany przez bibliotekę standardową, którego używaliśmy w
rozdziale 6:

```rust
enum Option<T> {
    Some(T),
    None,
}
```

Ta definicja powinna być teraz dla ciebie bardziej zrozumiała. Jak widać, enum
`Option<T>` jest generyczny względem typu `T` i ma dwa warianty: `Some`, który
przechowuje jedną wartość typu `T`, oraz wariant `None`, który nie przechowuje
żadnej wartości. Za pomocą enuma `Option<T>` możemy wyrazić abstrakcyjne
pojęcie wartości opcjonalnej, a ponieważ `Option<T>` jest generyczny, możemy
korzystać z tej abstrakcji bez względu na typ wartości opcjonalnej.

Enumy również mogą używać wielu typów generycznych. Przykładem jest definicja
enuma `Result`, którego używaliśmy w rozdziale 9:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Enum `Result` jest generyczny względem dwóch typów, `T` i `E`, i ma dwa
warianty: `Ok`, który przechowuje wartość typu `T`, oraz `Err`, który
przechowuje wartość typu `E`. Dzięki tej definicji wygodnie jest używać enuma
`Result` wszędzie tam, gdzie operacja może się powieść (zwrócić wartość
pewnego typu `T`) albo nie powieść (zwrócić błąd pewnego typu `E`). Właśnie
tego użyliśmy do otwarcia pliku w listingu 9-3, gdzie za `T` podstawiony został
typ `std::fs::File`, gdy plik otwarto pomyślnie, a za `E` typ
`std::io::Error`, gdy przy otwieraniu pliku wystąpiły problemy.

Gdy rozpoznasz w swoim kodzie sytuacje z wieloma definicjami struktur lub
enumów, które różnią się tylko typami przechowywanych wartości, możesz uniknąć
powielania, używając zamiast tego typów generycznych.

### W definicjach metod {#in-method-definitions}

Możemy implementować metody na strukturach i enumach (jak w rozdziale 5) i
również w ich definicjach używać typów generycznych. Listing 10-9 pokazuje
strukturę `Point<T>` zdefiniowaną w listingu 10-6 z zaimplementowaną na niej
metodą o nazwie `x`.

<Listing number="10-9" file-name="src/main.rs" caption="Implementacja metody o nazwie `x` na strukturze `Point<T>`, która zwraca referencję do pola `x` typu `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-09/src/main.rs}}
```

</Listing>

Zdefiniowaliśmy tu na `Point<T>` metodę o nazwie `x`, która zwraca referencję
do danych w polu `x`.

Zwróć uwagę, że musimy zadeklarować `T` zaraz po `impl`, aby móc użyć `T` do
określenia, że implementujemy metody na typie `Point<T>`. Dzięki zadeklarowaniu
`T` jako typu generycznego po `impl` Rust może rozpoznać, że typ w nawiasach
ostrych w `Point` jest typem generycznym, a nie konkretnym. Moglibyśmy wybrać
dla tego parametru generycznego inną nazwę niż dla parametru generycznego
zadeklarowanego w definicji struktury, ale przyjęło się używać tej samej nazwy.
Jeśli napiszesz metodę w bloku `impl`, który deklaruje typ generyczny, ta metoda
zostanie zdefiniowana na każdej instancji typu, niezależnie od tego, jaki
konkretny typ zostanie ostatecznie podstawiony za typ generyczny.

Definiując metody na typie, możemy też określić ograniczenia dla typów
generycznych. Moglibyśmy na przykład zaimplementować metody tylko na instancjach
`Point<f32>`, a nie na instancjach `Point<T>` z dowolnym typem generycznym. W
listingu 10-10 używamy konkretnego typu `f32`, co oznacza, że po `impl` nie
deklarujemy żadnych typów.

<Listing number="10-10" file-name="src/main.rs" caption="Blok `impl`, który dotyczy tylko struktury z określonym konkretnym typem w miejscu generycznego parametru typu `T`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-10/src/main.rs:here}}
```

</Listing>

Ten kod oznacza, że typ `Point<f32>` będzie miał metodę
`distance_from_origin`; pozostałe instancje `Point<T>`, w których `T` nie jest
typu `f32`, nie będą miały zdefiniowanej tej metody. Metoda mierzy, jak daleko
nasz punkt znajduje się od punktu o współrzędnych (0.0, 0.0), i korzysta z
operacji matematycznych dostępnych tylko dla typów zmiennoprzecinkowych.

<!-- BEGIN INTERVENTION: 694bb2d0-f2e6-4b0b-a3e7-2d9f9e8b3d09 -->
W ten sposób nie można jednocześnie zaimplementować konkretnej *i* generycznej metody o tej samej nazwie. Gdyby na przykład zaimplementować ogólną metodę `distance_from_origin` dla wszystkich typów `T` i konkretną `distance_from_origin` dla `f32`, kompilator odrzuciłby program: Rust nie wie, której implementacji użyć przy wywołaniu `Point<f32>::distance_from_origin`. Ogólniej mówiąc, Rust nie ma mechanizmów podobnych do dziedziczenia, które pozwalałyby specjalizować metody, jak w językach obiektowych, z jednym wyjątkiem (domyślnych metod traitów), który omówimy w następnym podrozdziale.
<!-- END INTERVENTION -->

Generyczne parametry typu w definicji struktury nie zawsze są takie same jak te,
których używasz w sygnaturach metod tej samej struktury. Listing 10-11 używa
typów generycznych `X1` i `Y1` dla struktury `Point` oraz `X2` i `Y2` dla
sygnatury metody `mixup`, aby przykład był czytelniejszy. Metoda tworzy nową
instancję `Point` z wartością `x` z `Point` będącego `self` (typu `X1`) i
wartością `y` z przekazanego `Point` (typu `Y2`).

<Listing number="10-11" file-name="src/main.rs" caption="Metoda używająca typów generycznych innych niż w definicji jej struktury">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-11/src/main.rs}}
```

</Listing>

W `main` zdefiniowaliśmy `Point`, który ma `i32` dla `x` (o wartości `5`) i
`f64` dla `y` (o wartości `10.4`). Zmienna `p2` to struktura `Point`, która ma
wycinek łańcucha (*string slice*) dla `x` (o wartości `"Hello"`) i `char` dla
`y` (o wartości `c`). Wywołanie `mixup` na `p1` z argumentem `p2` daje nam `p3`,
które będzie miało `i32` dla `x`, ponieważ `x` pochodzi z `p1`. Zmienna `p3`
będzie miała `char` dla `y`, ponieważ `y` pochodzi z `p2`. Wywołanie makra
`println!` wypisze `p3.x = 5, p3.y = c`.

Celem tego przykładu jest pokazanie sytuacji, w której część parametrów
generycznych jest deklarowana przy `impl`, a część przy definicji metody.
Parametry generyczne `X1` i `Y1` deklarujemy tu po `impl`, ponieważ należą do
definicji struktury. Parametry generyczne `X2` i `Y2` deklarujemy po `fn mixup`,
ponieważ mają znaczenie tylko dla metody.

### Wydajność kodu korzystającego z typów generycznych {#performance-of-code-using-generics}

Być może zastanawiasz się, czy używanie generycznych parametrów typu wiąże się z
kosztem w czasie działania. Dobra wiadomość jest taka, że używanie typów
generycznych nie spowolni programu w porównaniu z użyciem konkretnych typów.

Rust osiąga to, wykonując w czasie kompilacji (*compile-time*) monomorfizację
kodu korzystającego z typów generycznych. _Monomorfizacja_ (*monomorphization*)
to proces zamieniania kodu generycznego na kod konkretny przez wypełnienie go
konkretnymi typami używanymi podczas kompilacji. W tym procesie kompilator robi
coś odwrotnego niż my, gdy tworzyliśmy funkcję generyczną w listingu 10-5:
przegląda wszystkie miejsca, w których wywoływany jest kod generyczny, i
generuje kod dla konkretnych typów, z którymi jest on wywoływany.

Zobaczmy, jak to działa, na przykładzie generycznego enuma `Option<T>` z
biblioteki standardowej:

```rust
let integer = Some(5);
let float = Some(5.0);
```

Kompilując ten kod, Rust wykonuje monomorfizację. W trakcie tego procesu
kompilator odczytuje wartości użyte w instancjach `Option<T>` i rozpoznaje dwa
rodzaje `Option<T>`: jeden z `i32`, drugi z `f64`. W związku z tym rozwija
generyczną definicję `Option<T>` w dwie definicje wyspecjalizowane dla `i32` i
`f64`, zastępując definicję generyczną konkretnymi.

Zmonomorfizowana wersja kodu wygląda podobnie do poniższej (kompilator używa
innych nazw niż te, których używamy tu dla ilustracji):

<Listing file-name="src/main.rs">

```rust
enum Option_i32 {
    Some(i32),
    None,
}

enum Option_f64 {
    Some(f64),
    None,
}

fn main() {
    let integer = Option_i32::Some(5);
    let float = Option_f64::Some(5.0);
}
```

</Listing>

Generyczny `Option<T>` zostaje zastąpiony konkretnymi definicjami utworzonymi
przez kompilator. Ponieważ Rust kompiluje kod generyczny do kodu, który w każdym
przypadku określa konkretny typ, nie ponosimy w czasie działania żadnego kosztu
za używanie typów generycznych. W czasie działania kod jest tak samo wydajny,
jakbyśmy ręcznie powielili każdą definicję. Proces monomorfizacji sprawia, że
typy generyczne w Ruście są w czasie działania niezwykle wydajne.

{{#quiz ../quizzes/ch10-01-generics.toml}}

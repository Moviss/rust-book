## Zaawansowane funkcje i domknięcia {#advanced-functions-and-closures}

W tym podrozdziale omówimy kilka zaawansowanych mechanizmów związanych z
funkcjami i domknięciami (*closures*), w tym wskaźniki na funkcje i zwracanie
domknięć.

### Wskaźniki na funkcje {#function-pointers}

Mówiliśmy już o tym, jak przekazywać domknięcia do funkcji; do funkcji można
jednak przekazywać także zwykłe funkcje! Ta technika przydaje się, gdy chcesz
przekazać już zdefiniowaną funkcję, zamiast definiować nowe domknięcie. Funkcje
są automatycznie konwertowane na typ `fn` (z małym _f_), którego nie należy
mylić z *traitem* (cechą typu, zbliżoną do interfejsu) domknięć `Fn`. Typ `fn` nazywa się _wskaźnikiem na
funkcję_ (*function pointer*). Przekazywanie funkcji za pomocą wskaźników na
funkcje pozwala używać funkcji jako argumentów innych funkcji.

Składnia określająca, że parametr jest wskaźnikiem na funkcję, przypomina
składnię domknięć, co widać w listingu 20-28. Zdefiniowaliśmy w nim funkcję
`add_one`, która dodaje 1 do swojego parametru. Funkcja `do_twice` przyjmuje dwa
parametry: wskaźnik na dowolną funkcję, która przyjmuje parametr typu `i32` i
zwraca `i32`, oraz jedną wartość typu `i32`. Funkcja `do_twice` dwukrotnie
wywołuje funkcję `f`, przekazując jej wartość `arg`, a następnie dodaje do
siebie wyniki obu wywołań. Funkcja `main` wywołuje `do_twice` z argumentami
`add_one` i `5`.

<Listing number="20-28" file-name="src/main.rs" caption="Użycie typu `fn`, aby przyjąć wskaźnik na funkcję jako argument">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-28/src/main.rs}}
```

</Listing>

Ten kod wypisuje `The answer is: 12`. Określamy, że parametr `f` w `do_twice`
jest typu `fn`, który przyjmuje jeden parametr typu `i32` i zwraca `i32`.
Następnie możemy wywołać `f` w treści `do_twice`. W `main` możemy przekazać
nazwę funkcji `add_one` jako pierwszy argument `do_twice`.

W przeciwieństwie do domknięć `fn` jest typem, a nie traitem, więc podajemy
`fn` bezpośrednio jako typ parametru, zamiast deklarować generyczny parametr
typu z jednym z traitów `Fn` jako ograniczeniem traitu (*trait bound*).

Wskaźniki na funkcje implementują wszystkie trzy traity domknięć (`Fn`, `FnMut`
i `FnOnce`), co oznacza, że wskaźnik na funkcję zawsze możesz przekazać jako
argument funkcji, która oczekuje domknięcia. Najlepiej pisać funkcje z użyciem
typu generycznego (*generic type*) i jednego z traitów domknięć, aby mogły
przyjmować zarówno funkcje, jak i domknięcia.

Mimo to przykładem sytuacji, w której chcielibyśmy przyjmować tylko `fn`, a nie
domknięcia, jest współpraca z zewnętrznym kodem, który nie ma domknięć: funkcje
w C mogą przyjmować funkcje jako argumenty, ale C nie ma domknięć.

Jako przykład sytuacji, w której można użyć albo domknięcia zdefiniowanego w
miejscu, albo nazwanej funkcji, przyjrzyjmy się użyciu metody `map` dostarczanej
przez trait `Iterator` z biblioteki standardowej. Aby za pomocą metody `map`
zamienić wektor (*vector*) liczb na wektor łańcuchów znaków (*strings*), możemy
użyć domknięcia, jak w listingu 20-29.

<Listing number="20-29" caption="Użycie domknięcia z metodą `map` do konwersji liczb na łańcuchy znaków">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-29/src/main.rs:here}}
```

</Listing>

Zamiast domknięcia możemy też jako argument `map` podać nazwę funkcji. Listing
20-30 pokazuje, jak by to wyglądało.

<Listing number="20-30" caption="Użycie funkcji `String::to_string` z metodą `map` do konwersji liczb na łańcuchy znaków">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-30/src/main.rs:here}}
```

</Listing>

Zauważ, że musimy użyć w pełni kwalifikowanej składni, o której mówiliśmy w
podrozdziale [„Zaawansowane traity”][advanced-traits]<!-- ignore -->, ponieważ
dostępnych jest kilka funkcji o nazwie `to_string`.

Używamy tu funkcji `to_string` zdefiniowanej w traicie `ToString`, który
biblioteka standardowa implementuje dla każdego typu implementującego `Display`.

Przypomnij sobie z podrozdziału [„Wartości enumów”][enum-values]<!-- ignore -->
w rozdziale 6, że nazwa każdego zdefiniowanego przez nas wariantu *enuma* (typu
wyliczeniowego) staje się również funkcją inicjalizującą. Tych funkcji
inicjalizujących możemy używać jako wskaźników na funkcje implementujących
traity domknięć, co oznacza, że możemy je podawać jako argumenty metod
przyjmujących domknięcia, jak w listingu 20-31.

<Listing number="20-31" caption="Użycie inicjalizatora wariantu enuma z metodą `map` do utworzenia instancji `Status` z liczb">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-31/src/main.rs:here}}
```

</Listing>

Tworzymy tu instancje `Status::Value` z każdej wartości `u32` z zakresu, na
którym wywołano `map`, używając funkcji inicjalizującej `Status::Value`. Jedni
wolą ten styl, inni wolą używać domknięć. Oba kompilują się do tego samego kodu,
więc używaj tego, który jest dla ciebie czytelniejszy.

### Zwracanie domknięć {#returning-closures}

Domknięcia są reprezentowane przez traity, co oznacza, że nie można zwracać
domknięć bezpośrednio. W większości przypadków, w których chcielibyśmy zwrócić
trait, możemy zamiast tego użyć typu konkretnego implementującego ten trait jako
wartości zwracanej funkcji. Z domknięciami zwykle nie da się jednak tak zrobić,
ponieważ nie mają one typu konkretnego, który można zwrócić. Na przykład nie
wolno użyć wskaźnika na funkcję `fn` jako typu zwracanego, jeśli domknięcie
przechwytuje jakiekolwiek wartości ze swojego zasięgu (*scope*).

Zamiast tego zwykle użyjesz składni `impl Trait`, którą poznaliśmy w
rozdziale 10. Możesz zwrócić dowolny typ funkcyjny, używając `Fn`, `FnOnce` i
`FnMut`. Na przykład kod z listingu 20-32 skompiluje się bez problemu.

<Listing number="20-32" caption="Zwracanie domknięcia z funkcji za pomocą składni `impl Trait`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-32/src/lib.rs}}
```

</Listing>

Jak jednak zauważyliśmy w podrozdziale
[„Wnioskowanie i adnotacje typów domknięć”][closure-types]<!-- ignore --> w
rozdziale 13, każde domknięcie ma też swój własny, odrębny typ. Jeśli musisz
pracować z wieloma funkcjami o tej samej sygnaturze, ale różnych
implementacjach, musisz użyć dla nich obiektu
traitu (*trait object*). Zobacz, co się stanie, jeśli napiszesz kod taki jak w
listingu 20-33.

<Listing file-name="src/main.rs" number="20-33" caption="Tworzenie `Vec<T>` z domknięć zdefiniowanych przez funkcje zwracające typy `impl Fn`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-33/src/main.rs}}
```

</Listing>

Mamy tu dwie funkcje, `returns_closure` i `returns_initialized_closure`, które
obie zwracają `impl Fn(i32) -> i32`. Zauważ, że zwracane przez nie domknięcia
są różne, mimo że implementują ten sam typ. Jeśli spróbujemy to skompilować,
Rust poinformuje nas, że to nie zadziała:

```text
{{#include ../listings/ch20-advanced-features/listing-20-33/output.txt}}
```

Komunikat o błędzie mówi, że za każdym razem, gdy zwracamy `impl Trait`, Rust
tworzy unikalny _typ nieprzezroczysty_ (*opaque type*), czyli typ, w którego
szczegóły – to, co Rust dla nas konstruuje – nie możemy zajrzeć; nie możemy też
odgadnąć, jaki typ Rust wygeneruje, żeby zapisać go samodzielnie. Mimo że te
funkcje zwracają domknięcia implementujące ten sam trait, `Fn(i32) -> i32`, typy
nieprzezroczyste generowane przez Rusta dla każdej z nich są różne. (Przypomina
to sytuację, w której Rust tworzy różne typy konkretne dla odrębnych bloków
async, nawet jeśli mają ten sam typ wyjściowy, co widzieliśmy w podrozdziale
[„Typ `Pin` i trait `Unpin`”][future-types]<!-- ignore --> w rozdziale 17).
Rozwiązanie tego problemu widzieliśmy już kilka razy: możemy użyć obiektu
traitu, jak w listingu 20-34.

<Listing number="20-34" caption="Tworzenie `Vec<T>` z domknięć zdefiniowanych przez funkcje zwracające `Box<dyn Fn>`, dzięki czemu mają one ten sam typ">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-34/src/main.rs:here}}
```

</Listing>

Ten kod skompiluje się bez problemu. Więcej o obiektach traitów znajdziesz w
podrozdziale
[„Używanie obiektów traitów do abstrahowania wspólnego zachowania”][trait-objects]<!-- ignore -->
w rozdziale 18.

Teraz przyjrzyjmy się makrom!

{{#quiz ../quizzes/ch19-05-advanced-functions-and-closures.toml}}

[advanced-traits]: ch20-02-advanced-traits.html#advanced-traits
[enum-values]: ch06-01-defining-an-enum.html#enum-values
[closure-types]: ch13-01-closures.html#closure-type-inference-and-annotation
[future-types]: ch17-03-more-futures.html
[trait-objects]: ch18-02-trait-objects.html

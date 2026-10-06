## Zaawansowane typy {#advanced-types}

System typów Rusta ma kilka mechanizmów, o których dotąd tylko wspomnieliśmy,
ale których jeszcze nie omówiliśmy. Zaczniemy od ogólnego omówienia newtype’ów
i zastanowimy się, dlaczego są przydatne jako typy. Potem przejdziemy do
aliasów typów – mechanizmu podobnego do newtype’ów, ale o nieco innej
semantyce. Omówimy też typ `!` oraz typy o dynamicznym rozmiarze.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-for-type-safety-and-abstraction"></a>

### Bezpieczeństwo typów i abstrakcja dzięki wzorcowi newtype {#type-safety-and-abstraction-with-the-newtype-pattern}

Ten podrozdział zakłada, że znasz już wcześniejszy podrozdział
[„Implementowanie zewnętrznych traitów za pomocą wzorca newtype”][newtype]<!-- ignore -->.
Wzorzec newtype przydaje się także do zadań wykraczających poza te, które
dotąd omówiliśmy, m.in. do statycznego zapewniania, że wartości nigdy nie
zostaną pomylone, oraz do wskazywania jednostek wartości. Przykład użycia
newtype’ów do wskazywania jednostek widzieliśmy w listingu 20-16: struktury
(*struct*) `Millimeters` i `Meters` opakowywały wartości `u32` w newtype. Gdyby
napisać funkcję z parametrem typu `Millimeters`, nie dałoby się skompilować
programu, który przypadkiem próbowałby wywołać ją z wartością typu `Meters`
albo zwykłym `u32`.

Wzorca newtype możemy też użyć, by ukryć za abstrakcją niektóre szczegóły
implementacji typu: nowy typ może udostępniać publiczne API inne niż API
prywatnego typu wewnętrznego.

Newtype’y mogą również ukrywać wewnętrzną implementację. Moglibyśmy na przykład
udostępnić typ `People` opakowujący `HashMap<i32, String>`, który przechowuje
identyfikator osoby powiązany z jej imieniem. Kod korzystający z `People`
miałby kontakt tylko z udostępnionym przez nas publicznym API, np. z metodą
dodającą imię do kolekcji `People`; ten kod nie musiałby wiedzieć, że
wewnętrznie przypisujemy imionom identyfikatory typu `i32`. Wzorzec newtype to
lekki sposób na osiągnięcie hermetyzacji ukrywającej szczegóły implementacji,
którą omówiliśmy w podrozdziale [„Hermetyzacja, która ukrywa szczegóły
implementacji”][encapsulation-that-hides-implementation-details]<!-- ignore -->
w rozdziale 18.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-type-synonyms-with-type-aliases"></a>

### Synonimy typów i aliasy typów {#type-synonyms-and-type-aliases}

Rust pozwala zadeklarować _alias typu_ (*type alias*), czyli nadać istniejącemu
typowi inną nazwę. Służy do tego słowo kluczowe (*keyword*) `type`. Możemy na
przykład utworzyć alias `Kilometers` dla `i32` w taki sposób:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:here}}
```

Teraz alias `Kilometers` jest _synonimem_ (*synonym*) typu `i32`; w odróżnieniu
od typów `Millimeters` i `Meters`, które utworzyliśmy w listingu 20-16,
`Kilometers` nie jest odrębnym, nowym typem. Wartości typu `Kilometers` będą
traktowane tak samo jak wartości typu `i32`:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-04-kilometers-alias/src/main.rs:there}}
```

Ponieważ `Kilometers` i `i32` to ten sam typ, możemy dodawać do siebie wartości
obu typów i przekazywać wartości `Kilometers` do funkcji przyjmujących
parametry `i32`. Przy takim podejściu tracimy jednak korzyści ze sprawdzania
typów, jakie daje omówiony wcześniej wzorzec newtype. Innymi słowy, jeśli
gdzieś pomylimy wartości `Kilometers` i `i32`, kompilator nie zgłosi błędu.

Synonimy typów służą przede wszystkim do ograniczania powtórzeń. Możemy mieć na
przykład taki długi typ:

```rust,ignore
Box<dyn Fn() + Send + 'static>
```

Wpisywanie tego długiego typu w sygnaturach funkcji i w adnotacjach typów w
całym kodzie bywa męczące i sprzyja błędom. Wyobraź sobie projekt pełen kodu
takiego jak w listingu 20-25.

<Listing number="20-25" caption="Używanie długiego typu w wielu miejscach">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-25/src/main.rs:here}}
```

</Listing>

Alias typu ułatwia zarządzanie tym kodem, bo ogranicza powtórzenia. W listingu
20-26 wprowadziliśmy dla rozwlekłego typu alias o nazwie `Thunk` i możemy
zastąpić wszystkie użycia tego typu krótszym aliasem `Thunk`.

<Listing number="20-26" caption="Wprowadzenie aliasu typu `Thunk` w celu ograniczenia powtórzeń">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-26/src/main.rs:here}}
```

</Listing>

Ten kod znacznie łatwiej czytać i pisać! Wybór znaczącej nazwy aliasu typu
może też pomóc wyrazić twoje zamiary (_thunk_ to określenie kodu, który ma
zostać obliczony później, więc to trafna nazwa dla przechowywanego domknięcia
(*closure*)).

Aliasy typów często stosuje się także z typem `Result<T, E>`, by ograniczyć
powtórzenia. Weźmy moduł `std::io` z biblioteki standardowej. Operacje
wejścia-wyjścia często zwracają `Result<T, E>`, by obsłużyć sytuacje, w których
operacja się nie powiedzie. Ta biblioteka ma strukturę `std::io::Error`, która
reprezentuje wszystkie możliwe błędy wejścia-wyjścia. Wiele funkcji w `std::io`
zwraca `Result<T, E>`, w którym `E` to `std::io::Error`, np. te funkcje z
*traitu* (cecha typu, zbliżona do interfejsu) `Write`:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-05-write-trait/src/lib.rs}}
```

`Result<..., Error>` powtarza się wiele razy. Dlatego `std::io` zawiera taką
deklarację aliasu typu:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:here}}
```

Ponieważ ta deklaracja znajduje się w module `std::io`, możemy używać w pełni
kwalifikowanego aliasu `std::io::Result<T>`, czyli `Result<T, E>`, w którym za
`E` podstawiono `std::io::Error`. Sygnatury funkcji traitu `Write` wyglądają w
efekcie tak:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-06-result-alias/src/lib.rs:there}}
```

Alias typu pomaga na dwa sposoby: ułatwia pisanie kodu _i_ zapewnia spójny
interfejs w całym `std::io`. Ponieważ to tylko alias, jest to po prostu kolejny
`Result<T, E>`, co oznacza, że możemy używać z nim wszystkich metod działających
na `Result<T, E>`, a także specjalnej składni, takiej jak operator `?`.

### Typ never, który nigdy nie zwraca {#the-never-type-that-never-returns}

Rust ma specjalny typ o nazwie `!`, który w żargonie teorii typów nazywa się
_typem pustym_ (*empty type*), bo nie ma żadnych wartości. Wolimy nazywać go
_typem never_ (*never type*), ponieważ zajmuje miejsce typu zwracanego, gdy
funkcja nigdy nie zwraca sterowania. Oto przykład:

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-07-never-type/src/lib.rs:here}}
```

Ten kod czyta się jako „funkcja `bar` zwraca never”. Funkcje, które zwracają
never, nazywamy _funkcjami rozbieżnymi_ (*diverging functions*). Nie możemy
tworzyć wartości typu `!`, więc `bar` nigdy nie może zwrócić sterowania.

Do czego jednak może się przydać typ, dla którego nie da się utworzyć żadnej
wartości? Przypomnij sobie kod z listingu 2-5, fragment gry w zgadywanie
liczby; odtworzyliśmy jego część w listingu 20-27.

<Listing number="20-27" caption="`match` z ramieniem kończącym się instrukcją `continue`">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:ch19}}
```

</Listing>

Wtedy pominęliśmy pewne szczegóły tego kodu. W podrozdziale [„Konstrukcja
przepływu sterowania `match`”][the-match-control-flow-construct]<!-- ignore -->
w rozdziale 6 wyjaśniliśmy, że wszystkie ramiona (*arms*) `match` muszą zwracać
ten sam typ. Dlatego na przykład taki kod nie działa:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-08-match-arms-different-types/src/main.rs:here}}
```

Typ `guess` w tym kodzie musiałby być jednocześnie liczbą całkowitą _i_
łańcuchem znaków (*string*), a Rust wymaga, by `guess` miało tylko jeden typ.
Co więc zwraca `continue`? Jak to możliwe, że w listingu 20-27 mogliśmy zwrócić
`u32` z jednego ramienia, a drugie ramię kończyło się instrukcją `continue`?

Jak się pewnie domyślasz, `continue` ma wartość typu `!`. Oznacza to, że gdy
Rust oblicza typ `guess`, patrzy na oba ramiona dopasowania: pierwsze z
wartością typu `u32`, drugie z wartością typu `!`. Ponieważ `!` nigdy nie może
mieć wartości, Rust uznaje, że typem `guess` jest `u32`.

Formalnie opisuje się to tak: wyrażenia (*expressions*) typu `!` mogą zostać
przekształcone (*coerced*) w dowolny inny typ. Możemy zakończyć to ramię
`match` instrukcją `continue`, ponieważ `continue` nie zwraca wartości, tylko
przenosi sterowanie z powrotem na początek pętli, więc w przypadku `Err` nigdy
nie przypisujemy wartości do `guess`.

Typ never przydaje się także z makrem `panic!`. Przypomnij sobie funkcję
`unwrap`, którą wywołujemy na wartościach `Option<T>`, by uzyskać wartość albo
wywołać panikę (*panic*); ma ona taką definicję:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-09-unwrap-definition/src/lib.rs:here}}
```

W tym kodzie dzieje się to samo co w `match` z listingu 20-27: Rust widzi, że
`val` ma typ `T`, a `panic!` ma typ `!`, więc wynikiem całego wyrażenia `match`
jest `T`. Ten kod działa, ponieważ `panic!` nie produkuje wartości, tylko
kończy program. W przypadku `None` nie zwrócimy żadnej wartości z `unwrap`,
więc ten kod jest poprawny.

Ostatnim przykładem wyrażenia typu `!` jest pętla:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-10-loop-returns-never/src/main.rs:here}}
```

Ta pętla nigdy się nie kończy, więc wartością wyrażenia jest `!`. Nie byłoby
tak jednak, gdybyśmy dodali `break`, bo pętla zakończyłaby się po dotarciu do
`break`.

### Typy o dynamicznym rozmiarze i trait `Sized` {#dynamically-sized-types-and-the-sized-trait}

Rust musi znać pewne szczegóły swoich typów, np. ile miejsca zaalokować na
wartość danego typu. Przez to jeden zakątek jego systemu typów jest na początku
nieco mylący: pojęcie _typów o dynamicznym rozmiarze_ (*dynamically sized
types*). Nazywane czasem _DST_ albo _typami bez określonego rozmiaru_
(*unsized types*), pozwalają pisać kod korzystający z wartości, których rozmiar
możemy poznać dopiero w czasie działania programu.

Przyjrzyjmy się szczegółom typu o dynamicznym rozmiarze o nazwie `str`, którego
używamy w całej książce. Tak, nie `&str`, lecz samo `str` jest DST. W wielu
sytuacjach, np. przy przechowywaniu tekstu wpisanego przez użytkownika, nie
możemy znać długości łańcucha aż do czasu działania programu. Oznacza to, że nie
możemy utworzyć zmiennej typu `str` ani przyjąć argumentu typu `str`. Weźmy
następujący kod, który nie działa:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-11-cant-create-str/src/main.rs:here}}
```

Rust musi wiedzieć, ile pamięci zaalokować na każdą wartość danego typu, a
wszystkie wartości jednego typu muszą zajmować tyle samo pamięci. Gdyby Rust
pozwolił nam napisać ten kod, te dwie wartości `str` musiałyby zajmować tyle
samo miejsca. Mają jednak różne długości: `s1` potrzebuje 12 bajtów, a `s2` 15.
Dlatego nie da się utworzyć zmiennej przechowującej wartość typu o dynamicznym
rozmiarze.

Co więc robimy? W tej sytuacji znasz już odpowiedź: nadajemy `s1` i `s2` typ
`&str`, czyli wycinka łańcucha (*string slice*), zamiast `str`. Jak pamiętasz z
podrozdziału [„Wycinki łańcuchów”][string-slices]<!-- ignore --> w rozdziale 4,
struktura danych wycinka przechowuje tylko pozycję początkową i długość
wycinka. Zatem choć `&T` to pojedyncza wartość przechowująca adres pamięci, pod
którym znajduje się `T`, wycinek łańcucha to _dwie_ wartości: adres `str` i
jego długość. Dzięki temu rozmiar wartości wycinka łańcucha możemy poznać w
czasie kompilacji (*compile-time*): jest on dwa razy większy niż rozmiar
`usize`. Innymi słowy, zawsze znamy rozmiar wycinka łańcucha, bez względu na
to, jak długi jest łańcuch, do którego się odnosi. Ogólnie rzecz biorąc, w taki
właśnie sposób używa się w Ruście typów o dynamicznym rozmiarze: mają one
dodatkowy fragment metadanych, który przechowuje rozmiar dynamicznej
informacji. Złota zasada typów o dynamicznym rozmiarze mówi, że wartości takich
typów musimy zawsze umieszczać za jakimś wskaźnikiem.

`str` możemy łączyć z wszelkiego rodzaju wskaźnikami, np. `Box<str>` albo
`Rc<str>`. Właściwie już to widzieliśmy, tyle że z innym typem o dynamicznym
rozmiarze: traitami. Każdy trait jest typem o dynamicznym rozmiarze, do którego
możemy się odwołać za pomocą nazwy traitu. W podrozdziale [„Używanie obiektów
traitów do abstrahowania wspólnego zachowania”][using-trait-objects-to-abstract-over-shared-behavior]<!--
ignore --> w rozdziale 18 wspomnieliśmy, że aby używać traitów jako obiektów traitów
(*trait objects*), musimy umieścić je za wskaźnikiem, np. `&dyn Trait` lub
`Box<dyn Trait>` (zadziałałby też `Rc<dyn Trait>`).

Do pracy z DST Rust udostępnia trait `Sized`, który określa, czy rozmiar typu
jest znany w czasie kompilacji. Ten trait jest automatycznie implementowany dla
wszystkiego, czego rozmiar jest znany w czasie kompilacji. Ponadto Rust
niejawnie dodaje ograniczenie `Sized` do każdej funkcji generycznej. Oznacza to,
że definicja funkcji generycznej taka jak ta:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-12-generic-fn-definition/src/lib.rs}}
```

jest w rzeczywistości traktowana tak, jakbyśmy napisali:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-13-generic-implicit-sized-bound/src/lib.rs}}
```

Domyślnie funkcje generyczne działają tylko na typach, których rozmiar jest
znany w czasie kompilacji. Możesz jednak złagodzić to ograniczenie za pomocą
następującej specjalnej składni:

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-14-generic-maybe-sized/src/lib.rs}}
```

Ograniczenie traitu (*trait bound*) `?Sized` oznacza „`T` może, ale nie musi
być `Sized`”, a ten zapis zastępuje domyślną regułę, zgodnie z którą typy
generyczne (*generics*) muszą mieć rozmiar znany w czasie kompilacji. Składnia
`?Trait` w tym znaczeniu jest dostępna tylko dla `Sized`, a nie dla innych
traitów.

Zauważ też, że zmieniliśmy typ parametru `t` z `T` na `&T`. Ponieważ typ może
nie być `Sized`, musimy używać go za jakimś wskaźnikiem. W tym przypadku
wybraliśmy referencję (*reference*).

Teraz porozmawiamy o funkcjach i domknięciach!

{{#quiz ../quizzes/ch19-04-advanced-types.toml}}

[encapsulation-that-hides-implementation-details]: ch18-01-what-is-oo.html#encapsulation-that-hides-implementation-details
[string-slices]: ch04-04-slices.html#string-slices
[the-match-control-flow-construct]: ch06-02-match.html#the-match-control-flow-construct
[using-trait-objects-to-abstract-over-shared-behavior]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern

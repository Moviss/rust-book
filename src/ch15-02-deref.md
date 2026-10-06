<!-- Old headings. Do not remove or links may break. -->

<a id="treating-smart-pointers-like-regular-references-with-the-deref-trait"></a>
<a id="treating-smart-pointers-like-regular-references-with-deref"></a>

## Traktowanie inteligentnych wskaźników jak zwykłych referencji {#treating-smart-pointers-like-regular-references}

Implementacja *traitu* (cecha typu, zbliżona do interfejsu) `Deref` pozwala
dostosować zachowanie _operatora dereferencji_ (*dereference operator*) `*` –
nie mylić z operatorem mnożenia ani z operatorem glob (*glob operator*). Gdy
zaimplementujesz `Deref` tak, by inteligentny wskaźnik (*smart pointer*) można
było traktować jak zwykłą referencję (*reference*), możesz pisać kod operujący
na referencjach i używać go także z inteligentnymi wskaźnikami.

Najpierw zobaczymy, jak operator dereferencji działa ze zwykłymi referencjami.
Potem spróbujemy zdefiniować własny typ, który zachowuje się jak `Box<T>`, i
przekonamy się, dlaczego operator dereferencji nie działa na nim tak jak na
referencji. Sprawdzimy, jak implementacja traitu `Deref` pozwala inteligentnym
wskaźnikom działać podobnie do referencji. Na koniec przyjrzymy się mechanizmowi
*deref coercion* (automatyczna konwersja przez dereferencję) w Ruście i temu,
jak pozwala on pracować zarówno z referencjami, jak i z inteligentnymi
wskaźnikami.

<!-- Old headings. Do not remove or links may break. -->

<a id="following-the-pointer-to-the-value-with-the-dereference-operator"></a>
<a id="following-the-pointer-to-the-value"></a>

### Podążanie za referencją do wartości {#following-the-reference-to-the-value}

Zwykła referencja jest rodzajem wskaźnika, a wskaźnik można sobie wyobrazić jako
strzałkę prowadzącą do wartości przechowywanej gdzieś indziej. W listingu 15-6
tworzymy referencję do wartości typu `i32`, a następnie używamy operatora
dereferencji, by podążyć za referencją do wartości.

<Listing number="15-6" file-name="src/main.rs" caption="Użycie operatora dereferencji do podążenia za referencją do wartości typu `i32`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-06/src/main.rs}}
```

</Listing>

Zmienna `x` przechowuje wartość `5` typu `i32`. Ustawiamy `y` na referencję do
`x`. Możemy sprawdzić asercją, że `x` jest równe `5`. Jeśli jednak chcemy
sformułować asercję o wartości w `y`, musimy użyć `*y`, by podążyć za referencją
do wartości, na którą wskazuje (stąd _dereferencja_), tak aby kompilator mógł
porównać faktyczną wartość. Po wykonaniu dereferencji `y` mamy dostęp do liczby
całkowitej, na którą wskazuje `y`, i możemy porównać ją z `5`.

Gdybyśmy zamiast tego spróbowali napisać `assert_eq!(5, y);`, dostalibyśmy taki
błąd kompilacji:

```console
{{#include ../listings/ch15-smart-pointers/output-only-01-comparing-to-reference/output.txt}}
```

Porównywanie liczby z referencją do liczby jest niedozwolone, bo to różne typy.
Musimy użyć operatora dereferencji, by podążyć za referencją do wartości, na
którą wskazuje.

### Używanie `Box<T>` jak referencji {#using-boxt-like-a-reference}

Kod z listingu 15-6 możemy przepisać tak, by zamiast referencji używał `Box<T>`.
Operator dereferencji użyty na `Box<T>` w listingu 15-7 działa tak samo jak
operator dereferencji użyty na referencji w listingu 15-6.

<Listing number="15-7" file-name="src/main.rs" caption="Użycie operatora dereferencji na `Box<i32>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-07/src/main.rs}}
```

</Listing>

Główna różnica między listingiem 15-7 a listingiem 15-6 polega na tym, że tutaj
ustawiamy `y` na instancję *boxa* (wskaźnik na dane umieszczone na stercie)
wskazującego na skopiowaną wartość `x`, a nie na referencję wskazującą na
wartość `x`. W ostatniej asercji możemy użyć operatora dereferencji, by podążyć
za wskaźnikiem boxa w taki sam sposób, jak wtedy, gdy `y` było referencją. Teraz
zdefiniujemy własny typ boxa, by sprawdzić, co szczególnego jest w `Box<T>`, że
pozwala nam używać operatora dereferencji.

### Definiowanie własnego inteligentnego wskaźnika {#defining-our-own-smart-pointer}

Zbudujmy typ opakowujący podobny do typu `Box<T>` z biblioteki standardowej, by
zobaczyć, jak typy inteligentnych wskaźników domyślnie zachowują się inaczej niż
referencje. Potem zobaczymy, jak dodać możliwość używania operatora
dereferencji.

> Uwaga: między typem `MyBox<T>`, który zaraz zbudujemy, a prawdziwym `Box<T>`
> jest jedna duża różnica: nasza wersja nie będzie przechowywać danych na
> stercie (*heap*). W tym przykładzie skupiamy się na `Deref`, więc to, gdzie
> dane są faktycznie przechowywane, jest mniej ważne niż zachowanie podobne do
> wskaźnika.

Typ `Box<T>` jest ostatecznie zdefiniowany jako struktura krotkowa (*tuple
struct*) z jednym elementem, więc listing 15-8 definiuje typ `MyBox<T>` w ten
sam sposób. Zdefiniujemy też funkcję `new`, odpowiadającą funkcji `new`
zdefiniowanej dla `Box<T>`.

<Listing number="15-8" file-name="src/main.rs" caption="Definicja typu `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-08/src/main.rs:here}}
```

</Listing>

Definiujemy strukturę (*struct*) o nazwie `MyBox` i deklarujemy parametr
generyczny `T`, bo chcemy, by nasz typ mógł przechowywać wartości dowolnego
typu. Typ `MyBox` jest strukturą krotkową z jednym elementem typu `T`. Funkcja
`MyBox::new` przyjmuje jeden parametr typu `T` i zwraca instancję `MyBox`
przechowującą przekazaną wartość.

Spróbujmy dodać do listingu 15-8 funkcję `main` z listingu 15-7 i zmienić ją
tak, by używała zdefiniowanego przez nas typu `MyBox<T>` zamiast `Box<T>`. Kod w
listingu 15-9 się nie skompiluje, bo Rust nie wie, jak wykonać dereferencję
`MyBox`.

<Listing number="15-9" file-name="src/main.rs" caption="Próba użycia `MyBox<T>` w taki sam sposób, w jaki używaliśmy referencji i `Box<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-09/src/main.rs:here}}
```

</Listing>

Oto błąd kompilacji, który otrzymujemy:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-09/output.txt}}
```

Na naszym typie `MyBox<T>` nie można wykonać dereferencji, bo nie
zaimplementowaliśmy dla niego tej możliwości. Aby umożliwić dereferencję
operatorem `*`, implementujemy trait `Deref`.

<!-- Old headings. Do not remove or links may break. -->

<a id="treating-a-type-like-a-reference-by-implementing-the-deref-trait"></a>

### Implementowanie traitu `Deref` {#implementing-the-deref-trait}

Jak omówiliśmy w podrozdziale [„Implementowanie traitu dla
typu”][impl-trait]<!-- ignore --> w rozdziale 10, aby zaimplementować trait,
musimy dostarczyć implementacje jego wymaganych metod. Trait `Deref`,
dostarczany przez bibliotekę standardową, wymaga zaimplementowania jednej metody
o nazwie `deref`, która pożycza `self` i zwraca referencję do wewnętrznych
danych. Listing 15-10 zawiera implementację `Deref`, którą należy dodać do
definicji `MyBox<T>`.

<Listing number="15-10" file-name="src/main.rs" caption="Implementacja `Deref` dla `MyBox<T>`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-10/src/main.rs:here}}
```

</Listing>

Składnia `type Target = T;` definiuje typ powiązany (*associated type*), którego
używa trait `Deref`. Typy powiązane to nieco inny sposób deklarowania parametru
generycznego, ale na razie nie musisz się nimi przejmować; omówimy je
dokładniej w rozdziale 20.

Ciało metody `deref` wypełniamy wyrażeniem `&self.0`, aby `deref` zwracała
referencję do wartości, do której chcemy uzyskać dostęp operatorem `*`. Jak
pamiętasz z podrozdziału [„Tworzenie różnych typów za pomocą struktur
krotkowych”][tuple-structs]<!--
ignore --> w rozdziale 5, `.0` daje dostęp do pierwszej wartości w strukturze
krotkowej. Funkcja `main` z listingu 15-9, która wywołuje `*` na wartości
`MyBox<T>`, teraz się kompiluje, a asercje przechodzą!

Bez traitu `Deref` kompilator potrafi wykonać dereferencję tylko referencji `&`.
Metoda `deref` daje kompilatorowi możliwość wzięcia wartości dowolnego typu
implementującego `Deref` i wywołania metody `deref`, by uzyskać referencję, na
której potrafi on wykonać dereferencję.

Gdy w listingu 15-9 wpisaliśmy `*y`, Rust w rzeczywistości wykonał w tle taki
kod:

```rust,ignore
*(y.deref())
```

Rust zastępuje operator `*` wywołaniem metody `deref`, a następnie zwykłą
dereferencją, dzięki czemu nie musimy się zastanawiać, czy trzeba wywołać metodę
`deref`. Ten mechanizm Rusta pozwala pisać kod, który działa identycznie
niezależnie od tego, czy mamy zwykłą referencję, czy typ implementujący `Deref`.

To, że metoda `deref` zwraca referencję do wartości i że zwykła dereferencja
poza nawiasami w `*(y.deref())` nadal jest potrzebna, wynika z systemu własności
(*ownership*). Gdyby metoda `deref` zwracała samą wartość zamiast referencji do
niej, wartość zostałaby przeniesiona (*move*) z `self`. Ani w tym przypadku, ani
w większości przypadków, w których używamy operatora dereferencji, nie chcemy
przejmować własności wewnętrznej wartości w `MyBox<T>`.

Zwróć uwagę, że operator `*` zostaje zastąpiony wywołaniem metody `deref`, a
następnie wywołaniem operatora `*` tylko raz, za każdym razem, gdy używamy `*` w
naszym kodzie. Ponieważ zastępowanie operatora `*` nie jest rekurencyjne w
nieskończoność, otrzymujemy dane typu `i32`, które pasują do `5` w `assert_eq!`
w listingu 15-9.

<!-- Old headings. Do not remove or links may break. -->

<a id="implicit-deref-coercions-with-functions-and-methods"></a>
<a id="using-deref-coercions-in-functions-and-methods"></a>

### Używanie deref coercion w funkcjach i metodach {#using-deref-coercion-in-functions-and-methods}

_Deref coercion_ zamienia referencję do typu implementującego trait `Deref` na
referencję do innego typu. Na przykład deref coercion może zamienić `&String` na
`&str`, ponieważ `String` implementuje trait `Deref` tak, że zwraca `&str`.
Deref coercion to udogodnienie, które Rust stosuje do argumentów funkcji i
metod; działa wyłącznie dla typów implementujących trait `Deref`. Zachodzi
automatycznie, gdy jako argument funkcji lub metody przekazujemy referencję do
wartości określonego typu, który nie pasuje do typu parametru w definicji tej
funkcji lub metody. Sekwencja wywołań metody `deref` zamienia podany przez nas
typ na typ, którego potrzebuje parametr.

Deref coercion dodano do Rusta po to, by osoby piszące wywołania funkcji i metod
nie musiały dodawać tak wielu jawnych referencji i dereferencji za pomocą `&` i
`*`. Mechanizm deref coercion pozwala nam też pisać więcej kodu, który działa
zarówno z referencjami, jak i z inteligentnymi wskaźnikami.

Aby zobaczyć deref coercion w działaniu, użyjmy typu `MyBox<T>` zdefiniowanego w
listingu 15-8 oraz implementacji `Deref` dodanej w listingu 15-10. Listing 15-11
pokazuje definicję funkcji, która ma parametr będący wycinkiem łańcucha
(*string slice*).

<Listing number="15-11" file-name="src/main.rs" caption="Funkcja `hello` z parametrem `name` typu `&str`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-11/src/main.rs:here}}
```

</Listing>

Funkcję `hello` możemy wywołać z wycinkiem łańcucha jako argumentem, na przykład
`hello("Rust");`. Deref coercion umożliwia wywołanie `hello` z referencją do
wartości typu `MyBox<String>`, jak pokazuje listing 15-12.

<Listing number="15-12" file-name="src/main.rs" caption="Wywołanie `hello` z referencją do wartości `MyBox<String>`, co działa dzięki deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-12/src/main.rs:here}}
```

</Listing>

Wywołujemy tu funkcję `hello` z argumentem `&m`, który jest referencją do
wartości `MyBox<String>`. Ponieważ w listingu 15-10 zaimplementowaliśmy trait
`Deref` dla `MyBox<T>`, Rust może zamienić `&MyBox<String>` na `&String`,
wywołując `deref`. Biblioteka standardowa dostarcza implementację `Deref` dla
`String`, która zwraca wycinek łańcucha; jest to opisane w dokumentacji API
traitu `Deref`. Rust ponownie wywołuje `deref`, by zamienić `&String` na `&str`,
co pasuje do definicji funkcji `hello`.

Gdyby Rust nie implementował deref coercion, zamiast kodu z listingu 15-12
musielibyśmy napisać kod z listingu 15-13, by wywołać `hello` z wartością typu
`&MyBox<String>`.

<Listing number="15-13" file-name="src/main.rs" caption="Kod, który musielibyśmy napisać, gdyby Rust nie miał deref coercion">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-13/src/main.rs:here}}
```

</Listing>

`(*m)` wykonuje dereferencję `MyBox<String>` do `String`. Następnie `&` i `[..]`
pobierają wycinek łańcucha `String` równy całemu łańcuchowi, by pasował do
sygnatury `hello`. Bez deref coercion ten kod, pełen wszystkich tych symboli,
jest trudniejszy do czytania, pisania i zrozumienia. Deref coercion pozwala
Rustowi wykonać te konwersje za nas automatycznie.

Gdy trait `Deref` jest zdefiniowany dla danych typów, Rust przeanalizuje typy i
użyje `Deref::deref` tyle razy, ile trzeba, by uzyskać referencję pasującą do
typu parametru. Liczba potrzebnych wstawień `Deref::deref` jest ustalana w
czasie kompilacji (*compile-time*), więc korzystanie z deref coercion nie wiąże
się z żadnym narzutem w czasie działania!

<!-- Old headings. Do not remove or links may break. -->

<a id="how-deref-coercion-interacts-with-mutability"></a>

### Deref coercion a referencje mutowalne {#handling-deref-coercion-with-mutable-references}

Podobnie jak trait `Deref` służy do nadpisania operatora `*` dla referencji
niemutowalnych, trait `DerefMut` służy do nadpisania operatora `*` dla
referencji mutowalnych (*mutable*).

Rust wykonuje deref coercion, gdy napotka typy i implementacje traitów w trzech
przypadkach:

1. z `&T` na `&U`, gdy `T: Deref<Target=U>`;
2. z `&mut T` na `&mut U`, gdy `T: DerefMut<Target=U>`;
3. z `&mut T` na `&U`, gdy `T: Deref<Target=U>`.

Dwa pierwsze przypadki są takie same, z tą różnicą, że drugi dotyczy
mutowalności. Pierwszy przypadek mówi, że jeśli masz `&T`, a `T` implementuje
`Deref` do jakiegoś typu `U`, możesz w przezroczysty sposób uzyskać `&U`. Drugi
przypadek mówi, że ta sama deref coercion zachodzi dla referencji mutowalnych.

Trzeci przypadek jest bardziej podchwytliwy: Rust zamieni też referencję
mutowalną na niemutowalną. Odwrotna zamiana _nie_ jest jednak możliwa:
referencje niemutowalne nigdy nie zostaną zamienione na mutowalne. Zgodnie z
regułami pożyczania (*borrowing*), jeśli masz referencję mutowalną, musi ona być
jedyną referencją do tych danych (w przeciwnym razie program by się nie
skompilował). Zamiana jednej referencji mutowalnej na jedną referencję
niemutowalną nigdy nie złamie reguł pożyczania. Zamiana referencji niemutowalnej
na mutowalną wymagałaby, by początkowa referencja niemutowalna była jedyną
referencją niemutowalną do tych danych, a reguły pożyczania tego nie
gwarantują. Dlatego Rust nie może założyć, że zamiana referencji niemutowalnej
na mutowalną jest możliwa.

{{#quiz ../quizzes/ch15-02-deref.toml}}

[impl-trait]: ch10-02-traits.html#implementing-a-trait-on-a-type
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs

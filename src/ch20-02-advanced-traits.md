## Zaawansowane traity {#advanced-traits}

*Traity* (cechy typów, zbliżone do interfejsów) omówiliśmy po raz pierwszy w
podrozdziale [„Definiowanie wspólnego zachowania za pomocą
traitów”][traits]<!-- ignore --> w rozdziale 10, ale pominęliśmy wtedy
bardziej zaawansowane szczegóły. Teraz, gdy wiesz już więcej o Ruście, możemy
zejść do konkretów.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-placeholder-types-in-trait-definitions-with-associated-types"></a>
<a id="associated-types"></a>

### Definiowanie traitów z typami powiązanymi {#defining-traits-with-associated-types}

*Typy powiązane* (*associated types*) łączą z traitem symbol zastępczy
(*placeholder*) typu, dzięki czemu definicje metod traitu mogą używać tych
typów zastępczych w swoich sygnaturach. Typ implementujący trait określa, jaki
konkretny typ zostanie użyty zamiast typu zastępczego w danej implementacji. W
ten sposób możemy zdefiniować trait, który używa pewnych typów, nie wiedząc
dokładnie, czym te typy są, aż do chwili implementacji traitu.

O większości zaawansowanych mechanizmów z tego rozdziału mówiliśmy, że rzadko
są potrzebne. Typy powiązane plasują się gdzieś pośrodku: używa się ich rzadziej
niż mechanizmów opisanych w pozostałej części książki, ale częściej niż wielu
innych mechanizmów omawianych w tym rozdziale.

Przykładem traitu z typem powiązanym jest trait `Iterator` z biblioteki
standardowej. Typ powiązany nazywa się `Item` i zastępuje typ wartości, po
których iteruje typ implementujący trait `Iterator`. Definicję traitu
`Iterator` pokazuje listing 20-13.

<Listing number="20-13" caption="Definicja traitu `Iterator` z typem powiązanym `Item`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-13/src/lib.rs}}
```

</Listing>

Typ `Item` jest symbolem zastępczym, a definicja metody `next` pokazuje, że
będzie ona zwracać wartości typu `Option<Self::Item>`. Typy implementujące
trait `Iterator` określą konkretny typ dla `Item`, a metoda `next` będzie
zwracać `Option` zawierający wartość tego konkretnego typu.

Typy powiązane mogą się wydawać pojęciem podobnym do typów generycznych
(*generics*), bo te drugie również pozwalają zdefiniować funkcję bez określania,
jakie typy może ona obsługiwać. Aby zbadać różnicę między tymi pojęciami,
przyjrzymy się implementacji traitu `Iterator` dla typu o nazwie `Counter`,
która określa, że typem `Item` jest `u32`:

<Listing file-name="src/lib.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-22-iterator-on-counter/src/lib.rs:ch19}}
```

</Listing>

Ta składnia wydaje się porównywalna ze składnią typów generycznych. Dlaczego
więc po prostu nie zdefiniować traitu `Iterator` z użyciem typów generycznych,
jak w listingu 20-14?

<Listing number="20-14" caption="Hipotetyczna definicja traitu `Iterator` z użyciem typów generycznych">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-14/src/lib.rs}}
```

</Listing>

Różnica polega na tym, że przy typach generycznych, jak w listingu 20-14,
musimy dodawać adnotacje typów w każdej implementacji. Ponieważ możemy też
zaimplementować `Iterator<String> for Counter` albo dla dowolnego innego typu,
moglibyśmy mieć wiele implementacji `Iterator` dla `Counter`. Innymi słowy,
gdy trait ma parametr generyczny, można go zaimplementować dla danego typu
wiele razy, za każdym razem zmieniając konkretne typy generycznych parametrów
typu. Używając metody `next` na `Counter`, musielibyśmy podawać adnotacje
typów, aby wskazać, której implementacji `Iterator` chcemy użyć.

Przy typach powiązanych nie musimy dodawać adnotacji typów, ponieważ nie można
zaimplementować traitu dla danego typu wiele razy. W listingu 20-13, w
definicji z typem powiązanym, możemy wybrać typ `Item` tylko raz, bo może
istnieć tylko jedno `impl Iterator for Counter`. Nie musimy więc wszędzie, gdzie
wywołujemy `next` na `Counter`, określać, że chcemy iteratora wartości `u32`.

Typy powiązane stają się też częścią kontraktu traitu: typy implementujące
trait muszą dostarczyć typ, który zajmie miejsce symbolu zastępczego typu
powiązanego. Typy powiązane często mają nazwę opisującą, jak typ będzie
używany, a udokumentowanie typu powiązanego w dokumentacji API to dobra praktyka.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-generic-type-parameters-and-operator-overloading"></a>

### Domyślne parametry generyczne i przeciążanie operatorów {#using-default-generic-parameters-and-operator-overloading}

Używając generycznych parametrów typu, możemy określić domyślny typ konkretny
dla typu generycznego (*generic type*). Dzięki temu typy implementujące trait
nie muszą podawać typu konkretnego, jeśli typ domyślny im odpowiada. Typ
domyślny określasz przy deklarowaniu typu generycznego za pomocą składni
`<PlaceholderType=ConcreteType>`.

Świetnym przykładem sytuacji, w której ta technika się przydaje, jest
_przeciążanie operatorów_ (*operator overloading*), czyli dostosowywanie
zachowania operatora (np. `+`) w określonych sytuacjach.

Rust nie pozwala tworzyć własnych operatorów ani przeciążać dowolnych
operatorów. Możesz jednak przeciążać operacje i odpowiadające im traity
wymienione w `std::ops`, implementując traity związane z danym operatorem. Na
przykład w listingu 20-15 przeciążamy operator `+`, aby dodawać do siebie dwie
instancje `Point`. Robimy to, implementując trait `Add` dla struktury
(*struct*) `Point`.

<Listing number="20-15" file-name="src/main.rs" caption="Implementacja traitu `Add` przeciążająca operator `+` dla instancji `Point`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-15/src/main.rs}}
```

</Listing>

Metoda `add` dodaje wartości `x` dwóch instancji `Point` oraz wartości `y`
dwóch instancji `Point`, tworząc nowy `Point`. Trait `Add` ma typ powiązany o
nazwie `Output`, który określa typ zwracany przez metodę `add`.

Domyślny typ generyczny w tym kodzie znajduje się w traicie `Add`. Oto jego
definicja:

```rust
trait Add<Rhs=Self> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}
```

Ten kod powinien wyglądać w zasadzie znajomo: trait z jedną metodą i typem
powiązanym. Nowością jest `Rhs=Self`: ta składnia nazywa się _domyślnymi
parametrami typu_ (*default type parameters*). Generyczny parametr typu `Rhs`
(skrót od „right-hand side”, czyli „prawa strona”) określa typ parametru `rhs`
w metodzie `add`. Jeśli przy implementowaniu traitu `Add` nie podamy
konkretnego typu dla `Rhs`, typem `Rhs` będzie domyślnie `Self`, czyli typ, dla
którego implementujemy `Add`.

Implementując `Add` dla `Point`, użyliśmy wartości domyślnej `Rhs`, ponieważ
chcieliśmy dodawać dwie instancje `Point`. Przyjrzyjmy się przykładowi
implementacji traitu `Add`, w którym chcemy dostosować typ `Rhs` zamiast używać
wartości domyślnej.

Mamy dwie struktury, `Millimeters` i `Meters`, przechowujące wartości w różnych
jednostkach. Takie cienkie opakowanie istniejącego typu w inną strukturę nazywa
się _wzorcem newtype_ (*newtype pattern*); opisujemy go dokładniej w
podrozdziale [„Implementowanie zewnętrznych traitów za pomocą wzorca
newtype”][newtype]<!-- ignore -->. Chcemy dodawać wartości w milimetrach do
wartości w metrach i sprawić, by implementacja `Add` poprawnie wykonywała
konwersję. Możemy zaimplementować `Add` dla `Millimeters` z `Meters` jako
`Rhs`, jak w listingu 20-16.

<Listing number="20-16" file-name="src/lib.rs" caption="Implementacja traitu `Add` dla `Millimeters`, pozwalająca dodawać `Millimeters` i `Meters`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-16/src/lib.rs}}
```

</Listing>

Aby dodawać `Millimeters` i `Meters`, piszemy `impl Add<Meters>`, ustawiając
wartość parametru typu `Rhs` zamiast używać domyślnego `Self`.

Domyślnych parametrów typu będziesz używać na dwa główne sposoby:

1. aby rozszerzyć typ bez psucia istniejącego kodu;
2. aby umożliwić dostosowanie w szczególnych przypadkach, których większość
   użytkowników nie będzie potrzebować.

Trait `Add` z biblioteki standardowej jest przykładem drugiego zastosowania:
zwykle dodajesz do siebie dwa typy tego samego rodzaju, ale trait `Add` daje
możliwość dostosowania wykraczającego poza ten przypadek. Użycie domyślnego
parametru typu w definicji traitu `Add` sprawia, że przez większość czasu nie
musisz podawać dodatkowego parametru. Innymi słowy, odpada trochę szablonowego
kodu (*boilerplate*) w implementacji, co ułatwia korzystanie z traitu.

Pierwsze zastosowanie jest podobne do drugiego, ale działa w odwrotną stronę:
jeśli chcesz dodać parametr typu do istniejącego traitu, możesz nadać mu wartość
domyślną, aby rozszerzyć funkcjonalność traitu bez psucia istniejącego kodu
implementacji.

<!-- Old headings. Do not remove or links may break. -->

<a id="fully-qualified-syntax-for-disambiguation-calling-methods-with-the-same-name"></a>
<a id="disambiguating-between-methods-with-the-same-name"></a>

### Rozróżnianie metod o tej samej nazwie {#disambiguating-between-identically-named-methods}

Nic w Ruście nie zabrania, by trait miał metodę o tej samej nazwie co metoda
innego traitu, ani nie zabrania implementowania obu tych traitów dla jednego
typu. Można też zaimplementować bezpośrednio na typie metodę o tej samej nazwie
co metody z traitów.

Wywołując metody o tej samej nazwie, musisz powiedzieć Rustowi, której z nich
chcesz użyć. Spójrz na kod w listingu 20-17, w którym zdefiniowaliśmy dwa
traity, `Pilot` i `Wizard`, z metodą o nazwie `fly` w każdym z nich. Następnie
implementujemy oba traity dla typu `Human`, który ma już zaimplementowaną
metodę o nazwie `fly`. Każda z metod `fly` robi coś innego.

<Listing number="20-17" file-name="src/main.rs" caption="Dwa traity zdefiniowane z metodą `fly` i zaimplementowane dla typu `Human` oraz metoda `fly` zaimplementowana bezpośrednio na `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-17/src/main.rs:here}}
```

</Listing>

Gdy wywołujemy `fly` na instancji `Human`, kompilator domyślnie wywołuje
metodę zaimplementowaną bezpośrednio na typie, jak pokazuje listing 20-18.

<Listing number="20-18" file-name="src/main.rs" caption="Wywołanie `fly` na instancji `Human`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-18/src/main.rs:here}}
```

</Listing>

Uruchomienie tego kodu wypisze `*waving arms furiously*`, co pokazuje, że Rust
wywołał metodę `fly` zaimplementowaną bezpośrednio na `Human`.

Aby wywołać metody `fly` z traitu `Pilot` albo z traitu `Wizard`, musimy użyć
bardziej jawnej składni, określającej, o którą metodę `fly` nam chodzi. Tę
składnię przedstawia listing 20-19.

<Listing number="20-19" file-name="src/main.rs" caption="Określenie, którą metodę `fly` z którego traitu chcemy wywołać">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-19/src/main.rs:here}}
```

</Listing>

Podanie nazwy traitu przed nazwą metody wyjaśnia Rustowi, którą implementację
`fly` chcemy wywołać. Moglibyśmy też napisać `Human::fly(&person)`, co jest
równoważne użytemu w listingu 20-19 `person.fly()`, ale jest nieco dłuższe do
napisania, jeśli nie musimy rozstrzygać niejednoznaczności.

Uruchomienie tego kodu wypisuje:

```console
{{#include ../listings/ch20-advanced-features/listing-20-19/output.txt}}
```

Ponieważ metoda `fly` przyjmuje parametr `self`, gdybyśmy mieli dwa _typy_,
które implementują jeden _trait_, Rust mógłby ustalić, której implementacji
traitu użyć, na podstawie typu `self`.

Jednak funkcje powiązane (*associated functions*), które nie są metodami, nie
mają parametru `self`. Gdy wiele typów lub traitów definiuje funkcje niebędące
metodami o tej samej nazwie, Rust nie zawsze wie, o który typ ci chodzi, chyba
że użyjesz w pełni kwalifikowanej składni (*fully qualified syntax*). Na
przykład w listingu 20-20 tworzymy trait dla schroniska dla zwierząt, które
chce nadawać wszystkim szczeniętom imię Spot. Tworzymy trait `Animal` z
powiązaną funkcją niebędącą metodą o nazwie `baby_name`. Trait `Animal` jest
zaimplementowany dla struktury `Dog`, na której bezpośrednio definiujemy także
powiązaną funkcję niebędącą metodą `baby_name`.

<Listing number="20-20" file-name="src/main.rs" caption="Trait z funkcją powiązaną i typ z funkcją powiązaną o tej samej nazwie, który również implementuje ten trait">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-20/src/main.rs}}
```

</Listing>

Kod nadający wszystkim szczeniętom imię Spot implementujemy w funkcji
powiązanej `baby_name` zdefiniowanej na `Dog`. Typ `Dog` implementuje również
trait `Animal`, który opisuje właściwości wspólne dla wszystkich zwierząt. Młode psy
nazywa się szczeniętami, co wyraża implementacja traitu `Animal` dla `Dog` w
funkcji `baby_name` powiązanej z traitem `Animal`.

W `main` wywołujemy funkcję `Dog::baby_name`, która wywołuje funkcję powiązaną
zdefiniowaną bezpośrednio na `Dog`. Ten kod wypisuje:

```console
{{#include ../listings/ch20-advanced-features/listing-20-20/output.txt}}
```

Nie o taki wynik nam chodziło. Chcemy wywołać funkcję `baby_name` będącą
częścią traitu `Animal`, który zaimplementowaliśmy dla `Dog`, tak aby kod
wypisał `A baby dog is called a puppy`. Technika podawania nazwy traitu,
której użyliśmy w listingu 20-19, tu nie pomoże: jeśli zmienimy `main` na kod z
listingu 20-21, dostaniemy błąd kompilacji.

<Listing number="20-21" file-name="src/main.rs" caption="Próba wywołania funkcji `baby_name` z traitu `Animal`, przy czym Rust nie wie, której implementacji użyć">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-21/src/main.rs:here}}
```

</Listing>

Ponieważ `Animal::baby_name` nie ma parametru `self`, a mogą istnieć inne typy
implementujące trait `Animal`, Rust nie potrafi ustalić, której implementacji
`Animal::baby_name` chcemy. Dostaniemy taki błąd kompilatora:

```console
{{#include ../listings/ch20-advanced-features/listing-20-21/output.txt}}
```

Aby rozstrzygnąć niejednoznaczność i powiedzieć Rustowi, że chcemy użyć
implementacji `Animal` dla `Dog`, a nie implementacji `Animal` dla jakiegoś
innego typu, musimy użyć w pełni kwalifikowanej składni. Listing 20-22
pokazuje, jak jej użyć.

<Listing number="20-22" file-name="src/main.rs" caption="Użycie w pełni kwalifikowanej składni, aby wskazać, że chcemy wywołać funkcję `baby_name` z traitu `Animal` w implementacji dla `Dog`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-22/src/main.rs:here}}
```

</Listing>

Podajemy Rustowi adnotację typu w nawiasach ostrych, która wskazuje, że chcemy
wywołać metodę `baby_name` z traitu `Animal` w implementacji dla `Dog`: mówimy
w ten sposób, że w tym wywołaniu funkcji chcemy traktować typ `Dog` jako
`Animal`. Teraz ten kod wypisze to, czego chcemy:

```console
{{#include ../listings/ch20-advanced-features/listing-20-22/output.txt}}
```

Ogólnie w pełni kwalifikowana składnia jest zdefiniowana następująco:

```rust,ignore
<Type as Trait>::function(receiver_if_method, next_arg, ...);
```

W przypadku funkcji powiązanych, które nie są metodami, nie byłoby `receiver`:
byłaby tylko lista pozostałych argumentów. W pełni kwalifikowanej składni
można używać wszędzie, gdzie wywołujesz funkcje lub metody. Wolno jednak
pominąć każdą część tej składni, którą Rust może ustalić na podstawie innych
informacji w programie. Tej bardziej rozwlekłej składni potrzebujesz tylko w
sytuacjach, gdy istnieje wiele implementacji o tej samej nazwie i Rust
potrzebuje pomocy, by ustalić, którą implementację chcesz wywołać.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-supertraits-to-require-one-traits-functionality-within-another-trait"></a>

### Używanie supertraitów {#using-supertraits}

Czasem możesz napisać definicję traitu, która zależy od innego traitu: chcesz,
by typ implementujący pierwszy trait musiał implementować również drugi.
Robisz to po to, by definicja twojego traitu mogła korzystać z elementów
powiązanych drugiego traitu. Trait, na którym opiera się definicja twojego
traitu, nazywa się _supertraitem_ (*supertrait*) twojego traitu.

Załóżmy na przykład, że chcemy utworzyć trait `OutlinePrint` z metodą
`outline_print`, która wypisze podaną wartość sformatowaną tak, by była
otoczona ramką z gwiazdek. Jeśli więc struktura `Point` implementuje trait
`Display` z biblioteki standardowej tak, że daje on `(x, y)`, to wywołanie
`outline_print` na instancji `Point` z wartościami `1` dla `x` i `3` dla `y`
powinno wypisać:

```text
**********
*        *
* (1, 3) *
*        *
**********
```

W implementacji metody `outline_print` chcemy korzystać z funkcjonalności
traitu `Display`. Musimy więc określić, że trait `OutlinePrint` będzie działał
tylko dla typów, które również implementują `Display` i zapewniają
funkcjonalność potrzebną `OutlinePrint`. Możemy to zrobić w definicji traitu,
pisząc `OutlinePrint: Display`. Ta technika przypomina dodanie do traitu
ograniczenia traitu (*trait bound*). Listing 20-23 pokazuje implementację
traitu `OutlinePrint`.

<Listing number="20-23" file-name="src/main.rs" caption="Implementacja traitu `OutlinePrint`, który wymaga funkcjonalności z `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-23/src/main.rs:here}}
```

</Listing>

Ponieważ określiliśmy, że `OutlinePrint` wymaga traitu `Display`, możemy użyć
funkcji `to_string`, która jest automatycznie zaimplementowana dla każdego
typu implementującego `Display`. Gdybyśmy spróbowali użyć `to_string` bez
dodania dwukropka i traitu `Display` po nazwie traitu, dostalibyśmy błąd
informujący, że w bieżącym zasięgu (*scope*) nie znaleziono metody o nazwie
`to_string` dla typu `&Self`.

Zobaczmy, co się stanie, gdy spróbujemy zaimplementować `OutlinePrint` dla
typu, który nie implementuje `Display`, takiego jak struktura `Point`:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/src/main.rs:here}}
```

</Listing>

Dostajemy błąd informujący, że `Display` jest wymagany, ale nie został
zaimplementowany:

```console
{{#include ../listings/ch20-advanced-features/no-listing-02-impl-outlineprint-for-point/output.txt}}
```

Aby to naprawić, implementujemy `Display` dla `Point` i spełniamy w ten sposób
ograniczenie, którego wymaga `OutlinePrint`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-03-impl-display-for-point/src/main.rs:here}}
```

</Listing>

Teraz implementacja traitu `OutlinePrint` dla `Point` skompiluje się
pomyślnie i możemy wywołać `outline_print` na instancji `Point`, aby wyświetlić
ją w ramce z gwiazdek.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-newtype-pattern-to-implement-external-traits-on-external-types"></a>
<a id="using-the-newtype-pattern-to-implement-external-traits"></a>

### Implementowanie zewnętrznych traitów za pomocą wzorca newtype {#implementing-external-traits-with-the-newtype-pattern}

W podrozdziale [„Implementowanie traitu dla
typu”][implementing-a-trait-on-a-type]<!-- ignore --> w rozdziale 10
wspomnieliśmy o regule sieroty (*orphan rule*), zgodnie z którą możemy
zaimplementować trait dla typu tylko wtedy, gdy trait lub typ (albo oba) są
lokalne dla naszego *crate’a* (jednostki kompilacji w Ruście). To ograniczenie
można obejść za pomocą wzorca newtype, który polega na utworzeniu nowego typu w
postaci struktury krotkowej (*tuple struct*). (Struktury krotkowe omówiliśmy w
podrozdziale [„Tworzenie różnych typów za pomocą struktur
krotkowych”][tuple-structs]<!-- ignore --> w rozdziale 5.) Struktura krotkowa
będzie miała jedno pole i będzie cienkim opakowaniem typu, dla którego chcemy
zaimplementować trait. Typ opakowujący jest wtedy lokalny dla naszego crate’a i
możemy zaimplementować dla niego trait. Termin _newtype_ pochodzi z języka
programowania Haskell. Używanie tego wzorca nie wiąże się z żadnym kosztem
wydajności w czasie działania, a typ opakowujący jest usuwany w czasie
kompilacji (*compile-time*).

Załóżmy na przykład, że chcemy zaimplementować `Display` dla `Vec<T>`, czego
reguła sieroty nie pozwala zrobić bezpośrednio, ponieważ trait `Display` i typ
`Vec<T>` są zdefiniowane poza naszym crate’em. Możemy utworzyć strukturę
`Wrapper` przechowującą instancję `Vec<T>`, a następnie zaimplementować
`Display` dla `Wrapper` i użyć wartości `Vec<T>`, jak w listingu 20-24.

<Listing number="20-24" file-name="src/main.rs" caption="Utworzenie typu `Wrapper` wokół `Vec<String>` w celu zaimplementowania `Display`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-24/src/main.rs}}
```

</Listing>

Implementacja `Display` używa `self.0`, aby uzyskać dostęp do wewnętrznego
`Vec<T>`, ponieważ `Wrapper` jest strukturą krotkową, a `Vec<T>` jest
elementem o indeksie 0 w krotce. Następnie możemy korzystać z funkcjonalności
traitu `Display` na `Wrapper`.

Wadą tej techniki jest to, że `Wrapper` to nowy typ, więc nie ma metod
wartości, którą przechowuje. Musielibyśmy zaimplementować wszystkie metody
`Vec<T>` bezpośrednio na `Wrapper` tak, by delegowały do `self.0`, co
pozwoliłoby traktować `Wrapper` dokładnie jak `Vec<T>`. Gdybyśmy chcieli, aby
nowy typ miał wszystkie metody typu wewnętrznego, rozwiązaniem byłoby
zaimplementowanie traitu `Deref` dla `Wrapper` tak, by zwracał typ wewnętrzny
(implementowanie traitu `Deref` omawialiśmy w podrozdziale [„Traktowanie
inteligentnych wskaźników jak zwykłych referencji”][smart-pointer-deref]<!--
ignore --> w rozdziale 15). Gdybyśmy nie chcieli, aby typ `Wrapper` miał
wszystkie metody typu wewnętrznego – na przykład żeby ograniczyć zachowanie
typu `Wrapper` – musielibyśmy ręcznie zaimplementować tylko te metody, których
faktycznie potrzebujemy.

Wzorzec newtype przydaje się również wtedy, gdy traity nie wchodzą w grę.
Zmieńmy temat i przyjrzyjmy się kilku zaawansowanym sposobom pracy z systemem
typów Rusta.

{{#quiz ../quizzes/ch19-03-advanced-traits.toml}}

[newtype]: ch20-02-advanced-traits.html#implementing-external-traits-with-the-newtype-pattern
[implementing-a-trait-on-a-type]: ch10-02-traits.html#implementing-a-trait-on-a-type
[traits]: ch10-02-traits.html
[smart-pointer-deref]: ch15-02-deref.html#treating-smart-pointers-like-regular-references
[tuple-structs]: ch05-01-defining-structs.html#creating-different-types-with-tuple-structs

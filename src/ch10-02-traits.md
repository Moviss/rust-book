<!-- Old headings. Do not remove or links may break. -->

<a id="traits-defining-shared-behavior"></a>

## Definiowanie wspólnego zachowania za pomocą traitów {#defining-shared-behavior-with-traits}

_Trait_ (cecha typu, zbliżona do interfejsu) definiuje funkcjonalność,
którą ma dany typ i którą może współdzielić z innymi typami. Za pomocą traitów
możemy w abstrakcyjny sposób definiować wspólne zachowanie. Za pomocą
_ograniczeń traitów_ (*trait bounds*) możemy określić, że typ generyczny może
być dowolnym typem, który ma określone zachowanie.

> Uwaga: traity są podobne do mechanizmu nazywanego w innych językach często
> _interfejsami_ (*interfaces*), choć różnią się od niego w kilku kwestiach.

### Definiowanie traitu {#defining-a-trait}

Zachowanie typu składa się z metod, które możemy na nim wywołać. Różne typy
współdzielą to samo zachowanie, jeśli na każdym z nich możemy wywołać te same
metody. Definicje traitów są sposobem grupowania sygnatur metod w celu
zdefiniowania zestawu zachowań potrzebnych do osiągnięcia jakiegoś celu.

Załóżmy na przykład, że mamy kilka struktur (*struct*) przechowujących różne
rodzaje i ilości tekstu: strukturę `NewsArticle`, która przechowuje artykuł
prasowy nadesłany z określonego miejsca, oraz `SocialPost`, który może mieć
najwyżej 280 znaków, a do tego metadane wskazujące, czy jest to nowy post,
udostępnienie (*repost*), czy odpowiedź na inny post.

Chcemy napisać crate biblioteczny (*crate* to jednostka kompilacji w Ruście)
agregatora mediów o nazwie `aggregator`, który potrafi wyświetlać podsumowania
danych przechowywanych w instancji `NewsArticle` lub `SocialPost`. Potrzebujemy
więc podsumowania z każdego typu, a poprosimy o nie, wywołując na instancji
metodę `summarize`. Listing 10-12 pokazuje definicję publicznego traitu
`Summary`, który wyraża to zachowanie.

<Listing number="10-12" file-name="src/lib.rs" caption="Trait `Summary` składający się z zachowania zapewnianego przez metodę `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-12/src/lib.rs}}
```

</Listing>

Deklarujemy tu trait za pomocą słowa kluczowego (*keyword*) `trait`, po którym
podajemy nazwę traitu, czyli w tym przypadku `Summary`. Deklarujemy też trait
jako `pub`, aby crate’y zależne od tego crate’a również mogły z niego korzystać,
co zobaczymy w kilku przykładach. W nawiasach klamrowych deklarujemy sygnatury
metod opisujące zachowania typów implementujących ten trait; tutaj jest to
`fn summarize(&self) -> String`.

Po sygnaturze metody, zamiast podawać implementację w nawiasach klamrowych,
stawiamy średnik. Każdy typ implementujący ten trait musi zapewnić własne
zachowanie w ciele metody. Kompilator wymusi, aby każdy typ, który ma trait
`Summary`, miał zdefiniowaną metodę `summarize` dokładnie z tą sygnaturą.

Trait może mieć w swoim ciele wiele metod: sygnatury metod wypisuje się po
jednej w wierszu, a każdy wiersz kończy się średnikiem.

### Implementowanie traitu dla typu {#implementing-a-trait-on-a-type}

Skoro zdefiniowaliśmy już oczekiwane sygnatury metod traitu `Summary`, możemy
go zaimplementować dla typów w naszym agregatorze mediów. Listing 10-13 pokazuje
implementację traitu `Summary` dla struktury `NewsArticle`, która do utworzenia
wartości zwracanej przez `summarize` używa nagłówka, autora i miejsca. Dla
struktury `SocialPost` definiujemy `summarize` jako nazwę użytkownika, po której
następuje cały tekst posta, zakładając, że treść posta jest już ograniczona do
280 znaków.

<Listing number="10-13" file-name="src/lib.rs" caption="Implementacja traitu `Summary` dla typów `NewsArticle` i `SocialPost`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-13/src/lib.rs:here}}
```

</Listing>

Implementowanie traitu dla typu przypomina implementowanie zwykłych metod.
Różnica polega na tym, że po `impl` podajemy nazwę traitu, który chcemy
zaimplementować, potem słowo kluczowe `for`, a następnie nazwę typu, dla którego
chcemy ten trait zaimplementować. W bloku `impl` umieszczamy sygnatury metod
zdefiniowane w definicji traitu. Zamiast stawiać średnik po każdej sygnaturze,
używamy nawiasów klamrowych i wypełniamy ciało metody konkretnym zachowaniem,
jakie metody traitu mają mieć dla danego typu.

Skoro biblioteka zaimplementowała już trait `Summary` dla `NewsArticle` i
`SocialPost`, użytkownicy crate’a mogą wywoływać metody traitu na instancjach
`NewsArticle` i `SocialPost` tak samo, jak wywołujemy zwykłe metody. Jedyna
różnica polega na tym, że użytkownik musi wprowadzić do zasięgu (*scope*) nie
tylko typy, lecz także trait. Oto przykład, jak crate binarny mógłby użyć
naszego crate’a bibliotecznego `aggregator`:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-01-calling-trait-method/src/main.rs}}
```

Ten kod wypisuje `1 new post: horse_ebooks: of course, as you probably already
know, people`.

Inne crate’y zależne od crate’a `aggregator` również mogą wprowadzić trait
`Summary` do zasięgu, aby zaimplementować `Summary` dla własnych typów. Warto
zwrócić uwagę na jedno ograniczenie: trait możemy zaimplementować dla typu tylko
wtedy, gdy trait, typ albo oba są lokalne dla naszego crate’a. Na przykład
możemy zaimplementować traity z biblioteki standardowej, takie jak `Display`,
dla własnego typu, takiego jak `SocialPost`, w ramach funkcjonalności naszego
crate’a `aggregator`, ponieważ typ `SocialPost` jest lokalny dla crate’a
`aggregator`. Możemy też zaimplementować `Summary` dla `Vec<T>` w naszym
crate’cie `aggregator`, ponieważ trait `Summary` jest lokalny dla crate’a
`aggregator`.

Nie możemy jednak implementować zewnętrznych traitów dla zewnętrznych typów. Na
przykład nie możemy zaimplementować traitu `Display` dla `Vec<T>` w naszym
crate’cie `aggregator`, ponieważ zarówno `Display`, jak i `Vec<T>` są
zdefiniowane w bibliotece standardowej i nie są lokalne dla crate’a
`aggregator`. To ograniczenie jest częścią właściwości nazywanej _spójnością_
(*coherence*), a dokładniej _regułą sieroty_ (*orphan rule*), nazwaną tak,
ponieważ brakuje typu-rodzica. Ta reguła gwarantuje, że cudzy kod nie zepsuje
twojego kodu i odwrotnie. Bez niej dwa crate’y mogłyby zaimplementować ten sam
trait dla tego samego typu, a Rust nie wiedziałby, której implementacji użyć.

<!-- Old headings. Do not remove or links may break. -->

<a id="default-implementations"></a>

### Używanie implementacji domyślnych {#using-default-implementations}

Czasem przydaje się domyślne zachowanie dla niektórych lub wszystkich metod
traitu, zamiast wymagać implementacji wszystkich metod w każdym typie. Wtedy,
implementując trait dla konkretnego typu, możemy zachować albo nadpisać
domyślne zachowanie każdej metody.

W listingu 10-14 określamy domyślny łańcuch znaków (*string*) dla metody
`summarize` traitu `Summary`, zamiast tylko definiować sygnaturę metody, jak
zrobiliśmy w listingu 10-12.

<Listing number="10-14" file-name="src/lib.rs" caption="Definicja traitu `Summary` z domyślną implementacją metody `summarize`">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-14/src/lib.rs:here}}
```

</Listing>

Aby podsumowywać instancje `NewsArticle` za pomocą implementacji domyślnej,
podajemy pusty blok `impl`: `impl Summary for NewsArticle {}`.

Choć nie definiujemy już metody `summarize` bezpośrednio dla `NewsArticle`,
zapewniliśmy implementację domyślną i określiliśmy, że `NewsArticle`
implementuje trait `Summary`. Dzięki temu nadal możemy wywołać metodę
`summarize` na instancji `NewsArticle`, na przykład tak:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-02-calling-default-impl/src/main.rs:here}}
```

Ten kod wypisuje `New article available! (Read more...)`.

Utworzenie implementacji domyślnej nie wymaga od nas żadnych zmian w
implementacji `Summary` dla `SocialPost` z listingu 10-13. Wynika to z tego, że
składnia nadpisywania implementacji domyślnej jest taka sama jak składnia
implementowania metody traitu, która nie ma implementacji domyślnej.

Implementacje domyślne mogą wywoływać inne metody tego samego traitu, nawet
jeśli te metody nie mają implementacji domyślnej. W ten sposób trait może
zapewniać wiele użytecznej funkcjonalności, wymagając od typów implementujących
określenia tylko niewielkiej jej części. Na przykład moglibyśmy zdefiniować
trait `Summary` tak, aby miał metodę `summarize_author`, której implementacja
jest wymagana, a następnie zdefiniować metodę `summarize` z implementacją
domyślną, która wywołuje metodę `summarize_author`:

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:here}}
```

Aby użyć tej wersji `Summary`, przy implementowaniu traitu dla typu wystarczy
zdefiniować `summarize_author`:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/lib.rs:impl}}
```

Po zdefiniowaniu `summarize_author` możemy wywoływać `summarize` na instancjach
struktury `SocialPost`, a domyślna implementacja `summarize` wywoła podaną przez
nas definicję `summarize_author`. Ponieważ zaimplementowaliśmy
`summarize_author`, trait `Summary` dał nam zachowanie metody `summarize` bez
konieczności pisania dodatkowego kodu. Wygląda to tak:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-03-default-impl-calls-other-methods/src/main.rs:here}}
```

Ten kod wypisuje `1 new post: (Read more from @horse_ebooks...)`.

Zwróć uwagę, że z implementacji nadpisującej daną metodę nie można wywołać
domyślnej implementacji tej samej metody.

{{#quiz ../quizzes/ch10-02-traits-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="traits-as-parameters"></a>

### Używanie traitów jako parametrów {#using-traits-as-parameters}

Skoro już wiesz, jak definiować i implementować traity, możemy sprawdzić, jak
używać traitów do definiowania funkcji przyjmujących wiele różnych typów.
Użyjemy traitu `Summary`, który zaimplementowaliśmy dla typów `NewsArticle` i
`SocialPost` w listingu 10-13, aby zdefiniować funkcję `notify`. Wywołuje ona
metodę `summarize` na swoim parametrze `item`, który jest jakiegoś typu
implementującego trait `Summary`. W tym celu używamy składni `impl Trait`, o
tak:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-04-traits-as-parameters/src/lib.rs:here}}
```

Zamiast konkretnego typu parametru `item` podajemy słowo kluczowe `impl` i nazwę
traitu. Ten parametr przyjmuje dowolny typ, który implementuje wskazany trait.
W ciele `notify` możemy wywoływać na `item` dowolne metody pochodzące z traitu
`Summary`, na przykład `summarize`. Możemy wywołać `notify` i przekazać dowolną
instancję `NewsArticle` lub `SocialPost`. Kod, który wywoła tę funkcję z
jakimkolwiek innym typem, na przykład `String` lub `i32`, się nie skompiluje,
ponieważ te typy nie implementują `Summary`.

<!-- Old headings. Do not remove or links may break. -->

<a id="fixing-the-largest-function-with-trait-bounds"></a>

#### Składnia ograniczeń traitów {#trait-bound-syntax}

Składnia `impl Trait` sprawdza się w prostych przypadkach, ale w rzeczywistości
jest lukrem składniowym dla dłuższej formy, nazywanej _ograniczeniem traitu_;
wygląda ona tak:

```rust,ignore
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}
```

Ta dłuższa forma jest równoważna przykładowi z poprzedniego podrozdziału, ale
bardziej rozwlekła. Ograniczenia traitów umieszczamy przy deklaracji parametru
typu generycznego, po dwukropku, w nawiasach ostrych.

Składnia `impl Trait` jest wygodna i w prostych przypadkach daje bardziej
zwięzły kod, natomiast pełniejsza składnia ograniczeń traitów pozwala wyrazić
bardziej złożone przypadki. Możemy na przykład mieć dwa parametry
implementujące `Summary`. Ze składnią `impl Trait` wygląda to tak:

```rust,ignore
pub fn notify(item1: &impl Summary, item2: &impl Summary) {
```

Użycie `impl Trait` jest właściwe, jeśli chcemy, aby ta funkcja pozwalała
parametrom `item1` i `item2` mieć różne typy (o ile oba typy implementują
`Summary`). Jeśli jednak chcemy wymusić, aby oba parametry miały ten sam typ,
musimy użyć ograniczenia traitu, o tak:

```rust,ignore
pub fn notify<T: Summary>(item1: &T, item2: &T) {
```

Typ generyczny `T`, podany jako typ parametrów `item1` i `item2`, ogranicza
funkcję tak, że konkretny typ wartości przekazanych jako argumenty `item1` i
`item2` musi być taki sam.

<!-- Old headings. Do not remove or links may break. -->

<a id="specifying-multiple-trait-bounds-with-the--syntax"></a>

#### Wiele ograniczeń traitów ze składnią `+` {#multiple-trait-bounds-with-the--syntax}

Możemy też podać więcej niż jedno ograniczenie traitu. Załóżmy, że chcemy, aby
`notify` używała na `item` zarówno formatowania wyświetlania, jak i
`summarize`: w definicji `notify` określamy, że `item` musi implementować
zarówno `Display`, jak i `Summary`. Możemy to zrobić za pomocą składni `+`:

```rust,ignore
pub fn notify(item: &(impl Summary + Display)) {
```

Składnia `+` działa również z ograniczeniami traitów dla typów generycznych:

```rust,ignore
pub fn notify<T: Summary + Display>(item: &T) {
```

Przy tych dwóch ograniczeniach traitów ciało `notify` może wywołać `summarize`
i użyć `{}` do sformatowania `item`.

#### Czytelniejsze ograniczenia traitów z klauzulą `where` {#clearer-trait-bounds-with-where-clauses}

Zbyt wiele ograniczeń traitów ma swoje wady. Każdy typ generyczny ma własne
ograniczenia traitów, więc funkcje z wieloma parametrami typów generycznych
mogą zawierać mnóstwo informacji o ograniczeniach traitów między nazwą funkcji
a listą parametrów, przez co sygnatura funkcji staje się trudna do odczytania.
Dlatego Rust ma alternatywną składnię pozwalającą podać ograniczenia traitów w
klauzuli `where` po sygnaturze funkcji. Zamiast pisać tak:

```rust,ignore
fn some_function<T: Display + Clone, U: Clone + Debug>(t: &T, u: &U) -> i32 {
```

możemy użyć klauzuli `where`, o tak:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-07-where-clause/src/lib.rs:here}}
```

Sygnatura tej funkcji jest mniej zagracona: nazwa funkcji, lista parametrów i
typ zwracany są blisko siebie, podobnie jak w funkcji bez wielu ograniczeń
traitów.

### Zwracanie typów implementujących traity {#returning-types-that-implement-traits}

Składni `impl Trait` możemy też użyć w miejscu typu zwracanego, aby zwrócić
wartość jakiegoś typu implementującego trait, jak tutaj:

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-05-returning-impl-trait/src/lib.rs:here}}
```

Używając `impl Summary` jako typu zwracanego, określamy, że funkcja
`returns_summarizable` zwraca jakiś typ implementujący trait `Summary`, bez
podawania nazwy konkretnego typu. W tym przypadku `returns_summarizable`
zwraca `SocialPost`, ale kod wywołujący tę funkcję nie musi o tym wiedzieć.

Możliwość określenia typu zwracanego wyłącznie przez trait, który on
implementuje, jest szczególnie przydatna w kontekście domknięć (*closures*) i
iteratorów, które omawiamy w rozdziale 13. Domknięcia i iteratory tworzą typy
znane tylko kompilatorowi albo typy, których zapisanie jest bardzo długie.
Składnia `impl Trait` pozwala zwięźle określić, że funkcja zwraca jakiś typ
implementujący trait `Iterator`, bez wypisywania bardzo długiego typu.

Składni `impl Trait` możesz jednak używać tylko wtedy, gdy zwracasz jeden typ.
Na przykład ten kod, który zwraca albo `NewsArticle`, albo `SocialPost`, z
typem zwracanym określonym jako `impl Summary`, nie zadziała:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-06-impl-trait-returns-one-type/src/lib.rs:here}}
```

Zwracanie albo `NewsArticle`, albo `SocialPost` jest niedozwolone ze względu na
ograniczenia sposobu, w jaki składnia `impl Trait` jest zaimplementowana w
kompilatorze. Jak napisać funkcję o takim zachowaniu, omówimy w podrozdziale
[„Używanie obiektów traitów do abstrahowania wspólnego zachowania”][trait-objects]<!-- ignore -->
w rozdziale 18.

### Warunkowe implementowanie metod za pomocą ograniczeń traitów {#using-trait-bounds-to-conditionally-implement-methods}

Używając ograniczenia traitu w bloku `impl` z parametrami typów generycznych,
możemy warunkowo implementować metody dla typów, które implementują wskazane
traity. Na przykład typ `Pair<T>` z listingu 10-15 zawsze implementuje funkcję
`new`, zwracającą nową instancję `Pair<T>` (przypomnij sobie z podrozdziału
[„Składnia metod”][methods]<!-- ignore --> w rozdziale 5, że `Self` jest
aliasem typu dla typu bloku `impl`, czyli w tym przypadku `Pair<T>`). Jednak w
następnym bloku `impl` `Pair<T>` implementuje metodę `cmp_display` tylko
wtedy, gdy jego typ wewnętrzny `T` implementuje trait `PartialOrd`, który
umożliwia porównywanie, _oraz_ trait `Display`, który umożliwia wypisywanie.

<Listing number="10-15" file-name="src/lib.rs" caption="Warunkowe implementowanie metod typu generycznego w zależności od ograniczeń traitów">

```rust,noplayground
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-15/src/lib.rs}}
```

</Listing>

Możemy też warunkowo zaimplementować trait dla każdego typu, który implementuje
inny trait. Implementacje traitu dla dowolnego typu spełniającego ograniczenia
traitów nazywamy _implementacjami zbiorczymi_ (*blanket implementations*);
biblioteka standardowa Rusta korzysta z nich bardzo często. Na przykład
biblioteka standardowa implementuje trait `ToString` dla każdego typu, który
implementuje trait `Display`. Blok `impl` w bibliotece standardowej wygląda
podobnie do tego kodu:

```rust,ignore
impl<T: Display> ToString for T {
    // --snip--
}
```

Ponieważ biblioteka standardowa ma tę implementację zbiorczą, możemy wywołać
metodę `to_string`, zdefiniowaną przez trait `ToString`, na każdym typie
implementującym trait `Display`. Na przykład liczby całkowite możemy zamienić
na odpowiadające im wartości `String` w ten sposób, ponieważ liczby całkowite
implementują `Display`:

```rust
let s = 3.to_string();
```

Implementacje zbiorcze widać w dokumentacji traitu w sekcji „Implementors”.

Traity i ograniczenia traitów pozwalają pisać kod, który używa parametrów typów
generycznych, aby ograniczyć powielanie kodu, a zarazem wskazać kompilatorowi,
że typ generyczny ma mieć określone zachowanie. Kompilator może wtedy użyć
informacji z ograniczeń traitów, aby sprawdzić, czy wszystkie konkretne typy
używane z naszym kodem zapewniają poprawne zachowanie. W językach typowanych
dynamicznie dostalibyśmy błąd w czasie działania, gdybyśmy wywołali na typie
metodę, której ten typ nie definiuje. Rust przenosi jednak te błędy do czasu
kompilacji (*compile time*), więc musimy naprawić problemy, zanim kod w ogóle
będzie mógł się uruchomić. Co więcej, nie musimy pisać kodu sprawdzającego
zachowanie w czasie działania, ponieważ sprawdziliśmy je już w czasie
kompilacji. Poprawia to wydajność bez rezygnowania z elastyczności typów
generycznych.

{{#quiz ../quizzes/ch10-02-traits-sec2.toml}}

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[methods]: ch05-03-method-syntax.html#method-syntax

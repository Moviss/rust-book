<!-- Old headings. Do not remove or links may break. -->

<a id="using-trait-objects-that-allow-for-values-of-different-types"></a>

## Używanie obiektów traitów do abstrahowania wspólnego zachowania {#using-trait-objects-to-abstract-over-shared-behavior}

W rozdziale 8 wspomnieliśmy, że jednym z ograniczeń wektorów (*vector*) jest to,
że mogą przechowywać elementy tylko jednego typu. W listingu 8-9 obeszliśmy ten
problem, definiując *enum* (typ wyliczeniowy) `SpreadsheetCell` z wariantami do
przechowywania liczb całkowitych, zmiennoprzecinkowych i tekstu. Dzięki temu
mogliśmy przechowywać w każdej komórce dane różnych typów, a mimo to mieć
wektor reprezentujący wiersz komórek. To w zupełności dobre rozwiązanie, gdy
wymienne elementy należą do stałego zbioru typów, który znamy w chwili
kompilacji kodu.

Czasem jednak chcemy, aby użytkownik naszej biblioteki mógł rozszerzać zbiór
typów dopuszczalnych w danej sytuacji. Aby pokazać, jak można to osiągnąć,
utworzymy przykładowe narzędzie do budowania graficznego interfejsu użytkownika
(GUI), które przechodzi przez listę elementów i na każdym z nich wywołuje
metodę `draw`, aby narysować go na ekranie – to powszechna technika w
narzędziach GUI. Utworzymy biblioteczny *crate* (jednostkę kompilacji w
Ruście) o nazwie `gui`, zawierający strukturę biblioteki GUI. Ten crate mógłby
udostępniać kilka typów do użytku, na przykład `Button` lub `TextField`. Poza
tym użytkownicy `gui` będą chcieli tworzyć własne typy, które da się narysować:
jedna osoba może na przykład dodać `Image`, a inna `SelectBox`.

Pisząc bibliotekę, nie jesteśmy w stanie przewidzieć ani zdefiniować
wszystkich typów, które inni programiści mogą chcieć utworzyć. Wiemy jednak, że
`gui` musi śledzić wiele wartości różnych typów i wywoływać metodę `draw` na
każdej z tych wartości. Nie musi wiedzieć, co dokładnie się stanie, gdy
wywołamy metodę `draw`, a jedynie to, że wartość będzie miała tę metodę
dostępną do wywołania.

W języku z dziedziczeniem moglibyśmy w tym celu zdefiniować klasę o nazwie
`Component` z metodą o nazwie `draw`. Pozostałe klasy, takie jak `Button`,
`Image` i `SelectBox`, dziedziczyłyby po `Component`, a tym samym
odziedziczyłyby metodę `draw`. Każda z nich mogłaby nadpisać metodę `draw`,
aby zdefiniować własne zachowanie, ale framework mógłby traktować wszystkie te
typy tak, jakby były instancjami `Component`, i wywoływać na nich `draw`.
Ponieważ jednak Rust nie ma dziedziczenia, potrzebujemy innego sposobu na
zbudowanie biblioteki `gui`, który pozwoli użytkownikom tworzyć nowe typy
zgodne z tą biblioteką.

### Definiowanie traitu dla wspólnego zachowania {#defining-a-trait-for-common-behavior}

Aby zaimplementować zachowanie, które ma mieć `gui`, zdefiniujemy *trait*
(cechę typu, zbliżoną do interfejsu) o nazwie `Draw` z jedną metodą o nazwie
`draw`. Następnie możemy zdefiniować wektor, który przyjmuje obiekt traitu.
_Obiekt traitu_ (*trait object*) wskazuje zarówno na instancję typu
implementującego wskazany przez nas trait, jak i na tablicę służącą do
wyszukiwania metod traitu dla tego typu w czasie działania programu. Obiekt
traitu tworzymy, podając jakiś rodzaj wskaźnika, na przykład referencję
(*reference*) lub inteligentny wskaźnik (*smart pointer*) `Box<T>`, następnie
słowo kluczowe (*keyword*) `dyn`, a potem odpowiedni trait. (Powód, dla którego
obiekty traitów muszą używać wskaźnika, omówimy w podrozdziale [„Typy o
dynamicznym rozmiarze i trait `Sized`”][dynamically-sized]<!-- ignore --> w
rozdziale 20). Obiektów traitów możemy używać zamiast typu generycznego lub
konkretnego. Wszędzie tam, gdzie użyjemy obiektu traitu, system typów Rusta w
czasie kompilacji (*compile-time*) zagwarantuje, że każda wartość użyta w tym
kontekście będzie implementować trait obiektu traitu. W rezultacie nie musimy
znać wszystkich możliwych typów w czasie kompilacji.

Wspominaliśmy, że w Ruście powstrzymujemy się od nazywania struktur (*struct*)
i enumów „obiektami”, aby odróżnić je od obiektów w innych językach. W
strukturze lub enumie dane w polach struktury i zachowanie w blokach `impl` są
od siebie oddzielone, podczas gdy w innych językach dane i zachowanie połączone
w jedno pojęcie często nazywa się obiektem. Obiekty traitów różnią się od
obiektów w innych językach tym, że nie możemy dodać do obiektu traitu danych.
Obiekty traitów nie są tak ogólnie przydatne jak obiekty w innych językach:
ich konkretnym celem jest umożliwienie abstrahowania wspólnego zachowania.

Listing 18-3 pokazuje, jak zdefiniować trait o nazwie `Draw` z jedną metodą o
nazwie `draw`.

<Listing number="18-3" file-name="src/lib.rs" caption="Definicja traitu `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-03/src/lib.rs}}
```

</Listing>

Ta składnia powinna wyglądać znajomo po naszych rozważaniach o definiowaniu
traitów w rozdziale 10. Dalej pojawia się nowa składnia: listing 18-4
definiuje strukturę o nazwie `Screen`, która przechowuje wektor o nazwie
`components`. Ten wektor jest typu `Box<dyn Draw>`, czyli obiektu traitu;
to typ zastępczy dla dowolnego typu wewnątrz `Box`, który implementuje trait
`Draw`.

<Listing number="18-4" file-name="src/lib.rs" caption="Definicja struktury `Screen` z polem `components` przechowującym wektor obiektów traitów implementujących trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-04/src/lib.rs:here}}
```

</Listing>

W strukturze `Screen` zdefiniujemy metodę o nazwie `run`, która wywoła metodę
`draw` na każdym elemencie `components`, jak pokazano w listingu 18-5.

<Listing number="18-5" file-name="src/lib.rs" caption="Metoda `run` w `Screen`, która wywołuje metodę `draw` na każdym komponencie">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-05/src/lib.rs:here}}
```

</Listing>

Działa to inaczej niż definiowanie struktury, która używa generycznego
parametru typu z ograniczeniami traitów (*trait bounds*). Generyczny parametr
typu można zastąpić tylko jednym typem konkretnym naraz, natomiast obiekty
traitów pozwalają, by w czasie działania programu miejsce obiektu traitu
zajmowało wiele typów konkretnych. Moglibyśmy na przykład zdefiniować
strukturę `Screen` z użyciem typu generycznego (*generic type*) i ograniczenia
traitu, jak w listingu 18-6.

<Listing number="18-6" file-name="src/lib.rs" caption="Alternatywna implementacja struktury `Screen` i jej metody `run` z użyciem typów generycznych i ograniczeń traitów">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-06/src/lib.rs:here}}
```

</Listing>

To ogranicza nas do instancji `Screen`, która ma listę komponentów wyłącznie
typu `Button` albo wyłącznie typu `TextField`. Jeśli zawsze będziesz mieć tylko
jednorodne kolekcje, lepiej użyć typów generycznych (*generics*) i ograniczeń
traitów, ponieważ definicje zostaną w czasie kompilacji poddane monomorfizacji
(*monomorphization*), aby używały typów konkretnych.

Z kolei w podejściu z obiektami traitów jedna instancja `Screen` może
przechowywać `Vec<T>` zawierający zarówno `Box<Button>`, jak i
`Box<TextField>`. Przyjrzyjmy się, jak to działa, a potem omówimy wpływ na
wydajność w czasie działania programu.

### Implementowanie traitu {#implementing-the-trait}

Teraz dodamy kilka typów implementujących trait `Draw`. Dostarczymy typ
`Button`. Ponownie: faktyczna implementacja biblioteki GUI wykracza poza
zakres tej książki, więc metoda `draw` nie będzie miała w ciele żadnej
użytecznej implementacji. Aby wyobrazić sobie, jak mogłaby wyglądać taka
implementacja, przyjmijmy, że struktura `Button` ma pola `width`, `height` i
`label`, jak pokazano w listingu 18-7.

<Listing number="18-7" file-name="src/lib.rs" caption="Struktura `Button` implementująca trait `Draw`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-07/src/lib.rs:here}}
```

</Listing>

Pola `width`, `height` i `label` w `Button` będą się różnić od pól innych
komponentów; na przykład typ `TextField` mógłby mieć te same pola i dodatkowo
pole `placeholder`. Każdy z typów, które chcemy rysować na ekranie, będzie
implementował trait `Draw`, ale w metodzie `draw` będzie używał innego kodu,
aby określić, jak narysować dany typ – tak jak robi to tutaj `Button` (bez
faktycznego kodu GUI, jak wspomnieliśmy). Typ `Button` mógłby na przykład mieć
dodatkowy blok `impl` z metodami związanymi z tym, co się dzieje, gdy
użytkownik kliknie przycisk. Tego rodzaju metody nie będą miały zastosowania
do typów takich jak `TextField`.

Jeśli ktoś korzystający z naszej biblioteki zdecyduje się zaimplementować
strukturę `SelectBox` z polami `width`, `height` i `options`, zaimplementuje
również trait `Draw` dla typu `SelectBox`, jak pokazano w listingu 18-8.

<Listing number="18-8" file-name="src/main.rs" caption="Inny crate, który używa `gui` i implementuje trait `Draw` dla struktury `SelectBox`">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-08/src/main.rs:here}}
```

</Listing>

### Używanie traitu {#using-the-trait}

Użytkownik naszej biblioteki może teraz napisać funkcję `main`, która utworzy
instancję `Screen`. Do instancji `Screen` może dodać `SelectBox` i `Button`,
umieszczając każdy z nich w `Box<T>`, dzięki czemu stają się obiektami traitów.
Następnie może wywołać metodę `run` na instancji `Screen`, która wywoła `draw`
na każdym z komponentów. Listing 18-9 pokazuje tę implementację.

<Listing number="18-9" file-name="src/main.rs" caption="Używanie obiektów traitów do przechowywania wartości różnych typów implementujących ten sam trait">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-09/src/main.rs:here}}
```

</Listing>

Pisząc bibliotekę, nie wiedzieliśmy, że ktoś może dodać typ `SelectBox`, ale
nasza implementacja `Screen` potrafiła obsłużyć nowy typ i go narysować,
ponieważ `SelectBox` implementuje trait `Draw`, co oznacza, że implementuje
metodę `draw`.

Ta koncepcja – zajmowanie się wyłącznie komunikatami, na które wartość
odpowiada, a nie jej konkretnym typem – przypomina koncepcję _typowania
kaczkowego_ (*duck typing*) w językach typowanych dynamicznie: jeśli coś chodzi
jak kaczka i kwacze jak kaczka, to musi być kaczką! W implementacji `run` w
`Screen` z listingu 18-5 `run` nie musi wiedzieć, jaki jest konkretny typ
każdego komponentu. Nie sprawdza, czy komponent jest instancją `Button`, czy
`SelectBox`, tylko wywołuje na nim metodę `draw`. Podając `Box<dyn Draw>` jako
typ wartości w wektorze `components`, określiliśmy, że `Screen` potrzebuje
wartości, na których możemy wywołać metodę `draw`.

Zaletą używania obiektów traitów i systemu typów Rusta do pisania kodu
podobnego do kodu z typowaniem kaczkowym jest to, że nigdy nie musimy w czasie
działania programu sprawdzać, czy wartość implementuje daną metodę, ani
martwić się błędami, gdy wartość nie implementuje metody, a mimo to ją
wywołamy. Rust nie skompiluje naszego kodu, jeśli wartości nie implementują
traitów wymaganych przez obiekty traitów.

Na przykład listing 18-10 pokazuje, co się stanie, jeśli spróbujemy utworzyć
`Screen` z `String` jako komponentem.

<Listing number="18-10" file-name="src/main.rs" caption="Próba użycia typu, który nie implementuje traitu obiektu traitu">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-10/src/main.rs}}
```

</Listing>

Otrzymamy ten błąd, ponieważ `String` nie implementuje traitu `Draw`:

```console
{{#include ../listings/ch18-oop/listing-18-10/output.txt}}
```

Ten błąd informuje nas, że albo przekazujemy do `Screen` coś, czego nie
zamierzaliśmy przekazać, i powinniśmy przekazać inny typ, albo powinniśmy
zaimplementować `Draw` dla `String`, aby `Screen` mógł wywołać na nim `draw`.

<!-- BEGIN INTERVENTION: cce62358-5291-4eb3-84d6-fbc570873ee3 -->

### Obiekty traitów a wnioskowanie typów {#trait-objects-and-type-inference}

Jedną z wad obiektów traitów jest ich współdziałanie z wnioskowaniem typów
(*type inference*). Weźmy na przykład wnioskowanie typów dla `Vec<T>`. Gdy `T`
nie jest obiektem traitu, Rustowi wystarczy znajomość typu jednego elementu
wektora, aby wywnioskować `T`. Dlatego pusty wektor powoduje błąd wnioskowania
typów:

```rust,ignore,does_not_compile
# fn main() {
let v = vec![];
// error[E0282]: type annotations needed for `Vec<T>`
# }
```

Dodanie elementu pozwala jednak Rustowi wywnioskować typ wektora:

```rust,ignore
# fn main() {
let v = vec!["Hello world"];
// ok, v : Vec<&str>
# }
```

W przypadku obiektów traitów wnioskowanie typów jest trudniejsze. Załóżmy na
przykład, że próbujemy wydzielić tablicę `components` z listingu 18-9 do
osobnej zmiennej, w ten sposób:

```rust,ignore,does_not_compile
fn main() {
    let components = vec![
        Box::new(SelectBox { /* .. */ }),
        Box::new(Button { /* .. */ }),
    ];
    let screen = Screen { components };
    screen.run();
}
```

<span class="caption">Listing 18-11: Wydzielenie tablicy components powoduje błąd typu</span>

Po tej refaktoryzacji program przestaje się kompilować! Kompilator odrzuca go
z następującym błędem:

```text
error[E0308]: mismatched types
   --> test.rs:55:14
    |
55  |       Box::new(Button {
    |  _____--------_^
    | |     |
    | |     arguments to this function are incorrect
56  | |       width: 50,
57  | |       height: 10,
58  | |       label: String::from("OK"),
59  | |     }),
    | |_____^ expected `SelectBox`, found `Button`
```

W listingu 18-9 kompilator rozumie, że wektor `components` musi mieć typ
`Vec<Box<dyn Draw>>`, ponieważ jest to określone w definicji struktury
`Screen`. W listingu 18-11 kompilator traci jednak tę informację w miejscu,
w którym definiowana jest zmienna `components`. Aby rozwiązać problem, musisz
dać wskazówkę algorytmowi wnioskowania typów. Możesz to zrobić za pomocą
jawnego rzutowania dowolnego elementu wektora, na przykład tak:

```rust,ignore
let components = vec![
    Box::new(SelectBox { /* .. */ }) as Box<dyn Draw>,
    Box::new(Button { /* .. */ }),
];
```

Albo za pomocą adnotacji typu w wiązaniu let, na przykład tak:

```rust,ignore
let components: Vec<Box<dyn Draw>> = vec![
    Box::new(SelectBox { /* .. */ }),
    Box::new(Button { /* .. */ }),
];
```

Ogólnie warto pamiętać, że w kwestii wnioskowania typów obiekty traitów mogą
pogorszyć wygodę pracy programistów korzystających z API.

<!-- END INTERVENTION: cce62358-5291-4eb3-84d6-fbc570873ee3 -->


<!-- Old headings. Do not remove or links may break. -->

<a id="trait-objects-perform-dynamic-dispatch"></a>

### Dynamiczne wywoływanie metod {#performing-dynamic-dispatch}

Przypomnij sobie z podrozdziału [„Wydajność kodu korzystającego z typów
generycznych”][performance-of-code-using-generics]<!-- ignore --> w rozdziale
10 nasze omówienie procesu monomorfizacji, który kompilator wykonuje na typach
generycznych: kompilator generuje niegeneryczne implementacje funkcji i metod
dla każdego typu konkretnego, którego używamy w miejsce generycznego parametru
typu. Kod powstały w wyniku monomorfizacji realizuje _statyczne wywoływanie_
(*static dispatch*), czyli sytuację, w której kompilator już w czasie
kompilacji wie, którą metodę wywołujesz. Przeciwieństwem jest _dynamiczne
wywoływanie_ (*dynamic dispatch*), w którym kompilator nie jest w stanie
ustalić w czasie kompilacji, którą metodę wywołujesz. W przypadku dynamicznego
wywoływania kompilator generuje kod, który w czasie działania programu ustali,
którą metodę wywołać.

Gdy używamy obiektów traitów, Rust musi stosować dynamiczne wywoływanie.
Kompilator nie zna wszystkich typów, które mogą zostać użyte z kodem
korzystającym z obiektów traitów, więc nie wie, którą metodę zaimplementowaną
dla którego typu wywołać. Zamiast tego w czasie działania programu Rust używa
wskaźników wewnątrz obiektu traitu, aby ustalić, którą metodę wywołać. To
wyszukiwanie wiąże się z kosztem w czasie działania, który nie występuje przy
statycznym wywoływaniu. Dynamiczne wywoływanie uniemożliwia też kompilatorowi
wstawienie kodu metody w miejsce wywołania (*inlining*), co z kolei blokuje
niektóre optymalizacje. Rust ma ponadto reguły określające, gdzie można, a
gdzie nie można używać dynamicznego wywoływania, zwane _zgodnością z dyn_
(*dyn compatibility*). Reguły te wykraczają poza zakres tego omówienia, ale
możesz przeczytać o nich więcej [w dokumentacji Rust
Reference][dyn-compatibility]<!-- ignore -->. Zyskaliśmy jednak dodatkową
elastyczność w kodzie, który napisaliśmy w listingu 18-5, i mogliśmy ją
wykorzystać w listingu 18-9, więc jest to kompromis, który warto rozważyć.

{{#quiz ../quizzes/ch17-02-trait-objects.toml}}

[performance-of-code-using-generics]: ch10-01-syntax.html#performance-of-code-using-generics
[dynamically-sized]: ch20-03-advanced-types.html#dynamically-sized-types-and-the-sized-trait
[dyn-compatibility]: https://doc.rust-lang.org/reference/items/traits.html#dyn-compatibility

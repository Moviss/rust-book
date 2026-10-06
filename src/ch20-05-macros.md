## Makra {#macros}

W całej książce używaliśmy makr takich jak `println!`, ale nie zgłębiliśmy
jeszcze w pełni, czym jest makro i jak działa. Termin _makro_ odnosi się do
całej rodziny mechanizmów Rusta – makr deklaratywnych (*declarative macros*)
tworzonych za pomocą `macro_rules!` oraz trzech rodzajów makr proceduralnych:

- własnych makr `#[derive]`, które określają kod dodawany przez atrybut `derive`
  użyty na strukturach (*structs*) i *enumach* (typach wyliczeniowych);
- makr atrybutowych, które definiują własne atrybuty, możliwe do użycia na
  dowolnym elemencie;
- makr funkcyjnych, które wyglądają jak wywołania funkcji, ale operują na
  tokenach podanych jako ich argument.

Omówimy je po kolei, ale najpierw zastanówmy się, po co w ogóle potrzebujemy
makr, skoro mamy już funkcje.

### Różnice między makrami a funkcjami {#the-difference-between-macros-and-functions}

W gruncie rzeczy makra są sposobem pisania kodu, który pisze inny kod; nazywa się to
_metaprogramowaniem_ (*metaprogramming*). W dodatku C omawiamy atrybut `derive`,
który generuje za ciebie implementację różnych *traitów* (cech typów,
zbliżonych do interfejsów). W całej książce używaliśmy też makr `println!` i
`vec!`. Wszystkie te makra _rozwijają się_ (*expand*), tworząc więcej kodu, niż
napisano ręcznie.

Metaprogramowanie pomaga zmniejszyć ilość kodu, który trzeba napisać i
utrzymywać, a to jest również jedna z ról funkcji. Makra mają jednak pewne dodatkowe
możliwości, których funkcje nie mają.

Sygnatura funkcji musi deklarować liczbę i typ parametrów funkcji. Makra
natomiast mogą przyjmować zmienną liczbę parametrów: możemy wywołać
`println!("hello")` z jednym argumentem albo `println!("hello {}", name)` z
dwoma. Ponadto makra są rozwijane, zanim kompilator zinterpretuje znaczenie
kodu, więc makro może na przykład zaimplementować trait dla danego typu.
Funkcja tego nie potrafi, bo jest wywoływana w czasie działania programu, a
trait musi zostać zaimplementowany w czasie kompilacji (*compile-time*).

Wadą implementowania makra zamiast funkcji jest to, że definicje makr są
bardziej złożone niż definicje funkcji, bo piszesz kod Rusta, który pisze kod
Rusta. Z powodu tej pośredniości (*indirection*) definicje makr są na ogół
trudniejsze do przeczytania, zrozumienia i utrzymania niż definicje funkcji.

Kolejna ważna różnica między makrami a funkcjami polega na tym, że makra
trzeba zdefiniować lub wprowadzić do zasięgu (*scope*) _przed_ ich wywołaniem w
pliku, podczas gdy funkcje można definiować i wywoływać w dowolnym miejscu.

<!-- Old headings. Do not remove or links may break. -->

<a id="declarative-macros-with-macro_rules-for-general-metaprogramming"></a>

### Makra deklaratywne do ogólnego metaprogramowania {#declarative-macros-for-general-metaprogramming}

Najczęściej używaną formą makr w Ruście jest _makro deklaratywne_. Bywają one
też nazywane „makrami przez przykład” (*macros by example*), „makrami
`macro_rules!`” albo po prostu „makrami”. W swojej istocie makra deklaratywne pozwalają napisać coś podobnego do wyrażenia (*expression*)
`match` w Ruście. Jak omówiliśmy w rozdziale 6, wyrażenia `match` to struktury
sterujące, które przyjmują wyrażenie, porównują jego wynikową wartość ze
wzorcami, a następnie wykonują kod powiązany z pasującym wzorcem. Makra również
porównują wartość ze wzorcami powiązanymi z określonym kodem: w tej sytuacji
wartością jest dosłowny kod źródłowy Rusta przekazany do makra, wzorce są
porównywane ze strukturą tego kodu źródłowego, a kod powiązany z każdym
wzorcem, gdy ten pasuje, zastępuje kod przekazany do makra. Wszystko to dzieje
się podczas kompilacji.

Do zdefiniowania makra służy konstrukcja `macro_rules!`. Sprawdźmy, jak używać
`macro_rules!`, przyglądając się definicji makra `vec!`. W rozdziale 8
pokazaliśmy, jak za pomocą makra `vec!` utworzyć nowy wektor (*vector*) z
określonymi wartościami. Na przykład poniższe makro tworzy nowy wektor
zawierający trzy liczby całkowite:

```rust
let v: Vec<u32> = vec![1, 2, 3];
```

Makra `vec!` moglibyśmy też użyć do utworzenia wektora dwóch liczb całkowitych
albo wektora pięciu wycinków łańcucha (*string slices*). Nie dałoby się zrobić
tego samego za pomocą funkcji, bo nie znalibyśmy z góry liczby ani typu
wartości.

Listing 20-35 przedstawia nieco uproszczoną definicję makra `vec!`.

<Listing number="20-35" file-name="src/lib.rs" caption="Uproszczona wersja definicji makra `vec!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-35/src/lib.rs}}
```

</Listing>

> Uwaga: rzeczywista definicja makra `vec!` w bibliotece standardowej zawiera
> kod, który z góry alokuje odpowiednią ilość pamięci. Ten kod jest optymalizacją,
> której tu nie uwzględniamy, aby uprościć przykład.

Adnotacja `#[macro_export]` oznacza, że to makro powinno być dostępne zawsze,
gdy *crate* (jednostka kompilacji w Ruście), w którym je zdefiniowano,
zostanie wprowadzony do zasięgu. Bez tej adnotacji makra nie da się wprowadzić
do zasięgu.

Następnie zaczynamy definicję makra od `macro_rules!` i nazwy definiowanego
makra _bez_ wykrzyknika. Po nazwie, w tym przypadku `vec`, następują nawiasy
klamrowe wyznaczające treść definicji makra.

Struktura treści `vec!` przypomina strukturę wyrażenia `match`. Mamy tu jedno
ramię (*arm*) ze wzorcem `( $( $x:expr ),* )`, po którym następuje `=>` i blok
kodu powiązany z tym wzorcem. Jeśli wzorzec pasuje, zostanie wyemitowany
powiązany z nim blok kodu. Ponieważ to jedyny wzorzec w tym makrze, istnieje
tylko jeden poprawny sposób dopasowania; każdy inny wzorzec spowoduje błąd.
Bardziej złożone makra mają więcej niż jedno ramię.

Poprawna składnia wzorców w definicjach makr różni się od składni wzorców
omówionej w rozdziale 19, bo wzorce makr są dopasowywane do struktury kodu
Rusta, a nie do wartości. Przeanalizujmy, co oznaczają poszczególne elementy
wzorca w listingu 20-29; pełną składnię wzorców makr znajdziesz w [dokumentacji
Rust Reference][ref].

Najpierw używamy pary nawiasów okrągłych, by objąć cały wzorzec. Znakiem dolara
(`$`) deklarujemy w systemie makr zmienną, która będzie zawierać kod Rusta
pasujący do wzorca. Znak dolara jasno pokazuje, że jest to zmienna makra, a nie
zwykła zmienna Rusta. Dalej następuje para nawiasów okrągłych, która
przechwytuje wartości pasujące do wzorca wewnątrz nawiasów, aby użyć ich w
kodzie zastępującym. Wewnątrz `$()` znajduje się `$x:expr`, które dopasowuje
dowolne wyrażenie Rusta i nadaje mu nazwę `$x`.

Przecinek po `$()` oznacza, że między kolejnymi wystąpieniami kodu pasującego do
kodu w `$()` musi pojawić się dosłowny znak przecinka jako separator. `*`
oznacza, że wzorzec dopasowuje zero lub więcej wystąpień tego, co poprzedza `*`.

Gdy wywołujemy to makro jako `vec![1, 2, 3];`, wzorzec `$x` zostaje dopasowany
trzykrotnie, do trzech wyrażeń `1`, `2` i `3`.

Spójrzmy teraz na wzorzec w treści kodu powiązanego z tym ramieniem:
`temp_vec.push()` wewnątrz `$()*` jest generowane dla każdej części pasującej do
`$()` we wzorcu – zero lub więcej razy, zależnie od tego, ile razy wzorzec
zostanie dopasowany. `$x` zostaje zastąpione każdym dopasowanym wyrażeniem. Gdy
wywołamy to makro jako `vec![1, 2, 3];`, kod wygenerowany w miejsce tego
wywołania makra będzie wyglądał tak:

```rust,ignore
{
    let mut temp_vec = Vec::new();
    temp_vec.push(1);
    temp_vec.push(2);
    temp_vec.push(3);
    temp_vec
}
```

Zdefiniowaliśmy makro, które przyjmuje dowolną liczbę argumentów dowolnego typu
i potrafi wygenerować kod tworzący wektor z podanymi elementami.

Aby dowiedzieć się więcej o pisaniu makr, zajrzyj do dokumentacji online lub
innych źródeł, takich jak książka [„The Little Book of Rust Macros”][tlborm],
którą zapoczątkował Daniel Keep, a kontynuuje Lukas Wirth.

### Makra proceduralne do generowania kodu z atrybutów {#procedural-macros-for-generating-code-from-attributes}

Drugą formą makr jest makro proceduralne, które działa bardziej jak funkcja (i
jest rodzajem procedury). _Makra proceduralne_ (*procedural macros*) przyjmują
pewien kod na wejściu, operują na nim i zwracają pewien kod na wyjściu, zamiast
dopasowywać wzorce i zastępować kod innym kodem, jak robią to makra
deklaratywne. Trzy rodzaje makr proceduralnych to własne makra `derive`, makra
atrybutowe i makra funkcyjne; wszystkie działają w podobny sposób.

Przy tworzeniu makr proceduralnych ich definicje muszą znajdować się we własnym
crate’cie o specjalnym typie. Wynika to ze skomplikowanych przyczyn
technicznych, które mamy nadzieję w przyszłości wyeliminować. W listingu 20-36
pokazujemy, jak zdefiniować makro proceduralne; `some_attribute` jest tu
symbolem zastępczym (*placeholder*) oznaczającym użycie konkretnego rodzaju
makra.

<Listing number="20-36" file-name="src/lib.rs" caption="Przykład definiowania makra proceduralnego">

```rust,ignore
use proc_macro::TokenStream;

#[some_attribute]
pub fn some_name(input: TokenStream) -> TokenStream {
}
```

</Listing>

Funkcja definiująca makro proceduralne przyjmuje `TokenStream` na wejściu i
zwraca `TokenStream` na wyjściu. Typ `TokenStream` jest zdefiniowany w crate’cie
`proc_macro`, dołączonym do Rusta, i reprezentuje sekwencję tokenów. To rdzeń
makra: kod źródłowy, na którym operuje makro, tworzy wejściowy `TokenStream`, a
kod generowany przez makro to wyjściowy `TokenStream`. Funkcja ma też
dołączony atrybut, który określa, jaki rodzaj makra proceduralnego tworzymy. W
jednym crate’cie możemy mieć wiele rodzajów makr proceduralnych.

Przyjrzyjmy się różnym rodzajom makr proceduralnych. Zaczniemy od własnego
makra `derive`, a potem wyjaśnimy drobne różnice, którymi odróżniają się
pozostałe formy.

<!-- Old headings. Do not remove or links may break. -->

<a id="how-to-write-a-custom-derive-macro"></a>

### Własne makra `derive` {#custom-derive-macros}

Utwórzmy crate o nazwie `hello_macro`, który definiuje trait o nazwie
`HelloMacro` z jedną funkcją powiązaną (*associated function*) o nazwie
`hello_macro`. Zamiast zmuszać naszych użytkowników do implementowania traitu
`HelloMacro` dla każdego z ich typów, dostarczymy makro proceduralne, dzięki
któremu użytkownicy będą mogli oznaczyć swój typ adnotacją
`#[derive(HelloMacro)]` i otrzymać domyślną implementację funkcji `hello_macro`.
Domyślna implementacja wypisze `Hello, Macro! My name is TypeName!`, gdzie
`TypeName` to nazwa typu, dla którego zdefiniowano ten trait. Innymi słowy,
napiszemy crate, który pozwoli innemu programiście napisać z jego pomocą kod
taki jak w listingu 20-37.

<Listing number="20-37" file-name="src/main.rs" caption="Kod, który użytkownik naszego crate’a będzie mógł napisać, korzystając z naszego makra proceduralnego">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-37/src/main.rs}}
```

</Listing>

Gdy skończymy, ten kod wypisze `Hello, Macro! My name is Pancakes!`. Pierwszym
krokiem jest utworzenie nowego crate’a bibliotecznego w ten sposób:

```console
$ cargo new hello_macro --lib
```

Następnie w listingu 20-38 zdefiniujemy trait `HelloMacro` i jego funkcję
powiązaną.

<Listing file-name="src/lib.rs" number="20-38" caption="Prosty trait, którego użyjemy z makrem `derive`">

```rust,noplayground
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-38/hello_macro/src/lib.rs}}
```

</Listing>

Mamy trait i jego funkcję. Na tym etapie użytkownik naszego crate’a mógłby
zaimplementować ten trait, aby uzyskać pożądaną funkcjonalność, jak w listingu
20-39.

<Listing number="20-39" file-name="src/main.rs" caption="Jak by to wyglądało, gdyby użytkownicy ręcznie implementowali trait `HelloMacro`">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-39/pancakes/src/main.rs}}
```

</Listing>

Musieliby jednak pisać blok implementacji dla każdego typu, którego chcieliby
używać z `hello_macro`; chcemy oszczędzić im tej pracy.

Ponadto nie możemy jeszcze zapewnić funkcji `hello_macro` domyślnej
implementacji, która wypisze nazwę typu, dla którego zaimplementowano trait:
Rust nie ma mechanizmu refleksji, więc nie może sprawdzić nazwy typu w czasie
działania programu. Potrzebujemy makra, które wygeneruje kod w czasie
kompilacji.

Kolejnym krokiem jest zdefiniowanie makra proceduralnego. W chwili pisania tego
tekstu makra proceduralne muszą znajdować się we własnym crate’cie. Być może w
przyszłości to ograniczenie zostanie zniesione. Konwencja nazywania crate’ów i
crate’ów z makrami jest następująca: dla crate’a o nazwie `foo` crate z
własnym makrem proceduralnym `derive` nazywa się `foo_derive`. Utwórzmy nowy
crate o nazwie `hello_macro_derive` wewnątrz naszego projektu `hello_macro`:

```console
$ cargo new hello_macro_derive --lib
```

Nasze dwa crate’y są ściśle powiązane, więc tworzymy crate z makrem
proceduralnym w katalogu crate’a `hello_macro`. Jeśli zmienimy definicję traitu
w `hello_macro`, będziemy musieli zmienić także implementację makra
proceduralnego w `hello_macro_derive`. Oba crate’y trzeba będzie opublikować
osobno, a programiści używający tych crate’ów będą musieli dodać oba jako
zależności i wprowadzić oba do zasięgu. Moglibyśmy zamiast tego sprawić, by
crate `hello_macro` używał `hello_macro_derive` jako zależności i
reeksportował (*re-export*) kod makra proceduralnego. Jednak sposób, w jaki
zorganizowaliśmy projekt, pozwala programistom używać `hello_macro` nawet
wtedy, gdy nie chcą funkcjonalności `derive`.

Musimy zadeklarować crate `hello_macro_derive` jako crate z makrem
proceduralnym. Będziemy też potrzebować funkcjonalności z crate’ów `syn` i
`quote`, jak za chwilę zobaczysz, więc musimy dodać je jako zależności. Dodaj
poniższy fragment do pliku _Cargo.toml_ crate’a `hello_macro_derive`:

<Listing file-name="hello_macro_derive/Cargo.toml">

```toml
{{#include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/Cargo.toml:6:12}}
```

</Listing>

Aby zacząć definiować makro proceduralne, umieść kod z listingu 20-40 w pliku
_src/lib.rs_ crate’a `hello_macro_derive`. Zwróć uwagę, że ten kod nie
skompiluje się, dopóki nie dodamy definicji funkcji `impl_hello_macro`.

<Listing number="20-40" file-name="hello_macro_derive/src/lib.rs" caption="Kod, którego będzie wymagać większość crate’ów z makrami proceduralnymi, aby przetwarzać kod Rusta">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-40/hello_macro/hello_macro_derive/src/lib.rs}}
```

</Listing>

Zauważ, że podzieliliśmy kod na funkcję `hello_macro_derive`, odpowiedzialną za
parsowanie `TokenStream`, i funkcję `impl_hello_macro`, odpowiedzialną za
przekształcanie drzewa składni: dzięki temu pisanie makra proceduralnego jest
wygodniejsze. Kod w funkcji zewnętrznej (tutaj `hello_macro_derive`) będzie
taki sam w niemal każdym crate’cie z makrem proceduralnym, jaki zobaczysz lub
utworzysz. Kod, który umieścisz w treści funkcji wewnętrznej (tutaj
`impl_hello_macro`), będzie się różnił w zależności od przeznaczenia twojego
makra proceduralnego.

Wprowadziliśmy trzy nowe crate’y: `proc_macro`, [`syn`][syn]<!-- ignore --> i
[`quote`][quote]<!-- ignore -->. Crate `proc_macro` jest dołączony do Rusta,
więc nie musieliśmy dodawać go do zależności w _Cargo.toml_. Crate
`proc_macro` to API kompilatora, które pozwala z poziomu naszego kodu odczytywać
kod Rusta i nim manipulować.

Crate `syn` parsuje kod Rusta z łańcucha znaków (*string*) do struktury danych,
na której możemy wykonywać operacje. Crate `quote` zamienia struktury danych
`syn` z powrotem w kod Rusta. Te crate’y znacznie ułatwiają parsowanie
dowolnego kodu Rusta, z jakim możemy chcieć pracować: napisanie pełnego parsera
kodu Rusta nie jest prostym zadaniem.

Funkcja `hello_macro_derive` zostanie wywołana, gdy użytkownik naszej biblioteki
umieści `#[derive(HelloMacro)]` przy typie. Jest to możliwe, ponieważ
oznaczyliśmy tu funkcję `hello_macro_derive` atrybutem `proc_macro_derive` i
podaliśmy nazwę `HelloMacro`, zgodną z nazwą naszego traitu; tej konwencji
przestrzega większość makr proceduralnych.

Funkcja `hello_macro_derive` najpierw przekształca `input` z `TokenStream` w
strukturę danych, którą możemy następnie interpretować i na której możemy
wykonywać operacje. Tu do gry wchodzi `syn`. Funkcja `parse` z `syn` przyjmuje
`TokenStream` i zwraca strukturę `DeriveInput` reprezentującą sparsowany kod
Rusta. Listing 20-41 przedstawia istotne fragmenty struktury `DeriveInput`, którą
otrzymujemy z parsowania łańcucha `struct Pancakes;`.

<Listing number="20-41" caption="Instancja `DeriveInput`, którą otrzymujemy, parsując kod z atrybutem makra z listingu 20-37">

```rust,ignore
DeriveInput {
    // --snip--

    ident: Ident {
        ident: "Pancakes",
        span: #0 bytes(95..103)
    },
    data: Struct(
        DataStruct {
            struct_token: Struct,
            fields: Unit,
            semi_token: Some(
                Semi
            )
        }
    )
}
```

</Listing>

Pola tej struktury pokazują, że sparsowany kod Rusta to struktura jednostkowa z
`ident` (_identyfikatorem_, czyli nazwą) równym `Pancakes`. Struktura ma więcej
pól, opisujących wszelkiego rodzaju kod Rusta; więcej informacji znajdziesz w
[dokumentacji `syn` dla `DeriveInput`][syn-docs].

Wkrótce zdefiniujemy funkcję `impl_hello_macro`, w której zbudujemy nowy kod
Rusta, który chcemy dołączyć. Zanim to jednak zrobimy, zauważ, że wynikiem
naszego makra `derive` również jest `TokenStream`. Zwrócony `TokenStream` jest
dodawany do kodu pisanego przez użytkowników naszego crate’a, więc gdy
skompilują swój crate, otrzymają dodatkową funkcjonalność, którą zapewniamy w
zmodyfikowanym `TokenStream`.

Być może zwróciło twoją uwagę, że wywołujemy tu `unwrap`, aby funkcja
`hello_macro_derive` wywołała panikę (*panic*), jeśli wywołanie funkcji
`syn::parse` się nie powiedzie. Nasze makro proceduralne musi panikować przy
błędach, ponieważ funkcje `proc_macro_derive` muszą zwracać `TokenStream`, a
nie `Result`, aby były zgodne z API makr proceduralnych. Uprościliśmy ten
przykład, używając `unwrap`; w kodzie produkcyjnym należy podawać bardziej
szczegółowe komunikaty o tym, co poszło nie tak, używając `panic!` lub
`expect`.

Skoro mamy już kod, który zamienia oznaczony adnotacją kod Rusta z
`TokenStream` w instancję `DeriveInput`, wygenerujmy kod implementujący trait
`HelloMacro` dla oznaczonego typu, jak pokazano w listingu 20-42.

<Listing number="20-42" file-name="hello_macro_derive/src/lib.rs" caption="Implementacja traitu `HelloMacro` z użyciem sparsowanego kodu Rusta">

```rust,ignore
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-42/hello_macro/hello_macro_derive/src/lib.rs:here}}
```

</Listing>

Za pomocą `ast.ident` otrzymujemy instancję struktury `Ident` zawierającą nazwę
(identyfikator) oznaczonego typu. Struktura z listingu 20-41 pokazuje, że gdy
uruchomimy funkcję `impl_hello_macro` na kodzie z listingu 20-37, otrzymany
`ident` będzie miał pole `ident` o wartości `"Pancakes"`. Zatem zmienna `name`
w listingu 20-42 będzie zawierać instancję struktury `Ident`, która po
wypisaniu da łańcuch `"Pancakes"`, czyli nazwę struktury z listingu 20-37.

Makro `quote!` pozwala zdefiniować kod Rusta, który chcemy zwrócić. Kompilator
oczekuje czegoś innego niż bezpośredni wynik działania makra `quote!`, więc
musimy przekształcić ten wynik w `TokenStream`. Robimy to, wywołując metodę
`into`, która konsumuje tę reprezentację pośrednią i zwraca wartość wymaganego
typu `TokenStream`.

Makro `quote!` zapewnia też bardzo wygodny mechanizm szablonów: możemy wpisać
`#name`, a `quote!` zastąpi to wartością zmiennej `name`. Można nawet stosować
powtórzenia podobnie jak w zwykłych makrach. Dokładne wprowadzenie znajdziesz w
[dokumentacji crate’a `quote`][quote-docs].

Chcemy, aby nasze makro proceduralne generowało implementację naszego traitu
`HelloMacro` dla typu oznaczonego przez użytkownika, który możemy uzyskać za
pomocą `#name`. Implementacja traitu ma jedną funkcję, `hello_macro`, której
treść zawiera funkcjonalność, jaką chcemy zapewnić: wypisanie `Hello, Macro! My
name is`, a następnie nazwy oznaczonego typu.

Użyte tu makro `stringify!` jest wbudowane w Rusta. Przyjmuje ono wyrażenie
Rusta, takie jak `1 + 2`, i w czasie kompilacji zamienia je w literał
łańcuchowy, taki jak `"1 + 2"`. Różni się to od `format!` czy `println!`, które
są makrami obliczającymi wartość wyrażenia, a następnie zamieniającymi wynik w
`String`. Istnieje możliwość, że wejście `#name` będzie wyrażeniem do wypisania
dosłownie, dlatego używamy `stringify!`. Użycie `stringify!` oszczędza też
alokację, bo zamienia `#name` w literał łańcuchowy w czasie kompilacji.

Na tym etapie `cargo build` powinno zakończyć się powodzeniem zarówno w
`hello_macro`, jak i w `hello_macro_derive`. Połączmy te crate’y z kodem z
listingu 20-37, aby zobaczyć makro proceduralne w działaniu! Utwórz nowy
projekt binarny w katalogu _projects_ za pomocą `cargo new pancakes`. Musimy
dodać `hello_macro` i `hello_macro_derive` jako zależności w pliku _Cargo.toml_
crate’a `pancakes`. Jeśli publikujesz swoje wersje `hello_macro` i
`hello_macro_derive` w [crates.io](https://crates.io/)<!-- ignore -->, będą to
zwykłe zależności; jeśli nie, możesz podać je jako zależności `path` w
następujący sposób:

```toml
{{#include ../listings/ch20-advanced-features/no-listing-21-pancakes/pancakes/Cargo.toml:6:8}}
```

Umieść kod z listingu 20-37 w pliku _src/main.rs_ i uruchom `cargo run`:
program powinien wypisać `Hello, Macro! My name is Pancakes!`. Implementacja
traitu `HelloMacro` z makra proceduralnego została dołączona bez potrzeby
implementowania jej przez crate `pancakes`; to `#[derive(HelloMacro)]` dodało
implementację traitu.

Następnie zobaczmy, czym inne rodzaje makr proceduralnych różnią się od
własnych makr `derive`.

### Makra atrybutowe {#attribute-like-macros}

Makra atrybutowe (*attribute-like macros*) są podobne do własnych makr `derive`,
ale zamiast generować kod dla atrybutu `derive`, pozwalają tworzyć nowe
atrybuty. Są też bardziej elastyczne: `derive` działa tylko dla struktur i
enumów, a atrybuty można stosować także do innych elementów, na przykład
funkcji. Oto przykład użycia makra atrybutowego. Załóżmy, że masz atrybut o
nazwie `route`, którym oznaczasz funkcje, korzystając z frameworka aplikacji
webowych:

```rust,ignore
#[route(GET, "/")]
fn index() {
```

Ten atrybut `#[route]` byłby zdefiniowany przez framework jako makro
proceduralne. Sygnatura funkcji definiującej makro wyglądałaby tak:

```rust,ignore
#[proc_macro_attribute]
pub fn route(attr: TokenStream, item: TokenStream) -> TokenStream {
```

Mamy tu dwa parametry typu `TokenStream`. Pierwszy dotyczy zawartości atrybutu:
części `GET, "/"`. Drugi to treść elementu, do którego dołączony jest atrybut:
w tym przypadku `fn index() {}` i reszta treści funkcji.

Poza tym makra atrybutowe działają tak samo jak własne makra `derive`: tworzysz
crate o typie `proc-macro` i implementujesz funkcję, która generuje potrzebny
ci kod!

### Makra funkcyjne {#function-like-macros}

Makra funkcyjne (*function-like macros*) definiują makra, które wyglądają jak
wywołania funkcji. Podobnie jak makra `macro_rules!` są bardziej elastyczne niż
funkcje; mogą na przykład przyjmować nieznaną z góry liczbę argumentów. Jednak
makra `macro_rules!` można definiować wyłącznie za pomocą składni
przypominającej dopasowywanie wzorców, którą omówiliśmy wcześniej w podrozdziale
[„Makra deklaratywne do ogólnego metaprogramowania”][decl]<!-- ignore -->.
Makra funkcyjne przyjmują parametr `TokenStream`, a ich definicja manipuluje
tym `TokenStream` za pomocą kodu Rusta, tak jak w przypadku dwóch pozostałych
rodzajów makr proceduralnych. Przykładem makra funkcyjnego jest makro `sql!`,
które można by wywołać tak:

```rust,ignore
let sql = sql!(SELECT * FROM posts WHERE id=1);
```

To makro parsowałoby umieszczone w nim zapytanie SQL i sprawdzało, czy jest
ono poprawne składniowo, co jest znacznie bardziej złożonym przetwarzaniem, niż
potrafi wykonać makro `macro_rules!`. Makro `sql!` byłoby zdefiniowane tak:

```rust,ignore
#[proc_macro]
pub fn sql(input: TokenStream) -> TokenStream {
```

Ta definicja przypomina sygnaturę własnego makra `derive`: otrzymujemy tokeny
znajdujące się wewnątrz nawiasów i zwracamy kod, który chcieliśmy wygenerować.

{{#quiz ../quizzes/ch19-06-macros.toml}}

## Podsumowanie {#summary}

Uff! Masz teraz w swoim zestawie narzędzi kilka mechanizmów Rusta, których
zapewne nie będziesz często używać, ale będziesz wiedzieć, że są dostępne w
bardzo szczególnych sytuacjach. Wprowadziliśmy kilka złożonych tematów, dzięki
czemu, gdy napotkasz je w sugestiach w komunikatach o błędach lub w kodzie
innych osób, rozpoznasz te koncepcje i tę składnię. Traktuj ten rozdział jako
punkt odniesienia, który poprowadzi cię do rozwiązań.

Następnie wykorzystamy w praktyce wszystko, o czym mówiliśmy w całej książce, i
zrealizujemy jeszcze jeden projekt!

[ref]: https://doc.rust-lang.org/reference/macros-by-example.html
[tlborm]: https://veykril.github.io/tlborm/
[syn]: https://crates.io/crates/syn
[quote]: https://crates.io/crates/quote
[syn-docs]: https://docs.rs/syn/2.0/syn/struct.DeriveInput.html
[quote-docs]: https://docs.rs/quote
[decl]: #declarative-macros-with-macro_rules-for-general-metaprogramming

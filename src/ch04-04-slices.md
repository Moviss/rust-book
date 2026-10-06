## Typ wycinka {#the-slice-type}

*Wycinki* (*slices*) pozwalają odwołać się do ciągłej sekwencji elementów w
[kolekcji](ch08-00-common-collections.md) zamiast do całej kolekcji. Wycinek
jest rodzajem referencji (*reference*), a więc wskaźnikiem niebędącym
właścicielem danych.

Żeby pokazać, do czego przydają się wycinki, rozwiążmy mały problem
programistyczny: napiszmy funkcję, która przyjmuje łańcuch znaków (*string*)
złożony ze słów rozdzielonych spacjami i zwraca pierwsze słowo, jakie w nim
znajdzie. Jeśli funkcja nie znajdzie w łańcuchu spacji, cały łańcuch musi być
jednym słowem, więc należy zwrócić go w całości. Bez wycinków sygnaturę tej
funkcji moglibyśmy zapisać tak:

```rust,ignore
fn first_word(s: &String) -> ?
```

Funkcja `first_word` przyjmuje jako parametr `&String`. Nie potrzebujemy
własności (*ownership*) łańcucha, więc to w porządku. Ale co powinniśmy zwrócić? Nie mamy
właściwie sposobu, żeby mówić o *części* łańcucha. Moglibyśmy jednak zwrócić
indeks końca słowa, wyznaczonego przez spację. Spróbujmy tego, jak pokazuje
listing 4-7.

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:here}}
```

<span class="caption">Listing 4-7: Funkcja `first_word`, która zwraca indeks
bajtu w parametrze typu `String`</span>

Musimy przejść przez `String` element po elemencie i sprawdzić, czy dana
wartość jest spacją, dlatego zamieniamy nasz `String` na tablicę bajtów za
pomocą metody `as_bytes`:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:as_bytes}}
```

Następnie tworzymy iterator po tablicy bajtów za pomocą metody `iter`:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:iter}}
```

Iteratory omówimy dokładniej w [rozdziale 13][ch13]<!-- ignore -->. Na razie
wystarczy wiedzieć, że `iter` to metoda, która zwraca kolejne elementy
kolekcji, a `enumerate` opakowuje wynik `iter` i zwraca każdy element jako
część krotki (*tuple*). Pierwszym elementem krotki zwracanej przez `enumerate`
jest indeks, a drugim referencja do elementu. To nieco wygodniejsze niż
samodzielne obliczanie indeksu.

Ponieważ metoda `enumerate` zwraca krotkę, możemy ją zdestrukturyzować za
pomocą wzorców. Wzorce omówimy szerzej w [rozdziale 6][ch6]<!-- ignore -->. W
pętli `for` podajemy wzorzec, w którym `i` oznacza indeks z krotki, a `&item`
pojedynczy bajt z krotki. Ponieważ `.iter().enumerate()` daje nam referencję
do elementu, we wzorcu używamy `&`.

Wewnątrz pętli `for` szukamy bajtu oznaczającego spację, korzystając ze
składni literału bajtowego. Jeśli znajdziemy spację, zwracamy jej pozycję. W
przeciwnym razie zwracamy długość łańcucha, używając `s.len()`:

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-07/src/main.rs:inside_for}}
```

Mamy teraz sposób na znalezienie indeksu końca pierwszego słowa w łańcuchu,
ale jest pewien problem. Zwracamy sam `usize`, a ta liczba ma sens tylko w
kontekście `&String`. Innymi słowy, ponieważ jest to wartość oddzielna od
`String`, nie ma gwarancji, że w przyszłości nadal będzie poprawna. Weźmy
program z listingu 4-8, który używa funkcji `first_word` z listingu 4-7.

<span class="filename">Plik: src/main.rs</span>

```aquascope,interpreter+permissions,boundaries,stepper,horizontal
fn first_word(s: &String) -> usize {
    let bytes = s.as_bytes();

    for (i, &item) in bytes.iter().enumerate() {
        if item == b' ' {
            return i;
        }
    }

    s.len()
}

fn main() {
    let mut s = String::from("hello world");`(focus)`
    let word = first_word(&s);`[]`
    s.clear();`[]``{}`    
}
``` 

<span class="caption">Listing 4-8: Zapisanie wyniku wywołania funkcji
`first_word`, a następnie zmiana zawartości `String`</span>

Ten program kompiluje się bez błędów, ponieważ po wywołaniu `first_word`
zmienna `s` zachowuje uprawnienie (*permission*) do zapisu. Ponieważ `word` w
ogóle nie jest powiązane ze stanem `s`, `word` nadal zawiera wartość `5`.
Moglibyśmy użyć tej wartości `5` razem ze zmienną `s`, żeby spróbować wydobyć
pierwsze słowo, ale byłby to błąd, bo zawartość `s` zmieniła się od chwili,
gdy zapisaliśmy `5` w `word`.

Pilnowanie, żeby indeks w `word` nie rozjechał się z danymi w `s`, jest żmudne
i podatne na błędy! Zarządzanie takimi indeksami staje się jeszcze bardziej
kruche, gdy napiszemy funkcję `second_word`. Jej sygnatura musiałaby wyglądać
tak:

```rust,ignore
fn second_word(s: &String) -> (usize, usize) {
```

Teraz śledzimy indeks początkowy *i* końcowy, a do tego mamy jeszcze więcej
wartości, które obliczono na podstawie danych w określonym stanie, ale które w
ogóle nie są z tym stanem związane. Krążą nam po programie trzy niepowiązane
zmienne, które trzeba utrzymywać w zgodności.

Na szczęście Rust ma rozwiązanie tego problemu: wycinki łańcuchów.

### Wycinki łańcuchów {#string-slices}

*Wycinek łańcucha* (*string slice*) to referencja do części `String`. Wygląda
tak:

```aquascope,interpreter
#fn main() {
let s = String::from("hello world");

let hello: &str = &s[0..5];
let world: &str = &s[6..11];
let s2: &String = &s; `[]`
#}
```

Zamiast referencji do całego `String` (jak `s2`) `hello` jest referencją do
fragmentu `String`, określonego dodatkowym zapisem `[0..5]`. Wycinki tworzymy
za pomocą zakresu w nawiasach kwadratowych, podając
`[starting_index..ending_index]`, gdzie `starting_index` to pierwsza pozycja
w wycinku, a `ending_index` to pozycja o jeden większa od ostatniej pozycji w
wycinku.

Wycinki są szczególnym rodzajem referencji, ponieważ są „grubymi” wskaźnikami
(*fat pointers*), czyli wskaźnikami z metadanymi. Tutaj metadaną jest
długość wycinka. Możemy ją zobaczyć, jeśli zmienimy wizualizację tak, żeby
zajrzeć do wnętrza struktur danych Rusta:

```aquascope,interpreter,concreteTypes,hideCode
fn main() {
    let s = String::from("hello world");

    let hello: &str = &s[0..5];
    let world: &str = &s[6..11];
    let s2: &String = &s; // not a slice, for comparison
    `[]`
}
```

Zauważ, że zmienne `hello` i `world` mają pola `ptr` i `len`, które razem
wyznaczają podkreślone obszary łańcucha na stercie (*heap*). Widać tu też, jak
naprawdę wygląda `String`: łańcuch to wektor bajtów (`Vec<u8>`), który zawiera
długość `len` oraz bufor `buf` ze wskaźnikiem `ptr` i pojemnością `cap`.

Ponieważ wycinki są referencjami, zmieniają też uprawnienia do danych, do
których się odwołują. Zauważ na przykład poniżej, że gdy `hello` zostaje
utworzone jako wycinek `s`, zmienna `s` traci uprawnienia do zapisu i
własności:

```aquascope,permissions,stepper,boundaries
fn main() {
    let mut s = String::from("hello");
    let hello: &str = &s[0..5];
    println!("{hello}");
    s.push_str(" world");
}
```

#### Składnia zakresów {#range-syntax}

Jeśli w składni zakresów `..` w Ruście chcesz zacząć od indeksu zero, możesz
pominąć wartość przed dwiema kropkami. Innymi słowy, te zapisy są równoważne:

```rust
let s = String::from("hello");

let slice = &s[0..2];
let slice = &s[..2];
```

Na tej samej zasadzie, jeśli wycinek obejmuje ostatni bajt `String`, możesz
pominąć końcową liczbę. Te zapisy są więc równoważne:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[3..len];
let slice = &s[3..];
```

Możesz też pominąć obie wartości, żeby wziąć wycinek całego łańcucha. Te
zapisy są więc równoważne:

```rust
let s = String::from("hello");

let len = s.len();

let slice = &s[0..len];
let slice = &s[..];
```

> Uwaga: indeksy zakresu wycinka łańcucha muszą wypadać na prawidłowych
> granicach znaków UTF-8. Jeśli spróbujesz utworzyć wycinek łańcucha w środku
> znaku wielobajtowego, program zakończy się błędem. Na potrzeby wprowadzenia
> wycinków łańcuchów zakładamy w tej sekcji wyłącznie znaki ASCII; dokładniejsze
> omówienie obsługi UTF-8 znajdziesz w podrozdziale
> [„Przechowywanie tekstu zakodowanego w UTF-8 w łańcuchach”][strings]<!-- ignore -->
> w rozdziale 8.

#### Przepisanie `first_word` z użyciem wycinków łańcuchów {#rewriting-first_word-with-string-slices}

Mając to wszystko na uwadze, przepiszmy `first_word` tak, żeby zwracała
wycinek. Typ oznaczający „wycinek łańcucha” zapisujemy jako `&str`:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/no-listing-18-first-word-slice/src/main.rs:here}}
```

Indeks końca słowa uzyskujemy tak samo jak w listingu 4-7: szukając
pierwszego wystąpienia spacji. Gdy znajdziemy spację, zwracamy wycinek
łańcucha, używając początku łańcucha i indeksu spacji jako indeksów
początkowego i końcowego.

Teraz, gdy wywołujemy `first_word`, dostajemy z powrotem jedną wartość,
związaną z danymi, na których się opiera. Wartość ta składa się z referencji
do punktu początkowego wycinka i liczby elementów w wycinku.

Zwracanie wycinka sprawdziłoby się też w funkcji `second_word`:

```rust,ignore
fn second_word(s: &String) -> &str {
```

Mamy teraz proste API, którego znacznie trudniej użyć źle, bo kompilator
zapewni, że referencje do `String` pozostaną poprawne. Pamiętasz błąd w
programie z listingu 4-8, gdy uzyskaliśmy indeks końca pierwszego słowa, a
potem wyczyściliśmy łańcuch, przez co indeks stał się nieprawidłowy? Ten kod
był logicznie niepoprawny, ale nie zgłaszał od razu żadnych błędów. Problemy
ujawniłyby się później, gdybyśmy dalej próbowali używać indeksu pierwszego
słowa z opróżnionym łańcuchem. Wycinki sprawiają, że taki błąd jest
niemożliwy, i dużo wcześniej informują nas o problemie w kodzie. Na przykład:

<span class="filename">Plik: src/main.rs</span>

```aquascope,permissions,boundaries,stepper,shouldFail
#fn first_word(s: &String) -> &str {
#    let bytes = s.as_bytes();
#
#    for (i, &item) in bytes.iter().enumerate() {
#        if item == b' ' {
#            return &s[0..i];
#        }
#    }
#
#    &s[..]
#}
fn main() {
    let mut s = String::from("hello world");
    let word = first_word(&s);`(focus,paths:s)`
    s.clear();`{}`
    println!("the first word is: {}", word);
}
```

Widać, że wywołanie `first_word` odbiera teraz zmiennej `s` uprawnienie do
zapisu, co uniemożliwia wywołanie `s.clear()`. Oto błąd kompilatora:

```console
{{#include ../listings/ch04-understanding-ownership/no-listing-19-slice-error/output.txt}}
```

Przypomnij sobie z zasad pożyczania (*borrowing*), że jeśli mamy do czegoś
niemutowalną referencję, nie możemy jednocześnie wziąć referencji mutowalnej
(*mutable*). Ponieważ `clear` musi skrócić `String`, potrzebuje referencji
mutowalnej. `println!` po wywołaniu `clear` używa referencji z `word`, więc
niemutowalna referencja musi w tym miejscu nadal być aktywna. Rust nie
pozwala, żeby mutowalna referencja w `clear` i niemutowalna referencja w
`word` istniały jednocześnie, więc kompilacja kończy się niepowodzeniem. Rust
nie tylko ułatwił korzystanie z naszego API, ale też wyeliminował całą klasę
błędów w czasie kompilacji (*compile-time*)!

#### Literały łańcuchowe są wycinkami {#string-literals-are-slices}

Wspominaliśmy już, że literały łańcuchowe są przechowywane wewnątrz pliku
binarnego. Teraz, gdy znamy wycinki, możemy właściwie zrozumieć literały
łańcuchowe:

```rust
let s = "Hello, world!";
```

Typem `s` jest tu `&str`: to wycinek wskazujący na konkretne miejsce w pliku
binarnym. Dlatego też literały łańcuchowe są niemutowalne – `&str` jest
niemutowalną referencją.

#### Wycinki łańcuchów jako parametry {#string-slices-as-parameters}

Skoro wiesz, że wycinki można brać zarówno z literałów, jak i z wartości
`String`, możemy jeszcze raz ulepszyć `first_word` – tym razem jej sygnaturę:

```rust,ignore
fn first_word(s: &String) -> &str {
```

Bardziej doświadczony rustowiec (*Rustacean*) napisałby zamiast tego
sygnaturę z listingu 4-9, bo pozwala ona używać tej samej funkcji zarówno dla
wartości `&String`, jak i `&str`.

```rust,ignore
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:here}}
```

<span class="caption">Listing 4-9: Ulepszenie funkcji `first_word` przez
użycie wycinka łańcucha jako typu parametru `s`</span>

Jeśli mamy wycinek łańcucha, możemy przekazać go bezpośrednio. Jeśli mamy
`String`, możemy przekazać wycinek tego `String` albo referencję do `String`.
Ta elastyczność wykorzystuje *deref coercion* (automatyczną konwersję przez
dereferencję) – mechanizm, który omówimy w podrozdziale
[„Używanie deref coercion w funkcjach i metodach”][deref-coercions]<!--ignore-->
w rozdziale 15.

Gdy funkcja przyjmuje wycinek łańcucha zamiast referencji do `String`, nasze
API staje się bardziej ogólne i użyteczne, a nie tracimy żadnej
funkcjonalności:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch04-understanding-ownership/listing-04-09/src/main.rs:usage}}
```

### Inne wycinki {#other-slices}

Wycinki łańcuchów, jak można się domyślić, dotyczą tylko łańcuchów. Istnieje jednak
również ogólniejszy typ wycinka. Weźmy taką tablicę:

```rust
let a = [1, 2, 3, 4, 5];
```

Tak jak możemy chcieć odwołać się do części łańcucha, możemy chcieć odwołać
się do części tablicy. Robimy to tak:

```rust
let a = [1, 2, 3, 4, 5];

let slice = &a[1..3];

assert_eq!(slice, &[2, 3]);
```

Ten wycinek ma typ `&[i32]`. Działa tak samo jak wycinki łańcuchów: przechowuje
referencję do pierwszego elementu i długość. Takiego rodzaju wycinków będziesz
używać dla najróżniejszych innych kolekcji. Kolekcje te omówimy szczegółowo,
gdy będziemy mówić o wektorach w rozdziale 8.

{{#quiz ../quizzes/ch04-04-slices.toml}}

## Podsumowanie {#summary}

Wycinki to szczególny rodzaj referencji, które odwołują się do podzakresów
sekwencji, takiej jak łańcuch znaków czy wektor. W czasie działania programu
wycinek jest reprezentowany jako „gruby” wskaźnik, który zawiera wskaźnik na
początek zakresu i długość zakresu. Jedną z zalet wycinków w porównaniu z
zakresami opartymi na indeksach jest to, że wycinek nie może zostać
unieważniony, gdy jest używany.

[ch13]: ch13-02-iterators.html
[ch6]: ch06-02-match.html#patterns-that-bind-to-values
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[deref-coercions]: ch15-02-deref.html#implicit-deref-coercions-with-functions-and-methods

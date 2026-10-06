## Typy danych {#data-types}

Każda wartość w Ruście ma określony _typ danych_ (*data type*), który mówi
Rustowi, z jakimi danymi ma do czynienia, żeby wiedział, jak z nimi pracować.
Przyjrzymy się dwóm podzbiorom typów danych: typom skalarnym i złożonym.

Pamiętaj, że Rust jest językiem _statycznie typowanym_ (*statically typed*), co
oznacza, że musi znać typy wszystkich zmiennych w czasie kompilacji
(*compile-time*). Kompilator zwykle potrafi wywnioskować, jakiego typu chcemy
użyć, na podstawie wartości i sposobu, w jaki jej używamy. Gdy możliwych typów
jest wiele, jak wtedy, gdy w sekcji
[„Porównywanie odpowiedzi z sekretną liczbą”][comparing-the-guess-to-the-secret-number]<!-- ignore -->
w rozdziale 2 konwertowaliśmy `String` na typ liczbowy za pomocą `parse`, musimy
dodać adnotację typu (*type annotation*), na przykład tak:

```rust
let guess: u32 = "42".parse().expect("Not a number!");
```

Jeśli nie dodamy adnotacji typu `: u32` widocznej w powyższym kodzie, Rust
wyświetli następujący błąd, który oznacza, że kompilator potrzebuje od nas
więcej informacji, żeby wiedzieć, jakiego typu chcemy użyć:

```console
{{#include ../listings/ch03-common-programming-concepts/output-only-01-no-type-annotations/output.txt}}
```

Przy innych typach danych zobaczysz inne adnotacje typów.

### Typy skalarne {#scalar-types}

Typ _skalarny_ (*scalar*) reprezentuje pojedynczą wartość. Rust ma cztery
podstawowe typy skalarne: liczby całkowite, liczby zmiennoprzecinkowe, wartości
logiczne i znaki. Być może znasz je z innych języków programowania. Zobaczmy, jak
działają w Ruście.

#### Typy całkowitoliczbowe {#integer-types}

_Liczba całkowita_ (*integer*) to liczba bez części ułamkowej. W rozdziale 2
użyliśmy jednego typu całkowitoliczbowego, typu `u32`. Ta deklaracja typu
oznacza, że powiązana z nią wartość powinna być liczbą całkowitą bez znaku (typy
całkowitoliczbowe ze znakiem zaczynają się od `i` zamiast `u`), która zajmuje 32
bity. Tabela 3-1 pokazuje wbudowane typy całkowitoliczbowe w Ruście. Do
zadeklarowania typu wartości całkowitej możemy użyć dowolnego z tych wariantów.

<span class="caption">Tabela 3-1: Typy całkowitoliczbowe w Ruście</span>

| Długość  | Ze znakiem  | Bez znaku |
| ------- | ------- | -------- |
| 8 bitów   | `i8`    | `u8`     |
| 16 bitów  | `i16`   | `u16`    |
| 32 bity  | `i32`   | `u32`    |
| 64 bity  | `i64`   | `u64`    |
| 128 bitów | `i128`  | `u128`   |
| Zależna od architektury | `isize` | `usize`  |

Każdy wariant może być ze znakiem albo bez znaku i ma jawnie określony rozmiar.
Określenia _ze znakiem_ (*signed*) i _bez znaku_ (*unsigned*) mówią o tym, czy
liczba może być ujemna – innymi słowy, czy liczba musi mieć przy sobie znak (ze
znakiem), czy zawsze będzie dodatnia i dlatego można ją zapisać bez znaku (bez
znaku). To tak jak z zapisywaniem liczb na papierze: gdy znak ma znaczenie,
liczbę zapisuje się ze znakiem plus albo minus; gdy jednak można bezpiecznie
założyć, że liczba jest dodatnia, zapisuje się ją bez znaku. Liczby ze znakiem
są przechowywane w [kodzie uzupełnień do dwóch][twos-complement]<!-- ignore
-->.

Każdy wariant ze znakiem może przechowywać liczby od −(2<sup>n − 1</sup>) do
2<sup>n − 1</sup> − 1 włącznie, gdzie _n_ to liczba bitów używanych przez ten
wariant. Zatem `i8` może przechowywać liczby od −(2<sup>7</sup>) do
2<sup>7</sup> − 1, czyli od −128 do 127. Warianty bez znaku mogą przechowywać
liczby od 0 do 2<sup>n</sup> − 1, więc `u8` może przechowywać liczby od 0 do
2<sup>8</sup> − 1, czyli od 0 do 255.

Ponadto typy `isize` i `usize` zależą od architektury komputera, na którym
działa program: mają 64 bity na architekturze 64-bitowej i 32 bity na
architekturze 32-bitowej.

Literały całkowitoliczbowe możesz zapisywać w dowolnej z postaci pokazanych w
tabeli 3-2. Zauważ, że literały liczbowe, które mogą mieć kilka typów
liczbowych, dopuszczają przyrostek typu, taki jak `57u8`, wskazujący typ.
W literałach liczbowych można też używać `_` jako wizualnego separatora, który
ułatwia czytanie liczby, np. `1_000` ma tę samą wartość, co zapis `1000`.

<span class="caption">Tabela 3-2: Literały całkowitoliczbowe w Ruście</span>

| Literał liczbowy  | Przykład       |
| ---------------- | ------------- |
| Dziesiętny          | `98_222`      |
| Szesnastkowy              | `0xff`        |
| Ósemkowy            | `0o77`        |
| Dwójkowy           | `0b1111_0000` |
| Bajtowy (tylko `u8`) | `b'A'`        |

Skąd więc wiadomo, jakiego typu całkowitoliczbowego użyć? Jeśli nie masz
pewności, domyślne wybory Rusta są zwykle dobrym punktem wyjścia: domyślnym
typem całkowitoliczbowym jest `i32`. Typów `isize` i `usize` używa się głównie
do indeksowania różnego rodzaju kolekcji.

> ##### Przepełnienie liczby całkowitej {#integer-overflow}
>
> Załóżmy, że masz zmienną typu `u8`, która może przechowywać wartości od 0
> do 255. Jeśli spróbujesz zmienić wartość tej zmiennej na wartość spoza tego
> zakresu, np. 256, nastąpi _przepełnienie liczby całkowitej_ (*integer
> overflow*), co może skutkować jednym z dwóch zachowań. Gdy kompilujesz w
> trybie debugowania, Rust dodaje sprawdzenia przepełnienia, które w takiej
> sytuacji wywołują w czasie działania _panikę_ (*panic*) programu. W Ruście
> mówi się, że program _panikuje_ (*panicking*), gdy kończy działanie z
> błędem; panikę omówimy dokładniej w sekcji
> [„Błędy nieodwracalne i `panic!`”][unrecoverable-errors-with-panic]<!-- ignore -->
> w rozdziale 9.
>
> Gdy kompilujesz w trybie wydania z flagą `--release`, Rust _nie_ dodaje
> sprawdzeń przepełnienia powodujących panikę. Zamiast tego, jeśli dojdzie do
> przepełnienia, Rust wykonuje _zawijanie w kodzie uzupełnień do dwóch_
> (*two’s complement wrapping*). Mówiąc w skrócie, wartości większe od
> maksymalnej wartości, jaką może przechowywać typ, „zawijają się” do minimalnej
> wartości tego typu. W przypadku `u8` wartość 256 staje się 0, wartość 257
> staje się 1 i tak dalej. Program nie spanikuje, ale zmienna będzie miała
> wartość, która prawdopodobnie nie jest tą, której się spodziewasz. Poleganie
> na zawijaniu przy przepełnieniu uważa się za błąd.
>
> Aby jawnie obsłużyć możliwość przepełnienia, możesz użyć następujących rodzin
> metod, które biblioteka standardowa udostępnia dla prymitywnych typów
> liczbowych:
>
> - zawijanie we wszystkich trybach za pomocą metod `wrapping_*`, np.
>   `wrapping_add`;
> - zwrócenie wartości `None` w razie przepełnienia za pomocą metod `checked_*`;
> - zwrócenie wartości wraz z wartością logiczną informującą, czy nastąpiło
>   przepełnienie, za pomocą metod `overflowing_*`;
> - nasycenie, czyli zatrzymanie się na minimalnej lub maksymalnej wartości,
>   za pomocą metod `saturating_*`.

#### Typy zmiennoprzecinkowe {#floating-point-types}

Rust ma też dwa typy prymitywne dla _liczb zmiennoprzecinkowych_
(*floating-point numbers*), czyli liczb z częścią ułamkową. Typy
zmiennoprzecinkowe w Ruście to `f32` i `f64`, o rozmiarach odpowiednio 32 i 64
bitów. Typem domyślnym jest `f64`, ponieważ na współczesnych procesorach działa
mniej więcej tak samo szybko jak `f32`, a zapewnia większą precyzję. Wszystkie
typy zmiennoprzecinkowe są typami ze znakiem.

Oto przykład, który pokazuje liczby zmiennoprzecinkowe w działaniu:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-06-floating-point/src/main.rs}}
```

Liczby zmiennoprzecinkowe są reprezentowane zgodnie ze standardem IEEE-754.

#### Operacje liczbowe {#numeric-operations}

Rust obsługuje dla wszystkich typów liczbowych podstawowe operacje
matematyczne, jakich można się spodziewać: dodawanie, odejmowanie, mnożenie,
dzielenie i resztę z dzielenia. Dzielenie liczb całkowitych obcina wynik w
stronę zera do najbliższej liczby całkowitej. Poniższy kod pokazuje, jak użyć
każdej z operacji liczbowych w instrukcji (*statement*) `let`:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-07-numeric-operations/src/main.rs}}
```

Każde wyrażenie (*expression*) w tych instrukcjach używa operatora
matematycznego i daje w wyniku pojedynczą wartość, która jest następnie
wiązana ze zmienną. [Dodatek B][appendix_b]<!-- ignore --> zawiera listę
wszystkich operatorów dostępnych w Ruście.

#### Typ logiczny {#the-boolean-type}

Podobnie jak w większości innych języków programowania, typ logiczny w Ruście ma
dwie możliwe wartości: `true` i `false`. Wartości logiczne zajmują jeden bajt.
Typ logiczny w Ruście zapisuje się jako `bool`. Na przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-08-boolean/src/main.rs}}
```

Wartości logicznych używa się głównie w konstrukcjach warunkowych, takich jak
wyrażenie `if`. Działanie wyrażeń `if` w Ruście omówimy w sekcji
[„Przepływ sterowania”][control-flow]<!-- ignore -->.

#### Typ znakowy {#the-character-type}

Typ `char` to najbardziej prymitywny typ alfabetyczny w Ruście. Oto kilka
przykładów deklarowania wartości `char`:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-09-char/src/main.rs}}
```

Zauważ, że literały `char` zapisujemy w apostrofach, w odróżnieniu od literałów
łańcuchów znaków (*string*), które zapisuje się w cudzysłowach. Typ `char` w
Ruście ma rozmiar 4 bajtów i reprezentuje skalarną wartość Unicode (*Unicode
scalar value*), co oznacza, że może reprezentować znacznie więcej niż samo
ASCII. Litery z akcentami, znaki chińskie, japońskie i koreańskie, emoji oraz
spacje o zerowej szerokości – to wszystko poprawne wartości `char` w Ruście.
Skalarne wartości Unicode mieszczą się w zakresach od `U+0000` do `U+D7FF` i od
`U+E000` do `U+10FFFF` włącznie. „Znak” nie jest jednak tak naprawdę pojęciem
w Unicode, więc twoje intuicyjne wyobrażenie o tym, czym jest „znak”, może nie
pokrywać się z tym, czym jest `char` w Ruście. Szczegółowo omówimy ten temat w
sekcji
[„Przechowywanie tekstu w UTF-8 za pomocą łańcuchów znaków”][strings]<!-- ignore -->
w rozdziale 8.

{{#quiz ../quizzes/ch03-02-data-types-sec1-scalar.toml}}

### Typy złożone {#compound-types}

_Typy złożone_ (*compound types*) pozwalają zgrupować wiele wartości w jednym
typie. Rust ma dwa prymitywne typy złożone: krotki i tablice.

#### Typ krotki {#the-tuple-type}

_Krotka_ (*tuple*) to ogólny sposób na zgrupowanie kilku wartości różnych typów
w jednym typie złożonym. Krotki mają stałą długość: po zadeklarowaniu nie mogą
się powiększyć ani zmniejszyć.

Krotkę tworzymy, zapisując w nawiasach okrągłych listę wartości rozdzielonych
przecinkami. Każda pozycja w krotce ma swój typ, a typy poszczególnych wartości
w krotce nie muszą być takie same. W tym przykładzie dodaliśmy opcjonalne
adnotacje typów:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-10-tuples/src/main.rs}}
```

Zmienna `tup` jest wiązana z całą krotką, ponieważ krotka jest traktowana jako
pojedynczy element złożony. Aby wydobyć z krotki poszczególne wartości, możemy
użyć dopasowywania wzorców (*pattern matching*) i rozłożyć wartość krotki, na
przykład tak:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-11-destructuring-tuples/src/main.rs}}
```

Ten program najpierw tworzy krotkę i wiąże ją ze zmienną `tup`. Następnie za
pomocą wzorca w `let` bierze `tup` i zamienia ją na trzy osobne zmienne: `x`,
`y` i `z`. Nazywa się to _destrukturyzacją_ (*destructuring*), ponieważ
rozbija pojedynczą krotkę na trzy części. Na koniec program wypisuje wartość
`y`, czyli `6.4`.

Do elementu krotki możemy też odwołać się bezpośrednio, pisząc kropkę (`.`), a
po niej indeks wartości, do której chcemy uzyskać dostęp. Na przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-12-tuple-indexing/src/main.rs}}
```

Ten program tworzy krotkę `x`, a następnie odwołuje się do każdego jej elementu
za pomocą odpowiedniego indeksu. Jak w większości języków programowania,
pierwszy indeks w krotce to 0.

Krotka bez żadnych wartości ma specjalną nazwę: _wartość jednostkowa_ (*unit*).
Zarówno tę wartość, jak i odpowiadający jej typ zapisuje się jako `()`;
reprezentują one pustą wartość albo pusty typ zwracany. Wyrażenia niejawnie
zwracają wartość jednostkową, jeśli nie zwracają żadnej innej wartości.

Możemy też modyfikować poszczególne elementy mutowalnej (*mutable*) krotki. Na
przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
fn main() {
    let mut x: (i32, i32) = (1, 2);
    x.0 = 0;
    x.1 += 5;
}
```

Ten program ustawia pierwszy element na zero i dodaje pięć do drugiego elementu.
Ostateczna wartość `x` to `(0, 7)`.

#### Typ tablicowy {#the-array-type}

Innym sposobem na kolekcję wielu wartości jest _tablica_ (*array*). W
odróżnieniu od krotki każdy element tablicy musi mieć ten sam typ. W odróżnieniu
od tablic w niektórych innych językach tablice w Ruście mają stałą długość.

Wartości tablicy zapisujemy jako listę rozdzieloną przecinkami w nawiasach
kwadratowych:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-13-arrays/src/main.rs}}
```

Tablice są przydatne, gdy chcesz, żeby dane były alokowane na stosie (*stack*),
tak jak w przypadku innych poznanych dotąd typów, a nie na stercie (*heap*)
(stos i stertę omówimy dokładniej w [rozdziale 4][stack-and-heap]<!-- ignore -->),
albo gdy chcesz mieć pewność, że zawsze będziesz mieć stałą liczbę elementów.
Tablica nie jest jednak tak elastyczna jak typ wektora. Wektor to podobny typ
kolekcji udostępniany przez bibliotekę standardową, który _może_ się powiększać
i zmniejszać, ponieważ jego zawartość znajduje się na stercie. Jeśli nie masz
pewności, czy użyć tablicy, czy wektora, najpewniej lepiej wybrać wektor.
[Rozdział 8][vectors]<!-- ignore --> omawia wektory bardziej szczegółowo.

Tablice są jednak bardziej przydatne, gdy wiesz, że liczba elementów nie będzie
musiała się zmieniać. Na przykład gdyby program używał nazw miesięcy,
prawdopodobnie lepiej użyć tablicy niż wektora, ponieważ wiadomo, że zawsze
będzie ona zawierać 12 elementów:

```rust
let months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];
```

Typ tablicy zapisuje się w nawiasach kwadratowych: typ każdego elementu,
średnik, a potem liczba elementów tablicy, o tak:

```rust
let a: [i32; 5] = [1, 2, 3, 4, 5];
```

Tutaj `i32` to typ każdego elementu. Liczba `5` po średniku oznacza, że tablica
zawiera pięć elementów.

Możesz też zainicjalizować tablicę tak, żeby każdy element miał tę samą
wartość. W tym celu podajesz w nawiasach kwadratowych wartość początkową, po
niej średnik, a następnie długość tablicy, jak tutaj:

```rust
let a = [3; 5];
```

Tablica o nazwie `a` będzie zawierać `5` elementów, z których każdy będzie
początkowo mieć wartość `3`. Daje to ten sam efekt co zapis
`let a = [3, 3, 3, 3, 3];`, ale w bardziej zwięzłej formie.

<!-- Old headings. Do not remove or links may break. -->
<a id="accessing-array-elements"></a>

#### Dostęp do elementów tablicy {#array-element-access}

Tablica to pojedynczy fragment pamięci o znanym, stałym rozmiarze, który może
zostać zaalokowany na stosie. Do elementów tablicy możesz odwoływać się za
pomocą indeksowania, o tak:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-14-array-indexing/src/main.rs}}
```

W tym przykładzie zmienna o nazwie `first` otrzyma wartość `1`, ponieważ taka
wartość znajduje się w tablicy pod indeksem `[0]`. Zmienna o nazwie `second`
otrzyma wartość `2` spod indeksu `[1]` tablicy.

#### Nieprawidłowy dostęp do elementu tablicy {#invalid-array-element-access}

Zobaczmy, co się stanie, jeśli spróbujesz odwołać się do elementu tablicy
leżącego za jej końcem. Załóżmy, że uruchamiasz poniższy kod, który podobnie
jak gra w zgadywanie z rozdziału 2 pobiera od użytkownika indeks tablicy:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,panics
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access/src/main.rs}}
```

Ten kod kompiluje się bez błędów. Jeśli uruchomisz go za pomocą `cargo run` i
wpiszesz `0`, `1`, `2`, `3` lub `4`, program wypisze wartość znajdującą się pod
tym indeksem w tablicy. Jeśli zamiast tego wpiszesz liczbę wykraczającą poza
koniec tablicy, np. `10`, zobaczysz taki wynik:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-15-invalid-array-access
cargo run
10
-->

```console
thread 'main' panicked at src/main.rs:19:19:
index out of bounds: the len is 5 but the index is 10
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Program zakończył się błędem czasu działania w miejscu, w którym w operacji
indeksowania użyto nieprawidłowej wartości. Program zakończył działanie z
komunikatem o błędzie i nie wykonał końcowej instrukcji `println!`. Gdy
próbujesz odwołać się do elementu za pomocą indeksowania, Rust sprawdza, czy
podany indeks jest mniejszy od długości tablicy. Jeśli indeks jest większy od
długości tablicy lub jej równy, Rust panikuje. To sprawdzenie musi się odbyć w
czasie działania programu, zwłaszcza w tym przypadku, ponieważ kompilator nie
ma żadnej możliwości, żeby wiedzieć, jaką wartość wpisze użytkownik, gdy później
uruchomi kod.

To przykład działania zasad bezpieczeństwa pamięci w Ruście. W wielu językach
niskiego poziomu takie sprawdzenie nie jest wykonywane i gdy podasz
nieprawidłowy indeks, może dojść do dostępu do nieprawidłowej pamięci. Rust
chroni cię przed tego rodzaju błędem, natychmiast kończąc działanie programu,
zamiast pozwolić na dostęp do pamięci i kontynuować. Rozdział 9 omawia więcej
zagadnień obsługi błędów w Ruście i pokazuje, jak pisać czytelny, bezpieczny
kod, który ani nie panikuje, ani nie pozwala na dostęp do nieprawidłowej
pamięci.

{{#quiz ../quizzes/ch03-02-data-types-sec2-compound.toml}}

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[twos-complement]: https://en.wikipedia.org/wiki/Two%27s_complement
[control-flow]: ch03-05-control-flow.html#control-flow
[strings]: ch08-02-strings.html#storing-utf-8-encoded-text-with-strings
[stack-and-heap]: ch04-01-what-is-ownership.html
[vectors]: ch08-01-vectors.html
[unrecoverable-errors-with-panic]: ch09-01-unrecoverable-errors-with-panic.html
[wrapping]: https://doc.rust-lang.org/std/num/struct.Wrapping.html
[appendix_b]: appendix-02-operators.md

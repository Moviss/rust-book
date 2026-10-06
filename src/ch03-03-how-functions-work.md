## Funkcje {#functions}

Funkcje są w kodzie Rusta wszechobecne. Znasz już jedną z najważniejszych
funkcji w tym języku: funkcję `main`, która jest punktem wejścia wielu
programów. Znasz też słowo kluczowe (*keyword*) `fn`, które pozwala deklarować
nowe funkcje.

W kodzie Rusta nazwy funkcji i zmiennych zapisuje się zwyczajowo w stylu
_snake case_: wszystkie litery są małe, a słowa oddzielają podkreślenia. Oto
program zawierający przykładową definicję funkcji:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-16-functions/src/main.rs}}
```

Funkcję definiujemy w Ruście, wpisując `fn`, a po nim nazwę funkcji i parę
nawiasów okrągłych. Nawiasy klamrowe wskazują kompilatorowi, gdzie zaczyna się i
kończy ciało funkcji.

Każdą zdefiniowaną funkcję możemy wywołać, wpisując jej nazwę, a po niej parę
nawiasów okrągłych. Ponieważ `another_function` jest zdefiniowana w programie,
można ją wywołać z wnętrza funkcji `main`. Zwróć uwagę, że w kodzie źródłowym
zdefiniowaliśmy `another_function` _po_ funkcji `main`; równie dobrze
moglibyśmy ją zdefiniować przed nią. Dla Rusta nie ma znaczenia, gdzie
definiujesz funkcje, liczy się tylko to, by były zdefiniowane gdzieś w zasięgu
(*scope*) widocznym dla wywołującego.

Utwórzmy nowy projekt binarny o nazwie _functions_, by dokładniej przyjrzeć się
funkcjom. Umieść przykład z `another_function` w pliku _src/main.rs_ i uruchom
go. Powinno pojawić się następujące wyjście:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-16-functions/output.txt}}
```

Wiersze wykonują się w kolejności, w jakiej występują w funkcji `main`. Najpierw
wypisywany jest komunikat „Hello, world!”, a potem wywoływana jest
`another_function` i wypisywany jest jej komunikat.

### Parametry {#parameters}

Funkcje możemy definiować z _parametrami_, czyli specjalnymi zmiennymi, które są
częścią sygnatury funkcji. Jeśli funkcja ma parametry, możesz przekazać jej
konkretne wartości tych parametrów. Formalnie konkretne wartości nazywa się
_argumentami_, ale w potocznej rozmowie słów _parametr_ i _argument_ używa się
zamiennie, zarówno na określenie zmiennych w definicji funkcji, jak i
konkretnych wartości przekazywanych przy jej wywołaniu.

W tej wersji `another_function` dodajemy parametr:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/src/main.rs}}
```

Uruchom ten program; powinno pojawić się następujące wyjście:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-17-functions-with-parameters/output.txt}}
```

Deklaracja `another_function` ma jeden parametr o nazwie `x`. Typ `x` określono
jako `i32`. Gdy przekazujemy `5` do `another_function`, makro `println!` wstawia
`5` w miejsce pary nawiasów klamrowych zawierających `x` w łańcuchu
formatującym.

W sygnaturach funkcji _musisz_ deklarować typ każdego parametru. To świadoma
decyzja projektowa Rusta: wymaganie adnotacji typów w definicjach funkcji
sprawia, że kompilator prawie nigdy nie potrzebuje ich w innych miejscach kodu,
by ustalić, o jaki typ ci chodzi. Kompilator może też podawać bardziej pomocne
komunikaty o błędach, jeśli wie, jakich typów oczekuje funkcja.

Definiując kilka parametrów, oddziel ich deklaracje przecinkami, w ten sposób:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/src/main.rs}}
```

Ten przykład tworzy funkcję o nazwie `print_labeled_measurement` z dwoma
parametrami. Pierwszy parametr nazywa się `value` i jest typu `i32`. Drugi
nazywa się `unit_label` i jest typu `char`. Funkcja wypisuje następnie tekst
zawierający zarówno `value`, jak i `unit_label`.

Spróbujmy uruchomić ten kod. Zastąp program znajdujący się obecnie w pliku
_src/main.rs_ projektu _functions_ powyższym przykładem i uruchom go poleceniem
`cargo run`:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-18-functions-with-multiple-parameters/output.txt}}
```

Ponieważ wywołaliśmy funkcję z `5` jako wartością `value` i `'h'` jako wartością
`unit_label`, wyjście programu zawiera te wartości.

{{#quiz ../quizzes/ch03-03-functions-sec1-parameters.toml}}

### Instrukcje i wyrażenia {#statements-and-expressions}

Ciała funkcji składają się z ciągu instrukcji (*statement*), opcjonalnie
zakończonego wyrażeniem (*expression*). Funkcje, które dotąd omówiliśmy, nie
miały wyrażenia końcowego, ale wyrażenie jako część instrukcji już się pojawiło.
Ponieważ Rust jest językiem opartym na wyrażeniach, to ważne rozróżnienie. Inne
języki nie mają takich rozróżnień, przyjrzyjmy się więc, czym są instrukcje i
wyrażenia oraz jak różnice między nimi wpływają na ciała funkcji.

- _Instrukcje_ to polecenia, które wykonują jakąś czynność i nie zwracają
  wartości.
- _Wyrażenia_ obliczają się do wartości wynikowej.

Spójrzmy na kilka przykładów.
Tak naprawdę używaliśmy już instrukcji i wyrażeń. Utworzenie zmiennej i
przypisanie jej wartości słowem kluczowym `let` jest instrukcją. W listingu 3-1
`let y = 6;` jest instrukcją.

<Listing number="3-1" file-name="src/main.rs" caption="Deklaracja funkcji `main` zawierająca jedną instrukcję">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-01/src/main.rs}}
```

</Listing>

Definicje funkcji również są instrukcjami; cały poprzedni przykład sam w sobie
jest instrukcją. (Jak za chwilę zobaczymy, wywołanie funkcji instrukcją już nie
jest).

Instrukcje nie zwracają wartości. Dlatego nie możesz przypisać instrukcji `let`
do innej zmiennej, jak próbuje zrobić poniższy kod; dostaniesz błąd:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/src/main.rs}}
```

Gdy uruchomisz ten program, błąd będzie wyglądał tak:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-19-statements-vs-expressions/output.txt}}
```

Instrukcja `let y = 6` nie zwraca wartości, więc `x` nie ma z czym się związać.
Inaczej jest w innych językach, takich jak C i Ruby, w których przypisanie
zwraca przypisaną wartość. W tych językach możesz napisać `x = y = 6` i
sprawić, że zarówno `x`, jak i `y` będą miały wartość `6`; w Ruście tak nie
jest.

Wyrażenia obliczają się do wartości i stanowią większość pozostałego kodu, jaki
napiszesz w Ruście. Weźmy działanie matematyczne, takie jak `5 + 6`, które jest
wyrażeniem obliczającym się do wartości `11`. Wyrażenia mogą być częścią
instrukcji: w listingu 3-1 `6` w instrukcji `let y = 6;` jest wyrażeniem
obliczającym się do wartości `6`. Wywołanie funkcji jest wyrażeniem. Wywołanie
makra jest wyrażeniem. Nowy blok zasięgu utworzony nawiasami klamrowymi jest
wyrażeniem, na przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-20-blocks-are-expressions/src/main.rs}}
```

To wyrażenie:

```rust,ignore
{
    let x = 3;
    x + 1
}
```

jest blokiem, który w tym przypadku oblicza się do `4`. Ta wartość zostaje
związana z `y` w ramach instrukcji `let`. Zwróć uwagę na wiersz `x + 1` bez
średnika na końcu, w odróżnieniu od większości wierszy, które dotąd się
pojawiły. Wyrażenia nie kończą się średnikiem. Jeśli dodasz średnik na końcu
wyrażenia, zamienisz je w instrukcję, która wtedy nie zwróci wartości. Pamiętaj
o tym, gdy za chwilę będziesz poznawać wyrażenia i wartości zwracane przez
funkcje.

### Funkcje zwracające wartości {#functions-with-return-values}

Funkcje mogą zwracać wartości do kodu, który je wywołuje. Nie nadajemy nazw
zwracanym wartościom, ale musimy zadeklarować ich typ po strzałce (`->`). W
Ruście wartość zwracana przez funkcję jest tożsama z wartością ostatniego
wyrażenia w bloku ciała funkcji. Możesz wyjść z funkcji wcześniej, używając
słowa kluczowego `return` i podając wartość, ale większość funkcji niejawnie
zwraca ostatnie wyrażenie. Oto przykład funkcji, która zwraca wartość:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/src/main.rs}}
```

W funkcji `five` nie ma wywołań funkcji, makr ani nawet instrukcji `let` –
jest tylko sama liczba `5`. To całkowicie poprawna funkcja w Ruście. Zwróć
uwagę, że określono też typ zwracany funkcji: `-> i32`. Uruchom ten kod;
wyjście powinno wyglądać tak:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-21-function-return-values/output.txt}}
```

`5` w funkcji `five` jest wartością zwracaną przez funkcję, dlatego typ zwracany
to `i32`. Przyjrzyjmy się temu dokładniej. Ważne są dwie rzeczy. Po pierwsze,
wiersz `let x = five();` pokazuje, że wartości zwracanej przez funkcję używamy
do zainicjowania zmiennej. Ponieważ funkcja `five` zwraca `5`, ten wiersz jest
równoważny poniższemu:

```rust
let x = 5;
```

Po drugie, funkcja `five` nie ma parametrów i definiuje typ wartości zwracanej.
Ciało funkcji to samotne `5` bez średnika, ponieważ jest to wyrażenie, którego
wartość chcemy zwrócić.

Spójrzmy na inny przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-22-function-parameter-and-return/src/main.rs}}
```

Uruchomienie tego kodu wypisze `The value of x is: 6`. Co się jednak stanie,
jeśli na końcu wiersza z `x + 1` postawimy średnik, zmieniając wyrażenie w
instrukcję?

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/src/main.rs}}
```

Kompilacja tego kodu zakończy się następującym błędem:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-23-statements-dont-return-values/output.txt}}
```

Główny komunikat o błędzie, `mismatched types`, ujawnia sedno problemu z tym
kodem. Definicja funkcji `plus_one` mówi, że zwróci ona `i32`, ale instrukcje
nie obliczają się do wartości, co wyraża `()`, typ jednostkowy (*unit type*).
Zatem nic nie zostaje zwrócone, co jest sprzeczne z definicją funkcji i
powoduje błąd. W tym wyjściu Rust podaje komunikat, który może pomóc naprawić
problem: sugeruje usunięcie średnika, co usunęłoby błąd.

{{#quiz ../quizzes/ch03-03-functions-sec2-expressions.toml}}

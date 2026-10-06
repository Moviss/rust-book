## Błędy odwracalne i `Result` {#recoverable-errors-with-result}

Większość błędów nie jest na tyle poważna, żeby trzeba było całkowicie
zatrzymywać program. Czasem funkcja kończy się niepowodzeniem z powodu, który
łatwo zinterpretować i na który łatwo zareagować. Jeśli na przykład próbujesz
otworzyć plik i operacja się nie udaje, bo plik nie istnieje, możesz zamiast
kończyć proces utworzyć ten plik.

Jak pamiętasz z podrozdziału [„Obsługa potencjalnych błędów za pomocą `Result`”][handle_failure]<!--
ignore --> w rozdziale 2, *enum* (typ wyliczeniowy) `Result` jest zdefiniowany
jako mający dwa warianty, `Ok` i `Err`:

```rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

`T` i `E` to generyczne parametry typu: typy generyczne (*generics*)
omówimy dokładniej w rozdziale 10. Na razie wystarczy wiedzieć, że `T`
reprezentuje typ wartości zwracanej w przypadku powodzenia wewnątrz wariantu
`Ok`, a `E` – typ błędu zwracanego w przypadku niepowodzenia wewnątrz wariantu
`Err`. Ponieważ `Result` ma te generyczne parametry typu, możemy używać typu
`Result` i zdefiniowanych na nim funkcji w wielu różnych sytuacjach, w których
wartość powodzenia i wartość błędu, które chcemy zwrócić, mogą się różnić.

Wywołajmy funkcję, która zwraca wartość `Result`, bo może zakończyć się
niepowodzeniem. W listingu 9-3 próbujemy otworzyć plik.

<Listing number="9-3" file-name="src/main.rs" caption="Otwieranie pliku">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-03/src/main.rs}}
```

</Listing>

Typem zwracanym przez `File::open` jest `Result<T, E>`. Implementacja
`File::open` podstawiła za parametr generyczny `T` typ wartości powodzenia,
czyli `std::fs::File`, który jest uchwytem pliku. Typem `E` użytym w wartości
błędu jest `std::io::Error`. Taki typ zwracany oznacza, że wywołanie
`File::open` może się powieść i zwrócić uchwyt pliku, z którego możemy czytać
lub do którego możemy pisać. Wywołanie funkcji może też się nie udać: plik może
na przykład nie istnieć albo możemy nie mieć uprawnień dostępu do niego.
Funkcja `File::open` musi mieć sposób, żeby powiedzieć nam, czy się powiodła,
czy nie, i jednocześnie przekazać nam albo uchwyt pliku, albo informacje o
błędzie. Właśnie te informacje przekazuje enum `Result`.

Jeśli `File::open` się powiedzie, wartością zmiennej `greeting_file_result`
będzie instancja `Ok` zawierająca uchwyt pliku. Jeśli się nie powiedzie,
wartością `greeting_file_result` będzie instancja `Err` zawierająca więcej
informacji o rodzaju błędu, który wystąpił.

Musimy uzupełnić kod z listingu 9-3 tak, żeby podejmował różne działania w
zależności od wartości zwróconej przez `File::open`. Listing 9-4 pokazuje jeden
ze sposobów obsłużenia `Result` za pomocą podstawowego narzędzia: wyrażenia
`match`, które omówiliśmy w rozdziale 6.

<Listing number="9-4" file-name="src/main.rs" caption="Użycie wyrażenia `match` do obsłużenia wariantów `Result`, które mogą zostać zwrócone">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-04/src/main.rs}}
```

</Listing>

Zwróć uwagę, że podobnie jak enum `Option`, enum `Result` i jego warianty
zostały wprowadzone do zasięgu (*scope*) przez *prelude* (zestaw elementów
importowanych automatycznie), więc w ramionach (*arms*) `match` nie musimy
pisać `Result::` przed wariantami `Ok` i `Err`.

Gdy wynikiem jest `Ok`, ten kod zwróci wewnętrzną wartość `file` z wariantu
`Ok`, a następnie przypiszemy ten uchwyt pliku do zmiennej `greeting_file`. Po
`match` możemy używać uchwytu pliku do czytania lub pisania.

Drugie ramię `match` obsługuje przypadek, w którym z `File::open` dostajemy
wartość `Err`. W tym przykładzie postanowiliśmy wywołać makro `panic!`. Jeśli w
bieżącym katalogu nie ma pliku o nazwie _hello.txt_, a uruchomimy ten kod,
zobaczymy następujący komunikat z makra `panic!`:

```console
{{#include ../listings/ch09-error-handling/listing-09-04/output.txt}}
```

Jak zwykle komunikat mówi nam dokładnie, co poszło nie tak.

### Dopasowywanie różnych błędów {#matching-on-different-errors}

Kod z listingu 9-4 wywoła `panic!` bez względu na to, dlaczego `File::open` się
nie powiodło. Chcemy jednak podejmować różne działania w zależności od przyczyny
niepowodzenia. Jeśli `File::open` nie powiodło się, bo plik nie istnieje,
chcemy utworzyć plik i zwrócić uchwyt do nowego pliku. Jeśli `File::open` nie
powiodło się z jakiegokolwiek innego powodu – na przykład dlatego, że nie
mieliśmy uprawnień do otwarcia pliku – nadal chcemy, żeby kod wywołał `panic!`
tak samo jak w listingu 9-4. W tym celu dodajemy wewnętrzne wyrażenie `match`,
pokazane w listingu 9-5.

<Listing number="9-5" file-name="src/main.rs" caption="Obsługa różnych rodzajów błędów na różne sposoby">

<!-- ignore this test because otherwise it creates hello.txt which causes other
tests to fail lol -->

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-05/src/main.rs}}
```

</Listing>

Typem wartości, którą `File::open` zwraca wewnątrz wariantu `Err`, jest
`io::Error` – struktura (*struct*) dostarczana przez bibliotekę standardową. Ta
struktura ma metodę `kind`, którą możemy wywołać, żeby otrzymać wartość
`io::ErrorKind`. Enum `io::ErrorKind` jest dostarczany przez bibliotekę
standardową i ma warianty reprezentujące różne rodzaje błędów, które mogą
wyniknąć z operacji `io`. Interesuje nas wariant `ErrorKind::NotFound`, który
oznacza, że plik, który próbujemy otworzyć, jeszcze nie istnieje. Dopasowujemy
więc `greeting_file_result`, ale mamy też wewnętrzne dopasowanie
`error.kind()`.

W wewnętrznym dopasowaniu chcemy sprawdzić, czy wartość zwrócona przez
`error.kind()` jest wariantem `NotFound` enuma `ErrorKind`. Jeśli tak, próbujemy
utworzyć plik za pomocą `File::create`. Ponieważ jednak `File::create` również
może się nie powieść, potrzebujemy drugiego ramienia w wewnętrznym wyrażeniu
`match`. Gdy pliku nie da się utworzyć, wypisywany jest inny komunikat o
błędzie. Drugie ramię zewnętrznego `match` pozostaje bez zmian, więc program
panikuje przy każdym błędzie poza brakiem pliku.

> #### Alternatywy dla `match` w połączeniu z `Result<T, E>` {#alternatives-to-using-match-with-resultt-e}
>
> To sporo `match`! Wyrażenie `match` jest bardzo przydatne, ale też bardzo
> podstawowe. W rozdziale 13 poznasz domknięcia (*closures*), których używa się
> z wieloma metodami zdefiniowanymi na `Result<T, E>`. Przy obsłudze wartości
> `Result<T, E>` w kodzie te metody bywają zwięźlejsze niż `match`.
>
> Oto na przykład inny sposób zapisania tej samej logiki co w listingu 9-5, tym
> razem z użyciem domknięć i metody `unwrap_or_else`:
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore
> use std::fs::File;
> use std::io::ErrorKind;
>
> fn main() {
>     let greeting_file = File::open("hello.txt").unwrap_or_else(|error| {
>         if error.kind() == ErrorKind::NotFound {
>             File::create("hello.txt").unwrap_or_else(|error| {
>                 panic!("Problem creating the file: {error:?}");
>             })
>         } else {
>             panic!("Problem opening the file: {error:?}");
>         }
>     });
> }
> ```
>
> Choć ten kod zachowuje się tak samo jak listing 9-5, nie zawiera żadnych
> wyrażeń `match` i czyta się go łatwiej. Wróć do tego przykładu po przeczytaniu
> rozdziału 13 i poszukaj metody `unwrap_or_else` w dokumentacji biblioteki
> standardowej. Wiele innych takich metod pozwala uporządkować ogromne,
> zagnieżdżone wyrażenia `match` przy obsłudze błędów.

{{#quiz ../quizzes/ch09-02-recoverable-errors-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="shortcuts-for-panic-on-error-unwrap-and-expect"></a>

#### Skróty do paniki w razie błędu {#shortcuts-for-panic-on-error}

Użycie `match` sprawdza się wystarczająco dobrze, ale bywa dość rozwlekłe i nie
zawsze dobrze oddaje intencję. Typ `Result<T, E>` ma zdefiniowanych wiele metod
pomocniczych do różnych, bardziej konkretnych zadań. Metoda `unwrap` to
skrót zaimplementowany dokładnie tak jak wyrażenie `match`, które napisaliśmy w
listingu 9-4. Jeśli wartość `Result` jest wariantem `Ok`, `unwrap` zwróci
wartość z wnętrza `Ok`. Jeśli `Result` jest wariantem `Err`, `unwrap` wywoła za
nas makro `panic!`. Oto przykład działania `unwrap`:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-04-unwrap/src/main.rs}}
```

</Listing>

Jeśli uruchomimy ten kod bez pliku _hello.txt_, zobaczymy komunikat o błędzie z
wywołania `panic!`, które wykonuje metoda `unwrap`:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-04-unwrap
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:4:49:
called `Result::unwrap()` on an `Err` value: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

Podobnie metoda `expect` pozwala nam dodatkowo wybrać komunikat o błędzie dla
`panic!`. Użycie `expect` zamiast `unwrap` i podanie dobrych komunikatów o
błędach pozwala wyrazić intencję i ułatwia wyśledzenie źródła paniki
(*panic*). Składnia `expect` wygląda tak:

<Listing file-name="src/main.rs">

```rust,should_panic
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-05-expect/src/main.rs}}
```

</Listing>

`expect` używamy tak samo jak `unwrap`: żeby zwrócić uchwyt pliku albo wywołać
makro `panic!`. Komunikatem o błędzie, którego `expect` użyje w wywołaniu
`panic!`, będzie parametr przekazany do `expect`, a nie domyślny komunikat
`panic!`, którego używa `unwrap`. Wygląda to tak:

<!-- manual-regeneration
cd listings/ch09-error-handling/no-listing-05-expect
cargo run
copy and paste relevant text
-->

```text
thread 'main' panicked at src/main.rs:5:10:
hello.txt should be included in this project: Os { code: 2, kind: NotFound, message: "No such file or directory" }
```

W kodzie produkcyjnym większość rustowców (*Rustaceans*) wybiera `expect`
zamiast `unwrap` i podaje więcej kontekstu, wyjaśniając, dlaczego operacja ma
się zawsze powieść. Dzięki temu, jeśli twoje założenia kiedykolwiek okażą się
błędne, będziesz mieć więcej informacji przy debugowaniu.

### Propagowanie błędów {#propagating-errors}

Gdy implementacja funkcji wywołuje coś, co może się nie powieść, zamiast
obsługiwać błąd wewnątrz samej funkcji, możesz zwrócić go do kodu wywołującego,
żeby to on zdecydował, co zrobić. Nazywa się to _propagowaniem_ (*propagating*)
błędu i daje więcej kontroli kodowi wywołującemu, który może mieć więcej
informacji albo logiki określającej sposób obsługi błędu niż to, czym
dysponujesz w kontekście swojego kodu.

Listing 9-6 pokazuje na przykład funkcję, która odczytuje nazwę użytkownika z
pliku. Jeśli plik nie istnieje albo nie da się go odczytać, funkcja zwróci te
błędy do kodu, który ją wywołał.

<Listing number="9-6" file-name="src/main.rs" caption="Funkcja, która zwraca błędy do kodu wywołującego za pomocą `match`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-06/src/main.rs:here}}
```

</Listing>

Tę funkcję można napisać dużo krócej, ale zaczniemy od zrobienia wielu rzeczy
ręcznie, żeby przyjrzeć się obsłudze błędów; na końcu pokażemy krótszy sposób.
Spójrzmy najpierw na typ zwracany funkcji: `Result<String, io::Error>`.
Oznacza to, że funkcja zwraca wartość typu `Result<T, E>`, w którym za parametr
generyczny `T` podstawiono konkretny typ `String`, a za typ generyczny `E` –
konkretny typ `io::Error`.

Jeśli funkcja zakończy się powodzeniem bez żadnych problemów, kod, który ją
wywołuje, otrzyma wartość `Ok` przechowującą `String` – nazwę użytkownika
(`username`), którą funkcja odczytała z pliku. Jeśli funkcja napotka jakiś
problem, kod wywołujący otrzyma wartość `Err` przechowującą instancję
`io::Error`, która zawiera więcej informacji o tym, na czym polegał problem.
Wybraliśmy `io::Error` jako typ zwracany tej funkcji, bo tak się składa, że jest
to typ wartości błędu zwracanej przez obie wywoływane w ciele funkcji operacje,
które mogą się nie powieść: funkcję `File::open` i metodę `read_to_string`.

Ciało funkcji zaczyna się od wywołania funkcji `File::open`. Następnie
obsługujemy wartość `Result` za pomocą `match` podobnego do `match` z listingu
9-4. Jeśli `File::open` się powiedzie, uchwyt pliku w zmiennej wzorca `file`
staje się wartością mutowalnej zmiennej `username_file` i funkcja działa dalej.
W przypadku `Err`, zamiast wywoływać `panic!`, używamy słowa kluczowego
(*keyword*) `return`, żeby wcześnie wyjść z całej funkcji i przekazać wartość
błędu z `File::open`, teraz w zmiennej wzorca `e`, z powrotem do kodu
wywołującego jako wartość błędu tej funkcji.

Jeśli więc mamy uchwyt pliku w `username_file`, funkcja tworzy następnie nowy
`String` w zmiennej `username` i wywołuje metodę `read_to_string` na uchwycie
pliku w `username_file`, żeby wczytać zawartość pliku do `username`. Metoda
`read_to_string` również zwraca `Result`, bo może się nie powieść, nawet jeśli
`File::open` się powiodło. Potrzebujemy więc kolejnego `match`, żeby obsłużyć
ten `Result`: jeśli `read_to_string` się powiedzie, to nasza funkcja się
powiodła i zwracamy nazwę użytkownika z pliku, która jest teraz w `username`,
opakowaną w `Ok`. Jeśli `read_to_string` się nie powiedzie, zwracamy wartość
błędu tak samo, jak zwróciliśmy wartość błędu w `match` obsługującym wartość
zwracaną przez `File::open`. Nie musimy jednak jawnie pisać `return`, bo jest to
ostatnie wyrażenie w funkcji.

Kod, który wywołuje ten kod, zajmie się następnie obsługą otrzymanej wartości:
albo `Ok` zawierającej nazwę użytkownika, albo `Err` zawierającej `io::Error`.
To kod wywołujący decyduje, co zrobić z tymi wartościami. Jeśli kod wywołujący
dostanie wartość `Err`, może na przykład wywołać `panic!` i zakończyć program
awarią, użyć domyślnej nazwy użytkownika albo poszukać nazwy użytkownika gdzieś
indziej niż w pliku. Nie mamy wystarczających informacji o tym, co właściwie
próbuje zrobić kod wywołujący, więc propagujemy wszystkie informacje o
powodzeniu lub błędzie w górę, żeby mógł je odpowiednio obsłużyć.

Ten wzorzec propagowania błędów jest w Ruście tak powszechny, że Rust udostępnia
operator znaku zapytania `?`, który to ułatwia.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-shortcut-for-propagating-errors-the--operator"></a>

#### Skrót w postaci operatora `?` {#the--operator-shortcut}

Listing 9-7 pokazuje implementację `read_username_from_file`, która działa tak
samo jak w listingu 9-6, ale korzysta z operatora `?`.

<Listing number="9-7" file-name="src/main.rs" caption="Funkcja, która zwraca błędy do kodu wywołującego za pomocą operatora `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-07/src/main.rs:here}}
```

</Listing>

Operator `?` umieszczony po wartości `Result` działa niemal tak samo jak
wyrażenia `match`, które zdefiniowaliśmy do obsługi wartości `Result` w
listingu 9-6. Jeśli wartością `Result` jest `Ok`, wartość z wnętrza `Ok`
zostanie zwrócona z tego wyrażenia i program będzie działał dalej. Jeśli
wartością jest `Err`, `Err` zostanie zwrócone z całej funkcji, tak jakbyśmy
użyli słowa kluczowego `return`, dzięki czemu wartość błędu zostanie
propagowana do kodu wywołującego.

Działanie wyrażenia `match` z listingu 9-6 różni się jednak od działania
operatora `?`: wartości błędów, na których wywołano operator `?`, przechodzą
przez funkcję `from` zdefiniowaną w `From`. Jest to *trait* (cecha typu,
zbliżona do interfejsu) z biblioteki standardowej, który służy do konwertowania
wartości jednego typu na inny. Gdy operator `?` wywołuje funkcję `from`,
otrzymany typ błędu jest konwertowany na typ błędu zdefiniowany w typie
zwracanym bieżącej funkcji. Przydaje się to, gdy funkcja zwraca jeden typ błędu
reprezentujący wszystkie sposoby, na jakie może się nie powieść, nawet jeśli
poszczególne jej części mogą zawodzić z wielu różnych powodów.

Moglibyśmy na przykład zmienić funkcję `read_username_from_file` z listingu
9-7 tak, żeby zwracała zdefiniowany przez nas własny typ błędu o nazwie
`OurError`. Jeśli zdefiniujemy też `impl From<io::Error> for OurError`, żeby
tworzyć instancję `OurError` z `io::Error`, to wywołania operatora `?` w ciele
`read_username_from_file` wywołają `from` i przekonwertują typy błędów bez
potrzeby dodawania do funkcji żadnego kodu.

W kontekście listingu 9-7 operator `?` na końcu wywołania `File::open` zwróci
wartość z wnętrza `Ok` do zmiennej `username_file`. Jeśli wystąpi błąd,
operator `?` wcześnie wyjdzie z całej funkcji i przekaże wartość `Err` do kodu
wywołującego. To samo dotyczy `?` na końcu wywołania `read_to_string`.

Operator `?` eliminuje mnóstwo szablonowego kodu (*boilerplate*) i upraszcza
implementację tej funkcji. Moglibyśmy nawet jeszcze bardziej skrócić ten kod,
łącząc wywołania metod w łańcuch bezpośrednio po `?`, jak pokazano w listingu
9-8.

<Listing number="9-8" file-name="src/main.rs" caption="Łączenie wywołań metod w łańcuch po operatorze `?`">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-08/src/main.rs:here}}
```

</Listing>

Przenieśliśmy tworzenie nowego `String` w `username` na początek funkcji; ta
część się nie zmieniła. Zamiast tworzyć zmienną `username_file`, dołączyliśmy
wywołanie `read_to_string` bezpośrednio do wyniku
`File::open("hello.txt")?`. Nadal mamy `?` na końcu wywołania `read_to_string`
i nadal zwracamy wartość `Ok` zawierającą `username`, gdy zarówno `File::open`,
jak i `read_to_string` się powiodą, zamiast zwracać błędy. Funkcjonalność znów
jest taka sama jak w listingach 9-6 i 9-7; to po prostu inny, wygodniejszy
sposób zapisu.

Listing 9-9 pokazuje, jak skrócić to jeszcze bardziej za pomocą
`fs::read_to_string`.

<Listing number="9-9" file-name="src/main.rs" caption="Użycie `fs::read_to_string` zamiast otwierania, a potem odczytywania pliku">

<!-- Deliberately not using rustdoc_include here; the `main` function in the
file panics. We do want to include it for reader experimentation purposes, but
don't want to include it for rustdoc testing purposes. -->

```rust
{{#include ../listings/ch09-error-handling/listing-09-09/src/main.rs:here}}
```

</Listing>

Wczytywanie pliku do łańcucha znaków (*string*) to dość częsta operacja, więc
biblioteka standardowa udostępnia wygodną funkcję `fs::read_to_string`, która
otwiera plik, tworzy nowy `String`, odczytuje zawartość pliku, umieszcza ją w
tym `String` i go zwraca. Oczywiście użycie `fs::read_to_string` nie dałoby nam
okazji do wyjaśnienia całej obsługi błędów, dlatego najpierw zrobiliśmy to
dłuższą drogą.

<!-- Old headings. Do not remove or links may break. -->

<a id="where-the--operator-can-be-used"></a>

#### Gdzie używać operatora `?` {#where-to-use-the--operator}

Operatora `?` można używać tylko w funkcjach, których typ zwracany jest zgodny z
wartością, na której użyto `?`. Wynika to z tego, że operator `?` jest
zdefiniowany tak, by wcześnie zwracać wartość z funkcji, w taki sam sposób jak
wyrażenie `match` zdefiniowane w listingu 9-6. W listingu 9-6 `match` używał
wartości `Result`, a ramię wczesnego powrotu zwracało wartość `Err(e)`. Typem
zwracanym funkcji musi być `Result`, żeby był zgodny z tym `return`.

W listingu 9-10 zobaczmy, jaki błąd otrzymamy, jeśli użyjemy operatora `?` w
funkcji `main` o typie zwracanym niezgodnym z typem wartości, na której używamy
`?`.

<Listing number="9-10" file-name="src/main.rs" caption="Próba użycia `?` w funkcji `main`, która zwraca `()`, nie skompiluje się.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-10/src/main.rs}}
```

</Listing>

Ten kod otwiera plik, co może się nie powieść. Operator `?` występuje po
wartości `Result` zwróconej przez `File::open`, ale ta funkcja `main` ma typ
zwracany `()`, a nie `Result`. Gdy skompilujemy ten kod, otrzymamy następujący
komunikat o błędzie:

```console
{{#include ../listings/ch09-error-handling/listing-09-10/output.txt}}
```

Ten błąd wskazuje, że operatora `?` wolno nam używać tylko w funkcji, która
zwraca `Result`, `Option` albo inny typ implementujący `FromResidual`.

Błąd możesz naprawić na dwa sposoby. Pierwszy to zmiana typu zwracanego funkcji
na zgodny z wartością, na której używasz operatora `?`, o ile nic ci w tym nie
przeszkadza. Drugi to użycie `match` albo jednej z metod `Result<T, E>`, żeby
obsłużyć `Result<T, E>` w dowolny odpowiedni sposób.

Komunikat o błędzie wspominał też, że `?` można używać również z wartościami
`Option<T>`. Podobnie jak w przypadku użycia `?` na `Result`, `?` na `Option`
możesz używać tylko w funkcji, która zwraca `Option`. Operator `?` wywołany na
`Option<T>` zachowuje się podobnie jak wywołany na `Result<T, E>`: jeśli
wartością jest `None`, `None` zostanie w tym miejscu wcześnie zwrócone z
funkcji. Jeśli wartością jest `Some`, wartość z wnętrza `Some` jest wynikiem
wyrażenia, a funkcja działa dalej. Listing 9-11 zawiera przykład funkcji, która
znajduje ostatni znak pierwszego wiersza podanego tekstu.

<Listing number="9-11" caption="Użycie operatora `?` na wartości `Option<T>`">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-11/src/main.rs:here}}
```

</Listing>

Ta funkcja zwraca `Option<char>`, bo możliwe, że jest tam jakiś znak, ale
możliwe też, że go nie ma. Kod przyjmuje argument `text` będący wycinkiem
łańcucha (*string slice*) i wywołuje na nim metodę `lines`, która zwraca
iterator po wierszach łańcucha. Ponieważ funkcja chce zbadać pierwszy wiersz,
wywołuje `next` na iteratorze, żeby pobrać z niego pierwszą wartość. Jeśli
`text` jest pustym łańcuchem, to wywołanie `next` zwróci `None` – wtedy
używamy `?`, żeby przerwać i zwrócić `None` z `last_char_of_first_line`. Jeśli
`text` nie jest pustym łańcuchem, `next` zwróci wartość `Some` zawierającą
wycinek łańcucha z pierwszym wierszem `text`.

Operator `?` wydobywa wycinek łańcucha, a my możemy wywołać na nim `chars`, żeby
otrzymać iterator po jego znakach. Interesuje nas ostatni znak tego pierwszego
wiersza, więc wywołujemy `last`, żeby zwrócić ostatni element iteratora. Jest
to `Option`, bo możliwe, że pierwszy wiersz jest pustym łańcuchem, na przykład
gdy `text` zaczyna się od pustego wiersza, ale w innych wierszach ma znaki, jak
w `"\nhi"`. Jeśli jednak w pierwszym wierszu jest ostatni znak, zostanie on
zwrócony w wariancie `Some`. Operator `?` pośrodku daje nam zwięzły sposób
wyrażenia tej logiki i pozwala zaimplementować funkcję w jednym wierszu. Gdyby
nie dało się używać operatora `?` na `Option`, musielibyśmy zaimplementować tę
logikę za pomocą większej liczby wywołań metod albo wyrażenia `match`.

Zwróć uwagę, że operatora `?` możesz używać na `Result` w funkcji, która zwraca
`Result`, i operatora `?` na `Option` w funkcji, która zwraca `Option`, ale nie
możesz ich mieszać. Operator `?` nie przekonwertuje automatycznie `Result` na
`Option` ani odwrotnie; w takich przypadkach możesz dokonać konwersji jawnie za
pomocą metod takich jak `ok` na `Result` czy `ok_or` na `Option`.

Jak dotąd wszystkie funkcje `main`, których używaliśmy, zwracały `()`. Funkcja
`main` jest wyjątkowa, bo stanowi punkt wejścia i punkt wyjścia programu
wykonywalnego, i istnieją ograniczenia co do jej typu zwracanego, żeby program
zachowywał się zgodnie z oczekiwaniami.

Na szczęście `main` może też zwracać `Result<(), E>`. Listing 9-12 zawiera kod z
listingu 9-10, ale zmieniliśmy typ zwracany `main` na
`Result<(), Box<dyn Error>>` i dodaliśmy na końcu wartość zwracaną `Ok(())`.
Teraz ten kod się skompiluje.

<Listing number="9-12" file-name="src/main.rs" caption="Zmiana `main` tak, by zwracała `Result<(), E>`, pozwala używać operatora `?` na wartościach `Result`.">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-12/src/main.rs}}
```

</Listing>

Typ `Box<dyn Error>` to obiekt traitu (*trait object*), o którym opowiemy w
podrozdziale [„Używanie obiektów traitów do abstrahowania wspólnego zachowania”][trait-objects]<!-- ignore -->
w rozdziale 18. Na razie możesz czytać `Box<dyn Error>` jako „dowolny rodzaj
błędu”. Użycie `?` na wartości `Result` w funkcji `main` z typem błędu
`Box<dyn Error>` jest dozwolone, bo pozwala wcześnie zwrócić dowolną wartość
`Err`. Choć ciało tej funkcji `main` zwraca tylko błędy typu `std::io::Error`,
dzięki podaniu `Box<dyn Error>` ta sygnatura pozostanie poprawna nawet wtedy,
gdy do ciała `main` dodamy więcej kodu zwracającego inne błędy.

Gdy funkcja `main` zwraca `Result<(), E>`, plik wykonywalny zakończy działanie z
wartością `0`, jeśli `main` zwróci `Ok(())`, i z wartością niezerową, jeśli
`main` zwróci wartość `Err`. Pliki wykonywalne napisane w C zwracają przy
zakończeniu liczby całkowite: programy, które kończą się pomyślnie, zwracają
liczbę `0`, a programy, w których wystąpił błąd, zwracają liczbę inną niż `0`.
Rust również zwraca liczby całkowite z plików wykonywalnych, żeby zachować
zgodność z tą konwencją.

Funkcja `main` może zwracać dowolne typy implementujące
[trait `std::process::Termination`][termination]<!-- ignore -->, który zawiera
funkcję `report` zwracającą `ExitCode`. Więcej informacji o implementowaniu
traitu `Termination` dla własnych typów znajdziesz w dokumentacji biblioteki
standardowej.

Skoro omówiliśmy już szczegóły wywoływania `panic!` i zwracania `Result`,
wróćmy do tematu, jak zdecydować, którego z nich użyć w danej sytuacji.

{{#quiz ../quizzes/ch09-02-recoverable-errors-sec2.toml}}

[handle_failure]: ch02-00-guessing-game-tutorial.html#handling-potential-failure-with-result
[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior
[termination]: https://doc.rust-lang.org/std/process/trait.Termination.html

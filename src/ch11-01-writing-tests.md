## Jak pisać testy {#how-to-write-tests}

_Testy_ to funkcje Rusta, które sprawdzają, czy kod niebędący testem działa w
oczekiwany sposób. Ciała funkcji testowych zwykle wykonują trzy czynności:

- Przygotowują potrzebne dane lub stan.
- Uruchamiają kod, który chcesz przetestować.
- Sprawdzają za pomocą asercji, czy wyniki są zgodne z oczekiwaniami.

Przyjrzyjmy się mechanizmom, które Rust udostępnia specjalnie do pisania testów
wykonujących te czynności. Należą do nich atrybut `test`, kilka makr oraz
atrybut `should_panic`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-anatomy-of-a-test-function"></a>

### Struktura funkcji testowych {#structuring-test-functions}

W najprostszej postaci test w Ruście to funkcja oznaczona atrybutem `test`.
Atrybuty to metadane opisujące fragmenty kodu w Ruście; przykładem jest atrybut
`derive`, którego używaliśmy ze strukturami (*struct*) w rozdziale 5. Aby
zamienić funkcję w funkcję testową, dodaj `#[test]` w wierszu przed `fn`. Gdy
uruchamiasz testy poleceniem `cargo test`, Rust buduje plik binarny programu
uruchamiającego testy (*test runner*), który uruchamia oznaczone funkcje i
raportuje, czy każda z funkcji testowych przechodzi, czy kończy się
niepowodzeniem.

Za każdym razem, gdy tworzymy za pomocą Cargo nowy projekt biblioteki,
automatycznie generuje się dla nas moduł testów z funkcją testową. Ten moduł
daje ci szablon do pisania testów, dzięki czemu nie musisz sprawdzać dokładnej
struktury i składni za każdym razem, gdy zaczynasz nowy projekt. Możesz dodać
tyle dodatkowych funkcji testowych i modułów testów, ile tylko chcesz!

Zanim przetestujemy jakikolwiek kod, poznamy niektóre aspekty działania testów,
eksperymentując z szablonowym testem. Potem napiszemy kilka testów z
prawdziwego zdarzenia, które wywołują napisany przez nas kod i sprawdzają za
pomocą asercji, że zachowuje się on poprawnie.

Utwórzmy nowy projekt biblioteki o nazwie `adder`, która będzie dodawać dwie
liczby:

```console
$ cargo new adder --lib
     Created library `adder` project
$ cd adder
```

Zawartość pliku _src/lib.rs_ w bibliotece `adder` powinna wyglądać jak w
listingu 11-1.

<Listing number="11-1" file-name="src/lib.rs" caption="Kod wygenerowany automatycznie przez `cargo new`">

<!-- manual-regeneration
cd listings/ch11-writing-automated-tests
rm -rf listing-11-01
cargo new listing-11-01 --lib --name adder
cd listing-11-01
echo "$ cargo test" > output.txt
RUSTFLAGS="-A unused_variables -A dead_code" RUST_TEST_THREADS=1 cargo test >> output.txt 2>&1
git diff output.txt # commit any relevant changes; discard irrelevant ones
cd ../../..
-->

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-01/src/lib.rs}}
```

</Listing>

Plik zaczyna się od przykładowej funkcji `add`, abyśmy mieli co testować.

Na razie skupmy się wyłącznie na funkcji `it_works`. Zwróć uwagę na adnotację
`#[test]`: ten atrybut wskazuje, że jest to funkcja testowa, więc program
uruchamiający testy wie, że ma ją traktować jako test. W module `tests` możemy
mieć też funkcje niebędące testami, które pomagają przygotować typowe scenariusze
lub wykonać typowe operacje, dlatego zawsze musimy wskazać, które funkcje są
testami.

Ciało przykładowej funkcji używa makra `assert_eq!`, aby sprawdzić za pomocą
asercji, że zmienna `result`, zawierająca wynik wywołania `add` z argumentami 2
i 2, jest równa 4. Ta asercja jest przykładem formatu typowego testu. Uruchommy
test, aby zobaczyć, że przechodzi.

Polecenie `cargo test` uruchamia wszystkie testy w naszym projekcie, jak widać w
listingu 11-2.

<Listing number="11-2" caption="Wynik uruchomienia automatycznie wygenerowanego testu">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-01/output.txt}}
```

</Listing>

Cargo skompilowało i uruchomiło test. Widzimy linię `running 1 test`. Kolejna
linia pokazuje nazwę wygenerowanej funkcji testowej, `tests::it_works`, oraz to,
że wynikiem uruchomienia tego testu jest `ok`. Ogólne podsumowanie
`test result: ok.` oznacza, że wszystkie testy przeszły, a fragment
`1 passed; 0 failed` podaje łączną liczbę testów, które przeszły lub zakończyły
się niepowodzeniem.

Test można oznaczyć jako ignorowany, aby w określonej sytuacji się nie
uruchamiał; omówimy to w podrozdziale [„Ignorowanie testów, chyba że wyraźnie
o nie poproszono”][ignoring]<!-- ignore --> w dalszej części tego rozdziału.
Ponieważ tutaj tego nie zrobiliśmy, podsumowanie pokazuje `0 ignored`. Możemy
też przekazać do polecenia `cargo test` argument, aby uruchomić tylko testy,
których nazwa pasuje do podanego łańcucha znaków (*string*); nazywa się to
_filtrowaniem_ (*filtering*), a omówimy je w podrozdziale [„Uruchamianie
podzbioru testów według nazwy”][subset]<!-- ignore -->. Tutaj nie filtrowaliśmy
uruchamianych testów, więc koniec podsumowania pokazuje `0 filtered out`.

Statystyka `0 measured` dotyczy testów wydajności (*benchmark*), które mierzą
wydajność kodu. W chwili pisania tej książki testy wydajności są dostępne tylko
w Ruście nightly. Więcej informacji znajdziesz w [dokumentacji testów
wydajności][bench].

Następna część wyniku testów, zaczynająca się od `Doc-tests adder`, zawiera
wyniki testów dokumentacyjnych. Nie mamy jeszcze żadnych testów
dokumentacyjnych, ale Rust potrafi kompilować wszystkie przykłady kodu, które
pojawiają się w dokumentacji naszego API. Ten mechanizm pomaga utrzymywać
dokumentację i kod w zgodzie! Sposób pisania testów dokumentacyjnych omówimy w
podrozdziale [„Komentarze dokumentacyjne jako
testy”][doc-comments]<!-- ignore --> w rozdziale 14. Na razie zignorujemy wynik
`Doc-tests`.

Zacznijmy dostosowywać test do naszych potrzeb. Najpierw zmień nazwę funkcji
`it_works` na inną, na przykład `exploration`, w ten sposób:

<span class="filename">Plik: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/src/lib.rs}}
```

Następnie ponownie uruchom `cargo test`. Wynik pokazuje teraz `exploration`
zamiast `it_works`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-01-changing-test-name/output.txt}}
```

Teraz dodamy kolejny test, ale tym razem taki, który zakończy się
niepowodzeniem! Testy kończą się niepowodzeniem, gdy coś w funkcji testowej
wywoła panikę (*panic*). Każdy test jest uruchamiany w nowym wątku, a gdy wątek
główny zauważy, że wątek testu zakończył działanie, test zostaje oznaczony jako
nieudany. W rozdziale 9 mówiliśmy o tym, że najprostszym sposobem wywołania
paniki jest wywołanie makra `panic!`. Dodaj nowy test jako funkcję o nazwie
`another`, tak aby plik _src/lib.rs_ wyglądał jak w listingu 11-3.

<Listing number="11-3" file-name="src/lib.rs" caption="Dodanie drugiego testu, który zakończy się niepowodzeniem, ponieważ wywołujemy makro `panic!`">

```rust,panics,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-03/src/lib.rs}}
```

</Listing>

Ponownie uruchom testy za pomocą `cargo test`. Wynik powinien wyglądać jak w
listingu 11-4, który pokazuje, że test `exploration` przeszedł, a `another`
zakończył się niepowodzeniem.

<Listing number="11-4" caption="Wyniki testów, gdy jeden test przechodzi, a drugi kończy się niepowodzeniem">

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-03/output.txt}}
```

</Listing>

<!-- manual-regeneration
rg panicked listings/ch11-writing-automated-tests/listing-11-03/output.txt
check the line number of the panic matches the line number in the following paragraph
 -->

Zamiast `ok` linia `test tests::another` pokazuje `FAILED`. Między
poszczególnymi wynikami a podsumowaniem pojawiają się dwie nowe sekcje. Pierwsza
wyświetla szczegółową przyczynę niepowodzenia każdego testu. W tym przypadku
dowiadujemy się, że `tests::another` zakończył się niepowodzeniem, ponieważ
spanikował z komunikatem `Make this test fail` w wierszu 17 pliku
_src/lib.rs_. Następna sekcja zawiera same nazwy wszystkich nieudanych testów,
co przydaje się, gdy testów jest dużo, a szczegółowych komunikatów o
niepowodzeniach też jest mnóstwo. Nazwy
nieudanego testu możemy użyć, aby uruchomić tylko ten test i łatwiej go
debugować; więcej o sposobach uruchamiania testów powiemy w podrozdziale
[„Sterowanie sposobem uruchamiania
testów”][controlling-how-tests-are-run]<!-- ignore -->.

Na końcu wyświetla się linia podsumowania: ogólny wynik naszych testów to
`FAILED`. Jeden test przeszedł, a jeden zakończył się niepowodzeniem.

Skoro już wiesz, jak wyglądają wyniki testów w różnych sytuacjach, przyjrzyjmy
się kilku makrom innym niż `panic!`, które przydają się w testach.

<!-- Old headings. Do not remove or links may break. -->

<a id="checking-results-with-the-assert-macro"></a>

### Sprawdzanie wyników za pomocą `assert!` {#checking-results-with-assert}

Makro `assert!`, udostępniane przez bibliotekę standardową, przydaje się, gdy
chcesz się upewnić, że jakiś warunek w teście daje wartość `true`. Przekazujemy
makru `assert!` argument, który daje wartość logiczną. Jeśli ta wartość to
`true`, nic się nie dzieje i test przechodzi. Jeśli to `false`, makro `assert!`
wywołuje `panic!`, przez co test kończy się niepowodzeniem. Makro `assert!`
pomaga nam sprawdzić, czy nasz kod działa tak, jak zamierzamy.

W rozdziale 5, w listingu 5-15, użyliśmy struktury `Rectangle` i metody
`can_hold`, które powtarzamy tutaj w listingu 11-5. Umieśćmy ten kod w pliku
_src/lib.rs_, a następnie napiszmy dla niego kilka testów z użyciem makra
`assert!`.

<Listing number="11-5" file-name="src/lib.rs" caption="Struktura `Rectangle` i jej metoda `can_hold` z rozdziału 5">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-05/src/lib.rs}}
```

</Listing>

Metoda `can_hold` zwraca wartość logiczną, co oznacza, że idealnie nadaje się
do użycia z makrem `assert!`. W listingu 11-6 piszemy test, który sprawdza
metodę `can_hold`: tworzy instancję `Rectangle` o szerokości 8 i wysokości 7 i
sprawdza za pomocą asercji, że może ona pomieścić inną instancję `Rectangle` o
szerokości 5 i wysokości 1.

<Listing number="11-6" file-name="src/lib.rs" caption="Test metody `can_hold`, który sprawdza, czy większy prostokąt rzeczywiście może pomieścić mniejszy">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-06/src/lib.rs:here}}
```

</Listing>

Zwróć uwagę na wiersz `use super::*;` wewnątrz modułu `tests`. Moduł `tests`
jest zwykłym modułem, który podlega standardowym regułom widoczności omówionym
w rozdziale 7 w podrozdziale [„Ścieżki do elementów w drzewie
modułów”][paths-for-referring-to-an-item-in-the-module-tree]<!-- ignore -->.
Ponieważ moduł `tests` jest modułem wewnętrznym, musimy wprowadzić testowany
kod z modułu zewnętrznego do zasięgu (*scope*) modułu wewnętrznego. Używamy tu
operatora glob (*glob operator*), więc wszystko, co zdefiniujemy w module
zewnętrznym, jest dostępne w module `tests`.

Nazwaliśmy nasz test `larger_can_hold_smaller` i utworzyliśmy dwie potrzebne
instancje `Rectangle`. Następnie wywołaliśmy makro `assert!` i przekazaliśmy mu
wynik wywołania `larger.can_hold(&smaller)`. To wyrażenie powinno zwrócić
`true`, więc nasz test powinien przejść. Sprawdźmy!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-06/output.txt}}
```

Przechodzi! Dodajmy kolejny test, tym razem sprawdzający za pomocą asercji, że
mniejszy prostokąt nie może pomieścić większego:

<span class="filename">Plik: src/lib.rs</span>

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/src/lib.rs:here}}
```

Ponieważ poprawnym wynikiem funkcji `can_hold` jest w tym przypadku `false`,
musimy zanegować ten wynik, zanim przekażemy go do makra `assert!`. Dzięki
temu nasz test przejdzie, jeśli `can_hold` zwróci `false`:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-02-adding-another-rectangle-test/output.txt}}
```

Dwa testy przechodzą! Zobaczmy teraz, co się stanie z wynikami testów, gdy
wprowadzimy do kodu błąd. Zmienimy implementację metody `can_hold`, zastępując
znak większości (`>`) znakiem mniejszości (`<`) przy porównywaniu szerokości:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/src/lib.rs:here}}
```

Uruchomienie testów daje teraz następujący wynik:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-03-introducing-a-bug/output.txt}}
```

Nasze testy wychwyciły błąd! Ponieważ `larger.width` wynosi `8`, a
`smaller.width` wynosi `5`, porównanie szerokości w `can_hold` zwraca teraz
`false`: 8 nie jest mniejsze niż 5.

<!-- Old headings. Do not remove or links may break. -->

<a id="testing-equality-with-the-assert_eq-and-assert_ne-macros"></a>

### Testowanie równości za pomocą `assert_eq!` i `assert_ne!` {#testing-equality-with-assert_eq-and-assert_ne}

Typowym sposobem weryfikowania działania kodu jest sprawdzanie, czy wynik
testowanego kodu jest równy wartości, której się po nim spodziewasz. Można to
zrobić, używając makra `assert!` i przekazując mu wyrażenie z operatorem `==`.
Jest to jednak tak powszechny test, że biblioteka standardowa udostępnia parę
makr – `assert_eq!` i `assert_ne!` – które pozwalają wykonać go wygodniej. Te
makra porównują dwa argumenty, sprawdzając odpowiednio ich równość lub
nierówność. Jeśli asercja się nie powiedzie, wypisują też obie wartości, co
ułatwia zobaczenie, _dlaczego_ test zakończył się niepowodzeniem. Makro
`assert!` natomiast informuje jedynie, że wyrażenie `==` dało wartość `false`,
nie wypisując wartości, które doprowadziły do `false`.

W listingu 11-7 piszemy funkcję o nazwie `add_two`, która dodaje `2` do swojego
parametru, a następnie testujemy ją za pomocą makra `assert_eq!`.

<Listing number="11-7" file-name="src/lib.rs" caption="Testowanie funkcji `add_two` za pomocą makra `assert_eq!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-07/src/lib.rs}}
```

</Listing>

Sprawdźmy, czy przechodzi!

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-07/output.txt}}
```

Tworzymy zmienną o nazwie `result`, która przechowuje wynik wywołania
`add_two(2)`. Następnie przekazujemy `result` i `4` jako argumenty makra
`assert_eq!`. Linia wyniku dla tego testu to
`test tests::it_adds_two ... ok`, a tekst `ok` oznacza, że nasz test przeszedł!

Wprowadźmy do kodu błąd, aby zobaczyć, jak wygląda `assert_eq!`, gdy asercja się
nie powiedzie. Zmień implementację funkcji `add_two` tak, aby dodawała `3`:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/src/lib.rs:here}}
```

Ponownie uruchom testy:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-04-bug-in-add-two/output.txt}}
```

Nasz test wychwycił błąd! Test `tests::it_adds_two` zakończył się
niepowodzeniem, a komunikat mówi nam, że nie powiodła się asercja
`left == right`, oraz podaje wartości `left` i `right`. Ten komunikat pomaga zacząć
debugowanie: argument `left`, w którym umieściliśmy wynik wywołania
`add_two(2)`, miał wartość `5`, a argument `right` – `4`. Łatwo sobie
wyobrazić, jak bardzo jest to pomocne, gdy mamy dużo testów.

Zwróć uwagę, że w niektórych językach i frameworkach testowych parametry funkcji
sprawdzających równość nazywają się `expected` i `actual`, a kolejność podawania
argumentów ma znaczenie. W Ruście jednak nazywają się one `left` i `right`, a
kolejność, w jakiej podajemy wartość oczekiwaną i wartość zwróconą przez kod,
nie ma znaczenia. Asercję w tym teście moglibyśmy zapisać jako
`assert_eq!(4, result)`, co dałoby ten sam komunikat o niepowodzeniu,
wyświetlający `` assertion `left == right` failed ``.

Makro `assert_ne!` przechodzi, jeśli dwie przekazane mu wartości nie są równe, i
kończy się niepowodzeniem, jeśli są równe. To makro jest najbardziej przydatne,
gdy nie wiemy na pewno, jaka wartość _będzie_, ale wiemy, jaka na pewno _nie
powinna_ być. Jeśli na przykład testujemy funkcję, która na pewno w jakiś sposób
zmienia swoje dane wejściowe, ale sposób tej zmiany zależy od dnia tygodnia, w
którym uruchamiamy testy, najlepiej będzie sprawdzić za pomocą asercji, że wynik
funkcji nie jest równy danym wejściowym.

Pod spodem makra `assert_eq!` i `assert_ne!` używają odpowiednio operatorów
`==` i `!=`. Gdy asercja się nie powiedzie, makra te wypisują swoje argumenty z
formatowaniem debugowania, co oznacza, że porównywane wartości muszą
implementować *trait* (cecha typu, zbliżona do interfejsu) `PartialEq` oraz
trait `Debug`. Wszystkie typy prymitywne i większość typów z biblioteki
standardowej implementuje te traity. W przypadku zdefiniowanych przez ciebie
struktur i typów *enum* (typ wyliczeniowy) musisz zaimplementować `PartialEq`,
aby sprawdzać za pomocą asercji równość wartości tych typów. Musisz też
zaimplementować `Debug`, aby można było wypisać wartości, gdy asercja się nie
powiedzie. Ponieważ oba te traity da się wyprowadzić (*derive*), o czym
wspominaliśmy przy listingu 5-12 w rozdziale 5, zwykle wystarczy dodać adnotację
`#[derive(PartialEq, Debug)]` do definicji struktury lub enuma. Więcej
szczegółów o tych i innych traitach wyprowadzalnych znajdziesz w dodatku C,
[„Traity wyprowadzalne”][derivable-traits]<!-- ignore -->.

### Dodawanie własnych komunikatów o niepowodzeniu {#adding-custom-failure-messages}

Do makr `assert!`, `assert_eq!` i `assert_ne!` możesz też przekazać jako
argumenty opcjonalne własny komunikat, który zostanie wypisany razem z
komunikatem o niepowodzeniu. Wszystkie argumenty podane po argumentach
wymaganych są przekazywane do makra `format!` (omawianego w podrozdziale
[„Łączenie za pomocą `+` lub `format!`”][concatenating]<!--
ignore --> w rozdziale 8), więc możesz przekazać łańcuch formatujący zawierający
symbole zastępcze (*placeholder*) `{}` oraz wartości, które mają je wypełnić.
Własne komunikaty przydają się do dokumentowania znaczenia asercji; gdy test
zakończy się niepowodzeniem, łatwiej zrozumiesz, na czym polega problem z kodem.

Załóżmy na przykład, że mamy funkcję, która wita ludzi po imieniu, i chcemy
przetestować, że imię przekazane do funkcji pojawia się w jej wyniku:

<span class="filename">Plik: src/lib.rs</span>
```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-05-greeter/src/lib.rs}}
```

Wymagania dotyczące tego programu nie zostały jeszcze uzgodnione i jesteśmy
niemal pewni, że tekst `Hello` na początku powitania się zmieni. Uznaliśmy, że
nie chcemy aktualizować testu przy każdej zmianie wymagań, więc zamiast
sprawdzać dokładną równość z wartością zwracaną przez funkcję `greeting`,
sprawdzimy za pomocą asercji tylko to, czy wynik zawiera tekst parametru
wejściowego.

Wprowadźmy teraz do tego kodu błąd, zmieniając `greeting` tak, aby pomijała
`name`, i zobaczmy, jak wygląda domyślny komunikat o niepowodzeniu testu:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/src/lib.rs:here}}
```

Uruchomienie tego testu daje następujący wynik:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-06-greeter-with-bug/output.txt}}
```

Ten wynik informuje jedynie, że asercja się nie powiodła i w którym wierszu się
znajduje. Bardziej przydatny komunikat o niepowodzeniu wypisałby wartość
zwróconą przez funkcję `greeting`. Dodajmy własny komunikat o niepowodzeniu,
złożony z łańcucha formatującego z symbolem zastępczym, który zostanie
wypełniony faktyczną wartością otrzymaną z funkcji `greeting`:

```rust,ignore
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/src/lib.rs:here}}
```

Teraz po uruchomieniu testu otrzymamy bardziej pouczający komunikat o błędzie:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-07-custom-failure-message/output.txt}}
```

W wyniku testu widzimy wartość, którą faktycznie otrzymaliśmy, co pomogłoby nam
ustalić, co się stało zamiast tego, czego oczekiwaliśmy.

### Sprawdzanie paniki za pomocą `should_panic` {#checking-for-panics-with-should_panic}

Oprócz sprawdzania wartości zwracanych ważne jest też sprawdzenie, czy nasz kod
obsługuje sytuacje błędne tak, jak tego oczekujemy. Weźmy na przykład typ
`Guess`, który utworzyliśmy w rozdziale 9, w listingu 9-13. Inny kod
korzystający z `Guess` polega na gwarancji, że instancje `Guess` będą zawierać
tylko wartości od 1 do 100. Możemy napisać test, który upewnia się, że próba
utworzenia instancji `Guess` z wartością spoza tego zakresu wywołuje panikę.

Robimy to, dodając do naszej funkcji testowej atrybut `should_panic`. Test
przechodzi, jeśli kod wewnątrz funkcji spanikuje; test kończy się
niepowodzeniem, jeśli kod wewnątrz funkcji nie spanikuje.

Listing 11-8 pokazuje test, który sprawdza, czy sytuacje błędne w `Guess::new`
występują wtedy, gdy się ich spodziewamy.

<Listing number="11-8" file-name="src/lib.rs" caption="Testowanie, czy dany warunek wywoła `panic!`">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-08/src/lib.rs}}
```

</Listing>

Atrybut `#[should_panic]` umieszczamy po atrybucie `#[test]`, a przed funkcją
testową, której dotyczy. Zobaczmy wynik, gdy ten test przechodzi:

```console
{{#include ../listings/ch11-writing-automated-tests/listing-11-08/output.txt}}
```

Wygląda dobrze! Wprowadźmy teraz do kodu błąd, usuwając warunek, zgodnie z
którym funkcja `new` panikuje, jeśli wartość jest większa niż 100:

```rust,not_desired_behavior,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/src/lib.rs:here}}
```

Gdy uruchomimy test z listingu 11-8, zakończy się on niepowodzeniem:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-08-guess-with-bug/output.txt}}
```

Tym razem komunikat nie jest zbyt pomocny, ale gdy spojrzymy na funkcję
testową, zobaczymy, że jest oznaczona adnotacją `#[should_panic]`. Otrzymane
niepowodzenie oznacza, że kod w funkcji testowej nie wywołał paniki.

Testy używające `should_panic` mogą być nieprecyzyjne. Test `should_panic`
przeszedłby nawet wtedy, gdyby test spanikował z innego powodu niż ten, którego
się spodziewaliśmy. Aby testy `should_panic` były bardziej precyzyjne, możemy
dodać do atrybutu `should_panic` opcjonalny parametr `expected`. Środowisko
testowe (*test harness*) upewni się wtedy, że komunikat o niepowodzeniu zawiera
podany tekst. Weźmy na przykład zmodyfikowany kod `Guess` z listingu 11-9, w
którym funkcja `new` panikuje z różnymi komunikatami w zależności od tego, czy
wartość jest za mała, czy za duża.

<Listing number="11-9" file-name="src/lib.rs" caption="Testowanie wywołania `panic!` z komunikatem paniki zawierającym podany podłańcuch">

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/listing-11-09/src/lib.rs:here}}
```

</Listing>

Ten test przejdzie, ponieważ wartość, którą umieściliśmy w parametrze
`expected` atrybutu `should_panic`, jest podłańcuchem komunikatu, z jakim
panikuje funkcja `Guess::new`. Mogliśmy podać cały oczekiwany komunikat paniki,
który w tym przypadku brzmiałby
`Guess value must be less than or equal to 100, got 200`. To, co podasz,
zależy od tego, jaka część komunikatu paniki jest unikalna lub dynamiczna, oraz
od tego, jak precyzyjny ma być test. W tym przypadku podłańcuch komunikatu
paniki wystarczy, aby upewnić się, że kod w funkcji testowej wykonuje gałąź
`else if value > 100`.

Aby zobaczyć, co się dzieje, gdy test `should_panic` z komunikatem `expected`
kończy się niepowodzeniem, ponownie wprowadźmy do kodu błąd, zamieniając
miejscami ciała bloków `if value < 1` i `else if value > 100`:

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/src/lib.rs:here}}
```

Tym razem, gdy uruchomimy test `should_panic`, zakończy się on niepowodzeniem:

```console
{{#include ../listings/ch11-writing-automated-tests/no-listing-09-guess-with-panic-msg-bug/output.txt}}
```

Komunikat o niepowodzeniu wskazuje, że ten test rzeczywiście spanikował, tak
jak oczekiwaliśmy, ale komunikat paniki nie zawierał oczekiwanego łańcucha
`less than or equal to 100`. Komunikat paniki, który faktycznie otrzymaliśmy,
brzmiał `Guess value must be greater than or equal to 1, got 200`. Teraz
możemy zacząć szukać, gdzie tkwi nasz błąd!

### Używanie `Result<T, E>` w testach {#using-resultt-e-in-tests}

Wszystkie dotychczasowe testy panikują, gdy kończą się niepowodzeniem. Możemy też
pisać testy, które używają `Result<T, E>`! Oto test z listingu 11-1 przepisany
tak, aby używał `Result<T, E>` i zamiast panikować, zwracał `Err`:

```rust,noplayground
{{#rustdoc_include ../listings/ch11-writing-automated-tests/no-listing-10-result-in-tests/src/lib.rs:here}}
```

Funkcja `it_works` ma teraz typ zwracany `Result<(), String>`. W ciele funkcji,
zamiast wywoływać makro `assert_eq!`, zwracamy `Ok(())`, gdy test przechodzi, i
`Err` z wartością typu `String` w środku, gdy test kończy się niepowodzeniem.

Pisanie testów zwracających `Result<T, E>` pozwala używać w ich ciele operatora
znaku zapytania, co bywa wygodnym sposobem pisania testów, które powinny
zakończyć się niepowodzeniem, jeśli którakolwiek operacja w nich zwróci wariant
`Err`.

Adnotacji `#[should_panic]` nie można używać w testach, które używają
`Result<T, E>`. Aby sprawdzić za pomocą asercji, że operacja zwraca wariant
`Err`, _nie_ używaj operatora znaku zapytania na wartości `Result<T, E>`. Zamiast tego użyj
`assert!(value.is_err())`.

Skoro znasz już kilka sposobów pisania testów, przyjrzyjmy się temu, co dzieje
się podczas uruchamiania testów, i poznajmy różne opcje, których możemy używać
z poleceniem `cargo test`.

{{#quiz ../quizzes/ch11-01-writing-tests.toml}}

[concatenating]: ch08-02-strings.html#concatenating-with--or-format
[bench]: https://doc.rust-lang.org/unstable-book/library-features/test.html
[ignoring]: ch11-02-running-tests.html#ignoring-tests-unless-specifically-requested
[subset]: ch11-02-running-tests.html#running-a-subset-of-tests-by-name
[controlling-how-tests-are-run]: ch11-02-running-tests.html#controlling-how-tests-are-run
[derivable-traits]: appendix-03-derivable-traits.html
[doc-comments]: ch14-02-publishing-to-crates-io.html#documentation-comments-as-tests
[paths-for-referring-to-an-item-in-the-module-tree]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

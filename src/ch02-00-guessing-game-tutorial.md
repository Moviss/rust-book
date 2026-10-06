# Programujemy grę w zgadywanie {#programming-a-guessing-game}

Zanurzmy się w Ruście, realizując razem praktyczny projekt! Ten rozdział
przedstawia kilka popularnych pojęć Rusta na przykładzie prawdziwego programu.
Poznasz `let`, `match`, metody, funkcje powiązane (*associated functions*),
zewnętrzne *crate’y* (jednostki kompilacji w Ruście) i wiele więcej! W kolejnych
rozdziałach omówimy te zagadnienia dokładniej. W tym rozdziale po prostu
przećwiczysz podstawy.

Zaimplementujemy klasyczne zadanie dla początkujących programistów: grę w
zgadywanie. Działa ona tak: program losuje liczbę całkowitą od 1 do 100, a
następnie prosi gracza o podanie odpowiedzi. Po wpisaniu odpowiedzi program
informuje, czy podana liczba jest za mała, czy za duża. Jeśli odpowiedź jest
poprawna, gra wyświetla gratulacje i kończy działanie.

> **Uwaga:** w tym rozdziale nie ma quizów, ponieważ ma on jedynie pozwolić ci poczuć, jak wygląda ten język.

## Tworzenie nowego projektu {#setting-up-a-new-project}

Aby utworzyć nowy projekt, przejdź do katalogu _projects_ utworzonego w
rozdziale 1 i za pomocą Cargo utwórz nowy projekt w ten sposób:

```console
$ cargo new guessing_game
$ cd guessing_game
```

Pierwsze polecenie, `cargo new`, przyjmuje jako pierwszy argument nazwę projektu
(`guessing_game`). Drugie polecenie przechodzi do katalogu nowego projektu.

Zajrzyj do wygenerowanego pliku _Cargo.toml_:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial
rm -rf no-listing-01-cargo-new
cargo new no-listing-01-cargo-new --name guessing_game
cd no-listing-01-cargo-new
cargo run > output.txt 2>&1
cd ../../..
-->

<span class="filename">Plik: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/Cargo.toml}}
```

Jak już wiesz z rozdziału 1, `cargo new` generuje dla ciebie program „Hello,
world!”. Zajrzyj do pliku _src/main.rs_:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/src/main.rs}}
```

Teraz skompilujmy ten program „Hello, world!” i uruchommy go w jednym kroku za
pomocą polecenia `cargo run`:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-01-cargo-new/output.txt}}
```

Polecenie `run` przydaje się, gdy trzeba szybko wprowadzać w projekcie kolejne
zmiany, tak jak zrobimy to w tej grze, szybko sprawdzając każdą wersję przed
przejściem do następnej.

Otwórz ponownie plik _src/main.rs_. Cały kod będziesz pisać w tym pliku.

## Przetwarzanie odpowiedzi gracza {#processing-a-guess}

Pierwsza część programu gry poprosi użytkownika o dane wejściowe, przetworzy je
i sprawdzi, czy mają oczekiwaną postać. Na początek pozwolimy graczowi wpisać
odpowiedź. Wpisz do pliku _src/main.rs_ kod z listingu 2-1.

<Listing number="2-1" file-name="src/main.rs" caption="Kod, który pobiera odpowiedź od użytkownika i ją wypisuje">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:all}}
```

</Listing>

Ten kod zawiera sporo informacji, więc przejdźmy przez niego linia po linii. Aby
pobrać dane od użytkownika, a następnie wypisać wynik, musimy wprowadzić do
zasięgu (*scope*) bibliotekę wejścia-wyjścia `io`. Biblioteka `io` pochodzi z
biblioteki standardowej, znanej jako `std`:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:io}}
```

Domyślnie Rust ma zestaw elementów zdefiniowanych w bibliotece standardowej,
które wprowadza do zasięgu każdego programu. Ten zestaw nazywa się _prelude_
(zestaw elementów importowanych automatycznie), a jego pełną zawartość możesz
zobaczyć [w dokumentacji biblioteki standardowej][prelude].

Jeśli typu, którego chcesz użyć, nie ma w prelude, musisz jawnie wprowadzić go
do zasięgu za pomocą instrukcji (*statement*) `use`. Użycie biblioteki `std::io`
daje ci dostęp do wielu przydatnych funkcji, w tym do możliwości przyjmowania
danych od użytkownika.

Jak pokazaliśmy w rozdziale 1, funkcja `main` jest punktem wejścia do programu:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:main}}
```

Składnia `fn` deklaruje nową funkcję; nawiasy `()` wskazują, że funkcja nie ma
parametrów; a nawias klamrowy `{` rozpoczyna ciało funkcji.

Z rozdziału 1 wiesz też, że `println!` to makro, które wypisuje łańcuch znaków
(*string*) na ekranie:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print}}
```

Ten kod wypisuje komunikat informujący, na czym polega gra, i prosi użytkownika
o dane wejściowe.

### Przechowywanie wartości w zmiennych {#storing-values-with-variables}

Następnie utworzymy _zmienną_, w której zapiszemy dane od użytkownika:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:string}}
```

Teraz program zaczyna być interesujący! W tej krótkiej linii dzieje się bardzo
dużo. Do utworzenia zmiennej używamy instrukcji `let`. Oto kolejny przykład:

```rust,ignore
let apples = 5;
```

Ta linia tworzy nową zmienną o nazwie `apples` i wiąże ją z wartością `5`. W
Ruście zmienne są domyślnie niemutowalne (*immutable*), co oznacza, że gdy już
nadamy zmiennej wartość, ta wartość się nie zmieni. Szczegółowo omówimy to
pojęcie w podrozdziale [„Zmienne i mutowalność”][variables-and-mutability]<!-- ignore -->
w rozdziale 3. Aby zmienna była mutowalna (*mutable*), dodajemy `mut` przed
jej nazwą:

```rust,ignore
let apples = 5; // immutable
let mut bananas = 5; // mutable
```

> Uwaga: składnia `//` rozpoczyna komentarz, który trwa do końca wiersza. Rust
> ignoruje całą zawartość komentarzy. Komentarze omówimy dokładniej w
> [rozdziale 3][comments]<!-- ignore -->.

Wracając do programu gry: wiesz już, że `let mut guess` wprowadzi mutowalną
zmienną o nazwie `guess`. Znak równości (`=`) mówi Rustowi, że chcemy teraz
powiązać coś ze zmienną. Po prawej stronie znaku równości znajduje się wartość,
z którą zostaje powiązana zmienna `guess`, czyli wynik wywołania `String::new`,
funkcji zwracającej nową instancję typu `String`.
[`String`][string]<!-- ignore --> to typ łańcucha znaków dostarczany przez
bibliotekę standardową; jest to rozszerzalny fragment tekstu zakodowany w UTF-8.

Składnia `::` w `::new` wskazuje, że `new` jest funkcją powiązaną typu `String`.
_Funkcja powiązana_ to funkcja zaimplementowana na typie, w tym przypadku na
`String`. Ta funkcja `new` tworzy nowy, pusty łańcuch znaków. Funkcję `new`
znajdziesz w wielu typach, ponieważ to popularna nazwa funkcji, która tworzy
nową wartość jakiegoś rodzaju.

Podsumowując, linia `let mut guess = String::new();` utworzyła mutowalną
zmienną, która jest obecnie powiązana z nową, pustą instancją typu `String`.
Uff!

### Pobieranie danych od użytkownika {#receiving-user-input}

Przypomnij sobie, że funkcjonalność wejścia-wyjścia z biblioteki standardowej
dołączyliśmy w pierwszej linii programu za pomocą `use std::io;`. Teraz
wywołamy funkcję `stdin` z modułu `io`, która pozwoli nam obsłużyć dane od
użytkownika:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:read}}
```

Gdybyśmy nie zaimportowali modułu `io` za pomocą `use std::io;` na początku
programu, nadal moglibyśmy użyć tej funkcji, zapisując jej wywołanie jako
`std::io::stdin`. Funkcja `stdin` zwraca instancję
[`std::io::Stdin`][iostdin]<!-- ignore -->, czyli typu reprezentującego uchwyt
do standardowego wejścia twojego terminala.

Następnie linia `.read_line(&mut guess)` wywołuje metodę
[`read_line`][read_line]<!--
ignore --> na uchwycie standardowego wejścia, aby pobrać dane od użytkownika.
Przekazujemy też `&mut guess` jako argument `read_line`, aby wskazać, w którym
łańcuchu znaków ma zapisać dane od użytkownika. Zadaniem `read_line` jest
pobranie wszystkiego, co użytkownik wpisze na standardowe wejście, i dopisanie
tego do łańcucha znaków (bez nadpisywania jego zawartości), dlatego
przekazujemy ten łańcuch jako argument. Argument musi być mutowalny, aby metoda
mogła zmienić zawartość łańcucha.

Znak `&` wskazuje, że ten argument jest _referencją_ (*reference*), która
pozwala wielu częściom kodu korzystać z jednego fragmentu danych bez
wielokrotnego kopiowania tych danych w pamięci. Referencje to złożony
mechanizm, a jedną z głównych zalet Rusta jest to, jak bezpieczne i łatwe jest
korzystanie z nich. Do ukończenia tego programu nie musisz znać wielu
szczegółów. Na razie wystarczy wiedzieć, że referencje, podobnie jak zmienne, są
domyślnie niemutowalne. Dlatego musisz napisać `&mut guess` zamiast `&guess`,
aby referencja była mutowalna. (Rozdział 4 wyjaśni referencje dokładniej).

<!-- Old headings. Do not remove or links may break. -->

<a id="handling-potential-failure-with-the-result-type"></a>

### Obsługa potencjalnych błędów za pomocą `Result` {#handling-potential-failure-with-result}

Wciąż omawiamy tę samą linię kodu. Teraz przechodzimy do trzeciej linii tekstu,
ale zauważ, że nadal jest to część jednej logicznej linii kodu. Kolejna część
to ta metoda:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:expect}}
```

Moglibyśmy zapisać ten kod tak:

```rust,ignore
io::stdin().read_line(&mut guess).expect("Failed to read line");
```

Jedna długa linia jest jednak trudna do czytania, dlatego najlepiej ją
podzielić. Gdy wywołujesz metodę za pomocą składni `.method_name()`, często
warto wstawić znak nowej linii i inne białe znaki, aby rozbić długie linie.
Omówmy teraz, co robi ta linia.

Jak wspomnieliśmy wcześniej, `read_line` umieszcza wszystko, co wpisze
użytkownik, w przekazanym jej łańcuchu znaków, ale zwraca też wartość `Result`.
[`Result`][result]<!--
ignore --> to [_typ wyliczeniowy_][enums]<!-- ignore -->,
często nazywany _enumem_ (*enum*), czyli typ, który może znajdować się w jednym
z kilku możliwych stanów. Każdy możliwy stan nazywamy _wariantem_.

[Rozdział 6][enums]<!-- ignore --> omówi enumy bardziej szczegółowo. Zadaniem
typów `Result` jest przechowywanie informacji potrzebnych do obsługi błędów.

Warianty `Result` to `Ok` i `Err`. Wariant `Ok` oznacza, że operacja się
powiodła, i zawiera wygenerowaną wartość. Wariant `Err` oznacza, że operacja się
nie powiodła, i zawiera informacje o tym, jak lub dlaczego do tego doszło.

Wartości typu `Result`, tak jak wartości każdego typu, mają zdefiniowane metody.
Instancja `Result` ma [metodę `expect`][expect]<!-- ignore -->, którą możesz
wywołać. Jeśli ta instancja `Result` jest wartością `Err`, `expect` spowoduje
awarię programu i wyświetli komunikat przekazany jako argument do `expect`.
Jeśli metoda `read_line` zwróci `Err`, prawdopodobnie będzie to skutek błędu
pochodzącego z systemu operacyjnego. Jeśli ta instancja `Result` jest wartością
`Ok`, `expect` weźmie wartość przechowywaną w `Ok` i zwróci ci tylko tę wartość
do dalszego użycia. W tym przypadku tą wartością jest liczba bajtów danych
wpisanych przez użytkownika.

Jeśli nie wywołasz `expect`, program się skompiluje, ale otrzymasz ostrzeżenie:

```console
{{#include ../listings/ch02-guessing-game-tutorial/no-listing-02-without-expect/output.txt}}
```

Rust ostrzega, że nie użyto wartości `Result` zwróconej przez `read_line`, co
oznacza, że program nie obsłużył możliwego błędu.

Właściwym sposobem na pozbycie się ostrzeżenia jest napisanie kodu obsługującego
błędy, ale w naszym przypadku chcemy po prostu przerwać program, gdy pojawi się
problem, więc możemy użyć `expect`. O tym, jak program może kontynuować
działanie po błędzie, dowiesz się w [rozdziale 9][recover]<!-- ignore -->.

### Wypisywanie wartości za pomocą symboli zastępczych w `println!` {#printing-values-with-println-placeholders}

Poza zamykającym nawiasem klamrowym do omówienia w dotychczasowym kodzie została
już tylko jedna linia:

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-01/src/main.rs:print_guess}}
```

Ta linia wypisuje łańcuch znaków, który zawiera teraz dane wpisane przez
użytkownika. Para nawiasów klamrowych `{}` to symbol zastępczy (*placeholder*):
wyobraź sobie `{}` jako małe szczypce kraba, które trzymają wartość na miejscu.
Przy wypisywaniu wartości zmiennej jej nazwę można umieścić wewnątrz nawiasów
klamrowych. Przy wypisywaniu wyniku obliczenia wyrażenia (*expression*) umieść w
łańcuchu formatującym puste nawiasy klamrowe, a po łańcuchu formatującym podaj
oddzieloną przecinkami listę wyrażeń, które mają zostać wypisane w kolejnych
pustych symbolach zastępczych, w tej samej kolejności. Wypisanie zmiennej i
wyniku wyrażenia w jednym wywołaniu `println!` wyglądałoby tak:

```rust
let x = 5;
let y = 10;

println!("x = {x} and y + 2 = {}", y + 2);
```

Ten kod wypisałby `x = 5 and y + 2 = 12`.

### Testowanie pierwszej części {#testing-the-first-part}

Przetestujmy pierwszą część gry. Uruchom ją za pomocą `cargo run`:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-01/
cargo clean
cargo run
input 6 -->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 6.44s
     Running `target/debug/guessing_game`
Guess the number!
Please input your guess.
6
You guessed: 6
```

Na tym etapie pierwsza część gry jest gotowa: pobieramy dane z klawiatury, a
następnie je wypisujemy.

## Generowanie sekretnej liczby {#generating-a-secret-number}

Następnie musimy wygenerować sekretną liczbę, którą użytkownik będzie próbował
odgadnąć. Sekretna liczba powinna być za każdym razem inna, aby grę można było
z przyjemnością przejść więcej niż raz. Użyjemy losowej liczby od 1 do 100, żeby
gra nie była zbyt trudna. Biblioteka standardowa Rusta nie zawiera jeszcze
funkcji do generowania liczb losowych. Zespół Rusta udostępnia jednak
[crate `rand`][randcrate], który zapewnia taką funkcjonalność.

<!-- Old headings. Do not remove or links may break. -->
<a id="using-a-crate-to-get-more-functionality"></a>

### Rozszerzanie funkcjonalności za pomocą crate’a {#increasing-functionality-with-a-crate}

Pamiętaj, że crate to zbiór plików z kodem źródłowym w Ruście. Projekt, który
budujemy, to crate binarny, czyli plik wykonywalny. Crate `rand` jest crate’em
bibliotecznym, czyli zawiera kod przeznaczony do użycia w innych programach,
którego nie można uruchomić samodzielnie.

Koordynowanie zewnętrznych crate’ów to dziedzina, w której Cargo naprawdę
błyszczy. Zanim napiszemy kod korzystający z `rand`, musimy zmodyfikować plik
_Cargo.toml_, aby dodać crate `rand` jako zależność. Otwórz teraz ten plik i
dodaj na jego końcu, pod nagłówkiem sekcji `[dependencies]`, który utworzyło
dla ciebie Cargo, następującą linię. Podaj `rand` dokładnie tak jak my, z tym
numerem wersji, inaczej przykłady kodu z tego samouczka mogą nie działać:

<!-- When updating the version of `rand` used, also update the version of
`rand` used in these files so they all match:
* ch07-04-bringing-paths-into-scope-with-the-use-keyword.md
* ch14-03-cargo-workspaces.md
-->

<span class="filename">Plik: Cargo.toml</span>

```toml
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-02/Cargo.toml:8:}}
```

W pliku _Cargo.toml_ wszystko, co następuje po nagłówku, należy do sekcji, która
trwa aż do rozpoczęcia kolejnej sekcji. W `[dependencies]` informujesz Cargo, od
jakich zewnętrznych crate’ów zależy twój projekt i jakich wersji tych crate’ów
potrzebujesz. W tym przypadku określamy crate `rand` za pomocą specyfikatora
wersji semantycznej `0.8.5`. Cargo rozumie
[wersjonowanie semantyczne][semver]<!-- ignore --> (czasem nazywane _SemVer_),
czyli standard zapisu numerów wersji. Specyfikator `0.8.5` jest tak naprawdę
skrótem od `^0.8.5`, co oznacza dowolną wersję nie niższą niż 0.8.5, ale niższą
niż 0.9.0.

Cargo uznaje, że te wersje mają publiczne API zgodne z wersją 0.8.5, a taki
zapis gwarantuje, że dostaniesz najnowsze wydanie poprawkowe, które nadal
skompiluje się z kodem z tego rozdziału. Nie ma gwarancji, że wersja 0.9.0 lub
nowsza będzie miała to samo API, z którego korzystają poniższe przykłady.

Teraz, bez zmieniania kodu, zbudujmy projekt, tak jak pokazuje listing 2-2.

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
rm Cargo.lock
cargo clean
cargo build -->

<Listing number="2-2" caption="Wynik uruchomienia `cargo build` po dodaniu crate’a `rand` jako zależności">

```console
$ cargo build
  Updating crates.io index
   Locking 15 packages to latest Rust 1.85.0 compatible versions
    Adding rand v0.8.5 (available: v0.9.0)
 Compiling proc-macro2 v1.0.93
 Compiling unicode-ident v1.0.17
 Compiling libc v0.2.170
 Compiling cfg-if v1.0.0
 Compiling byteorder v1.5.0
 Compiling getrandom v0.2.15
 Compiling rand_core v0.6.4
 Compiling quote v1.0.38
 Compiling syn v2.0.98
 Compiling zerocopy-derive v0.7.35
 Compiling zerocopy v0.7.35
 Compiling ppv-lite86 v0.2.20
 Compiling rand_chacha v0.3.1
 Compiling rand v0.8.5
 Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
  Finished `dev` profile [unoptimized + debuginfo] target(s) in 2.48s
```

</Listing>

Możesz zobaczyć inne numery wersji (ale wszystkie będą zgodne z kodem dzięki
SemVer!) i inne linie (zależnie od systemu operacyjnego), a linie mogą pojawić
się w innej kolejności.

Gdy dołączamy zewnętrzną zależność, Cargo pobiera najnowsze wersje wszystkiego,
czego ta zależność potrzebuje, z _rejestru_, czyli kopii danych z
[Crates.io][cratesio]. Crates.io to miejsce, w którym członkowie ekosystemu
Rusta publikują swoje projekty open source w Ruście, aby inni mogli z nich
korzystać.

Po zaktualizowaniu rejestru Cargo sprawdza sekcję `[dependencies]` i pobiera
wszystkie wymienione crate’y, które nie zostały jeszcze pobrane. W tym przypadku,
choć jako zależność podaliśmy tylko `rand`, Cargo pobrało też inne crate’y,
których `rand` potrzebuje do działania. Po pobraniu crate’ów Rust je kompiluje,
a następnie kompiluje projekt z dostępnymi zależnościami.

Jeśli od razu ponownie uruchomisz `cargo build` bez wprowadzania zmian, nie
zobaczysz żadnego wyniku poza linią `Finished`. Cargo wie, że już pobrało i
skompilowało zależności, a w pliku _Cargo.toml_ nie zmieniło się nic, co ich
dotyczy. Cargo wie też, że twój kod się nie zmienił, więc nie
kompiluje go ponownie. Nie mając nic do zrobienia, po prostu kończy działanie.

Jeśli otworzysz plik _src/main.rs_, wprowadzisz drobną zmianę, a potem zapiszesz
go i ponownie zbudujesz projekt, zobaczysz tylko dwie linie wyniku:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
touch src/main.rs
cargo build -->

```console
$ cargo build
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
```

Te linie pokazują, że Cargo aktualizuje kompilację tylko o twoją drobną zmianę
w pliku _src/main.rs_. Twoje zależności się nie zmieniły, więc Cargo wie, że
może ponownie wykorzystać to, co już dla nich pobrało i skompilowało.

<!-- Old headings. Do not remove or links may break. -->
<a id="ensuring-reproducible-builds-with-the-cargo-lock-file"></a>

#### Zapewnianie powtarzalnych kompilacji {#ensuring-reproducible-builds}

Cargo ma mechanizm, który gwarantuje, że za każdym razem, gdy ty lub ktokolwiek
inny zbuduje twój kod, powstanie ten sam artefakt: Cargo będzie używać tylko
tych wersji zależności, które zostały podane, dopóki nie wskażesz inaczej.
Załóżmy na przykład, że w przyszłym tygodniu ukaże się wersja 0.8.6 crate’a
`rand`, która zawiera ważną poprawkę błędu, ale też regresję, która zepsuje
twój kod. Aby sobie z tym poradzić, Rust tworzy plik _Cargo.lock_ przy
pierwszym uruchomieniu `cargo build`, więc mamy go teraz w katalogu
_guessing_game_.

Gdy budujesz projekt po raz pierwszy, Cargo ustala wszystkie wersje zależności
spełniające kryteria, a następnie zapisuje je w pliku _Cargo.lock_. Gdy
w przyszłości będziesz budować projekt, Cargo zobaczy, że plik _Cargo.lock_
istnieje, i użyje podanych w nim wersji, zamiast ponownie ustalać wersje od
zera. Dzięki temu automatycznie otrzymujesz powtarzalną kompilację. Innymi
słowy, dzięki plikowi _Cargo.lock_ twój projekt pozostanie przy wersji 0.8.5,
dopóki jawnie go nie zaktualizujesz. Ponieważ plik _Cargo.lock_ jest ważny dla
powtarzalności kompilacji, często dodaje się go do systemu kontroli wersji
razem z resztą kodu projektu.

#### Aktualizowanie crate’a do nowej wersji {#updating-a-crate-to-get-a-new-version}

Gdy _rzeczywiście_ chcesz zaktualizować crate, Cargo udostępnia polecenie
`update`, które zignoruje plik _Cargo.lock_ i ustali wszystkie najnowsze wersje
zgodne z twoją specyfikacją w _Cargo.toml_. Następnie Cargo zapisze te wersje w
pliku _Cargo.lock_. Domyślnie jednak Cargo będzie szukać tylko wersji wyższych
niż 0.8.5 i niższych niż 0.9.0. Jeśli ukazały się dwie nowe wersje crate’a
`rand`, 0.8.6 i 0.999.0, po uruchomieniu `cargo update` zobaczysz następujący wynik:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-02/
cargo update
assuming there is a new 0.8.x version of rand; otherwise use another update
as a guide to creating the hypothetical output shown here -->

```console
$ cargo update
    Updating crates.io index
     Locking 1 package to latest Rust 1.85.0 compatible version
    Updating rand v0.8.5 -> v0.8.6 (available: v0.999.0)
```

Cargo ignoruje wydanie 0.999.0. W tym momencie zauważysz też zmianę w pliku
_Cargo.lock_, która odnotowuje, że używasz teraz wersji 0.8.6 crate’a `rand`.
Aby użyć `rand` w wersji 0.999.0 lub dowolnej wersji z serii 0.999._x_,
trzeba by zmienić plik _Cargo.toml_ tak, by wyglądał następująco (nie
wprowadzaj jednak tej zmiany, ponieważ dalsze przykłady zakładają, że używasz
`rand` 0.8):

```toml
[dependencies]
rand = "0.999.0"
```

Przy następnym uruchomieniu `cargo build` Cargo zaktualizuje rejestr dostępnych
crate’ów i ponownie oceni wymagania dotyczące `rand` zgodnie z nową, podaną
przez ciebie wersją.

O [Cargo][doccargo]<!-- ignore --> i [jego ekosystemie][doccratesio]<!-- ignore -->
można powiedzieć znacznie więcej; omówimy to w rozdziale 14, ale na razie to
wszystko, co musisz wiedzieć. Cargo bardzo ułatwia ponowne wykorzystywanie
bibliotek, dzięki czemu rustowcy (*Rustaceans*) mogą pisać mniejsze projekty
złożone z wielu pakietów.

### Generowanie liczby losowej {#generating-a-random-number}

Zacznijmy używać `rand` do wygenerowania liczby do odgadnięcia. Następnym
krokiem jest zaktualizowanie pliku _src/main.rs_, tak jak pokazuje listing 2-3.

<Listing number="2-3" file-name="src/main.rs" caption="Dodanie kodu generującego liczbę losową">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-03/src/main.rs:all}}
```

</Listing>

Najpierw dodajemy linię `use rand::Rng;`. *Trait* (cecha typu, zbliżona do
interfejsu) `Rng` definiuje metody implementowane przez generatory liczb
losowych i musi znajdować się w zasięgu, abyśmy mogli używać tych metod.
Rozdział 10 omówi traity szczegółowo.

Następnie dodajemy dwie linie w środku. W pierwszej z nich wywołujemy funkcję
`rand::thread_rng`, która daje nam konkretny generator liczb losowych, którego
użyjemy: lokalny dla bieżącego wątku wykonania, z ziarnem dostarczanym przez
system operacyjny. Potem wywołujemy metodę `gen_range` na generatorze liczb
losowych. Ta metoda jest zdefiniowana przez trait `Rng`, który wprowadziliśmy do
zasięgu instrukcją `use rand::Rng;`. Metoda `gen_range` przyjmuje jako argument
wyrażenie zakresu i generuje liczbę losową z tego zakresu. Rodzaj wyrażenia
zakresu, którego tu używamy, ma postać `start..=end` i obejmuje zarówno dolną,
jak i górną granicę, więc aby zażądać liczby od 1 do 100, musimy podać
`1..=100`.

> Uwaga: nie będziesz z góry wiedzieć, których traitów użyć ani które metody i
> funkcje wywołać z danego crate’a, dlatego każdy crate ma dokumentację z
> instrukcjami użycia. Kolejną przydatną funkcją Cargo jest to, że uruchomienie
> polecenia `cargo doc --open` zbuduje lokalnie dokumentację dostarczaną przez
> wszystkie twoje zależności i otworzy ją w przeglądarce. Jeśli interesuje cię
> na przykład inna funkcjonalność crate’a `rand`, uruchom `cargo doc --open` i
> kliknij `rand` na pasku bocznym po lewej.

Druga nowa linia wypisuje sekretną liczbę. Przydaje się to podczas tworzenia
programu, by móc go przetestować, ale usuniemy ją z ostatecznej wersji. To
niezbyt ciekawa gra, jeśli program wypisuje odpowiedź zaraz po uruchomieniu!

Spróbuj uruchomić program kilka razy:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-03/
cargo run
4
cargo run
5
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 7
Please input your guess.
4
You guessed: 4

$ cargo run
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.02s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 83
Please input your guess.
5
You guessed: 5
```

Za każdym razem liczba losowa powinna być inna, a wszystkie liczby powinny
mieścić się w przedziale od 1 do 100. Świetna robota!

## Porównywanie odpowiedzi z sekretną liczbą {#comparing-the-guess-to-the-secret-number}

Skoro mamy już dane od użytkownika i liczbę losową, możemy je porównać. Ten
krok pokazuje listing 2-4. Zwróć uwagę, że ten kod jeszcze się nie skompiluje –
za chwilę wyjaśnimy dlaczego.

<Listing number="2-4" file-name="src/main.rs" caption="Obsługa możliwych wyników porównania dwóch liczb">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-04/src/main.rs:here}}
```

</Listing>

Najpierw dodajemy kolejną instrukcję `use`, która wprowadza do zasięgu typ
`std::cmp::Ordering` z biblioteki standardowej. Typ `Ordering` to kolejny enum,
z wariantami `Less`, `Greater` i `Equal`. To trzy możliwe wyniki porównania
dwóch wartości.

Następnie dodajemy na dole pięć nowych linii, które korzystają z typu
`Ordering`. Metoda `cmp` porównuje dwie wartości i można ją wywołać na
wszystkim, co da się porównać. Przyjmuje referencję do tego, z czym chcesz
porównać wartość: tutaj porównuje `guess` z `secret_number`. Następnie zwraca
wariant enuma `Ordering`, który wprowadziliśmy do zasięgu instrukcją `use`.
Używamy wyrażenia [`match`][match]<!-- ignore -->, aby zdecydować, co zrobić
dalej, na podstawie tego, który wariant `Ordering` zwróciło wywołanie `cmp` z
wartościami `guess` i `secret_number`.

Wyrażenie `match` składa się z _ramion_ (*arms*). Ramię składa się z
_wzorca_ (*pattern*), do którego dopasowujemy wartość, oraz kodu, który ma zostać wykonany,
jeśli wartość przekazana do `match` pasuje do wzorca tego ramienia. Rust bierze
wartość przekazaną do `match` i po kolei sprawdza wzorzec każdego ramienia.
Wzorce i konstrukcja `match` to potężne możliwości Rusta: pozwalają wyrazić
wiele sytuacji, które mogą spotkać twój kod, i dbają o to, by obsłużyć je
wszystkie. Omówimy je szczegółowo odpowiednio w rozdziałach 6 i 19.

Przeanalizujmy przykład z użytym tutaj wyrażeniem `match`. Załóżmy, że
użytkownik podał liczbę 50, a wylosowana tym razem sekretna liczba to 38.

Gdy kod porówna 50 z 38, metoda `cmp` zwróci `Ordering::Greater`, ponieważ 50
jest większe od 38. Wyrażenie `match` otrzymuje wartość `Ordering::Greater` i
zaczyna sprawdzać wzorzec każdego ramienia. Patrzy na wzorzec pierwszego
ramienia, `Ordering::Less`, i stwierdza, że wartość `Ordering::Greater` nie
pasuje do `Ordering::Less`, więc pomija kod w tym ramieniu i przechodzi do
następnego. Wzorzec kolejnego ramienia to `Ordering::Greater`, który _pasuje_ do
`Ordering::Greater`! Kod powiązany z tym ramieniem zostanie wykonany i wypisze
na ekranie `Too big!`. Wyrażenie `match` kończy się po pierwszym udanym
dopasowaniu, więc w tym scenariuszu nie sprawdzi już ostatniego ramienia.

Kod z listingu 2-4 jednak jeszcze się nie skompiluje. Spróbujmy:

<!--
The error numbers in this output should be that of the code **WITHOUT** the
anchor or snip comments
-->

```console
{{#include ../listings/ch02-guessing-game-tutorial/listing-02-04/output.txt}}
```

Sedno błędu mówi o _niezgodnych typach_ (*mismatched types*). Rust ma silny,
statyczny system typów. Ma jednak również wnioskowanie typów
(*type inference*). Gdy napisaliśmy `let mut guess = String::new()`, Rust potrafił
wywnioskować, że `guess` powinno być typu `String`, i nie kazał nam podawać
typu. Z kolei `secret_number` jest typu liczbowego. Kilka typów liczbowych
Rusta może przyjąć wartość od 1 do 100: `i32`, liczba 32-bitowa; `u32`, liczba
32-bitowa bez znaku; `i64`, liczba 64-bitowa; a także inne. Jeśli nie określono
inaczej, Rust domyślnie używa `i32` – i to jest typ `secret_number`, chyba że
gdzieś indziej dodasz informacje o typie, które sprawią, że Rust wywnioskuje
inny typ liczbowy. Przyczyną błędu jest to, że Rust nie potrafi porównać
łańcucha znaków z typem liczbowym.

Ostatecznie chcemy przekonwertować `String`, który program wczytuje jako dane
wejściowe, na typ liczbowy, aby móc porównać go liczbowo z sekretną liczbą.
Robimy to, dodając tę linię do ciała funkcji `main`:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/src/main.rs:here}}
```

Ta linia to:

```rust,ignore
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

Tworzymy zmienną o nazwie `guess`. Ale chwila, czy program nie ma już zmiennej o
nazwie `guess`? Ma, ale Rust uprzejmie pozwala nam przesłonić poprzednią
wartość `guess` nową. _Przesłanianie_ (*shadowing*) pozwala ponownie użyć nazwy
zmiennej `guess`, zamiast zmuszać nas do tworzenia dwóch osobnych zmiennych,
np. `guess_str` i `guess`. Omówimy to dokładniej w
[rozdziale 3][shadowing]<!-- ignore -->, ale na razie wiedz, że ta możliwość
jest często używana, gdy chcesz przekonwertować wartość z jednego typu na inny.

Wiążemy tę nową zmienną z wyrażeniem `guess.trim().parse()`. `guess` w tym
wyrażeniu odnosi się do pierwotnej zmiennej `guess`, która zawierała dane
wejściowe jako łańcuch znaków. Metoda `trim` wywołana na instancji `String`
usunie wszystkie białe znaki z początku i końca, co musimy zrobić, zanim
przekonwertujemy łańcuch na `u32`, który może zawierać tylko dane liczbowe.
Użytkownik musi nacisnąć <kbd>enter</kbd>, aby zakończyć działanie `read_line`
i wprowadzić swoją odpowiedź, co dodaje do łańcucha znak nowej linii. Jeśli na
przykład użytkownik wpisze <kbd>5</kbd> i naciśnie <kbd>enter</kbd>, `guess`
będzie wyglądać tak: `5\n`. `\n` oznacza „nową linię”. (W systemie Windows
naciśnięcie <kbd>enter</kbd> daje znak powrotu karetki i znak nowej linii,
`\r\n`). Metoda `trim` usuwa `\n` lub `\r\n`, zostawiając samo `5`.

[Metoda `parse` na łańcuchach znaków][parse]<!-- ignore --> konwertuje łańcuch
na inny typ. Tutaj używamy jej do konwersji z łańcucha na liczbę. Musimy podać
Rustowi dokładny typ liczbowy, którego chcemy, pisząc `let guess: u32`.
Dwukropek (`:`) po `guess` mówi Rustowi, że dodamy adnotację typu zmiennej.
Rust ma kilka wbudowanych typów liczbowych; widoczny tutaj `u32` to 32-bitowa
liczba całkowita bez znaku. To dobry domyślny wybór dla niewielkiej liczby
dodatniej. O innych typach liczbowych dowiesz się w
[rozdziale 3][integers]<!-- ignore -->.

Co więcej, adnotacja `u32` w tym przykładowym programie i porównanie z
`secret_number` sprawiają, że Rust wywnioskuje, że `secret_number` również
powinno być typu `u32`. Teraz więc porównujemy dwie wartości tego samego typu!

Metoda `parse` zadziała tylko na znakach, które logicznie da się przekonwertować
na liczby, więc łatwo może spowodować błąd. Gdyby na przykład łańcuch zawierał
`A👍%`, nie dałoby się go przekonwertować na liczbę. Ponieważ może się to nie
powieść, metoda `parse` zwraca typ `Result`, podobnie jak metoda `read_line`
(omówiona wcześniej w podrozdziale
[„Obsługa potencjalnych błędów za pomocą `Result`”](#handling-potential-failure-with-result)<!-- ignore -->).
Potraktujemy ten `Result` tak samo, ponownie używając metody `expect`. Jeśli
`parse` zwróci wariant `Err` typu `Result`, ponieważ nie zdołała utworzyć
liczby z łańcucha, wywołanie `expect` spowoduje awarię gry i wypisze
przekazany mu komunikat. Jeśli `parse` zdoła przekonwertować łańcuch na liczbę,
zwróci wariant `Ok` typu `Result`, a `expect` zwróci liczbę, której chcemy,
z wartości `Ok`.

Uruchommy teraz program:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-03-convert-string-to-number/
touch src/main.rs
cargo run
  76
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.26s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 58
Please input your guess.
  76
You guessed: 76
Too big!
```

Świetnie! Mimo że przed liczbą wpisano spacje, program i tak ustalił, że
użytkownik podał 76. Uruchom program kilka razy, aby sprawdzić, jak zachowuje
się przy różnych danych wejściowych: odgadnij liczbę, podaj liczbę za dużą i
podaj liczbę za małą.

Większość gry już działa, ale użytkownik może podać tylko jedną odpowiedź.
Zmieńmy to, dodając pętlę!

## Wiele prób dzięki pętli {#allowing-multiple-guesses-with-looping}

Słowo kluczowe `loop` tworzy nieskończoną pętlę. Dodamy pętlę, aby dać
użytkownikom więcej szans na odgadnięcie liczby:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-04-looping/src/main.rs:here}}
```

Jak widać, przenieśliśmy do pętli wszystko, począwszy od prośby o podanie
odpowiedzi. Pamiętaj, aby wciąć linie wewnątrz pętli o kolejne cztery spacje, i
uruchom program ponownie. Program będzie teraz w nieskończoność prosić o kolejną
odpowiedź, co w praktyce wprowadza nowy problem. Wygląda na to, że użytkownik
nie może wyjść z gry!

Użytkownik zawsze może przerwać program skrótem klawiszowym
<kbd>ctrl</kbd>-<kbd>C</kbd>. Istnieje jednak inny sposób, by uciec przed tym
nienasyconym potworem – wspomnieliśmy o nim przy omawianiu `parse` w
podrozdziale
[„Porównywanie odpowiedzi z sekretną liczbą”](#comparing-the-guess-to-the-secret-number)<!-- ignore -->:
jeśli użytkownik wpisze coś, co nie jest liczbą, program ulegnie awarii. Możemy
to wykorzystać, aby pozwolić użytkownikowi wyjść z gry, jak pokazano tutaj:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/no-listing-04-looping/
touch src/main.rs
cargo run
(too small guess)
(too big guess)
(correct guess)
quit
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.23s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 59
Please input your guess.
45
You guessed: 45
Too small!
Please input your guess.
60
You guessed: 60
Too big!
Please input your guess.
59
You guessed: 59
You win!
Please input your guess.
quit

thread 'main' panicked at src/main.rs:28:47:
Please type a number!: ParseIntError { kind: InvalidDigit }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```

Wpisanie `quit` zakończy grę, ale jak zauważysz, zrobi to również wpisanie
czegokolwiek innego, co nie jest liczbą. To, delikatnie mówiąc, nie jest
optymalne rozwiązanie; chcemy, aby gra kończyła się także po odgadnięciu
właściwej liczby.

### Kończenie gry po poprawnej odpowiedzi {#quitting-after-a-correct-guess}

Zaprogramujmy grę tak, by kończyła się, gdy użytkownik wygra, dodając
instrukcję `break`:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/no-listing-05-quitting/src/main.rs:here}}
```

Dodanie linii `break` po `You win!` sprawia, że program wychodzi z pętli, gdy
użytkownik poprawnie odgadnie sekretną liczbę. Wyjście z pętli oznacza także
zakończenie programu, ponieważ pętla jest ostatnią częścią `main`.

### Obsługa niepoprawnych danych wejściowych {#handling-invalid-input}

Aby jeszcze bardziej dopracować działanie gry, zamiast przerywać program, gdy
użytkownik wpisze coś, co nie jest liczbą, sprawmy, by gra zignorowała taką
odpowiedź i użytkownik mógł zgadywać dalej. Możemy to zrobić, zmieniając linię,
w której `guess` jest konwertowane ze `String` na `u32`, tak jak pokazuje
listing 2-5.

<Listing number="2-5" file-name="src/main.rs" caption="Ignorowanie odpowiedzi, która nie jest liczbą, i prośba o kolejną odpowiedź zamiast przerywania programu">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-05/src/main.rs:here}}
```

</Listing>

Zastępujemy wywołanie `expect` wyrażeniem `match`, aby zamiast przerywać
program w razie błędu, obsłużyć ten błąd. Pamiętaj, że `parse` zwraca typ
`Result`, a `Result` to enum z wariantami `Ok` i `Err`. Używamy tu wyrażenia
`match`, tak jak zrobiliśmy to z wynikiem `Ordering` metody `cmp`.

Jeśli `parse` zdoła przekształcić łańcuch w liczbę, zwróci wartość `Ok`
zawierającą otrzymaną liczbę. Ta wartość `Ok` będzie pasować do wzorca
pierwszego ramienia, a wyrażenie `match` po prostu zwróci wartość `num`, którą
`parse` wytworzyła i umieściła w wartości `Ok`. Ta liczba trafi dokładnie tam,
gdzie jej potrzebujemy – do nowej zmiennej `guess`, którą tworzymy.

Jeśli `parse` _nie_ zdoła przekształcić łańcucha w liczbę, zwróci wartość
`Err`, która zawiera więcej informacji o błędzie. Wartość `Err` nie pasuje do
wzorca `Ok(num)` w pierwszym ramieniu `match`, ale pasuje do wzorca `Err(_)` w
drugim ramieniu. Podkreślnik `_` to wartość, która pasuje do wszystkiego; w tym
przykładzie mówimy, że chcemy dopasować wszystkie wartości `Err`, bez względu na
to, jakie informacje zawierają. Program wykona więc kod drugiego ramienia,
`continue`, który każe programowi przejść do następnej iteracji pętli `loop` i
poprosić o kolejną odpowiedź. W efekcie program ignoruje wszystkie błędy, które
może napotkać `parse`!

Teraz wszystko w programie powinno działać zgodnie z oczekiwaniami. Spróbujmy:

<!-- manual-regeneration
cd listings/ch02-guessing-game-tutorial/listing-02-05/
cargo run
(too small guess)
(too big guess)
foo
(correct guess)
-->

```console
$ cargo run
   Compiling guessing_game v0.1.0 (file:///projects/guessing_game)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.13s
     Running `target/debug/guessing_game`
Guess the number!
The secret number is: 61
Please input your guess.
10
You guessed: 10
Too small!
Please input your guess.
99
You guessed: 99
Too big!
Please input your guess.
foo
Please input your guess.
61
You guessed: 61
You win!
```

Wspaniale! Jedna drobna, ostatnia poprawka i gra w zgadywanie będzie gotowa.
Przypomnij sobie, że program nadal wypisuje sekretną liczbę. Przydawało się to
podczas testowania, ale psuje grę. Usuńmy `println!`, który wypisuje sekretną
liczbę. Listing 2-6 przedstawia ostateczną wersję kodu.

<Listing number="2-6" file-name="src/main.rs" caption="Kompletny kod gry w zgadywanie">

```rust,ignore
{{#rustdoc_include ../listings/ch02-guessing-game-tutorial/listing-02-06/src/main.rs}}
```

</Listing>

Udało ci się zbudować grę w zgadywanie. Gratulacje!

## Podsumowanie {#summary}

Ten projekt w praktyczny sposób wprowadził cię w wiele nowych pojęć Rusta:
`let`, `match`, funkcje, korzystanie z zewnętrznych crate’ów i inne. W kilku
kolejnych rozdziałach poznasz te pojęcia bardziej szczegółowo. Rozdział 3
omawia pojęcia obecne w większości języków programowania, takie jak zmienne,
typy danych i funkcje, i pokazuje, jak używać ich w Ruście. Rozdział 4 zgłębia
własność (*ownership*), czyli mechanizm, który odróżnia Rusta od innych języków.
Rozdział 5 omawia struktury (*structs*) i składnię metod, a rozdział 6 wyjaśnia,
jak działają enumy.

[prelude]: https://doc.rust-lang.org/std/prelude/index.html
[variables-and-mutability]: ch03-01-variables-and-mutability.html#variables-and-mutability
[comments]: ch03-04-comments.html
[string]: https://doc.rust-lang.org/std/string/struct.String.html
[iostdin]: https://doc.rust-lang.org/std/io/struct.Stdin.html
[read_line]: https://doc.rust-lang.org/std/io/struct.Stdin.html#method.read_line
[result]: https://doc.rust-lang.org/std/result/enum.Result.html
[enums]: ch06-00-enums.html
[expect]: https://doc.rust-lang.org/std/result/enum.Result.html#method.expect
[recover]: ch09-02-recoverable-errors-with-result.html
[randcrate]: https://crates.io/crates/rand
[semver]: http://semver.org
[cratesio]: https://crates.io/
[doccargo]: https://doc.rust-lang.org/cargo/
[doccratesio]: https://doc.rust-lang.org/cargo/reference/publishing.html
[match]: ch06-02-match.html
[shadowing]: ch03-01-variables-and-mutability.html#shadowing
[parse]: https://doc.rust-lang.org/std/primitive.str.html#method.parse
[integers]: ch03-02-data-types.html#integer-types

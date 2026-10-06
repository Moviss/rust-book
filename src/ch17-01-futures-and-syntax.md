## Future’y i składnia async {#futures-and-the-async-syntax}

Kluczowymi elementami programowania asynchronicznego w Ruście są _future’y_
(wartości, które będą gotowe później) oraz słowa kluczowe (*keywords*) `async` i
`await`.

_Future_ to wartość, która może nie być gotowa teraz, ale stanie się gotowa w
pewnym momencie w przyszłości. (To samo pojęcie występuje w wielu językach,
czasem pod innymi nazwami, takimi jak _task_ albo _promise_). Rust udostępnia
*trait* (cechę typu, zbliżoną do interfejsu) `Future` jako element składowy,
dzięki któremu różne operacje asynchroniczne mogą być zaimplementowane za pomocą
różnych struktur danych, ale ze wspólnym interfejsem. W Ruście future’y to typy
implementujące trait `Future`. Każdy future przechowuje własne informacje o tym,
jaki postęp już nastąpił i co oznacza dla niego „gotowość”.

Słowo kluczowe `async` możesz zastosować do bloków i funkcji, aby określić, że
mogą zostać przerwane i wznowione. Wewnątrz bloku async lub funkcji
asynchronicznej możesz użyć słowa kluczowego `await`, aby _oczekiwać na future’a_
(czyli poczekać, aż stanie się gotowy). Każde miejsce, w którym oczekujesz na
future’a wewnątrz bloku lub funkcji asynchronicznej, jest potencjalnym punktem,
w którym ten blok lub ta funkcja może się wstrzymać i wznowić. Proces
sprawdzania, czy wartość future’a jest już dostępna, nazywa się _odpytywaniem_
(*polling*).

Niektóre inne języki, takie jak C# i JavaScript, również używają słów
kluczowych `async` i `await` do programowania asynchronicznego. Jeśli znasz te
języki, możesz zauważyć istotne różnice w tym, jak Rust obsługuje tę składnię.
Jak się przekonamy, jest ku temu dobry powód!

Pisząc asynchroniczny kod w Ruście, przez większość czasu używamy słów
kluczowych `async` i `await`. Rust kompiluje je do równoważnego kodu
korzystającego z traitu `Future`, podobnie jak kompiluje pętle `for` do
równoważnego kodu korzystającego z traitu `Iterator`. Ponieważ jednak Rust
udostępnia trait `Future`, możesz też w razie potrzeby zaimplementować go dla
własnych typów danych. Wiele funkcji, które zobaczymy w tym rozdziale, zwraca
typy z własnymi implementacjami traitu `Future`. Do definicji tego traitu
wrócimy pod koniec rozdziału i dokładniej przyjrzymy się temu, jak działa, ale
na razie te szczegóły wystarczą, żeby iść dalej.

Wszystko to może wydawać się nieco abstrakcyjne, więc napiszmy nasz pierwszy
program asynchroniczny: mały *web scraper* (program pobierający dane ze stron
internetowych). Przekażemy mu z wiersza poleceń dwa adresy URL, pobierzemy obie
strony współbieżnie i zwrócimy wynik tej, która zostanie pobrana jako pierwsza.
W tym przykładzie pojawi się sporo nowej składni, ale nie martw się – po drodze
wyjaśnimy wszystko, co musisz wiedzieć.

## Nasz pierwszy program asynchroniczny {#our-first-async-program}

Aby w tym rozdziale skupić się na nauce programowania asynchronicznego, a nie
na żonglowaniu elementami ekosystemu, przygotowaliśmy *crate* (jednostkę
kompilacji w Ruście) `trpl` (`trpl` to skrót od „The Rust Programming
Language”). Za pomocą reeksportowania (*re-exporting*) udostępnia on wszystkie
potrzebne typy, traity i funkcje, głównie z crate’ów
[`futures`][futures-crate]<!-- ignore --> i [`tokio`][tokio]<!-- ignore -->.
Crate `futures` jest oficjalnym miejscem eksperymentów Rusta z kodem
asynchronicznym i to właśnie w nim pierwotnie zaprojektowano trait `Future`.
Tokio to obecnie najpowszechniej używane w Ruście asynchroniczne środowisko
uruchomieniowe (*runtime*), zwłaszcza w aplikacjach webowych. Istnieją też inne
świetne środowiska uruchomieniowe, które mogą lepiej pasować do twoich potrzeb.
Pod spodem `trpl` korzystamy z crate’a `tokio`, ponieważ jest dobrze
przetestowany i szeroko używany.

W niektórych przypadkach `trpl` zmienia też nazwy oryginalnych API lub je
opakowuje, aby pozwolić ci skupić się na szczegółach istotnych dla tego
rozdziału. Jeśli chcesz zrozumieć, co robi ten crate, zachęcamy do zajrzenia do
[jego kodu źródłowego][crate-source]. Zobaczysz tam, z jakiego crate’a pochodzi
każdy reeksportowany element, a także obszerne komentarze wyjaśniające, co ten
crate robi.

Utwórz nowy projekt binarny o nazwie `hello-async` i dodaj crate `trpl` jako
zależność:

```console
$ cargo new hello-async
$ cd hello-async
$ cargo add trpl
```

Teraz możemy użyć różnych elementów dostarczanych przez `trpl`, aby napisać nasz
pierwszy program asynchroniczny. Zbudujemy małe narzędzie wiersza poleceń, które
pobiera dwie strony internetowe, wyciąga z każdej element `<title>` i wypisuje
tytuł tej strony, dla której cały ten proces zakończy się jako pierwszy.

### Definiowanie funkcji page_title {#defining-the-page_title-function}

Zacznijmy od napisania funkcji, która przyjmuje jako parametr adres URL jednej
strony, wysyła do niego żądanie i zwraca tekst elementu `<title>` (zob. listing
17-1).

<Listing number="17-1" file-name="src/main.rs" caption="Definiowanie funkcji asynchronicznej pobierającej element title ze strony HTML">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-01/src/main.rs:all}}
```

</Listing>

Najpierw definiujemy funkcję o nazwie `page_title` i oznaczamy ją słowem
kluczowym `async`. Następnie używamy funkcji `trpl::get`, aby pobrać
przekazany adres URL, i dodajemy słowo kluczowe `await`, aby oczekiwać na
odpowiedź. Aby uzyskać tekst odpowiedzi `response`, wywołujemy jej metodę
`text` i ponownie oczekujemy na wynik za pomocą słowa kluczowego `await`. Oba te
kroki są asynchroniczne. W przypadku funkcji `get` musimy poczekać, aż serwer
odeśle pierwszą część swojej odpowiedzi, która zawiera nagłówki HTTP, ciasteczka
i tak dalej, i może zostać dostarczona oddzielnie od treści odpowiedzi. Zwłaszcza
gdy treść jest bardzo duża, dotarcie całości może trochę potrwać. Ponieważ musimy
poczekać, aż dotrze _cała_ odpowiedź, metoda `text` również jest asynchroniczna.

Musimy jawnie oczekiwać na oba te future’y, ponieważ future’y w Ruście są
leniwe (*lazy*): nic nie robią, dopóki nie poprosisz ich o to słowem kluczowym
`await`. (W rzeczywistości Rust wyświetli ostrzeżenie kompilatora, jeśli nie
użyjesz future’a). Może ci to przypominać omówienie iteratorów w podrozdziale
[„Przetwarzanie serii elementów za pomocą iteratorów”][iterators-lazy]<!-- ignore -->
w rozdziale 13. Iteratory nic nie robią, dopóki nie wywołasz ich metody `next` –
bezpośrednio albo za pomocą pętli `for` lub metod takich jak `map`, które pod
spodem używają `next`. Podobnie future’y nic nie robią, dopóki jawnie ich o to
nie poprosisz. Ta leniwość pozwala Rustowi nie uruchamiać kodu asynchronicznego,
dopóki nie jest on rzeczywiście potrzebny.

> Uwaga: to inne zachowanie niż to, które widzieliśmy przy użyciu `thread::spawn`
> w podrozdziale [„Tworzenie nowego wątku za pomocą spawn”][thread-spawn]<!-- ignore -->
> w rozdziale 16, gdzie domknięcie (*closure*) przekazane do innego wątku
> zaczynało działać natychmiast. Różni się to także od podejścia do
> asynchroniczności w wielu innych językach. Jest to jednak ważne, aby Rust mógł
> zapewnić swoje gwarancje wydajności, tak samo jak w przypadku iteratorów.

Gdy mamy już `response_text`, możemy sparsować go do instancji typu `Html` za
pomocą `Html::parse`. Zamiast surowego łańcucha znaków (*string*) mamy teraz typ
danych, dzięki któremu możemy pracować z HTML-em jako bogatszą strukturą danych.
W szczególności możemy użyć metody `select_first`, aby znaleźć pierwsze
wystąpienie danego selektora CSS. Przekazując łańcuch `"title"`, otrzymamy
pierwszy element `<title>` w dokumencie, jeśli taki istnieje. Ponieważ może nie
być żadnego pasującego elementu, `select_first` zwraca `Option<ElementRef>`. Na
koniec używamy metody `Option::map`, która pozwala pracować z elementem w
`Option`, jeśli jest obecny, i nie robić nic, jeśli go nie ma. (Moglibyśmy tu
też użyć wyrażenia (*expression*) `match`, ale `map` jest bardziej idiomatyczne).
W treści funkcji przekazywanej do `map` wywołujemy `inner_html` na `title`, aby
uzyskać jego zawartość, która jest typu `String`. Ostatecznie otrzymujemy
`Option<String>`.

Zauważ, że słowo kluczowe `await` w Ruście umieszcza się _po_ wyrażeniu, na
które oczekujesz, a nie przed nim. Oznacza to, że jest to słowo kluczowe
_postfiksowe_. Jeśli używasz `async` w innych językach, może to odbiegać od
tego, co znasz, ale w Ruście znacznie ułatwia to pracę z łańcuchami wywołań
metod. W rezultacie moglibyśmy zmienić treść `page_title` tak, aby
połączyć w łańcuch wywołania funkcji `trpl::get` i `text`, z `await` pomiędzy
nimi, jak pokazano w listingu 17-2.

<Listing number="17-2" file-name="src/main.rs" caption="Łączenie wywołań w łańcuch ze słowem kluczowym `await`">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-02/src/main.rs:chaining}}
```

</Listing>

W ten sposób udało nam się napisać naszą pierwszą funkcję asynchroniczną! Zanim
dodamy w `main` kod, który ją wywoła, porozmawiajmy jeszcze chwilę o tym, co
napisaliśmy i co to oznacza.

Gdy Rust napotyka _blok_ oznaczony słowem kluczowym `async`, kompiluje go do
unikalnego, anonimowego typu danych implementującego trait `Future`. Gdy Rust
napotyka _funkcję_ oznaczoną `async`, kompiluje ją do nieasynchronicznej
funkcji, której treścią jest blok async. Typ zwracany funkcji
asynchronicznej to anonimowy typ danych, który kompilator tworzy dla tego bloku
async.

Zatem napisanie `async fn` jest równoważne napisaniu funkcji, która zwraca
_future’a_ dającego wartość typu zwracanego. Dla kompilatora definicja funkcji
taka jak `async fn page_title` z listingu 17-1 jest mniej więcej równoważna
nieasynchronicznej funkcji zdefiniowanej w ten sposób:

```rust
# extern crate trpl; // required for mdbook test
use std::future::Future;
use trpl::Html;

fn page_title(url: &str) -> impl Future<Output = Option<String>> {
    async move {
        let text = trpl::get(url).await.text().await;
        Html::parse(&text)
            .select_first("title")
            .map(|title| title.inner_html())
    }
}
```

Przeanalizujmy po kolei każdą część przekształconej wersji:

- Używa ona składni `impl Trait`, którą omawialiśmy w rozdziale 10 w
  podrozdziale [„Używanie traitów jako parametrów”][impl-trait]<!-- ignore -->.
- Zwracana wartość implementuje trait `Future` z typem powiązanym (*associated
  type*) `Output`. Zauważ, że typ `Output` to `Option<String>`, czyli to samo
  co pierwotny typ zwracany z wersji `async fn` funkcji `page_title`.
- Cały kod wywoływany w treści pierwotnej funkcji jest opakowany w blok
  `async move`. Pamiętaj, że bloki są wyrażeniami. Cały ten blok jest
  wyrażeniem zwracanym z funkcji.
- Ten blok async daje wartość typu `Option<String>`, jak przed
  chwilą opisaliśmy. Ta wartość odpowiada typowi `Output` w typie zwracanym.
  Działa to tak samo jak w przypadku innych bloków, które już znasz.
- Nowa treść funkcji jest blokiem `async move` ze względu na sposób, w jaki
  używa parametru `url`. (O różnicy między `async` a `async move` powiemy
  znacznie więcej w dalszej części rozdziału).

Teraz możemy wywołać `page_title` w `main`.

<!-- Old headings. Do not remove or links may break. -->

<a id ="determining-a-single-pages-title"></a>

### Wykonywanie funkcji asynchronicznej za pomocą środowiska uruchomieniowego {#executing-an-async-function-with-a-runtime}

Na początek pobierzemy tytuł pojedynczej strony, jak pokazano w listingu 17-3.
Niestety ten kod jeszcze się nie kompiluje.

<Listing number="17-3" file-name="src/main.rs" caption="Wywołanie funkcji `page_title` z `main` z argumentem podanym przez użytkownika">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-03/src/main.rs:main}}
```

</Listing>

Stosujemy ten sam wzorzec, którego użyliśmy do pobierania argumentów wiersza
poleceń w podrozdziale [„Przyjmowanie argumentów wiersza
poleceń”][cli-args]<!-- ignore --> w rozdziale 12. Następnie przekazujemy
argument z adresem URL do `page_title` i oczekujemy na wynik. Ponieważ wartość
zwracana przez future’a jest typu `Option<String>`, używamy wyrażenia `match`,
aby wypisać różne komunikaty w zależności od tego, czy strona miała element
`<title>`.

Słowa kluczowego `await` możemy używać wyłącznie w funkcjach lub blokach
asynchronicznych, a Rust nie pozwala oznaczyć specjalnej funkcji `main` jako
`async`.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-03
cargo build
copy just the compiler error
-->

```text
error[E0752]: `main` function is not allowed to be `async`
 --> src/main.rs:6:1
  |
6 | async fn main() {
  | ^^^^^^^^^^^^^^^ `main` function is not allowed to be `async`
```

Funkcji `main` nie można oznaczyć jako `async`, ponieważ kod asynchroniczny
wymaga _środowiska uruchomieniowego_: crate’a Rusta, który zarządza
szczegółami wykonywania kodu asynchronicznego. Funkcja `main` programu może
_zainicjalizować_ środowisko uruchomieniowe, ale sama _nie jest_ środowiskiem
uruchomieniowym. (Za chwilę zobaczymy dokładniej, dlaczego tak jest). Każdy
program w Ruście, który wykonuje kod asynchroniczny, ma co najmniej jedno
miejsce, w którym konfiguruje środowisko uruchomieniowe wykonujące future’y.

Większość języków obsługujących asynchroniczność ma wbudowane środowisko
uruchomieniowe, ale Rust nie. Zamiast tego dostępnych jest wiele różnych
asynchronicznych środowisk uruchomieniowych, z których każde idzie na inne
kompromisy, odpowiednie dla przypadku użycia, do którego jest przeznaczone. Na
przykład serwer WWW o wysokiej przepustowości, z wieloma rdzeniami procesora i
dużą ilością RAM, ma zupełnie inne potrzeby niż mikrokontroler z jednym
rdzeniem, niewielką ilością RAM i bez możliwości alokacji na stercie (*heap*).
Crate’y dostarczające te środowiska uruchomieniowe często udostępniają też
asynchroniczne wersje typowych funkcjonalności, takich jak wejście-wyjście
plikowe lub sieciowe.

Tutaj i w całej dalszej części tego rozdziału będziemy używać funkcji
`block_on` z crate’a `trpl`, która przyjmuje future’a jako argument i blokuje
bieżący wątek, dopóki ten future nie zakończy działania. Pod spodem wywołanie
`block_on` konfiguruje za pomocą crate’a `tokio` środowisko uruchomieniowe,
które służy do uruchomienia przekazanego future’a (zachowanie `block_on` z
crate’a `trpl` jest podobne do funkcji `block_on` z innych crate’ów
dostarczających środowiska uruchomieniowe). Gdy future się zakończy, `block_on`
zwraca wartość, którą ten future zwrócił.

Moglibyśmy przekazać future’a zwróconego przez `page_title` bezpośrednio do
`block_on`, a po jego zakończeniu dopasować wynikowy `Option<String>`, tak jak
próbowaliśmy w listingu 17-3. Jednak w większości przykładów w tym
rozdziale (i w większości kodu asynchronicznego w prawdziwym świecie) będziemy
robić więcej niż jedno wywołanie funkcji asynchronicznej, więc zamiast tego
przekażemy blok `async` i jawnie będziemy oczekiwać na wynik wywołania
`page_title`, jak w listingu 17-4.

<Listing number="17-4" caption="Oczekiwanie na blok async za pomocą `trpl::block_on`" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook test does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-04/src/main.rs:run}}
```

</Listing>

Gdy uruchomimy ten kod, otrzymamy zachowanie, którego początkowo oczekiwaliśmy:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-04
cargo build # skip all the build noise
cargo run -- "https://www.rust-lang.org"
# copy the output here
-->

```console
$ cargo run -- "https://www.rust-lang.org"
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.05s
     Running `target/debug/async_await 'https://www.rust-lang.org'`
The title for https://www.rust-lang.org was
            Rust Programming Language
```

Uff – w końcu mamy działający kod asynchroniczny! Zanim jednak dodamy kod, który
urządzi wyścig między dwiema stronami, wróćmy na chwilę do tego, jak działają
future’y.

Każdy _punkt oczekiwania_ (*await point*) – czyli każde miejsce, w którym kod
używa słowa kluczowego `await` – to miejsce, w którym sterowanie jest
oddawane środowisku uruchomieniowemu. Aby to działało, Rust musi śledzić stan
związany z blokiem async, tak aby środowisko uruchomieniowe mogło
rozpocząć inną pracę, a potem wrócić, gdy będzie gotowe, by ponownie spróbować
posunąć naprzód pierwszą. Jest to niewidoczna maszyna stanów, tak jakby
napisać *enum* (typ wyliczeniowy) taki jak poniższy, aby zapisywać bieżący stan
w każdym punkcie oczekiwania:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-state-machine/src/lib.rs:enum}}
```

Ręczne pisanie kodu przechodzącego między poszczególnymi stanami byłoby jednak
żmudne i podatne na błędy, zwłaszcza gdy trzeba później dodać do kodu więcej
funkcjonalności i więcej stanów. Na szczęście kompilator Rusta automatycznie
tworzy struktury danych maszyny stanów dla kodu asynchronicznego i nimi
zarządza. Wszystkie zwykłe reguły pożyczania (*borrowing*) i własności
(*ownership*) dotyczące struktur danych nadal obowiązują i, na szczęście,
kompilator zajmuje się też ich sprawdzaniem i podaje przydatne komunikaty o
błędach. Kilka z nich omówimy w dalszej części rozdziału.

Ostatecznie coś musi wykonywać tę maszynę stanów i tym czymś jest środowisko
uruchomieniowe. (Dlatego, zgłębiając temat środowisk uruchomieniowych, możesz
natknąć się na wzmianki o _egzekutorach_ (*executors*): egzekutor to część
środowiska uruchomieniowego odpowiedzialna za wykonywanie kodu
asynchronicznego).

Teraz widać, dlaczego w listingu 17-3 kompilator nie pozwolił nam uczynić samej
funkcji `main` asynchroniczną. Gdyby `main` była funkcją asynchroniczną, coś
innego musiałoby zarządzać maszyną stanów dla future’a zwróconego przez `main`,
ale `main` jest punktem startowym programu! Zamiast tego wywołaliśmy w `main`
funkcję `trpl::block_on`, aby skonfigurować środowisko uruchomieniowe i
uruchomić future’a zwróconego przez blok `async` aż do jego zakończenia.

> Uwaga: niektóre środowiska uruchomieniowe udostępniają makra, dzięki którym
> _możesz_ napisać asynchroniczną funkcję `main`. Te makra przepisują
> `async fn main() { ... }` na zwykłą `fn main`, która robi to samo, co my
> zrobiliśmy ręcznie w listingu 17-4: wywołuje funkcję, która wykonuje future’a
> do końca, tak jak robi to `trpl::block_on`.

Teraz połączmy te elementy i zobaczmy, jak możemy pisać kod współbieżny.

<!-- Old headings. Do not remove or links may break. -->

<a id="racing-our-two-urls-against-each-other"></a>

### Współbieżny wyścig dwóch adresów URL {#racing-two-urls-against-each-other-concurrently}

W listingu 17-5 wywołujemy `page_title` z dwoma różnymi adresami URL
przekazanymi z wiersza poleceń i urządzamy między nimi wyścig, wybierając tego
future’a, który zakończy się jako pierwszy.

<Listing number="17-5" caption="Wywołanie `page_title` dla dwóch adresów URL, aby sprawdzić, który zwróci wynik jako pierwszy" file-name="src/main.rs">

<!-- should_panic,noplayground because mdbook does not pass args -->

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch17-async-await/listing-17-05/src/main.rs:all}}
```

</Listing>

Zaczynamy od wywołania `page_title` dla każdego z adresów URL podanych przez
użytkownika. Wynikowe future’y zapisujemy jako `title_fut_1` i `title_fut_2`.
Pamiętaj, że one jeszcze nic nie robią, ponieważ future’y są leniwe, a my
jeszcze na nie nie oczekiwaliśmy. Następnie przekazujemy future’y do
`trpl::select`, która zwraca wartość wskazującą, który z przekazanych jej
future’ów zakończył się jako pierwszy.

> Uwaga: pod spodem `trpl::select` jest zbudowana na bardziej ogólnej funkcji
> `select` zdefiniowanej w crate’cie `futures`. Funkcja `select` z crate’a
> `futures` potrafi wiele rzeczy, których nie potrafi funkcja `trpl::select`,
> ale ma też dodatkową złożoność, którą na razie możemy pominąć.

Każdy z future’ów może całkiem zasadnie „wygrać”, więc zwracanie `Result` nie
miałoby sensu. Zamiast tego `trpl::select` zwraca typ, którego jeszcze nie
widzieliśmy: `trpl::Either`. Typ `Either` jest nieco podobny do `Result`, bo ma
dwa przypadki. W przeciwieństwie do `Result` w `Either` nie ma jednak wbudowanego
pojęcia sukcesu ani porażki. Zamiast tego używa `Left` i `Right`, aby wskazać
„jedno albo drugie”:

```rust
enum Either<A, B> {
    Left(A),
    Right(B),
}
```

Funkcja `select` zwraca `Left` z wynikiem pierwszego future’a, jeśli wygra
pierwszy argument, oraz `Right` z wynikiem drugiego future’a, jeśli to _on_
wygra. Odpowiada to kolejności, w jakiej argumenty występują w wywołaniu
funkcji: pierwszy argument jest na lewo od drugiego.

Aktualizujemy też `page_title` tak, aby zwracała ten sam adres URL, który został
do niej przekazany. Dzięki temu, jeśli strona, która odpowie pierwsza, nie ma
elementu `<title>`, który możemy odczytać, nadal możemy wypisać sensowny
komunikat. Mając tę informację, na koniec aktualizujemy wywołanie `println!`,
aby wskazywało zarówno, który adres URL zakończył się jako pierwszy, jak i jaki
jest ewentualny `<title>` strony internetowej pod tym adresem.

Udało ci się zbudować mały działający web scraper! Wybierz kilka adresów URL i
uruchom to narzędzie wiersza poleceń. Może się okazać, że niektóre strony są
konsekwentnie szybsze od innych, a w innych przypadkach szybsza strona zmienia
się między uruchomieniami. Co ważniejsze, znasz już podstawy pracy z future’ami,
więc teraz możemy zagłębić się w to, co możemy robić za pomocą programowania
asynchronicznego.

{{#quiz ../quizzes/async-01-futures-and-syntax.toml}}

[impl-trait]: ch10-02-traits.html#traits-as-parameters
[iterators-lazy]: ch13-02-iterators.html
[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[cli-args]: ch12-01-accepting-command-line-arguments.html

<!-- TODO: map source link version to version of Rust? -->

[crate-source]: https://github.com/rust-lang/book/tree/main/packages/trpl
[futures-crate]: https://crates.io/crates/futures
[tokio]: https://tokio.rs

## Hello, world! {#hello-world}

Masz już zainstalowanego Rusta, więc czas napisać pierwszy program w tym
języku. Ucząc się nowego języka, tradycyjnie pisze się mały program, który
wypisuje na ekranie tekst `Hello, world!`, więc zrobimy tu to samo!

> Uwaga: Ta książka zakłada podstawową znajomość wiersza poleceń. Rust nie
> stawia żadnych szczególnych wymagań co do edytora, narzędzi ani miejsca, w
> którym przechowujesz kod, więc jeśli wolisz zamiast wiersza poleceń używać
> IDE, śmiało korzystaj ze swojego ulubionego. Wiele IDE w jakimś stopniu
> obsługuje dziś Rusta; szczegóły znajdziesz w dokumentacji swojego IDE. Zespół
> Rusta skupia się na zapewnieniu świetnej obsługi Rusta w IDE dzięki
> `rust-analyzer`. Więcej szczegółów znajdziesz w
> [dodatku D][devtools]<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="creating-a-project-directory"></a>

### Przygotowanie katalogu projektu {#project-directory-setup}

Zacznij od utworzenia katalogu, w którym będziesz przechowywać kod w Ruście.
Dla Rusta nie ma znaczenia, gdzie znajduje się twój kod, ale na potrzeby
ćwiczeń i projektów z tej książki proponujemy utworzyć katalog _projects_ w
katalogu domowym i trzymać w nim wszystkie swoje projekty.

Otwórz terminal i wpisz poniższe polecenia, aby utworzyć katalog _projects_, a
w nim katalog na projekt „Hello, world!”.

W systemach Linux i macOS oraz w PowerShellu w systemie Windows wpisz:

```console
$ mkdir ~/projects
$ cd ~/projects
$ mkdir hello_world
$ cd hello_world
```

W wierszu poleceń CMD w systemie Windows wpisz:

```cmd
> mkdir "%USERPROFILE%\projects"
> cd /d "%USERPROFILE%\projects"
> mkdir hello_world
> cd hello_world
```

<!-- Old headings. Do not remove or links may break. -->
<a id="writing-and-running-a-rust-program"></a>

### Podstawy programu w Ruście {#rust-program-basics}

Następnie utwórz nowy plik źródłowy i nazwij go _main.rs_. Pliki Rusta zawsze
mają rozszerzenie _.rs_. Jeśli nazwa pliku składa się z więcej niż jednego
słowa, przyjęło się oddzielać słowa podkreślnikiem. Na przykład używaj nazwy
_hello_world.rs_ zamiast _helloworld.rs_.

Teraz otwórz utworzony przed chwilą plik _main.rs_ i wpisz kod z listingu 1-1.

<Listing number="1-1" file-name="main.rs" caption="Program, który wypisuje `Hello, world!`">

```rust
fn main() {
    println!("Hello, world!");
}
```

</Listing>

Zapisz plik i wróć do okna terminala w katalogu _~/projects/hello_world_. W
systemie Linux lub macOS wpisz następujące polecenia, aby skompilować i
uruchomić plik:

```console
$ rustc main.rs
$ ./main
Hello, world!
```

W systemie Windows zamiast `./main` wpisz polecenie `.\main`:

```powershell
> rustc main.rs
> .\main
Hello, world!
```

Niezależnie od systemu operacyjnego w terminalu powinien pojawić się łańcuch
znaków (*string*) `Hello, world!`. Jeśli nie widzisz tego wyniku, zajrzyj do
części [„Rozwiązywanie problemów”][troubleshooting]<!-- ignore --> w podrozdziale
„Instalacja”, gdzie opisano, jak uzyskać pomoc.

Jeśli pojawił się napis `Hello, world!` – gratulacje! Udało ci się oficjalnie
napisać program w Ruście. Tym samym jesteś programistą Rusta – witaj!

<!-- Old headings. Do not remove or links may break. -->

<a id="anatomy-of-a-rust-program"></a>

### Anatomia programu w Ruście {#the-anatomy-of-a-rust-program}

Przyjrzyjmy się dokładnie programowi „Hello, world!”. Oto pierwszy element
układanki:

```rust
fn main() {

}
```

Te linie definiują funkcję o nazwie `main`. Funkcja `main` jest wyjątkowa:
zawsze jest pierwszym kodem uruchamianym w każdym wykonywalnym programie w
Ruście. Pierwsza linia deklaruje funkcję o nazwie `main`, która nie ma
parametrów i niczego nie zwraca. Gdyby miała parametry, znalazłyby się one w
nawiasach (`()`).

Ciało funkcji jest otoczone przez `{}`. Rust wymaga nawiasów klamrowych wokół
ciała każdej funkcji. Dobrym stylem jest umieszczanie otwierającego nawiasu
klamrowego w tej samej linii co deklaracja funkcji, z jedną spacją pomiędzy.

> Uwaga: Jeśli chcesz trzymać się standardowego stylu we wszystkich projektach w
> Ruście, możesz użyć narzędzia do automatycznego formatowania o nazwie
> `rustfmt`, które sformatuje twój kod w określonym stylu (więcej o `rustfmt` w
> [dodatku D][devtools]<!-- ignore -->). Zespół Rusta dołączył to narzędzie do
> standardowej dystrybucji Rusta, podobnie jak `rustc`, więc powinno być już
> zainstalowane na twoim komputerze!

Ciało funkcji `main` zawiera następujący kod:

```rust
println!("Hello, world!");
```

Ta linia wykonuje całą pracę w tym małym programie: wypisuje tekst na ekranie.
Warto zwrócić tu uwagę na trzy ważne szczegóły.

Po pierwsze, `println!` wywołuje makro Rusta. Gdyby zamiast tego wywoływało
funkcję, zapisalibyśmy je jako `println` (bez `!`). Makra Rusta to sposób na
pisanie kodu, który generuje kod rozszerzający składnię Rusta; omówimy je
dokładniej w [rozdziale 20][ch20-macros]<!-- ignore -->. Na razie wystarczy ci
wiedza, że użycie `!` oznacza wywołanie makra zamiast zwykłej funkcji i że makra
nie zawsze podlegają tym samym regułom co funkcje.

Po drugie, widzisz łańcuch `"Hello, world!"`. Przekazujemy go jako argument do
`println!` i zostaje on wypisany na ekranie.

Po trzecie, kończymy linię średnikiem (`;`), który oznacza, że to wyrażenie
(*expression*) się zakończyło i może zacząć się następne. Większość linii kodu
w Ruście kończy się średnikiem.

<!-- Old headings. Do not remove or links may break. -->
<a id="compiling-and-running-are-separate-steps"></a>

### Kompilacja i uruchomienie {#compilation-and-execution}

Udało ci się właśnie uruchomić nowo utworzony program, więc przyjrzyjmy się
kolejno każdemu krokowi tego procesu.

Zanim uruchomisz program w Ruście, musisz go skompilować kompilatorem Rusta:
wpisz polecenie `rustc` i przekaż mu nazwę pliku źródłowego, tak jak tutaj:

```console
$ rustc main.rs
```

Jeśli znasz C lub C++, zauważysz, że przypomina to `gcc` lub `clang`. Po
udanej kompilacji Rust tworzy wykonywalny plik binarny.

W systemach Linux i macOS oraz w PowerShellu w systemie Windows możesz zobaczyć
plik wykonywalny, wpisując w powłoce polecenie `ls`:

```console
$ ls
main  main.rs
```

W systemach Linux i macOS zobaczysz dwa pliki. W PowerShellu w systemie Windows
zobaczysz te same trzy pliki co w CMD. W CMD w systemie Windows wpisz:

```cmd
> dir /B %= the /B option says to only show the file names =%
main.exe
main.pdb
main.rs
```

Widać tu plik z kodem źródłowym z rozszerzeniem _.rs_, plik wykonywalny
(_main.exe_ w systemie Windows, a _main_ na wszystkich innych platformach) oraz,
w systemie Windows, plik z informacjami do debugowania z rozszerzeniem _.pdb_.
Następnie uruchamiasz plik _main_ lub _main.exe_, w ten sposób:

```console
$ ./main # or .\main on Windows
```

Jeśli twój plik _main.rs_ zawiera program „Hello, world!”, to polecenie wypisze
w terminalu `Hello, world!`.

Jeśli lepiej znasz język dynamiczny, taki jak Ruby, Python czy JavaScript,
kompilowanie i uruchamianie programu jako osobne kroki może być dla ciebie
czymś nowym. Rust jest językiem _kompilowanym z wyprzedzeniem_
(*ahead-of-time compiled*), co oznacza, że możesz skompilować program i dać plik
wykonywalny komuś innemu, a ta osoba uruchomi go nawet bez zainstalowanego
Rusta. Jeśli dasz komuś plik _.rb_, _.py_ lub _.js_, musi on mieć zainstalowaną
implementację – odpowiednio – języka Ruby, Python lub JavaScript. Za to w tych
językach do skompilowania i uruchomienia programu wystarczy jedno polecenie.
W projektowaniu języków wszystko jest kompromisem.

Sama kompilacja za pomocą `rustc` wystarczy w prostych programach, ale gdy
projekt się rozrośnie, zechcesz zarządzać wszystkimi opcjami i łatwo udostępniać
swój kod. Za chwilę przedstawimy ci narzędzie Cargo, które pomoże ci pisać
prawdziwe programy w Ruście.

{{#quiz ../quizzes/ch01-02-hello-world.toml}}


[troubleshooting]: ch01-01-installation.html#troubleshooting
[devtools]: appendix-04-useful-development-tools.html
[ch20-macros]: ch20-05-macros.html

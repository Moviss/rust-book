## Hello, Cargo! {#hello-cargo}

Cargo to system budowania i menedżer pakietów Rusta. Większość rustowców
(*Rustaceans*) używa tego narzędzia do zarządzania swoimi projektami w Ruście,
bo Cargo wykonuje za ciebie mnóstwo zadań, takich jak budowanie kodu, pobieranie
bibliotek, od których twój kod zależy, i budowanie tych bibliotek. (Biblioteki
potrzebne twojemu kodowi nazywamy _zależnościami_).

Najprostsze programy w Ruście, takie jak ten, który napisaliśmy do tej pory, nie
mają żadnych zależności. Gdybyśmy zbudowali projekt „Hello, world!” za pomocą
Cargo, korzystałby on tylko z tej części Cargo, która odpowiada za budowanie
kodu. Gdy zaczniesz pisać bardziej złożone programy w Ruście, będziesz dodawać
zależności, a jeśli rozpoczniesz projekt z użyciem Cargo, dodawanie zależności
będzie znacznie prostsze.

Ponieważ ogromna większość projektów w Ruście korzysta z Cargo, w dalszej części
książki zakładamy, że ty również go używasz. Cargo instaluje się razem z Rustem,
jeśli korzystasz z oficjalnych instalatorów omówionych w podrozdziale
[„Instalacja”][installation]<!-- ignore -->. Jeśli Rust został zainstalowany w
inny sposób, sprawdź, czy masz Cargo, wpisując w terminalu:

```console
$ cargo --version
```

Jeśli widzisz numer wersji, Cargo jest zainstalowane! Jeśli widzisz błąd, np.
`command not found`, zajrzyj do dokumentacji wybranej metody instalacji, aby
dowiedzieć się, jak zainstalować Cargo osobno.

### Tworzenie projektu za pomocą Cargo {#creating-a-project-with-cargo}

Utwórzmy nowy projekt za pomocą Cargo i zobaczmy, czym różni się od naszego
pierwotnego projektu „Hello, world!”. Wróć do katalogu _projects_ (albo do innego
wybranego przez ciebie miejsca na kod). Następnie, w dowolnym systemie
operacyjnym, uruchom:

```console
$ cargo new hello_cargo
$ cd hello_cargo
```

Pierwsze polecenie tworzy nowy katalog i projekt o nazwie _hello_cargo_.
Nazwaliśmy nasz projekt _hello_cargo_, a Cargo tworzy jego pliki w katalogu o tej
samej nazwie.

Przejdź do katalogu _hello_cargo_ i wyświetl listę plików. Zobaczysz, że Cargo
wygenerowało dla nas dwa pliki i jeden katalog: plik _Cargo.toml_ oraz katalog
_src_ z plikiem _main.rs_ w środku.

Zainicjowało też nowe repozytorium Git wraz z plikiem _.gitignore_. Pliki Gita
nie zostaną wygenerowane, jeśli uruchomisz `cargo new` wewnątrz istniejącego
repozytorium Git; możesz zmienić to zachowanie, używając `cargo new --vcs=git`.

> Uwaga: Git to popularny system kontroli wersji. Możesz sprawić, że `cargo new`
> użyje innego systemu kontroli wersji albo żadnego, za pomocą flagi `--vcs`.
> Uruchom `cargo new --help`, aby zobaczyć dostępne opcje.

Otwórz _Cargo.toml_ w wybranym edytorze tekstu. Plik powinien wyglądać podobnie
do kodu z listingu 1-2.

<Listing number="1-2" file-name="Cargo.toml" caption="Zawartość pliku *Cargo.toml* wygenerowanego przez `cargo new`">

```toml
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
```

</Listing>

Ten plik jest w formacie [_TOML_][toml]<!-- ignore --> (_Tom’s Obvious, Minimal
Language_), którego Cargo używa do konfiguracji.

Pierwsza linia, `[package]`, to nagłówek sekcji wskazujący, że następujące po nim
instrukcje konfigurują pakiet (*package*). Gdy będziemy dodawać do tego pliku
więcej informacji, dodamy też inne sekcje.

Kolejne trzy linie ustawiają informacje konfiguracyjne, których Cargo potrzebuje
do skompilowania twojego programu: nazwę, wersję i edycję (*edition*) Rusta,
której należy użyć. O kluczu `edition` opowiemy w [dodatku E][appendix-e]<!-- ignore -->.

Ostatnia linia, `[dependencies]`, rozpoczyna sekcję, w której wymieniasz
zależności swojego projektu. W Ruście pakiety kodu nazywamy _crate’ami_ (*crate*
to jednostka kompilacji w Ruście). W tym projekcie nie będziemy potrzebować
żadnych innych crate’ów, ale w pierwszym projekcie z rozdziału 2 już tak, więc
wtedy skorzystamy z tej sekcji zależności.

Teraz otwórz _src/main.rs_ i przyjrzyj się mu:

<span class="filename">Plik: src/main.rs</span>

```rust
fn main() {
    println!("Hello, world!");
}
```

Cargo wygenerowało dla ciebie program „Hello, world!”, dokładnie taki sam jak
ten, który napisaliśmy w listingu 1-1! Jak dotąd nasz projekt różni się od
projektu wygenerowanego przez Cargo tym, że Cargo umieściło kod w katalogu
_src_, a w katalogu głównym mamy plik konfiguracyjny _Cargo.toml_.

Cargo oczekuje, że pliki źródłowe będą się znajdować w katalogu _src_. Katalog
główny projektu jest przeznaczony tylko na pliki README, informacje o licencji,
pliki konfiguracyjne i wszystko inne, co nie jest związane z twoim kodem.
Używanie Cargo pomaga utrzymać porządek w projektach. Wszystko ma swoje miejsce
i wszystko jest na swoim miejscu.

Projekt rozpoczęty bez Cargo, tak jak nasz projekt „Hello, world!”, możesz
przekształcić w projekt korzystający z Cargo. Przenieś kod
projektu do katalogu _src_ i utwórz odpowiedni plik _Cargo.toml_. Plik
_Cargo.toml_ najłatwiej uzyskać, uruchamiając `cargo init`, które utworzy go za
ciebie automatycznie.

### Budowanie i uruchamianie projektu Cargo {#building-and-running-a-cargo-project}

Zobaczmy teraz, co się zmienia, gdy budujemy i uruchamiamy program „Hello,
world!” za pomocą Cargo! Będąc w katalogu _hello_cargo_, zbuduj projekt,
wpisując następujące polecenie:

```console
$ cargo build
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 2.85 secs
```

To polecenie tworzy plik wykonywalny w _target/debug/hello_cargo_ (lub
_target\debug\hello_cargo.exe_ w systemie Windows), a nie w bieżącym katalogu.
Ponieważ domyślnie powstaje wersja debugowa, Cargo umieszcza plik binarny w
katalogu o nazwie _debug_. Plik wykonywalny możesz uruchomić tym poleceniem:

```console
$ ./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows
Hello, world!
```

Jeśli wszystko pójdzie dobrze, w terminalu powinien pojawić się napis
`Hello, world!`. Pierwsze uruchomienie `cargo build` sprawia też, że Cargo
tworzy w katalogu głównym nowy plik: _Cargo.lock_. Ten plik śledzi dokładne
wersje zależności w twoim projekcie. Ten projekt nie ma zależności, więc plik
jest dość ubogi. Nigdy nie trzeba będzie zmieniać tego pliku ręcznie; Cargo
zarządza jego zawartością za ciebie.

Właśnie zbudowaliśmy projekt za pomocą `cargo build` i uruchomiliśmy go przez
`./target/debug/hello_cargo`, ale możemy też użyć `cargo run`, aby skompilować
kod, a następnie uruchomić powstały plik wykonywalny – wszystko jednym
poleceniem:

```console
$ cargo run
    Finished dev [unoptimized + debuginfo] target(s) in 0.0 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Używanie `cargo run` jest wygodniejsze niż pamiętanie o uruchomieniu
`cargo build`, a potem wpisywanie pełnej ścieżki do pliku binarnego, dlatego
większość programistów korzysta z `cargo run`.

Zauważ, że tym razem nie zobaczyliśmy komunikatu informującego, że Cargo
kompiluje `hello_cargo`. Cargo ustaliło, że pliki się nie zmieniły, więc nie
budowało projektu ponownie, tylko uruchomiło plik binarny. Gdyby kod źródłowy
się zmienił, Cargo zbudowałoby projekt ponownie przed jego uruchomieniem i
pojawiłby się taki komunikat:

```console
$ cargo run
   Compiling hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.33 secs
     Running `target/debug/hello_cargo`
Hello, world!
```

Cargo udostępnia też polecenie `cargo check`. To polecenie szybko sprawdza twój
kod, aby upewnić się, że się kompiluje, ale nie tworzy pliku wykonywalnego:

```console
$ cargo check
   Checking hello_cargo v0.1.0 (file:///projects/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.32 secs
```

Dlaczego ktoś miałby nie chcieć pliku wykonywalnego? Często `cargo check` działa
znacznie szybciej niż `cargo build`, ponieważ pomija etap tworzenia pliku
wykonywalnego. Jeśli podczas pisania kodu stale sprawdzasz swoją pracę, dzięki
`cargo check` szybciej dowiesz się, czy projekt nadal się kompiluje! Dlatego
wielu rustowców regularnie uruchamia `cargo check` w trakcie pisania programu,
aby upewnić się, że się kompiluje. Następnie uruchamiają `cargo build`, gdy są
gotowi użyć pliku wykonywalnego.

Podsumujmy, czego dotąd dowiedzieliśmy się o Cargo:

- Projekt możemy utworzyć za pomocą `cargo new`.
- Projekt możemy zbudować za pomocą `cargo build`.
- Projekt możemy zbudować i uruchomić w jednym kroku za pomocą `cargo run`.
- Za pomocą `cargo check` możemy sprawdzić projekt pod kątem błędów, budując
  go bez tworzenia pliku binarnego.
- Cargo nie zapisuje wyniku budowania w tym samym katalogu co nasz kod, tylko w
  katalogu _target/debug_.

Dodatkową zaletą Cargo jest to, że polecenia są takie same niezależnie od
systemu operacyjnego, na którym pracujesz. Dlatego od tej pory nie będziemy już
podawać osobnych instrukcji dla Linuksa i macOS oraz dla Windowsa.

### Budowanie wersji wydaniowej {#building-for-release}

Gdy twój projekt będzie wreszcie gotowy do wydania, możesz użyć
`cargo build --release`, aby skompilować go z optymalizacjami. To polecenie
utworzy plik wykonywalny w _target/release_ zamiast w _target/debug_.
Optymalizacje sprawiają, że twój kod w Ruście działa szybciej, ale ich włączenie
wydłuża czas kompilacji programu. Dlatego istnieją dwa różne profile: jeden do
programowania, gdy chcesz budować projekt szybko i często, oraz drugi do
budowania ostatecznej wersji programu dla użytkownika – takiej, która nie będzie
wielokrotnie przebudowywana i będzie działać możliwie szybko. Jeśli mierzysz
czas działania swojego kodu testami wydajności (*benchmark*), pamiętaj, aby
uruchomić `cargo build --release` i wykonywać pomiary na pliku wykonywalnym w
_target/release_.

<!-- Old headings. Do not remove or links may break. -->
<a id="cargo-as-convention"></a>

### Korzystanie z konwencji Cargo {#leveraging-cargos-conventions}

W prostych projektach Cargo nie daje wiele w porównaniu z samym użyciem `rustc`,
ale udowodni swoją wartość, gdy twoje programy staną się bardziej złożone. Gdy
programy rozrosną się do wielu plików lub będą potrzebować zależności, znacznie
łatwiej jest pozwolić Cargo koordynować budowanie.

Choć projekt `hello_cargo` jest prosty, korzysta już z dużej części prawdziwych
narzędzi, których będziesz używać przez resztę swojej kariery z Rustem. W
praktyce, aby pracować nad dowolnym istniejącym projektem, możesz użyć
następujących poleceń, żeby pobrać kod za pomocą Gita, przejść do katalogu
projektu i go zbudować:

```console
$ git clone example.org/someproject
$ cd someproject
$ cargo build
```

Więcej informacji o Cargo znajdziesz w [jego dokumentacji][cargo].

{{#quiz ../quizzes/ch01-03-hello-cargo.toml}}


## Podsumowanie {#summary}

Twoja przygoda z Rustem zaczęła się świetnie! Z tego rozdziału wiesz już, jak:

- instalować najnowszą stabilną wersję Rusta za pomocą `rustup`;
- aktualizować Rusta do nowszej wersji;
- otwierać lokalnie zainstalowaną dokumentację;
- pisać i uruchamiać program „Hello, world!”, używając bezpośrednio `rustc`;
- tworzyć i uruchamiać nowy projekt zgodnie z konwencjami Cargo.

To świetny moment, by zbudować bardziej rozbudowany program i przyzwyczaić się
do czytania i pisania kodu w Ruście. Dlatego w rozdziale 2 napiszemy program do
gry w zgadywanie. Jeśli wolisz zacząć od poznania tego, jak w Ruście działają
popularne koncepcje programistyczne, zajrzyj do rozdziału 3, a potem wróć do
rozdziału 2.

[installation]: ch01-01-installation.html#installation
[toml]: https://toml.io
[appendix-e]: appendix-05-editions.html
[cargo]: https://doc.rust-lang.org/cargo/

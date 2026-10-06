## Publikowanie crate’a w Crates.io {#publishing-a-crate-to-cratesio}

Korzystaliśmy już z pakietów z [crates.io](https://crates.io/)<!-- ignore -->
jako zależności naszego projektu, ale możesz też dzielić się swoim kodem z
innymi, publikując własne pakiety (*package*). Rejestr, w którym publikuje się
każdy *crate* (jednostka kompilacji w Ruście), czyli
[crates.io](https://crates.io/)<!-- ignore -->, rozpowszechnia kod źródłowy
twoich pakietów, więc przechowuje przede wszystkim kod open source.

Rust i Cargo mają mechanizmy, dzięki którym opublikowany pakiet łatwiej znaleźć
i łatwiej go używać. Omówimy teraz niektóre z nich, a następnie wyjaśnimy, jak
opublikować pakiet.

### Tworzenie przydatnych komentarzy dokumentacyjnych {#making-useful-documentation-comments}

Rzetelna dokumentacja pakietów pomoże innym użytkownikom zrozumieć, jak i kiedy
z nich korzystać, więc warto poświęcić czas na jej pisanie. W rozdziale 3
omówiliśmy, jak komentować kod w Ruście za pomocą dwóch ukośników, `//`. Rust ma
też specjalny rodzaj komentarza przeznaczony do dokumentacji, nazywany po prostu
_komentarzem dokumentacyjnym_, z którego generowana
jest dokumentacja w HTML-u. Ta dokumentacja wyświetla treść komentarzy
dokumentacyjnych dla publicznych elementów API i jest przeznaczona dla
programistów, którzy chcą wiedzieć, jak _używać_ twojego crate’a, a nie jak
jest on _zaimplementowany_.

Komentarze dokumentacyjne zaczynają się od trzech ukośników, `///`, zamiast
dwóch i obsługują notację Markdown do formatowania tekstu. Umieszczaj je
bezpośrednio przed elementem, który dokumentują. Listing 14-1 pokazuje
komentarze dokumentacyjne funkcji `add_one` w crate’cie o nazwie `my_crate`.

<Listing number="14-1" file-name="src/lib.rs" caption="Komentarz dokumentacyjny funkcji">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-01/src/lib.rs}}
```

</Listing>

Podajemy tu opis tego, co robi funkcja `add_one`, rozpoczynamy sekcję z
nagłówkiem `Examples`, a potem pokazujemy kod demonstrujący, jak używać funkcji
`add_one`. Dokumentację w HTML-u możemy wygenerować z tego komentarza
dokumentacyjnego, uruchamiając `cargo doc`. To polecenie uruchamia narzędzie
`rustdoc` dostarczane razem z Rustem i umieszcza wygenerowaną dokumentację w
HTML-u w katalogu _target/doc_.

Dla wygody polecenie `cargo doc --open` zbuduje dokumentację w HTML-u dla
bieżącego crate’a (a także dokumentację wszystkich jego zależności) i otworzy
wynik w przeglądarce internetowej. Przejdź do funkcji `add_one`, a zobaczysz,
jak wyświetla się tekst z komentarzy dokumentacyjnych, co pokazuje rysunek 14-1.

<img alt="Wygenerowana dokumentacja w HTML-u funkcji `add_one` z crate’a `my_crate`" src="img/trpl14-01.png" class="center" />

<span class="caption">Rysunek 14-1: Dokumentacja w HTML-u funkcji
`add_one`</span>

#### Często używane sekcje {#commonly-used-sections}

W listingu 14-1 użyliśmy nagłówka Markdown `# Examples`, aby utworzyć w HTML-u
sekcję zatytułowaną „Examples”. Oto inne sekcje, których autorzy crate’ów
często używają w swojej dokumentacji:

- **Panics**: sytuacje, w których dokumentowana funkcja może wywołać panikę
  (*panic*). Wywołujący funkcję, którzy nie chcą, żeby ich programy panikowały,
  powinni zadbać o to, by nie wywoływać jej w takich sytuacjach.
- **Errors**: jeśli funkcja zwraca `Result`, opis rodzajów błędów, które mogą
  wystąpić, i warunków, w których mogą zostać zwrócone, pomoże wywołującym
  napisać kod obsługujący różne rodzaje błędów na różne sposoby.
- **Safety**: jeśli wywołanie funkcji jest `unsafe` (niebezpieczny kod omawiamy
  w rozdziale 20), powinna istnieć sekcja wyjaśniająca, dlaczego funkcja jest
  niebezpieczna, i opisująca niezmienniki, których przestrzegania funkcja
  oczekuje od wywołujących.

Większość komentarzy dokumentacyjnych nie potrzebuje wszystkich tych sekcji,
ale to dobra lista kontrolna przypominająca o tych aspektach kodu, o których
użytkownicy będą chcieli się dowiedzieć.

#### Komentarze dokumentacyjne jako testy {#documentation-comments-as-tests}

Dodawanie przykładowych bloków kodu do komentarzy dokumentacyjnych pomaga
pokazać, jak używać twojej biblioteki, i ma dodatkową zaletę: uruchomienie
`cargo test` wykona przykłady kodu z dokumentacji jako testy! Nie ma nic lepszego
niż dokumentacja z przykładami. Ale nie ma też nic gorszego niż przykłady, które
nie działają, bo kod zmienił się od czasu napisania dokumentacji. Jeśli
uruchomimy `cargo test` z dokumentacją funkcji `add_one` z listingu 14-1,
zobaczymy w wynikach testów sekcję, która wygląda tak:

<!-- manual-regeneration
cd listings/ch14-more-about-cargo/listing-14-01/
cargo test
copy just the doc-tests section below
-->

```text
   Doc-tests my_crate

running 1 test
test src/lib.rs - add_one (line 5) ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.27s
```

Jeśli teraz zmienimy funkcję albo przykład tak, że `assert_eq!` w przykładzie
spowoduje panikę, i ponownie uruchomimy `cargo test`, zobaczymy, że testy
dokumentacyjne wychwycą rozbieżność między przykładem a kodem!

<!-- Old headings. Do not remove or links may break. -->

<a id="commenting-contained-items"></a>

#### Komentarze do elementu zawierającego {#contained-item-comments}

Komentarz dokumentacyjny w stylu `//!` dodaje dokumentację do elementu, który
*zawiera* te komentarze, a nie do elementów, które *następują* po nich. Zwykle
używamy takich komentarzy w pliku korzenia crate’a (*crate root*; zgodnie z
konwencją jest to _src/lib.rs_) albo wewnątrz modułu, aby udokumentować crate
lub moduł jako całość.

Na przykład, aby dodać dokumentację opisującą przeznaczenie crate’a `my_crate`,
który zawiera funkcję `add_one`, dodajemy komentarze dokumentacyjne zaczynające
się od `//!` na początku pliku _src/lib.rs_, jak pokazuje listing 14-2.

<Listing number="14-2" file-name="src/lib.rs" caption="Dokumentacja crate’a `my_crate` jako całości">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-02/src/lib.rs:here}}
```

</Listing>

Zwróć uwagę, że po ostatnim wierszu zaczynającym się od `//!` nie ma żadnego
kodu. Ponieważ komentarze zaczęliśmy od `//!` zamiast `///`, dokumentujemy
element, który zawiera ten komentarz, a nie element, który po nim następuje. W
tym przypadku tym elementem jest plik _src/lib.rs_, czyli korzeń crate’a. Te
komentarze opisują cały crate.

Gdy uruchomimy `cargo doc --open`, te komentarze wyświetlą się na stronie
głównej dokumentacji `my_crate`, nad listą publicznych elementów crate’a, jak
pokazuje rysunek 14-2.

Komentarze dokumentacyjne wewnątrz elementów są przydatne zwłaszcza do opisu
crate’ów i modułów. Używaj ich, aby wyjaśnić ogólne przeznaczenie kontenera i
pomóc użytkownikom zrozumieć organizację crate’a.

<img alt="Wygenerowana dokumentacja w HTML-u z komentarzem dotyczącym całego crate’a" src="img/trpl14-02.png" class="center" />

<span class="caption">Rysunek 14-2: Wygenerowana dokumentacja `my_crate`
z komentarzem opisującym cały crate</span>

{{#quiz ../quizzes/ch14-02-publishing-to-crates-io-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="exporting-a-convenient-public-api-with-pub-use"></a>

### Eksportowanie wygodnego publicznego API {#exporting-a-convenient-public-api}

Struktura publicznego API to ważna kwestia przy publikowaniu crate’a. Osoby
korzystające z twojego crate’a znają jego strukturę gorzej niż ty i jeśli crate
ma rozbudowaną hierarchię modułów, mogą mieć trudności ze znalezieniem
elementów, których chcą użyć.

W rozdziale 7 omówiliśmy, jak upubliczniać elementy za pomocą słowa kluczowego
(*keyword*) `pub` i jak wprowadzać elementy do zasięgu (*scope*) za pomocą słowa
kluczowego `use`. Jednak struktura, która wydaje ci się sensowna podczas
tworzenia crate’a, może nie być zbyt wygodna dla jego użytkowników. Być może
zechcesz zorganizować swoje struktury (*struct*) w wielopoziomową hierarchię,
ale wtedy osoby, które chcą użyć typu zdefiniowanego głęboko w tej hierarchii,
mogą mieć problem z odkryciem, że ten typ w ogóle istnieje. Mogą też być
zirytowane koniecznością wpisywania
`use my_crate::some_module::another_module::UsefulType;` zamiast
`use my_crate::UsefulType;`.

Dobra wiadomość jest taka, że jeśli struktura _nie_ jest wygodna dla innych
korzystających z niej w innej bibliotece, nie musisz zmieniać wewnętrznej
organizacji kodu. Zamiast tego możesz reeksportować elementy za pomocą
`pub use`, tworząc strukturę publiczną różną od prywatnej. _Reeksportowanie_
(*re-exporting*) bierze publiczny element z jednego miejsca i upublicznia go w
innym, tak jakby był zdefiniowany właśnie tam.

Załóżmy na przykład, że napisaliśmy bibliotekę `art` do modelowania pojęć
artystycznych. W tej bibliotece są dwa moduły: moduł `kinds` zawierający dwa
*enumy* (typy wyliczeniowe) o nazwach `PrimaryColor` i `SecondaryColor` oraz
moduł `utils` zawierający funkcję o nazwie `mix`, jak pokazuje listing 14-3.

<Listing number="14-3" file-name="src/lib.rs" caption="Biblioteka `art` z elementami zorganizowanymi w moduły `kinds` i `utils`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-03/src/lib.rs:here}}
```

</Listing>

Rysunek 14-3 pokazuje, jak wyglądałaby strona główna dokumentacji tego crate’a
wygenerowanej przez `cargo doc`.

<img alt="Wygenerowana dokumentacja crate’a `art` z listą modułów `kinds` i `utils`" src="img/trpl14-03.png" class="center" />

<span class="caption">Rysunek 14-3: Strona główna dokumentacji `art` z listą
modułów `kinds` i `utils`</span>

Zwróć uwagę, że typy `PrimaryColor` i `SecondaryColor` nie są wymienione na
stronie głównej, podobnie jak funkcja `mix`. Aby je zobaczyć, musimy kliknąć
`kinds` i `utils`.

Inny crate zależny od tej biblioteki potrzebowałby instrukcji `use`, które
wprowadzają elementy z `art` do zasięgu, podając obecnie zdefiniowaną strukturę
modułów. Listing 14-4 pokazuje przykład crate’a, który używa elementów
`PrimaryColor` i `mix` z crate’a `art`.

<Listing number="14-4" file-name="src/main.rs" caption="Crate używający elementów crate’a `art` z wyeksportowaną strukturą wewnętrzną">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-04/src/main.rs}}
```

</Listing>

Autor kodu z listingu 14-4, który używa crate’a `art`, musiał ustalić, że
`PrimaryColor` znajduje się w module `kinds`, a `mix` w module `utils`.
Struktura modułów crate’a `art` jest ważniejsza dla programistów pracujących
nad crate’em `art` niż dla tych, którzy go używają. Struktura wewnętrzna nie
zawiera żadnych przydatnych informacji dla kogoś, kto próbuje zrozumieć, jak
używać crate’a `art`, a raczej wprowadza zamęt, bo programiści, którzy go
używają, muszą się domyślić, gdzie szukać, i muszą podawać nazwy modułów w
instrukcjach `use`.

Aby usunąć wewnętrzną organizację z publicznego API, możemy zmodyfikować kod
crate’a `art` z listingu 14-3, dodając instrukcje `pub use`, które reeksportują
elementy na najwyższym poziomie, jak pokazuje listing 14-5.

<Listing number="14-5" file-name="src/lib.rs" caption="Dodanie instrukcji `pub use` reeksportujących elementy">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-05/src/lib.rs:here}}
```

</Listing>

Dokumentacja API, którą `cargo doc` wygeneruje dla tego crate’a, będzie teraz
wymieniać reeksporty na stronie głównej i do nich linkować, jak pokazuje rysunek
14-4, dzięki czemu typy `PrimaryColor` i `SecondaryColor` oraz funkcję `mix`
łatwiej znaleźć.

<img alt="Wygenerowana dokumentacja crate’a `art` z reeksportami na stronie głównej" src="img/trpl14-04.png" class="center" />

<span class="caption">Rysunek 14-4: Strona główna dokumentacji `art` z listą
reeksportów</span>

Użytkownicy crate’a `art` nadal mogą widzieć i używać wewnętrznej struktury z
listingu 14-3, jak pokazano w listingu 14-4, albo mogą korzystać z wygodniejszej
struktury z listingu 14-5, jak pokazuje listing 14-6.

<Listing number="14-6" file-name="src/main.rs" caption="Program używający reeksportowanych elementów z crate’a `art`">

```rust,ignore
{{#rustdoc_include ../listings/ch14-more-about-cargo/listing-14-06/src/main.rs:here}}
```

</Listing>

Gdy modułów zagnieżdżonych jest wiele, reeksportowanie typów na najwyższym
poziomie za pomocą `pub use` może znacząco poprawić wygodę osób korzystających z
crate’a. Innym częstym zastosowaniem `pub use` jest reeksportowanie definicji z
zależności w bieżącym crate’cie, tak aby definicje tamtego crate’a stały się
częścią publicznego API twojego crate’a.

Tworzenie użytecznej struktury publicznego API to bardziej sztuka niż nauka i
możesz ją stopniowo dopracowywać, aż znajdziesz API, które najlepiej sprawdza
się u twoich użytkowników. Użycie `pub use` daje ci swobodę w organizowaniu
wewnętrznej struktury crate’a i oddziela tę strukturę od tego, co pokazujesz
użytkownikom. Przejrzyj kod niektórych zainstalowanych crate’ów i sprawdź, czy
ich struktura wewnętrzna różni się od publicznego API.

### Zakładanie konta w Crates.io {#setting-up-a-cratesio-account}

Zanim opublikujesz jakikolwiek crate, musisz założyć konto w
[crates.io](https://crates.io/)<!-- ignore --> i uzyskać token API. W tym celu
wejdź na stronę główną [crates.io](https://crates.io/)<!-- ignore --> i zaloguj
się przez konto GitHub. (Konto GitHub jest obecnie wymagane, ale w przyszłości
serwis może obsługiwać inne sposoby zakładania konta.) Po zalogowaniu przejdź do
ustawień konta pod adresem
[https://crates.io/me/](https://crates.io/me/)<!-- ignore --> i pobierz swój
klucz API. Następnie uruchom polecenie `cargo login` i wklej klucz API, gdy pojawi się prośba o jego podanie, na przykład tak:

```console
$ cargo login
abcdefghijklmnopqrstuvwxyz012345
```

To polecenie przekaże Cargo twój token API i zapisze go lokalnie w pliku
_~/.cargo/credentials.toml_. Pamiętaj, że ten token jest tajny: nie udostępniaj
go nikomu. Jeśli z jakiegokolwiek powodu komuś go udostępnisz, unieważnij go i
wygeneruj nowy token w [crates.io](https://crates.io/)<!-- ignore
-->.

### Dodawanie metadanych do nowego crate’a {#adding-metadata-to-a-new-crate}

Załóżmy, że masz crate, który chcesz opublikować. Przed publikacją musisz dodać
pewne metadane w sekcji `[package]` pliku _Cargo.toml_ tego crate’a.

Twój crate będzie potrzebował unikalnej nazwy. Podczas pracy nad crate’em
lokalnie możesz nazwać go, jak chcesz. Jednak nazwy crate’ów w
[crates.io](https://crates.io/)<!-- ignore --> są przydzielane według zasady
„kto pierwszy, ten lepszy”. Gdy nazwa crate’a zostanie zajęta, nikt inny nie
może opublikować crate’a o tej nazwie. Zanim spróbujesz opublikować crate,
wyszukaj nazwę, której chcesz użyć. Jeśli jest już zajęta, musisz znaleźć inną
nazwę i zmienić pole `name` w pliku _Cargo.toml_ w sekcji `[package]`, aby użyć
nowej nazwy przy publikacji, na przykład tak:

<span class="filename">Plik: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
```

Nawet jeśli wybierzesz unikalną nazwę, to gdy na tym etapie uruchomisz
`cargo publish`, aby opublikować crate, dostaniesz ostrzeżenie, a potem błąd:

<!-- manual-regeneration
Create a new package with an unregistered name, making no further modifications
  to the generated package, so it is missing the description and license fields.
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
warning: manifest has no description, license, license-file, documentation, homepage or repository.
See https://doc.rust-lang.org/cargo/reference/manifest.html#package-metadata for more info.
--snip--
error: failed to publish to registry at https://crates.io

Caused by:
  the remote server responded with an error (status 400 Bad Request): missing or empty metadata fields: description, license. Please see https://doc.rust-lang.org/cargo/reference/manifest.html for more information on configuring these fields
```

Ten błąd wynika z braku kilku kluczowych informacji: opis i licencja są
wymagane, aby inni wiedzieli, co robi twój crate i na jakich warunkach mogą z
niego korzystać. W pliku _Cargo.toml_ dodaj opis składający się z jednego lub
dwóch zdań, bo będzie on wyświetlany przy twoim crate’cie w wynikach
wyszukiwania. W polu `license` musisz podać _wartość identyfikatora licencji_.
Identyfikatory, których możesz tu użyć, znajdziesz na stronie
[Software Package Data Exchange (SPDX) fundacji Linux Foundation][spdx]. Na
przykład, aby określić, że twój crate jest objęty licencją MIT, dodaj
identyfikator `MIT`:

<span class="filename">Plik: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
license = "MIT"
```

Jeśli chcesz użyć licencji, której nie ma w SPDX, musisz umieścić jej tekst w
pliku, dołączyć ten plik do projektu, a następnie zamiast klucza `license` użyć
`license-file`, aby podać nazwę tego pliku.

Wskazówki dotyczące wyboru licencji odpowiedniej dla twojego projektu
wykraczają poza zakres tej książki. Wiele osób ze społeczności Rusta licencjonuje
swoje projekty tak samo jak Rust, czyli na podwójnej licencji
`MIT OR Apache-2.0`. Ta praktyka pokazuje, że możesz też podać kilka identyfikatorów
licencji rozdzielonych `OR`, aby objąć projekt wieloma licencjami.

Po dodaniu unikalnej nazwy, wersji, opisu i licencji plik _Cargo.toml_ projektu
gotowego do publikacji może wyglądać tak:

<span class="filename">Plik: Cargo.toml</span>

```toml
[package]
name = "guessing_game"
version = "0.1.0"
edition = "2024"
description = "A fun game where you guess what number the computer has chosen."
license = "MIT OR Apache-2.0"

[dependencies]
```

[Dokumentacja Cargo](https://doc.rust-lang.org/cargo/) opisuje inne metadane,
które możesz podać, aby inni mogli łatwiej odnaleźć twój crate i z niego
korzystać.

### Publikowanie w Crates.io {#publishing-to-cratesio}

Skoro masz już konto, zapisany token API, wybraną nazwę crate’a i podane
wymagane metadane, możesz go opublikować! Publikacja crate’a przesyła jego
konkretną wersję do [crates.io](https://crates.io/)<!-- ignore -->, aby inni
mogli z niej korzystać.

Zachowaj ostrożność, bo publikacja jest _trwała_. Wersji nie można nigdy
nadpisać, a kodu nie da się usunąć poza pewnymi szczególnymi sytuacjami. Jednym
z głównych celów crates.io jest pełnienie roli trwałego archiwum kodu, tak aby
kompilacje wszystkich projektów zależnych od crate’ów z
[crates.io](https://crates.io/)<!-- ignore --> nadal działały. Gdyby można było
usuwać wersje, realizacja tego celu byłaby niemożliwa. Nie ma za to limitu
liczby wersji crate’a, które możesz opublikować.

Uruchom ponownie polecenie `cargo publish`. Tym razem powinno się udać:

<!-- manual-regeneration
go to some valid crate, publish a new version
cargo publish
copy just the relevant lines below
-->

```console
$ cargo publish
    Updating crates.io index
   Packaging guessing_game v0.1.0 (file:///projects/guessing_game)
    Packaged 6 files, 1.2KiB (895.0B compressed)
   Verifying guessing_game v0.1.0 (file:///projects/guessing_game)
   Compiling guessing_game v0.1.0
(file:///projects/guessing_game/target/package/guessing_game-0.1.0)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.19s
   Uploading guessing_game v0.1.0 (file:///projects/guessing_game)
    Uploaded guessing_game v0.1.0 to registry `crates-io`
note: waiting for `guessing_game v0.1.0` to be available at registry
`crates-io`.
You may press ctrl-c to skip waiting; the crate should be available shortly.
   Published guessing_game v0.1.0 at registry `crates-io`
```

Gratulacje! Udało ci się udostępnić swój kod społeczności Rusta i teraz każdy
może łatwo dodać twój crate jako zależność swojego projektu.

### Publikowanie nowej wersji istniejącego crate’a {#publishing-a-new-version-of-an-existing-crate}

Gdy wprowadzisz zmiany w swoim crate’cie i zechcesz wydać nową wersję, zmień
wartość `version` w pliku _Cargo.toml_ i opublikuj crate ponownie. Na podstawie
rodzaju wprowadzonych zmian ustal odpowiedni numer następnej wersji, kierując
się [regułami wersjonowania semantycznego][semver]. Następnie uruchom
`cargo publish`, aby przesłać nową wersję.

<!-- Old headings. Do not remove or links may break. -->

<a id="removing-versions-from-cratesio-with-cargo-yank"></a>
<a id="deprecating-versions-from-cratesio-with-cargo-yank"></a>

### Wycofywanie wersji z Crates.io {#deprecating-versions-from-cratesio}

Choć nie możesz usunąć poprzednich wersji crate’a, możesz sprawić, że żadne
przyszłe projekty nie dodadzą ich jako nowej zależności. Przydaje się to, gdy
któraś wersja crate’a jest z jakiegoś powodu wadliwa. W takich sytuacjach Cargo
umożliwia wycofanie (*yanking*) wersji crate’a.

_Wycofanie_ wersji uniemożliwia nowym projektom uzależnienie się od niej, a
jednocześnie pozwala wszystkim istniejącym projektom, które od niej zależą,
nadal działać. W praktyce wycofanie oznacza, że żaden projekt z plikiem
_Cargo.lock_ nie przestanie działać, a żaden w przyszłości wygenerowany plik
_Cargo.lock_ nie będzie korzystał z wycofanej wersji.

Aby wycofać wersję crate’a, w katalogu wcześniej opublikowanego crate’a uruchom
`cargo yank` i podaj, którą wersję chcesz wycofać. Jeśli na przykład
opublikowaliśmy crate o nazwie `guessing_game` w wersji 1.0.1 i chcemy ją
wycofać, uruchomimy w katalogu projektu `guessing_game` następujące polecenie:

<!-- manual-regeneration:
cargo yank carol-test --version 2.1.0
cargo yank carol-test --version 2.1.0 --undo
-->

```console
$ cargo yank --vers 1.0.1
    Updating crates.io index
        Yank guessing_game@1.0.1
```

Dodając do polecenia `--undo`, możesz też cofnąć wycofanie i ponownie pozwolić
projektom zależeć od danej wersji:

```console
$ cargo yank --vers 1.0.1 --undo
    Updating crates.io index
      Unyank guessing_game@1.0.1
```

Wycofanie _nie_ usuwa żadnego kodu. Nie pozwala na przykład usunąć
przypadkowo przesłanych sekretów. Jeśli coś takiego się zdarzy, musisz
natychmiast zmienić te sekrety.

{{#quiz ../quizzes/ch14-02-publishing-to-crates-io-sec2.toml}}

[spdx]: https://spdx.org/licenses/
[semver]: https://semver.org/

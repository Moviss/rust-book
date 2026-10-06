## Budujemy jednowątkowy serwer WWW {#building-a-single-threaded-web-server}

Zaczniemy od napisania działającego jednowątkowego serwera WWW. Zanim
przejdziemy do kodu, rzućmy okiem na protokoły używane przy budowaniu serwerów
WWW. Ich szczegóły wykraczają poza zakres tej książki, ale krótki przegląd da ci
potrzebne informacje.

Dwa główne protokoły, z których korzystają serwery WWW, to _Hypertext Transfer
Protocol_ _(HTTP)_ i _Transmission Control Protocol_ _(TCP)_. Oba są
protokołami typu _żądanie–odpowiedź_, co oznacza, że _klient_ inicjuje żądania,
a _serwer_ nasłuchuje żądań i udziela klientowi odpowiedzi. Zawartość tych
żądań i odpowiedzi definiują protokoły.

TCP jest protokołem niższego poziomu, który opisuje szczegóły tego, jak
informacje trafiają z jednego serwera do drugiego, ale nie określa, czym te
informacje są. HTTP działa na bazie TCP i definiuje zawartość żądań i
odpowiedzi. Technicznie da się używać HTTP z innymi protokołami, ale w
zdecydowanej większości przypadków HTTP przesyła swoje dane przez TCP. Będziemy
pracować na surowych bajtach żądań i odpowiedzi TCP i HTTP.

### Nasłuchiwanie połączenia TCP {#listening-to-the-tcp-connection}

Nasz serwer WWW musi nasłuchiwać połączenia TCP, więc od tego zaczniemy.
Biblioteka standardowa oferuje moduł `std::net`, który nam to umożliwia.
Utwórzmy nowy projekt w zwykły sposób:

```console
$ cargo new hello
     Created binary (application) `hello` project
$ cd hello
```

Na początek wpisz kod z listingu 21-1 do pliku _src/main.rs_. Ten kod będzie
nasłuchiwał pod lokalnym adresem `127.0.0.1:7878` przychodzących strumieni TCP.
Gdy otrzyma przychodzący strumień, wypisze `Connection established!`.

<Listing number="21-1" file-name="src/main.rs" caption="Nasłuchiwanie przychodzących strumieni i wypisywanie komunikatu po otrzymaniu strumienia">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-01/src/main.rs}}
```

</Listing>

Za pomocą `TcpListener` możemy nasłuchiwać połączeń TCP pod adresem
`127.0.0.1:7878`. Część adresu przed dwukropkiem to adres IP oznaczający twój
komputer (jest taki sam na każdym komputerze i nie oznacza konkretnie komputera
autorów), a `7878` to port. Wybraliśmy ten port z dwóch powodów: HTTP zwykle
nie jest na nim przyjmowany, więc nasz serwer raczej nie wejdzie w konflikt z
innym serwerem WWW działającym na twojej maszynie, a 7878 to słowo _rust_
wpisane na klawiaturze telefonu.

Funkcja `bind` działa tu podobnie jak funkcja `new`: zwraca nową instancję
`TcpListener`. Nazywa się `bind`, ponieważ w sieciach podłączenie się do portu
w celu nasłuchiwania określa się mianem „wiązania z portem” (*binding to a
port*).

Funkcja `bind` zwraca `Result<T, E>`, co oznacza, że wiązanie może się nie
powieść, na przykład gdybyśmy uruchomili dwie instancje naszego programu i
dwa programy nasłuchiwałyby na tym samym porcie. Ponieważ piszemy prosty serwer
wyłącznie w celach edukacyjnych, nie będziemy się przejmować obsługą tego
rodzaju błędów; zamiast tego używamy `unwrap`, aby zatrzymać program, gdy
wystąpią błędy.

Metoda `incoming` typu `TcpListener` zwraca iterator, który daje nam sekwencję
strumieni (a dokładniej strumieni typu `TcpStream`). Pojedynczy _strumień_
(*stream*) reprezentuje otwarte połączenie między klientem a serwerem.
_Połączenie_ to nazwa całego procesu żądania i odpowiedzi, w którym klient
łączy się z serwerem, serwer generuje odpowiedź i zamyka połączenie. Będziemy
więc odczytywać dane z `TcpStream`, aby zobaczyć, co wysłał klient, a następnie
zapisywać odpowiedź do strumienia, aby odesłać dane klientowi. Ogólnie rzecz
biorąc, ta pętla `for` będzie po kolei przetwarzać każde połączenie i
dostarczać nam serię strumieni do obsłużenia.

Na razie obsługa strumienia polega na wywołaniu `unwrap`, aby zakończyć
program, jeśli strumień zawiera jakiekolwiek błędy; jeśli błędów nie ma,
program wypisuje komunikat. W następnym listingu dodamy więcej funkcjonalności
dla przypadku powodzenia. Metoda `incoming` może zwracać błędy, gdy klient łączy
się z serwerem, ponieważ tak naprawdę nie iterujemy po połączeniach, lecz po
_próbach połączenia_. Połączenie może się nie udać z wielu powodów, w dużej
mierze zależnych od systemu operacyjnego. Na przykład wiele systemów
operacyjnych ma limit jednocześnie otwartych połączeń; kolejne próby połączenia
ponad tę liczbę będą kończyć się błędem, dopóki część otwartych połączeń nie
zostanie zamknięta.

Spróbujmy uruchomić ten kod! Wywołaj `cargo run` w terminalu, a następnie
otwórz w przeglądarce adres _127.0.0.1:7878_. Przeglądarka powinna pokazać
komunikat o błędzie w rodzaju „Connection reset”, ponieważ serwer na razie nie
odsyła żadnych danych. Gdy jednak zajrzysz do terminala, zobaczysz kilka
komunikatów wypisanych w chwili, gdy przeglądarka połączyła się z serwerem!

```text
     Running `target/debug/hello`
Connection established!
Connection established!
Connection established!
```

Czasem dla jednego żądania przeglądarki zobaczysz wiele wypisanych
komunikatów; powodem może być to, że przeglądarka wysyła żądanie o stronę, a
także żądania o inne zasoby, takie jak ikona _favicon.ico_ wyświetlana na karcie
przeglądarki.

Możliwe też, że przeglądarka próbuje połączyć się z serwerem wiele razy,
ponieważ serwer nie odpowiada żadnymi danymi. Gdy `stream` wychodzi poza zasięg
(*scope*) i zostaje zwolniony (*drop*) na końcu pętli, połączenie jest
zamykane w ramach implementacji `drop`. Przeglądarki czasem radzą sobie z
zamkniętymi połączeniami, ponawiając próbę, bo problem może być chwilowy.

Przeglądarki czasem otwierają też wiele połączeń z serwerem bez wysyłania
żadnych żądań, dzięki czemu, jeśli *jednak* później je wyślą, żądania te
zostaną obsłużone szybciej. Gdy tak się dzieje, nasz serwer widzi każde połączenie bez względu na
to, czy przez to połączenie przychodzą jakieś żądania. Robi tak na przykład
wiele wersji przeglądarek opartych na Chrome; możesz wyłączyć tę optymalizację,
używając trybu prywatnego lub innej przeglądarki.

Najważniejsze jest to, że udało nam się uzyskać uchwyt do połączenia TCP!

Pamiętaj, aby zatrzymać program, naciskając <kbd>ctrl</kbd>-<kbd>C</kbd>, gdy
skończysz uruchamiać daną wersję kodu. Następnie po każdej serii zmian w kodzie
uruchom program ponownie poleceniem `cargo run`, aby mieć pewność, że działa
najnowszy kod.

### Odczytywanie żądania {#reading-the-request}

Zaimplementujmy odczytywanie żądania od przeglądarki! Aby rozdzielić
odpowiedzialności – najpierw uzyskanie połączenia, a potem wykonanie z nim
jakiejś czynności – utworzymy nową funkcję do przetwarzania połączeń. W nowej
funkcji `handle_connection` odczytamy dane ze strumienia TCP i je wypiszemy,
aby zobaczyć dane wysyłane przez przeglądarkę. Zmień kod tak, aby wyglądał jak
w listingu 21-2.

<Listing number="21-2" file-name="src/main.rs" caption="Odczytywanie danych z `TcpStream` i ich wypisywanie">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-02/src/main.rs}}
```

</Listing>

Wprowadzamy `std::io::BufReader` i `std::io::prelude` do zasięgu, aby uzyskać
dostęp do *traitów* (cech typów, zbliżonych do interfejsów) i typów, które
pozwalają odczytywać dane ze strumienia i zapisywać do niego. W pętli `for` w
funkcji `main` zamiast wypisywać komunikat o nawiązaniu połączenia, wywołujemy
teraz nową funkcję `handle_connection` i przekazujemy do niej `stream`.

W funkcji `handle_connection` tworzymy nową instancję `BufReader`, która
opakowuje referencję do `stream`. `BufReader` dodaje buforowanie, zarządzając
za nas wywołaniami metod traitu `std::io::Read`.

Tworzymy zmienną o nazwie `http_request`, aby zebrać wiersze żądania, które
przeglądarka wysyła do naszego serwera. Zaznaczamy, że chcemy zebrać te wiersze
w wektorze (*vector*), dodając adnotację typu `Vec<_>`.

`BufReader` implementuje trait `std::io::BufRead`, który udostępnia metodę
`lines`. Metoda `lines` zwraca iterator po wartościach `Result<String,
std::io::Error>`, dzieląc strumień danych za każdym razem, gdy napotka bajt
nowej linii. Aby otrzymać każdy `String`, wywołujemy `map` i `unwrap` na każdym
`Result`. `Result` może być błędem, jeśli dane nie są poprawnym UTF-8 lub jeśli
wystąpił problem z odczytem ze strumienia. Raz jeszcze: program produkcyjny
powinien obsługiwać te błędy łagodniej, ale dla prostoty w przypadku błędu
zatrzymujemy program.

Przeglądarka sygnalizuje koniec żądania HTTP, wysyłając dwa znaki nowej linii
pod rząd, więc aby pobrać ze strumienia jedno żądanie, pobieramy wiersze, dopóki
nie trafimy na wiersz będący pustym łańcuchem. Po zebraniu wierszy w wektorze
wypisujemy je, używając czytelnego formatowania debugowego, aby przyjrzeć się
instrukcjom, które przeglądarka wysyła do naszego serwera.

Wypróbujmy ten kod! Uruchom program i ponownie wyślij żądanie z przeglądarki.
Zauważ, że w przeglądarce nadal zobaczymy stronę błędu, ale wyjście programu w
terminalu będzie teraz wyglądać podobnie do tego:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-02
cargo run
make a request to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.42s
     Running `target/debug/hello`
Request: [
    "GET / HTTP/1.1",
    "Host: 127.0.0.1:7878",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.5",
    "Accept-Encoding: gzip, deflate, br",
    "DNT: 1",
    "Connection: keep-alive",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
    "Cache-Control: max-age=0",
]
```

W zależności od przeglądarki wyjście może się nieco różnić. Teraz, gdy
wypisujemy dane żądania, możemy zobaczyć, dlaczego jedno żądanie przeglądarki
daje wiele połączeń: wystarczy spojrzeć na ścieżkę po `GET` w pierwszym wierszu
żądania. Jeśli wszystkie powtórzone połączenia żądają _/_, wiemy, że
przeglądarka próbuje wielokrotnie pobrać _/_, ponieważ nie dostaje odpowiedzi od
naszego programu.

Rozłóżmy te dane żądania na części, aby zrozumieć, o co przeglądarka prosi nasz
program.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-closer-look-at-an-http-request"></a>
<a id="looking-closer-at-an-http-request"></a>

### Bliższe spojrzenie na żądanie HTTP {#looking-more-closely-at-an-http-request}

HTTP jest protokołem tekstowym, a żądanie ma następujący format:

```text
Method Request-URI HTTP-Version CRLF
headers CRLF
message-body
```

Pierwszy wiersz to _wiersz żądania_ (*request line*), który zawiera informacje
o tym, czego żąda klient. Pierwsza część wiersza żądania wskazuje używaną
metodę, taką jak `GET` lub `POST`, która opisuje, w jaki sposób klient wysyła
to żądanie. Nasz klient użył żądania `GET`, co oznacza, że prosi o informacje.

Następna część wiersza żądania to _/_, co wskazuje _ujednolicony identyfikator
zasobów_ (*uniform resource identifier*, _URI_), którego żąda klient. URI to
prawie, choć nie całkiem, to samo co _ujednolicony lokalizator zasobów_
(*uniform resource locator*, _URL_). Różnica między URI a URL nie ma znaczenia
dla naszych celów w tym rozdziale, ale specyfikacja HTTP używa terminu _URI_,
więc możemy tu w myślach zastąpić _URI_ przez _URL_.

Ostatnia część to wersja HTTP używana przez klienta, a następnie wiersz żądania
kończy się sekwencją CRLF. (_CRLF_ to skrót od _carriage return_ i _line feed_,
czyli powrotu karetki i przesunięcia o wiersz – terminów z czasów maszyn do
pisania!) Sekwencję CRLF można też zapisać jako `\r\n`, gdzie `\r` to powrót
karetki, a `\n` to przesunięcie o wiersz. _Sekwencja CRLF_ oddziela wiersz
żądania od pozostałych danych żądania. Zauważ, że gdy CRLF jest wypisywane,
widzimy początek nowej linii, a nie `\r\n`.

Patrząc na dane wiersza żądania, które otrzymaliśmy dotychczas po uruchomieniu
programu, widzimy, że metodą jest `GET`, URI żądania to _/_, a wersja to
`HTTP/1.1`.

Po wierszu żądania pozostałe wiersze, począwszy od `Host:`, to nagłówki.
Żądania `GET` nie mają treści.

Spróbuj wysłać żądanie z innej przeglądarki lub poprosić o inny adres, na
przykład _127.0.0.1:7878/test_, aby zobaczyć, jak zmieniają się dane żądania.

Skoro wiemy już, o co prosi przeglądarka, odeślijmy jakieś dane!

### Zapisywanie odpowiedzi {#writing-a-response}

Zaimplementujemy wysyłanie danych w odpowiedzi na żądanie klienta. Odpowiedzi
mają następujący format:

```text
HTTP-Version Status-Code Reason-Phrase CRLF
headers CRLF
message-body
```

Pierwszy wiersz to _wiersz statusu_ (*status line*), który zawiera wersję HTTP
użytą w odpowiedzi, liczbowy kod statusu podsumowujący wynik żądania oraz frazę
statusu (*reason phrase*), czyli tekstowy opis kodu statusu. Po sekwencji CRLF
następują ewentualne nagłówki, kolejna sekwencja CRLF i treść odpowiedzi.

Oto przykładowa odpowiedź, która używa HTTP w wersji 1.1, ma kod statusu 200,
frazę statusu OK, nie ma nagłówków ani treści:

```text
HTTP/1.1 200 OK\r\n\r\n
```

Kod statusu 200 to standardowa odpowiedź oznaczająca sukces. Ten tekst to
malutka odpowiedź HTTP oznaczająca powodzenie. Zapiszmy ją do strumienia jako
odpowiedź na pomyślne żądanie! Usuń z funkcji `handle_connection` makro
`println!`, które wypisywało dane żądania, i zastąp je kodem z listingu 21-3.

<Listing number="21-3" file-name="src/main.rs" caption="Zapisywanie do strumienia malutkiej odpowiedzi HTTP oznaczającej powodzenie">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-03/src/main.rs:here}}
```

</Listing>

Pierwszy nowy wiersz definiuje zmienną `response`, która przechowuje dane
komunikatu o powodzeniu. Następnie wywołujemy `as_bytes` na `response`, aby
przekonwertować dane łańcucha na bajty. Metoda `write_all` wywoływana na
`stream` przyjmuje `&[u8]` i wysyła te bajty bezpośrednio przez połączenie.
Ponieważ operacja `write_all` może się nie powieść, tak jak wcześniej używamy
`unwrap` na ewentualnym wyniku z błędem. I znów: w prawdziwej aplikacji
należałoby tu dodać obsługę błędów.

Po tych zmianach uruchommy kod i wyślijmy żądanie. Nie wypisujemy już żadnych
danych w terminalu, więc poza wyjściem Cargo nic nie zobaczymy. Gdy otworzysz
w przeglądarce adres _127.0.0.1:7878_, zamiast błędu powinna pojawić się pusta
strona. Udało ci się właśnie ręcznie zaprogramować odbieranie żądania HTTP i
wysyłanie odpowiedzi!

### Zwracanie prawdziwego HTML-a {#returning-real-html}

Zaimplementujmy zwracanie czegoś więcej niż pustej strony. Utwórz nowy plik
_hello.html_ w katalogu głównym projektu, a nie w katalogu _src_. Możesz wpisać
dowolny HTML; listing 21-4 pokazuje jedną z możliwości.

<Listing number="21-4" file-name="hello.html" caption="Przykładowy plik HTML do zwrócenia w odpowiedzi">

```html
{{#include ../listings/ch21-web-server/listing-21-05/hello.html}}
```

</Listing>

To minimalny dokument HTML5 z nagłówkiem i odrobiną tekstu. Aby serwer zwracał
go po otrzymaniu żądania, zmodyfikujemy `handle_connection` tak jak w listingu
21-5, aby odczytać plik HTML, dodać go do odpowiedzi jako treść i wysłać.

<Listing number="21-5" file-name="src/main.rs" caption="Wysyłanie zawartości pliku *hello.html* jako treści odpowiedzi">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-05/src/main.rs:here}}
```

</Listing>

Dodaliśmy `fs` do instrukcji `use`, aby wprowadzić do zasięgu moduł systemu
plików z biblioteki standardowej. Kod odczytujący zawartość pliku do łańcucha
powinien wyglądać znajomo; używaliśmy go, gdy odczytywaliśmy zawartość pliku w
naszym projekcie wejścia-wyjścia w listingu 12-4.

Następnie za pomocą `format!` dodajemy zawartość pliku jako treść odpowiedzi
oznaczającej powodzenie. Aby odpowiedź HTTP była poprawna, dodajemy nagłówek
`Content-Length`, ustawiony na rozmiar treści odpowiedzi – w tym wypadku na
rozmiar `hello.html`.

Uruchom ten kod poleceniem `cargo run` i otwórz w przeglądarce adres
_127.0.0.1:7878_; powinien wyświetlić się twój HTML!

Obecnie ignorujemy dane żądania w `http_request` i bezwarunkowo odsyłamy
zawartość pliku HTML. Oznacza to, że jeśli spróbujesz otworzyć w przeglądarce
adres _127.0.0.1:7878/something-else_, nadal otrzymasz tę samą odpowiedź HTML.
Na razie nasz serwer jest bardzo ograniczony i nie robi tego, co robi większość
serwerów WWW. Chcemy dostosowywać odpowiedzi do żądania i odsyłać plik HTML
tylko w odpowiedzi na poprawnie sformułowane żądanie o _/_.

### Walidacja żądania i selektywne odpowiadanie {#validating-the-request-and-selectively-responding}

Na razie nasz serwer WWW zwraca HTML z pliku bez względu na to, czego zażądał
klient. Dodajmy sprawdzanie, czy przeglądarka żąda _/_, przed zwróceniem pliku
HTML, oraz zwracanie błędu, jeśli przeglądarka żąda czegokolwiek innego. W tym
celu musimy zmodyfikować `handle_connection`, jak pokazano w listingu 21-6. Ten
nowy kod porównuje zawartość otrzymanego żądania ze znaną nam postacią żądania
o _/_ i dodaje bloki `if` i `else`, aby różnie traktować żądania.

<Listing number="21-6" file-name="src/main.rs" caption="Obsługa żądań o */* inaczej niż pozostałych żądań">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-06/src/main.rs:here}}
```

</Listing>

Będziemy patrzeć tylko na pierwszy wiersz żądania HTTP, więc zamiast wczytywać
całe żądanie do wektora, wywołujemy `next`, aby pobrać pierwszy element z
iteratora. Pierwsze `unwrap` zajmuje się `Option` i zatrzymuje program, jeśli
iterator nie ma elementów. Drugie `unwrap` obsługuje `Result` i działa tak samo
jak `unwrap` w `map` dodanym w listingu 21-2.

Następnie sprawdzamy, czy `request_line` jest równe wierszowi żądania GET do
ścieżki _/_. Jeśli tak, blok `if` zwraca zawartość naszego pliku HTML.

Jeśli `request_line` _nie_ jest równe żądaniu GET do ścieżki _/_, oznacza to,
że otrzymaliśmy jakieś inne żądanie. Za chwilę dodamy do bloku `else` kod
odpowiadający na wszystkie pozostałe żądania.

Uruchom teraz ten kod i otwórz adres _127.0.0.1:7878_; powinien pojawić się
HTML z pliku _hello.html_. Jeśli wyślesz jakiekolwiek inne żądanie, na przykład
_127.0.0.1:7878/something-else_, otrzymasz błąd połączenia podobny do tych,
które widać było po uruchomieniu kodu z listingów 21-1 i 21-2.

Dodajmy teraz kod z listingu 21-7 do bloku `else`, aby zwracać odpowiedź z
kodem statusu 404, który sygnalizuje, że nie znaleziono treści, o którą
prosiło żądanie. Zwrócimy też trochę HTML-a ze stroną, którą przeglądarka
wyświetli, aby poinformować użytkownika końcowego o odpowiedzi.

<Listing number="21-7" file-name="src/main.rs" caption="Odpowiadanie kodem statusu 404 i stroną błędu, jeśli zażądano czegokolwiek innego niż */*">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-07/src/main.rs:here}}
```

</Listing>

Tym razem nasza odpowiedź ma wiersz statusu z kodem statusu 404 i frazą
statusu `NOT FOUND`. Treścią odpowiedzi będzie HTML z pliku _404.html_. Na
potrzeby strony błędu musisz utworzyć plik _404.html_ obok _hello.html_;
ponownie możesz użyć dowolnego HTML-a albo przykładowego HTML-a z listingu
21-8.

<Listing number="21-8" file-name="404.html" caption="Przykładowa zawartość strony odsyłanej w każdej odpowiedzi 404">

```html
{{#include ../listings/ch21-web-server/listing-21-07/404.html}}
```

</Listing>

Po tych zmianach ponownie uruchom serwer. Żądanie o _127.0.0.1:7878_ powinno
zwrócić zawartość _hello.html_, a każde inne żądanie, na przykład
_127.0.0.1:7878/foo_, powinno zwrócić HTML błędu z _404.html_.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-touch-of-refactoring"></a>

### Refaktoryzacja {#refactoring}

Na razie bloki `if` i `else` zawierają mnóstwo powtórzeń: oba odczytują pliki
i zapisują ich zawartość do strumienia. Jedyne różnice to wiersz statusu i
nazwa pliku. Uczyńmy kod zwięźlejszym, wyciągając te różnice do osobnych
wierszy `if` i `else`, które przypiszą wartości wiersza statusu i nazwy pliku
do zmiennych; potem możemy bezwarunkowo użyć tych zmiennych w kodzie, który
odczytuje plik i zapisuje odpowiedź. Listing 21-9 pokazuje kod wynikowy po
zastąpieniu dużych bloków `if` i `else`.

<Listing number="21-9" file-name="src/main.rs" caption="Refaktoryzacja bloków `if` i `else` tak, aby zawierały tylko kod różniący się w obu przypadkach">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-09/src/main.rs:here}}
```

</Listing>

Teraz bloki `if` i `else` zwracają tylko odpowiednie wartości wiersza statusu i
nazwy pliku w krotce (*tuple*); następnie za pomocą destrukturyzacji
przypisujemy te dwie wartości do `status_line` i `filename`, używając wzorca w
instrukcji (*statement*) `let`, jak omówiliśmy w rozdziale 19.

Wcześniej powielony kod znajduje się teraz poza blokami `if` i `else` i używa
zmiennych `status_line` i `filename`. Dzięki temu łatwiej dostrzec różnicę
między oboma przypadkami, a jeśli zechcemy zmienić sposób odczytywania pliku i
zapisywania odpowiedzi, wystarczy zaktualizować kod w jednym miejscu.
Zachowanie kodu z listingu 21-9 będzie takie samo jak kodu z listingu 21-7.

Wspaniale! Mamy teraz prosty serwer WWW napisany w około 40 wierszach kodu w
Ruście, który odpowiada na jedno żądanie stroną z treścią, a na wszystkie
pozostałe – odpowiedzią 404.

Obecnie nasz serwer działa w jednym wątku, co oznacza, że może obsługiwać tylko
jedno żądanie naraz. Sprawdźmy, dlaczego może to być problem, symulując kilka
powolnych żądań. Następnie poprawimy serwer tak, aby mógł obsługiwać wiele
żądań jednocześnie.

<!-- Old headings. Do not remove or links may break. -->

<a id="writing-error-messages-to-standard-error-instead-of-standard-output"></a>

## Przekierowywanie błędów na standardowe wyjście błędów {#redirecting-errors-to-standard-error}

Obecnie całe wyjście programu wypisujemy w terminalu za pomocą makra
`println!`. W większości terminali istnieją dwa rodzaje wyjścia: _standardowe
wyjście_ (`stdout`) dla ogólnych informacji i _standardowe wyjście błędów_
(`stderr`) dla komunikatów o błędach. Dzięki temu rozróżnieniu użytkownicy mogą
skierować wyniki poprawnego działania programu do pliku, a komunikaty o błędach
nadal widzieć na ekranie.

Makro `println!` potrafi wypisywać tylko na standardowe wyjście, więc do
wypisywania na standardowe wyjście błędów musimy użyć czegoś innego.

### Sprawdzanie, gdzie trafiają błędy {#checking-where-errors-are-written}

Najpierw zobaczmy, jak treść wypisywana przez `minigrep` trafia obecnie na
standardowe wyjście, łącznie z komunikatami o błędach, które chcielibyśmy
zamiast tego wypisywać na standardowe wyjście błędów. Zrobimy to,
przekierowując strumień standardowego wyjścia do pliku i celowo wywołując błąd.
Nie przekierujemy strumienia standardowego wyjścia błędów, więc wszystko, co
zostanie na nie wysłane, nadal będzie wyświetlane na ekranie.

Od programów wiersza poleceń oczekuje się, że komunikaty o błędach będą wysyłać
do strumienia standardowego wyjścia błędów, abyśmy widzieli je na ekranie nawet
wtedy, gdy przekierujemy strumień standardowego wyjścia do pliku. Nasz program
obecnie nie zachowuje się poprawnie: za chwilę zobaczymy, że zamiast tego
zapisuje komunikat o błędzie do pliku!

Aby pokazać to zachowanie, uruchomimy program z `>` i ścieżką pliku,
_output.txt_, do którego chcemy przekierować strumień standardowego wyjścia. Nie
przekażemy żadnych argumentów, co powinno spowodować błąd:

```console
$ cargo run > output.txt
```

Składnia `>` mówi powłoce, aby zapisała zawartość standardowego wyjścia do pliku
_output.txt_ zamiast na ekran. Nie zobaczyliśmy na ekranie spodziewanego
komunikatu o błędzie, więc musiał on trafić do pliku. Oto zawartość
_output.txt_:

```text
Problem parsing arguments: not enough arguments
```

Zgadza się, nasz komunikat o błędzie jest wypisywany na standardowe wyjście.
Znacznie bardziej przydatne jest wypisywanie takich komunikatów o błędach na
standardowe wyjście błędów, tak aby do pliku trafiały tylko dane z poprawnego
uruchomienia. Zmienimy to.

### Wypisywanie błędów na standardowe wyjście błędów {#printing-errors-to-standard-error}

Użyjemy kodu z listingu 12-24, aby zmienić sposób wypisywania komunikatów o
błędach. Dzięki refaktoryzacji przeprowadzonej wcześniej w tym rozdziale cały
kod wypisujący komunikaty o błędach znajduje się w jednej funkcji, `main`.
Biblioteka standardowa udostępnia makro `eprintln!`, które wypisuje do strumienia
standardowego wyjścia błędów, więc zmieńmy oba miejsca, w których do wypisywania
błędów wywoływaliśmy `println!`, tak aby używały `eprintln!`.

<Listing number="12-24" file-name="src/main.rs" caption="Wypisywanie komunikatów o błędach na standardowe wyjście błędów zamiast na standardowe wyjście za pomocą `eprintln!`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-24/src/main.rs:here}}
```

</Listing>

Uruchommy teraz program ponownie w ten sam sposób, bez żadnych argumentów i z
przekierowaniem standardowego wyjścia za pomocą `>`:

```console
$ cargo run > output.txt
Problem parsing arguments: not enough arguments
```

Teraz widzimy błąd na ekranie, a _output.txt_ jest pusty, czyli program
zachowuje się tak, jak oczekujemy od programów wiersza poleceń.

Uruchommy program jeszcze raz z argumentami, które nie powodują błędu, ale nadal
przekierowując standardowe wyjście do pliku:

```console
$ cargo run -- to poem.txt > output.txt
```

W terminalu nie zobaczymy żadnego wyjścia, a _output.txt_ będzie zawierał nasze
wyniki:

<span class="filename">Plik: output.txt</span>

```text
Are you nobody, too?
How dreary to be somebody!
```

To pokazuje, że teraz zgodnie z oczekiwaniami używamy standardowego wyjścia dla
wyników poprawnego działania, a standardowego wyjścia błędów dla komunikatów o
błędach.

## Podsumowanie {#summary}

W tym rozdziale przypomnieliśmy niektóre z najważniejszych pojęć, które już
znasz, i pokazaliśmy, jak wykonywać typowe operacje wejścia-wyjścia w Ruście. Korzystając z argumentów wiersza poleceń, plików,
zmiennych środowiskowych i makra `eprintln!` do wypisywania błędów, możesz
teraz pisać aplikacje wiersza poleceń. W połączeniu z pojęciami z poprzednich
rozdziałów twój kod będzie dobrze zorganizowany, będzie efektywnie przechowywał
dane w odpowiednich strukturach danych, sprawnie obsługiwał błędy i będzie
dobrze przetestowany.

Następnie przyjrzymy się mechanizmom Rusta, na które wpłynęły języki
funkcyjne: domknięciom (*closures*) i iteratorom.

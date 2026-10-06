## Łagodne zamykanie i sprzątanie {#graceful-shutdown-and-cleanup}

Kod z listingu 21-20 odpowiada na żądania asynchronicznie dzięki puli wątków,
tak jak zamierzaliśmy. Dostajemy kilka ostrzeżeń o polach `workers`, `id` i
`thread`, których nie używamy bezpośrednio, co przypomina nam, że niczego nie
sprzątamy. Gdy zatrzymujemy wątek główny mało eleganckim sposobem
<kbd>ctrl</kbd>-<kbd>C</kbd>, wszystkie pozostałe wątki również zostają
natychmiast zatrzymane, nawet jeśli są w trakcie obsługi żądania.

Następnie zaimplementujemy więc *trait* (cechę typu, zbliżoną do interfejsu)
`Drop`, aby wywołać `join` na każdym wątku w puli, tak by wątki mogły dokończyć
obsługiwane żądania przed zamknięciem. Potem zaimplementujemy sposób, by
przekazać wątkom, że mają przestać przyjmować nowe żądania i się zakończyć. Aby
zobaczyć ten kod w działaniu, zmodyfikujemy serwer tak, żeby przyjął tylko dwa
żądania, a potem przeprowadził łagodne zamykanie (*graceful shutdown*) swojej
puli wątków.

Warto zauważyć jedno: nic z tego nie wpływa na części kodu odpowiedzialne za
wykonywanie domknięć (*closures*), więc wszystko tutaj wyglądałoby tak samo,
gdybyśmy używali puli wątków w środowisku uruchomieniowym (*runtime*) dla kodu
asynchronicznego.

### Implementacja traitu `Drop` dla `ThreadPool` {#implementing-the-drop-trait-on-threadpool}

Zacznijmy od zaimplementowania `Drop` dla naszej puli wątków. Gdy pula zostaje
zwolniona (*drop*), wszystkie wątki powinny zostać dołączone, aby mieć
pewność, że dokończą swoją pracę. Listing 21-22 pokazuje pierwszą próbę
implementacji `Drop`; ten kod jeszcze nie do końca działa.

<Listing number="21-22" file-name="src/lib.rs" caption="Dołączanie każdego wątku, gdy pula wątków wychodzi poza zasięg">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-22/src/lib.rs:here}}
```

</Listing>

Najpierw przechodzimy w pętli po wszystkich elementach `workers` puli wątków.
Używamy do tego `&mut`, ponieważ `self` jest referencją mutowalną (*mutable*), a
musimy też móc modyfikować `worker`. Dla każdego `worker` wypisujemy komunikat, że
ta konkretna instancja `Worker` się zamyka, a następnie wywołujemy `join` na
wątku tej instancji `Worker`. Jeśli wywołanie `join` się nie powiedzie, używamy
`unwrap`, aby Rust wpadł w panikę (*panic*) i przeszedł do zamknięcia, które
łagodne już nie jest.

Oto błąd, który dostajemy przy kompilacji tego kodu:

```console
{{#include ../listings/ch21-web-server/listing-21-22/output.txt}}
```

Błąd mówi nam, że nie możemy wywołać `join`, ponieważ mamy tylko mutowalne
pożyczenie (*borrow*) każdego `worker`, a `join` przejmuje własność
(*ownership*) swojego argumentu. Aby rozwiązać ten problem, musimy przenieść
(*move*) wątek z instancji
`Worker`, która jest właścicielem `thread`, tak by `join` mogło skonsumować
wątek. Jednym ze sposobów jest podejście, które zastosowaliśmy w listingu 18-15.
Gdyby `Worker` przechowywał `Option<thread::JoinHandle<()>>`, moglibyśmy wywołać
metodę `take` na `Option`, aby przenieść wartość z wariantu `Some` i zostawić na
jej miejscu wariant `None`. Innymi słowy, działający `Worker` miałby w `thread`
wariant `Some`, a gdybyśmy chcieli posprzątać po `Worker`, zastąpilibyśmy `Some`
przez `None`, tak by `Worker` nie miał wątku do uruchomienia.

Jednak sytuacja ta pojawiałaby się _wyłącznie_ przy zwalnianiu `Worker`. W
zamian musielibyśmy mieć do czynienia z `Option<thread::JoinHandle<()>>` wszędzie
tam, gdzie odwołujemy się do `worker.thread`. Idiomatyczny Rust dość często
korzysta z `Option`, ale gdy zauważysz, że w ramach takiego obejścia opakowujesz
w `Option` coś, o czym wiesz, że zawsze będzie obecne, warto poszukać innych
podejść, dzięki którym kod będzie czytelniejszy i mniej podatny na błędy.

W tym przypadku istnieje lepsza alternatywa: metoda `Vec::drain`. Przyjmuje ona
parametr będący zakresem, który określa, jakie elementy usunąć z wektora
(*vector*), i zwraca iterator po tych elementach. Przekazanie składni zakresu
`..` usunie z wektora *każdą* wartość.

Musimy więc zaktualizować implementację `drop` dla `ThreadPool` w ten sposób:

<Listing file-name="src/lib.rs">

```rust
{{#rustdoc_include ../listings/ch21-web-server/no-listing-04-update-drop-definition/src/lib.rs:here}}
```

</Listing>

To rozwiązuje błąd kompilatora i nie wymaga żadnych innych zmian w naszym
kodzie. Zauważ, że ponieważ drop może zostać wywołany podczas paniki, unwrap
również może spanikować i wywołać podwójną panikę, która natychmiast kończy
awaryjnie program i przerywa wszelkie trwające sprzątanie. W przykładowym programie to nie
problem, ale w kodzie produkcyjnym nie jest to zalecane.

### Sygnalizowanie wątkom, by przestały nasłuchiwać zadań {#signaling-to-the-threads-to-stop-listening-for-jobs}

Po wszystkich wprowadzonych zmianach nasz kod kompiluje się bez żadnych
ostrzeżeń. Zła wiadomość jest jednak taka, że ten kod wciąż nie działa tak, jak
byśmy chcieli. Kluczowa jest logika domknięć uruchamianych przez wątki instancji
`Worker`: w tej chwili wywołujemy `join`, ale to nie zamknie wątków, ponieważ w
nieskończonej pętli `loop` szukają one zadań. Jeśli spróbujemy zwolnić naszą
`ThreadPool` przy obecnej implementacji `drop`, wątek główny zablokuje się na
zawsze, czekając na zakończenie pierwszego wątku.

Aby naprawić ten problem, musimy zmienić implementację `drop` dla `ThreadPool`, a
następnie pętlę w `Worker`.

Najpierw zmienimy implementację `drop` dla `ThreadPool` tak, by jawnie zwalniała
`sender` przed oczekiwaniem na zakończenie wątków. Listing 21-23 pokazuje zmiany
w `ThreadPool`, które jawnie zwalniają `sender`. W odróżnieniu od wątku tutaj
_rzeczywiście_ musimy użyć `Option`, aby móc przenieść `sender` z `ThreadPool` za
pomocą `Option::take`.

<Listing number="21-23" file-name="src/lib.rs" caption="Jawne zwolnienie `sender` przed dołączeniem wątków `Worker`">

```rust,noplayground,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-23/src/lib.rs:here}}
```

</Listing>

Zwolnienie `sender` zamyka kanał, co oznacza, że żadne kolejne komunikaty nie
zostaną już wysłane. Gdy to nastąpi, wszystkie wywołania `recv`, które instancje
`Worker` wykonują w nieskończonej pętli, zwrócą błąd. W listingu 21-24 zmieniamy
pętlę w `Worker` tak, by w takim przypadku łagodnie z niej wychodziła, co oznacza,
że wątki zakończą się, gdy implementacja `drop` dla `ThreadPool` wywoła na nich
`join`.

<Listing number="21-24" file-name="src/lib.rs" caption="Jawne wyjście z pętli, gdy `recv` zwraca błąd">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-24/src/lib.rs:here}}
```

</Listing>

Aby zobaczyć ten kod w działaniu, zmodyfikujmy funkcję `main` tak, by
przyjmowała tylko dwa żądania, a potem łagodnie zamykała serwer, jak pokazano w listingu 21-25.

<Listing number="21-25" file-name="src/main.rs" caption="Zamknięcie serwera po obsłużeniu dwóch żądań przez wyjście z pętli">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/listing-21-25/src/main.rs:here}}
```

</Listing>

Prawdziwy serwer WWW raczej nie powinien się zamykać po obsłużeniu zaledwie dwóch
żądań. Ten kod jedynie pokazuje, że łagodne zamykanie i sprzątanie działają
poprawnie.

Metoda `take` jest zdefiniowana w traicie `Iterator` i ogranicza iterację do
co najwyżej dwóch pierwszych elementów. `ThreadPool` wyjdzie poza zasięg
(*scope*) na końcu `main` i zostanie uruchomiona implementacja `drop`.

Uruchom serwer poleceniem `cargo run` i wyślij trzy żądania. Trzecie żądanie
powinno zakończyć się błędem, a w terminalu powinno pojawić się wyjście podobne
do tego:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-25
cargo run
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
curl http://127.0.0.1:7878
third request will error because server will have shut down
copy output below
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.41s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Shutting down.
Shutting down worker 0
Worker 3 got a job; executing.
Worker 1 disconnected; shutting down.
Worker 2 disconnected; shutting down.
Worker 3 disconnected; shutting down.
Worker 0 disconnected; shutting down.
Shutting down worker 1
Shutting down worker 2
Shutting down worker 3
```

Identyfikatory `Worker` i komunikaty mogą u ciebie zostać wypisane w innej
kolejności. Z komunikatów widać, jak działa ten kod: instancje `Worker` 0 i 3
dostały dwa pierwsze żądania. Po drugim połączeniu serwer przestał przyjmować
kolejne, a implementacja `Drop` dla `ThreadPool` zaczyna się wykonywać, zanim
`Worker 3` w ogóle rozpocznie swoje zadanie. Zwolnienie `sender` odłącza wszystkie
instancje `Worker` i każe im się zakończyć. Każda instancja `Worker` wypisuje
komunikat w chwili odłączenia, a następnie pula wątków wywołuje `join`, aby
poczekać na zakończenie wątku każdego `Worker`.

Zwróć uwagę na jeden ciekawy aspekt tego konkretnego wykonania: `ThreadPool`
zwolniła `sender` i zanim którykolwiek `Worker` otrzymał błąd, spróbowaliśmy
dołączyć `Worker 0`. `Worker 0` nie otrzymał jeszcze błędu z `recv`, więc wątek
główny się zablokował, czekając na zakończenie `Worker 0`. W międzyczasie
`Worker 3` otrzymał zadanie, a potem wszystkie wątki otrzymały błąd. Gdy
`Worker 0` się zakończył, wątek główny poczekał na zakończenie pozostałych
instancji `Worker`. W tym momencie wszystkie one wyszły już ze swoich pętli i się
zatrzymały.

Gratulacje! Ukończyliśmy nasz projekt: mamy prosty serwer WWW, który używa puli
wątków, by odpowiadać asynchronicznie. Potrafimy łagodnie zamknąć serwer,
sprzątając przy tym wszystkie wątki w puli.

Oto pełny kod do wglądu:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/main.rs}}
```

</Listing>

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-07-final-code/src/lib.rs}}
```

</Listing>

Moglibyśmy zrobić tu więcej! Jeśli chcesz dalej rozwijać ten projekt, oto kilka
pomysłów:

- Dodaj więcej dokumentacji do `ThreadPool` i jej publicznych metod.
- Dodaj testy funkcjonalności biblioteki.
- Zamień wywołania `unwrap` na solidniejszą obsługę błędów.
- Użyj `ThreadPool` do wykonania jakiegoś innego zadania niż obsługa żądań
  sieciowych.
- Znajdź *crate* (jednostkę kompilacji w Ruście) z pulą wątków na
  [crates.io](https://crates.io/) i zaimplementuj z jego pomocą podobny serwer
  WWW. Następnie porównaj jego API i solidność z zaimplementowaną przez nas pulą
  wątków.

## Podsumowanie {#summary}

Dobra robota! Udało ci się dotrzeć do końca książki! Chcemy ci podziękować za
wspólną podróż po Ruście. Możesz już implementować własne
projekty w Ruście i pomagać przy projektach innych osób. Pamiętaj, że istnieje
przyjazna społeczność innych rustowców (*Rustaceans*), którzy chętnie pomogą ci
uporać się z każdym wyzwaniem, jakie napotkasz w swojej przygodzie z Rustem.

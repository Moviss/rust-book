<!-- Old headings. Do not remove or links may break. -->

<a id="using-message-passing-to-transfer-data-between-threads"></a>

## Przesyłanie danych między wątkami za pomocą przekazywania komunikatów {#transfer-data-between-threads-with-message-passing}

Coraz popularniejszym sposobem zapewnienia bezpiecznej współbieżności
(*concurrency*) jest przekazywanie komunikatów (*message passing*): wątki lub
aktorzy komunikują się, wysyłając sobie nawzajem komunikaty zawierające dane.
Oto ta idea ujęta w hasło z [dokumentacji języka Go](https://golang.org/doc/effective_go.html#concurrency):
„Nie komunikuj się przez współdzielenie pamięci; zamiast tego współdziel pamięć
przez komunikację”.

Aby umożliwić współbieżność opartą na wysyłaniu komunikatów, biblioteka
standardowa Rusta dostarcza implementację kanałów. *Kanał* to ogólne pojęcie
programistyczne oznaczające mechanizm, za pomocą którego dane są przesyłane z
jednego wątku do drugiego.

Kanał w programowaniu możesz sobie wyobrazić jako kanał wodny o określonym
kierunku przepływu, na przykład strumień albo rzekę. Jeśli wrzucisz do rzeki
coś takiego jak gumową kaczuszkę, popłynie ona z prądem aż do końca drogi
wodnej.

Kanał ma dwie połówki: nadajnik i odbiornik. Nadajnik to miejsce w górze rzeki,
w którym wrzucasz gumową kaczuszkę do wody, a odbiornik to miejsce w dole
rzeki, do którego kaczuszka w końcu dopływa. Jedna część twojego kodu wywołuje
metody nadajnika z danymi, które chcesz wysłać, a inna sprawdza, czy po stronie
odbiorczej pojawiły się komunikaty. Mówimy, że kanał jest *zamknięty*, jeśli
nadajnik albo odbiornik zostanie zwolniony (*drop*).

Stopniowo napiszemy program, w którym jeden wątek generuje wartości i wysyła je
kanałem, a drugi wątek je odbiera i wypisuje. Aby zilustrować ten mechanizm,
będziemy przesyłać między wątkami proste wartości. Gdy już poznasz tę technikę,
możesz używać kanałów dla dowolnych wątków, które muszą się ze sobą
komunikować, na przykład w systemie czatu albo w systemie, w którym wiele
wątków wykonuje części obliczeń i wysyła wyniki częściowe do jednego wątku,
który je agreguje.

Najpierw w listingu 16-6 utworzymy kanał, ale nic z nim nie zrobimy. Zauważ,
że ten kod jeszcze się nie skompiluje, bo Rust nie wie, jakiego typu wartości
chcemy wysyłać kanałem.

<Listing number="16-6" file-name="src/main.rs" caption="Tworzenie kanału i przypisanie jego dwóch połówek do `tx` i `rx`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-06/src/main.rs}}
```

</Listing>

Nowy kanał tworzymy za pomocą funkcji `mpsc::channel`; `mpsc` to skrót od
*multiple producer, single consumer* (wielu producentów, jeden konsument).
Krótko mówiąc, sposób, w jaki biblioteka standardowa Rusta implementuje kanały,
sprawia, że kanał może mieć wiele końców *wysyłających*, które produkują
wartości, ale tylko jeden koniec *odbierający*, który te wartości konsumuje.
Wyobraź sobie wiele strumieni wpływających do jednej dużej rzeki: wszystko, co
zostanie wysłane którymkolwiek ze strumieni, trafi na końcu do jednej rzeki. Na
razie zaczniemy od jednego producenta, ale gdy ten przykład zacznie działać,
dodamy kolejnych.

Funkcja `mpsc::channel` zwraca krotkę (*tuple*), której pierwszy element to
koniec wysyłający – nadajnik – a drugi to koniec odbierający – odbiornik. Skróty
`tx` i `rx` są tradycyjnie używane w wielu dziedzinach odpowiednio dla
*transmitter* (nadajnik) i *receiver* (odbiornik), więc tak nazywamy nasze
zmienne, aby wskazać każdy z końców. Używamy instrukcji (*statement*) `let` ze
wzorcem, który destrukturyzuje krotkę; użycie wzorców w instrukcjach `let` i
destrukturyzację omówimy w rozdziale 19. Na razie wystarczy wiedzieć, że takie
użycie instrukcji `let` to wygodny sposób na wyciągnięcie poszczególnych części
krotki zwracanej przez `mpsc::channel`.

Przenieśmy koniec wysyłający do nowego wątku i każmy mu wysłać jeden łańcuch
znaków (*string*), tak aby nowy wątek komunikował się z wątkiem głównym, jak pokazano w listingu 16-7. Przypomina to wrzucenie gumowej
kaczuszki do rzeki w jej górnym biegu albo wysłanie wiadomości na czacie z
jednego wątku do drugiego.

<Listing number="16-7" file-name="src/main.rs" caption='Przeniesienie `tx` do nowego wątku i wysłanie `"hi"`'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-07/src/main.rs}}
```

</Listing>

Ponownie używamy `thread::spawn`, aby utworzyć nowy wątek, a następnie `move`,
aby przenieść (*move*) `tx` do domknięcia (*closure*), dzięki czemu nowy
wątek staje się właścicielem `tx`. Nowy wątek musi być właścicielem
nadajnika, aby móc wysyłać komunikaty przez kanał.

Nadajnik ma metodę `send`, która przyjmuje wartość, którą chcemy wysłać. Metoda
`send` zwraca typ `Result<T, E>`, więc jeśli odbiornik został już zwolniony i
nie ma dokąd wysłać wartości, operacja wysyłania zwróci błąd. W tym przykładzie
wywołujemy `unwrap`, aby w razie błędu wywołać panikę (*panic*). W prawdziwej
aplikacji obsłużylibyśmy go jednak porządnie: wróć do rozdziału 9, aby
przypomnieć sobie strategie właściwej obsługi błędów.

W listingu 16-8 odbierzemy wartość z odbiornika w wątku głównym. Przypomina to
wyłowienie gumowej kaczuszki z wody u ujścia rzeki albo odebranie wiadomości na
czacie.

<Listing number="16-8" file-name="src/main.rs" caption='Odebranie wartości `"hi"` w wątku głównym i wypisanie jej'>

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-08/src/main.rs}}
```

</Listing>

Odbiornik ma dwie przydatne metody: `recv` i `try_recv`. Używamy `recv` (skrót
od *receive*, czyli „odbierz”), która zablokuje wykonywanie wątku głównego i
będzie czekać, aż kanałem zostanie wysłana jakaś wartość. Gdy wartość zostanie
wysłana, `recv` zwróci ją opakowaną w `Result<T, E>`. Gdy nadajnik zostanie
zamknięty, `recv` zwróci błąd, sygnalizując, że więcej wartości już nie
nadejdzie.

Metoda `try_recv` nie blokuje, lecz od razu zwraca `Result<T, E>`: wartość
`Ok` zawierającą komunikat, jeśli jakiś jest dostępny, albo wartość `Err`,
jeśli w tej chwili nie ma żadnych komunikatów. Użycie `try_recv` przydaje się,
gdy ten wątek ma inną pracę do wykonania podczas oczekiwania na komunikaty:
moglibyśmy napisać pętlę, która co jakiś czas wywołuje `try_recv`, obsługuje
komunikat, jeśli jest dostępny, a w przeciwnym razie przez chwilę zajmuje się
czymś innym, zanim sprawdzi ponownie.

W tym przykładzie dla prostoty użyliśmy `recv`; wątek główny nie ma nic innego
do roboty poza czekaniem na komunikaty, więc zablokowanie go jest właściwe.

Po uruchomieniu kodu z listingu 16-8 zobaczymy wartość wypisaną przez wątek
główny:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
```

Doskonale!

<!-- Old headings. Do not remove or links may break. -->

<a id="channels-and-ownership-transference"></a>

### Przekazywanie własności przez kanały {#transferring-ownership-through-channels}

Reguły własności (*ownership*) odgrywają kluczową rolę w wysyłaniu komunikatów,
ponieważ pomagają pisać bezpieczny kod współbieżny. Zapobieganie błędom w
programowaniu współbieżnym to właśnie korzyść z myślenia o własności w całym
programie w Ruście. Przeprowadźmy eksperyment, który pokaże, jak kanały i
własność współpracują, aby zapobiegać problemom: spróbujemy użyć wartości `val`
w nowym wątku *po* wysłaniu jej kanałem. Spróbuj skompilować kod z listingu
16-9, aby zobaczyć, dlaczego ten kod jest niedozwolony.

<Listing number="16-9" file-name="src/main.rs" caption="Próba użycia `val` po wysłaniu jej kanałem">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-09/src/main.rs}}
```

</Listing>

Tutaj próbujemy wypisać `val` po wysłaniu jej kanałem za pomocą `tx.send`.
Dopuszczenie tego byłoby złym pomysłem: gdy wartość zostanie wysłana do innego
wątku, ten wątek mógłby ją zmodyfikować albo zwolnić, zanim spróbujemy jej
ponownie użyć. Modyfikacje dokonane przez inny wątek mogłyby potencjalnie
prowadzić do błędów lub nieoczekiwanych wyników z powodu niespójnych albo
nieistniejących danych. Rust zgłasza nam jednak błąd, gdy próbujemy skompilować
kod z listingu 16-9:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-09/output.txt}}
```

Nasza pomyłka związana ze współbieżnością spowodowała błąd w czasie kompilacji
(*compile-time*). Funkcja `send` przejmuje własność swojego parametru, a gdy
wartość zostaje przeniesiona, jej właścicielem staje się odbiornik. To
chroni nas przed przypadkowym ponownym użyciem wartości po jej wysłaniu; system
własności sprawdza, czy wszystko jest w porządku.

<!-- Old headings. Do not remove or links may break. -->

<a id="sending-multiple-values-and-seeing-the-receiver-waiting"></a>

### Wysyłanie wielu wartości {#sending-multiple-values}

Kod z listingu 16-8 skompilował się i zadziałał, ale nie pokazał wyraźnie, że
dwa odrębne wątki rozmawiają ze sobą przez kanał.

W listingu 16-10 wprowadziliśmy kilka zmian, które udowodnią, że kod z listingu
16-8 działa współbieżnie: nowy wątek będzie teraz wysyłał wiele komunikatów i
robił sekundową przerwę między kolejnymi komunikatami.

<Listing number="16-10" file-name="src/main.rs" caption="Wysyłanie wielu komunikatów z przerwami między nimi">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-10/src/main.rs}}
```

</Listing>

Tym razem nowy wątek ma wektor (*vector*) łańcuchów, które chcemy wysłać do
wątku głównego. Iterujemy po nich, wysyłając każdy osobno, i między kolejnymi
wysłaniami robimy przerwę, wywołując funkcję `thread::sleep` z wartością
`Duration` równą jednej sekundzie.

W wątku głównym nie wywołujemy już jawnie funkcji `recv`: zamiast tego
traktujemy `rx` jak iterator. Każdą odebraną wartość wypisujemy. Gdy kanał
zostanie zamknięty, iteracja się zakończy.

Po uruchomieniu kodu z listingu 16-10 powinno się pojawić następujące wyjście,
z sekundową przerwą między kolejnymi liniami:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: from
Got: the
Got: thread
```

Ponieważ w pętli `for` w wątku głównym nie ma żadnego kodu, który robiłby
przerwy albo opóźnienia, widać, że to wątek główny czeka na odebranie wartości
od nowego wątku.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-multiple-producers-by-cloning-the-transmitter"></a>

### Tworzenie wielu producentów {#creating-multiple-producers}

Wspomnieliśmy wcześniej, że `mpsc` to akronim od *multiple producer, single
consumer*. Wykorzystajmy `mpsc` i rozszerzmy kod z listingu 16-10 tak, aby
utworzyć wiele wątków, które wysyłają wartości do tego samego odbiornika.
Możemy to zrobić, klonując nadajnik, jak pokazano w listingu 16-11.

<Listing number="16-11" file-name="src/main.rs" caption="Wysyłanie wielu komunikatów od wielu producentów">

```rust,noplayground
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-11/src/main.rs:here}}
```

</Listing>

Tym razem, zanim utworzymy pierwszy nowy wątek, wywołujemy `clone` na
nadajniku. Otrzymujemy w ten sposób nowy nadajnik, który możemy przekazać do
pierwszego nowego wątku. Oryginalny nadajnik przekazujemy do drugiego nowego
wątku. Mamy więc dwa wątki, z których każdy wysyła inne komunikaty do
jednego odbiornika.

Po uruchomieniu kodu wyjście powinno wyglądać mniej więcej tak:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Got: hi
Got: more
Got: from
Got: messages
Got: for
Got: the
Got: thread
Got: you
```

W zależności od systemu wartości mogą pojawić się w innej kolejności. To
właśnie sprawia, że współbieżność jest zarówno interesująca, jak i trudna. Jeśli
poeksperymentujesz z `thread::sleep`, podając różne wartości w różnych wątkach,
każde uruchomienie będzie jeszcze bardziej niedeterministyczne i za każdym
razem da inne wyjście.

Skoro już wiemy, jak działają kanały, przyjrzyjmy się innej metodzie
współbieżności.

{{#quiz ../quizzes/ch16-02-message-passing.toml}}
## Używanie wątków do jednoczesnego uruchamiania kodu {#using-threads-to-run-code-simultaneously}

W większości współczesnych systemów operacyjnych kod uruchomionego programu
działa w _procesie_ (*process*), a system operacyjny zarządza wieloma procesami
naraz. W obrębie programu również możesz mieć niezależne części, które działają
jednocześnie. Mechanizmy uruchamiające te niezależne części nazywamy _wątkami_
(*threads*). Na przykład serwer WWW mógłby mieć wiele wątków, aby móc
odpowiadać na więcej niż jedno żądanie w tym samym czasie.

Podzielenie obliczeń w programie na wiele wątków, aby wykonywać wiele zadań
jednocześnie, może poprawić wydajność, ale zwiększa też złożoność. Ponieważ
wątki mogą działać jednocześnie, nie ma żadnej wbudowanej gwarancji co do
kolejności, w jakiej wykonają się części kodu w różnych wątkach. Może to
prowadzić do problemów takich jak:

- sytuacja wyścigu (*race condition*), w której wątki uzyskują dostęp do danych
  lub zasobów w niespójnej kolejności;
- zakleszczenie (*deadlock*), w którym dwa wątki czekają na siebie nawzajem, co
  uniemożliwia obu dalsze działanie;
- błędy, które pojawiają się tylko w określonych sytuacjach i trudno je
  niezawodnie odtworzyć i naprawić.

Rust stara się ograniczać negatywne skutki używania wątków, ale programowanie w
kontekście wielowątkowym nadal wymaga starannego przemyślenia i struktury kodu
innej niż w programach działających w jednym wątku.

Języki programowania implementują wątki na kilka różnych sposobów, a wiele
systemów operacyjnych udostępnia API, które język programowania może wywołać,
aby tworzyć nowe wątki. Biblioteka standardowa Rusta używa modelu implementacji
wątków _1:1_, w którym program używa jednego wątku systemu operacyjnego na
każdy wątek języka. Istnieją *crate’y* (jednostki kompilacji w Ruście)
implementujące inne modele wątków, które przyjmują inne kompromisy niż model
1:1. Jeszcze inne podejście do współbieżności (*concurrency*) zapewnia system
async Rusta, który poznamy w następnym rozdziale.

### Tworzenie nowego wątku za pomocą `spawn` {#creating-a-new-thread-with-spawn}

Aby utworzyć nowy wątek, wywołujemy funkcję `thread::spawn` i przekazujemy jej
domknięcie (*closure*) zawierające kod, który chcemy uruchomić w nowym wątku
(domknięcia omawialiśmy w rozdziale 13). Przykład w listingu 16-1 wypisuje pewien
tekst z wątku głównego, a inny tekst z nowego wątku.

<Listing number="16-1" file-name="src/main.rs" caption="Tworzenie nowego wątku, który wypisuje jedno, podczas gdy wątek główny wypisuje coś innego">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-01/src/main.rs}}
```

</Listing>

Zwróć uwagę, że gdy wątek główny programu w Ruście się kończy, wszystkie
utworzone przez niego wątki zostają zamknięte, niezależnie od tego, czy
skończyły działać. Wyjście tego programu może się za każdym razem nieco różnić,
ale będzie wyglądać podobnie do tego:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 1 from the spawned thread!
hi number 2 from the main thread!
hi number 2 from the spawned thread!
hi number 3 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the main thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
```

Wywołania `thread::sleep` zmuszają wątek do wstrzymania wykonywania na krótki
czas, co pozwala działać innemu wątkowi. Wątki prawdopodobnie będą działać
na zmianę, ale nie jest to gwarantowane: zależy to od tego, jak system
operacyjny szereguje wątki. W tym uruchomieniu wątek główny wypisał tekst jako
pierwszy, mimo że w kodzie instrukcja wypisująca z nowego wątku występuje
wcześniej. I choć kazaliśmy nowemu wątkowi wypisywać, dopóki `i` nie osiągnie
`9`, doszedł on tylko do `5`, zanim wątek główny się zakończył.

Jeśli po uruchomieniu tego kodu widzisz tylko wyjście z wątku głównego albo nie
widzisz żadnego przeplatania się, spróbuj zwiększyć liczby w zakresach, aby
system operacyjny miał więcej okazji do przełączania się między wątkami.

<!-- Old headings. Do not remove or links may break. -->

<a id="waiting-for-all-threads-to-finish-using-join-handles"></a>

### Czekanie na zakończenie wszystkich wątków {#waiting-for-all-threads-to-finish}

Kod z listingu 16-1 nie tylko zwykle przedwcześnie zatrzymuje nowy wątek z
powodu zakończenia wątku głównego, ale – ponieważ nie ma gwarancji co do
kolejności wykonywania wątków – nie możemy nawet zagwarantować, że nowy wątek w
ogóle zdąży się uruchomić!

Problem nowego wątku, który się nie uruchamia albo kończy przedwcześnie, możemy
rozwiązać, zapisując wartość zwracaną przez `thread::spawn` w zmiennej. Typem
zwracanym przez `thread::spawn` jest `JoinHandle<T>`. `JoinHandle<T>` to
wartość, której jesteśmy właścicielem, a wywołanie na niej metody `join`
sprawia, że czekamy na zakończenie jej wątku. Listing 16-2 pokazuje, jak użyć
`JoinHandle<T>` wątku utworzonego w listingu 16-1 i jak wywołać `join`, aby
upewnić się, że nowy wątek zakończy się przed wyjściem z `main`.

<Listing number="16-2" file-name="src/main.rs" caption="Zapisanie `JoinHandle<T>` zwróconego przez `thread::spawn`, aby zagwarantować, że wątek wykona się do końca">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-02/src/main.rs}}
```

</Listing>

Wywołanie `join` na uchwycie blokuje aktualnie działający wątek, dopóki wątek
reprezentowany przez ten uchwyt się nie zakończy. _Zablokowanie_ (*blocking*)
wątku oznacza, że nie może on wykonywać pracy ani się zakończyć. Ponieważ
umieściliśmy wywołanie `join` za pętlą `for` wątku głównego, uruchomienie
listingu 16-2 powinno dać wyjście podobne do tego:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 1 from the spawned thread!
hi number 3 from the main thread!
hi number 2 from the spawned thread!
hi number 4 from the main thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
```

Oba wątki nadal działają na zmianę, ale wątek główny czeka z powodu wywołania
`handle.join()` i nie kończy się, dopóki nowy wątek nie skończy działania.

Zobaczmy jednak, co się stanie, gdy zamiast tego przeniesiemy `handle.join()`
przed pętlę `for` w `main`, w ten sposób:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/no-listing-01-join-too-early/src/main.rs}}
```

</Listing>

Wątek główny poczeka, aż nowy wątek się zakończy, a dopiero potem wykona swoją
pętlę `for`, więc wyjście nie będzie już przeplatane, jak widać tutaj:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the spawned thread!
hi number 2 from the spawned thread!
hi number 3 from the spawned thread!
hi number 4 from the spawned thread!
hi number 5 from the spawned thread!
hi number 6 from the spawned thread!
hi number 7 from the spawned thread!
hi number 8 from the spawned thread!
hi number 9 from the spawned thread!
hi number 1 from the main thread!
hi number 2 from the main thread!
hi number 3 from the main thread!
hi number 4 from the main thread!
```

Drobne szczegóły, takie jak miejsce wywołania `join`, mogą wpływać na to, czy
twoje wątki działają jednocześnie.

### Używanie domknięć `move` z wątkami {#using-move-closures-with-threads}

Słowa kluczowego (*keyword*) `move` będziemy często używać z domknięciami
przekazywanymi do `thread::spawn`, ponieważ domknięcie przejmuje wtedy własność
(*ownership*) wartości, których używa ze środowiska, przekazując tym samym
własność tych wartości z jednego wątku do drugiego. W podrozdziale
[„Przechwytywanie referencji lub przenoszenie własności”][capture]<!-- ignore
--> w rozdziale 13 omawialiśmy `move` w kontekście domknięć. Teraz skupimy się
bardziej na współdziałaniu `move` z `thread::spawn`.

Zwróć uwagę, że w listingu 16-1 domknięcie przekazywane do `thread::spawn` nie
przyjmuje żadnych argumentów: w kodzie nowego wątku nie używamy żadnych danych
z wątku głównego. Aby użyć w nowym wątku danych z wątku głównego, domknięcie
nowego wątku musi przechwycić potrzebne mu wartości. Listing 16-3 pokazuje
próbę utworzenia wektora (*vector*) w wątku głównym i użycia go w nowym wątku.
Jak jednak zaraz zobaczysz, to jeszcze nie zadziała.

<Listing number="16-3" file-name="src/main.rs" caption="Próba użycia w innym wątku wektora utworzonego przez wątek główny">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-03/src/main.rs}}
```

</Listing>

Domknięcie używa `v`, więc przechwyci `v` i uczyni je częścią swojego
środowiska. Ponieważ `thread::spawn` uruchamia to domknięcie w nowym wątku,
powinniśmy mieć dostęp do `v` wewnątrz tego nowego wątku. Jednak podczas
kompilacji tego przykładu otrzymujemy następujący błąd:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-03/output.txt}}
```

Rust _wnioskuje_, jak przechwycić `v`, a ponieważ `println!` potrzebuje tylko
referencji (*reference*) do `v`, domknięcie próbuje pożyczyć (*borrow*) `v`.
Jest jednak pewien problem: Rust nie jest w stanie określić, jak długo nowy
wątek będzie działał, więc nie wie, czy referencja do `v` zawsze będzie
poprawna.

Listing 16-4 przedstawia scenariusz, w którym referencja do `v` z większym
prawdopodobieństwem okaże się niepoprawna.

<Listing number="16-4" file-name="src/main.rs" caption="Wątek z domknięciem, które próbuje przechwycić referencję do `v` z wątku głównego, który zwalnia `v`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-04/src/main.rs}}
```

</Listing>

Gdyby Rust pozwolił nam uruchomić ten kod, istniałaby możliwość, że nowy wątek
zostałby od razu odsunięty w tło, w ogóle się nie uruchamiając. Nowy wątek ma
w sobie referencję do `v`, ale wątek główny natychmiast doprowadza do zwolnienia
(*drop*) `v` za pomocą funkcji `drop`, którą omawialiśmy w rozdziale 15. Gdy
nowy wątek zacznie się wykonywać, `v` nie jest już poprawne, więc referencja do
niego również jest niepoprawna. O nie!

Aby naprawić błąd kompilatora z listingu 16-3, możemy skorzystać z rady z
komunikatu o błędzie:

<!-- manual-regeneration
after automatic regeneration, look at listings/ch16-fearless-concurrency/listing-16-03/output.txt and copy the relevant part
-->

```text
help: to force the closure to take ownership of `v` (and any other referenced variables), use the `move` keyword
  |
6 |     let handle = thread::spawn(move || {
  |                                ++++
```

Dodając słowo kluczowe `move` przed domknięciem, zmuszamy domknięcie do
przejęcia własności używanych wartości, zamiast pozwalać Rustowi wywnioskować,
że powinno je pożyczyć. Modyfikacja listingu 16-3 pokazana w listingu 16-5
skompiluje się i zadziała zgodnie z naszymi zamiarami.

<Listing number="16-5" file-name="src/main.rs" caption="Użycie słowa kluczowego `move`, aby zmusić domknięcie do przejęcia własności używanych wartości">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-05/src/main.rs}}
```

</Listing>

Moglibyśmy ulec pokusie, aby tak samo naprawić kod z listingu 16-4, w którym
wątek główny wywołuje `drop`, czyli użyć domknięcia `move`. Ta poprawka jednak
nie zadziała, ponieważ to, co próbuje zrobić listing 16-4, jest niedozwolone z
innego powodu. Gdybyśmy dodali `move` do domknięcia, nastąpiłoby przeniesienie
(*move*) `v` do środowiska domknięcia i nie moglibyśmy już wywołać na nim
`drop` w wątku głównym. Zamiast tego dostalibyśmy taki błąd kompilatora:

```console
{{#include ../listings/ch16-fearless-concurrency/output-only-01-move-drop/output.txt}}
```

Reguły własności Rusta znów nas uratowały! Kod z listingu 16-3 zgłosił błąd,
ponieważ Rust zachowywał się ostrożnie i tylko pożyczał `v` wątkowi, co
oznaczało, że wątek główny teoretycznie mógł unieważnić referencję nowego
wątku. Polecając Rustowi przenieść własność `v` do nowego wątku, gwarantujemy
Rustowi, że wątek główny nie będzie już używał `v`. Jeśli w ten sam sposób
zmienimy listing 16-4, naruszymy reguły własności, gdy spróbujemy użyć `v` w
wątku głównym. Słowo kluczowe `move` zastępuje ostrożne domyślne zachowanie
Rusta, czyli pożyczanie; nie pozwala nam naruszać reguł własności.

Skoro omówiliśmy już, czym są wątki i jakie metody udostępnia API wątków,
przyjrzyjmy się kilku sytuacjom, w których możemy z nich korzystać.

{{#quiz ../quizzes/ch16-01-threads.toml}}

[capture]: ch13-01-closures.html#capturing-references-or-moving-ownership

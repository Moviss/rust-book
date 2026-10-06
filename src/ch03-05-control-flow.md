## Przepływ sterowania {#control-flow}

Możliwość uruchomienia kodu w zależności od tego, czy warunek ma wartość `true`,
oraz możliwość wielokrotnego uruchamiania kodu, dopóki warunek ma wartość
`true`, to podstawowe elementy większości języków programowania. Najczęściej
używanymi konstrukcjami, które pozwalają sterować przepływem wykonania kodu w
Ruście, są wyrażenia (*expressions*) `if` oraz pętle.

### Wyrażenia `if` {#if-expressions}

Wyrażenie `if` pozwala rozgałęzić kod w zależności od warunków. Podajesz
warunek, a potem mówisz: „Jeśli ten warunek jest spełniony, uruchom ten blok
kodu. Jeśli nie jest spełniony, nie uruchamiaj tego bloku kodu”.

Aby przyjrzeć się wyrażeniu `if`, utwórz w katalogu _projects_ nowy projekt o
nazwie _branches_. W pliku _src/main.rs_ wpisz następujący kod:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/src/main.rs}}
```

Każde wyrażenie `if` zaczyna się od słowa kluczowego (*keyword*) `if`, po którym
następuje warunek. Tutaj warunek sprawdza, czy zmienna `number` ma wartość
mniejszą niż 5. Blok kodu, który ma się wykonać, gdy warunek ma wartość `true`,
umieszczamy w nawiasach klamrowych bezpośrednio za warunkiem. Bloki kodu powiązane z
warunkami w wyrażeniach `if` nazywa się czasem _ramionami_ (*arms*), tak samo
jak ramiona w wyrażeniach `match`, które omawialiśmy w sekcji
[„Porównywanie odpowiedzi z sekretną liczbą”][comparing-the-guess-to-the-secret-number]<!--
ignore --> rozdziału 2.

Opcjonalnie możemy też dodać wyrażenie `else`, co tutaj zrobiliśmy, aby dać
programowi alternatywny blok kodu do wykonania, gdyby warunek miał
wartość `false`. Jeśli nie podasz wyrażenia `else`, a warunek ma wartość
`false`, program po prostu pominie blok `if` i przejdzie do dalszej części
kodu.

Spróbuj uruchomić ten kod; powinien wypisać następujący wynik:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-26-if-true/output.txt}}
```

Zmieńmy wartość `number` na taką, przy której warunek ma wartość `false`, i
zobaczmy, co się stanie:

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/src/main.rs:here}}
```

Uruchom program ponownie i spójrz na wynik:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-27-if-false/output.txt}}
```

Warto też zauważyć, że warunek w tym kodzie _musi_ być typu `bool`. Jeśli
warunek nie jest typu `bool`, dostaniemy błąd. Spróbuj na przykład uruchomić
następujący kod:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/src/main.rs}}
```

Tym razem warunek `if` daje wartość `3`, a Rust zgłasza błąd:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-28-if-condition-must-be-bool/output.txt}}
```

Błąd informuje, że Rust oczekiwał wartości typu `bool`, a dostał liczbę
całkowitą. W odróżnieniu od języków takich jak Ruby czy JavaScript Rust nie
próbuje automatycznie konwertować typów innych niż logiczne na wartość
logiczną. Musisz zrobić to jawnie i zawsze podawać `if` wartość logiczną jako
warunek. Jeśli na przykład chcemy, aby blok kodu `if` wykonał się tylko wtedy,
gdy liczba jest różna od `0`, możemy zmienić wyrażenie `if` na następujące:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-29-if-not-equal-0/src/main.rs}}
```

Uruchomienie tego kodu wypisze `number was something other than zero`.

#### Obsługa wielu warunków za pomocą `else if` {#handling-multiple-conditions-with-else-if}

Możesz użyć wielu warunków, łącząc `if` i `else` w wyrażenie `else if`. Na
przykład:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/src/main.rs}}
```

Ten program może pójść jedną z czterech ścieżek. Po jego uruchomieniu powinien
pojawić się następujący wynik:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-30-else-if/output.txt}}
```

W trakcie działania program sprawdza po kolei każde wyrażenie `if` i wykonuje
pierwszy blok, którego warunek ma wartość `true`. Zwróć uwagę, że choć 6 jest
podzielne przez 2, nie widzimy komunikatu `number is divisible by 2` ani tekstu
`number is not divisible by 4, 3, or 2` z bloku `else`. Dzieje się tak, ponieważ
Rust wykonuje tylko blok dla pierwszego warunku o wartości `true`, a gdy go
znajdzie, nie sprawdza już pozostałych.

Zbyt wiele wyrażeń `else if` może zaśmiecić kod, więc jeśli masz ich więcej niż
jedno, warto rozważyć refaktoryzację. W rozdziale 6 opisujemy potężną
konstrukcję rozgałęziającą Rusta o nazwie `match`, przeznaczoną właśnie do
takich sytuacji.

#### Użycie `if` w instrukcji `let` {#using-if-in-a-let-statement}

Ponieważ `if` jest wyrażeniem, możemy go użyć po prawej stronie instrukcji
(*statement*) `let`, aby przypisać jego wynik do zmiennej, tak jak w listingu
3-2.

<Listing number="3-2" file-name="src/main.rs" caption="Przypisanie wyniku wyrażenia `if` do zmiennej">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-02/src/main.rs}}
```

</Listing>

Zmienna `number` zostanie związana z wartością zależną od wyniku wyrażenia
`if`. Uruchom ten kod i zobacz, co się stanie:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-02/output.txt}}
```

Pamiętaj, że blok kodu przyjmuje wartość ostatniego wyrażenia, które zawiera,
a same liczby również są wyrażeniami. Tutaj wartość całego wyrażenia `if`
zależy od tego, który blok kodu zostanie wykonany. Oznacza to, że wartości,
które mogą być wynikiem poszczególnych ramion `if`, muszą być tego samego
typu; w listingu 3-2 wynikami zarówno ramienia `if`, jak i ramienia `else` były
liczby całkowite typu `i32`. Jeśli typy się nie zgadzają, jak w poniższym
przykładzie, dostaniemy błąd:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/src/main.rs}}
```

Przy próbie kompilacji tego kodu dostaniemy błąd. Ramiona `if` i `else` mają
wartości niezgodnych typów, a Rust dokładnie wskazuje, gdzie w programie leży
problem:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-31-arms-must-return-same-type/output.txt}}
```

Wyrażenie w bloku `if` daje liczbę całkowitą, a wyrażenie w bloku `else` –
łańcuch znaków (*string*). To nie zadziała, ponieważ zmienne muszą mieć jeden
typ, a Rust musi jednoznacznie wiedzieć w czasie kompilacji (*compile-time*),
jakiego typu jest zmienna `number`. Znajomość typu `number` pozwala
kompilatorowi sprawdzić, czy ten typ jest poprawny wszędzie, gdzie używamy
`number`. Rust nie mógłby tego zrobić, gdyby typ `number` był ustalany dopiero
w czasie działania programu; kompilator byłby bardziej złożony i dawałby mniej
gwarancji co do kodu, gdyby musiał śledzić wiele hipotetycznych typów dla
każdej zmiennej.

{{#quiz ../quizzes/ch03-05-control-flow-sec1-if.toml}}

### Powtarzanie za pomocą pętli {#repetition-with-loops}

Często przydaje się wykonanie bloku kodu więcej niż raz. Do tego celu Rust
udostępnia kilka rodzajów _pętli_ (*loops*), które przechodzą przez kod w ciele
pętli do końca, a potem natychmiast zaczynają od początku. Aby poeksperymentować
z pętlami, utwórzmy nowy projekt o nazwie _loops_.

Rust ma trzy rodzaje pętli: `loop`, `while` i `for`. Wypróbujmy każdą z nich.

#### Powtarzanie kodu za pomocą `loop` {#repeating-code-with-loop}

Słowo kluczowe `loop` każe Rustowi wykonywać blok kodu raz za razem, w
nieskończoność albo do momentu, w którym jawnie każesz mu przestać.

Na przykład zmień plik _src/main.rs_ w katalogu _loops_ tak, aby wyglądał
następująco:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-loop/src/main.rs}}
```

Po uruchomieniu tego programu zobaczymy, jak `again!` jest wypisywane bez
przerwy, dopóki ręcznie nie zatrzymamy programu. Większość terminali obsługuje
skrót klawiszowy <kbd>ctrl</kbd>-<kbd>C</kbd>, który przerywa program
utknięty w nieskończonej pętli. Wypróbuj to:

<!-- manual-regeneration
cd listings/ch03-common-programming-concepts/no-listing-32-loop
cargo run
CTRL-C
-->

```console
$ cargo run
   Compiling loops v0.1.0 (file:///projects/loops)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.08s
     Running `target/debug/loops`
again!
again!
again!
again!
^Cagain!
```

Symbol `^C` oznacza miejsce, w którym naciśnięto <kbd>ctrl</kbd>-<kbd>C</kbd>.

Słowo `again!` może, ale nie musi pojawić się po `^C`, w zależności od tego, w
którym miejscu pętli znajdował się kod w chwili otrzymania sygnału przerwania.

Na szczęście Rust daje też możliwość wyjścia z pętli z poziomu kodu. Możesz
umieścić w pętli słowo kluczowe `break`, aby wskazać programowi, kiedy ma
przestać wykonywać pętlę. Przypomnij sobie, że zrobiliśmy tak w grze w
zgadywanie w sekcji
[„Kończenie gry po poprawnej odpowiedzi”][quitting-after-a-correct-guess]<!-- ignore
--> rozdziału 2, aby zakończyć program, gdy użytkownik wygrał, odgadując właściwą
liczbę.

W grze w zgadywanie użyliśmy też `continue`, które w pętli każe programowi
pominąć resztę kodu w bieżącej iteracji pętli i przejść do następnej iteracji.

#### Zwracanie wartości z pętli {#returning-values-from-loops}

Jednym z zastosowań `loop` jest ponawianie operacji, o której wiesz, że może
się nie powieść, na przykład sprawdzania, czy wątek zakończył swoją pracę.
Może być też potrzebne przekazanie wyniku tej operacji z pętli do reszty kodu.
W tym celu możesz dodać wartość, którą chcesz zwrócić, po wyrażeniu `break`
używanym do zatrzymania pętli; ta wartość zostanie zwrócona z pętli, tak aby
można było jej użyć, jak pokazano tutaj:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-33-return-value-from-loop/src/main.rs}}
```

Przed pętlą deklarujemy zmienną o nazwie `counter` i inicjalizujemy ją wartością
`0`. Następnie deklarujemy zmienną o nazwie `result`, która przechowa wartość
zwróconą z pętli. W każdej iteracji pętli dodajemy `1` do zmiennej `counter`, a
potem sprawdzamy, czy `counter` jest równe `10`. 
Gdy tak jest, używamy słowa kluczowego `break` z wartością `counter * 2`. 
Po pętli stawiamy średnik, aby zakończyć instrukcję przypisującą wartość do `result`. Na koniec
wypisujemy wartość `result`, która w tym przypadku wynosi `20`.

Możesz też użyć `return` wewnątrz pętli. O ile `break` wychodzi tylko z
bieżącej pętli, `return` zawsze wychodzi z bieżącej funkcji.

> *Uwaga:* średnik po `break counter * 2` jest formalnie opcjonalny. `break` bardzo przypomina `return`:
> oba mogą opcjonalnie przyjąć wyrażenie jako argument i oba zmieniają przepływ sterowania (*control flow*).
> Kod po `break` lub `return` nigdy nie zostaje wykonany, więc kompilator Rusta traktuje wyrażenie `break` i
> wyrażenie `return` tak, jakby miały wartość jednostkową (*unit*), czyli `()`.

<!-- Old headings. Do not remove or links may break. -->
<a id="loop-labels-to-disambiguate-between-multiple-loops"></a>

#### Rozróżnianie pętli za pomocą etykiet {#disambiguating-with-loop-labels}

Jeśli masz pętle w pętlach, `break` i `continue` odnoszą się do najbardziej
wewnętrznej pętli w danym miejscu. Możesz opcjonalnie oznaczyć pętlę
_etykietą pętli_ (*loop label*), której potem użyjesz z `break` lub `continue`,
aby wskazać, że te słowa kluczowe dotyczą pętli z etykietą, a nie najbardziej
wewnętrznej pętli. Etykiety pętli muszą zaczynać się od pojedynczego apostrofu. Oto
przykład z dwiema zagnieżdżonymi pętlami:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/src/main.rs}}
```

Zewnętrzna pętla ma etykietę `'counting_up` i liczy w górę od 0 do 2.
Wewnętrzna pętla bez etykiety odlicza w dół od 10 do 9. Pierwsze `break`, które
nie podaje etykiety, wychodzi tylko z wewnętrznej pętli. Instrukcja
`break 'counting_up;` wychodzi z zewnętrznej pętli. Ten kod wypisuje:

```console
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-32-5-loop-labels/output.txt}}
```

<!-- Old headings. Do not remove or links may break. -->
<a id="conditional-loops-with-while"></a>

#### Upraszczanie pętli warunkowych za pomocą while {#streamlining-conditional-loops-with-while}

Program często musi sprawdzać warunek wewnątrz pętli. Dopóki warunek ma wartość
`true`, pętla działa. Gdy warunek przestaje mieć wartość `true`, program
wywołuje `break` i zatrzymuje pętlę. Takie zachowanie można zaimplementować za
pomocą kombinacji `loop`, `if`, `else` i `break`; jeśli chcesz, możesz teraz
spróbować zrobić to w programie. Ten wzorzec jest jednak tak powszechny, że
Rust ma dla niego wbudowaną konstrukcję językową: pętlę `while`. W listingu 3-3
używamy `while`, aby program wykonał pętlę trzy razy, za każdym razem odliczając
w dół, a po zakończeniu pętli wypisał komunikat i zakończył działanie.

<Listing number="3-3" file-name="src/main.rs" caption="Użycie pętli `while` do uruchamiania kodu, dopóki warunek ma wartość `true`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-03/src/main.rs}}
```

</Listing>

Ta konstrukcja eliminuje sporo zagnieżdżeń, które byłyby potrzebne przy użyciu
`loop`, `if`, `else` i `break`, a przy tym jest czytelniejsza. Dopóki warunek ma
wartość `true`, kod się wykonuje; w przeciwnym razie program wychodzi z pętli.

#### Przechodzenie przez kolekcję za pomocą `for` {#looping-through-a-collection-with-for}

Konstrukcji `while` możesz też użyć do przechodzenia przez elementy kolekcji,
na przykład tablicy. Pętla z listingu 3-4 wypisuje każdy element tablicy `a`.

<Listing number="3-4" file-name="src/main.rs" caption="Przechodzenie przez wszystkie elementy kolekcji za pomocą pętli `while`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-04/src/main.rs}}
```

</Listing>

Ten kod przechodzi kolejno przez elementy tablicy. Zaczyna od indeksu `0`, a
potem wykonuje pętlę, aż dotrze do ostatniego indeksu w tablicy (czyli do
chwili, gdy `index < 5` przestanie mieć wartość `true`). Uruchomienie tego kodu
wypisze każdy element tablicy:

```console
{{#include ../listings/ch03-common-programming-concepts/listing-03-04/output.txt}}
```

Zgodnie z oczekiwaniami w terminalu pojawia się wszystkich pięć wartości z
tablicy. Choć `index` w pewnym momencie osiągnie wartość `5`, pętla kończy się
przed próbą pobrania z tablicy szóstej wartości.

To podejście łatwo prowadzi jednak do błędów; jeśli wartość indeksu lub
warunek będą niepoprawne, program może spanikować (*panic*). Gdyby na przykład
zmienić definicję tablicy `a` tak, aby miała cztery elementy, ale zapomnieć
zaktualizować warunek na `while index < 4`, kod by spanikował. Jest też
powolne, ponieważ kompilator dodaje kod wykonywany w czasie działania, który w
każdej iteracji pętli sprawdza, czy indeks mieści się w granicach tablicy.

Bardziej zwięzłą alternatywą jest pętla `for`, która wykonuje kod dla każdego
elementu kolekcji. Pętla `for` wygląda tak jak kod w listingu 3-5.

<Listing number="3-5" file-name="src/main.rs" caption="Przechodzenie przez wszystkie elementy kolekcji za pomocą pętli `for`">

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/listing-03-05/src/main.rs}}
```

</Listing>

Po uruchomieniu tego kodu zobaczymy ten sam wynik co w listingu 3-4. Co
ważniejsze, zwiększyliśmy bezpieczeństwo kodu i wyeliminowaliśmy ryzyko błędów
wynikających z wyjścia poza koniec tablicy albo z niedojścia do niego i
pominięcia niektórych elementów. Kod maszynowy generowany z pętli `for` może być
też wydajniejszy, ponieważ indeksu nie trzeba porównywać z długością tablicy w
każdej iteracji.

Przy pętli `for` nie musisz pamiętać o zmianie innego kodu, gdy zmienisz liczbę
wartości w tablicy, co byłoby konieczne przy metodzie z listingu 3-4.

Bezpieczeństwo i zwięzłość pętli `for` sprawiają, że jest to najczęściej
używana konstrukcja pętli w Ruście. Nawet gdy chcesz wykonać kod określoną
liczbę razy, jak w przykładzie z odliczaniem, który w listingu 3-3 używał pętli
`while`, większość rustowców (*Rustaceans*) użyłaby pętli `for`. Służy do tego
`Range` z biblioteki standardowej, który generuje kolejne liczby, zaczynając od
jednej liczby i kończąc przed drugą.

Tak wyglądałoby odliczanie z użyciem pętli `for` i innej metody, o której
jeszcze nie mówiliśmy, `rev`, odwracającej zakres:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-34-for-range/src/main.rs}}
```

Ten kod jest trochę ładniejszy, prawda?

{{#quiz ../quizzes/ch03-05-control-flow-sec2-loops.toml}}

## Podsumowanie {#summary}

Udało się! To był obszerny rozdział: poznaliśmy zmienne, skalarne i złożone
typy danych, funkcje, komentarze, wyrażenia `if` oraz pętle! Aby przećwiczyć
omówione tu pojęcia, spróbuj napisać programy, które:

- przeliczają temperatury między stopniami Fahrenheita i Celsjusza;
- generują *n*-tą liczbę Fibonacciego;
- wypisują tekst kolędy „The Twelve Days of Christmas”, wykorzystując
  powtórzenia w piosence.

Gdy zechcesz ruszyć dalej, omówimy pojęcie w Ruście, które zazwyczaj _nie_
występuje w innych językach programowania: własność (*ownership*).

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[quitting-after-a-correct-guess]: ch02-00-guessing-game-tutorial.html#quitting-after-a-correct-guess

## Zmienne i mutowalność {#variables-and-mutability}

Jak wspomnieliśmy w sekcji [„Przechowywanie wartości w
zmiennych”][storing-values-with-variables]<!-- ignore -->, zmienne są domyślnie
niemutowalne (*immutable*). To jedna z wielu zachęt, którymi Rust skłania cię do
pisania kodu w sposób wykorzystujący bezpieczeństwo i łatwą współbieżność
(*concurrency*), jakie oferuje. Nadal jednak możesz uczynić swoje zmienne
mutowalnymi (*mutable*). Przyjrzyjmy się, jak i dlaczego Rust zachęca do
preferowania niemutowalności oraz dlaczego czasem warto z niej zrezygnować.

Gdy zmienna jest niemutowalna, to po związaniu wartości z nazwą nie możesz tej
wartości zmienić. Aby to zilustrować, utwórz w katalogu _projects_ nowy projekt
o nazwie _variables_ za pomocą polecenia `cargo new variables`.

Następnie w nowym katalogu _variables_ otwórz plik _src/main.rs_ i zastąp jego
zawartość poniższym kodem, który na razie się nie skompiluje:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/src/main.rs}}
```

Zapisz i uruchom program za pomocą `cargo run`. Powinien pojawić się komunikat
o błędzie dotyczącym niemutowalności, taki jak poniżej:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-01-variables-are-immutable/output.txt}}
```

Ten przykład pokazuje, jak kompilator pomaga znajdować błędy w programach. Błędy
kompilacji bywają frustrujące, ale tak naprawdę oznaczają tylko, że twój program
jeszcze nie robi bezpiecznie tego, czego od niego oczekujesz; _nie_ oznaczają,
że jesteś kiepskim programistą! Doświadczeni rustowcy (*Rustaceans*) też
dostają błędy kompilacji.

Otrzymany komunikat o błędzie `` cannot assign twice to immutable variable `x` `` pojawił się, ponieważ próbujesz przypisać drugą wartość do niemutowalnej zmiennej `x`.

To ważne, że dostajemy błędy w czasie kompilacji (*compile-time*), gdy
próbujemy zmienić wartość oznaczoną jako niemutowalna, bo właśnie taka sytuacja
może prowadzić do błędów w programie. Jeśli jedna część kodu działa przy
założeniu, że wartość nigdy się nie zmieni, a inna część kodu tę wartość
zmienia, to pierwsza część może nie robić tego, do czego została zaprojektowana.
Przyczynę takiego błędu trudno potem wyśledzić, zwłaszcza gdy druga część kodu
zmienia wartość tylko _czasami_. Kompilator Rusta gwarantuje, że jeśli
deklarujesz, że wartość się nie zmieni, to naprawdę się nie zmieni, więc nie
musisz sam tego pilnować. Dzięki temu łatwiej jest rozumować o kodzie.

Mutowalność bywa jednak bardzo przydatna i może ułatwić pisanie kodu. Choć
zmienne są domyślnie niemutowalne, możesz uczynić je mutowalnymi, dodając `mut`
przed nazwą zmiennej, tak jak w [rozdziale
2][storing-values-with-variables]<!-- ignore -->. Dodanie `mut` przekazuje też
intencję przyszłym czytelnikom kodu: sygnalizuje, że inne części kodu będą
zmieniać wartość tej zmiennej.

Zmieńmy na przykład _src/main.rs_ na następujący kod:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/src/main.rs}}
```

Gdy teraz uruchomimy program, otrzymamy:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-02-adding-mut/output.txt}}
```

Gdy użyjemy `mut`, możemy zmienić wartość związaną z `x` z `5` na `6`.
Ostatecznie to ty decydujesz, czy użyć mutowalności, i zależy to od tego, co
uznasz za najczytelniejsze w danej sytuacji.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec1-variables.toml}}

<!-- Old headings. Do not remove or links may break. -->
<a id="constants"></a>

### Deklarowanie stałych {#declaring-constants}

Podobnie jak zmienne niemutowalne, _stałe_ (*constants*) to wartości związane z
nazwą, których nie wolno zmieniać, ale między stałymi a zmiennymi jest kilka
różnic.

Po pierwsze, ze stałymi nie można używać `mut`. Stałe nie są niemutowalne tylko
domyślnie – są niemutowalne zawsze. Stałe deklaruje się słowem kluczowym
`const` zamiast `let`, a typ wartości _musi_ być opatrzony adnotacją. Typy i
adnotacje typów omówimy w następnej sekcji, [„Typy
danych”][data-types]<!-- ignore -->, więc na razie nie przejmuj się
szczegółami. Zapamiętaj tylko, że zawsze musisz podać adnotację typu.

Stałe można deklarować w dowolnym zasięgu (*scope*), także globalnym, dzięki
czemu przydają się do wartości, o których musi wiedzieć wiele części kodu.

Ostatnia różnica polega na tym, że stałej można przypisać tylko wyrażenie stałe
(*constant expression*), a nie wynik wartości, którą dałoby się obliczyć
wyłącznie w czasie działania programu.

Oto przykład deklaracji stałej:

```rust
const THREE_HOURS_IN_SECONDS: u32 = 60 * 60 * 3;
```

Stała nazywa się `THREE_HOURS_IN_SECONDS`, a jej wartością jest wynik mnożenia
60 (liczby sekund w minucie) przez 60 (liczbę minut w godzinie) przez 3 (liczbę
godzin, które chcemy liczyć w tym programie). Konwencja nazewnicza Rusta dla
stałych to same wielkie litery z podkreśleniami między słowami. Kompilator
potrafi obliczyć w czasie kompilacji ograniczony zestaw operacji, co pozwala
nam zapisać tę wartość w sposób łatwiejszy do zrozumienia i sprawdzenia, zamiast
przypisywać stałej wartość 10 800. Więcej informacji o tym, jakich operacji
można używać przy deklarowaniu stałych, znajdziesz w [sekcji dokumentacji Rust
Reference o obliczaniu wyrażeń stałych][const-eval].

Stałe są ważne przez cały czas działania programu, w obrębie zasięgu, w którym
je zadeklarowano. Ta właściwość sprawia, że stałe przydają się do wartości z
dziedziny twojej aplikacji, o których może potrzebować wiedzieć wiele części
programu, takich jak maksymalna liczba punktów, jaką może zdobyć gracz w grze,
albo prędkość światła.

Nazywanie wartości wpisanych na sztywno w kod i używanych w całym programie jako
stałych pomaga przekazać znaczenie tych wartości przyszłym opiekunom kodu.
Dzięki temu w kodzie jest też tylko jedno miejsce, które trzeba zmienić, gdyby
taka wartość wymagała w przyszłości aktualizacji.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec2-constants.toml}}

### Przesłanianie {#shadowing}

Jak pokazał samouczek z grą w zgadywanie w [rozdziale
2][comparing-the-guess-to-the-secret-number]<!-- ignore -->, możesz
zadeklarować nową zmienną o tej samej nazwie co poprzednia. Rustowcy mówią, że
pierwsza zmienna jest _przesłonięta_ (*shadowed*) przez drugą, co oznacza, że
gdy użyjesz nazwy zmiennej, kompilator zobaczy drugą zmienną. W efekcie druga zmienna przysłania pierwszą i przejmuje wszystkie
użycia tej nazwy, dopóki sama nie zostanie przesłonięta albo nie skończy się
zasięg. Zmienną możemy przesłonić, używając tej samej nazwy i ponownie stosując
słowo kluczowe `let`, w ten sposób:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/src/main.rs}}
```

Ten program najpierw wiąże `x` z wartością `5`. Następnie tworzy nową zmienną
`x`, powtarzając `let x =`, bierze pierwotną wartość i dodaje do niej `1`, więc
wartość `x` wynosi `6`. Potem, w wewnętrznym zasięgu utworzonym przez nawiasy
klamrowe, trzecia instrukcja (*statement*) `let` również przesłania `x` i tworzy
nową zmienną, mnożąc poprzednią wartość przez `2`, przez co `x` ma wartość
`12`. Gdy ten zasięg się kończy, wewnętrzne przesłanianie przestaje działać i
`x` znów wynosi `6`. Po uruchomieniu program wypisze:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-03-shadowing/output.txt}}
```

Przesłanianie różni się od oznaczenia zmiennej jako `mut`, ponieważ jeśli
przypadkiem spróbujemy ponownie przypisać wartość do tej zmiennej bez słowa
kluczowego `let`, dostaniemy błąd kompilacji. Używając `let`, możemy wykonać na
wartości kilka przekształceń, a po ich zakończeniu zmienna pozostanie
niemutowalna.

Druga różnica między `mut` a przesłanianiem polega na tym, że ponowne użycie
słowa kluczowego `let` faktycznie tworzy nową zmienną, więc możemy zmienić typ
wartości, a zachować tę samą nazwę. Załóżmy na przykład, że program prosi
użytkownika, by pokazał, ile spacji chce mieć między fragmentami tekstu, wpisując
znaki spacji, a my chcemy zapisać te dane wejściowe jako liczbę:

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-04-shadowing-can-change-types/src/main.rs:here}}
```

Pierwsza zmienna `spaces` ma typ łańcucha znaków (*string*), a druga zmienna
`spaces` – typ liczbowy. Przesłanianie oszczędza nam więc wymyślania różnych
nazw, takich jak `spaces_str` i `spaces_num`; zamiast tego możemy ponownie użyć
prostszej nazwy `spaces`. Jeśli jednak spróbujemy użyć do tego `mut`, jak
pokazano poniżej, dostaniemy błąd kompilacji:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/src/main.rs:here}}
```

Błąd mówi, że nie wolno nam zmieniać typu zmiennej:

```console
{{#include ../listings/ch03-common-programming-concepts/no-listing-05-mut-cant-change-types/output.txt}}
```

Skoro już wiemy, jak działają zmienne, przyjrzyjmy się innym typom danych, jakie
mogą mieć.

{{#quiz ../quizzes/ch03-01-variables-and-mutability-sec3-shadowing.toml}}

[comparing-the-guess-to-the-secret-number]: ch02-00-guessing-game-tutorial.html#comparing-the-guess-to-the-secret-number
[data-types]: ch03-02-data-types.html#data-types
[storing-values-with-variables]: ch02-00-guessing-game-tutorial.html#storing-values-with-variables
[const-eval]: https://doc.rust-lang.org/reference/const_eval.html

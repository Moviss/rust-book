## Wszystkie miejsca, w których można używać wzorców {#all-the-places-patterns-can-be-used}

Wzorce pojawiają się w Ruście w wielu miejscach i używasz ich często, nawet o
tym nie wiedząc! W tym podrozdziale omówimy wszystkie miejsca, w których wzorce
są dozwolone.

### Ramiona `match` {#match-arms}

Jak wspomnieliśmy w rozdziale 6, używamy wzorców w ramionach (*arms*) wyrażeń
(*expressions*) `match`. Formalnie wyrażenie `match` składa się ze słowa
kluczowego (*keyword*) `match`, dopasowywanej wartości i jednego lub więcej
ramion, z których każde zawiera wzorzec i wyrażenie wykonywane, jeśli wartość
pasuje do wzorca danego ramienia:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre><code>match <em>VALUE</em> {
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
    <em>PATTERN</em> => <em>EXPRESSION</em>,
}</code></pre>

Oto na przykład wyrażenie `match` z listingu 6-5, które dopasowuje wartość
`Option<i32>` w zmiennej `x`:

```rust,ignore
match x {
    None => None,
    Some(i) => Some(i + 1),
}
```

Wzorcami w tym wyrażeniu `match` są `None` i `Some(i)` po lewej stronie każdej
strzałki.

Wyrażenia `match` muszą być wyczerpujące (*exhaustive*) w tym sensie, że muszą
uwzględniać wszystkie możliwe wartości wyrażenia w `match`. Jednym ze sposobów
na upewnienie się, że uwzględniono wszystkie możliwości, jest umieszczenie w
ostatnim ramieniu wzorca przechwytującego wszystko (*catch-all*): na przykład
nazwa zmiennej pasująca do dowolnej wartości nigdy nie zawiedzie, a więc
obejmuje wszystkie pozostałe przypadki.

Szczególny wzorzec `_` pasuje do wszystkiego, ale nigdy nie wiąże wartości ze
zmienną, dlatego często używa się go w ostatnim ramieniu. Wzorzec `_` przydaje
się na przykład wtedy, gdy chcesz zignorować każdą wartość, której nie
wymieniono wcześniej. Wzorzec `_` omówimy dokładniej w podrozdziale
[„Ignorowanie wartości we wzorcu”][ignoring-values-in-a-pattern]<!-- ignore -->
w dalszej części tego rozdziału.

### Instrukcje `let` {#let-statements}

Przed tym rozdziałem jawnie omawialiśmy używanie wzorców tylko z `match` i
`if let`, ale w rzeczywistości używaliśmy ich także w innych miejscach, w tym w
instrukcjach (*statements*) `let`. Weźmy na przykład to proste przypisanie
zmiennej za pomocą `let`:

```rust
let x = 5;
```

Za każdym razem, gdy używasz takiej instrukcji `let`, używasz wzorców, nawet
jeśli nie zdajesz sobie z tego sprawy! Bardziej formalnie instrukcja `let`
wygląda tak:

<!--
  Manually formatted rather than using Markdown intentionally: Markdown does not
  support italicizing code in the body of a block like this!
-->

<pre>
<code>let <em>PATTERN</em> = <em>EXPRESSION</em>;</code>
</pre>

W instrukcjach takich jak `let x = 5;`, w których miejsce PATTERN zajmuje nazwa
zmiennej, ta nazwa jest po prostu szczególnie prostą formą wzorca. Rust
porównuje wyrażenie ze wzorcem i przypisuje wszystkie znalezione nazwy. Zatem w
przykładzie `let x = 5;` `x` jest wzorcem, który oznacza „zwiąż to, co tu
pasuje, ze zmienną `x`”. Ponieważ nazwa `x` stanowi cały wzorzec, w praktyce
oznacza on „zwiąż wszystko ze zmienną `x`, niezależnie od wartości”.

Aby wyraźniej zobaczyć aspekt dopasowywania wzorców (*pattern matching*) w
`let`, przyjrzyj się listingowi 19-1, w którym wzorzec użyty z `let`
destrukturyzuje krotkę (*tuple*).


<Listing number="19-1" caption="Użycie wzorca do destrukturyzacji krotki i utworzenia trzech zmiennych naraz">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-01/src/main.rs:here}}
```

</Listing>

Dopasowujemy tu krotkę do wzorca. Rust porównuje wartość `(1, 2, 3)` ze
wzorcem `(x, y, z)` i stwierdza, że wartość pasuje do wzorca – to znaczy, że
liczba elementów jest w obu taka sama – więc wiąże `1` z `x`, `2` z `y`, a `3`
z `z`. Możesz traktować ten wzorzec krotki jak trzy zagnieżdżone w nim
pojedyncze wzorce zmiennych.

Jeśli liczba elementów we wzorcu nie zgadza się z liczbą elementów krotki,
typy jako całość nie będą pasować i dostaniemy błąd kompilatora. Na przykład
listing 19-2 pokazuje próbę destrukturyzacji krotki z trzema elementami na dwie
zmienne, która się nie powiedzie.

<Listing number="19-2" caption="Niepoprawnie skonstruowany wzorzec, którego zmienne nie odpowiadają liczbie elementów krotki">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-02/src/main.rs:here}}
```

</Listing>

Próba skompilowania tego kodu kończy się takim błędem typu:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-02/output.txt}}
```

Aby naprawić błąd, moglibyśmy zignorować jedną lub więcej wartości krotki za
pomocą `_` lub `..`, jak zobaczysz w podrozdziale [„Ignorowanie wartości we
wzorcu”][ignoring-values-in-a-pattern]<!-- ignore -->. Jeśli problem polega na
tym, że we wzorcu jest za dużo zmiennych, rozwiązaniem jest dopasowanie typów
przez usunięcie zmiennych, tak aby liczba zmiennych była równa liczbie
elementów krotki.

### Wyrażenia warunkowe `if let` {#conditional-if-let-expressions}

W rozdziale 6 omówiliśmy, jak używać wyrażeń `if let` głównie jako krótszego
sposobu zapisania odpowiednika `match`, który dopasowuje tylko jeden przypadek.
Opcjonalnie `if let` może mieć odpowiadający mu blok `else` z kodem
wykonywanym, gdy wzorzec w `if let` nie pasuje.

Listing 19-3 pokazuje, że można też dowolnie łączyć wyrażenia `if let`,
`else if` i `else if let`. Daje nam to większą elastyczność niż wyrażenie
`match`, w którym możemy wyrazić tylko jedną wartość porównywaną ze wzorcami.
Rust nie wymaga też, by warunki w serii ramion `if let`, `else if` i
`else if let` były ze sobą powiązane.

Kod w listingu 19-3 ustala kolor tła na podstawie serii sprawdzeń kilku
warunków. Na potrzeby tego przykładu utworzyliśmy zmienne z wartościami
wpisanymi na sztywno, które prawdziwy program mógłby otrzymać od użytkownika.

<Listing number="19-3" file-name="src/main.rs" caption="Łączenie `if let`, `else if`, `else if let` i `else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-03/src/main.rs}}
```

</Listing>

Jeśli użytkownik poda ulubiony kolor, zostanie on użyty jako kolor tła. Jeśli
ulubiony kolor nie został podany, a dziś jest wtorek, kolorem tła jest zielony.
W przeciwnym razie, jeśli użytkownik poda swój wiek jako łańcuch znaków
(*string*), który uda się sparsować jako liczbę, kolorem jest fioletowy albo
pomarańczowy, w zależności od wartości liczby. Jeśli żaden z tych warunków nie
jest spełniony, kolorem tła jest niebieski.

Ta struktura warunkowa pozwala obsłużyć złożone wymagania. Przy wartościach
wpisanych tu na sztywno ten przykład wypisze
`Using purple as the background color`.

Jak widać, `if let` może też wprowadzać nowe zmienne, które przesłaniają
(*shadow*) istniejące zmienne w taki sam sposób jak ramiona `match`:
wiersz `if let Ok(age) = age` wprowadza nową zmienną `age`, zawierającą
wartość z wariantu `Ok`, i przesłania nią istniejącą zmienną `age`. Oznacza
to, że warunek `if age > 30` musimy umieścić wewnątrz tego bloku: nie możemy połączyć
tych dwóch warunków w `if let Ok(age) = age && age > 30`. Nowa zmienna `age`,
którą chcemy porównać z 30, nie jest ważna, dopóki nowy zasięg (*scope*) nie
rozpocznie się nawiasem klamrowym.

Wadą wyrażeń `if let` jest to, że kompilator nie sprawdza ich wyczerpywalności,
podczas gdy w przypadku wyrażeń `match` to robi. Gdybyśmy pominęli ostatni blok
`else`, a przez to nie obsłużyli niektórych przypadków, kompilator nie
ostrzegłby nas przed możliwym błędem logicznym.

### Pętle warunkowe `while let` {#while-let-conditional-loops}

Pętla warunkowa `while let`, zbudowana podobnie jak `if let`, pozwala pętli
`while` działać tak długo, jak długo wzorzec pasuje. W listingu 19-4 pokazujemy
pętlę `while let`, która czeka na komunikaty przesyłane między wątkami, tym
razem jednak sprawdzając `Result` zamiast `Option`.

<Listing number="19-4" caption="Użycie pętli `while let` do wypisywania wartości tak długo, jak `rx.recv()` zwraca `Ok`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-04/src/main.rs:here}}
```

</Listing>

Ten przykład wypisuje `1`, `2`, a potem `3`. Metoda `recv` pobiera pierwszy
komunikat ze strony odbiorczej kanału i zwraca `Ok(value)`. Gdy po raz pierwszy
zetknęliśmy się z `recv` w rozdziale 16, rozpakowywaliśmy błąd bezpośrednio
albo traktowaliśmy odbiornik jak iterator w pętli `for`. Jak jednak pokazuje
listing 19-4, możemy też użyć `while let`, ponieważ metoda `recv` zwraca `Ok`
za każdym razem, gdy nadejdzie komunikat, dopóki istnieje nadajnik, a gdy
strona nadawcza się rozłączy, zwraca `Err`.

### Pętle `for` {#for-loops}

W pętli `for` wartość następująca bezpośrednio po słowie kluczowym `for` jest
wzorcem. Na przykład w `for x in y` wzorcem jest `x`. Listing 19-5 pokazuje,
jak użyć wzorca w pętli `for` do destrukturyzacji, czyli rozłożenia na części,
krotki w ramach pętli `for`.


<Listing number="19-5" caption="Użycie wzorca w pętli `for` do destrukturyzacji krotki">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-05/src/main.rs:here}}
```

</Listing>

Kod z listingu 19-5 wypisze:


```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-05/output.txt}}
```

Przekształcamy iterator za pomocą metody `enumerate` tak, by zwracał wartość
oraz jej indeks, umieszczone w krotce. Pierwszą zwróconą wartością jest krotka
`(0, 'a')`. Gdy ta wartość zostanie dopasowana do wzorca `(index, value)`,
index będzie równy `0`, a value będzie równe `'a'`, co spowoduje wypisanie
pierwszej linii wyjścia.


### Parametry funkcji {#function-parameters}

Parametry funkcji również mogą być wzorcami. Kod z listingu 19-6, w którym
deklarujemy funkcję o nazwie `foo` przyjmującą jeden parametr `x` typu `i32`,
powinien już wyglądać znajomo.

<Listing number="19-6" caption="Sygnatura funkcji używająca wzorców w parametrach">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-06/src/main.rs:here}}
```

</Listing>

Część `x` to wzorzec! Podobnie jak w przypadku `let`, moglibyśmy dopasować
krotkę w argumentach funkcji do wzorca. Listing 19-7 rozdziela wartości krotki
w chwili przekazywania jej do funkcji.

<Listing number="19-7" file-name="src/main.rs" caption="Funkcja z parametrami, które destrukturyzują krotkę">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-07/src/main.rs}}
```

</Listing>

Ten kod wypisuje `Current location: (3, 5)`. Wartości `&(3, 5)` pasują do
wzorca `&(x, y)`, więc `x` ma wartość `3`, a `y` wartość `5`.

Wzorców możemy też używać w listach parametrów domknięć (*closures*) tak samo
jak w listach parametrów funkcji, ponieważ domknięcia są podobne do funkcji, co
omówiliśmy w rozdziale 13.

Znasz już kilka sposobów używania wzorców, ale wzorce nie działają tak samo
we wszystkich miejscach, w których możemy ich użyć. W niektórych miejscach
wzorce muszą być nieodrzucalne (*irrefutable*), w innych mogą to być wzorce
odrzucalne (*refutable*). Tymi dwoma pojęciami zajmiemy się teraz.

{{#quiz ../quizzes/ch18-01-all-the-places-for-patterns.toml}}

[ignoring-values-in-a-pattern]: ch19-03-pattern-syntax.html#ignoring-values-in-a-pattern

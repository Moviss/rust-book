<!-- Old headings. Do not remove or links may break. -->

<a id="the-match-control-flow-operator"></a>

## Konstrukcja przepływu sterowania `match` {#the-match-control-flow-construct}

Rust ma niezwykle potężną konstrukcję przepływu sterowania (*control flow*)
o nazwie `match`, która pozwala porównać wartość z serią wzorców, a następnie
wykonać kod zależnie od tego, który wzorzec pasuje. Wzorce mogą składać się
z literałów, nazw zmiennych, symboli wieloznacznych (*wildcards*) i wielu innych
elementów; [rozdział 19][ch19-00-patterns]<!-- ignore --> omawia wszystkie
rodzaje wzorców i ich działanie. Siła `match` bierze się z ekspresywności
wzorców oraz z tego, że kompilator potwierdza obsłużenie wszystkich możliwych
przypadków.

Wyobraź sobie wyrażenie `match` jako sortownicę monet: monety zsuwają się po
torze z otworami różnej wielkości i każda wpada do pierwszego napotkanego
otworu, w który się mieści. Tak samo wartości przechodzą przez kolejne wzorce
w `match` i przy pierwszym wzorcu, do którego wartość „pasuje”, trafia ona do
powiązanego bloku kodu, który zostaje wykonany.

Skoro mowa o monetach, użyjmy ich jako przykładu z `match`! Możemy napisać
funkcję, która przyjmuje nieznaną amerykańską monetę i – podobnie jak maszyna
licząca – ustala, jaka to moneta, i zwraca jej wartość w centach, jak pokazano
w listingu 6-3.

<Listing number="6-3" caption="Enum i wyrażenie `match`, którego wzorcami są warianty tego enuma">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-03/src/main.rs:here}}
```

</Listing>

Przeanalizujmy `match` w funkcji `value_in_cents`. Najpierw piszemy słowo
kluczowe `match`, a po nim wyrażenie – tutaj jest to wartość `coin`.
Przypomina to wyrażenie warunkowe używane z `if`, ale jest istotna różnica:
w `if` warunek musi dawać wartość logiczną, a tutaj może być dowolnego typu.
Typem `coin` w tym przykładzie jest enum `Coin`, który zdefiniowaliśmy
w pierwszym wierszu.

Dalej są ramiona (*arms*) `match`. Ramię składa się z dwóch części: wzorca
i kodu. Pierwsze ramię ma tu wzorzec będący wartością `Coin::Penny`, a po nim
operator `=>`, który oddziela wzorzec od kodu do wykonania. Kodem jest w tym
przypadku po prostu wartość `1`. Kolejne ramiona oddziela się przecinkami.

Gdy wyrażenie `match` się wykonuje, porównuje wynikową wartość ze wzorcem
każdego ramienia po kolei. Jeśli wzorzec pasuje do wartości, wykonywany jest
kod powiązany z tym wzorcem. Jeśli nie pasuje, wykonanie przechodzi do
następnego ramienia – zupełnie jak w sortownicy monet. Ramion może być tyle,
ile potrzebujemy: w listingu 6-3 nasze `match` ma cztery ramiona.

Kod powiązany z każdym ramieniem jest wyrażeniem, a wynikowa wartość wyrażenia
w pasującym ramieniu jest wartością zwracaną przez całe wyrażenie `match`.

Zwykle nie używamy nawiasów klamrowych, jeśli kod ramienia jest krótki – jak
w listingu 6-3, gdzie każde ramię po prostu zwraca wartość. Jeśli chcesz
wykonać w ramieniu kilka wierszy kodu, musisz użyć nawiasów klamrowych, a przecinek
po ramieniu staje się wtedy opcjonalny. Na przykład poniższy kod wypisuje
„Lucky penny!” przy każdym wywołaniu metody z `Coin::Penny`, ale nadal zwraca
ostatnią wartość bloku, czyli `1`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-08-match-arm-multiple-lines/src/main.rs:here}}
```

### Wzorce wiążące wartości {#patterns-that-bind-to-values}

Kolejną przydatną cechą ramion `match` jest to, że mogą wiązać się z częściami
wartości pasujących do wzorca. W ten sposób możemy wydobywać wartości
z wariantów enuma.

Na przykład zmieńmy jeden z wariantów naszego enuma tak, aby przechowywał
w sobie dane. W latach 1999–2008 Stany Zjednoczone biły ćwierćdolarówki, które
na jednej stronie miały inny wzór dla każdego z 50 stanów. Żadne inne monety
nie dostały stanowych wzorów, więc tylko ćwierćdolarówki mają tę dodatkową
wartość. Możemy dodać tę informację do naszego `enum`, zmieniając wariant
`Quarter` tak, by przechowywał wartość `UsState`, co zrobiliśmy w listingu 6-4.

<Listing number="6-4" caption="Enum `Coin`, w którym wariant `Quarter` przechowuje też wartość `UsState`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-04/src/main.rs:here}}
```

</Listing>

Wyobraźmy sobie, że znajomy próbuje zebrać wszystkie 50 stanowych
ćwierćdolarówek. Sortując drobne według rodzaju monety, będziemy też podawać
nazwę stanu powiązanego z każdą ćwierćdolarówką, żeby znajomy mógł dodać ją do
kolekcji, jeśli jeszcze jej nie ma.

W wyrażeniu `match` w tym kodzie dodajemy do wzorca pasującego do wartości
wariantu `Coin::Quarter` zmienną o nazwie `state`. Gdy `Coin::Quarter` pasuje,
zmienna `state` zostanie związana z wartością stanu tej ćwierćdolarówki.
Następnie możemy użyć `state` w kodzie tego ramienia, o tak:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-09-variable-in-pattern/src/main.rs:here}}
```

Gdybyśmy wywołali `value_in_cents(Coin::Quarter(UsState::Alaska))`, `coin`
miałoby wartość `Coin::Quarter(UsState::Alaska)`. Gdy porównujemy tę wartość
z kolejnymi ramionami, żadne nie pasuje, dopóki nie dojdziemy do
`Coin::Quarter(state)`. W tym momencie `state` zostaje związane z wartością
`UsState::Alaska`. Możemy wtedy użyć tego wiązania w wyrażeniu `println!`,
wydobywając w ten sposób wewnętrzną wartość stanu z wariantu `Quarter` enuma
`Coin`.

<!-- Old headings. Do not remove or links may break. -->

<a id="matching-with-optiont"></a>

### Wzorzec `match` dla `Option<T>` {#the-optiont-match-pattern}


W poprzednim podrozdziale chcieliśmy wydobyć wewnętrzną wartość `T` z wariantu
`Some`, używając `Option<T>`; `Option<T>` możemy też obsłużyć za pomocą
`match`, tak jak zrobiliśmy to z enumem `Coin`! Zamiast monet będziemy
porównywać warianty `Option<T>`, ale wyrażenie `match` działa tak samo.

Załóżmy, że chcemy napisać funkcję, która przyjmuje `Option<i32>` i jeśli
w środku jest wartość, dodaje do niej 1. Jeśli w środku nie ma wartości,
funkcja powinna zwrócić wartość `None` i nie próbować wykonywać żadnych
operacji.

Dzięki `match` tę funkcję bardzo łatwo napisać – będzie wyglądać jak
w listingu 6-5.

<Listing number="6-5" caption="Funkcja używająca wyrażenia `match` na `Option<i32>`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:here}}
```

</Listing>

Przyjrzyjmy się dokładniej pierwszemu wywołaniu `plus_one`. Gdy wywołujemy
`plus_one(five)`, zmienna `x` w ciele `plus_one` będzie miała wartość
`Some(5)`. Następnie porównujemy ją z kolejnymi ramionami:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Wartość `Some(5)` nie pasuje do wzorca `None`, więc przechodzimy do następnego
ramienia:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:second_arm}}
```

Czy `Some(5)` pasuje do `Some(i)`? Tak! Mamy ten sam wariant. `i` zostaje
związane z wartością zawartą w `Some`, więc `i` przyjmuje wartość `5`. Następnie
wykonuje się kod ramienia, więc dodajemy 1 do wartości `i` i tworzymy nową
wartość `Some` z naszą sumą `6` w środku.

Rozważmy teraz drugie wywołanie `plus_one` w listingu 6-5, w którym `x` ma
wartość `None`. Wchodzimy do `match` i porównujemy z pierwszym ramieniem:

```rust,ignore
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-05/src/main.rs:first_arm}}
```

Pasuje! Nie ma wartości, do której można by coś dodać, więc program się
zatrzymuje i zwraca wartość `None` po prawej stronie `=>`. Ponieważ pasowało
pierwsze ramię, żadne inne ramiona nie są porównywane.

Łączenie `match` z enumami przydaje się w wielu sytuacjach. Ten wzorzec
zobaczysz w kodzie w Ruście bardzo często: `match` na enumie, związanie zmiennej
z danymi w środku, a potem wykonanie kodu na ich podstawie. Na początku bywa to
trochę zawiłe, ale gdy się przyzwyczaisz, zaczniesz żałować, że nie masz tego
we wszystkich językach. To niezmiennie jeden z ulubionych mechanizmów
użytkowników.

### Dopasowania są wyczerpujące {#matches-are-exhaustive}

Musimy omówić jeszcze jeden aspekt `match`: wzorce ramion muszą obejmować
wszystkie możliwości. Rozważ taką wersję naszej funkcji `plus_one`, która ma
błąd i się nie skompiluje:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/src/main.rs:here}}
```

Nie obsłużyliśmy przypadku `None`, więc ten kod spowoduje błąd. Na szczęście
to błąd, który Rust potrafi wychwycić. Jeśli spróbujemy skompilować ten kod,
otrzymamy taki błąd:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-10-non-exhaustive-match/output.txt}}
```

Rust wie, że nie uwzględniliśmy każdego możliwego przypadku, a nawet wie, o
którym wzorcu zapomnieliśmy! Dopasowania w Ruście są _wyczerpujące_
(*exhaustive*): musimy wyczerpać każdą możliwość, aby kod był poprawny.
Zwłaszcza w przypadku `Option<T>`: gdy Rust nie pozwala nam zapomnieć
o jawnym obsłużeniu przypadku `None`, chroni nas przed założeniem, że mamy
wartość, gdy w rzeczywistości możemy mieć null – i tym samym uniemożliwia
popełnienie omówionego wcześniej błędu wartego miliard dolarów.

### Wzorce przechwytujące wszystko i symbol zastępczy `_` {#catch-all-patterns-and-the-_-placeholder}

Używając enumów, możemy też wykonać specjalne działania dla kilku konkretnych
wartości, a dla wszystkich pozostałych – jedno działanie domyślne. Wyobraź
sobie, że implementujemy grę, w której po wyrzuceniu 3 na kostce twój gracz się
nie rusza, tylko dostaje nowy, wymyślny kapelusz. Po wyrzuceniu 7 gracz traci
wymyślny kapelusz. Przy wszystkich innych wartościach gracz przesuwa się o tyle
pól na planszy. Oto `match` implementujące tę logikę – wynik rzutu kostką jest
wpisany na sztywno zamiast losowany, a cała pozostała logika jest
reprezentowana przez funkcje bez ciał, bo ich faktyczna implementacja wykracza
poza ten przykład:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-15-binding-catchall/src/main.rs:here}}
```

W pierwszych dwóch ramionach wzorcami są literały `3` i `7`. W ostatnim
ramieniu, które obejmuje każdą inną możliwą wartość, wzorcem jest zmienna,
którą nazwaliśmy `other`. Kod wykonywany dla ramienia `other` używa tej
zmiennej, przekazując ją do funkcji `move_player`.

Ten kod się kompiluje, mimo że nie wymieniliśmy wszystkich możliwych wartości
typu `u8`, ponieważ ostatni wzorzec pasuje do wszystkich wartości, których nie
wymieniono wprost. Ten wzorzec przechwytujący wszystko (*catch-all*) spełnia
wymóg, by `match` było wyczerpujące. Zauważ, że ramię przechwytujące wszystko
musimy umieścić na końcu, ponieważ wzorce są sprawdzane po kolei. Gdybyśmy
umieścili je wcześniej, pozostałe ramiona nigdy by się nie wykonały, więc Rust
ostrzeże nas, jeśli dodamy ramiona po ramieniu przechwytującym wszystko!

Rust ma też wzorzec, którego możemy użyć, gdy chcemy przechwycić wszystko, ale
nie chcemy _używać_ wartości we wzorcu przechwytującym: `_` to specjalny
wzorzec, który pasuje do dowolnej wartości i nie wiąże się z nią. Mówi to
Rustowi, że nie zamierzamy używać tej wartości, więc Rust nie ostrzeże nas
o nieużywanej zmiennej.

Zmieńmy zasady gry: teraz, jeśli wyrzucisz cokolwiek innego niż 3 lub 7, musisz
rzucić ponownie. Nie potrzebujemy już wartości przechwytującej wszystko, więc
możemy zmienić kod tak, by zamiast zmiennej o nazwie `other` używał `_`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-16-underscore-catchall/src/main.rs:here}}
```

Ten przykład również spełnia wymóg wyczerpywalności, ponieważ w ostatnim
ramieniu jawnie ignorujemy wszystkie pozostałe wartości; o niczym nie
zapomnieliśmy.

Na koniec zmienimy zasady gry jeszcze raz: jeśli wyrzucisz cokolwiek innego niż
3 lub 7, w twojej turze nic się nie dzieje. Możemy to wyrazić, używając
wartości jednostkowej (*unit*; to typ pustej krotki, o którym wspominaliśmy
w podrozdziale [„Typ krotki”][tuples]<!-- ignore -->) jako kodu ramienia `_`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-17-underscore-unit/src/main.rs:here}}
```

Mówimy tu Rustowi wprost, że nie zamierzamy używać żadnej innej wartości,
która nie pasuje do wzorca we wcześniejszym ramieniu, i że w takim przypadku
nie chcemy wykonywać żadnego kodu.

Więcej o wzorcach i dopasowywaniu powiemy w
[rozdziale 19][ch19-00-patterns]<!-- ignore -->.

<!-- BEGIN INTERVENTION: 1e4f082c-ffa4-4d33-8726-2dbcd72e1aa2 -->
### Jak dopasowania współdziałają z własnością {#how-matches-interact-with-ownership}

Jeśli enum zawiera dane, których nie da się kopiować, np. String, musisz uważać, czy `match` przeniesie (*move*) te dane, czy je pożyczy (*borrow*). Na przykład ten program używający `Option<String>` się skompiluje:

```aquascope,permissions,stepper,boundaries
# fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

match opt {
    Some(_) => println!("Some!"),
    None => println!("None!")
};

println!("{:?}", opt);
# }
```

Jeśli jednak w `Some(_)` zamienimy symbol zastępczy (*placeholder*) na nazwę zmiennej, np. `Some(s)`, program się NIE skompiluje:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

match opt {
    // _ became s
    Some(s) => println!("Some: {}", s),
    None => println!("None!")
};

println!("{:?}", opt);`{}`
#}
```


`opt` to zwykły enum &mdash; jego typem jest `Option<String>`, a nie referencja, taka jak `&Option<String>`. Dlatego `match` na `opt` przeniesie nieignorowane pola, takie jak `s`. Zwróć uwagę, że w drugim programie `opt` wcześniej niż w pierwszym traci uprawnienia (*permissions*) do odczytu i własności. Po wyrażeniu `match` dane wewnątrz `opt` zostały przeniesione, więc odczytanie `opt` w `println` jest niedozwolone.

Jeśli chcemy zajrzeć do `opt` bez przenoszenia jego zawartości, idiomatycznym rozwiązaniem jest dopasowanie na referencji:

```aquascope,permissions,stepper,boundaries
#fn main() {
let opt: Option<String> = 
    Some(String::from("Hello world"));

// opt became &opt
match &opt {
    Some(s) => println!("Some: {}", s),
    None => println!("None!")
};

println!("{:?}", opt);
#}
```

Rust „przepycha w dół” referencję z zewnętrznego enuma, `&Option<String>`, do wewnętrznego pola, `&String`. Dlatego `s` ma typ `&String`, a `opt` można użyć po `match`. Aby lepiej zrozumieć ten mechanizm „przepychania w dół”, zajrzyj do sekcji o [trybach wiązania](https://doc.rust-lang.org/reference/patterns.html#binding-modes) w dokumentacji Rust Reference.
<!-- END INTERVENTION -->

{{#quiz ../quizzes/ch06-02-match.toml}}

[tuples]: ch03-02-data-types.html#the-tuple-type

[ch19-00-patterns]: ch19-00-patterns.html

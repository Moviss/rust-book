## Zwięzły przepływ sterowania z `if let` i `let...else` {#concise-control-flow-with-if-let-and-letelse}

Składnia `if let` pozwala połączyć `if` i `let` w mniej rozwlekły sposób obsługi
wartości pasujących do jednego wzorca z pominięciem pozostałych. Weźmy program
z listingu 6-6, który dopasowuje wartość typu `Option<u8>` w zmiennej
`config_max`, ale chce wykonać kod tylko wtedy, gdy wartość jest wariantem
`Some`.

<Listing number="6-6" caption="Wyrażenie `match`, które wykonuje kod tylko wtedy, gdy wartość to `Some`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-06/src/main.rs:here}}
```

</Listing>

Jeśli wartość to `Some`, wypisujemy wartość z wariantu `Some`, wiążąc ją we
wzorcu ze zmienną `max`. Z wartością `None` nie chcemy nic robić. Aby zadowolić
wyrażenie `match`, po obsłużeniu tylko jednego wariantu musimy dopisać
`_ => ()`, a dodawanie takiego szablonowego kodu (*boilerplate*) jest irytujące.

Zamiast tego możemy zapisać to krócej za pomocą `if let`. Poniższy kod działa
tak samo jak `match` z listingu 6-6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-12-if-let/src/main.rs:here}}
```

Składnia `if let` przyjmuje wzorzec i wyrażenie rozdzielone znakiem równości.
Działa tak samo jak `match`: wyrażenie zostaje przekazane do `match`, a wzorzec
jest jego pierwszym ramieniem (*arm*). W tym przykładzie wzorcem jest
`Some(max)`, a `max` zostaje związane z wartością wewnątrz `Some`. Możemy wtedy
użyć `max` w ciele bloku `if let` tak samo, jak używaliśmy `max` w odpowiednim
ramieniu `match`. Kod w bloku `if let` wykonuje się tylko wtedy, gdy wartość
pasuje do wzorca.

Użycie `if let` oznacza mniej pisania, mniej wcięć i mniej szablonowego kodu.
Tracisz jednak sprawdzanie wyczerpywalności (*exhaustive checking*), które
wymusza `match` i które gwarantuje, że nie zapomnisz obsłużyć żadnego przypadku.
Wybór między `match` a `if let` zależy od tego, co robisz w konkretnej sytuacji,
i od tego, czy zysk w zwięzłości jest wart utraty sprawdzania wyczerpywalności.

Innymi słowy, `if let` możesz traktować jako lukier składniowy dla wyrażenia
`match`, które wykonuje kod, gdy wartość pasuje do jednego wzorca, a wszystkie
pozostałe wartości ignoruje.

Do `if let` możemy dołączyć `else`. Blok kodu po `else` jest taki sam jak blok
kodu, który należałby do przypadku `_` w wyrażeniu `match` równoważnym
konstrukcji `if let` z `else`. Przypomnij sobie definicję *enuma* (typu
wyliczeniowego) `Coin` z listingu 6-4, w której wariant `Quarter` przechowywał
także wartość `UsState`. Gdybyśmy chcieli policzyć wszystkie napotkane monety
inne niż ćwierćdolarówki, a jednocześnie ogłaszać, z jakiego stanu pochodzą
ćwierćdolarówki, moglibyśmy to zrobić za pomocą wyrażenia `match`, o tak:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-13-count-and-announce-match/src/main.rs:here}}
```

Albo moglibyśmy użyć wyrażenia `if let` z `else`, o tak:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-14-count-and-announce-if-let-else/src/main.rs:here}}
```

## Pozostawanie na „szczęśliwej ścieżce” z `let...else` {#staying-on-the-happy-path-with-letelse}

Często spotykany wzorzec postępowania polega na wykonaniu jakichś obliczeń, gdy
wartość jest obecna, a w przeciwnym razie zwróceniu wartości domyślnej.
Kontynuując przykład monet z wartością `UsState`: gdybyśmy chcieli powiedzieć
coś zabawnego w zależności od tego, jak stary jest stan z ćwierćdolarówki,
moglibyśmy dodać do `UsState` metodę sprawdzającą wiek stanu, na przykład tak:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:state}}
```

Następnie moglibyśmy użyć `if let`, aby dopasować rodzaj monety, wprowadzając
zmienną `state` w ciele warunku, jak w listingu 6-7.

<Listing number="6-7" caption="Sprawdzanie, czy stan istniał w 1900 roku, za pomocą instrukcji warunkowych zagnieżdżonych w `if let`">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-07/src/main.rs:describe}}
```

</Listing>

To działa, ale cała praca trafiła do ciała instrukcji `if let`, a jeśli to, co
trzeba zrobić, jest bardziej skomplikowane, trudno może być prześledzić, jak
dokładnie mają się do siebie gałęzie najwyższego poziomu. Moglibyśmy też
wykorzystać to, że wyrażenia dają wartość: albo uzyskać `state` z `if let`,
albo wcześniej wyjść z funkcji, jak w listingu 6-8. (Coś podobnego dałoby się
zrobić także z `match`).

<Listing number="6-8" caption="Użycie `if let` do uzyskania wartości albo wcześniejszego wyjścia z funkcji">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-08/src/main.rs:describe}}
```

</Listing>

Ale i to na swój sposób trudno się śledzi! Jedna gałąź `if let` daje wartość,
a druga całkowicie wychodzi z funkcji.

Aby ten częsty wzorzec dało się wyrazić zgrabniej, Rust ma `let...else`.
Składnia `let...else` przyjmuje wzorzec po lewej stronie i wyrażenie po prawej,
bardzo podobnie jak `if let`, ale nie ma gałęzi `if`, tylko gałąź `else`. Jeśli
wzorzec pasuje, wartość z wzorca zostanie związana w zewnętrznym zasięgu
(*scope*). Jeśli wzorzec _nie_ pasuje, program przejdzie do ramienia `else`,
które musi wyjść z funkcji.

W listingu 6-9 widać, jak wygląda listing 6-8 po użyciu `let...else` zamiast
`if let`.

<Listing number="6-9" caption="Użycie `let...else` dla czytelniejszego przepływu przez funkcję">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-09/src/main.rs:describe}}
```

</Listing>

Zauważ, że w ten sposób główne ciało funkcji pozostaje na „szczęśliwej ścieżce”
(*happy path*), a przepływ sterowania (*control flow*) w obu gałęziach nie
różni się tak znacząco, jak w przypadku `if let`.

Jeśli trafisz na sytuację, w której logika programu jest zbyt rozwlekła, by
wyrazić ją za pomocą `match`, pamiętaj, że w Ruście masz do dyspozycji także
`if let` i `let...else`.

{{#quiz ../quizzes/ch06-03-if-let.toml}}

## Podsumowanie {#summary}

Omówiliśmy, jak za pomocą enumów tworzyć własne typy, których wartość może być
jedną z wyliczonego zbioru wartości. Pokazaliśmy, jak typ `Option<T>` z
biblioteki standardowej pomaga wykorzystać system typów do zapobiegania błędom.
Gdy wartości enuma zawierają dane, możesz je wydobyć i użyć za pomocą `match`
lub `if let`, w zależności od tego, ile przypadków musisz obsłużyć.

Twoje programy w Ruście potrafią teraz wyrażać pojęcia z twojej dziedziny za
pomocą struktur (*struct*) i enumów. Tworzenie własnych typów do użycia w API zapewnia
bezpieczeństwo typów: kompilator dopilnuje, aby każda funkcja otrzymywała tylko
wartości oczekiwanego przez nią typu.

Aby udostępnić użytkownikom dobrze zorganizowane API, proste w użyciu i
udostępniające dokładnie to, czego będą potrzebować, przejdźmy teraz do modułów
Rusta.

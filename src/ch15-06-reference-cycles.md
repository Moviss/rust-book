## Cykle referencji mogą powodować wycieki pamięci {#reference-cycles-can-leak-memory}

Gwarancje bezpieczeństwa pamięci w Ruście utrudniają, ale nie uniemożliwiają,
przypadkowe utworzenie pamięci, która nigdy nie zostanie posprzątana (nazywa się
to _wyciekiem pamięci_). Całkowite zapobieganie wyciekom pamięci nie należy do
gwarancji Rusta, co oznacza, że wycieki pamięci są w Ruście bezpieczne z punktu
widzenia pamięci. Możemy się przekonać, że Rust dopuszcza wycieki pamięci,
używając `Rc<T>` i `RefCell<T>`: da się utworzyć referencje (*references*), w
których elementy odwołują się do siebie nawzajem w cyklu. Powoduje to wyciek
pamięci, ponieważ licznik referencji każdego elementu w cyklu nigdy nie spadnie
do 0, a wartości nigdy nie zostaną zwolnione (*drop*).

### Tworzenie cyklu referencji {#creating-a-reference-cycle}

Zobaczmy, jak może powstać cykl referencji i jak temu zapobiec, zaczynając od
definicji *enuma* (typu wyliczeniowego) `List` i metody `tail` w listingu 15-25.

<Listing number="15-25" file-name="src/main.rs" caption="Definicja listy cons, która przechowuje `RefCell<T>`, dzięki czemu możemy zmienić to, na co wskazuje wariant `Cons`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-25/src/main.rs:here}}
```

</Listing>

Używamy kolejnej odmiany definicji `List` z listingu 15-5. Drugi element
wariantu `Cons` ma teraz typ `RefCell<Rc<List>>`, co oznacza, że zamiast
możliwości modyfikowania wartości `i32`, jak w listingu 15-24, chcemy
modyfikować wartość `List`, na którą wskazuje wariant `Cons`. Dodajemy też
metodę `tail`, aby wygodnie sięgać do drugiego elementu, gdy mamy wariant
`Cons`.

W listingu 15-26 dodajemy funkcję `main`, która korzysta z definicji z listingu
15-25. Ten kod tworzy listę w `a` oraz listę w `b`, która wskazuje na listę w
`a`. Następnie modyfikuje listę w `a` tak, aby wskazywała na `b`, tworząc cykl
referencji. Po drodze umieściliśmy instrukcje `println!`, które pokazują, ile
wynoszą liczniki referencji w różnych momentach tego procesu.

<Listing number="15-26" file-name="src/main.rs" caption="Tworzenie cyklu referencji z dwóch wartości `List` wskazujących na siebie nawzajem">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-26/src/main.rs:here}}
```

</Listing>

Tworzymy instancję `Rc<List>` przechowującą wartość `List` w zmiennej `a`, z
początkową listą `5, Nil`. Następnie tworzymy instancję `Rc<List>`
przechowującą inną wartość `List` w zmiennej `b`, która zawiera wartość `10` i
wskazuje na listę w `a`.

Modyfikujemy `a` tak, aby zamiast na `Nil` wskazywała na `b`, tworząc cykl.
Robimy to, używając metody `tail`, by uzyskać referencję do
`RefCell<Rc<List>>` w `a`, którą umieszczamy w zmiennej `link`. Następnie
wywołujemy metodę `borrow_mut` na `RefCell<Rc<List>>`, aby zmienić wartość w
środku z `Rc<List>` przechowującego wartość `Nil` na `Rc<List>` z `b`.

Gdy uruchomimy ten kod, pozostawiając na razie ostatnie `println!` w
komentarzu, otrzymamy następujące wyjście:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-26/output.txt}}
```

Po zmianie listy w `a` tak, by wskazywała na `b`, licznik referencji instancji
`Rc<List>` zarówno w `a`, jak i w `b` wynosi 2. Na końcu `main` Rust zwalnia
zmienną `b`, co zmniejsza licznik referencji instancji `Rc<List>` z `b` z 2
do 1. Pamięć, którą ta instancja `Rc<List>` zajmuje na stercie (*heap*), nie
zostanie w tym momencie zwolniona, ponieważ jej licznik referencji wynosi 1, a
nie 0. Następnie Rust zwalnia `a`, co zmniejsza licznik referencji instancji `Rc<List>` z `a`
również z 2 do 1. Pamięci tej instancji także nie da się zwolnić, ponieważ
druga instancja `Rc<List>` wciąż się do niej odwołuje. Pamięć zaalokowana na
listę na zawsze pozostanie nieposprzątana. Aby zobrazować ten cykl referencji,
przygotowaliśmy diagram na rysunku 15-4.

<img alt="Prostokąt oznaczony „a”, który wskazuje na prostokąt zawierający liczbę całkowitą 5. Prostokąt oznaczony „b”, który wskazuje na prostokąt zawierający liczbę całkowitą 10. Prostokąt zawierający 5 wskazuje na prostokąt zawierający 10, a prostokąt zawierający 10 wskazuje z powrotem na prostokąt zawierający 5, tworząc cykl." src="img/trpl15-04.svg" class="center" />

<span class="caption">Rysunek 15-4: Cykl referencji list `a` i `b` wskazujących
na siebie nawzajem</span>

Jeśli usuniesz komentarz z ostatniego `println!` i uruchomisz program, Rust
spróbuje wypisać ten cykl, w którym `a` wskazuje na `b`, które wskazuje na `a`
i tak dalej, aż do przepełnienia stosu (*stack*).

W porównaniu z prawdziwym programem skutki utworzenia cyklu referencji w tym
przykładzie nie są zbyt poważne: zaraz po utworzeniu cyklu program się kończy.
Gdyby jednak bardziej złożony program zaalokował w cyklu dużo pamięci i
trzymał ją przez długi czas, zużywałby więcej pamięci, niż potrzebuje, i mógłby
przeciążyć system, doprowadzając do wyczerpania dostępnej pamięci.

Utworzenie cyklu referencji nie jest łatwe, ale nie jest też niemożliwe. Jeśli
masz wartości `RefCell<T>` zawierające wartości `Rc<T>` albo podobne
zagnieżdżone kombinacje typów z wewnętrzną mutowalnością
(*interior mutability*) i zliczaniem referencji (*reference counting*), musisz
pilnować, by nie tworzyć cykli; nie możesz liczyć na to, że Rust je wykryje.
Utworzenie cyklu referencji byłoby błędem logicznym w twoim programie, który
należy minimalizować za pomocą testów automatycznych, przeglądów kodu i innych
praktyk wytwarzania oprogramowania.

Innym sposobem unikania cykli referencji jest przeorganizowanie struktur danych
tak, aby niektóre referencje wyrażały własność (*ownership*), a inne nie. Dzięki
temu możesz mieć cykle złożone częściowo z relacji własności, a częściowo z relacji
niewyrażających własności, a tylko relacje własności wpływają na to, czy wartość
może zostać zwolniona. W listingu 15-25 zawsze chcemy, aby warianty `Cons` były
właścicielami swojej listy, więc przeorganizowanie struktury danych nie jest
możliwe. Przyjrzyjmy się przykładowi z grafami złożonymi z węzłów-rodziców i
węzłów-dzieci, aby zobaczyć, kiedy relacje niewyrażające własności są właściwym
sposobem zapobiegania cyklom referencji.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-reference-cycles-turning-an-rct-into-a-weakt"></a>

### Zapobieganie cyklom referencji za pomocą `Weak<T>` {#preventing-reference-cycles-using-weakt}

Do tej pory pokazaliśmy, że wywołanie `Rc::clone` zwiększa `strong_count`
instancji `Rc<T>`, a instancja `Rc<T>` jest sprzątana tylko wtedy, gdy jej
`strong_count` wynosi 0. Możesz też utworzyć słabą referencję do wartości
wewnątrz instancji `Rc<T>`, wywołując `Rc::downgrade` i przekazując referencję
do `Rc<T>`. *Silne referencje* (*strong references*) to sposób na współdzielenie
własności instancji `Rc<T>`. *Słabe referencje* (*weak references*) nie wyrażają
relacji własności, a ich liczba nie wpływa na to, kiedy instancja `Rc<T>`
zostanie posprzątana. Nie spowodują cyklu referencji, ponieważ każdy cykl
obejmujący jakieś słabe referencje zostanie przerwany, gdy licznik silnych
referencji wartości w nim uczestniczących spadnie do 0.

Gdy wywołujesz `Rc::downgrade`, dostajesz inteligentny wskaźnik
(*smart pointer*) typu `Weak<T>`. Zamiast zwiększać o 1 `strong_count` w
instancji `Rc<T>`, wywołanie `Rc::downgrade` zwiększa o 1 `weak_count`. Typ `Rc<T>`
używa `weak_count` do śledzenia, ile istnieje referencji `Weak<T>`, podobnie
jak w przypadku `strong_count`. Różnica polega na tym, że `weak_count` nie musi
wynosić 0, aby instancja `Rc<T>` została posprzątana.

Ponieważ wartość, do której odwołuje się `Weak<T>`, mogła już zostać zwolniona,
przed zrobieniem czegokolwiek z wartością wskazywaną przez `Weak<T>` musisz
upewnić się, że ta wartość nadal istnieje. Zrób to, wywołując na instancji `Weak<T>`
metodę `upgrade`, która zwraca `Option<Rc<T>>`. Otrzymasz wynik `Some`, jeśli
wartość `Rc<T>` nie została jeszcze zwolniona, i wynik `None`, jeśli wartość
`Rc<T>` została już zwolniona. Ponieważ `upgrade` zwraca `Option<Rc<T>>`, Rust
dopilnuje, aby obsłużono zarówno przypadek `Some`, jak i `None`, i nie powstanie
nieprawidłowy wskaźnik.

Jako przykład zamiast listy, której elementy znają tylko następny element,
utworzymy drzewo, którego elementy znają swoje elementy-dzieci _oraz_ swoje
elementy-rodziców.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-tree-data-structure-a-node-with-child-nodes"></a>

#### Tworzenie struktury danych drzewa {#creating-a-tree-data-structure}

Na początek zbudujemy drzewo z węzłami, które znają swoje węzły-dzieci.
Utworzymy strukturę (*struct*) o nazwie `Node`, która przechowuje własną
wartość `i32` oraz referencje do swoich wartości-dzieci typu `Node`:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:here}}
```

Chcemy, aby `Node` był właścicielem swoich dzieci, i chcemy współdzielić tę
własność ze zmiennymi, aby mieć bezpośredni dostęp do każdego `Node` w drzewie.
W tym celu definiujemy elementy `Vec<T>` jako wartości typu `Rc<Node>`. Chcemy
też móc modyfikować, które węzły są dziećmi innego węzła, dlatego w `children`
mamy `RefCell<T>` opakowujący `Vec<Rc<Node>>`.

Następnie użyjemy naszej definicji struktury i utworzymy jedną instancję `Node`
o nazwie `leaf` z wartością `3` i bez dzieci oraz drugą instancję o nazwie
`branch` z wartością `5` i `leaf` jako jednym z jej dzieci, jak pokazano w
listingu 15-27.

<Listing number="15-27" file-name="src/main.rs" caption="Tworzenie węzła `leaf` bez dzieci i węzła `branch`, którego jednym z dzieci jest `leaf`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-27/src/main.rs:there}}
```

</Listing>

Klonujemy `Rc<Node>` z `leaf` i zapisujemy go w `branch`, co oznacza, że `Node`
w `leaf` ma teraz dwóch właścicieli: `leaf` i `branch`. Z `branch` możemy
dostać się do `leaf` przez `branch.children`, ale nie ma sposobu, by dostać się
z `leaf` do `branch`. Powodem jest to, że `leaf` nie ma referencji do `branch`
i nie wie, że są ze sobą powiązane. Chcemy, aby `leaf` wiedział, że `branch`
jest jego rodzicem. Zajmiemy się tym teraz.

#### Dodawanie referencji od dziecka do rodzica {#adding-a-reference-from-a-child-to-its-parent}

Aby węzeł-dziecko wiedział o swoim rodzicu, musimy dodać pole `parent` do
definicji struktury `Node`. Problem polega na tym, jaki typ powinno mieć
`parent`. Wiemy, że nie może zawierać `Rc<T>`, ponieważ utworzyłoby to cykl
referencji: `leaf.parent` wskazywałoby na `branch`, a `branch.children` na
`leaf`, przez co ich wartości `strong_count` nigdy nie spadłyby do 0.

Patrząc na te relacje inaczej: węzeł-rodzic powinien być właścicielem swoich
dzieci – jeśli węzeł-rodzic zostanie zwolniony, jego węzły-dzieci też powinny
zostać zwolnione. Dziecko nie powinno jednak być właścicielem swojego rodzica –
jeśli zwolnimy węzeł-dziecko, rodzic nadal powinien istnieć. To zadanie dla
słabych referencji!

Zamiast `Rc<T>` sprawimy więc, że typ `parent` będzie używał `Weak<T>`, a
konkretnie `RefCell<Weak<Node>>`. Teraz definicja naszej struktury `Node`
wygląda tak:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:here}}
```

Węzeł będzie mógł odwoływać się do swojego węzła-rodzica, ale nie będzie jego
właścicielem. W listingu 15-28 aktualizujemy `main`, aby korzystał z nowej
definicji, dzięki czemu węzeł `leaf` będzie mógł odwołać się do swojego
rodzica, `branch`.

<Listing number="15-28" file-name="src/main.rs" caption="Węzeł `leaf` ze słabą referencją do swojego węzła-rodzica `branch`">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-28/src/main.rs:there}}
```

</Listing>

Tworzenie węzła `leaf` wygląda podobnie jak w listingu 15-27, z wyjątkiem pola
`parent`: `leaf` początkowo nie ma rodzica, więc tworzymy nową, pustą instancję
referencji `Weak<Node>`.

W tym momencie, gdy spróbujemy uzyskać referencję do rodzica `leaf` za pomocą
metody `upgrade`, dostaniemy wartość `None`. Widać to w wyjściu pierwszej
instrukcji `println!`:

```text
leaf parent = None
```

Gdy utworzymy węzeł `branch`, on również będzie miał w polu `parent` nową
referencję `Weak<Node>`, ponieważ `branch` nie ma węzła-rodzica. Nadal mamy
`leaf` jako jedno z dzieci `branch`. Gdy mamy już instancję `Node` w `branch`,
możemy zmodyfikować `leaf`, aby dać mu referencję `Weak<Node>` do jego rodzica.
Używamy metody `borrow_mut` na `RefCell<Weak<Node>>` w polu `parent` węzła
`leaf`, a następnie funkcji `Rc::downgrade`, aby utworzyć referencję
`Weak<Node>` do `branch` z `Rc<Node>` w `branch`.

Gdy ponownie wypiszemy rodzica `leaf`, tym razem dostaniemy wariant `Some`
zawierający `branch`: teraz `leaf` ma dostęp do swojego rodzica! Wypisując
`leaf`, unikamy też cyklu, który w listingu 15-26 kończył się ostatecznie
przepełnieniem stosu; referencje `Weak<Node>` są wypisywane jako `(Weak)`:

```text
leaf parent = Some(Node { value: 5, parent: RefCell { value: (Weak) },
children: RefCell { value: [Node { value: 3, parent: RefCell { value: (Weak) },
children: RefCell { value: [] } }] } })
```

Brak nieskończonego wyjścia oznacza, że ten kod nie utworzył cyklu referencji.
Możemy to stwierdzić także na podstawie wartości zwracanych przez wywołania
`Rc::strong_count` i `Rc::weak_count`.

#### Obserwowanie zmian `strong_count` i `weak_count` {#visualizing-changes-to-strong_count-and-weak_count}

Zobaczmy, jak zmieniają się wartości `strong_count` i `weak_count` instancji
`Rc<Node>`, gdy utworzymy nowy wewnętrzny zasięg (*scope*) i przeniesiemy do
niego tworzenie `branch`. Dzięki temu zobaczymy, co się dzieje, gdy `branch`
zostaje utworzony, a potem zwolniony, gdy wychodzi poza zasięg. Zmiany pokazano
w listingu 15-29.

<Listing number="15-29" file-name="src/main.rs" caption="Tworzenie `branch` w wewnętrznym zasięgu i sprawdzanie liczników silnych i słabych referencji">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-29/src/main.rs:here}}
```

</Listing>

Po utworzeniu `leaf` jego `Rc<Node>` ma licznik silnych referencji równy 1 i
licznik słabych referencji równy 0. W wewnętrznym zasięgu tworzymy `branch` i
wiążemy go z `leaf`; gdy w tym momencie wypiszemy liczniki, `Rc<Node>` w
`branch` będzie miał licznik silnych referencji równy 1 i licznik słabych
referencji równy 1 (bo `leaf.parent` wskazuje na `branch` przez `Weak<Node>`).
Gdy wypiszemy liczniki w `leaf`, zobaczymy, że licznik silnych referencji
wynosi 2, ponieważ `branch` przechowuje teraz w `branch.children` klon
`Rc<Node>` z `leaf`, ale licznik słabych referencji nadal wynosi 0.

Gdy wewnętrzny zasięg się kończy, `branch` wychodzi poza zasięg, a licznik silnych
referencji `Rc<Node>` spada do 0, więc jego `Node` zostaje zwolniony. Licznik
słabych referencji równy 1, pochodzący od `leaf.parent`, nie ma wpływu na to,
czy `Node` zostanie zwolniony, więc nie mamy żadnych wycieków pamięci!

Jeśli po końcu zasięgu spróbujemy dostać się do rodzica `leaf`, znów dostaniemy
`None`. Na końcu programu `Rc<Node>` w `leaf` ma licznik silnych referencji
równy 1 i licznik słabych referencji równy 0, ponieważ zmienna `leaf` jest
teraz znowu jedyną referencją do `Rc<Node>`.

Cała logika zarządzająca licznikami i zwalnianiem wartości jest wbudowana w
`Rc<T>` i `Weak<T>` oraz w ich implementacje *traitu* (cechy typu, zbliżonej do
interfejsu) `Drop`. Określając w definicji `Node`, że relacja od dziecka do
rodzica ma być referencją `Weak<T>`, możesz sprawić, że węzły-rodzice wskazują
na węzły-dzieci i odwrotnie, nie tworząc przy tym cyklu referencji ani wycieków
pamięci.

## Podsumowanie {#summary}

W tym rozdziale omówiliśmy, jak używać inteligentnych wskaźników, aby uzyskać
inne gwarancje i kompromisy niż te, które Rust domyślnie zapewnia dla zwykłych
referencji. Typ `Box<T>` ma znany rozmiar i wskazuje na dane zaalokowane na
stercie. Typ `Rc<T>` śledzi liczbę referencji do danych na stercie, dzięki
czemu dane mogą mieć wielu właścicieli. Typ `RefCell<T>`, dzięki swojej
wewnętrznej mutowalności, daje nam typ, którego możemy użyć, gdy potrzebujemy
typu niemutowalnego (*immutable*), ale musimy zmienić znajdującą się w nim
wartość; ponadto egzekwuje on reguły pożyczania (*borrowing*) w czasie działania,
a nie w czasie kompilacji (*compile-time*).

Omówiliśmy też traity `Deref` i `Drop`, na których opiera się znaczna część
funkcjonalności inteligentnych wskaźników. Przyjrzeliśmy się cyklom referencji,
które mogą powodować wycieki pamięci, oraz temu, jak im zapobiegać za pomocą
`Weak<T>`.

Jeśli ten rozdział wzbudził twoje zainteresowanie i chcesz zaimplementować
własne inteligentne wskaźniki, zajrzyj do [„The Rustonomicon”][nomicon], gdzie
znajdziesz więcej przydatnych informacji.

W następnym rozdziale zajmiemy się współbieżnością (*concurrency*) w Ruście.
Poznasz nawet kilka nowych inteligentnych wskaźników.

{{#quiz ../quizzes/ch15-06-reference-cycles.toml}}

[nomicon]: https://doc.rust-lang.org/nomicon/index.html

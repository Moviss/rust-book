## Używanie `Box<T>` do wskazywania na dane na stercie {#using-boxt-to-point-to-data-on-the-heap}

Najprostszym inteligentnym wskaźnikiem (*smart pointer*) jest *box* (wskaźnik
na dane umieszczone na stercie), którego typ zapisujemy jako `Box<T>`. _Boxy_
pozwalają przechowywać dane na stercie (*heap*) zamiast na stosie (*stack*). Na stosie pozostaje wskaźnik do danych na stercie. Różnicę między
stosem a stertą możesz sobie przypomnieć w rozdziale 4.

Boxy nie wiążą się z narzutem wydajnościowym, poza tym że przechowują dane na
stercie zamiast na stosie. Nie mają jednak też wielu dodatkowych możliwości.
Najczęściej będziesz ich używać w takich sytuacjach:

- gdy masz typ, którego rozmiaru nie da się poznać w czasie kompilacji
  (*compile-time*), a chcesz użyć wartości tego typu w kontekście, który
  wymaga dokładnego rozmiaru;
- gdy masz dużą ilość danych i chcesz przenieść własność (*ownership*), ale
  mieć pewność, że dane nie zostaną przy tym skopiowane;
- gdy chcesz być właścicielem wartości i zależy ci tylko na tym, by jej typ
  implementował określony *trait* (cecha typu, zbliżona do interfejsu), a nie
  na tym, by był konkretnym typem.

Pierwszą sytuację pokażemy w podrozdziale [„Umożliwianie typów rekurencyjnych
za pomocą boxów”](#enabling-recursive-types-with-boxes)<!-- ignore -->. W
drugim przypadku przeniesienie (*move*) własności dużej ilości danych może
trwać długo, ponieważ dane są kopiowane na stosie. Aby w takiej sytuacji
poprawić wydajność, możemy przechować dużą ilość danych na stercie w boxie.
Wtedy na stosie kopiowana jest tylko niewielka ilość danych wskaźnika, a dane,
do których się odnosi, pozostają w jednym miejscu na stercie. Trzeci przypadek
nazywamy _obiektem traitu_ (*trait object*), a w rozdziale 18 poświęcony jest
mu podrozdział [„Używanie obiektów traitów do abstrahowania wspólnego
zachowania”][trait-objects]<!-- ignore -->. To, czego się tu nauczysz,
zastosujesz więc ponownie w tamtym podrozdziale!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-store-data-on-the-heap"></a>

### Przechowywanie danych na stercie {#storing-data-on-the-heap}

Zanim omówimy zastosowanie `Box<T>` do przechowywania danych na stercie,
przedstawimy składnię oraz sposób pracy z wartościami przechowywanymi w
`Box<T>`.

Listing 15-1 pokazuje, jak użyć boxa do przechowania wartości `i32` na stercie.

<Listing number="15-1" file-name="src/main.rs" caption="Przechowywanie wartości `i32` na stercie za pomocą boxa">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-01/src/main.rs}}
```

</Listing>

Definiujemy zmienną `b`, której wartością jest `Box` wskazujący na wartość `5`,
zaalokowaną na stercie. Ten program wypisze `b = 5`; w tym przypadku możemy
uzyskać dostęp do danych w boxie podobnie, jak gdyby te dane znajdowały się na
stosie. Tak jak każda wartość będąca właścicielem swoich danych, box po wyjściu
poza zasięg (*scope*), co dzieje się z `b` na końcu `main`, zostanie
zdealokowany. Dealokacja obejmuje zarówno sam box (przechowywany na stosie), jak
i dane, na które wskazuje (przechowywane na stercie).

Umieszczanie pojedynczej wartości na stercie nie jest zbyt przydatne, więc
rzadko będziesz w ten sposób używać samych boxów. W większości sytuacji
bardziej odpowiednie jest trzymanie wartości takich jak pojedynczy `i32` na
stosie, gdzie są domyślnie przechowywane. Przyjrzyjmy się przypadkowi, w którym
boxy pozwalają nam definiować typy, których bez boxów nie moglibyśmy
zdefiniować.

### Umożliwianie typów rekurencyjnych za pomocą boxów {#enabling-recursive-types-with-boxes}

Wartość _typu rekurencyjnego_ (*recursive type*) może zawierać jako swoją część
inną wartość tego samego typu. Typy rekurencyjne stanowią problem, ponieważ Rust
musi w czasie kompilacji wiedzieć, ile miejsca zajmuje dany typ. Zagnieżdżanie
wartości typów rekurencyjnych mogłoby jednak teoretycznie trwać w
nieskończoność, więc Rust nie może wiedzieć, ile miejsca potrzebuje wartość.
Ponieważ boxy mają znany rozmiar, możemy umożliwić typy rekurencyjne, wstawiając
box do definicji typu rekurencyjnego.

Jako przykład typu rekurencyjnego zbadajmy listę cons. To typ danych często
spotykany w funkcyjnych językach programowania. Typ listy cons, który
zdefiniujemy, jest prosty, jeśli pominąć rekurencję; dlatego koncepcje z
przykładu, nad którym będziemy pracować, przydadzą się zawsze, gdy trafisz na
bardziej złożone sytuacje związane z typami rekurencyjnymi.

<!-- Old headings. Do not remove or links may break. -->

<a id="more-information-about-the-cons-list"></a>

#### Czym jest lista cons {#understanding-the-cons-list}

_Lista cons_ (*cons list*) to struktura danych wywodząca się z języka
programowania Lisp i jego dialektów, złożona z zagnieżdżonych par; jest to
lispowa wersja listy powiązanej (*linked list*). Jej nazwa pochodzi od funkcji
`cons` (skrót od _construct function_, czyli „funkcja konstruująca”) w Lispie,
która konstruuje nową parę ze swoich dwóch argumentów. Wywołując `cons` na
parze złożonej z wartości i innej pary, możemy konstruować listy cons złożone z
rekurencyjnych par.

Oto na przykład zapis w pseudokodzie listy cons zawierającej listę `1, 2, 3`,
w którym każda para jest ujęta w nawiasy:

```text
(1, (2, (3, Nil)))
```

Każdy element listy cons zawiera dwie rzeczy: wartość bieżącego elementu oraz
następny element. Ostatni element listy zawiera tylko wartość o nazwie `Nil`,
bez następnego elementu. Listę cons tworzy się przez rekurencyjne wywoływanie
funkcji `cons`. Kanoniczną nazwą oznaczającą przypadek bazowy rekurencji jest
`Nil`. Zauważ, że nie jest to to samo, co koncepcja „null” czy „nil” omówiona w
rozdziale 6, czyli wartość nieprawidłowa lub nieobecna.

Lista cons nie jest w Ruście często używaną strukturą danych. Gdy w Ruście
masz listę elementów, zwykle lepszym wyborem jest `Vec<T>`. Inne, bardziej
złożone rekurencyjne typy danych _są_ przydatne w różnych sytuacjach, ale
zaczynając w tym rozdziale od listy cons, możemy zbadać, jak boxy pozwalają
zdefiniować rekurencyjny typ danych, bez zbędnego rozpraszania uwagi.

Listing 15-2 zawiera definicję *enuma* (typu wyliczeniowego) dla listy
cons. Zauważ, że ten kod jeszcze się nie skompiluje, ponieważ typ `List` nie ma
znanego rozmiaru, co zaraz pokażemy.

<Listing number="15-2" file-name="src/main.rs" caption="Pierwsza próba zdefiniowania enuma reprezentującego strukturę danych listy cons z wartościami `i32`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-02/src/main.rs:here}}
```

</Listing>

> Uwaga: na potrzeby tego przykładu implementujemy listę cons, która
> przechowuje tylko wartości `i32`. Moglibyśmy zaimplementować ją za pomocą
> typów generycznych (*generics*), omówionych w rozdziale 10, i zdefiniować typ
> listy cons, który mógłby przechowywać wartości dowolnego typu.

Użycie typu `List` do przechowania listy `1, 2, 3` wyglądałoby jak kod w
listingu 15-3.

<Listing number="15-3" file-name="src/main.rs" caption="Użycie enuma `List` do przechowania listy `1, 2, 3`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-03/src/main.rs:here}}
```

</Listing>

Pierwsza wartość `Cons` zawiera `1` i kolejną wartość `List`. Ta wartość `List`
jest kolejną wartością `Cons`, która zawiera `2` i kolejną wartość `List`. Ta
wartość `List` jest jeszcze jedną wartością `Cons`, która zawiera `3` i wartość
`List`, którą jest wreszcie `Nil` – nierekurencyjny wariant sygnalizujący
koniec listy.

Jeśli spróbujemy skompilować kod z listingu 15-3, otrzymamy błąd pokazany w
listingu 15-4.

<Listing number="15-4" caption="Błąd, który otrzymujemy przy próbie zdefiniowania rekurencyjnego enuma">

```console
{{#include ../listings/ch15-smart-pointers/listing-15-03/output.txt}}
```

</Listing>

Błąd informuje, że ten typ „has infinite size” (ma nieskończony rozmiar).
Powodem jest to, że zdefiniowaliśmy `List` z wariantem rekurencyjnym: zawiera on
bezpośrednio inną wartość swojego własnego typu. W rezultacie Rust nie potrafi
ustalić, ile miejsca potrzebuje do przechowania wartości `List`. Rozłóżmy na
części, dlaczego otrzymujemy ten błąd. Najpierw przyjrzymy się temu, jak Rust
ustala, ile miejsca potrzebuje do przechowania wartości typu
nierekurencyjnego.

#### Obliczanie rozmiaru typu nierekurencyjnego {#computing-the-size-of-a-non-recursive-type}

Przypomnij sobie enum `Message` zdefiniowany w listingu 6-2, gdy omawialiśmy
definicje enumów w rozdziale 6:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

Aby ustalić, ile miejsca zaalokować dla wartości `Message`, Rust przegląda
każdy z wariantów, by sprawdzić, który z nich potrzebuje najwięcej miejsca.
Rust widzi, że `Message::Quit` nie potrzebuje żadnego miejsca, `Message::Move`
potrzebuje miejsca wystarczającego na przechowanie dwóch wartości `i32` i tak
dalej. Ponieważ używany będzie tylko jeden wariant, najwięcej miejsca, jakiego
będzie potrzebować wartość `Message`, to miejsce potrzebne do przechowania
największego z jej wariantów.

Porównaj to z tym, co się dzieje, gdy Rust próbuje ustalić, ile miejsca
potrzebuje typ rekurencyjny, taki jak enum `List` z listingu 15-2. Kompilator
zaczyna od wariantu `Cons`, który zawiera wartość typu `i32` i wartość typu
`List`. Dlatego `Cons` potrzebuje ilości miejsca równej rozmiarowi `i32` plus
rozmiarowi `List`. Aby ustalić, ile pamięci potrzebuje typ `List`, kompilator
przegląda warianty, zaczynając od wariantu `Cons`. Wariant `Cons` zawiera
wartość typu `i32` i wartość typu `List`, a ten proces trwa w nieskończoność,
jak pokazano na rysunku 15-1.

<img alt="Nieskończona lista Cons: prostokąt z etykietą „Cons” podzielony na dwa mniejsze prostokąty. Pierwszy mniejszy prostokąt ma etykietę „i32”, a drugi mniejszy prostokąt ma etykietę „Cons” i zawiera mniejszą wersję zewnętrznego prostokąta „Cons”. Prostokąty „Cons” zawierają coraz mniejsze wersje samych siebie, aż najmniejszy prostokąt o czytelnym rozmiarze zawiera symbol nieskończoności, wskazujący, że to powtarzanie trwa bez końca." src="img/trpl15-01.svg" class="center" style="width: 50%;" />

<span class="caption">Rysunek 15-1: Nieskończona lista `List` złożona z
nieskończenie wielu wariantów `Cons`</span>

<!-- Old headings. Do not remove or links may break. -->

<a id="using-boxt-to-get-a-recursive-type-with-a-known-size"></a>

#### Uzyskiwanie typu rekurencyjnego o znanym rozmiarze {#getting-a-recursive-type-with-a-known-size}

Ponieważ Rust nie potrafi ustalić, ile miejsca zaalokować dla typów
zdefiniowanych rekurencyjnie, kompilator zgłasza błąd z taką pomocną
sugestią:

<!-- manual-regeneration
after doing automatic regeneration, look at listings/ch15-smart-pointers/listing-15-03/output.txt and copy the relevant line
-->

```text
help: insert some indirection (e.g., a `Box`, `Rc`, or `&`) to break the cycle
  |
2 |     Cons(i32, Box<List>),
  |               ++++    +
```

W tej sugestii _pośredniość_ (*indirection*) oznacza, że zamiast przechowywać
wartość bezpośrednio, powinniśmy zmienić strukturę danych tak, by
przechowywała ją pośrednio – przechowując zamiast niej wskaźnik do tej
wartości.

Ponieważ `Box<T>` jest wskaźnikiem, Rust zawsze wie, ile miejsca potrzebuje
`Box<T>`: rozmiar wskaźnika nie zmienia się w zależności od ilości danych, na
które wskazuje. Oznacza to, że możemy umieścić `Box<T>` w wariancie `Cons`
zamiast bezpośrednio kolejnej wartości `List`. `Box<T>` będzie wskazywać na
następną wartość `List`, która będzie się znajdować na stercie, a nie wewnątrz
wariantu `Cons`. Koncepcyjnie nadal mamy listę złożoną z list zawierających
inne listy, ale ta implementacja przypomina teraz raczej umieszczanie
elementów obok siebie niż jednego wewnątrz drugiego.

Możemy zmienić definicję enuma `List` z listingu 15-2 oraz użycie `List` z
listingu 15-3 na kod z listingu 15-5, który się skompiluje.

<Listing number="15-5" file-name="src/main.rs" caption="Definicja `List`, która używa `Box<T>`, aby mieć znany rozmiar">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-05/src/main.rs}}
```

</Listing>

Wariant `Cons` potrzebuje rozmiaru `i32` plus miejsca na przechowanie danych
wskaźnika boxa. Wariant `Nil` nie przechowuje żadnych wartości, więc
potrzebuje na stosie mniej miejsca niż wariant `Cons`. Wiemy teraz, że każda
wartość `List` zajmie rozmiar `i32` plus rozmiar danych wskaźnika boxa. Dzięki
użyciu boxa przerwaliśmy nieskończony, rekurencyjny łańcuch, więc kompilator
może ustalić, ile miejsca potrzebuje do przechowania wartości `List`. Rysunek
15-2 pokazuje, jak wygląda teraz wariant `Cons`.

<img alt="Prostokąt z etykietą „Cons” podzielony na dwa mniejsze prostokąty. Pierwszy mniejszy prostokąt ma etykietę „i32”, a drugi mniejszy prostokąt ma etykietę „Box” i zawiera jeden wewnętrzny prostokąt z etykietą „usize”, reprezentujący skończony rozmiar wskaźnika boxa." src="img/trpl15-02.svg" class="center" />

<span class="caption">Rysunek 15-2: Lista `List`, która nie ma nieskończonego
rozmiaru, ponieważ `Cons` zawiera `Box`</span>

Boxy zapewniają jedynie pośredniość i alokację na stercie; nie mają żadnych
innych specjalnych możliwości, takich jak te, które zobaczymy w innych typach
inteligentnych wskaźników. Nie wiąże się z nimi też narzut wydajnościowy,
który pociągają za sobą te specjalne możliwości, więc mogą się przydać w
przypadkach takich jak lista cons, gdzie pośredniość jest jedynym potrzebnym
nam mechanizmem. Więcej zastosowań boxów poznamy w rozdziale 18.

Typ `Box<T>` jest inteligentnym wskaźnikiem, ponieważ implementuje trait
`Deref`, który pozwala traktować wartości `Box<T>` jak referencje (*reference*).
Gdy wartość `Box<T>` wychodzi poza zasięg, dane na stercie, na które wskazuje
box, również zostają posprzątane dzięki implementacji traitu `Drop`. Te dwa
traity będą jeszcze ważniejsze dla funkcjonalności zapewnianej przez pozostałe
typy inteligentnych wskaźników, które omówimy w dalszej części tego rozdziału.
Przyjrzyjmy się tym dwóm traitom dokładniej.

{{#quiz ../quizzes/ch15-01-box.toml}}

[trait-objects]: ch18-02-trait-objects.html#using-trait-objects-to-abstract-over-shared-behavior

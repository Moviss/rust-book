<!-- Old headings. Do not remove or links may break. -->

<a id="closures-anonymous-functions-that-can-capture-their-environment"></a>
<a id="closures-anonymous-functions-that-capture-their-environment"></a>

## Domknięcia {#closures}

Domknięcia (*closures*) w Ruście to funkcje anonimowe, które możesz zapisać w
zmiennej albo przekazać jako argumenty do innych funkcji. Domknięcie można
utworzyć w jednym miejscu, a potem wywołać je gdzie indziej, aby obliczyć jego
wartość w innym kontekście. W przeciwieństwie do funkcji domknięcia mogą
przechwytywać wartości z zasięgu (*scope*), w którym zostały zdefiniowane.
Pokażemy, jak te właściwości domknięć umożliwiają ponowne użycie kodu i dostosowywanie
zachowania.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-an-abstraction-of-behavior-with-closures"></a>
<a id="refactoring-using-functions"></a>
<a id="refactoring-with-closures-to-store-code"></a>
<a id="capturing-the-environment-with-closures"></a>

### Przechwytywanie środowiska {#capturing-the-environment}

Najpierw przyjrzymy się, jak za pomocą domknięć przechwytywać wartości ze
środowiska, w którym zostały zdefiniowane, aby użyć ich później. Oto scenariusz:
co jakiś czas nasza firma produkująca koszulki rozdaje w ramach promocji
ekskluzywną koszulkę z limitowanej edycji komuś z naszej listy mailingowej.
Osoby z listy mailingowej mogą opcjonalnie dodać do swojego profilu ulubiony
kolor. Jeśli osoba wybrana do otrzymania darmowej koszulki ma ustawiony ulubiony
kolor, dostaje koszulkę w tym kolorze. Jeśli nie podała ulubionego koloru,
dostaje koszulkę w kolorze, którego firma ma obecnie najwięcej.

Można to zaimplementować na wiele sposobów. W tym przykładzie użyjemy *enuma*
(typu wyliczeniowego) o nazwie `ShirtColor` z wariantami `Red` i `Blue` (dla
prostoty ograniczamy liczbę dostępnych kolorów). Stan magazynu firmy
reprezentujemy za pomocą struktury (*struct*) `Inventory` z polem o nazwie
`shirts`, które zawiera `Vec<ShirtColor>` reprezentujący kolory koszulek
dostępnych obecnie w magazynie. Metoda `giveaway` zdefiniowana na `Inventory`
pobiera opcjonalną preferencję koloru zwycięzcy darmowej koszulki i zwraca kolor
koszulki, którą ta osoba otrzyma. Pokazuje to listing 13-1.

<Listing number="13-1" file-name="src/main.rs" caption="Rozdawanie koszulek przez firmę">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-01/src/main.rs}}
```

</Listing>

Zmienna `store` zdefiniowana w `main` ma do rozdania w tej promocji limitowanej
edycji jeszcze dwie niebieskie koszulki i jedną czerwoną. Wywołujemy metodę
`giveaway` dla użytkownika, który woli czerwoną koszulkę, oraz dla użytkownika
bez żadnej preferencji.

Również ten kod można zaimplementować na wiele sposobów, a tutaj, żeby skupić
się na domknięciach, trzymamy się pojęć, które już znasz – z wyjątkiem ciała
metody `giveaway`, które używa domknięcia. W metodzie `giveaway` pobieramy
preferencję użytkownika jako parametr typu `Option<ShirtColor>` i wywołujemy na
`user_preference` metodę `unwrap_or_else`. [Metoda `unwrap_or_else` typu
`Option<T>`][unwrap-or-else]<!-- ignore --> jest zdefiniowana w bibliotece
standardowej. Przyjmuje jeden argument: domknięcie bez argumentów, które zwraca
wartość `T` (tego samego typu, który jest przechowywany w wariancie `Some` typu
`Option<T>`, w tym przypadku `ShirtColor`). Jeśli `Option<T>` jest wariantem
`Some`, `unwrap_or_else` zwraca wartość z wnętrza `Some`. Jeśli `Option<T>` jest
wariantem `None`, `unwrap_or_else` wywołuje domknięcie i zwraca wartość przez
nie zwróconą.

Jako argument `unwrap_or_else` podajemy wyrażenie (*expression*) domknięcia
`|| self.most_stocked()`. To domknięcie, które samo nie przyjmuje żadnych
parametrów (gdyby domknięcie miało parametry, pojawiłyby się między dwiema
pionowymi kreskami). Ciało domknięcia wywołuje `self.most_stocked()`. Tutaj
definiujemy domknięcie, a implementacja `unwrap_or_else` wywoła je później,
jeśli wynik będzie potrzebny.

Uruchomienie tego kodu wypisuje:

```console
{{#include ../listings/ch13-functional-features/listing-13-01/output.txt}}
```

Ciekawe jest to, że przekazaliśmy domknięcie, które wywołuje
`self.most_stocked()` na bieżącej instancji `Inventory`. Biblioteka standardowa
nie musiała nic wiedzieć o zdefiniowanych przez nas typach `Inventory` ani
`ShirtColor` ani o logice, której chcemy użyć w tym scenariuszu. Domknięcie
przechwytuje niemutowalną referencję (*reference*) do instancji `Inventory`
wskazywanej przez `self` i przekazuje ją wraz z podanym przez nas kodem do
metody `unwrap_or_else`. Funkcje natomiast nie potrafią w ten sposób
przechwytywać swojego środowiska.

<!-- Old headings. Do not remove or links may break. -->

<a id="closure-type-inference-and-annotation"></a>

### Wnioskowanie i adnotacje typów domknięć {#inferring-and-annotating-closure-types}

Między funkcjami a domknięciami jest więcej różnic. Domknięcia zwykle nie
wymagają adnotacji typów parametrów ani wartości zwracanej, tak jak wymagają
tego funkcje `fn`. Adnotacje typów są wymagane w funkcjach, ponieważ typy są
częścią jawnego interfejsu udostępnianego użytkownikom. Sztywne zdefiniowanie
tego interfejsu jest ważne, aby wszyscy byli zgodni co do tego, jakich typów
wartości funkcja używa i jakie zwraca. Domknięcia natomiast nie są używane w
takim udostępnianym interfejsie: przechowuje się je w zmiennych i używa bez
nadawania im nazw i udostępniania ich użytkownikom naszej biblioteki.

Domknięcia są zazwyczaj krótkie i mają znaczenie tylko w wąskim kontekście, a
nie w dowolnym scenariuszu. W tak ograniczonych kontekstach kompilator potrafi
wywnioskować typy parametrów i typ zwracany, podobnie jak potrafi wywnioskować
typy większości zmiennych (zdarzają się rzadkie przypadki, w których kompilator
również potrzebuje adnotacji typów domknięcia).

Podobnie jak w przypadku zmiennych, możemy dodać adnotacje typów, jeśli chcemy
zwiększyć jawność i czytelność kosztem większej rozwlekłości, niż jest to
absolutnie konieczne. Domknięcie z adnotacjami typów wyglądałoby jak definicja
pokazana w listingu 13-2. W tym przykładzie definiujemy domknięcie i zapisujemy
je w zmiennej, zamiast definiować je w miejscu, w którym przekazujemy je jako
argument, jak zrobiliśmy w listingu 13-1.

<Listing number="13-2" file-name="src/main.rs" caption="Dodawanie opcjonalnych adnotacji typów parametru i wartości zwracanej w domknięciu">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-02/src/main.rs:here}}
```

</Listing>

Po dodaniu adnotacji typów składnia domknięć bardziej przypomina składnię
funkcji. Dla porównania definiujemy tu funkcję, która dodaje 1 do swojego
parametru, i domknięcie o takim samym zachowaniu. Dodaliśmy kilka spacji, aby
wyrównać odpowiadające sobie części. Widać, że składnia domknięć jest podobna do
składni funkcji, z wyjątkiem użycia pionowych kresek i tego, jak dużo składni
jest opcjonalne:

```rust,ignore
fn  add_one_v1   (x: u32) -> u32 { x + 1 }
let add_one_v2 = |x: u32| -> u32 { x + 1 };
let add_one_v3 = |x|             { x + 1 };
let add_one_v4 = |x|               x + 1  ;
```

Pierwszy wiersz pokazuje definicję funkcji, a drugi – definicję domknięcia z
pełnymi adnotacjami. W trzecim wierszu usuwamy z definicji domknięcia adnotacje
typów. W czwartym usuwamy nawiasy klamrowe, które są opcjonalne, ponieważ ciało
domknięcia składa się tylko z jednego wyrażenia. Wszystkie te definicje są
poprawne i po wywołaniu zachowają się tak samo. Wiersze `add_one_v3` i
`add_one_v4` wymagają, aby domknięcia zostały wywołane, bo inaczej kod się nie
skompiluje – typy zostaną wywnioskowane na podstawie sposobu użycia. Przypomina
to sytuację, w której `let v = Vec::new();` potrzebuje albo adnotacji typów,
albo wstawienia do `Vec` wartości jakiegoś typu, aby Rust mógł wywnioskować typ.

W definicjach domknięć kompilator wywnioskuje po jednym typie konkretnym dla
każdego z ich parametrów i dla wartości zwracanej. Na przykład listing 13-3
pokazuje definicję krótkiego domknięcia, które po prostu zwraca wartość
otrzymaną jako parametr. To domknięcie nie jest zbyt przydatne poza potrzebami
tego przykładu. Zauważ, że nie dodaliśmy do definicji żadnych adnotacji typów.
Ponieważ nie ma adnotacji typów, domknięcie możemy wywołać z dowolnym typem –
tutaj za pierwszym razem zrobiliśmy to z typem `String`. Jeśli następnie
spróbujemy wywołać `example_closure` z liczbą całkowitą, dostaniemy błąd.

<Listing number="13-3" file-name="src/main.rs" caption="Próba wywołania domknięcia o wywnioskowanych typach z dwoma różnymi typami">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-03/src/main.rs:here}}
```

</Listing>

Kompilator zgłasza taki błąd:

```console
{{#include ../listings/ch13-functional-features/listing-13-03/output.txt}}
```

Gdy po raz pierwszy wywołujemy `example_closure` z wartością typu `String`,
kompilator wnioskuje, że typem `x` i typem zwracanym domknięcia jest `String`.
Te typy zostają następnie na stałe przypisane do domknięcia w
`example_closure`, a my dostajemy błąd typu przy następnej próbie użycia innego
typu z tym samym domknięciem.

{{#quiz ../quizzes/ch13-01-closures-sec1.toml}}

### Przechwytywanie referencji lub przenoszenie własności {#capturing-references-or-moving-ownership}

Domknięcia mogą przechwytywać wartości ze swojego środowiska na trzy sposoby,
które odpowiadają bezpośrednio trzem sposobom przyjmowania parametru przez
funkcję: pożyczanie (*borrowing*) niemutowalne, pożyczanie mutowalne (*mutable*)
i przejęcie własności (*ownership*). Domknięcie samo zdecyduje, którego z nich
użyć, na podstawie tego, co ciało funkcji robi z przechwyconymi wartościami.

W listingu 13-4 definiujemy domknięcie, które przechwytuje niemutowalną
referencję do wektora o nazwie `list`, ponieważ do wypisania wartości potrzebuje
tylko niemutowalnej referencji.

<Listing number="13-4" file-name="src/main.rs" caption="Definiowanie i wywoływanie domknięcia, które przechwytuje niemutowalną referencję">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-04/src/main.rs}}
```

</Listing>

Ten przykład pokazuje też, że zmienna może zostać związana z definicją
domknięcia, a później możemy wywołać domknięcie, używając nazwy zmiennej i
nawiasów, tak jakby nazwa zmiennej była nazwą funkcji.

Ponieważ możemy mieć jednocześnie wiele niemutowalnych referencji do `list`,
`list` jest nadal dostępna w kodzie przed definicją domknięcia, po definicji
domknięcia, ale przed jego wywołaniem, a także po wywołaniu domknięcia. Ten kod
się kompiluje, uruchamia i wypisuje:

```console
{{#include ../listings/ch13-functional-features/listing-13-04/output.txt}}
```

Następnie w listingu 13-5 zmieniamy ciało domknięcia tak, aby dodawało element
do wektora `list`. Domknięcie przechwytuje teraz mutowalną referencję.

<Listing number="13-5" file-name="src/main.rs" caption="Definiowanie i wywoływanie domknięcia, które przechwytuje mutowalną referencję">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-05/src/main.rs}}
```

</Listing>

Ten kod się kompiluje, uruchamia i wypisuje:

```console
{{#include ../listings/ch13-functional-features/listing-13-05/output.txt}}
```

Zauważ, że między definicją a wywołaniem domknięcia `borrows_mutably` nie ma
już `println!`: gdy `borrows_mutably` zostaje zdefiniowane, przechwytuje
mutowalną referencję do `list`. Po wywołaniu domknięcia nie używamy go więcej,
więc mutowalne pożyczenie się kończy. Między definicją domknięcia a jego
wywołaniem niemutowalne pożyczenie w celu wypisania nie jest dozwolone, ponieważ
gdy istnieje mutowalne pożyczenie, żadne inne pożyczenia nie są dozwolone.
Spróbuj dodać tam `println!` i zobacz, jaki komunikat błędu dostaniesz!

Jeśli chcesz zmusić domknięcie do przejęcia własności wartości, których używa ze
środowiska, mimo że ciało domknięcia nie potrzebuje jej koniecznie, możesz użyć
słowa kluczowego (*keyword*) `move` przed listą parametrów.

Ta technika przydaje się głównie przy przekazywaniu domknięcia do nowego wątku,
aby przenieść (*move*) dane tak, by ich właścicielem był nowy wątek. Wątki i
powody, dla których warto ich używać, omówimy szczegółowo w rozdziale 16, gdy
będziemy mówić o współbieżności (*concurrency*), ale na razie przyjrzyjmy się
krótko tworzeniu nowego wątku za pomocą domknięcia, które wymaga słowa
kluczowego `move`. Listing 13-6 pokazuje listing 13-4 zmodyfikowany tak, aby
wypisywał wektor w nowym wątku, a nie w wątku głównym.

<Listing number="13-6" file-name="src/main.rs" caption="Użycie `move`, aby zmusić domknięcie wątku do przejęcia własności `list`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-06/src/main.rs}}
```

</Listing>

Tworzymy nowy wątek i jako argument przekazujemy mu domknięcie do uruchomienia.
Ciało domknięcia wypisuje listę. W listingu 13-4 domknięcie przechwytywało
`list` tylko przez niemutowalną referencję, ponieważ to najmniejszy poziom
dostępu do `list` potrzebny do jej wypisania. W tym przykładzie, mimo że ciało
domknięcia nadal potrzebuje tylko niemutowalnej referencji, musimy określić, że
`list` ma zostać przeniesiona do domknięcia, umieszczając słowo kluczowe `move`
na początku definicji domknięcia. Gdyby wątek główny wykonał więcej operacji
przed wywołaniem `join` na nowym wątku, nowy wątek mógłby zakończyć się przed
resztą wątku głównego albo to wątek główny mógłby zakończyć się pierwszy. Gdyby
wątek główny zachował własność `list`, ale zakończył się przed nowym wątkiem i
zwolnił (*drop*) `list`, niemutowalna referencja w wątku byłaby nieprawidłowa.
Dlatego kompilator wymaga, aby `list` została przeniesiona do domknięcia
przekazanego nowemu wątkowi, tak aby referencja była prawidłowa. Spróbuj usunąć
słowo kluczowe `move` albo użyć `list` w wątku głównym po zdefiniowaniu
domknięcia i zobacz, jakie błędy kompilatora dostaniesz!

<!-- Old headings. Do not remove or links may break. -->

<a id="storing-closures-using-generic-parameters-and-the-fn-traits"></a>
<a id="limitations-of-the-cacher-implementation"></a>
<a id="moving-captured-values-out-of-the-closure-and-the-fn-traits"></a>
<a id="moving-captured-values-out-of-closures-and-the-fn-traits"></a>

### Przenoszenie przechwyconych wartości z domknięć {#moving-captured-values-out-of-closures}

Gdy domknięcie przechwyciło referencję albo przejęło własność wartości ze
środowiska, w którym zostało zdefiniowane (co wpływa na to, co – jeśli
cokolwiek – zostaje przeniesione _do_ domknięcia), kod w ciele domknięcia
określa, co stanie się z referencjami lub wartościami, gdy domknięcie zostanie
później wywołane (co wpływa na to, co – jeśli cokolwiek – zostaje przeniesione
_z_ domknięcia).

Ciało domknięcia może zrobić dowolną z następujących rzeczy: przenieść
przechwyconą wartość z domknięcia, zmodyfikować przechwyconą wartość, ani nie
przenosić, ani nie modyfikować wartości albo w ogóle niczego nie przechwytywać ze
środowiska.

Sposób, w jaki domknięcie przechwytuje i obsługuje wartości ze środowiska,
wpływa na to, które *traity* (cechy typów, zbliżone do interfejsów)
domknięcie implementuje, a traity to sposób, w jaki funkcje i struktury mogą
określić, jakich rodzajów domknięć mogą używać. Domknięcia automatycznie
implementują jeden, dwa lub wszystkie trzy z poniższych traitów `Fn`, w sposób
addytywny, zależnie od tego, jak ciało domknięcia obsługuje wartości:

* `FnOnce` dotyczy domknięć, które można wywołać raz. Wszystkie domknięcia
  implementują co najmniej ten trait, ponieważ wszystkie domknięcia można
  wywołać. Domknięcie, które przenosi przechwycone wartości ze swojego ciała,
  implementuje tylko `FnOnce` i żadnego innego traitu `Fn`, ponieważ można je
  wywołać tylko raz.
* `FnMut` dotyczy domknięć, które nie przenoszą przechwyconych wartości ze
  swojego ciała, ale mogą modyfikować przechwycone wartości. Takie domknięcia
  można wywołać więcej niż raz.
* `Fn` dotyczy domknięć, które nie przenoszą przechwyconych wartości ze swojego
  ciała i nie modyfikują przechwyconych wartości, a także domknięć, które
  niczego nie przechwytują ze swojego środowiska. Takie domknięcia można wywołać
  więcej niż raz bez modyfikowania ich środowiska, co jest ważne na przykład
  wtedy, gdy domknięcie jest wywoływane wielokrotnie współbieżnie.

Przyjrzyjmy się definicji metody `unwrap_or_else` typu `Option<T>`, której
użyliśmy w listingu 13-1:

```rust,ignore
impl<T> Option<T> {
    pub fn unwrap_or_else<F>(self, f: F) -> T
    where
        F: FnOnce() -> T
    {
        match self {
            Some(x) => x,
            None => f(),
        }
    }
}
```

Przypomnij sobie, że `T` to typ generyczny (*generic type*) reprezentujący typ
wartości w wariancie `Some` typu `Option`. Ten typ `T` jest również typem
zwracanym przez funkcję `unwrap_or_else`: kod, który wywołuje `unwrap_or_else`
na przykład na `Option<String>`, otrzyma `String`.

Zauważ dalej, że funkcja `unwrap_or_else` ma dodatkowy generyczny parametr typu
`F`. Typ `F` jest typem parametru o nazwie `f`, czyli domknięcia, które
przekazujemy przy wywołaniu `unwrap_or_else`.

Ograniczenie traitu (*trait bound*) określone dla typu generycznego `F` to
`FnOnce() -> T`, co oznacza, że `F` musi dać się wywołać raz, nie przyjmować
argumentów i zwracać `T`. Użycie `FnOnce` w ograniczeniu traitu wyraża warunek,
że `unwrap_or_else` nie wywoła `f` więcej niż raz. W ciele `unwrap_or_else`
widać, że jeśli `Option` jest `Some`, `f` nie zostanie wywołane. Jeśli `Option`
jest `None`, `f` zostanie wywołane raz. Ponieważ wszystkie domknięcia
implementują `FnOnce`, `unwrap_or_else` akceptuje wszystkie trzy rodzaje
domknięć i jest tak elastyczna, jak to tylko możliwe.

> Uwaga: jeśli to, co chcemy zrobić, nie wymaga przechwytywania wartości ze
> środowiska, możemy użyć nazwy funkcji zamiast domknięcia tam, gdzie
> potrzebujemy czegoś, co implementuje jeden z traitów `Fn`. Na przykład na
> wartości typu `Option<Vec<T>>` moglibyśmy wywołać `unwrap_or_else(Vec::new)`,
> aby otrzymać nowy, pusty wektor, jeśli wartością jest `None`. Kompilator
> automatycznie implementuje dla definicji funkcji ten z traitów `Fn`, który ma
> zastosowanie.

Przyjrzyjmy się teraz metodzie `sort_by_key` z biblioteki standardowej,
zdefiniowanej na wycinkach (*slices*), aby zobaczyć, czym różni się od
`unwrap_or_else` i dlaczego `sort_by_key` używa w ograniczeniu traitu `FnMut`
zamiast `FnOnce`. Domknięcie otrzymuje jeden argument w postaci referencji do
aktualnie rozpatrywanego elementu wycinka i zwraca wartość typu `K`, którą
można uporządkować. Ta funkcja przydaje się, gdy chcesz posortować wycinek
według określonego atrybutu każdego elementu. W listingu 13-7 mamy listę
instancji `Rectangle` i używamy `sort_by_key`, aby uporządkować je według
atrybutu `width` od najmniejszej do największej wartości.

<Listing number="13-7" file-name="src/main.rs" caption="Użycie `sort_by_key` do uporządkowania prostokątów według szerokości">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-07/src/main.rs}}
```

</Listing>

Ten kod wypisuje:

```console
{{#include ../listings/ch13-functional-features/listing-13-07/output.txt}}
```

`sort_by_key` jest zdefiniowana tak, by przyjmować domknięcie `FnMut`, ponieważ
wywołuje domknięcie wiele razy: raz dla każdego elementu wycinka. Domknięcie
`|r| r.width` niczego nie przechwytuje, nie modyfikuje ani nie przenosi ze
swojego środowiska, więc spełnia wymagania ograniczenia traitu.

Dla odmiany listing 13-8 pokazuje przykład domknięcia, które implementuje tylko
trait `FnOnce`, ponieważ przenosi wartość ze środowiska. Kompilator nie pozwoli
nam użyć tego domknięcia z `sort_by_key`.

<Listing number="13-8" file-name="src/main.rs" caption="Próba użycia domknięcia `FnOnce` z `sort_by_key`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-08/src/main.rs}}
```

</Listing>

To sztuczny, zawiły (i niedziałający) sposób na policzenie, ile razy
`sort_by_key` wywołuje domknięcie podczas sortowania `list`. Ten kod próbuje
liczyć wywołania, wstawiając `value` – wartość typu `String` ze środowiska
domknięcia – do wektora `sort_operations`. Domknięcie przechwytuje `value`, a
następnie przenosi `value` z domknięcia, przekazując własność `value` wektorowi
`sort_operations`. To domknięcie można wywołać raz; próba wywołania go po raz
drugi by się nie powiodła, ponieważ `value` nie byłoby już w środowisku, więc
nie dałoby się go ponownie wstawić do `sort_operations`! Dlatego to domknięcie
implementuje tylko `FnOnce`. Gdy próbujemy skompilować ten kod, dostajemy błąd
mówiący, że `value` nie może zostać przeniesione z domknięcia, ponieważ
domknięcie musi implementować `FnMut`:

```console
{{#include ../listings/ch13-functional-features/listing-13-08/output.txt}}
```

Błąd wskazuje wiersz w ciele domknięcia, który przenosi `value` ze środowiska.
Aby to naprawić, musimy zmienić ciało domknięcia tak, aby nie przenosiło
wartości ze środowiska. Prostszym sposobem na policzenie, ile razy domknięcie
zostało wywołane, jest trzymanie licznika w środowisku i zwiększanie jego
wartości w ciele domknięcia. Domknięcie z listingu 13-9 działa z `sort_by_key`,
ponieważ przechwytuje jedynie mutowalną referencję do licznika
`num_sort_operations`, więc można je wywołać więcej niż raz.

<Listing number="13-9" file-name="src/main.rs" caption="Użycie domknięcia `FnMut` z `sort_by_key` jest dozwolone.">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-09/src/main.rs}}
```

</Listing>

<!-- TODO: consider adding a section on the use<> operator -->

Podsumowując: traity `Fn` są ważne przy definiowaniu lub używaniu funkcji albo
typów korzystających z domknięć. W następnym podrozdziale omówimy iteratory.
Wiele metod iteratorów przyjmuje domknięcia jako argumenty, więc pamiętaj o tych
szczegółach dotyczących domknięć, gdy będziemy kontynuować!

{{#quiz ../quizzes/ch13-01-closures-sec2.toml}}

[unwrap-or-else]: https://doc.rust-lang.org/std/option/enum.Option.html#method.unwrap_or_else
[lifetime elision]: ch10-03-lifetime-syntax.html#lifetime-elision
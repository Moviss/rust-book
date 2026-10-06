## Składnia wzorców {#pattern-syntax}

W tym podrozdziale zbieramy całą składnię, której można używać we wzorcach, i
omawiamy, dlaczego i kiedy warto sięgnąć po każdy z jej elementów.

### Dopasowywanie literałów {#matching-literals}

Jak widzieliśmy w rozdziale 6, wzorce można dopasowywać bezpośrednio do
literałów. Poniższy kod pokazuje kilka przykładów:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-01-literals/src/main.rs:here}}
```

Ten kod wypisuje `one`, ponieważ wartością w `x` jest `1`. Ta składnia przydaje
się, gdy kod ma wykonać jakąś akcję po otrzymaniu konkretnej wartości.

### Dopasowywanie nazwanych zmiennych {#matching-named-variables}

Nazwane zmienne są wzorcami nieodrzucalnymi (*irrefutable*), które pasują do
każdej wartości; używaliśmy ich w tej książce wielokrotnie. Pojawia się jednak
pewna komplikacja, gdy używasz nazwanych zmiennych w wyrażeniach (*expression*)
`match`, `if let` lub `while let`. Każde z tych wyrażeń otwiera nowy zasięg
(*scope*), więc zmienne zadeklarowane we wzorcu wewnątrz takiego wyrażenia
przesłaniają zmienne o tej samej nazwie spoza konstrukcji – tak jak przy
przesłanianiu (*shadowing*) każdej innej zmiennej. W listingu 19-11 deklarujemy
zmienną `x` o wartości `Some(5)` oraz zmienną `y` o wartości `10`. Następnie
tworzymy wyrażenie `match` dla wartości `x`. Przyjrzyj się wzorcom w ramionach
(*arm*) dopasowania i wywołaniu `println!` na końcu i spróbuj ustalić, co
wypisze ten kod, zanim go uruchomisz lub przeczytasz dalszą część.

<Listing number="19-11" file-name="src/main.rs" caption="Wyrażenie `match` z ramieniem, które wprowadza nową zmienną przesłaniającą istniejącą zmienną `y`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-11/src/main.rs:here}}
```

</Listing>

Prześledźmy, co się dzieje, gdy wykonuje się wyrażenie `match`. Wzorzec w
pierwszym ramieniu nie pasuje do zdefiniowanej wartości `x`, więc wykonanie
przechodzi dalej.

Wzorzec w drugim ramieniu wprowadza nową zmienną `y`, która dopasuje dowolną
wartość wewnątrz wartości `Some`. Ponieważ jesteśmy w nowym zasięgu wewnątrz
wyrażenia `match`, jest to nowa zmienna `y`, a nie ta `y`, którą
zadeklarowaliśmy na początku z wartością `10`. To nowe wiązanie `y` dopasuje
dowolną wartość wewnątrz `Some`, a właśnie to mamy w `x`. Dlatego nowe `y`
zostaje związane z wewnętrzną wartością `Some` w `x`. Tą wartością jest `5`,
więc wykonuje się wyrażenie tego ramienia i wypisuje `Matched, y = 5`.

Gdyby `x` było wartością `None` zamiast `Some(5)`, wzorce w pierwszych dwóch
ramionach by nie pasowały, więc wartość zostałaby dopasowana do podkreślenia. We
wzorcu ramienia z podkreśleniem nie wprowadziliśmy zmiennej `x`, więc `x` w
wyrażeniu to wciąż zewnętrzne `x`, które nie zostało przesłonięte. W tym
hipotetycznym przypadku wyrażenie `match` wypisałoby `Default case, x = None`.

Gdy wyrażenie `match` się kończy, kończy się jego zasięg, a wraz z nim zasięg
wewnętrznego `y`. Ostatnie `println!` wypisuje `at the end: x = Some(5), y = 10`.

Aby utworzyć wyrażenie `match`, które porównuje wartości zewnętrznych `x` i
`y`, zamiast wprowadzać nową zmienną przesłaniającą istniejącą zmienną `y`,
musielibyśmy użyć warunku w postaci strażnika dopasowania (*match guard*).
Strażniki dopasowania omówimy później, w podrozdziale [„Dodatkowe warunki ze strażnikami
dopasowania”](#adding-conditionals-with-match-guards)<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->
<a id="multiple-patterns"></a>

### Dopasowywanie wielu wzorców {#matching-multiple-patterns}

W wyrażeniach `match` możesz dopasowywać wiele wzorców za pomocą składni `|`,
która jest operatorem _lub_ (*or*) dla wzorców. Na przykład w poniższym kodzie
dopasowujemy wartość `x` do ramion dopasowania, z których pierwsze zawiera
opcję _lub_. Oznacza to, że jeśli wartość `x` pasuje do którejkolwiek z wartości
w tym ramieniu, wykona się kod tego ramienia:


```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-02-multiple-patterns/src/main.rs:here}}
```

Ten kod wypisuje `one or two`.

### Dopasowywanie zakresów wartości za pomocą `..=` {#matching-ranges-of-values-with-}

Składnia `..=` pozwala dopasować wartość do zakresu domkniętego. W poniższym
kodzie, gdy wzorzec pasuje do dowolnej wartości z podanego zakresu, wykona się
odpowiednie ramię:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-03-ranges/src/main.rs:here}}
```

Jeśli `x` wynosi `1`, `2`, `3`, `4` lub `5`, dopasuje się pierwsze ramię. Przy
wielu dopasowywanych wartościach ta składnia jest wygodniejsza niż wyrażenie
tego samego za pomocą operatora `|`; gdybyśmy użyli `|`, musielibyśmy napisać
`1 | 2 | 3 | 4 | 5`. Podanie zakresu jest znacznie krótsze, zwłaszcza gdy
chcemy dopasować, powiedzmy, dowolną liczbę od 1 do 1000!

Kompilator sprawdza w czasie kompilacji, czy zakres nie jest pusty, a ponieważ
jedynymi typami, dla których Rust potrafi stwierdzić, czy zakres jest pusty,
są `char` i typy liczbowe, zakresy są dozwolone tylko dla wartości liczbowych i
wartości `char`.

Oto przykład z zakresami wartości `char`:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-04-ranges-of-char/src/main.rs:here}}
```

Rust ustala, że `'c'` mieści się w zakresie pierwszego wzorca, i wypisuje
`early ASCII letter`.

### Destrukturyzacja w celu rozbicia wartości {#destructuring-to-break-apart-values}

Wzorców możemy też używać do destrukturyzacji struktur (*structs*), *enumów*
(typów wyliczeniowych) i krotek (*tuples*), aby korzystać z różnych części
tych wartości. Omówmy kolejno każdy z tych rodzajów wartości.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs"></a>

#### Struktury {#structs}

Listing 19-12 pokazuje strukturę `Point` z dwoma polami, `x` i `y`, którą
możemy rozbić na części za pomocą wzorca w instrukcji (*statement*) `let`.

<Listing number="19-12" file-name="src/main.rs" caption="Destrukturyzacja pól struktury do osobnych zmiennych">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-12/src/main.rs}}
```

</Listing>

Ten kod tworzy zmienne `a` i `b`, które dopasowują wartości pól `x` i `y`
struktury `p`. Przykład pokazuje, że nazwy zmiennych we wzorcu nie muszą
odpowiadać nazwom pól struktury. Często jednak nadaje się zmiennym takie same
nazwy jak polom, żeby łatwiej było zapamiętać, która zmienna pochodzi z którego
pola. Ponieważ jest to powszechna praktyka, a zapis `let Point { x: x, y: y } = p;`
zawiera sporo powtórzeń, Rust ma skrócony zapis dla wzorców dopasowujących pola
struktury: wystarczy podać nazwę pola struktury, a zmienne utworzone ze wzorca
będą miały te same nazwy. Listing 19-13 działa tak samo jak kod z listingu
19-12, ale zmienne utworzone we wzorcu `let` to `x` i `y` zamiast `a` i `b`.

<Listing number="19-13" file-name="src/main.rs" caption="Destrukturyzacja pól struktury za pomocą skróconego zapisu pól">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-13/src/main.rs}}
```

</Listing>

Ten kod tworzy zmienne `x` i `y`, które dopasowują pola `x` i `y` zmiennej `p`.
W rezultacie zmienne `x` i `y` zawierają wartości ze struktury `p`.

W ramach wzorca struktury możemy też destrukturyzować za pomocą literałów,
zamiast tworzyć zmienne dla wszystkich pól. Dzięki temu możemy sprawdzać, czy
niektóre pola mają określone wartości, a jednocześnie tworzyć zmienne przy
destrukturyzacji pozostałych pól.

W listingu 19-14 mamy wyrażenie `match`, które dzieli wartości `Point` na trzy
przypadki: punkty leżące bezpośrednio na osi `x` (co zachodzi, gdy `y = 0`), na
osi `y` (`x = 0`) albo na żadnej z osi.

<Listing number="19-14" file-name="src/main.rs" caption="Destrukturyzacja i dopasowywanie literałów w jednym wzorcu">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-14/src/main.rs:here}}
```

</Listing>

Pierwsze ramię dopasuje każdy punkt leżący na osi `x`, ponieważ określa, że
pole `y` pasuje, jeśli jego wartość pasuje do literału `0`. Wzorzec nadal
tworzy zmienną `x`, której możemy użyć w kodzie tego ramienia.

Podobnie drugie ramię dopasowuje każdy punkt na osi `y`, określając, że pole
`x` pasuje, jeśli jego wartość wynosi `0`, i tworzy zmienną `y` dla wartości
pola `y`. Trzecie ramię nie zawiera żadnych literałów, więc dopasowuje każdy
inny `Point` i tworzy zmienne dla obu pól, `x` i `y`.

W tym przykładzie wartość `p` pasuje do drugiego ramienia, ponieważ `x`
zawiera `0`, więc ten kod wypisze `On the y axis at 7`.

Pamiętaj, że wyrażenie `match` przestaje sprawdzać ramiona, gdy znajdzie
pierwszy pasujący wzorzec, więc choć `Point { x: 0, y: 0 }` leży zarówno na osi
`x`, jak i na osi `y`, ten kod wypisałby tylko `On the x axis at 0`.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-enums"></a>

#### Enumy {#enums}

W tej książce destrukturyzowaliśmy już enumy (na przykład w listingu 6-5 w
rozdziale 6), ale nie powiedzieliśmy jeszcze wprost, że wzorzec służący do
destrukturyzacji enuma odpowiada sposobowi, w jaki zdefiniowano dane
przechowywane w enumie. Na przykład w listingu 19-15 używamy enuma `Message` z
listingu 6-2 i piszemy `match` ze wzorcami, które destrukturyzują każdą
wewnętrzną wartość.

<Listing number="19-15" file-name="src/main.rs" caption="Destrukturyzacja wariantów enuma przechowujących różne rodzaje wartości">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-15/src/main.rs}}
```

</Listing>

Ten kod wypisze `Change color to red 0, green 160, and blue 255`. Spróbuj
zmienić wartość `msg`, aby zobaczyć, jak wykonuje się kod z innych ramion.

W przypadku wariantów enuma bez żadnych danych, takich jak `Message::Quit`, nie
możemy już dalej destrukturyzować wartości. Możemy jedynie dopasować dosłowną
wartość `Message::Quit`, a we wzorcu nie ma żadnych zmiennych.

W przypadku wariantów enuma przypominających struktury, takich jak
`Message::Move`, możemy użyć wzorca podobnego do tego, którym dopasowujemy
struktury. Po nazwie wariantu umieszczamy nawiasy klamrowe, a w nich wymieniamy
pola ze zmiennymi, dzięki czemu rozbijamy wartość na części, których możemy
użyć w kodzie tego ramienia. Używamy tu skróconego zapisu, tak jak w listingu
19-13.

W przypadku wariantów enuma przypominających krotki, takich jak
`Message::Write`, który przechowuje krotkę z jednym elementem, i
`Message::ChangeColor`, który przechowuje krotkę z trzema elementami, wzorzec
jest podobny do tego, którym dopasowujemy krotki. Liczba zmiennych we wzorcu
musi być równa liczbie elementów w dopasowywanym wariancie.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-nested-structs-and-enums"></a>

#### Zagnieżdżone struktury i enumy {#nested-structs-and-enums}

Dotąd wszystkie nasze przykłady dopasowywały struktury lub enumy na jednym
poziomie głębokości, ale dopasowywanie działa też na elementach zagnieżdżonych!
Możemy na przykład zrefaktoryzować kod z listingu 19-15, aby obsługiwał kolory
RGB i HSV w komunikacie `ChangeColor`, co pokazuje listing 19-16.

<Listing number="19-16" caption="Dopasowywanie zagnieżdżonych enumów">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-16/src/main.rs}}
```

</Listing>

Wzorzec pierwszego ramienia w wyrażeniu `match` dopasowuje wariant enuma
`Message::ChangeColor`, który zawiera wariant `Color::Rgb`; następnie wzorzec
wiąże trzy wewnętrzne wartości `i32`. Wzorzec drugiego ramienia również
dopasowuje wariant enuma `Message::ChangeColor`, ale wewnętrzny enum pasuje do
`Color::Hsv`. Takie złożone warunki możemy wyrazić w jednym wyrażeniu `match`,
mimo że w grę wchodzą dwa enumy.

<!-- Old headings. Do not remove or links may break. -->

<a id="destructuring-structs-and-tuples"></a>

#### Struktury i krotki {#structs-and-tuples}

Wzorce destrukturyzujące możemy mieszać, łączyć i zagnieżdżać na jeszcze
bardziej złożone sposoby. Poniższy przykład pokazuje skomplikowaną
destrukturyzację, w której zagnieżdżamy struktury i krotki wewnątrz krotki i
wydobywamy z nich wszystkie wartości typów prymitywnych:

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/no-listing-05-destructuring-structs-and-tuples/src/main.rs:here}}
```

Ten kod pozwala rozbić złożone typy na części składowe, dzięki czemu możemy
osobno korzystać z wartości, które nas interesują.

Destrukturyzacja za pomocą wzorców to wygodny sposób na korzystanie z
fragmentów wartości, takich jak wartość każdego pola struktury, niezależnie od
siebie.

### Ignorowanie wartości we wzorcu {#ignoring-values-in-a-pattern}

Wiesz już, że czasem przydaje się ignorowanie wartości we wzorcu, na
przykład w ostatnim ramieniu `match`, aby uzyskać wzorzec przechwytujący
wszystko (*catch-all*), który w praktyce nic nie robi, ale uwzględnia wszystkie
pozostałe możliwe wartości. Istnieje kilka sposobów ignorowania całych wartości
lub ich części we wzorcu: użycie wzorca `_` (który już znasz), użycie wzorca
`_` wewnątrz innego wzorca, użycie nazwy zaczynającej się od podkreślenia albo
użycie `..` do zignorowania pozostałych części wartości. Zobaczmy, jak i
dlaczego używać każdego z tych wzorców.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-entire-value-with-_"></a>

#### Cała wartość za pomocą `_` {#an-entire-value-with-_}

Używaliśmy już podkreślenia jako symbolu wieloznacznego, który pasuje do każdej
wartości, ale nie wiąże się z nią. Jest to szczególnie przydatne w ostatnim
ramieniu wyrażenia `match`, ale możemy go użyć w dowolnym wzorcu, także w
parametrach funkcji, co pokazuje listing 19-17.

<Listing number="19-17" file-name="src/main.rs" caption="Użycie `_` w sygnaturze funkcji">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-17/src/main.rs}}
```

</Listing>

Ten kod całkowicie zignoruje wartość `3` przekazaną jako pierwszy argument i
wypisze `This code only uses the y parameter: 4`.

Zazwyczaj, gdy dany parametr funkcji przestaje być potrzebny, zmienia się
sygnaturę tak, by go nie zawierała. Zignorowanie parametru funkcji może być
jednak szczególnie przydatne na przykład wtedy, gdy implementujesz *trait*
(cechę typu, zbliżoną do interfejsu), który wymaga określonej sygnatury, a ciało
funkcji w twojej implementacji nie potrzebuje jednego z parametrów. Unikasz
wtedy ostrzeżenia kompilatora o nieużywanych parametrach funkcji, które
pojawiłoby się, gdyby zamiast tego użyć zwykłej nazwy.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-parts-of-a-value-with-a-nested-_"></a>

#### Części wartości za pomocą zagnieżdżonego `_` {#parts-of-a-value-with-a-nested-_}

Możemy też użyć `_` wewnątrz innego wzorca, aby zignorować tylko część wartości,
na przykład gdy chcemy sprawdzić tylko fragment wartości, a pozostałe części nie
są potrzebne w kodzie, który chcemy wykonać. Listing 19-18 pokazuje kod
odpowiedzialny za zarządzanie wartością ustawienia. Wymagania biznesowe są
takie, że użytkownik nie może nadpisać istniejącej, dostosowanej wartości
ustawienia, ale może usunąć ustawienie i nadać mu wartość, jeśli obecnie nie
jest ustawione.

<Listing number="19-18" caption="Użycie podkreślenia we wzorcach dopasowujących warianty `Some`, gdy nie potrzebujemy wartości wewnątrz `Some`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-18/src/main.rs:here}}
```

</Listing>

Ten kod wypisze `Can't overwrite an existing customized value`, a następnie
`setting is Some(5)`. W pierwszym ramieniu nie musimy dopasowywać ani używać
wartości wewnątrz żadnego z wariantów `Some`, ale musimy sprawdzić przypadek,
w którym zarówno `setting_value`, jak i `new_setting_value` są wariantem
`Some`. W takim przypadku wypisujemy powód, dla którego nie zmieniamy
`setting_value`, i wartość ta pozostaje niezmieniona.

We wszystkich pozostałych przypadkach (gdy `setting_value` lub
`new_setting_value` ma wartość `None`), wyrażonych wzorcem `_` w drugim
ramieniu, chcemy pozwolić na ustawienie `setting_value` na `new_setting_value`.

Podkreśleń możemy też użyć w kilku miejscach jednego wzorca, aby zignorować
określone wartości. Listing 19-19 pokazuje przykład ignorowania drugiej i
czwartej wartości w krotce pięciu elementów.

<Listing number="19-19" caption="Ignorowanie wielu części krotki">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-19/src/main.rs:here}}
```

</Listing>

Ten kod wypisze `Some numbers: 2, 8, 32`, a wartości `4` i `16` zostaną
zignorowane.

<!-- Old headings. Do not remove or links may break. -->

<a id="ignoring-an-unused-variable-by-starting-its-name-with-_"></a>

#### Nieużywana zmienna z nazwą zaczynającą się od `_` {#an-unused-variable-by-starting-its-name-with-_}

Jeśli utworzysz zmienną, ale nigdzie jej nie użyjesz, Rust zwykle zgłosi
ostrzeżenie, ponieważ nieużywana zmienna może oznaczać błąd. Czasem jednak
przydaje się możliwość utworzenia zmiennej, której jeszcze nie użyjesz, na
przykład podczas prototypowania albo na samym początku projektu. W takiej
sytuacji możesz powiedzieć Rustowi, żeby nie ostrzegał o nieużywanej zmiennej,
zaczynając jej nazwę od podkreślenia. W listingu 19-20 tworzymy dwie nieużywane
zmienne, ale podczas kompilacji tego kodu powinniśmy dostać ostrzeżenie tylko o
jednej z nich.

<Listing number="19-20" file-name="src/main.rs" caption="Nazwa zmiennej zaczynająca się od podkreślenia, aby uniknąć ostrzeżeń o nieużywanych zmiennych">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-20/src/main.rs}}
```

</Listing>

Dostajemy tu ostrzeżenie o nieużywanej zmiennej `y`, ale nie dostajemy
ostrzeżenia o nieużywanej zmiennej `_x`.

Zwróć uwagę na subtelną różnicę między użyciem samego `_` a użyciem nazwy
zaczynającej się od podkreślenia. Składnia `_x` nadal wiąże wartość ze
zmienną, natomiast `_` w ogóle niczego nie wiąże. Aby pokazać przypadek, w
którym to rozróżnienie ma znaczenie, w listingu 19-21 otrzymamy błąd.

<Listing number="19-21" caption="Nieużywana zmienna zaczynająca się od podkreślenia nadal wiąże wartość, co może oznaczać przejęcie jej na własność.">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-21/src/main.rs:here}}
```

</Listing>

Otrzymamy błąd, ponieważ i tak nastąpi przeniesienie (*move*) wartości `s` do
`_s`, co uniemożliwia ponowne użycie `s`. Samo podkreślenie natomiast nigdy nie
wiąże się z wartością. Listing 19-22 skompiluje się bez żadnych błędów, ponieważ `s`
nie zostaje przeniesione do `_`.

<Listing number="19-22" caption="Użycie podkreślenia nie wiąże wartości.">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-22/src/main.rs:here}}
```

</Listing>

Ten kod działa bez zarzutu, ponieważ nigdy nie wiążemy `s` z niczym; nie
następuje żadne przeniesienie.

<a id="ignoring-remaining-parts-of-a-value-with-"></a>

#### Pozostałe części wartości za pomocą `..` {#remaining-parts-of-a-value-with-}

W przypadku wartości składających się z wielu części możemy użyć składni `..`,
aby skorzystać z wybranych części i zignorować resztę, bez konieczności
wpisywania podkreślenia dla każdej ignorowanej wartości. Wzorzec `..` ignoruje
wszystkie części wartości, których nie dopasowaliśmy jawnie w pozostałej części
wzorca. W listingu 19-23 mamy strukturę `Point`, która przechowuje współrzędne
w przestrzeni trójwymiarowej. W wyrażeniu `match` chcemy operować tylko na
współrzędnej `x` i zignorować wartości w polach `y` i `z`.

<Listing number="19-23" caption="Ignorowanie wszystkich pól `Point` z wyjątkiem `x` za pomocą `..`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-23/src/main.rs:here}}
```

</Listing>

Podajemy wartość `x`, a potem po prostu dodajemy wzorzec `..`. To szybsze niż
wypisywanie `y: _` i `z: _`, zwłaszcza gdy pracujemy ze strukturami o wielu
polach w sytuacjach, w których istotne są tylko jedno lub dwa pola.

Składnia `..` rozwinie się do tylu wartości, ilu potrzeba. Listing 19-24
pokazuje, jak użyć `..` z krotką.

<Listing number="19-24" file-name="src/main.rs" caption="Dopasowanie tylko pierwszej i ostatniej wartości w krotce z pominięciem wszystkich pozostałych">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-24/src/main.rs}}
```

</Listing>

W tym kodzie pierwsza i ostatnia wartość są dopasowywane do `first` i `last`.
`..` dopasuje i zignoruje wszystko pomiędzy nimi.

Użycie `..` musi jednak być jednoznaczne. Jeśli nie jest jasne, które wartości
mają zostać dopasowane, a które zignorowane, Rust zgłosi błąd. Listing 19-25
pokazuje przykład niejednoznacznego użycia `..`, więc ten kod się nie
skompiluje.

<Listing number="19-25" file-name="src/main.rs" caption="Próba niejednoznacznego użycia `..`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-25/src/main.rs}}
```

</Listing>

Podczas kompilacji tego przykładu dostajemy taki błąd:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-25/output.txt}}
```

Rust nie jest w stanie ustalić, ile wartości w krotce zignorować przed
dopasowaniem wartości do `second`, ani ile kolejnych wartości zignorować
potem. Ten kod mógłby oznaczać, że chcemy zignorować `2`, związać `second` z
`4`, a następnie zignorować `8`, `16` i `32`; albo że chcemy zignorować `2` i
`4`, związać `second` z `8`, a następnie zignorować `16` i `32`; i tak dalej.
Nazwa zmiennej `second` nie ma dla Rusta żadnego szczególnego znaczenia, więc
dostajemy błąd kompilatora, ponieważ takie użycie `..` w dwóch miejscach jest
niejednoznaczne.

<!-- Old headings. Do not remove or links may break. -->

<a id="extra-conditionals-with-match-guards"></a>

### Dodatkowe warunki ze strażnikami dopasowania {#adding-conditionals-with-match-guards}

_Strażnik dopasowania_ to dodatkowy warunek `if`, podany po
wzorcu w ramieniu `match`, który również musi być spełniony, aby to ramię
zostało wybrane. Strażniki dopasowania przydają się do wyrażania bardziej
złożonych zależności, niż pozwala na to sam wzorzec. Zwróć jednak uwagę, że są
dostępne tylko w wyrażeniach `match`, a nie w wyrażeniach `if let` czy
`while let`.

Warunek może korzystać ze zmiennych utworzonych we wzorcu. Listing 19-26
pokazuje `match`, w którym pierwsze ramię ma wzorzec `Some(x)` oraz strażnika
dopasowania `if x % 2 == 0` (który da `true`, jeśli liczba jest parzysta).

<Listing number="19-26" caption="Dodanie strażnika dopasowania do wzorca">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-26/src/main.rs:here}}
```

</Listing>

Ten przykład wypisze `The number 4 is even`. Gdy `num` jest porównywane ze
wzorcem w pierwszym ramieniu, pasuje do niego, ponieważ `Some(4)` pasuje do
`Some(x)`. Następnie strażnik dopasowania sprawdza, czy reszta z dzielenia `x`
przez 2 jest równa 0, a ponieważ tak jest, wybrane zostaje pierwsze ramię.

Gdyby `num` miało zamiast tego wartość `Some(5)`, strażnik dopasowania w
pierwszym ramieniu dałby `false`, ponieważ reszta z dzielenia 5 przez 2 wynosi
1, a to nie jest 0. Rust przeszedłby wtedy do drugiego ramienia, które by
pasowało, ponieważ nie ma strażnika dopasowania, a więc pasuje do każdego
wariantu `Some`.

Warunku `if x % 2 == 0` nie da się wyrazić we wzorcu, więc strażnik
dopasowania pozwala nam wyrazić tę logikę. Wadą tej dodatkowej siły wyrazu
jest to, że gdy w grę wchodzą wyrażenia strażników dopasowania, kompilator nie
próbuje sprawdzać, czy dopasowanie jest wyczerpujące (*exhaustive*).

Omawiając listing 19-11, wspomnieliśmy, że do rozwiązania naszego problemu z
przesłanianiem we wzorcu możemy użyć strażników dopasowania. Przypomnij sobie,
że utworzyliśmy nową zmienną wewnątrz wzorca w wyrażeniu `match`, zamiast użyć
zmiennej spoza `match`. Ta nowa zmienna sprawiła, że nie mogliśmy porównać
wartości z wartością zmiennej zewnętrznej. Listing 19-27 pokazuje, jak
naprawić ten problem za pomocą strażnika dopasowania.

<Listing number="19-27" file-name="src/main.rs" caption="Użycie strażnika dopasowania do sprawdzenia równości ze zmienną zewnętrzną">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-27/src/main.rs}}
```

</Listing>

Ten kod wypisze teraz `Default case, x = Some(5)`. Wzorzec w drugim ramieniu
nie wprowadza nowej zmiennej `y`, która przesłoniłaby zewnętrzne `y`, więc
możemy użyć zewnętrznego `y` w strażniku dopasowania. Zamiast podawać wzorzec
`Some(y)`, który przesłoniłby zewnętrzne `y`, podajemy `Some(n)`. Tworzy to
nową zmienną `n`, która niczego nie przesłania, ponieważ poza `match` nie ma
zmiennej `n`.

Strażnik dopasowania `if n == y` nie jest wzorcem, więc nie wprowadza nowych
zmiennych. To `y` _jest_ zewnętrznym `y`, a nie nowym `y`, które by je
przesłaniało, i możemy szukać wartości równej zewnętrznemu `y`, porównując `n`
z `y`.

W strażniku dopasowania możesz też użyć operatora _lub_ `|`, aby podać wiele
wzorców; warunek strażnika będzie dotyczył wszystkich tych wzorców. Listing
19-28 pokazuje pierwszeństwo przy łączeniu wzorca używającego `|` ze
strażnikiem dopasowania. Najważniejsze w tym przykładzie jest to, że strażnik
`if y` dotyczy `4`, `5` _i_ `6`, choć mogłoby się wydawać, że `if y` dotyczy
tylko `6`.

<Listing number="19-28" caption="Łączenie wielu wzorców ze strażnikiem dopasowania">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-28/src/main.rs:here}}
```

</Listing>

Warunek dopasowania mówi, że ramię pasuje tylko wtedy, gdy wartość `x` jest
równa `4`, `5` lub `6` _oraz_ gdy `y` ma wartość `true`. Po uruchomieniu kodu
wzorzec pierwszego ramienia pasuje, ponieważ `x` wynosi `4`, ale strażnik
dopasowania `if y` daje `false`, więc pierwsze ramię nie zostaje wybrane. Kod
przechodzi do drugiego ramienia, które pasuje, i program wypisuje `no`. Dzieje
się tak, ponieważ warunek `if` dotyczy całego wzorca `4 | 5 | 6`, a nie tylko
ostatniej wartości `6`. Innymi słowy, pierwszeństwo strażnika dopasowania
względem wzorca wygląda tak:

```text
(4 | 5 | 6) if y => ...
```

a nie tak:

```text
4 | 5 | (6 if y) => ...
```

Po uruchomieniu kodu pierwszeństwo staje się oczywiste: gdyby strażnik
dopasowania dotyczył tylko ostatniej wartości na liście wartości podanych za
pomocą operatora `|`, ramię zostałoby dopasowane, a program wypisałby `yes`.

<!-- Old headings. Do not remove or links may break. -->

<a id="-bindings"></a>

### Używanie wiązań `@` {#using--bindings}

Operator _at_ `@` pozwala utworzyć zmienną przechowującą wartość, a
jednocześnie sprawdzać, czy ta wartość pasuje do wzorca. W listingu 19-29
chcemy sprawdzić, czy pole `id` wariantu `Message::Hello` mieści się w
zakresie `3..=7`. Chcemy też związać tę wartość ze zmienną `id`, aby móc jej
użyć w kodzie powiązanym z ramieniem.

<Listing number="19-29" caption="Użycie `@` do związania wartości we wzorcu przy jednoczesnym jej sprawdzeniu">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-29/src/main.rs:here}}
```

</Listing>

Ten przykład wypisze `Found an id in range: 5`. Podając `id @` przed zakresem
`3..=7`, przechwytujemy wartość pasującą do zakresu w zmiennej o nazwie `id`, a
jednocześnie sprawdzamy, czy wartość pasuje do wzorca zakresu.

W drugim ramieniu, gdzie we wzorcu podaliśmy tylko zakres, kod powiązany z
ramieniem nie ma zmiennej zawierającej faktyczną wartość pola `id`. Wartością
pola `id` mogło być 10, 11 lub 12, ale kod związany z tym wzorcem nie wie,
która z nich. Kod wzorca nie może użyć wartości z pola `id`, ponieważ nie
zapisaliśmy wartości `id` w zmiennej.

W ostatnim ramieniu, gdzie podaliśmy zmienną bez zakresu, wartość jest dostępna
w kodzie ramienia w zmiennej o nazwie `id`. Wynika to z tego, że użyliśmy
skróconego zapisu pól struktury. W przeciwieństwie do pierwszych dwóch ramion
nie sprawdzamy jednak w tym ramieniu wartości pola `id` w żaden sposób: do tego
wzorca pasuje dowolna wartość.

Użycie `@` pozwala w jednym wzorcu sprawdzić wartość i zapisać ją w zmiennej.

{{#quiz ../quizzes/ch18-03-pattern-syntax.toml}}

## Podsumowanie {#summary}

Wzorce w Ruście są bardzo przydatne do rozróżniania różnych rodzajów danych.
Gdy używasz ich w wyrażeniach `match`, Rust pilnuje, aby wzorce obejmowały
każdą możliwą wartość – inaczej program się nie skompiluje. Wzorce w
instrukcjach `let` i parametrach funkcji czynią te konstrukcje bardziej
użytecznymi, umożliwiając destrukturyzację wartości na mniejsze części i
przypisanie tych części do zmiennych. Możemy tworzyć proste lub złożone
wzorce, dopasowane do naszych potrzeb.

W kolejnym, przedostatnim rozdziale książki przyjrzymy się zaawansowanym
aspektom różnych mechanizmów Rusta.

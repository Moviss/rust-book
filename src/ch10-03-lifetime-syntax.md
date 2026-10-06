## Sprawdzanie poprawności referencji za pomocą czasów życia {#validating-references-with-lifetimes}

Czasy życia (*lifetimes*) to kolejny rodzaj typów generycznych (*generics*),
z którego już korzystaliśmy. Zamiast zapewniać, że typ ma pożądane przez nas
zachowanie, czasy życia gwarantują, że referencje (*references*) pozostają
poprawne tak długo, jak ich potrzebujemy.

W podrozdziale
[„Referencje i pożyczanie”][references-and-borrowing]<!-- ignore --> w rozdziale 4
nie omówiliśmy jednego szczegółu: każda referencja w Ruście ma czas życia, czyli
zasięg (*scope*), w którym jest poprawna. Najczęściej czasy życia są niejawne i wywnioskowane, podobnie jak
najczęściej wnioskowane są typy. Adnotacje typów musimy podawać tylko wtedy, gdy
możliwych jest kilka typów. Analogicznie adnotacje czasów życia musimy podawać
wtedy, gdy czasy życia referencji mogą być ze sobą powiązane na kilka różnych
sposobów. Rust wymaga, abyśmy opisywali te zależności za pomocą generycznych
parametrów czasu życia, dzięki czemu faktyczne referencje używane w czasie
działania programu na pewno będą poprawne.

Adnotacje czasów życia to pojęcie, którego większość innych języków
programowania w ogóle nie zna, więc może się ono wydawać obce. Choć w tym
rozdziale nie omówimy czasów życia w całości, przedstawimy typowe sytuacje, w
których możesz zetknąć się ze składnią czasów życia, aby łatwiej było ci oswoić
się z tą koncepcją.

<!-- Old headings. Do not remove or links may break. -->

<a id="preventing-dangling-references-with-lifetimes"></a>

### Wiszące referencje {#dangling-references}

Głównym celem czasów życia jest zapobieganie wiszącym referencjom (*dangling
references*), które – gdyby mogły istnieć – sprawiałyby, że program odwołuje się
do innych danych niż te, do których miał się odwoływać. Rozważmy program z
listingu 10-16, który ma zasięg zewnętrzny i wewnętrzny.

<!-- TODO(aquascope): support for nested scopes -->
<Listing number="10-16" caption="Próba użycia referencji, której wartość wyszła poza zasięg">

```rust,ignore,does_not_compile
fn main() {
    let r;

    {
        let x = 5;
        r = &x;
    }

    println!("r: {}", r);
}
```

</Listing>

> Uwaga: przykłady z listingów 10-16, 10-17 i 10-23 deklarują zmienne bez
> nadawania im wartości początkowej, więc nazwa zmiennej istnieje w zasięgu
> zewnętrznym. Na pierwszy rzut oka może się to wydawać sprzeczne z tym, że w
> Ruście nie ma wartości null. Jeśli jednak spróbujemy użyć zmiennej, zanim
> nadamy jej wartość, otrzymamy błąd w czasie kompilacji, co pokazuje, że Rust
> rzeczywiście nie dopuszcza wartości null.

Zasięg zewnętrzny deklaruje zmienną o nazwie `r` bez wartości początkowej, a
zasięg wewnętrzny – zmienną o nazwie `x` z wartością początkową `5`. Wewnątrz
zasięgu wewnętrznego próbujemy ustawić wartość `r` jako referencję do `x`.
Następnie zasięg wewnętrzny się kończy, a my próbujemy wypisać wartość z `r`.
Ten kod się nie skompiluje, ponieważ wartość, do której odnosi się `r`, wyszła
poza zasięg, zanim spróbowaliśmy jej użyć. Oto komunikat o błędzie:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-16/output.txt}}
```

Komunikat o błędzie mówi, że zmienna `x` „does not live long enough” („nie żyje
wystarczająco długo”). Powodem jest to, że `x` wyjdzie poza zasięg, gdy w
wierszu 7 skończy się zasięg wewnętrzny. Natomiast `r` jest wciąż poprawna w
zasięgu zewnętrznym; ponieważ jej zasięg jest większy, mówimy, że „żyje dłużej”.
Gdyby Rust pozwolił na działanie tego kodu, `r` odwoływałaby się do pamięci
zdealokowanej w chwili, gdy `x` wyszła poza zasięg, i nic, co próbowalibyśmy
zrobić z `r`, nie działałoby poprawnie. Jak więc Rust ustala, że ten kod jest
niepoprawny? Używa *borrow checkera* (mechanizmu sprawdzania pożyczeń).

### Borrow checker dba o to, by dane żyły dłużej niż referencje do nich {#the-borrow-checker-ensures-data-outlives-its-references}

Kompilator Rusta ma _borrow checker_, który porównuje zasięgi, aby ustalić, czy
wszystkie pożyczenia są poprawne. Listing 10-17 przedstawia ten sam kod co
listing 10-16, ale z adnotacjami pokazującymi czasy życia zmiennych.

<Listing number="10-17" caption="Adnotacje czasów życia `r` i `x`, nazwanych odpowiednio `'a` i `'b`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-17/src/main.rs}}
```

</Listing>

Oznaczyliśmy tu czas życia `r` jako `'a`, a czas życia `x` jako `'b`. Jak
widać, wewnętrzny blok `'b` jest dużo mniejszy niż zewnętrzny blok czasu życia
`'a`. W czasie kompilacji Rust porównuje rozmiary obu czasów życia i widzi, że
`r` ma czas życia `'a`, ale odwołuje się do pamięci o czasie życia `'b`.
Program zostaje odrzucony, ponieważ `'b` jest krótszy niż `'a`: obiekt, do
którego odnosi się referencja, nie żyje tak długo jak sama referencja.

Listing 10-18 poprawia kod tak, aby nie było w nim wiszącej referencji, i kod
kompiluje się bez żadnych błędów.

<Listing number="10-18" caption="Poprawna referencja, ponieważ dane mają dłuższy czas życia niż referencja">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-18/src/main.rs}}
```

</Listing>

Tutaj `x` ma czas życia `'b`, który w tym przypadku jest większy niż `'a`.
Oznacza to, że `r` może odwoływać się do `x`, ponieważ Rust wie, że referencja
w `r` będzie zawsze poprawna, dopóki poprawna jest `x`.

Skoro wiesz już, gdzie znajdują się czasy życia referencji i jak Rust analizuje
czasy życia, aby zagwarantować, że referencje zawsze będą poprawne, przyjrzyjmy
się generycznym czasom życia parametrów i wartości zwracanych przez funkcje.

### Generyczne czasy życia w funkcjach {#generic-lifetimes-in-functions}

Napiszemy funkcję, która zwraca dłuższy z dwóch wycinków łańcuchów (*string
slices*). Funkcja ta przyjmie dwa wycinki łańcuchów i zwróci jeden wycinek
łańcucha. Gdy zaimplementujemy funkcję `longest`, kod z listingu 10-19 powinien
wypisać `The longest string is abcd`.

<Listing number="10-19" file-name="src/main.rs" caption="Funkcja `main` wywołująca funkcję `longest`, aby znaleźć dłuższy z dwóch wycinków łańcuchów">

```rust,ignore
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-19/src/main.rs}}
```

</Listing>

Zauważ, że chcemy, aby funkcja przyjmowała wycinki łańcuchów, które są
referencjami, a nie łańcuchy znaków (*strings*), ponieważ nie chcemy, by funkcja
`longest` przejmowała własność (*ownership*) swoich parametrów. Więcej o tym,
dlaczego parametry użyte w listingu 10-19 są właśnie tymi, których potrzebujemy,
przeczytasz w podrozdziale
[„Wycinki łańcuchów jako parametry”][string-slices-as-parameters]<!-- ignore -->
w rozdziale 4.

Jeśli spróbujemy zaimplementować funkcję `longest` tak jak w listingu 10-20,
kod się nie skompiluje.

<Listing number="10-20" file-name="src/main.rs" caption="Implementacja funkcji `longest`, która zwraca dłuższy z dwóch wycinków łańcuchów, ale jeszcze się nie kompiluje">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/src/main.rs:here}}
```

</Listing>

Zamiast tego otrzymujemy następujący błąd, który mówi o czasach życia:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-20/output.txt}}
```

Tekst pomocy wskazuje, że typ zwracany potrzebuje generycznego parametru czasu
życia, ponieważ Rust nie potrafi określić, czy zwracana referencja odnosi się do
`x`, czy do `y`. Prawdę mówiąc, my też tego nie wiemy, ponieważ blok `if` w ciele
tej funkcji zwraca referencję do `x`, a blok `else` – referencję do `y`!

Definiując tę funkcję, nie znamy konkretnych wartości, które zostaną do niej
przekazane, więc nie wiemy, czy wykona się gałąź `if`, czy gałąź `else`. Nie
znamy też konkretnych czasów życia przekazywanych referencji, więc nie możemy
przyjrzeć się zasięgom, tak jak zrobiliśmy to w listingach 10-17 i 10-18, aby
ustalić, czy zwracana referencja zawsze będzie poprawna. Borrow checker również
nie potrafi tego ustalić, ponieważ nie wie, jak czasy życia `x` i `y` mają się
do czasu życia wartości zwracanej. Aby naprawić ten błąd, dodamy generyczne
parametry czasu życia, które określą zależność między referencjami, tak aby
borrow checker mógł przeprowadzić swoją analizę.

### Składnia adnotacji czasu życia {#lifetime-annotation-syntax}

Adnotacje czasu życia nie zmieniają tego, jak długo żyje którakolwiek z
referencji. Opisują natomiast zależności między czasami życia wielu referencji,
nie wpływając na same czasy życia. Tak jak funkcje mogą przyjmować dowolny typ,
gdy sygnatura określa generyczny parametr typu, tak samo mogą przyjmować
referencje o dowolnym czasie życia, gdy określa ona generyczny parametr czasu
życia.

Adnotacje czasu życia mają nieco nietypową składnię: nazwy parametrów czasu
życia muszą zaczynać się od apostrofu (`'`) i zwykle są w całości zapisane
małymi literami oraz bardzo krótkie, podobnie jak typy generyczne. Większość
osób używa nazwy `'a` dla pierwszej adnotacji czasu życia. Adnotacje parametrów
czasu życia umieszczamy po znaku `&` referencji, oddzielając adnotację od typu
referencji spacją.

Oto kilka przykładów: referencja do `i32` bez parametru czasu życia, referencja
do `i32` z parametrem czasu życia o nazwie `'a` oraz mutowalna (*mutable*)
referencja do `i32`, która również ma czas życia `'a`:

```rust,ignore
&i32        // a reference
&'a i32     // a reference with an explicit lifetime
&'a mut i32 // a mutable reference with an explicit lifetime
```

Pojedyncza adnotacja czasu życia sama w sobie nie ma większego znaczenia,
ponieważ adnotacje służą do informowania Rusta, jak generyczne parametry czasu
życia wielu referencji mają się do siebie nawzajem. Sprawdźmy, jak adnotacje
czasu życia odnoszą się do siebie w kontekście funkcji `longest`.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-function-signatures"></a>

### W sygnaturach funkcji {#in-function-signatures}

Aby użyć adnotacji czasu życia w sygnaturach funkcji, musimy zadeklarować
generyczne parametry czasu życia w nawiasach ostrych między nazwą funkcji a
listą parametrów, tak jak robiliśmy to z generycznymi parametrami typu.

Chcemy, aby sygnatura wyrażała następujące ograniczenie: zwracana referencja
będzie poprawna tak długo, jak poprawne są oba parametry. Taka jest zależność
między czasami życia parametrów a wartości zwracanej. Nazwiemy czas życia `'a`
i dodamy go do każdej referencji, jak pokazano w listingu 10-21.

<Listing number="10-21" file-name="src/main.rs" caption="Definicja funkcji `longest` określająca, że wszystkie referencje w sygnaturze muszą mieć ten sam czas życia `'a`">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-21/src/main.rs:here}}
```

</Listing>

Ten kod powinien się skompilować i dać oczekiwany wynik, gdy użyjemy go z
funkcją `main` z listingu 10-19.

Sygnatura funkcji mówi teraz Rustowi, że dla pewnego czasu życia `'a` funkcja
przyjmuje dwa parametry, z których oba są wycinkami łańcuchów żyjącymi co
najmniej tak długo jak czas życia `'a`. Sygnatura funkcji mówi też Rustowi, że
wycinek łańcucha zwrócony z funkcji będzie żył co najmniej tak długo jak czas
życia `'a`. W praktyce oznacza to, że czas życia referencji zwracanej przez
funkcję `longest` jest taki sam jak krótszy z czasów życia wartości, do których
odnoszą się argumenty funkcji. Właśnie z tych zależności ma korzystać Rust
podczas analizy tego kodu.

Pamiętaj, że określając parametry czasu życia w tej sygnaturze funkcji, nie
zmieniamy czasów życia żadnych przekazywanych ani zwracanych wartości.
Określamy natomiast, że borrow checker ma odrzucać wszelkie wartości, które nie
spełniają tych ograniczeń. Zauważ, że funkcja `longest` nie musi dokładnie
wiedzieć, jak długo będą żyć `x` i `y` – wystarczy, że za `'a` można podstawić
jakiś zasięg spełniający tę sygnaturę.

Gdy dodajemy adnotacje czasów życia w funkcjach, umieszczamy je w sygnaturze
funkcji, a nie w jej ciele. Adnotacje czasu życia stają się częścią kontraktu
funkcji, podobnie jak typy w sygnaturze. To, że sygnatury funkcji zawierają
kontrakt dotyczący czasów życia, sprawia, że analiza przeprowadzana przez
kompilator Rusta może być prostsza. Jeśli jest problem ze sposobem, w jaki
funkcja została opisana adnotacjami lub w jaki jest wywoływana, błędy
kompilatora mogą dokładniej wskazać odpowiednie miejsce w naszym kodzie i
naruszone ograniczenia. Gdyby natomiast kompilator Rusta sam więcej wnioskował
o tym, jakie zależności między czasami życia mieliśmy na myśli, mógłby być w
stanie wskazać jedynie użycie naszego kodu odległe o wiele kroków od przyczyny
problemu.

Gdy przekazujemy do `longest` konkretne referencje, konkretnym czasem życia
podstawianym za `'a` jest ta część zasięgu `x`, która pokrywa się z zasięgiem
`y`. Innymi słowy, generyczny czas życia `'a` otrzyma konkretny czas życia
równy krótszemu z czasów życia `x` i `y`. Ponieważ zwracaną referencję
opatrzyliśmy tym samym parametrem czasu życia `'a`, będzie ona również poprawna
przez czas równy krótszemu z czasów życia `x` i `y`.

Przyjrzyjmy się, jak adnotacje czasu życia ograniczają funkcję `longest`, gdy
przekazujemy do niej referencje o różnych konkretnych czasach życia. Listing
10-22 to prosty przykład.

<Listing number="10-22" file-name="src/main.rs" caption="Użycie funkcji `longest` z referencjami do wartości `String` o różnych konkretnych czasach życia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-22/src/main.rs:here}}
```

</Listing>

W tym przykładzie `string1` jest poprawna do końca zasięgu zewnętrznego,
`string2` jest poprawna do końca zasięgu wewnętrznego, a `result` odwołuje się
do czegoś, co jest poprawne do końca zasięgu wewnętrznego. Uruchom ten kod, a
zobaczysz, że borrow checker go akceptuje; kod się skompiluje i wypisze
`The longest string is long string is long`.

Spróbujmy teraz przykładu, który pokazuje, że czas życia referencji w `result`
musi być krótszym z czasów życia obu argumentów. Przeniesiemy deklarację
zmiennej `result` poza zasięg wewnętrzny, ale przypisanie wartości do zmiennej
`result` zostawimy wewnątrz zasięgu ze `string2`. Następnie przeniesiemy
`println!`, które używa `result`, poza zasięg wewnętrzny, za miejsce, w którym
ten zasięg się kończy. Kod z listingu 10-23 się nie skompiluje.

<Listing number="10-23" file-name="src/main.rs" caption="Próba użycia `result` po tym, jak `string2` wyszła poza zasięg">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/src/main.rs:here}}
```

</Listing>

Gdy spróbujemy skompilować ten kod, otrzymamy następujący błąd:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-23/output.txt}}
```

Błąd pokazuje, że aby `result` była poprawna w instrukcji `println!`,
`string2` musiałaby być poprawna do końca zasięgu zewnętrznego. Rust to wie,
ponieważ opatrzyliśmy czasy życia parametrów funkcji i wartości zwracanych tym
samym parametrem czasu życia `'a`.

Jako ludzie możemy spojrzeć na ten kod i zobaczyć, że `string1` jest dłuższa
niż `string2`, a zatem `result` będzie zawierać referencję do `string1`.
Ponieważ `string1` jeszcze nie wyszła poza zasięg, referencja do `string1`
będzie wciąż poprawna w instrukcji `println!`. Kompilator nie jest jednak w
stanie zobaczyć, że referencja jest w tym przypadku poprawna. Powiedzieliśmy
Rustowi, że czas życia referencji zwracanej przez funkcję `longest` jest taki
sam jak krótszy z czasów życia przekazanych referencji. Dlatego borrow checker
odrzuca kod z listingu 10-23 jako taki, który może zawierać niepoprawną
referencję.

Spróbuj zaprojektować więcej eksperymentów, w których zmieniasz wartości i
czasy życia referencji przekazywanych do funkcji `longest` oraz sposób użycia
zwracanej referencji. Zanim skompilujesz kod, postaw hipotezę, czy twoje
eksperymenty przejdą weryfikację borrow checkera, a potem sprawdź, czy była
trafna!

{{#quiz ../quizzes/ch10-03-lifetimes-sec1.toml}}

<!-- Old headings. Do not remove or links may break. -->

<a id="thinking-in-terms-of-lifetimes"></a>

### Zależności {#relationships}

Sposób, w jaki musisz określić parametry czasu życia, zależy od tego, co robi
twoja funkcja. Gdybyśmy na przykład zmienili implementację funkcji `longest`
tak, aby zawsze zwracała pierwszy parametr zamiast najdłuższego wycinka
łańcucha, nie musielibyśmy określać czasu życia parametru `y`. Następujący kod
się skompiluje:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-08-only-one-reference-with-lifetime/src/main.rs:here}}
```

</Listing>

Określiliśmy parametr czasu życia `'a` dla parametru `x` i typu zwracanego, ale
nie dla parametru `y`, ponieważ czas życia `y` nie ma żadnego związku z czasem
życia `x` ani wartości zwracanej.

Gdy zwracamy referencję z funkcji, parametr czasu życia typu zwracanego musi
odpowiadać parametrowi czasu życia jednego z parametrów. Jeśli zwracana
referencja _nie_ odnosi się do żadnego z parametrów, musi odnosić się do
wartości utworzonej wewnątrz tej funkcji. Byłaby to jednak wisząca referencja,
ponieważ wartość wyjdzie poza zasięg na końcu funkcji. Rozważmy następującą
próbę implementacji funkcji `longest`, która się nie skompiluje:

<Listing file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/src/main.rs:here}}
```

</Listing>

Choć określiliśmy tu parametr czasu życia `'a` dla typu zwracanego, ta
implementacja się nie skompiluje, ponieważ czas życia wartości zwracanej w
ogóle nie jest powiązany z czasem życia parametrów. Oto komunikat o błędzie,
który otrzymujemy:

```console
{{#include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-09-unrelated-lifetime/output.txt}}
```

Problem polega na tym, że `result` wychodzi poza zasięg i zostaje zwolniona na
końcu funkcji `longest`. Jednocześnie próbujemy zwrócić z funkcji referencję do
`result`. Nie da się określić parametrów czasu życia, które zmieniłyby fakt, że
referencja jest wisząca, a Rust nie pozwoli nam utworzyć wiszącej referencji.
W tym przypadku najlepszym rozwiązaniem byłoby zwrócenie zamiast referencji
typu będącego właścicielem swoich danych, tak aby za zwolnienie wartości
odpowiadała funkcja wywołująca.

Ostatecznie składnia czasów życia służy do łączenia czasów życia różnych
parametrów i wartości zwracanych przez funkcje. Gdy są one połączone, Rust ma
wystarczająco dużo informacji, aby zezwolić na operacje bezpieczne dla pamięci
i zabronić operacji, które tworzyłyby wiszące wskaźniki lub w inny sposób
naruszałyby bezpieczeństwo pamięci.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-struct-definitions"></a>

### W definicjach struktur {#in-struct-definitions}

Wszystkie zdefiniowane dotąd przez nas struktury (*structs*) przechowywały typy
będące właścicielami swoich danych. Możemy definiować struktury przechowujące
referencje, ale wtedy musimy dodać adnotację czasu życia do każdej referencji w
definicji struktury. Listing 10-24 zawiera strukturę o nazwie
`ImportantExcerpt`, która przechowuje wycinek łańcucha.

<Listing number="10-24" file-name="src/main.rs" caption="Struktura przechowująca referencję, co wymaga adnotacji czasu życia">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-24/src/main.rs}}
```

</Listing>

Ta struktura ma jedno pole `part`, które przechowuje wycinek łańcucha, czyli
referencję. Podobnie jak w przypadku generycznych typów danych, deklarujemy
nazwę generycznego parametru czasu życia w nawiasach ostrych po nazwie
struktury, aby móc użyć tego parametru w ciele definicji struktury. Ta
adnotacja oznacza, że instancja `ImportantExcerpt` nie może żyć dłużej niż
referencja, którą przechowuje w polu `part`.

Funkcja `main` tworzy tu instancję struktury `ImportantExcerpt`, która
przechowuje referencję do pierwszego zdania wartości `String` należącej do
zmiennej `novel`. Dane w `novel` istnieją, zanim zostanie utworzona instancja
`ImportantExcerpt`. Co więcej, `novel` wychodzi poza zasięg dopiero po tym, jak
poza zasięg wyjdzie `ImportantExcerpt`, więc referencja w instancji
`ImportantExcerpt` jest poprawna.

### Pomijanie czasów życia {#lifetime-elision}

Wiesz już, że każda referencja ma czas życia i że musisz określać parametry
czasu życia dla funkcji lub struktur używających referencji. Jednak w listingu
4-9 mieliśmy funkcję, pokazaną ponownie w listingu 10-25, która skompilowała
się bez adnotacji czasu życia.

<Listing number="10-25" file-name="src/lib.rs" caption="Funkcja zdefiniowana w listingu 4-9, która skompilowała się bez adnotacji czasu życia, mimo że zarówno parametr, jak i typ zwracany są referencjami">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-25/src/main.rs:here}}
```

</Listing>

Powód, dla którego ta funkcja kompiluje się bez adnotacji czasu życia, jest
historyczny: we wczesnych wersjach Rusta (sprzed 1.0) ten kod by się nie
skompilował, ponieważ każda referencja potrzebowała jawnego czasu życia. W
tamtym czasie sygnatura funkcji wyglądałaby tak:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Po napisaniu dużej ilości kodu w Ruście zespół Rusta zauważył, że programiści
w określonych sytuacjach wciąż na nowo wpisują te same adnotacje czasu życia.
Sytuacje te były przewidywalne i przebiegały według kilku deterministycznych
wzorców. Twórcy języka zaprogramowali te wzorce w kodzie kompilatora, tak aby
borrow checker mógł w tych sytuacjach wywnioskować czasy życia i nie
potrzebował jawnych adnotacji.

Ten fragment historii Rusta jest istotny, ponieważ możliwe, że pojawią się
kolejne deterministyczne wzorce, które zostaną dodane do kompilatora. W
przyszłości adnotacji czasu życia może być potrzebnych jeszcze mniej.

Wzorce zaprogramowane w analizie referencji w Ruście nazywamy _regułami
pomijania czasów życia_ (*lifetime elision rules*). Nie są to reguły, których
mają przestrzegać programiści; to zestaw szczególnych przypadków, które
kompilator weźmie pod uwagę, a jeśli twój kod do nich pasuje, nie musisz
jawnie zapisywać czasów życia.

Reguły pomijania nie zapewniają pełnego wnioskowania. Jeśli po zastosowaniu
reguł przez Rusta wciąż nie wiadomo jednoznacznie, jakie czasy życia mają
referencje, kompilator nie będzie zgadywał, jaki powinien być czas życia
pozostałych referencji. Zamiast zgadywać, kompilator zgłosi błąd, który możesz
naprawić, dodając adnotacje czasu życia.

Czasy życia parametrów funkcji lub metod nazywamy _wejściowymi czasami życia_
(*input lifetimes*), a czasy życia wartości zwracanych – _wyjściowymi czasami
życia_ (*output lifetimes*).

Kompilator używa trzech reguł, aby ustalić czasy życia referencji, gdy nie ma
jawnych adnotacji. Pierwsza reguła dotyczy wejściowych czasów życia, a druga i
trzecia – wyjściowych czasów życia. Jeśli kompilator dojdzie do końca trzech
reguł i wciąż będą referencje, dla których nie potrafi ustalić czasów życia,
zatrzyma się z błędem. Reguły te dotyczą zarówno definicji `fn`, jak i bloków
`impl`.

<!-- BEGIN INTERVENTION: d03748df-8dcf-4ec8-bd30-341927544665 -->
Pierwsza reguła mówi, że kompilator przypisuje osobny parametr czasu życia każdemu czasowi życia w każdym typie wejściowym. Referencje takie jak `&'_ i32` potrzebują parametru czasu życia, a struktury takie jak `ImportantExcerpt<'_>` również potrzebują parametru czasu życia. Na przykład:
* Funkcja `fn foo(x: &i32)` otrzyma jeden parametr czasu życia i stanie się `fn foo<'a>(x: &'a i32)`. 
* Funkcja `fn foo(x: &i32, y: &i32)` otrzyma dwa parametry czasu życia i stanie się `fn foo<'a, 'b>(x: &'a i32, y: &'b i32)`.
* Funkcja `fn foo(x: &ImportantExcerpt)` otrzyma dwa parametry czasu życia i stanie się `fn foo<'a, 'b>(x: &'a ImportantExcerpt<'b>)`.
<!-- END INTERVENTION -->

Druga reguła mówi, że jeśli istnieje dokładnie jeden wejściowy parametr czasu
życia, ten czas życia jest przypisywany wszystkim wyjściowym parametrom czasu
życia: `fn foo<'a>(x: &'a i32) -> &'a i32`.

Trzecia reguła mówi, że jeśli istnieje wiele wejściowych parametrów czasu
życia, ale jednym z nich jest `&self` lub `&mut self`, ponieważ chodzi o
metodę, to czas życia `self` jest przypisywany wszystkim wyjściowym parametrom
czasu życia. Ta trzecia reguła sprawia, że metody znacznie łatwiej się czyta i
pisze, ponieważ potrzeba mniej symboli.

Wyobraźmy sobie, że jesteśmy kompilatorem. Zastosujemy te reguły, aby ustalić
czasy życia referencji w sygnaturze funkcji `first_word` z listingu 10-25.
Sygnatura na początku nie ma żadnych czasów życia powiązanych z referencjami:

```rust,ignore
fn first_word(s: &str) -> &str {
```

Następnie kompilator stosuje pierwszą regułę, która mówi, że każdy parametr
otrzymuje własny czas życia. Jak zwykle nazwiemy go `'a`, więc sygnatura
wygląda teraz tak:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &str {
```

Druga reguła ma zastosowanie, ponieważ istnieje dokładnie jeden wejściowy czas
życia. Mówi ona, że czas życia jedynego parametru wejściowego zostaje
przypisany wyjściowemu czasowi życia, więc sygnatura wygląda teraz tak:

```rust,ignore
fn first_word<'a>(s: &'a str) -> &'a str {
```

Teraz wszystkie referencje w tej sygnaturze funkcji mają czasy życia, a
kompilator może kontynuować analizę bez potrzeby, by programista opatrywał
adnotacjami czasy życia w tej sygnaturze.

Przyjrzyjmy się innemu przykładowi, tym razem z funkcją `longest`, która nie
miała parametrów czasu życia, gdy zaczynaliśmy z nią pracę w listingu 10-20:

```rust,ignore
fn longest(x: &str, y: &str) -> &str {
```

Zastosujmy pierwszą regułę: każdy parametr otrzymuje własny czas życia. Tym
razem mamy dwa parametry zamiast jednego, więc mamy dwa czasy życia:

```rust,ignore
fn longest<'a, 'b>(x: &'a str, y: &'b str) -> &str {
```

Jak widać, druga reguła nie ma zastosowania, ponieważ jest więcej niż jeden
wejściowy czas życia. Trzecia reguła również nie ma zastosowania, ponieważ
`longest` jest funkcją, a nie metodą, więc żaden z parametrów nie jest `self`.
Po przejściu przez wszystkie trzy reguły wciąż nie ustaliliśmy czasu życia typu
zwracanego. Dlatego właśnie otrzymaliśmy błąd przy próbie kompilacji kodu z
listingu 10-20: kompilator przeszedł przez reguły pomijania czasów życia, ale
wciąż nie potrafił ustalić wszystkich czasów życia referencji w sygnaturze.

Ponieważ trzecia reguła w praktyce dotyczy tylko sygnatur metod, przyjrzymy się
teraz czasom życia w tym kontekście, aby zobaczyć, dlaczego dzięki trzeciej
regule rzadko musimy opatrywać adnotacjami czasy życia w sygnaturach metod.

<!-- Old headings. Do not remove or links may break. -->

<a id="lifetime-annotations-in-method-definitions"></a>

### W definicjach metod {#in-method-definitions}

Gdy implementujemy metody dla struktury z czasami życia, używamy tej samej
składni co w przypadku generycznych parametrów typu, jak pokazano w listingu
10-11. To, gdzie deklarujemy i używamy parametrów czasu życia, zależy od tego,
czy są one powiązane z polami struktury, czy z parametrami metody i wartościami
zwracanymi.

Nazwy czasów życia dla pól struktury zawsze trzeba zadeklarować po słowie
kluczowym `impl`, a następnie użyć ich po nazwie struktury, ponieważ te czasy
życia są częścią typu struktury.

W sygnaturach metod wewnątrz bloku `impl` referencje mogą być powiązane z
czasem życia referencji w polach struktury albo mogą być od niego niezależne.
Ponadto reguły pomijania czasów życia często sprawiają, że adnotacje czasu
życia w sygnaturach metod nie są potrzebne. Przyjrzyjmy się kilku przykładom z
użyciem struktury `ImportantExcerpt`, którą zdefiniowaliśmy w listingu 10-24.

Najpierw użyjemy metody o nazwie `level`, której jedynym parametrem jest
referencja do `self`, a wartością zwracaną jest `i32`, czyli nie referencja do
czegokolwiek:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:1st}}
```

Deklaracja parametru czasu życia po `impl` i jego użycie po nazwie typu są
wymagane, ale dzięki pierwszej regule pomijania nie musimy opatrywać adnotacją
czasu życia referencji do `self`.

Oto przykład, w którym ma zastosowanie trzecia reguła pomijania czasów życia:

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-10-lifetimes-on-methods/src/main.rs:3rd}}
```

Mamy dwa wejściowe czasy życia, więc Rust stosuje pierwszą regułę pomijania
czasów życia i nadaje zarówno `&self`, jak i `announcement` własne czasy życia.
Następnie, ponieważ jednym z parametrów jest `&self`, typ zwracany otrzymuje
czas życia `&self` i wszystkie czasy życia zostały ustalone.

### Statyczny czas życia {#the-static-lifetime}

Jednym ze szczególnych czasów życia, które musimy omówić, jest `'static`, który
oznacza, że dana referencja _może_ żyć przez cały czas działania programu.
Wszystkie literały łańcuchowe mają czas życia `'static`, co możemy zapisać w
adnotacji następująco:

```rust
let s: &'static str = "I have a static lifetime.";
```

Tekst tego łańcucha jest przechowywany bezpośrednio w pliku binarnym programu,
który jest zawsze dostępny. Dlatego czasem życia wszystkich literałów
łańcuchowych jest `'static`.

W komunikatach o błędach możesz zobaczyć sugestie, by użyć czasu życia
`'static`. Zanim jednak określisz `'static` jako czas życia referencji,
zastanów się, czy twoja referencja rzeczywiście żyje przez cały czas życia
programu i czy tego chcesz. W większości przypadków komunikat o błędzie
sugerujący czas życia `'static` wynika z próby utworzenia wiszącej referencji
lub z niedopasowania dostępnych czasów życia. W takich sytuacjach rozwiązaniem
jest naprawienie tych problemów, a nie określenie czasu życia `'static`.

<!-- Old headings. Do not remove or links may break. -->

<a id="generic-type-parameters-trait-bounds-and-lifetimes-together"></a>

## Generyczne parametry typu, ograniczenia traitów i czasy życia {#generic-type-parameters-trait-bounds-and-lifetimes}

Przyjrzyjmy się pokrótce składni, w której w jednej funkcji określamy
generyczne parametry typu, ograniczenia traitów (*trait bounds*) i czasy życia!

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/no-listing-11-generics-traits-and-lifetimes/src/main.rs:here}}
```

To funkcja `longest` z listingu 10-21, która zwraca dłuższy z dwóch wycinków
łańcuchów. Teraz ma jednak dodatkowy parametr o nazwie `ann` generycznego typu
`T`, za który można podstawić dowolny typ implementujący *trait* (cecha typu,
zbliżona do interfejsu) `Display`, jak określa klauzula `where`. Ten dodatkowy
parametr zostanie wypisany za pomocą `{}`, dlatego potrzebne jest ograniczenie
traitu `Display`. Ponieważ czasy życia są rodzajem typów generycznych,
deklaracje parametru czasu życia `'a` i generycznego parametru typu `T` trafiają
do tej samej listy w nawiasach ostrych po nazwie funkcji.

{{#quiz ../quizzes/ch10-03-lifetimes-sec2.toml}}

### Podsumowanie {#summary}

W tym rozdziale omówiliśmy wiele zagadnień! Teraz, gdy znasz generyczne
parametry typu, traity i ograniczenia traitów oraz generyczne parametry czasu
życia, możesz pisać kod bez powtórzeń, który działa w wielu różnych sytuacjach.
Generyczne parametry typu pozwalają stosować kod do różnych typów. Traity i
ograniczenia traitów zapewniają, że choć typy są generyczne, będą miały
zachowanie potrzebne w kodzie. Wiesz też, jak używać adnotacji czasów życia, aby
ten elastyczny kod nie miał żadnych wiszących referencji. A cała ta analiza
odbywa się w czasie kompilacji, więc nie wpływa na wydajność w czasie działania
programu!

Może trudno w to uwierzyć, ale o tematach omówionych w tym rozdziale można się
dowiedzieć dużo więcej: w rozdziale 18 omawiamy obiekty traitów (*trait
objects*), które są kolejnym sposobem korzystania z traitów. Istnieją też
bardziej złożone scenariusze z adnotacjami czasu życia, których będziesz
potrzebować tylko w bardzo zaawansowanych sytuacjach; o nich przeczytasz w
[Rust Reference][reference]. Najpierw jednak nauczysz się pisać testy w Ruście,
aby mieć pewność, że twój kod działa tak, jak powinien.

[references-and-borrowing]: ch04-02-references-and-borrowing.html#references-and-borrowing
[lifetime-permissions]: ch04-02-references-and-borrowing.html#permissions-are-returned-at-the-end-of-a-references-lifetime
[string-slices-as-parameters]: ch04-04-slices.html#string-slices-as-parameters
[reference]: https://doc.rust-lang.org/reference/trait-bounds.html

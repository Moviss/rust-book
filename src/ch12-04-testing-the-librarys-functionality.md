<!-- Old headings. Do not remove or links may break. -->
<a id="developing-the-librarys-functionality-with-test-driven-development"></a>

## Dodawanie funkcjonalności metodą programowania sterowanego testami {#adding-functionality-with-test-driven-development}

Skoro logika wyszukiwania znajduje się już w _src/lib.rs_, oddzielnie od funkcji
`main`, znacznie łatwiej jest pisać testy dla głównej funkcjonalności naszego
kodu. Możemy wywoływać funkcje bezpośrednio z różnymi argumentami i sprawdzać
zwracane wartości bez konieczności uruchamiania naszego pliku binarnego z
wiersza poleceń.

W tym podrozdziale dodamy logikę wyszukiwania do programu `minigrep`, stosując
programowanie sterowane testami (*test-driven development*, TDD) według
następujących kroków:

1. Napisz test, który kończy się niepowodzeniem, i uruchom go, aby się upewnić,
   że zawodzi z oczekiwanego powodu.
2. Napisz lub zmodyfikuj tylko tyle kodu, ile potrzeba, by nowy test przeszedł.
3. Zrefaktoryzuj kod, który właśnie dodano lub zmieniono, i upewnij się, że
   testy nadal przechodzą.
4. Powtórz od kroku 1!

Choć to tylko jeden z wielu sposobów pisania oprogramowania, TDD może pomóc w
kształtowaniu projektu kodu. Pisanie testu przed napisaniem kodu, dzięki
któremu test przejdzie, pomaga utrzymać wysokie pokrycie testami przez cały
proces.

Metodą TDD zaimplementujemy funkcjonalność, która faktycznie będzie wyszukiwać
zapytanie w zawartości pliku i tworzyć listę wierszy pasujących do zapytania.
Dodamy ją w funkcji o nazwie `search`.

### Pisanie testu, który kończy się niepowodzeniem {#writing-a-failing-test}

W _src/lib.rs_ dodamy moduł `tests` z funkcją testową, tak jak zrobiliśmy to w
[rozdziale 11][ch11-anatomy]<!-- ignore -->. Funkcja testowa określa
zachowanie, jakiego oczekujemy od funkcji `search`: przyjmie ona zapytanie oraz
tekst do przeszukania i zwróci tylko te wiersze tekstu, które zawierają
zapytanie. Ten test przedstawia listing 12-15.

<Listing number="12-15" file-name="src/lib.rs" caption="Tworzenie testu kończącego się niepowodzeniem dla funkcji `search` realizującej funkcjonalność, którą chcielibyśmy mieć">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-15/src/lib.rs:here}}
```

</Listing>

Ten test wyszukuje łańcuch znaków (*string*) `"duct"`. Przeszukiwany tekst ma
trzy wiersze, z których tylko jeden zawiera `"duct"` (zwróć uwagę, że ukośnik
wsteczny po otwierającym cudzysłowie mówi Rustowi, żeby nie wstawiał znaku nowej
linii na początku zawartości tego literału łańcuchowego). Sprawdzamy asercją, że
wartość zwrócona przez funkcję `search` zawiera tylko oczekiwany wiersz.

Gdybyśmy teraz uruchomili ten test, zakończyłby się niepowodzeniem, ponieważ
makro `unimplemented!` wywołuje panikę (*panic*) z komunikatem „not
implemented”. Zgodnie z zasadami TDD zrobimy mały krok: dodamy tylko tyle kodu,
by test nie panikował przy wywołaniu funkcji, definiując funkcję `search` tak,
aby zawsze zwracała pusty wektor (*vector*), jak pokazano w listingu 12-16.
Wtedy test powinien się skompilować i zakończyć niepowodzeniem, ponieważ pusty
wektor nie jest równy wektorowi zawierającemu wiersz `"safe, fast, productive."`.

<Listing number="12-16" file-name="src/lib.rs" caption="Zdefiniowanie funkcji `search` w stopniu wystarczającym, by jej wywołanie nie powodowało paniki">

```rust,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-16/src/lib.rs:here}}
```

</Listing>

Omówmy teraz, dlaczego musimy zdefiniować jawny czas życia (*lifetime*) `'a` w
sygnaturze `search` i użyć go przy argumencie `contents` oraz wartości
zwracanej. Jak pamiętasz z [rozdziału 10][ch10-lifetimes]<!-- ignore -->,
parametry czasu życia określają, czas życia którego argumentu jest powiązany z
czasem życia wartości zwracanej. W tym przypadku wskazujemy, że zwracany wektor
powinien zawierać wycinki łańcucha (*string slices*) odwołujące się do wycinków
argumentu `contents` (a nie argumentu `query`).

Innymi słowy, mówimy Rustowi, że dane zwracane przez funkcję `search` będą żyły
tak długo, jak dane przekazane do funkcji `search` w argumencie `contents`. To
ważne! Dane, do których odwołuje się wycinek, muszą być prawidłowe, aby
referencja była prawidłowa; jeśli kompilator założy, że tworzymy wycinki
łańcucha z `query`, a nie z `contents`, przeprowadzi swoje sprawdzenia
bezpieczeństwa niepoprawnie.

Jeśli zapomnimy o adnotacjach czasu życia i spróbujemy skompilować tę funkcję,
otrzymamy następujący błąd:

```console
{{#include ../listings/ch12-an-io-project/output-only-02-missing-lifetimes/output.txt}}
```

Rust nie może wiedzieć, którego z dwóch parametrów potrzebujemy dla wyniku,
więc musimy mu to powiedzieć jawnie. Zwróć uwagę, że tekst pomocy sugeruje
podanie tego samego parametru czasu życia dla wszystkich parametrów i typu
wyjściowego, co jest niepoprawne! Ponieważ `contents` to parametr zawierający
cały nasz tekst, a chcemy zwrócić pasujące fragmenty tego tekstu, wiemy, że
`contents` jest jedynym parametrem, który należy powiązać z wartością zwracaną
za pomocą składni czasów życia.

Inne języki programowania nie wymagają łączenia argumentów z wartościami
zwracanymi w sygnaturze, ale z czasem ta praktyka stanie się łatwiejsza. Możesz
porównać ten przykład z przykładami z podrozdziału [„Sprawdzanie poprawności
referencji za pomocą czasów życia”][validating-references-with-lifetimes]<!-- ignore -->
w rozdziale 10.

### Pisanie kodu, dzięki któremu test przejdzie {#writing-code-to-pass-the-test}

Obecnie nasz test kończy się niepowodzeniem, ponieważ zawsze zwracamy pusty
wektor. Aby to naprawić i zaimplementować `search`, nasz program musi wykonać
następujące kroki:

1. Przejść po kolei przez każdy wiersz zawartości.
2. Sprawdzić, czy wiersz zawiera nasze zapytanie.
3. Jeśli tak, dodać go do listy zwracanych wartości.
4. Jeśli nie, nic nie robić.
5. Zwrócić listę pasujących wyników.

Przejdźmy przez każdy krok, zaczynając od iterowania po wierszach.

#### Iterowanie po wierszach za pomocą metody `lines` {#iterating-through-lines-with-the-lines-method}

Rust ma przydatną metodę do iterowania po łańcuchach wiersz po wierszu,
wygodnie nazwaną `lines`, która działa tak, jak pokazano w listingu 12-17.
Zwróć uwagę, że ten kod jeszcze się nie skompiluje.

<Listing number="12-17" file-name="src/lib.rs" caption="Iterowanie po każdym wierszu w `contents`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-17/src/lib.rs:here}}
```

</Listing>

Metoda `lines` zwraca iterator. Iteratory omówimy szczegółowo w
[rozdziale 13][ch13-iterators]<!-- ignore -->. Przypomnij sobie jednak, że ten
sposób używania iteratora pojawił się już w [listingu 3-5][ch3-iter]<!-- ignore -->,
gdzie użyliśmy pętli `for` z iteratorem, aby wykonać kod dla każdego elementu
kolekcji.

#### Przeszukiwanie każdego wiersza pod kątem zapytania {#searching-each-line-for-the-query}

Następnie sprawdzimy, czy bieżący wiersz zawiera nasze zapytanie. Na szczęście
łańcuchy mają przydatną metodę `contains`, która robi to za nas! Dodaj
wywołanie metody `contains` w funkcji `search`, jak pokazano w listingu 12-18.
Zwróć uwagę, że ten kod nadal się nie skompiluje.

<Listing number="12-18" file-name="src/lib.rs" caption="Dodanie funkcjonalności sprawdzającej, czy wiersz zawiera łańcuch z `query`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-18/src/lib.rs:here}}
```

</Listing>

Na razie budujemy funkcjonalność krok po kroku. Aby kod się skompilował, musimy
zwrócić wartość z ciała funkcji, tak jak zapowiedzieliśmy w jej sygnaturze.

#### Przechowywanie pasujących wierszy {#storing-matching-lines}

Aby dokończyć tę funkcję, potrzebujemy sposobu na przechowanie pasujących
wierszy, które chcemy zwrócić. W tym celu możemy utworzyć mutowalny (*mutable*)
wektor przed pętlą `for` i wywoływać metodę `push`, aby zapisać `line` w
wektorze. Po pętli `for` zwracamy wektor, jak pokazano w listingu 12-19.

<Listing number="12-19" file-name="src/lib.rs" caption="Przechowywanie pasujących wierszy, aby można je było zwrócić">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-19/src/lib.rs:here}}
```

</Listing>

Teraz funkcja `search` powinna zwracać tylko wiersze zawierające `query`, a nasz
test powinien przejść. Uruchommy test:

```console
{{#include ../listings/ch12-an-io-project/listing-12-19/output.txt}}
```

Nasz test przeszedł, więc wiemy, że kod działa!

Na tym etapie moglibyśmy rozważyć możliwości refaktoryzacji implementacji
funkcji wyszukującej, dbając o to, by testy nadal przechodziły, a
funkcjonalność pozostała taka sama. Kod funkcji wyszukującej nie jest zły, ale
nie wykorzystuje niektórych przydatnych mechanizmów iteratorów. Wrócimy do tego przykładu w
[rozdziale 13][ch13-iterators]<!-- ignore -->, gdzie szczegółowo omówimy
iteratory, i zobaczymy, jak go ulepszyć.

Teraz cały program powinien działać! Wypróbujmy go, najpierw ze słowem, które
powinno zwrócić dokładnie jeden wiersz z utworu Emily Dickinson: _frog_.

```console
{{#include ../listings/ch12-an-io-project/no-listing-02-using-search-in-run/output.txt}}
```

Świetnie! Teraz spróbujmy słowa, które będzie pasować do wielu wierszy, na
przykład _body_:

```console
{{#include ../listings/ch12-an-io-project/output-only-03-multiple-matches/output.txt}}
```

Na koniec upewnijmy się, że nie otrzymamy żadnych wierszy, gdy wyszukamy słowo,
którego nie ma nigdzie w utworze, na przykład _monomorphization_:

```console
{{#include ../listings/ch12-an-io-project/output-only-04-no-matches/output.txt}}
```

Doskonale! Zbudowaliśmy własną miniwersję klasycznego narzędzia i sporo się
nauczyliśmy o strukturyzowaniu aplikacji. Dowiedzieliśmy się też co nieco o
plikowym wejściu i wyjściu, czasach życia, testowaniu oraz parsowaniu wiersza
poleceń.

Na zakończenie tego projektu krótko pokażemy, jak pracować ze zmiennymi
środowiskowymi i jak wypisywać na standardowe wyjście błędów – obie te rzeczy
przydają się przy pisaniu programów wiersza poleceń.

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[ch11-anatomy]: ch11-01-writing-tests.html#the-anatomy-of-a-test-function
[ch10-lifetimes]: ch10-03-lifetime-syntax.html
[ch3-iter]: ch03-05-control-flow.html#looping-through-a-collection-with-for
[ch13-iterators]: ch13-02-iterators.html

# Typy generyczne, traity i czasy życia {#generic-types-traits-and-lifetimes}

Każdy język programowania ma narzędzia do skutecznego radzenia sobie z
powielaniem pojęć. W Ruście jednym z takich narzędzi są _typy generyczne_
(*generics*): abstrakcyjne zamienniki konkretnych typów lub innych właściwości.
Możemy wyrazić zachowanie typów generycznych albo ich związek z innymi typami
generycznymi, nie wiedząc, co znajdzie się na ich miejscu podczas kompilacji i
uruchamiania kodu.

Funkcje mogą przyjmować parametry jakiegoś typu generycznego zamiast
konkretnego typu, takiego jak `i32` czy `String`, podobnie jak przyjmują
parametry o nieznanych wartościach, aby uruchamiać ten sam kod dla wielu
konkretnych wartości. W rzeczywistości używaliśmy już typów generycznych: w
rozdziale 6 z `Option<T>`, w rozdziale 8 z `Vec<T>` i `HashMap<K, V>`, a w
rozdziale 9 z `Result<T, E>`. W tym rozdziale zobaczysz, jak definiować własne
typy, funkcje i metody z użyciem typów generycznych!

Najpierw przypomnimy, jak wyodrębnić funkcję, aby ograniczyć powielanie kodu.
Potem tą samą techniką zrobimy funkcję generyczną z dwóch funkcji, które różnią
się tylko typami parametrów. Wyjaśnimy też, jak używać typów generycznych w
definicjach struktur (*struct*) i *enumów* (typów wyliczeniowych).

Następnie dowiesz się, jak używać _traitów_ (cech typu, zbliżonych do
interfejsu) do definiowania zachowania w sposób generyczny. Traity można łączyć
z typami generycznymi, aby ograniczyć typ generyczny tak, by przyjmował tylko
typy o określonym zachowaniu, a nie dowolny typ.

Na koniec omówimy _czasy życia_ (*lifetimes*): rodzaj typów generycznych, który
przekazuje kompilatorowi informacje o tym, jak referencje mają się do siebie
nawzajem. Czasy życia pozwalają nam dać kompilatorowi wystarczająco dużo
informacji o pożyczonych wartościach, by mógł zagwarantować poprawność
referencji w większej liczbie sytuacji, niż byłoby to możliwe bez naszej
pomocy.

## Usuwanie powielonego kodu przez wyodrębnienie funkcji {#removing-duplication-by-extracting-a-function}

Typy generyczne pozwalają zastąpić konkretne typy symbolem zastępczym
(*placeholder*), który reprezentuje wiele typów, i w ten sposób usunąć powielony
kod. Zanim zagłębimy się w składnię typów generycznych, zobaczmy najpierw, jak
usunąć powielony kod bez typów generycznych: przez wyodrębnienie funkcji, która
zastępuje konkretne wartości symbolem zastępczym reprezentującym wiele wartości.
Potem tą samą techniką wyodrębnimy funkcję generyczną! Ucząc się rozpoznawać
powielony kod, który można wyodrębnić do funkcji, zaczniesz też rozpoznawać
powielony kod, w którym da się użyć typów generycznych.

Zaczniemy od krótkiego programu z listingu 10-1, który znajduje największą
liczbę na liście.

<Listing number="10-1" file-name="src/main.rs" caption="Znajdowanie największej liczby na liście liczb">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-01/src/main.rs:here}}
```

</Listing>

Przechowujemy listę liczb całkowitych w zmiennej `number_list`, a referencję
(*reference*) do pierwszej liczby z listy umieszczamy w zmiennej o nazwie
`largest`. Następnie iterujemy po wszystkich liczbach na liście i jeśli bieżąca
liczba jest większa od liczby zapisanej w `largest`, podmieniamy referencję w
tej zmiennej. Jeśli natomiast bieżąca liczba jest mniejsza od największej
dotąd napotkanej liczby lub jej równa, zmienna się nie zmienia, a kod przechodzi
do następnej liczby na liście. Po przejrzeniu wszystkich liczb `largest` powinna
wskazywać największą liczbę, czyli w tym przypadku 100.

Teraz dostaliśmy zadanie znalezienia największej liczby na dwóch różnych
listach liczb. Możemy w tym celu powielić kod z listingu 10-1 i użyć tej samej
logiki w dwóch miejscach programu, jak pokazuje listing 10-2.

<Listing number="10-2" file-name="src/main.rs" caption="Kod znajdujący największą liczbę na *dwóch* listach liczb">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-02/src/main.rs}}
```

</Listing>

Choć ten kod działa, powielanie kodu jest żmudne i podatne na błędy. Musimy też
pamiętać, by przy każdej zmianie aktualizować kod w wielu miejscach.

Aby wyeliminować to powielanie, utworzymy abstrakcję: zdefiniujemy funkcję,
która działa na dowolnej liście liczb całkowitych przekazanej jako parametr.
Dzięki temu kod staje się czytelniejszy, a pojęcie znajdowania największej
liczby na liście możemy wyrazić abstrakcyjnie.

W listingu 10-3 wyodrębniamy kod znajdujący największą liczbę do funkcji o
nazwie `largest`. Następnie wywołujemy tę funkcję, aby znaleźć największą liczbę
na dwóch listach z listingu 10-2. Moglibyśmy też użyć tej funkcji dla dowolnej
innej listy wartości `i32`, jaką będziemy mieć w przyszłości.

<Listing number="10-3" file-name="src/main.rs" caption="Abstrakcyjny kod znajdujący największą liczbę na dwóch listach">

```rust
{{#rustdoc_include ../listings/ch10-generic-types-traits-and-lifetimes/listing-10-03/src/main.rs:here}}
```

</Listing>

Funkcja `largest` ma parametr o nazwie `list`, który reprezentuje dowolny
konkretny wycinek (*slice*) wartości `i32`, jaki możemy przekazać do funkcji.
W efekcie, gdy wywołujemy funkcję, kod działa na konkretnych wartościach, które
do niej przekazujemy.

Podsumowując, oto kroki, które wykonaliśmy, aby przekształcić kod z listingu
10-2 w kod z listingu 10-3:

1. Zidentyfikuj powielony kod.
1. Wyodrębnij powielony kod do ciała funkcji i określ wejścia oraz wartości
   zwracane tego kodu w sygnaturze funkcji.
1. Zaktualizuj oba miejsca z powielonym kodem tak, aby zamiast tego wywoływały
   funkcję.

Teraz wykonamy te same kroki z użyciem typów generycznych, aby ograniczyć
powielanie kodu. Tak jak ciało funkcji może działać na abstrakcyjnej liście
`list` zamiast na konkretnych wartościach, tak typy generyczne pozwalają kodowi
działać na abstrakcyjnych typach.

Załóżmy na przykład, że mamy dwie funkcje: jedną, która znajduje największy
element w wycinku wartości `i32`, i drugą, która znajduje największy element
w wycinku wartości `char`. Jak wyeliminować to powielanie? Przekonajmy się!

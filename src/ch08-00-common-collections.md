# Popularne kolekcje {#common-collections}

Biblioteka standardowa Rusta zawiera wiele bardzo przydatnych struktur danych
nazywanych _kolekcjami_ (*collections*). Większość innych typów danych
reprezentuje jedną konkretną wartość, kolekcje mogą natomiast zawierać wiele
wartości. W odróżnieniu od wbudowanych typów tablicy i krotki dane, na które
wskazują te kolekcje, są przechowywane na stercie (*heap*). Oznacza to, że ilość
danych nie musi być znana w czasie kompilacji (*compile-time*) i może rosnąć lub
maleć w trakcie działania programu. Każdy rodzaj kolekcji ma inne możliwości i
koszty, a wybór odpowiedniej kolekcji do danej sytuacji to umiejętność, którą
wyrobisz sobie z czasem. W tym rozdziale omówimy trzy kolekcje, których bardzo
często używa się w programach w Ruście:

- _Wektor_ (*vector*) pozwala przechowywać zmienną liczbę wartości obok siebie.
- _Łańcuch znaków_ (*string*) to kolekcja znaków. Typ `String` wspominaliśmy
  już wcześniej, ale w tym rozdziale omówimy go dokładnie.
- _Mapa haszująca_ (*hash map*) pozwala powiązać wartość z określonym kluczem.
  To konkretna implementacja ogólniejszej struktury danych nazywanej _mapą_
  (*map*).

Informacje o innych rodzajach kolekcji udostępnianych przez bibliotekę
standardową znajdziesz w [dokumentacji][collections].

Omówimy, jak tworzyć i aktualizować wektory, łańcuchy znaków i mapy haszujące,
a także co wyróżnia każdą z tych kolekcji.

[collections]: https://doc.rust-lang.org/std/collections/index.html

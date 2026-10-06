# Pisanie testów automatycznych {#writing-automated-tests}

W eseju „The Humble Programmer” z 1972 roku Edsger W. Dijkstra stwierdził, że
„testowanie programów może być bardzo skutecznym sposobem wykazania obecności
błędów, ale jest beznadziejnie niewystarczające do wykazania ich braku”. Nie
znaczy to, że nie powinniśmy starać się testować tak dużo, jak tylko możemy!

_Poprawność_ (*correctness*) programu to stopień, w jakim nasz kod robi to, co
zamierzamy. Rust został zaprojektowany z dużą troską o poprawność programów,
ale poprawność jest złożona i niełatwo jej dowieść. System typów Rusta dźwiga
ogromną część tego ciężaru, ale nie jest w stanie wychwycić wszystkiego.
Dlatego Rust ma wbudowaną obsługę pisania automatycznych testów
oprogramowania.

Załóżmy, że piszemy funkcję `add_two`, która dodaje 2 do dowolnej przekazanej
jej liczby. Sygnatura tej funkcji przyjmuje jako parametr liczbę całkowitą i
zwraca jako wynik liczbę całkowitą. Gdy implementujemy i kompilujemy tę
funkcję, Rust przeprowadza całe sprawdzanie typów i pożyczeń, które już
znasz, aby upewnić się na przykład, że nie przekazujemy do tej funkcji wartości
typu `String` ani nieprawidłowej referencji. Rust _nie jest_ jednak w stanie
sprawdzić, czy ta funkcja zrobi dokładnie to, co zamierzamy, czyli zwróci
parametr powiększony o 2, a nie, powiedzmy, parametr powiększony o 10 albo
pomniejszony o 50! Tu właśnie przydają się testy.

Możemy napisać testy, które sprawdzają na przykład, że gdy przekażemy `3` do
funkcji `add_two`, zwrócona wartość wynosi `5`. Możemy uruchamiać te testy po
każdej zmianie w kodzie, aby upewnić się, że dotychczasowe poprawne zachowanie
się nie zmieniło.

Testowanie to złożona umiejętność. Choć w jednym rozdziale nie omówimy
wszystkich szczegółów pisania dobrych testów, w tym rozdziale przyjrzymy się
mechanizmom testowania dostępnym w Ruście. Omówimy adnotacje i makra, z
których możesz korzystać przy pisaniu testów, domyślne zachowanie i opcje
uruchamiania testów oraz sposób podziału testów na testy jednostkowe i testy
integracyjne.

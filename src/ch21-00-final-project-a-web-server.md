# Projekt końcowy: budujemy wielowątkowy serwer WWW {#final-project-building-a-multithreaded-web-server}

To była długa podróż, ale dotarliśmy do końca książki. W tym rozdziale
zbudujemy razem jeszcze jeden projekt, aby zademonstrować niektóre z pojęć
omówionych w ostatnich rozdziałach i przypomnieć część wcześniejszych lekcji.

W ramach projektu końcowego napiszemy serwer WWW, który mówi „Hello!” i w
przeglądarce wygląda tak jak na rysunku 21-1.

Oto nasz plan budowy serwera WWW:

1. Poznać trochę TCP i HTTP.
2. Nasłuchiwać połączeń TCP na gnieździe.
3. Parsować niewielką liczbę żądań HTTP.
4. Utworzyć poprawną odpowiedź HTTP.
5. Zwiększyć przepustowość serwera za pomocą puli wątków.

<img alt="Zrzut ekranu przeglądarki, która odwiedza adres 127.0.0.1:8080 i wyświetla stronę z tekstem „Hello! Hi from Rust”" src="img/trpl21-01.png" class="center" style="width: 50%;" />

<span class="caption">Rysunek 21-1: Nasz końcowy wspólny projekt</span>

Zanim zaczniemy, wspomnijmy o dwóch rzeczach. Po pierwsze, metoda, której
użyjemy, nie będzie najlepszym sposobem budowania serwera WWW w Ruście.
Członkowie społeczności opublikowali w serwisie [crates.io](https://crates.io/)
wiele gotowych do użytku produkcyjnego *crate’ów* (jednostek kompilacji w
Ruście), które zawierają pełniejsze implementacje serwera WWW i puli wątków niż
ta, którą zbudujemy. Celem tego rozdziału jest jednak pomóc ci się uczyć, a nie
pójść na łatwiznę. Ponieważ Rust jest językiem programowania systemowego,
możemy wybrać poziom abstrakcji, na którym chcemy pracować, i zejść niżej, niż
jest to możliwe lub praktyczne w innych językach.

Po drugie, nie będziemy tu używać async i await. Zbudowanie puli wątków jest
samo w sobie wystarczająco dużym wyzwaniem, nawet bez budowania środowiska
uruchomieniowego (*runtime*) dla kodu asynchronicznego! Zwrócimy jednak uwagę,
jak async i await mogłyby się przydać przy niektórych problemach, które
napotkamy w tym rozdziale. Ostatecznie, jak wspomnieliśmy w rozdziale 17, wiele
środowisk uruchomieniowych dla kodu asynchronicznego zarządza swoją pracą za
pomocą pul wątków.

Dlatego podstawowy serwer HTTP i pulę wątków napiszemy ręcznie, aby poznać
ogólne idee i techniki stojące za crate’ami, których możesz używać w
przyszłości.

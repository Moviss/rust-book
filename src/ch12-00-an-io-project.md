# Projekt wejścia/wyjścia: budujemy program wiersza poleceń {#an-io-project-building-a-command-line-program}

Ten rozdział jest podsumowaniem wielu umiejętności, które udało ci się dotąd
zdobyć, i okazją do poznania kilku kolejnych możliwości biblioteki
standardowej. Zbudujemy narzędzie wiersza poleceń, które korzysta z plików oraz
z wejścia i wyjścia wiersza poleceń, żeby przećwiczyć część poznanych już
koncepcji Rusta.

> **Uwaga:** w tym rozdziale nie ma quizów, ponieważ ma on być jedynie praktycznym przewodnikiem.

Szybkość Rusta, jego bezpieczeństwo, kompilacja do pojedynczego pliku binarnego
i obsługa wielu platform sprawiają, że jest to idealny język do tworzenia
narzędzi wiersza poleceń. W naszym projekcie napiszemy więc własną wersję
klasycznego narzędzia wyszukiwania `grep` (**g**lobally search a **r**egular
**e**xpression and **p**rint). W najprostszym przypadku `grep` przeszukuje
wskazany plik pod kątem wskazanego łańcucha znaków (*string*). W tym celu
`grep` przyjmuje jako argumenty ścieżkę do pliku i łańcuch. Następnie odczytuje
plik, znajduje w nim wiersze zawierające podany łańcuch i je wypisuje.

Przy okazji pokażemy, jak sprawić, żeby nasze narzędzie korzystało z
możliwości terminala, z których korzysta wiele innych narzędzi wiersza
poleceń. Odczytamy wartość zmiennej środowiskowej, żeby użytkownik mógł
skonfigurować działanie naszego narzędzia. Komunikaty o błędach będziemy też
wypisywać na standardowe wyjście błędów (`stderr`) zamiast na standardowe
wyjście (`stdout`), dzięki czemu użytkownik może na przykład przekierować
poprawne wyniki do pliku, a komunikaty o błędach nadal widzieć na ekranie.

Andrew Gallant, członek społeczności Rusta, stworzył już w pełni funkcjonalną,
bardzo szybką wersję `grep` o nazwie `ripgrep`. Nasza wersja będzie w
porównaniu z nią dość prosta, ale ten rozdział da ci część wiedzy potrzebnej do
zrozumienia prawdziwego projektu takiego jak `ripgrep`.

Nasz projekt `grep` połączy wiele poznanych dotąd koncepcji:

- organizowanie kodu ([rozdział 7][ch7]<!-- ignore -->);
- używanie wektorów (*vector*) i łańcuchów znaków ([rozdział 8][ch8]<!-- ignore -->);
- obsługę błędów ([rozdział 9][ch9]<!-- ignore -->);
- używanie traitów (*trait*, cech typów, zbliżonych do interfejsów) i czasów życia (*lifetime*) tam, gdzie to stosowne ([rozdział 10][ch10]<!-- ignore -->);
- pisanie testów ([rozdział 11][ch11]<!-- ignore -->).

Krótko przedstawimy też domknięcia (*closure*), iteratory i obiekty traitów
(*trait object*), które szczegółowo omówią [rozdział 13][ch13]<!-- ignore --> i
[rozdział 18][ch18]<!-- ignore -->.

[ch7]: ch07-00-managing-growing-projects-with-packages-crates-and-modules.html
[ch8]: ch08-00-common-collections.html
[ch9]: ch09-00-error-handling.html
[ch10]: ch10-00-generics.html
[ch11]: ch11-00-testing.html
[ch13]: ch13-00-functional-features.html
[ch18]: ch18-00-oop.html

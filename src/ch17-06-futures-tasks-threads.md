## Wszystko razem: future’y, zadania i wątki {#putting-it-all-together-futures-tasks-and-threads}

Jak widzieliśmy w [rozdziale 16][ch16]<!-- ignore -->, wątki to jedno z podejść
do współbieżności (*concurrency*). W tym rozdziale poznaliśmy inne: async z
*future*’ami (wartościami, które będą gotowe później) i strumieniami
(*stream*). Jeśli zastanawiasz się, kiedy wybrać jedną metodę, a kiedy drugą,
odpowiedź brzmi: to zależy! W wielu przypadkach wybór nie sprowadza się do
„wątki _albo_ async”, lecz raczej „wątki _i_ async”.

Wiele systemów operacyjnych od dziesięcioleci udostępnia modele współbieżności
oparte na wątkach, dlatego obsługuje je wiele języków programowania. Modele te
nie są jednak wolne od kompromisów. W wielu systemach operacyjnych każdy wątek
zużywa sporo pamięci. Wątki wchodzą też w grę tylko wtedy, gdy obsługują je
system operacyjny i sprzęt. W odróżnieniu od popularnych komputerów
stacjonarnych i urządzeń mobilnych niektóre systemy wbudowane w ogóle nie mają
systemu operacyjnego, więc nie mają też wątków.

Model async oferuje inny – i ostatecznie uzupełniający – zestaw kompromisów. W
modelu async operacje współbieżne nie potrzebują własnych wątków. Zamiast tego
mogą działać w ramach zadań, tak jak wtedy, gdy w podrozdziale o strumieniach
użyliśmy `trpl::spawn_task`, aby rozpocząć pracę z poziomu funkcji
synchronicznej. Zadanie przypomina wątek, ale zamiast przez system operacyjny
jest zarządzane przez kod na poziomie biblioteki: środowisko uruchomieniowe
(*runtime*).

Nie bez powodu API do tworzenia wątków i tworzenia zadań są tak podobne. Wątki
wyznaczają granicę dla zbiorów operacji synchronicznych; współbieżność jest
możliwa _między_ wątkami. Zadania wyznaczają granicę dla zbiorów operacji
_asynchronicznych_; współbieżność jest możliwa zarówno _między_ zadaniami, jak i
_wewnątrz_ nich, ponieważ zadanie może przełączać się między future’ami w swoim
ciele. Wreszcie future’y są w Ruście najdrobniejszą jednostką współbieżności, a
każdy future może reprezentować całe drzewo innych future’ów. Środowisko
uruchomieniowe – a konkretnie jego egzekutor (*executor*) – zarządza
zadaniami, a zadania zarządzają future’ami. Pod tym względem zadania przypominają lekkie wątki zarządzane przez środowisko
uruchomieniowe, z dodatkowymi możliwościami wynikającymi z tego, że zarządza
nimi środowisko uruchomieniowe, a nie system operacyjny.

Nie znaczy to, że zadania async są zawsze lepsze od wątków (ani odwrotnie).
Współbieżność oparta na wątkach jest pod pewnymi względami prostszym modelem
programowania niż współbieżność z `async`. Może to być zaletą albo wadą. Wątki
działają w pewnym sensie na zasadzie „odpal i zapomnij”; nie mają natywnego
odpowiednika future’a, więc po prostu wykonują się do końca, a przerwać je może
tylko sam system operacyjny.

Okazuje się też, że wątki i zadania często bardzo dobrze ze sobą
współpracują, ponieważ zadania można (przynajmniej w niektórych środowiskach
uruchomieniowych) przenosić między wątkami. W rzeczywistości środowisko
uruchomieniowe, którego używamy – łącznie z funkcjami `spawn_blocking` i
`spawn_task` – jest pod spodem domyślnie wielowątkowe! Wiele środowisk
uruchomieniowych stosuje podejście zwane _kradzieżą pracy_ (*work stealing*),
aby niezauważalnie przenosić zadania między wątkami w zależności od bieżącego
obciążenia wątków i w ten sposób poprawiać ogólną wydajność systemu. To
podejście w rzeczywistości wymaga wątków _i_ zadań, a zatem także future’ów.

Zastanawiając się, której metody użyć w danej sytuacji, kieruj się tymi
praktycznymi wskazówkami:

- Jeśli praca _dobrze się zrównolegla_ (czyli jest ograniczona przez procesor),
  na przykład przetwarzanie dużej ilości danych, w której każdą część można
  przetworzyć osobno, lepszym wyborem są wątki.
- Jeśli praca jest _silnie współbieżna_ (czyli ograniczona przez
  wejście-wyjście), na przykład obsługa komunikatów z wielu różnych źródeł,
  które mogą napływać w różnych odstępach czasu lub z różną częstotliwością,
  lepszym wyborem jest async.

A jeśli potrzebujesz zarówno równoległości (*parallelism*), jak i
współbieżności, nie musisz wybierać między wątkami a async. Możesz swobodnie
używać ich razem, pozwalając każdemu z nich robić to, w czym sprawdza się
najlepiej. Listing 17-25 pokazuje na przykład dość typowe połączenie tego
rodzaju w rzeczywistym kodzie w Ruście.

<Listing number="17-25" caption="Wysyłanie komunikatów za pomocą blokującego kodu w wątku i oczekiwanie na komunikaty w bloku async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-25/src/main.rs:all}}
```

</Listing>

Zaczynamy od utworzenia kanału asynchronicznego, a następnie tworzymy wątek,
który za pomocą słowa kluczowego (*keyword*) `move` przejmuje własność
(*ownership*) strony nadawczej kanału. W wątku wysyłamy liczby od 1 do 10,
usypiając go na sekundę między kolejnymi wysłaniami. Na koniec uruchamiamy
future utworzony z bloku async przekazanego do `trpl::block_on`, tak jak przez
cały ten rozdział. W tym future’ze oczekujemy na te komunikaty, tak jak w innych
przykładach przekazywania komunikatów (*message passing*), które widzieliśmy.

Wracając do scenariusza, od którego zaczęliśmy ten rozdział, wyobraź sobie, że
uruchamiasz zestaw zadań kodowania wideo w dedykowanym wątku (bo kodowanie
wideo jest ograniczone przez obliczenia), ale o zakończeniu tych operacji
powiadamiasz interfejs użytkownika za pomocą kanału asynchronicznego. W
rzeczywistych zastosowaniach takich połączeń są niezliczone przykłady.

## Podsumowanie {#summary}

To nie ostatnie spotkanie ze współbieżnością w tej książce. Projekt z
[rozdziału 21][ch21]<!-- ignore --> zastosuje te koncepcje w bardziej
realistycznej sytuacji niż omówione tu proste przykłady i bezpośrednio porówna
rozwiązywanie problemów za pomocą wątków oraz za pomocą zadań i future’ów.

Niezależnie od tego, które z tych podejść wybierzesz, Rust daje ci narzędzia
potrzebne do pisania bezpiecznego, szybkiego, współbieżnego kodu – czy to dla
serwera WWW o dużej przepustowości, czy dla wbudowanego systemu operacyjnego.

W następnym rozdziale omówimy idiomatyczne sposoby modelowania problemów i
strukturyzowania rozwiązań, gdy twoje programy w Ruście stają się coraz
większe. Omówimy też, jak idiomy Rusta mają się do tych, które możesz znać z
programowania obiektowego.

[ch16]: http://localhost:3000/ch16-00-concurrency.html
[combining-futures]: ch17-03-more-futures.html#building-our-own-async-abstractions
[streams]: ch17-04-streams.html#composing-streams
[ch21]: ch21-00-final-project-a-web-server.html

<!-- Old headings. Do not remove or links may break. -->

<a id="turning-our-single-threaded-server-into-a-multithreaded-server"></a>
<a id="from-single-threaded-to-multithreaded-server"></a>

## Od serwera jednowątkowego do wielowątkowego {#from-a-single-threaded-to-a-multithreaded-server}

Obecnie serwer przetwarza żądania po kolei, co oznacza, że nie zajmie się drugim
połączeniem, dopóki nie skończy przetwarzać pierwszego. Gdyby serwer otrzymywał
coraz więcej żądań, takie szeregowe wykonywanie byłoby coraz mniej optymalne.
Jeśli serwer otrzyma żądanie, którego przetworzenie trwa długo, kolejne żądania
będą musiały czekać, aż długie żądanie się zakończy, nawet jeśli nowe żądania
dałoby się obsłużyć szybko. Trzeba to naprawić, ale najpierw zobaczmy ten problem w
praktyce.

<!-- Old headings. Do not remove or links may break. -->

<a id="simulating-a-slow-request-in-the-current-server-implementation"></a>

### Symulowanie wolnego żądania {#simulating-a-slow-request}

Sprawdzimy, jak wolno przetwarzane żądanie może wpłynąć na inne żądania
kierowane do obecnej implementacji naszego serwera. Listing 21-10 implementuje
obsługę żądania do _/sleep_ z symulowaną wolną odpowiedzią: przed odpowiedzią
serwer zasypia na pięć sekund.

<Listing number="21-10" file-name="src/main.rs" caption="Symulowanie wolnego żądania przez uśpienie na pięć sekund">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-10/src/main.rs:here}}
```

</Listing>

Skoro mamy już trzy przypadki, zamieniliśmy `if` na `match`. Musimy jawnie
dopasowywać wycinek (*slice*) `request_line`, aby porównać go ze wzorcami
będącymi wartościami literałów łańcuchowych; `match` nie wykonuje automatycznie
tworzenia referencji ani dereferencji (*dereference*), tak jak robi to metoda
porównująca równość.

Pierwsze ramię (*arm*) jest takie samo jak blok `if` z listingu 21-9. Drugie
ramię dopasowuje żądanie do _/sleep_. Po otrzymaniu takiego żądania serwer
zasypia na pięć sekund, zanim wyrenderuje stronę HTML informującą o sukcesie.
Trzecie ramię jest takie samo jak blok `else` z listingu 21-9.

Widać, jak prymitywny jest nasz serwer: prawdziwe biblioteki rozpoznawałyby
różne żądania w znacznie mniej rozwlekły sposób!

Uruchom serwer poleceniem `cargo run`. Następnie otwórz dwa okna przeglądarki:
jedno dla _http://127.0.0.1:7878_, a drugie dla _http://127.0.0.1:7878/sleep_.
Jeśli kilka razy wpiszesz URI _/_, tak jak wcześniej, zobaczysz, że serwer
odpowiada szybko. Ale jeśli wpiszesz _/sleep_, a potem wczytasz _/_, zobaczysz,
że _/_ czeka, aż `sleep` prześpi pełne pięć sekund, i dopiero wtedy się wczytuje.

Istnieje wiele technik, dzięki którym żądania nie gromadziłyby się za wolnym
żądaniem, w tym użycie async, tak jak zrobiliśmy to w rozdziale 17; my
zaimplementujemy pulę wątków (*thread pool*).

### Zwiększanie przepustowości za pomocą puli wątków {#improving-throughput-with-a-thread-pool}

_Pula wątków_ to grupa utworzonych wątków, które są gotowe i czekają na
obsłużenie zadania. Gdy program otrzymuje nowe zadanie, przydziela do niego
jeden z wątków z puli i ten wątek je przetwarza. Pozostałe wątki w puli mogą
obsługiwać inne zadania, które nadejdą, gdy pierwszy wątek jest zajęty. Kiedy
pierwszy wątek skończy przetwarzać swoje zadanie, wraca do puli bezczynnych
wątków, gotowy obsłużyć nowe zadanie. Pula wątków pozwala przetwarzać
połączenia współbieżnie, co zwiększa przepustowość serwera.

Ograniczymy liczbę wątków w puli do niewielkiej wartości, aby chronić się przed
atakami DoS; gdyby nasz program tworzył nowy wątek dla każdego nadchodzącego
żądania, ktoś wysyłający do serwera 10 milionów żądań mógłby narobić
spustoszenia, zużywając wszystkie zasoby serwera i całkowicie wstrzymując
przetwarzanie żądań.

Zamiast więc tworzyć nieograniczoną liczbę wątków, w puli będzie czekać stała
liczba wątków. Nadchodzące żądania są wysyłane do puli do przetworzenia. Pula
utrzymuje kolejkę nadchodzących żądań. Każdy z wątków w puli zdejmuje żądanie z
tej kolejki, obsługuje je, a potem prosi kolejkę o następne. Przy takim
projekcie możemy przetwarzać współbieżnie do _`N`_ żądań, gdzie _`N`_ to liczba
wątków. Jeśli każdy wątek odpowiada na długo trwające żądanie, kolejne żądania
nadal mogą gromadzić się w kolejce, ale zwiększyliśmy liczbę długich żądań,
które możemy obsłużyć, zanim do tego dojdzie.

Ta technika to tylko jeden z wielu sposobów na zwiększenie przepustowości
serwera WWW. Inne opcje, którym możesz się przyjrzeć, to model fork/join,
jednowątkowy model asynchronicznego wejścia-wyjścia i wielowątkowy model
asynchronicznego wejścia-wyjścia. Jeśli interesuje cię ten temat, możesz
poczytać więcej o innych rozwiązaniach i spróbować je zaimplementować; w
języku niskopoziomowym takim jak Rust wszystkie te opcje są możliwe.

Zanim zaczniemy implementować pulę wątków, zastanówmy się, jak powinno
wyglądać korzystanie z niej. Gdy projektujesz kod, napisanie najpierw
interfejsu klienta może ukierunkować projekt. Napisz API kodu tak, by miało
strukturę odpowiadającą temu, jak chcesz go wywoływać; potem zaimplementuj
funkcjonalność w ramach tej struktury, zamiast najpierw implementować
funkcjonalność, a dopiero potem projektować publiczne API.

Podobnie jak w projekcie z rozdziału 12 stosowaliśmy programowanie sterowane
testami (*test-driven development*, TDD), tutaj zastosujemy programowanie
sterowane kompilatorem (*compiler-driven development*). Napiszemy kod, który
wywołuje potrzebne nam funkcje, a potem przyjrzymy się błędom kompilatora, aby
ustalić, co zmienić dalej, żeby kod zadziałał. Zanim to jednak zrobimy, jako
punkt wyjścia przyjrzymy się technice, której nie zamierzamy użyć.

<!-- Old headings. Do not remove or links may break. -->

<a id="code-structure-if-we-could-spawn-a-thread-for-each-request"></a>

#### Tworzenie wątku dla każdego żądania {#spawning-a-thread-for-each-request}

Najpierw zobaczmy, jak mógłby wyglądać nasz kod, gdyby rzeczywiście tworzył
nowy wątek dla każdego połączenia. Jak wspomnieliśmy wcześniej, nie jest to
nasz docelowy plan ze względu na problemy związane z potencjalnie
nieograniczoną liczbą tworzonych wątków, ale to punkt wyjścia do uzyskania
najpierw działającego serwera wielowątkowego. Potem dodamy pulę wątków jako
ulepszenie i łatwiej będzie porównać oba rozwiązania.

Listing 21-11 pokazuje zmiany w `main`, dzięki którym w pętli `for` dla każdego
strumienia tworzony jest nowy wątek, który go obsługuje.

<Listing number="21-11" file-name="src/main.rs" caption="Tworzenie nowego wątku dla każdego strumienia">

```rust,no_run
{{#rustdoc_include ../listings/ch21-web-server/listing-21-11/src/main.rs:here}}
```

</Listing>

Jak wiesz z rozdziału 16, `thread::spawn` tworzy nowy wątek, a następnie
uruchamia w nim kod z domknięcia (*closure*). Jeśli uruchomisz ten kod i
wczytasz w przeglądarce _/sleep_, a potem _/_ w dwóch kolejnych kartach,
zobaczysz, że żądania do _/_ rzeczywiście nie muszą czekać na zakończenie
_/sleep_. Jednak, jak wspomnieliśmy, w końcu przeciąży to system, ponieważ
tworzysz nowe wątki bez żadnego limitu.

Być może pamiętasz też z rozdziału 17, że to dokładnie taka sytuacja, w której
async i await naprawdę błyszczą! Miej to na uwadze, gdy będziemy budować pulę
wątków, i zastanów się, co wyglądałoby inaczej, a co tak samo, gdybyśmy użyli
async.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-a-similar-interface-for-a-finite-number-of-threads"></a>

#### Tworzenie skończonej liczby wątków {#creating-a-finite-number-of-threads}

Chcemy, aby nasza pula wątków działała w podobny, znajomy sposób, tak by
przejście z wątków na pulę wątków nie wymagało dużych zmian w kodzie
korzystającym z naszego API. Listing 21-12 pokazuje hipotetyczny interfejs
struktury (*struct*) `ThreadPool`, której chcemy użyć zamiast `thread::spawn`.

<Listing number="21-12" file-name="src/main.rs" caption="Nasz idealny interfejs `ThreadPool`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-12/src/main.rs:here}}
```

</Listing>

Używamy `ThreadPool::new`, aby utworzyć nową pulę wątków z konfigurowalną
liczbą wątków, w tym przypadku czterema. Następnie w pętli `for` wywołanie
`pool.execute` ma interfejs podobny do `thread::spawn`: przyjmuje domknięcie,
które pula powinna uruchomić dla każdego strumienia. Musimy zaimplementować
`pool.execute` tak, aby przyjmowało domknięcie i przekazywało je do
uruchomienia jednemu z wątków w puli. Ten kod jeszcze się nie skompiluje, ale
spróbujemy, żeby kompilator podpowiedział nam, jak go naprawić.

<!-- Old headings. Do not remove or links may break. -->

<a id="building-the-threadpool-struct-using-compiler-driven-development"></a>

#### Budowanie `ThreadPool` metodą programowania sterowanego kompilatorem {#building-threadpool-using-compiler-driven-development}

Wprowadź zmiany z listingu 21-12 do _src/main.rs_, a następnie pozwólmy, by
błędy kompilatora zgłaszane przez `cargo check` kierowały naszą pracą. Oto
pierwszy błąd, jaki otrzymujemy:

```console
{{#include ../listings/ch21-web-server/listing-21-12/output.txt}}
```

Świetnie! Ten błąd mówi, że potrzebujemy typu lub modułu `ThreadPool`, więc
teraz go zbudujemy. Nasza implementacja `ThreadPool` będzie niezależna od
rodzaju pracy, jaką wykonuje serwer WWW. Zmieńmy więc *crate* (jednostkę
kompilacji w Ruście) `hello` z crate’a binarnego na crate biblioteczny, który
będzie zawierał implementację `ThreadPool`. Po przejściu na crate biblioteczny
moglibyśmy też używać tej osobnej biblioteki puli wątków do dowolnej pracy
wymagającej puli wątków, nie tylko do obsługi żądań sieciowych.

Utwórz plik _src/lib.rs_ z następującą zawartością – to najprostsza definicja
struktury `ThreadPool`, jaką na razie możemy mieć:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/lib.rs}}
```

</Listing>


Następnie zmodyfikuj plik _main.rs_, aby wprowadzić `ThreadPool` z crate’a
bibliotecznego do zasięgu (*scope*), dodając następujący kod na początku
_src/main.rs_:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/src/main.rs:here}}
```

</Listing>

Ten kod nadal nie zadziała, ale sprawdźmy go ponownie, aby zobaczyć kolejny
błąd, którym musimy się zająć:

```console
{{#include ../listings/ch21-web-server/no-listing-01-define-threadpool-struct/output.txt}}
```

Ten błąd wskazuje, że teraz musimy utworzyć dla `ThreadPool` funkcję powiązaną
(*associated function*) o nazwie `new`. Wiemy też, że `new` musi mieć jeden
parametr, który przyjmie `4` jako argument, i powinna zwracać instancję
`ThreadPool`. Zaimplementujmy najprostszą funkcję `new` o tych cechach:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/src/lib.rs}}
```

</Listing>

Wybraliśmy `usize` jako typ parametru `size`, ponieważ wiemy, że ujemna liczba
wątków nie ma sensu. Wiemy też, że użyjemy tego `4` jako liczby elementów w
kolekcji wątków, a do tego właśnie służy typ `usize`, jak omówiliśmy w
podrozdziale [„Typy całkowitoliczbowe”][integer-types]<!--
ignore --> w rozdziale 3.

Sprawdźmy kod ponownie:

```console
{{#include ../listings/ch21-web-server/no-listing-02-impl-threadpool-new/output.txt}}
```

Tym razem błąd wynika z tego, że `ThreadPool` nie ma metody `execute`.
Przypomnij sobie z podrozdziału [„Tworzenie skończonej liczby wątków”](#creating-a-finite-number-of-threads)<!-- ignore -->,
że zdecydowaliśmy, iż nasza pula wątków powinna mieć interfejs podobny do
`thread::spawn`. Ponadto zaimplementujemy funkcję `execute` tak, aby
przyjmowała otrzymane domknięcie i przekazywała je do uruchomienia
bezczynnemu wątkowi w puli.

Zdefiniujemy w `ThreadPool` metodę `execute`, która przyjmuje domknięcie jako
parametr. Przypomnij sobie z podrozdziału [„Przenoszenie przechwyconych wartości z domknięć”][moving-out-of-closures]<!-- ignore -->
w rozdziale 13, że domknięcia możemy przyjmować jako parametry za pomocą trzech
różnych *traitów* (cech typów, zbliżonych do interfejsów): `Fn`, `FnMut` i
`FnOnce`. Musimy zdecydować, którego rodzaju domknięcia tu użyć. Wiemy, że
ostatecznie zrobimy coś podobnego do implementacji `thread::spawn` z
biblioteki standardowej, więc możemy sprawdzić, jakie ograniczenia sygnatura
`thread::spawn` nakłada na swój parametr. Dokumentacja pokazuje nam:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Interesuje nas tu parametr typu `F`; parametr typu `T` dotyczy wartości
zwracanej i nim się nie zajmujemy. Widzimy, że `spawn` używa `FnOnce` jako
ograniczenia traitu (*trait bound*) dla `F`. Prawdopodobnie tego samego
chcemy i my, ponieważ ostatecznie przekażemy argument otrzymany w `execute` do
`spawn`. Możemy być jeszcze bardziej pewni, że `FnOnce` to trait, którego
chcemy użyć, ponieważ wątek uruchamiający żądanie wykona domknięcie tego
żądania tylko raz, co pasuje do `Once` w `FnOnce`.

Parametr typu `F` ma też ograniczenie traitu `Send` i ograniczenie czasu życia
(*lifetime*) `'static`, które przydają się w naszej sytuacji: potrzebujemy
`Send`, aby przenieść domknięcie z jednego wątku do drugiego, oraz `'static`,
ponieważ nie wiemy, ile czasu zajmie wątkowi wykonanie. Utwórzmy w
`ThreadPool` metodę `execute`, która przyjmie generyczny parametr typu `F` z
tymi ograniczeniami:

<Listing file-name="src/lib.rs">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/no-listing-03-define-execute/src/lib.rs:here}}
```

</Listing>

Nadal używamy `()` po `FnOnce`, ponieważ to `FnOnce` reprezentuje domknięcie,
które nie przyjmuje parametrów i zwraca typ jednostkowy (*unit type*) `()`.
Podobnie jak w definicjach funkcji, typ zwracany można pominąć w sygnaturze,
ale nawet jeśli nie mamy parametrów, nadal potrzebujemy nawiasów.

Znów jest to najprostsza implementacja metody `execute`: nie robi nic, ale
chcemy tylko, żeby nasz kod się skompilował. Sprawdźmy go ponownie:

```console
{{#include ../listings/ch21-web-server/no-listing-03-define-execute/output.txt}}
```

Kompiluje się! Zauważ jednak, że jeśli spróbujesz `cargo run` i wyślesz
żądanie z przeglądarki, zobaczysz w niej te same błędy, które widzieliśmy na
początku rozdziału. Nasza biblioteka jeszcze w ogóle nie wywołuje domknięcia
przekazanego do `execute`!

> Uwaga: o językach z rygorystycznymi kompilatorami, takich jak Haskell i Rust,
> można usłyszeć powiedzenie: „Jeśli kod się kompiluje, to działa”. To
> powiedzenie nie zawsze jest jednak prawdziwe. Nasz projekt się kompiluje, ale
> nie robi absolutnie nic! Gdybyśmy budowali prawdziwy, kompletny projekt, byłby
> to dobry moment, by zacząć pisać testy jednostkowe sprawdzające, czy kod się
> kompiluje _i_ zachowuje się tak, jak chcemy.

Zastanów się: co byłoby tu inaczej, gdybyśmy zamiast domknięcia mieli wykonać
*future* (wartość, która będzie gotowa później)?

#### Walidacja liczby wątków w `new` {#validating-the-number-of-threads-in-new}

Nie robimy nic z parametrami `new` i `execute`. Zaimplementujmy treść tych
funkcji tak, by zachowywały się zgodnie z naszymi oczekiwaniami. Na początek
zastanówmy się nad `new`. Wcześniej wybraliśmy dla parametru `size` typ bez
znaku, ponieważ pula z ujemną liczbą wątków nie ma sensu. Jednak pula z zerową
liczbą wątków również nie ma sensu, a zero jest całkowicie poprawną wartością
`usize`. Dodamy kod sprawdzający, czy `size` jest większe od zera, zanim
zwrócimy instancję `ThreadPool`, i sprawimy, że program spanikuje (*panic*),
jeśli otrzyma zero, używając makra `assert!`, jak pokazano w listingu 21-13.

<Listing number="21-13" file-name="src/lib.rs" caption="Implementacja `ThreadPool::new`, która panikuje, gdy `size` wynosi zero">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-13/src/lib.rs:here}}
```

</Listing>

Dodaliśmy też trochę dokumentacji do naszej `ThreadPool` za pomocą komentarzy
dokumentacyjnych. Zauważ, że zastosowaliśmy dobre praktyki dokumentowania,
dodając sekcję, która wymienia sytuacje, w których nasza funkcja może wywołać
panikę, jak omówiliśmy w rozdziale 14. Spróbuj uruchomić
`cargo doc --open` i kliknąć strukturę `ThreadPool`, aby zobaczyć, jak wygląda
wygenerowana dokumentacja dla `new`!

Zamiast dodawać makro `assert!`, tak jak zrobiliśmy tutaj, moglibyśmy zmienić
`new` na `build` i zwracać `Result`, podobnie jak zrobiliśmy z `Config::build`
w projekcie wejścia-wyjścia w listingu 12-9. Uznaliśmy jednak, że w tym
przypadku próba utworzenia puli wątków bez żadnych wątków powinna być błędem
nieodwracalnym (*unrecoverable error*). Jeśli czujesz się na siłach, spróbuj
napisać funkcję o nazwie `build` z następującą sygnaturą, aby porównać ją
z funkcją `new`:

```rust,ignore
pub fn build(size: usize) -> Result<ThreadPool, PoolCreationError> {
```

#### Tworzenie miejsca na przechowywanie wątków {#creating-space-to-store-the-threads}

Skoro mamy już sposób, by upewnić się, że liczba wątków do przechowania w puli
jest poprawna, możemy utworzyć te wątki i zapisać je w strukturze `ThreadPool`,
zanim ją zwrócimy. Ale jak „przechować” wątek? Przyjrzyjmy się jeszcze raz
sygnaturze `thread::spawn`:

```rust,ignore
pub fn spawn<F, T>(f: F) -> JoinHandle<T>
    where
        F: FnOnce() -> T,
        F: Send + 'static,
        T: Send + 'static,
```

Funkcja `spawn` zwraca `JoinHandle<T>`, gdzie `T` to typ zwracany przez
domknięcie. Spróbujmy również użyć `JoinHandle` i zobaczmy, co się stanie. W
naszym przypadku domknięcia przekazywane do puli wątków będą obsługiwać
połączenie i niczego nie zwracają, więc `T` będzie typem jednostkowym `()`.

Kod z listingu 21-14 się skompiluje, ale nie tworzy jeszcze żadnych wątków.
Zmieniliśmy definicję `ThreadPool` tak, by przechowywała wektor (*vector*)
instancji `thread::JoinHandle<()>`, zainicjalizowaliśmy wektor z pojemnością
`size`, przygotowaliśmy pętlę `for`, która uruchomi kod tworzący wątki, i
zwróciliśmy instancję `ThreadPool`, która je zawiera.

<Listing number="21-14" file-name="src/lib.rs" caption="Tworzenie wektora, w którym `ThreadPool` przechowuje wątki">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-14/src/lib.rs:here}}
```

</Listing>

Wprowadziliśmy `std::thread` do zasięgu w crate’cie bibliotecznym, ponieważ
używamy `thread::JoinHandle` jako typu elementów wektora w `ThreadPool`.

Po otrzymaniu poprawnego rozmiaru nasza `ThreadPool` tworzy nowy wektor, który
może pomieścić `size` elementów. Funkcja `with_capacity` wykonuje to samo
zadanie co `Vec::new`, ale z jedną ważną różnicą: z góry alokuje miejsce w
wektorze. Ponieważ wiemy, że musimy przechować w wektorze `size` elementów,
wykonanie tej alokacji z wyprzedzeniem jest nieco wydajniejsze niż użycie
`Vec::new`, który zmienia swój rozmiar w miarę wstawiania elementów.

Gdy ponownie uruchomisz `cargo check`, polecenie powinno zakończyć się
powodzeniem.

<!-- Old headings. Do not remove or links may break. -->
<a id ="a-worker-struct-responsible-for-sending-code-from-the-threadpool-to-a-thread"></a>

#### Wysyłanie kodu z `ThreadPool` do wątku {#sending-code-from-the-threadpool-to-a-thread}

W pętli `for` w listingu 21-14 zostawiliśmy komentarz dotyczący tworzenia
wątków. Teraz zobaczymy, jak faktycznie tworzyć wątki. Biblioteka standardowa
udostępnia do tworzenia wątków `thread::spawn`, a `thread::spawn` oczekuje
kodu, który wątek ma uruchomić, gdy tylko zostanie utworzony. W naszym
przypadku chcemy jednak utworzyć wątki i sprawić, by _czekały_ na kod, który
wyślemy później. Implementacja wątków w bibliotece standardowej nie daje
żadnej możliwości zrobienia tego; musimy zaimplementować to ręcznie.

Zaimplementujemy to zachowanie, wprowadzając między `ThreadPool` a wątkami
nową strukturę danych, która będzie nim zarządzać. Nazwiemy ją _Worker_
(pracownik) – to popularne określenie w implementacjach pul. `Worker` pobiera
kod, który trzeba uruchomić, i uruchamia go w swoim wątku.

Pomyśl o ludziach pracujących w kuchni restauracji: pracownicy czekają, aż
nadejdą zamówienia od klientów, a potem odpowiadają za ich przyjęcie i
realizację.

Zamiast przechowywać w puli wątków wektor instancji `JoinHandle<()>`, będziemy
przechowywać instancje struktury `Worker`. Każdy `Worker` będzie przechowywał
jedną instancję `JoinHandle<()>`. Następnie zaimplementujemy w `Worker` metodę,
która przyjmie domknięcie z kodem do uruchomienia i wyśle je do wykonania do
już działającego wątku. Każdemu `Worker` nadamy też `id`, abyśmy podczas
logowania lub debugowania mogli odróżnić od siebie poszczególne instancje
`Worker` w puli.

Oto nowy proces, który będzie przebiegał przy tworzeniu `ThreadPool`. Kod
wysyłający domknięcie do wątku zaimplementujemy, gdy już przygotujemy `Worker`
w ten sposób:

1. Zdefiniuj strukturę `Worker`, która przechowuje `id` i `JoinHandle<()>`.
2. Zmień `ThreadPool` tak, by przechowywała wektor instancji `Worker`.
3. Zdefiniuj funkcję `Worker::new`, która przyjmuje liczbę `id` i zwraca
   instancję `Worker` przechowującą `id` oraz wątek utworzony z pustym
   domknięciem.
4. W `ThreadPool::new` użyj licznika pętli `for` do wygenerowania `id`, utwórz
   nowy `Worker` z tym `id` i zapisz `Worker` w wektorze.

Jeśli lubisz wyzwania, spróbuj samodzielnie wprowadzić te zmiany, zanim
zajrzysz do kodu w listingu 21-15.

Gotowe? Oto listing 21-15 z jednym ze sposobów wprowadzenia powyższych zmian.

<Listing number="21-15" file-name="src/lib.rs" caption="Modyfikacja `ThreadPool` tak, by przechowywała instancje `Worker` zamiast bezpośrednio wątków">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-15/src/lib.rs:here}}
```

</Listing>

Zmieniliśmy nazwę pola w `ThreadPool` z `threads` na `workers`, ponieważ
przechowuje ono teraz instancje `Worker` zamiast instancji `JoinHandle<()>`.
Licznika z pętli `for` używamy jako argumentu `Worker::new` i każdy nowy
`Worker` zapisujemy w wektorze o nazwie `workers`.

Kod zewnętrzny (taki jak nasz serwer w _src/main.rs_) nie musi znać szczegółów
implementacji związanych z użyciem struktury `Worker` wewnątrz `ThreadPool`,
więc strukturę `Worker` i jej funkcję `new` czynimy prywatnymi. Funkcja
`Worker::new` używa przekazanego jej `id` i przechowuje instancję
`JoinHandle<()>` utworzoną przez uruchomienie nowego wątku z pustym
domknięciem.

> Uwaga: jeśli system operacyjny nie może utworzyć wątku z powodu braku
> zasobów systemowych, `thread::spawn` spanikuje. Spowoduje to panikę całego
> serwera, nawet jeśli utworzenie niektórych wątków mogłoby się powieść. Dla
> uproszczenia takie zachowanie jest w porządku, ale w produkcyjnej
> implementacji puli wątków prawdopodobnie lepiej byłoby użyć
> [`std::thread::Builder`][builder]<!-- ignore --> i jego metody
> [`spawn`][builder-spawn]<!-- ignore -->, która zamiast tego zwraca `Result`.

Ten kod się skompiluje i będzie przechowywał tyle instancji `Worker`, ile
podaliśmy jako argument `ThreadPool::new`. Ale _nadal_ nie przetwarzamy
domknięcia, które otrzymujemy w `execute`. Zobaczmy teraz, jak to zrobić.

#### Wysyłanie żądań do wątków przez kanały {#sending-requests-to-threads-via-channels}

Następny problem, którym się zajmiemy, polega na tym, że domknięcia
przekazywane do `thread::spawn` nie robią absolutnie nic. Obecnie domknięcie,
które chcemy wykonać, otrzymujemy w metodzie `execute`. Musimy jednak przekazać
`thread::spawn` domknięcie do uruchomienia przy tworzeniu każdego `Worker`
podczas tworzenia `ThreadPool`.

Chcemy, aby właśnie utworzone struktury `Worker` pobierały kod do uruchomienia
z kolejki przechowywanej w `ThreadPool` i wysyłały go do uruchomienia w swoim
wątku.

Kanały, które poznaliśmy w rozdziale 16 – prosty sposób komunikacji między
dwoma wątkami – świetnie się do tego nadają. Użyjemy kanału jako kolejki zadań,
a `execute` będzie wysyłać zadanie z `ThreadPool` do instancji `Worker`, które
przekażą je do swojego wątku. Oto plan:

1. `ThreadPool` utworzy kanał i zachowa nadajnik.
2. Każdy `Worker` zachowa odbiornik.
3. Utworzymy nową strukturę `Job`, która będzie przechowywać domknięcia, które
   chcemy przesyłać kanałem.
4. Metoda `execute` wyśle przez nadajnik zadanie, które chce wykonać.
5. W swoim wątku `Worker` będzie w pętli odczytywał odbiornik i wykonywał
   domknięcia wszystkich otrzymanych zadań.

Zacznijmy od utworzenia kanału w `ThreadPool::new` i przechowania nadajnika w
instancji `ThreadPool`, jak pokazano w listingu 21-16. Struktura `Job` na razie
niczego nie przechowuje, ale będzie typem elementów, które przesyłamy kanałem.

<Listing number="21-16" file-name="src/lib.rs" caption="Modyfikacja `ThreadPool` tak, by przechowywała nadajnik kanału przesyłającego instancje `Job`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-16/src/lib.rs:here}}
```

</Listing>

W `ThreadPool::new` tworzymy nasz nowy kanał, a pula przechowuje nadajnik. To
się pomyślnie skompiluje.

Spróbujmy przekazać odbiornik kanału do każdego `Worker`, gdy pula wątków
tworzy kanał. Wiemy, że chcemy używać odbiornika w wątku uruchamianym przez
instancje `Worker`, więc w domknięciu odwołamy się do parametru `receiver`. Kod
z listingu 21-17 jeszcze się nie do końca kompiluje.

<Listing number="21-17" file-name="src/lib.rs" caption="Przekazywanie odbiornika do każdego `Worker`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch21-web-server/listing-21-17/src/lib.rs:here}}
```

</Listing>

Wprowadziliśmy kilka drobnych i prostych zmian: przekazujemy odbiornik do
`Worker::new`, a potem używamy go wewnątrz domknięcia.

Gdy próbujemy sprawdzić ten kod, otrzymujemy taki błąd:

```console
{{#include ../listings/ch21-web-server/listing-21-17/output.txt}}
```

Kod próbuje przekazać `receiver` do wielu instancji `Worker`. To nie zadziała,
jak pamiętasz z rozdziału 16: implementacja kanału dostarczana przez Rusta to
wielu _producentów_, jeden _konsument_. Oznacza to, że nie możemy po prostu
sklonować konsumującego końca kanału, żeby naprawić ten kod. Nie chcemy też
wysyłać komunikatu wiele razy do wielu konsumentów; chcemy jednej listy
komunikatów i wielu instancji `Worker`, tak by każdy komunikat został
przetworzony raz.

Ponadto zdjęcie zadania z kolejki kanału wymaga modyfikowania `receiver`, więc
wątki potrzebują bezpiecznego sposobu współdzielenia i modyfikowania
`receiver`; w przeciwnym razie mogłyby wystąpić sytuacje wyścigu (*race
conditions*), omówione w rozdziale 16.

Przypomnij sobie bezpieczne wątkowo inteligentne wskaźniki (*smart pointers*)
omówione w rozdziale 16: aby współdzielić własność (*ownership*) między wieloma
wątkami i pozwolić wątkom modyfikować wartość, musimy użyć `Arc<Mutex<T>>`. Typ
`Arc` pozwoli wielu instancjom `Worker` być właścicielami odbiornika, a `Mutex`
zapewni, że w danej chwili tylko jeden `Worker` pobiera zadanie z odbiornika.
Listing 21-18 pokazuje zmiany, które musimy wprowadzić.

<Listing number="21-18" file-name="src/lib.rs" caption="Współdzielenie odbiornika między instancjami `Worker` za pomocą `Arc` i `Mutex`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-18/src/lib.rs:here}}
```

</Listing>

W `ThreadPool::new` umieszczamy odbiornik w `Arc` i `Mutex`. Dla każdego nowego
`Worker` klonujemy `Arc`, aby zwiększyć licznik referencji, dzięki czemu
instancje `Worker` mogą współdzielić własność odbiornika.

Po tych zmianach kod się kompiluje! Jesteśmy coraz bliżej!

#### Implementacja metody `execute` {#implementing-the-execute-method}

Zaimplementujmy wreszcie metodę `execute` w `ThreadPool`. Zmienimy też `Job`
ze struktury na alias typu dla obiektu traitu (*trait object*), który
przechowuje typ domknięcia otrzymywanego przez `execute`. Jak omówiliśmy w
podrozdziale [„Synonimy typów i aliasy typów”][type-aliases]<!-- ignore --> w rozdziale 20,
aliasy typów pozwalają skracać długie typy dla wygody użycia. Spójrz na
listing 21-19.

<Listing number="21-19" file-name="src/lib.rs" caption="Tworzenie aliasu typu `Job` dla `Box` przechowującego każde domknięcie, a następnie wysyłanie zadania kanałem">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-19/src/lib.rs:here}}
```

</Listing>

Po utworzeniu nowej instancji `Job` z domknięcia otrzymanego w `execute`
wysyłamy to zadanie przez nadający koniec kanału. Wywołujemy `unwrap` na
`send` na wypadek, gdyby wysyłanie się nie powiodło. Mogłoby się tak stać na
przykład wtedy, gdybyśmy zatrzymali wykonywanie wszystkich naszych wątków, co
oznaczałoby, że odbierający koniec przestał odbierać nowe komunikaty. W tej
chwili nie możemy zatrzymać wykonywania naszych wątków: działają one tak
długo, jak istnieje pula. Używamy `unwrap`, ponieważ wiemy, że przypadek
niepowodzenia nie wystąpi, ale kompilator tego nie wie.

Ale to jeszcze nie koniec! W `Worker` nasze domknięcie przekazywane do
`thread::spawn` nadal jedynie _odwołuje się_ do odbierającego końca kanału.
Zamiast tego potrzebujemy, aby domknięcie działało w nieskończonej pętli,
prosząc odbierający koniec kanału o zadanie i uruchamiając je, gdy je
otrzyma. Wprowadźmy w `Worker::new` zmianę pokazaną w listingu 21-20.

<Listing number="21-20" file-name="src/lib.rs" caption="Odbieranie i wykonywanie zadań w wątku instancji `Worker`">

```rust,noplayground
{{#rustdoc_include ../listings/ch21-web-server/listing-21-20/src/lib.rs:here}}
```

</Listing>

Najpierw wywołujemy `lock` na `receiver`, aby uzyskać blokadę mutexu, a
następnie wywołujemy `unwrap`, aby spanikować w razie jakichkolwiek błędów.
Uzyskanie blokady może się nie powieść, jeśli mutex jest w stanie _zatrutym_
(*poisoned*), co może się zdarzyć, gdy jakiś inny wątek spanikował, trzymając
blokadę, zamiast ją zwolnić. W takiej sytuacji wywołanie `unwrap`, aby ten
wątek spanikował, jest właściwym działaniem. Możesz śmiało zamienić to
`unwrap` na `expect` z komunikatem błędu, który ma dla ciebie znaczenie.

Jeśli uzyskamy blokadę mutexu, wywołujemy `recv`, aby odebrać `Job` z kanału.
Ostatnie `unwrap` również tu pomija wszelkie błędy, które mogą wystąpić, jeśli
wątek przechowujący nadajnik zakończył działanie – podobnie jak metoda `send`
zwraca `Err`, jeśli odbiornik zakończy działanie.

Wywołanie `recv` blokuje, więc jeśli nie ma jeszcze żadnego zadania, bieżący
wątek będzie czekał, aż zadanie stanie się dostępne. `Mutex<T>` zapewnia, że w
danej chwili tylko jeden wątek `Worker` próbuje pobrać zadanie.

Nasza pula wątków już działa! Uruchom ją poleceniem
`cargo run` i wyślij kilka żądań:

<!-- manual-regeneration
cd listings/ch21-web-server/listing-21-20
cargo run
make some requests to 127.0.0.1:7878
Can't automate because the output depends on making requests
-->

```console
$ cargo run
   Compiling hello v0.1.0 (file:///projects/hello)
warning: field `workers` is never read
 --> src/lib.rs:7:5
  |
6 | pub struct ThreadPool {
  |            ---------- field in this struct
7 |     workers: Vec<Worker>,
  |     ^^^^^^^
  |
  = note: `#[warn(dead_code)]` on by default

warning: fields `id` and `thread` are never read
  --> src/lib.rs:48:5
   |
47 | struct Worker {
   |        ------ fields in this struct
48 |     id: usize,
   |     ^^
49 |     thread: thread::JoinHandle<()>,
   |     ^^^^^^

warning: `hello` (lib) generated 2 warnings
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 4.91s
     Running `target/debug/hello`
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
Worker 1 got a job; executing.
Worker 3 got a job; executing.
Worker 0 got a job; executing.
Worker 2 got a job; executing.
```

Sukces! Mamy teraz pulę wątków, która asynchronicznie obsługuje połączenia.
Nigdy nie powstaje więcej niż cztery wątki, więc system nie zostanie
przeciążony, jeśli serwer otrzyma dużo żądań. Jeśli wyślemy żądanie do
_/sleep_, serwer będzie mógł obsługiwać inne żądania, zlecając je innemu
wątkowi.

> Uwaga: jeśli otworzysz _/sleep_ jednocześnie w kilku oknach przeglądarki,
> mogą się one wczytywać pojedynczo w pięciosekundowych odstępach. Niektóre
> przeglądarki wykonują wiele instancji tego samego żądania sekwencyjnie ze
> względu na buforowanie. To ograniczenie nie jest spowodowane przez nasz
> serwer WWW.

To dobry moment, żeby się zatrzymać i zastanowić, jak różniłby się kod z
listingów 21-18, 21-19 i 21-20, gdybyśmy do wykonania pracy używali
future’ów zamiast domknięcia. Które typy by się zmieniły? Czym różniłyby się
sygnatury metod, jeśli w ogóle? Które części kodu pozostałyby takie same?

Po poznaniu pętli `while let` w rozdziałach 17 i 19 możesz się zastanawiać,
dlaczego nie napisaliśmy kodu wątku `Worker` tak, jak pokazano w listingu
21-21.

<Listing number="21-21" file-name="src/lib.rs" caption="Alternatywna implementacja `Worker::new` z użyciem `while let`">

```rust,ignore,not_desired_behavior
{{#rustdoc_include ../listings/ch21-web-server/listing-21-21/src/lib.rs:here}}
```

</Listing>

Ten kod się kompiluje i działa, ale nie daje pożądanego zachowania wątków:
wolne żądanie nadal powoduje, że inne żądania czekają na przetworzenie.
Przyczyna jest dość subtelna: struktura `Mutex` nie ma publicznej metody
`unlock`, ponieważ własność blokady opiera się na czasie życia `MutexGuard<T>`
wewnątrz `LockResult<MutexGuard<T>>` zwracanego przez metodę `lock`. Dzięki
temu w czasie kompilacji (*compile-time*) *borrow checker* (mechanizm
sprawdzania pożyczeń) może wymusić regułę, że do zasobu strzeżonego przez
`Mutex` nie można uzyskać dostępu, jeśli nie trzymamy blokady. Jednak taka
implementacja może też sprawić, że blokada będzie trzymana dłużej, niż
zamierzano, jeśli nie będziemy uważać na czas życia `MutexGuard<T>`.

Kod z listingu 21-20, w którym użyto
`let job = receiver.lock().unwrap().recv().unwrap();`, działa, ponieważ przy
`let` wszelkie wartości tymczasowe użyte w wyrażeniu (*expression*) po prawej
stronie znaku równości są zwalniane (*dropped*) natychmiast po zakończeniu
instrukcji (*statement*) `let`. Natomiast `while let` (oraz `if let` i
`match`) nie zwalnia wartości tymczasowych aż do końca powiązanego bloku. W listingu 21-21
blokada pozostaje trzymana przez cały czas wywołania `job()`, co oznacza, że
inne instancje `Worker` nie mogą odbierać zadań.

[type-aliases]: ch20-03-advanced-types.html#type-synonyms-and-type-aliases
[integer-types]: ch03-02-data-types.html#integer-types
[moving-out-of-closures]: ch13-01-closures.html#moving-captured-values-out-of-closures
[builder]: https://doc.rust-lang.org/std/thread/struct.Builder.html
[builder-spawn]: https://doc.rust-lang.org/std/thread/struct.Builder.html#method.spawn

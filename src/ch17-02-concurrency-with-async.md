<!-- Old headings. Do not remove or links may break. -->

<a id="concurrency-with-async"></a>

## Stosowanie współbieżności z async {#applying-concurrency-with-async}

W tym podrozdziale zastosujemy async do niektórych z tych samych problemów
współbieżności (*concurrency*), z którymi w rozdziale 16 mierzyliśmy się za
pomocą wątków. Ponieważ wiele kluczowych idei omówiliśmy już tam, tutaj
skupimy się na tym, czym różnią się wątki i *future*’y (wartości, które będą
gotowe później).

W wielu przypadkach API do pracy ze współbieżnością przy użyciu async są
bardzo podobne do tych, których używa się z wątkami. W innych okazują się
zupełnie inne. Nawet gdy API dla wątków i async _wyglądają_ podobnie, często
zachowują się inaczej – i niemal zawsze mają inną charakterystykę wydajności.

<!-- Old headings. Do not remove or links may break. -->

<a id="counting"></a>

### Tworzenie nowego zadania za pomocą `spawn_task` {#creating-a-new-task-with-spawn_task}

Pierwszą operacją, którą zajęliśmy się w podrozdziale
[„Tworzenie nowego wątku za pomocą `spawn`”][thread-spawn]<!-- ignore --> w
rozdziale 16, było liczenie w dwóch osobnych wątkach. Zróbmy to samo przy
użyciu async. *Crate* (jednostka kompilacji w Ruście) `trpl` udostępnia funkcję
`spawn_task`, która wygląda bardzo podobnie do API `thread::spawn`, oraz
funkcję `sleep`, która jest asynchroniczną wersją API `thread::sleep`. Możemy
użyć ich razem do zaimplementowania przykładu z liczeniem, jak pokazano w
listingu 17-6.

<Listing number="17-6" caption="Tworzenie nowego zadania, które wypisuje jedno, podczas gdy zadanie główne wypisuje coś innego" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-06/src/main.rs:all}}
```

</Listing>

Na początek konfigurujemy funkcję `main` z użyciem `trpl::block_on`, aby nasza
funkcja najwyższego poziomu mogła być asynchroniczna.

> Uwaga: od tego miejsca w rozdziale każdy przykład będzie zawierał dokładnie
> ten sam kod opakowujący z `trpl::block_on` w `main`, więc często będziemy go
> pomijać, tak jak pomijamy `main`. Pamiętaj, aby umieścić go w swoim kodzie!

Następnie piszemy w tym bloku dwie pętle, z których każda zawiera wywołanie
`trpl::sleep`, czekające pół sekundy (500 milisekund) przed wysłaniem kolejnego
komunikatu. Jedną pętlę umieszczamy w treści `trpl::spawn_task`, a drugą w
pętli `for` najwyższego poziomu. Po wywołaniach `sleep` dodajemy też `await`.

Ten kod zachowuje się podobnie do implementacji opartej na wątkach – łącznie z
tym, że po uruchomieniu możesz zobaczyć w swoim terminalu komunikaty w innej
kolejności:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
```

Ta wersja kończy działanie, gdy tylko skończy się pętla `for` w treści głównego
bloku async, ponieważ zadanie utworzone przez `spawn_task` zostaje zamknięte
wraz z końcem funkcji `main`. Jeśli chcesz, aby działało aż do zakończenia
zadania, musisz użyć uchwytu (*join handle*), aby poczekać na zakończenie
pierwszego zadania. W przypadku wątków używaliśmy metody `join`, aby
„zablokować” program do czasu, aż wątek skończy działać. W listingu 17-7 możemy
zrobić to samo za pomocą `await`, ponieważ sam uchwyt zadania jest
*future*’em. Jego typ `Output` to `Result`, więc po oczekiwaniu na niego
dodatkowo go rozpakowujemy.

<Listing number="17-7" caption="Używanie `await` z uchwytem zadania, aby wykonać zadanie do końca" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-07/src/main.rs:handle}}
```

</Listing>

Ta zaktualizowana wersja działa, dopóki nie skończą się _obie_ pętle:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the second task!
hi number 1 from the first task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Jak dotąd wygląda na to, że async i wątki dają podobne wyniki, tylko z inną
składnią: używamy `await` zamiast wywoływać `join` na uchwycie i oczekujemy na
wywołania `sleep`.

Większa różnica polega na tym, że nie musieliśmy w tym celu tworzyć kolejnego
wątku systemu operacyjnego. W zasadzie nie musimy tu nawet tworzyć zadania.
Ponieważ bloki async kompilują się do anonimowych future’ów, możemy umieścić
każdą pętlę w bloku async i pozwolić środowisku uruchomieniowemu (*runtime*)
wykonać je obie do końca za pomocą funkcji `trpl::join`.

W podrozdziale
[„Czekanie na zakończenie wszystkich wątków”][join-handles]<!-- ignore --> w
rozdziale 16 pokazaliśmy, jak używać metody `join` na typie `JoinHandle`
zwracanym przez wywołanie `std::thread::spawn`. Funkcja `trpl::join` jest
podobna, ale działa na future’ach. Gdy przekażesz jej dwa future’y, tworzy
jeden nowy future, którego wynikiem jest krotka (*tuple*) zawierająca wyniki
obu przekazanych future’ów, gdy _oba_ się zakończą. Dlatego w listingu 17-8
używamy `trpl::join`, aby poczekać na zakończenie zarówno `fut1`, jak i
`fut2`. _Nie_ oczekujemy na `fut1` i `fut2`, lecz na nowy future utworzony
przez `trpl::join`. Ignorujemy jego wynik, ponieważ to tylko krotka zawierająca
dwie wartości jednostkowe (*unit*).

<Listing number="17-8" caption="Używanie `trpl::join` do oczekiwania na dwa anonimowe future’y" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-08/src/main.rs:join}}
```

</Listing>

Po uruchomieniu widzimy, że oba future’y wykonują się do końca:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
hi number 1 from the first task!
hi number 1 from the second task!
hi number 2 from the first task!
hi number 2 from the second task!
hi number 3 from the first task!
hi number 3 from the second task!
hi number 4 from the first task!
hi number 4 from the second task!
hi number 5 from the first task!
hi number 6 from the first task!
hi number 7 from the first task!
hi number 8 from the first task!
hi number 9 from the first task!
```

Teraz za każdym razem zobaczysz dokładnie tę samą kolejność, co bardzo różni
się od tego, co widzieliśmy w przypadku wątków i `trpl::spawn_task` w listingu
17-7. Dzieje się tak, ponieważ funkcja `trpl::join` jest _sprawiedliwa_
(*fair*), co oznacza, że sprawdza każdy future równie często, na przemian, i
nigdy nie pozwala jednemu wysforować się naprzód, jeśli drugi jest gotowy. W
przypadku wątków to system operacyjny decyduje, który wątek sprawdzić i jak
długo pozwolić mu działać. W asynchronicznym Ruście o tym, które zadanie
sprawdzić, decyduje środowisko uruchomieniowe. (W praktyce szczegóły się
komplikują, ponieważ asynchroniczne środowisko uruchomieniowe może w ramach
zarządzania współbieżnością wewnętrznie korzystać z wątków systemu
operacyjnego, więc zagwarantowanie sprawiedliwości może wymagać od niego więcej
pracy – ale nadal jest możliwe!) Środowiska uruchomieniowe nie muszą
gwarantować sprawiedliwości dla żadnej konkretnej operacji i często oferują
różne API, które pozwalają wybrać, czy sprawiedliwość jest ci potrzebna.

Wypróbuj kilka wariantów oczekiwania na future’y i zobacz, co się stanie:

- Usuń blok async wokół jednej z pętli albo wokół obu.
- Oczekuj na każdy blok async od razu po jego zdefiniowaniu.
- Opakuj w blok async tylko pierwszą pętlę i oczekuj na wynikowy future po
  treści drugiej pętli.

Dodatkowe wyzwanie: spróbuj ustalić, jaki będzie wynik w każdym przypadku,
_zanim_ uruchomisz kod!

<!-- Old headings. Do not remove or links may break. -->

<a id="message-passing"></a>
<a id="counting-up-on-two-tasks-using-message-passing"></a>

### Przesyłanie danych między dwoma zadaniami za pomocą przekazywania komunikatów {#sending-data-between-two-tasks-using-message-passing}

Współdzielenie danych między future’ami także będzie wyglądać znajomo:
ponownie użyjemy przekazywania komunikatów (*message passing*), ale tym razem z
asynchronicznymi wersjami typów i funkcji. Pójdziemy nieco inną drogą niż w
podrozdziale
[„Przesyłanie danych między wątkami za pomocą przekazywania komunikatów”][message-passing-threads]<!-- ignore -->
w rozdziale 16, aby pokazać kilka kluczowych różnic między współbieżnością
opartą na wątkach a współbieżnością opartą na future’ach. W listingu 17-9
zaczniemy od jednego bloku async – _bez_ tworzenia osobnego zadania, tak jak
tworzyliśmy osobny wątek.

<Listing number="17-9" caption="Tworzenie asynchronicznego kanału i przypisywanie jego dwóch połówek do `tx` i `rx`" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-09/src/main.rs:channel}}
```

</Listing>

Używamy tu `trpl::channel`, asynchronicznej wersji API kanału typu „wielu
producentów, jeden konsument”, którego używaliśmy z wątkami w rozdziale 16.
Asynchroniczna wersja API różni się od wersji opartej na wątkach tylko
nieznacznie: używa mutowalnego (*mutable*), a nie niemutowalnego odbiornika
`rx`, a jej metoda `recv` zwraca future, na który musimy oczekiwać, zamiast
bezpośrednio zwracać wartość. Teraz możemy wysyłać komunikaty od nadajnika do
odbiornika. Zwróć uwagę, że nie musimy tworzyć osobnego wątku ani nawet zadania;
wystarczy oczekiwać na wywołanie `rx.recv`.

Synchroniczna metoda `Receiver::recv` w `std::mpsc::channel` blokuje, dopóki
nie odbierze komunikatu. Metoda `trpl::Receiver::recv` tego nie robi, ponieważ
jest asynchroniczna. Zamiast blokować, oddaje sterowanie środowisku
uruchomieniowemu, dopóki nie zostanie odebrany komunikat albo dopóki strona
wysyłająca kanału się nie zamknie. Na wywołanie `send` natomiast nie oczekujemy,
ponieważ nie blokuje ono. Nie musi, bo kanał, do którego wysyłamy, jest
nieograniczony.

> Uwaga: ponieważ cały ten kod asynchroniczny działa w bloku async w wywołaniu
> `trpl::block_on`, wszystko w nim może uniknąć blokowania. Jednak kod _poza_
> nim będzie zablokowany do czasu, aż funkcja `block_on` zwróci wynik. Na tym
> właśnie polega sens funkcji `trpl::block_on`: pozwala _wybrać_, gdzie
> zablokować się na pewnym zestawie kodu asynchronicznego, a tym samym gdzie
> nastąpi przejście między kodem synchronicznym a asynchronicznym.

Zwróć uwagę na dwie rzeczy w tym przykładzie. Po pierwsze, komunikat dotrze
od razu. Po drugie, choć używamy tu future’a, nie ma jeszcze żadnej
współbieżności. Wszystko w listingu dzieje się po kolei, tak jak działoby się
bez żadnych future’ów.

Zajmijmy się pierwszą kwestią, wysyłając serię komunikatów i usypiając między
nimi, jak pokazano w listingu 17-10.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-10" caption="Wysyłanie i odbieranie wielu komunikatów przez asynchroniczny kanał i usypianie z użyciem `await` między kolejnymi komunikatami" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-10/src/main.rs:many-messages}}
```

</Listing>

Oprócz wysyłania komunikatów musimy je też odbierać. W tym przypadku, ponieważ
wiemy, ile komunikatów nadejdzie, moglibyśmy zrobić to ręcznie, wywołując
`rx.recv().await` cztery razy. W praktyce jednak zwykle będziemy czekać na
_nieznaną_ liczbę komunikatów, więc musimy czekać dalej, dopóki nie ustalimy,
że więcej komunikatów nie będzie.

W listingu 16-10 użyliśmy pętli `for` do przetworzenia wszystkich elementów
odebranych z synchronicznego kanału. Rust nie ma jednak jeszcze sposobu na
użycie pętli `for` z serią elementów _wytwarzanych asynchronicznie_, więc
musimy użyć pętli, której jeszcze nie widzieliśmy: warunkowej pętli
`while let`. To pętlowa wersja konstrukcji `if let`, którą poznaliśmy w
podrozdziale
[„Zwięzły przepływ sterowania z `if let` i `let...else`”][if-let]<!-- ignore -->
w rozdziale 6. Pętla będzie się wykonywać tak długo, jak długo podany w niej
wzorzec będzie pasował do wartości.

Wywołanie `rx.recv` zwraca future, na który oczekujemy. Środowisko
uruchomieniowe wstrzyma future, dopóki nie będzie on gotowy. Gdy nadejdzie
komunikat, future da wynik `Some(message)` – i tak za każdym razem, gdy
nadejdzie komunikat. Gdy kanał się zamknie, niezależnie od tego, czy nadeszły
_jakiekolwiek_ komunikaty, future da zamiast tego wynik `None`, aby
zasygnalizować, że nie ma więcej wartości, a więc powinniśmy zakończyć jego
odpytywanie (*polling*) – czyli przestać na niego oczekiwać.

Pętla `while let` łączy to wszystko w całość. Jeśli wynikiem wywołania
`rx.recv().await` jest `Some(message)`, uzyskujemy dostęp do komunikatu i
możemy go użyć w treści pętli, tak jak w przypadku `if let`. Jeśli wynikiem
jest `None`, pętla się kończy. Za każdym razem, gdy pętla wykona obieg,
ponownie trafia na punkt oczekiwania (*await point*), więc środowisko
uruchomieniowe znów ją wstrzymuje, dopóki nie nadejdzie kolejny komunikat.

Kod poprawnie wysyła i odbiera teraz wszystkie komunikaty. Niestety nadal
pozostaje kilka problemów. Po pierwsze, komunikaty nie przychodzą w odstępach
półsekundowych. Przychodzą wszystkie naraz, 2 sekundy (2000 milisekund) po
uruchomieniu programu. Po drugie, ten program nigdy się nie kończy! Zamiast
tego w nieskończoność czeka na nowe komunikaty. Musisz go zamknąć za pomocą
<kbd>ctrl</kbd>-<kbd>C</kbd>.

#### Kod w jednym bloku async wykonuje się liniowo {#code-within-one-async-block-executes-linearly}

Zacznijmy od zbadania, dlaczego komunikaty przychodzą wszystkie naraz po pełnym
opóźnieniu, zamiast przychodzić z odstępami między kolejnymi. W obrębie danego
bloku async kolejność, w jakiej słowa kluczowe (*keyword*) `await` występują w
kodzie, jest zarazem kolejnością, w jakiej wykonują się podczas działania
programu.

W listingu 17-10 jest tylko jeden blok async, więc wszystko w nim wykonuje się
liniowo. Nadal nie ma żadnej współbieżności. Najpierw wykonują się wszystkie
wywołania `tx.send`, przeplatane wszystkimi wywołaniami `trpl::sleep` i
związanymi z nimi punktami oczekiwania. Dopiero potem pętla `while let` może
przejść przez którykolwiek z punktów `await` na wywołaniach `recv`.

Aby uzyskać pożądane zachowanie, w którym opóźnienie występuje między
kolejnymi komunikatami, musimy umieścić operacje na `tx` i `rx` w osobnych
blokach async, jak pokazano w listingu 17-11. Wtedy środowisko uruchomieniowe
może wykonać każdy z nich osobno za pomocą `trpl::join`, tak jak w listingu
17-8. Ponownie oczekujemy na wynik wywołania `trpl::join`, a nie na poszczególne
future’y. Gdybyśmy oczekiwali na poszczególne future’y po kolei, wrócilibyśmy po
prostu do sekwencyjnego przepływu – dokładnie tego, czego staramy się _nie_
robić.

<!-- We cannot test this one because it never stops! -->

<Listing number="17-11" caption="Rozdzielenie `send` i `recv` na osobne bloki `async` i oczekiwanie na future’y tych bloków" file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch17-async-await/listing-17-11/src/main.rs:futures}}
```

</Listing>

Po aktualizacji kodu z listingu 17-11 komunikaty są wypisywane w odstępach
500 milisekund, a nie wszystkie w pośpiechu po 2 sekundach.

#### Przenoszenie własności do bloku async {#moving-ownership-into-an-async-block}

Program nadal jednak nigdy się nie kończy, a to z powodu sposobu, w jaki pętla
`while let` współdziała z `trpl::join`:

- Future zwrócony przez `trpl::join` kończy się dopiero wtedy, gdy zakończą się
  _oba_ przekazane mu future’y.
- Future `tx_fut` kończy się, gdy skończy usypianie po wysłaniu ostatniego
  komunikatu z `vals`.
- Future `rx_fut` nie zakończy się, dopóki nie skończy się pętla `while let`.
- Pętla `while let` nie skończy się, dopóki oczekiwanie na `rx.recv` nie da
  `None`.
- Oczekiwanie na `rx.recv` zwróci `None` dopiero wtedy, gdy drugi koniec kanału
  zostanie zamknięty.
- Kanał zamknie się tylko wtedy, gdy wywołamy `rx.close` albo gdy strona
  wysyłająca, `tx`, zostanie zwolniona (*drop*).
- Nigdzie nie wywołujemy `rx.close`, a `tx` nie zostanie zwolniony, dopóki nie
  skończy się najbardziej zewnętrzny blok async przekazany do `trpl::block_on`.
- Blok nie może się skończyć, ponieważ jest zablokowany w oczekiwaniu na
  zakończenie `trpl::join`, co prowadzi nas z powrotem na początek tej listy.

Obecnie blok async, w którym wysyłamy komunikaty, jedynie _pożycza_
(*borrows*) `tx`, ponieważ wysłanie komunikatu nie wymaga własności
(*ownership*). Gdybyśmy jednak mogli _przenieść_ `tx` do tego bloku async,
zostałby on zwolniony, gdy blok się skończy. W podrozdziale
[„Przechwytywanie referencji lub przenoszenie własności”][capture-or-move]<!-- ignore -->
w rozdziale 13 pokazaliśmy, jak używać słowa kluczowego `move` z
domknięciami (*closures*), a jak omówiliśmy w podrozdziale
[„Używanie domknięć `move` z wątkami”][move-threads]<!-- ignore --> w
rozdziale 16, podczas pracy z wątkami często musimy przenosić dane do
domknięć. Te same podstawowe zasady dotyczą bloków async, więc słowo kluczowe
`move` działa z blokami async tak samo jak z domknięciami.

W listingu 17-12 zmieniamy blok używany do wysyłania komunikatów z `async` na
`async move`.

<Listing number="17-12" caption="Poprawiona wersja kodu z listingu 17-11, która po zakończeniu pracy poprawnie się zamyka" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-12/src/main.rs:with-move}}
```

</Listing>

Gdy uruchomimy _tę_ wersję kodu, po wysłaniu i odebraniu ostatniego komunikatu
następuje łagodne zamykanie (*graceful shutdown*) programu. Zobaczmy teraz, co
trzeba by zmienić, aby wysyłać dane z więcej niż jednego future’a.

#### Łączenie wielu future’ów za pomocą makra `join!` {#joining-a-number-of-futures-with-the-join-macro}

Ten asynchroniczny kanał również obsługuje wielu producentów, więc jeśli
chcemy wysyłać komunikaty z wielu future’ów, możemy wywołać `clone` na `tx`,
jak pokazano w listingu 17-13.

<Listing number="17-13" caption="Używanie wielu producentów z blokami async" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-13/src/main.rs:here}}
```

</Listing>

Najpierw klonujemy `tx`, tworząc `tx1` poza pierwszym blokiem async.
Przenosimy `tx1` do tego bloku, tak jak wcześniej `tx`. Następnie przenosimy
oryginalny `tx` do _nowego_ bloku async, w którym wysyłamy kolejne komunikaty
z nieco dłuższym opóźnieniem. Tak się składa, że ten nowy blok async
umieszczamy po bloku async odbierającym komunikaty, ale równie dobrze mógłby
się znaleźć przed nim. Kluczowa jest kolejność, w jakiej oczekujemy na future’y,
a nie kolejność, w jakiej je tworzymy.

Oba bloki async wysyłające komunikaty muszą być blokami `async move`, aby
zarówno `tx`, jak i `tx1` zostały zwolnione po zakończeniu tych bloków. W
przeciwnym razie wrócimy do tej samej nieskończonej pętli, od której
zaczęliśmy.

Na koniec zamieniamy `trpl::join` na `trpl::join!`, aby obsłużyć dodatkowy
future: makro `join!` oczekuje na dowolną liczbę future’ów, o ile znamy ich
liczbę w czasie kompilacji (*compile-time*). Oczekiwanie na kolekcję o
nieznanej liczbie future’ów omówimy w dalszej części tego rozdziału.

Teraz widzimy wszystkie komunikaty z obu wysyłających future’ów, a ponieważ
future’y te stosują po wysłaniu nieco inne opóźnienia, komunikaty są również
odbierane w tych różnych odstępach:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
received 'hi'
received 'more'
received 'from'
received 'the'
received 'messages'
received 'future'
received 'for'
received 'you'
```

Zobaczyliśmy, jak używać przekazywania komunikatów do przesyłania danych
między future’ami, jak kod w bloku async wykonuje się sekwencyjnie, jak
przenosić własność do bloku async i jak łączyć wiele future’ów. Teraz omówmy,
jak i dlaczego informować środowisko uruchomieniowe, że może przełączyć się na
inne zadanie.

{{#quiz ../quizzes/async-02-concurrency-with-async.toml}}

[thread-spawn]: ch16-01-threads.html#creating-a-new-thread-with-spawn
[join-handles]: ch16-01-threads.html#waiting-for-all-threads-to-finish
[message-passing-threads]: ch16-02-message-passing.html
[if-let]: ch06-03-if-let.html
[capture-or-move]: ch13-01-closures.html#capturing-references-or-moving-ownership
[move-threads]: ch16-01-threads.html#using-move-closures-with-threads

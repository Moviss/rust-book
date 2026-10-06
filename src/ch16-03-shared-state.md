## Współbieżność ze współdzielonym stanem {#shared-state-concurrency}

Przekazywanie komunikatów (*message passing*) to dobry sposób na obsługę
współbieżności (*concurrency*), ale nie jedyny. Inną metodą jest dostęp wielu
wątków do tych samych współdzielonych danych. Przypomnij sobie ten fragment
hasła z dokumentacji języka Go: „Nie komunikuj się przez współdzielenie
pamięci”.

Jak wyglądałaby komunikacja przez współdzielenie pamięci? I dlaczego zwolennicy
przekazywania komunikatów przestrzegają przed współdzieleniem pamięci?

W pewnym sensie kanały w dowolnym języku programowania przypominają pojedynczą
własność (*ownership*), ponieważ po przesłaniu wartości kanałem nie należy już
jej używać. Współbieżność ze współdzieloną pamięcią przypomina natomiast
współwłasność: wiele wątków może jednocześnie korzystać z tego samego miejsca w
pamięci. Jak widać było w rozdziale 15, w którym inteligentne wskaźniki
(*smart pointers*) umożliwiły współwłasność, współwłasność może zwiększać
złożoność, bo tymi różnymi właścicielami trzeba zarządzać. System typów i
reguły własności Rusta bardzo pomagają w tym, by to zarządzanie było poprawne.
Jako przykład przyjrzyjmy się mutexom, jednemu z częściej używanych prymitywów
współbieżności dla współdzielonej pamięci.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-mutexes-to-allow-access-to-data-from-one-thread-at-a-time"></a>

### Kontrolowanie dostępu za pomocą mutexów {#controlling-access-with-mutexes}

_Mutex_ to skrót od _mutual exclusion_ (wzajemne wykluczanie): mutex pozwala w
danej chwili tylko jednemu wątkowi na dostęp do pewnych danych. Aby uzyskać
dostęp do danych w mutexie, wątek musi najpierw zasygnalizować, że go
potrzebuje, prosząc o uzyskanie blokady mutexu. _Blokada_ (*lock*) to struktura
danych będąca częścią mutexu, która śledzi, kto ma obecnie wyłączny dostęp do
danych. Dlatego mówi się, że mutex _strzeże_ (*guards*) przechowywanych danych
za pomocą systemu blokad.

Mutexy mają opinię trudnych w użyciu, bo trzeba pamiętać o dwóch regułach:

1. Przed użyciem danych musisz spróbować uzyskać blokadę.
2. Gdy skończysz pracę z danymi, których strzeże mutex, musisz je odblokować,
   aby inne wątki mogły uzyskać blokadę.

Jako metaforę mutexu z prawdziwego świata wyobraź sobie dyskusję panelową na
konferencji, na której jest tylko jeden mikrofon. Zanim panelista zabierze
głos, musi poprosić o mikrofon albo dać znak, że chce go użyć. Gdy dostanie
mikrofon, może mówić, jak długo zechce, a potem przekazuje mikrofon kolejnemu
paneliście, który chce zabrać głos. Jeśli panelista zapomni oddać mikrofon po
skończonej wypowiedzi, nikt inny nie będzie mógł mówić. Jeśli zarządzanie
wspólnym mikrofonem zawiedzie, panel nie przebiegnie zgodnie z planem!

Poprawne zarządzanie mutexami bywa niezwykle trudne, dlatego tak wiele osób
entuzjastycznie podchodzi do kanałów. Jednak dzięki systemowi typów i regułom
własności Rusta nie można się pomylić przy blokowaniu i odblokowywaniu.

#### API typu `Mutex<T>` {#the-api-of-mutext}

Aby pokazać, jak używać mutexu, zacznijmy od użycia go w kontekście
jednowątkowym, jak pokazano w listingu 16-12.

<Listing number="16-12" file-name="src/main.rs" caption="Poznawanie API typu `Mutex<T>` w kontekście jednowątkowym, dla uproszczenia">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-12/src/main.rs}}
```

</Listing>

Jak w przypadku wielu typów, tworzymy `Mutex<T>` za pomocą funkcji powiązanej
(*associated function*) `new`. Aby uzyskać dostęp do danych wewnątrz mutexu,
używamy metody `lock`, która uzyskuje blokadę. To wywołanie zablokuje bieżący
wątek, tak że nie będzie mógł wykonywać żadnej pracy, dopóki nie przyjdzie
nasza kolej na otrzymanie blokady.

Wywołanie `lock` zakończyłoby się niepowodzeniem, gdyby inny wątek trzymający
blokadę spanikował. W takim przypadku nikt nigdy nie mógłby uzyskać blokady,
więc zdecydowaliśmy się wywołać `unwrap`, aby w takiej sytuacji ten wątek
zakończył się paniką (*panic*).

Po uzyskaniu blokady możemy traktować zwróconą wartość, tutaj nazwaną `num`,
jako mutowalną (*mutable*) referencję (*reference*) do danych w środku. System
typów gwarantuje, że uzyskamy blokadę przed użyciem wartości w `m`. Typem `m`
jest `Mutex<i32>`, a nie `i32`, więc _musimy_ wywołać `lock`, aby móc użyć
wartości `i32`. Nie da się o tym zapomnieć – system typów w przeciwnym razie
nie pozwoli nam uzyskać dostępu do wewnętrznej wartości `i32`.

Wywołanie `lock` zwraca typ o nazwie `MutexGuard`, opakowany w `LockResult`,
który obsłużyliśmy wywołaniem `unwrap`. Typ `MutexGuard` implementuje `Deref`,
aby wskazywać na nasze wewnętrzne dane; ma też implementację `Drop`, która
automatycznie zwalnia blokadę, gdy `MutexGuard` wychodzi poza zasięg (*scope*),
co dzieje się na końcu wewnętrznego zasięgu. Dzięki temu nie ryzykujemy, że
zapomnimy zwolnić blokadę i uniemożliwimy innym wątkom korzystanie z mutexu,
bo zwolnienie blokady następuje automatycznie.

Po zwolnieniu (*drop*) blokady możemy wypisać wartość mutexu i zobaczyć, że
udało nam się zmienić wewnętrzną wartość `i32` na `6`.

<!-- Old headings. Do not remove or links may break. -->

<a id="sharing-a-mutext-between-multiple-threads"></a>

#### Współdzielony dostęp do `Mutex<T>` {#shared-access-to-mutext}

Spróbujmy teraz współdzielić wartość między wieloma wątkami za pomocą
`Mutex<T>`. Uruchomimy 10 wątków i każdy z nich zwiększy wartość licznika o 1,
tak aby licznik doszedł od 0 do 10. Przykład w listingu 16-13 spowoduje błąd
kompilatora, a my wykorzystamy ten błąd, aby dowiedzieć się więcej o używaniu
`Mutex<T>` i o tym, jak Rust pomaga nam używać go poprawnie.

<Listing number="16-13" file-name="src/main.rs" caption="Dziesięć wątków, z których każdy zwiększa licznik strzeżony przez `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-13/src/main.rs}}
```

</Listing>

Tworzymy zmienną `counter`, która przechowuje `i32` wewnątrz `Mutex<T>`, tak
jak w listingu 16-12. Następnie tworzymy 10 wątków, iterując po zakresie liczb.
Używamy `thread::spawn` i przekazujemy wszystkim wątkom to samo domknięcie
(*closure*): takie, które przenosi licznik do wątku, uzyskuje blokadę na
`Mutex<T>` przez wywołanie metody `lock`, a następnie dodaje 1 do wartości w
mutexie. Gdy wątek skończy wykonywać swoje domknięcie, `num` wyjdzie poza
zasięg i zwolni blokadę, aby inny wątek mógł ją uzyskać.

W wątku głównym zbieramy wszystkie uchwyty wątków. Następnie, tak jak w
listingu 16-2, wywołujemy `join` na każdym uchwycie, aby upewnić się, że
wszystkie wątki zakończyły działanie. Wtedy wątek główny uzyska blokadę i
wypisze wynik programu.

Zasugerowaliśmy, że ten przykład się nie skompiluje. Sprawdźmy teraz dlaczego!

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-13/output.txt}}
```

Komunikat o błędzie mówi, że wartość `counter` została przeniesiona w
poprzedniej iteracji pętli. Rust informuje nas, że nie możemy przenieść
własności blokady `counter` do wielu wątków. Naprawmy ten błąd kompilatora za
pomocą metody współwłasności, którą omówiliśmy w rozdziale 15.

#### Współwłasność w wielu wątkach {#multiple-ownership-with-multiple-threads}

W rozdziale 15 nadaliśmy wartości wielu właścicieli, używając inteligentnego
wskaźnika `Rc<T>` do utworzenia wartości ze zliczaniem referencji (*reference
counting*). Zróbmy tu to samo i zobaczmy, co się stanie. W listingu 16-14
opakujemy `Mutex<T>` w `Rc<T>` i sklonujemy `Rc<T>` przed przeniesieniem
własności do wątku.

<Listing number="16-14" file-name="src/main.rs" caption="Próba użycia `Rc<T>`, aby wiele wątków mogło być właścicielami `Mutex<T>`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-14/src/main.rs}}
```

</Listing>

Ponownie kompilujemy i dostajemy… inne błędy! Kompilator wiele nas uczy:

```console
{{#include ../listings/ch16-fearless-concurrency/listing-16-14/output.txt}}
```

Ależ ten komunikat o błędzie jest rozwlekły! Oto ważna część, na której warto
się skupić: `` `Rc<Mutex<i32>>` cannot be sent between threads safely ``.
Kompilator podaje też powód:
`` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. O `Send`
opowiemy w następnym podrozdziale: to *trait* (cecha typu, zbliżona do
interfejsu), jeden z tych, które zapewniają, że typy używane z wątkami są
przeznaczone do użycia w sytuacjach współbieżnych.

Niestety `Rc<T>` nie jest bezpieczny do współdzielenia między wątkami. Gdy
`Rc<T>` zarządza licznikiem referencji, zwiększa go przy każdym wywołaniu
`clone` i zmniejsza, gdy każdy klon zostaje zwolniony. Nie używa jednak żadnych
prymitywów współbieżności, które gwarantowałyby, że zmiany licznika nie zostaną
przerwane przez inny wątek. Mogłoby to prowadzić do błędnych wartości licznika
– subtelnych błędów, które z kolei mogłyby powodować wycieki pamięci albo
zwolnienie wartości, zanim skończymy z niej korzystać. Potrzebujemy typu, który
działa dokładnie jak `Rc<T>`, ale zmienia licznik referencji w sposób
bezpieczny wątkowo.

#### Atomowe zliczanie referencji z `Arc<T>` {#atomic-reference-counting-with-arct}

Na szczęście `Arc<T>` _jest_ typem podobnym do `Rc<T>`, którego można bezpiecznie
używać w sytuacjach współbieżnych. Litera _a_ oznacza _atomic_ (atomowy), czyli
jest to typ _atomowo zliczający referencje_ (*atomically reference-counted*).
Typy atomowe to dodatkowy rodzaj prymitywów współbieżności, którego nie
będziemy tu szczegółowo omawiać – więcej szczegółów znajdziesz w dokumentacji
biblioteki standardowej dla [`std::sync::atomic`][atomic]<!-- ignore -->. Na
razie wystarczy wiedzieć, że typy atomowe działają jak typy prymitywne, ale
można je bezpiecznie współdzielić między wątkami.

Możesz się zastanawiać, dlaczego nie wszystkie typy prymitywne są atomowe i
dlaczego typy biblioteki standardowej nie są domyślnie zaimplementowane z
użyciem `Arc<T>`. Powodem jest to, że bezpieczeństwo wątkowe wiąże się z
kosztem wydajności, który warto ponosić tylko wtedy, gdy naprawdę trzeba. Jeśli
wykonujesz operacje na wartościach tylko w jednym wątku, twój kod może działać
szybciej, gdy nie musi egzekwować gwarancji zapewnianych przez typy atomowe.

Wróćmy do naszego przykładu: `Arc<T>` i `Rc<T>` mają to samo API, więc
naprawiamy program, zmieniając wiersz z `use`, wywołanie `new` i wywołanie
`clone`. Kod w listingu 16-15 w końcu się skompiluje i uruchomi.

<Listing number="16-15" file-name="src/main.rs" caption="Użycie `Arc<T>` do opakowania `Mutex<T>`, aby móc współdzielić własność między wieloma wątkami">

```rust
{{#rustdoc_include ../listings/ch16-fearless-concurrency/listing-16-15/src/main.rs}}
```

</Listing>

Ten kod wypisze:

<!-- Not extracting output because changes to this output aren't significant;
the changes are likely to be due to the threads running differently rather than
changes in the compiler -->

```text
Result: 10
```

Udało się! Policzyliśmy od 0 do 10, co może nie wydawać się zbyt imponujące,
ale nauczyło nas sporo o `Mutex<T>` i bezpieczeństwie wątkowym. Struktury tego
programu możesz też użyć do bardziej skomplikowanych operacji niż tylko
zwiększanie licznika. Stosując tę strategię, możesz podzielić obliczenia na
niezależne części, rozdzielić je między wątki, a następnie użyć `Mutex<T>`, aby
każdy wątek uzupełnił końcowy wynik o swoją część.

Zwróć uwagę, że jeśli wykonujesz proste operacje liczbowe, istnieją typy
prostsze od `Mutex<T>`, dostępne w [module `std::sync::atomic` biblioteki
standardowej][atomic]<!-- ignore -->. Zapewniają one bezpieczny, współbieżny,
atomowy dostęp do typów prymitywnych. W tym przykładzie użyliśmy `Mutex<T>` z
typem prymitywnym, aby skupić się na tym, jak działa `Mutex<T>`.

<!-- Old headings. Do not remove or links may break. -->

<a id="similarities-between-refcelltrct-and-mutextarct"></a>

### Porównanie `RefCell<T>`/`Rc<T>` i `Mutex<T>`/`Arc<T>` {#comparing-refcelltrct-and-mutextarct}

Być może zwróciło twoją uwagę, że `counter` jest niemutowalny, a mimo to
mogliśmy uzyskać mutowalną referencję do wartości w jego wnętrzu; oznacza to,
że `Mutex<T>` zapewnia wewnętrzną mutowalność (*interior mutability*), tak jak
rodzina `Cell`. W ten sam sposób, w jaki w rozdziale 15 użyliśmy `RefCell<T>`, aby móc
modyfikować zawartość wewnątrz `Rc<T>`, używamy `Mutex<T>` do modyfikowania
zawartości wewnątrz `Arc<T>`.

Warto też zauważyć, że Rust nie uchroni cię przed wszystkimi rodzajami błędów
logicznych, gdy używasz `Mutex<T>`. Przypomnij sobie z rozdziału 15, że użycie
`Rc<T>` wiązało się z ryzykiem utworzenia cykli referencji, w których dwie
wartości `Rc<T>` odwołują się do siebie nawzajem, powodując wycieki pamięci.
Podobnie `Mutex<T>` wiąże się z ryzykiem powstania _zakleszczeń_
(*deadlocks*). Występują one, gdy operacja musi zablokować dwa zasoby, a dwa
wątki uzyskały po jednej z blokad, przez co czekają na siebie nawzajem w
nieskończoność. Jeśli interesują cię zakleszczenia, spróbuj napisać program w
Ruście, w którym występuje zakleszczenie; następnie poszukaj strategii
zapobiegania zakleszczeniom dla mutexów w dowolnym języku i spróbuj
zaimplementować je w Ruście. Dokumentacja API biblioteki standardowej dla
`Mutex<T>` i `MutexGuard` zawiera przydatne informacje.

Zakończymy ten rozdział omówieniem traitów `Send` i `Sync` oraz tego, jak
możemy ich używać z własnymi typami.

{{#quiz ../quizzes/ch16-03-shared-state.toml}}

[atomic]: https://doc.rust-lang.org/std/sync/atomic/index.html

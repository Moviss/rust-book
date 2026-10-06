<!-- Old headings. Do not remove or links may break. -->

<a id="extensible-concurrency-with-the-sync-and-send-traits"></a>
<a id="extensible-concurrency-with-the-send-and-sync-traits"></a>

## Rozszerzalna współbieżność dzięki `Send` i `Sync` {#extensible-concurrency-with-send-and-sync}

Co ciekawe, niemal każdy omówiony dotąd w tym rozdziale mechanizm współbieżności
(*concurrency*) był częścią biblioteki standardowej, a nie samego języka. Twoje
możliwości obsługi współbieżności nie ograniczają się do języka ani biblioteki
standardowej: możesz pisać własne mechanizmy współbieżności albo korzystać z
tych napisanych przez innych.

Do kluczowych pojęć współbieżności wbudowanych w sam język, a nie w bibliotekę
standardową, należą jednak *traity* (cechy typów, zbliżone do interfejsów)
`Send` i `Sync` z modułu `std::marker`.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-transference-of-ownership-between-threads-with-send"></a>

### Przekazywanie własności między wątkami {#transferring-ownership-between-threads}

Trait znacznikowy (*marker trait*) `Send` wskazuje, że własność (*ownership*)
wartości typu implementującego `Send` można przekazywać między wątkami. Niemal
każdy typ w Ruście implementuje `Send`, ale są wyjątki, w tym `Rc<T>`: ten typ
nie może implementować `Send`, ponieważ gdyby sklonować wartość `Rc<T>` i
spróbować przekazać własność klonu do innego wątku, oba wątki mogłyby
jednocześnie aktualizować licznik referencji. Z tego powodu `Rc<T>` jest
przeznaczony do użycia w sytuacjach jednowątkowych, w których nie chcesz płacić
wydajnościowej ceny za bezpieczeństwo wątkowe.

System typów Rusta i ograniczenia traitów (*trait bounds*) gwarantują więc, że
nigdy przypadkiem nie prześlesz wartości `Rc<T>` między wątkami w niebezpieczny
sposób. Gdy próbowaliśmy to zrobić w listingu 16-14, otrzymaliśmy błąd
`` the trait `Send` is not implemented for `Rc<Mutex<i32>>` ``. Kiedy
przeszliśmy na `Arc<T>`, który implementuje `Send`, kod się skompilował.

Każdy typ złożony wyłącznie z typów `Send` również jest automatycznie oznaczany
jako `Send`. Niemal wszystkie typy prymitywne są `Send`, z wyjątkiem surowych
wskaźników (*raw pointers*), które omówimy w rozdziale 20.

<!-- Old headings. Do not remove or links may break. -->

<a id="allowing-access-from-multiple-threads-with-sync"></a>

### Dostęp z wielu wątków {#accessing-from-multiple-threads}

Trait znacznikowy `Sync` wskazuje, że do typu implementującego `Sync` można
bezpiecznie odwoływać się z wielu wątków. Innymi słowy, dowolny typ `T`
implementuje `Sync`, jeśli `&T`, czyli niemutowalna (*immutable*) referencja
(*reference*) do `T`, implementuje `Send`, co oznacza, że referencję można
bezpiecznie przesłać do innego wątku. Podobnie jak w przypadku `Send`, wszystkie
typy prymitywne implementują `Sync`, a typy złożone wyłącznie z typów
implementujących `Sync` również implementują `Sync`.

<!-- BEGIN INTERVENTION: 43081862-aac8-4e18-9c55-1107ea4c7cc1 -->

`Sync` to w Ruście pojęcie najbliższe potocznemu znaczeniu określenia „bezpieczny wątkowo”, czyli tego, że z danego fragmentu danych może bezpiecznie korzystać wiele współbieżnych wątków. Osobne traity `Send` i `Sync` istnieją dlatego, że typ może być czasem jednym z nich, obydwoma albo żadnym. Na przykład:
*  Inteligentny wskaźnik (*smart pointer*) `Rc<T>` nie jest ani `Send`, ani `Sync` z opisanych wyżej powodów.
* Typ `RefCell<T>` (o którym mówiliśmy w rozdziale 15) oraz
rodzina pokrewnych typów `Cell<T>` są `Send` (jeśli `T: Send`), ale nie są `Sync`. `RefCell` można przesłać przez granicę wątku, ale nie można z niego korzystać współbieżnie, ponieważ sprawdzanie pożyczeń, które `RefCell<T>` wykonuje w czasie działania programu, nie jest zaimplementowane w sposób bezpieczny wątkowo. 
* Inteligentny wskaźnik `Mutex<T>` jest `Send` i `Sync`, więc można go używać do współdzielenia dostępu między wieloma wątkami, jak widać było w podrozdziale [„Współdzielony dostęp do `Mutex<T>`”][sharing-a-mutext-between-multiple-threads]<!-- ignore -->.
* Typ `MutexGuard<'a, T>` zwracany przez `Mutex::lock` jest `Sync` (jeśli `T: Sync`), ale nie jest `Send`. Nie jest `Send` właśnie dlatego, że [niektóre platformy wymagają, by mutex odblokował ten sam wątek, który go zablokował][mutex-guards-are-not-send].

<!-- END INTERVENTION: 43081862-aac8-4e18-9c55-1107ea4c7cc1 -->



### Ręczna implementacja `Send` i `Sync` jest niebezpieczna {#implementing-send-and-sync-manually-is-unsafe}

Ponieważ typy złożone wyłącznie z innych typów implementujących traity `Send` i
`Sync` same automatycznie implementują `Send` i `Sync`, nie musimy
implementować tych traitów ręcznie. Jako traity znacznikowe nie mają one nawet
żadnych metod do zaimplementowania. Przydają się jedynie do egzekwowania
niezmienników związanych ze współbieżnością.

Ręczna implementacja tych traitów wymaga pisania kodu w niebezpiecznym Ruście
(*unsafe Rust*). O używaniu niebezpiecznego Rusta opowiemy w rozdziale 20; na
razie ważne jest to, że budowanie nowych typów współbieżnych, które nie składają
się z części `Send` i `Sync`, wymaga starannego przemyślenia, by zachować
gwarancje bezpieczeństwa. [„The Rustonomicon”][nomicon] zawiera więcej
informacji o tych gwarancjach i o tym, jak ich dotrzymać.

## Podsumowanie {#summary}

To nie ostatnie spotkanie ze współbieżnością w tej książce: następny rozdział
poświęcony jest programowaniu asynchronicznemu, a projekt z rozdziału 21
wykorzysta pojęcia z tego rozdziału w bardziej realistycznej sytuacji niż
omawiane tutaj mniejsze przykłady.

Jak wspomnieliśmy wcześniej, ponieważ bardzo niewiele z tego, jak Rust obsługuje
współbieżność, jest częścią języka, wiele rozwiązań współbieżnych
zaimplementowano jako *crate’y* (jednostki kompilacji w Ruście). Rozwijają się
one szybciej niż biblioteka standardowa, więc koniecznie poszukaj w sieci
aktualnych, najnowocześniejszych crate’ów do użycia w sytuacjach wielowątkowych.

Biblioteka standardowa Rusta udostępnia kanały do przekazywania komunikatów
(*message passing*) oraz typy inteligentnych wskaźników, takie jak `Mutex<T>` i
`Arc<T>`, których można bezpiecznie używać w kontekstach współbieżnych. System
typów i *borrow checker* (mechanizm sprawdzania pożyczeń) gwarantują, że kod
korzystający z tych rozwiązań nie będzie zawierał wyścigów danych ani
nieprawidłowych referencji. Gdy już uda ci się skompilować kod, możesz mieć pewność, że będzie
bez problemu działał w wielu wątkach, bez trudnych do wytropienia błędów
typowych dla innych języków. Programowanie współbieżne nie jest już czymś, czego
trzeba się bać: ruszaj w świat i czyń swoje programy współbieżnymi – bez lęku!

{{#quiz ../quizzes/ch16-04-extensible-concurrency-send-and-sync.toml}}

[sharing-a-mutext-between-multiple-threads]: ch16-03-shared-state.html#sharing-a-mutext-between-multiple-threads
[nomicon]: https://doc.rust-lang.org/nomicon/index.html
[mutex-guards-are-not-send]: https://github.com/rust-lang/rust/issues/23465#issuecomment-82730326

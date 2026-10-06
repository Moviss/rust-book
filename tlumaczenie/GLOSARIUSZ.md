# Glosariusz

Obowiązuje tłumaczy i recenzentów (zob. `KONWENCJE.md`, sekcja „Terminologia”).
Zmienia go wyłącznie orkiestrator. Nowe terminy zgłaszaj w raporcie.

Kolumny: **EN | PL | Pierwsze wystąpienie | Zakazane (regex) | Uwagi**. Propozycje oznaczone wcześniej „?” zostały
potwierdzone w pilocie (Faza 2) i już się ich nie zmienia. Regexy dopasowuje `glosariusz_lint.py`. Słowa wieloznaczne celowo nie są
zakazane (np. „zakres”, „zamknięcie”, „odwołanie”, „zmienny”); pilnuje ich
recenzent.

| EN | PL | Pierwsze wystąpienie | Zakazane (regex) | Uwagi |
|---|---|---|---|---|
| ownership | własność | własność (*ownership*) | `\bposiadani\w*` | owner → właściciel |
| borrowing / to borrow | pożyczanie / pożyczyć | pożyczanie (*borrowing*) | `\bzapożycz\w*` | a borrow → pożyczenie |
| borrow checker | borrow checker | *borrow checker* (mechanizm sprawdzania pożyczeń) | `\bsprawdzacz\w*` | odmiana: borrow checkera |
| reference | referencja | referencja (*reference*) | `\bodnośnik\w*` | |
| mutable / immutable | mutowalny / niemutowalny | mutowalny (*mutable*) | `\bmodyfikowaln\w*` | mutability → mutowalność; nie „zmienny” (koliduje ze „zmienna”) |
| variable | zmienna | — | | |
| shadowing | przesłanianie | przesłanianie (*shadowing*) | `\bcieniowani\w*` | |
| scope | zasięg | zasięg (*scope*) | | „zakres” zarezerwowany dla *range* |
| range | zakres | — | | |
| move | przeniesienie / przenieść | przeniesienie (*move*) | | |
| copy / clone | kopiowanie / klonowanie | — | | traity `Copy`/`Clone` jako kod |
| drop | zwolnienie / zwolnić | zwolnienie (*drop*) | `\bupuszcz\w*` | „wartość zostaje zwolniona” |
| stack / heap | stos / sterta | stos (*stack*), sterta (*heap*) | `\bkop(iec\|c\w+)\b` | |
| pointer | wskaźnik | — | | |
| smart pointer | inteligentny wskaźnik | inteligentny wskaźnik (*smart pointer*) | | |
| raw pointer | surowy wskaźnik | surowy wskaźnik (*raw pointer*) | | |
| dangling reference | wisząca referencja | wisząca referencja (*dangling reference*) | | |
| dereference | dereferencja | dereferencja (*dereference*) | `\bwyłuskani\w*` | czasownik: „wykonać dereferencję” |
| deref coercion | deref coercion | *deref coercion* (automatyczna konwersja przez dereferencję) | | |
| undefined behavior | niezdefiniowane zachowanie | niezdefiniowane zachowanie (*undefined behavior*) | | |
| permission (Brown) | uprawnienie | uprawnienie (*permission*) | | litery R/W/O/F zostają |
| lifetime | czas życia | czas życia (*lifetime*) | `\bżywotnoś\w*` | lifetime elision → pomijanie czasów życia (*lifetime elision*) |
| slice | wycinek | wycinek (*slice*) | `\bplast(er\|r)\w*` | string slice → wycinek łańcucha (*string slice*) |
| string | łańcuch znaków | łańcuch znaków (*string*) | | skrótowo „łańcuch”; typ `String` jako kod |
| struct | struktura | struktura (*struct*) | | |
| enum | enum | *enum* (typ wyliczeniowy) | | odmiana: enuma, enumy |
| variant / field | wariant / pole | — | | |
| method | metoda | — | | |
| associated function | funkcja powiązana | funkcja powiązana (*associated function*) | `\bstowarzyszon\w*` | |
| associated type | typ powiązany | typ powiązany (*associated type*) | | |
| trait | trait | *trait* (cecha typu, zbliżona do interfejsu) | | odmiana: traitu, traity; alternatywa „cecha” |
| trait object | obiekt traitu | obiekt traitu (*trait object*) | | |
| trait bound | ograniczenie traitu | ograniczenie traitu (*trait bound*) | | |
| generics | typy generyczne | typy generyczne (*generics*) | `\btyp\w* ogóln\w*` | type parameter → parametr typu |
| pattern / pattern matching | wzorzec / dopasowywanie wzorców | dopasowywanie wzorców (*pattern matching*) | | match arm → ramię (*arm*) |
| refutable / irrefutable | odrzucalny / nieodrzucalny | wzorzec odrzucalny (*refutable*) | | |
| closure | domknięcie | domknięcie (*closure*) | | nie „zamknięcie” (zarezerwowane m.in. dla zamykania kanału) |
| iterator / iterator adapter | iterator / adapter iteratora | adapter iteratora (*iterator adapter*) | | consuming adapter → adapter konsumujący |
| crate | crate | *crate* (jednostka kompilacji w Ruście) | `\bskrzyn\w*` | odmiana: crate’a, crate’owi, w crate’cie, crate’y, crate’ów |
| package | pakiet | pakiet (*package*) | | |
| module / module tree | moduł / drzewo modułów | — | | |
| path | ścieżka | — | | |
| workspace | przestrzeń robocza | przestrzeń robocza (*workspace*) | | |
| dependency | zależność | — | | |
| release profile | profil wydania | profil wydania (*release profile*) | | |
| panic | panika / panikować | panika (*panic*) | | „program panikuje” |
| recoverable / unrecoverable error | błąd odwracalny / nieodwracalny | błąd odwracalny (*recoverable error*) | | |
| error propagation | propagowanie błędów | — | | |
| unit / integration test | test jednostkowy / integracyjny | — | | assertion → asercja |
| thread | wątek | — | | |
| concurrency / parallelism | współbieżność / równoległość | współbieżność (*concurrency*) | | |
| message passing | przekazywanie komunikatów | przekazywanie komunikatów (*message passing*) | | channel → kanał |
| mutex / lock | mutex / blokada | — | | „uzyskać blokadę” |
| deadlock | zakleszczenie | zakleszczenie (*deadlock*) | | |
| race condition / data race | wyścig / wyścig danych | sytuacja wyścigu (*race condition*) | | |
| reference counting | zliczanie referencji | zliczanie referencji (*reference counting*) | | |
| interior mutability | wewnętrzna mutowalność | wewnętrzna mutowalność (*interior mutability*) | | |
| future | future | *future* (wartość, która będzie gotowa później) | | odmiana: future’a |
| async runtime | środowisko uruchomieniowe | środowisko uruchomieniowe (*runtime*) | | |
| stream | strumień | strumień (*stream*) | | |
| graceful shutdown | łagodne zamykanie | łagodne zamykanie (*graceful shutdown*) | | rozdział 21 |
| macro | makro | — | | l.mn. makra; deklaratywne / proceduralne |
| unsafe Rust | niebezpieczny Rust | niebezpieczny Rust (*unsafe Rust*) | | słowo kluczowe `unsafe` jako kod |
| statement / expression | instrukcja / wyrażenie | instrukcja (*statement*), wyrażenie (*expression*) | | |
| tuple / array / vector | krotka / tablica / wektor | krotka (*tuple*) | | |
| hash map | mapa haszująca | mapa haszująca (*hash map*) | `\btablic\w* mieszając\w*` | |
| type inference | wnioskowanie typów | wnioskowanie typów (*type inference*) | | type annotation → adnotacja typu |
| zero-cost abstraction | abstrakcja o zerowym koszcie | abstrakcja o zerowym koszcie (*zero-cost abstraction*) | | |
| toolchain | zestaw narzędzi | zestaw narzędzi (*toolchain*) | | |
| standard library / prelude | biblioteka standardowa / prelude | *prelude* (zestaw elementów importowanych automatycznie) | | |
| attribute / derive | atrybut / derive | — | | `#[derive]` jako kod |
| Ownership Inventory (Brown) | Inwentaryzacja własności | — | | tytuł sekcji quizów |
| Rustaceans | rustowcy | rustowcy (*Rustaceans*) | `\brustacean\w*` | nazwa społeczności, piszemy małą literą |
| package manager | menedżer pakietów | — | | |
| build system | system budowania | — | | |
| build (rzeczownik) / debug build | kompilacja / wersja debugowa | — | | release build → wersja wydaniowa |
| executable / binary | plik wykonywalny / plik binarny | — | | |
| linker | linker | *linker* (konsolidator) | | |
| command line / terminal / shell | wiersz poleceń / terminal / powłoka | — | | prompt → znak zachęty |
| edition | edycja | edycja (*edition*) | | edycja 2024 |
| ahead-of-time compiled | kompilowany z wyprzedzeniem | kompilowany z wyprzedzeniem (*ahead-of-time compiled*) | | |
| compile time / run time | czas kompilacji / czas działania | w czasie kompilacji (*compile-time*) | | |
| box (`Box`) | box | *box* (wskaźnik na dane umieszczone na stercie) | `\bpude[łl]\w*` | odmiana: boxa, boxem, boxy, boxów |
| stack frame | ramka stosu | ramka (*frame*) | | |
| pointee | wartość wskazywana | wartość wskazywana (*pointee*) | | |
| allocate / deallocate / free | alokować / dealokować / zwolnić | — | | allocation → alokacja |
| benchmark | test wydajności | test wydajności (*benchmark*) | | |
| free / drop (dealokacja) | zwalnianie / zwolnić | zwalnianie (*freeing* lub *dropping*) | | gdy oryginał podaje oba słowa naraz |
| mutate | modyfikować | — | | „mutowalny” tylko dla *mutable* |
| endpoint | endpoint | — | | |
| segmentation fault | błąd segmentacji | — | | |
| dependency manager / build tool | menedżer zależności / narzędzie do budowania | — | | |
| nightly Rust | Rust nightly | — | | kanały: stable, beta, nightly |
| task (async) | zadanie | — | | |
| legacy code | zastany kod | — | | |
| open source / fork / code review | open source / fork / przegląd kodu | — | | |
| Rust Foundation / Rust Project | Rust Foundation / Projekt Rust | — | | nazwy własne |
| keyword | słowo kluczowe | słowo kluczowe (*keyword*) | | |
| control flow | przepływ sterowania | przepływ sterowania (*control flow*) | | |
| constant | stała | stała (*constant*) | | constant expression → wyrażenie stałe |
| unit type | typ jednostkowy | typ jednostkowy (*unit type*) | | wartość `()` jako kod |
| parameter / argument | parametr / argument | — | | |
| function signature | sygnatura funkcji | — | | |
| return value / return type | wartość zwracana / typ zwracany | — | | |
| binding (let) | wiązanie | — | | „zmienna jest związana z wartością” |
| evaluate to | dawać (wartość), obliczać się do | — | | „wyrażenie daje wartość 6” |
| format string | łańcuch formatujący | — | | |
| hardcoded | wpisany na sztywno | — | | |
| snake case | *snake case* | — | | nazwa stylu, bez tłumaczenia |
| unit value `()` | wartość jednostkowa | wartość jednostkowa (*unit*) | | typ: typ jednostkowy (*unit type*); nie „unit” bez tłumaczenia |
| data type / scalar / compound | typ danych / skalarny / złożony | — | | |
| integer / floating-point / Boolean | liczba całkowita / zmiennoprzecinkowa / wartość logiczna | — | | signed/unsigned → ze znakiem / bez znaku |
| integer overflow / wrapping | przepełnienie liczby całkowitej / zawijanie | — | | |
| literal | literał | — | | |
| destructuring | destrukturyzacja | — | | |
| loop label / iteration | etykieta pętli / iteracja | — | | |
| arm (`if`, `match`) | ramię | ramię (*arm*) | | |
| placeholder | symbol zastępczy | symbol zastępczy (*placeholder*) | | |
| handle | uchwyt | — | | |
| registry | rejestr | — | | crates.io jako nazwa własna |
| binary crate / library crate | crate binarny / crate biblioteczny | — | | |
| Semantic Versioning | wersjonowanie semantyczne | — | | |
| comment / documentation comment | komentarz / komentarz dokumentacyjny | — | | |
| garbage collector | mechanizm odśmiecania pamięci | mechanizm odśmiecania pamięci (*garbage collector*) | | |
| memory safety | bezpieczeństwo pamięci | — | | |
| debug mode / release mode | tryb debugowania / tryb wydania | — | | |
| place (Brown) | miejsce | miejsce (*place*) | | |
| use-after-free / double-free | użycie po zwolnieniu / podwójne zwolnienie | użycie po zwolnieniu (*use-after-free*) | | |
| alias / aliasing | alias / aliasowanie | — | | type alias → alias typu |
| shared reference | referencja współdzielona | — | | |
| fat pointer | „gruby” wskaźnik | „gruby” wskaźnik (*fat pointer*) | | |
| string literal | literał łańcuchowy | — | | |
| collection | kolekcja | — | | |
| statically typed | statycznie typowany | — | | |
| primitive type | typ prymitywny | — | | |
| mutation | modyfikowanie | modyfikowanie (*mutation*) | | |
| immutable / mutable reference | referencja niemutowalna / mutowalna | — | | shared → współdzielona, unique → unikalna |
| non-owning pointer | wskaźnik niebędący właścicielem | — | | |
| Pointer Safety Principle (Brown) | zasada bezpieczeństwa wskaźników | — | | |
| capacity | pojemność | — | | |
| syntactic sugar | lukier składniowy | — | | |
| lifetime parameter | parametr czasu życia | — | | |
| derive (czasownik) / derivable trait | wyprowadzać / trait wyprowadzalny | wyprowadzać (*derive*) | | „wyprowadzić trait `Debug`”; derived trait → trait wyprowadzony |
| refactor | refaktoryzować / refaktoryzacja | — | | |
| instance | instancja | — | | |
| outer attribute | atrybut zewnętrzny | — | | |
| standard output / standard error | standardowe wyjście / standardowe wyjście błędów | — | | |
| field init shorthand | skrócona inicjalizacja pól | skrócona inicjalizacja pól (*field init shorthand*) | | |
| struct update syntax | składnia aktualizacji struktury | składnia aktualizacji struktury (*struct update syntax*) | | |
| tuple struct / unit-like struct | struktura krotkowa / struktura jednostkowa | struktura krotkowa (*tuple struct*) | | |
| dot notation | notacja kropkowa | — | | |
| owned type | typ będący właścicielem swoich danych | — | | |
| getter | getter | getter (*getter*, metoda dostępowa) | | |
| reborrow | ponowne pożyczenie | — | | |
| constructor | konstruktor | — | | |
| namespace | przestrzeń nazw | — | | |
| substring | podłańcuch | — | | |
| tracing collector | odśmiecanie ze śledzeniem | — | | |
| exhaustive / exhaustiveness | wyczerpujący / wyczerpywalność | wyczerpujący (*exhaustive*) | | |
| catch-all pattern | wzorzec przechwytujący wszystko | wzorzec przechwytujący wszystko (*catch-all*) | | |
| wildcard | symbol wieloznaczny | — | | |
| null | null | — | | nieodmienne; wartość null, referencja null |
| type system | system typów | — | | |
| invariant | niezmiennik | — | | |
| constructor function (wariant enuma) | funkcja konstruująca | — | | |
| owns (dane) | jest właścicielem | — | | unikamy „posiada”; *property* → właściwość (nie „własność”) |
| reallocate | realokować | — | | |
| reference-counted pointer | wskaźnik ze zliczaniem referencji | — | | |
| boilerplate | szablonowy kod | szablonowy kod (*boilerplate*) | | |
| happy path | szczęśliwa ścieżka | szczęśliwa ścieżka (*happy path*) | | |
| branch (`if`/`else`) | gałąź | — | | odróżniamy od ramienia (*arm*) w `match` |
| anti-pattern | antywzorzec | — | | |
| caller | kod wywołujący / wywołujący | — | | |
| crate root | korzeń crate’a | korzeń crate’a (*crate root*) | | |
| item | element | — | | |
| privacy / private / public | prywatność / prywatny / publiczny | prywatność (*privacy*) | | |
| glob operator | operator glob | operator glob (*glob operator*) | | |
| submodule / parent / child / sibling | podmoduł / rodzic (moduł nadrzędny) / dziecko / rodzeństwo | — | | |
| encapsulation | hermetyzacja | — | | |
| module system | system modułów | system modułów (*module system*) | | |
| root module | moduł główny | — | | |
| build script | skrypt budowania | — | | |
| method syntax | składnia metod | składnia metod (*method syntax*) | | |
| receiver (metody) | odbiorca metody | — | | |
| absolute / relative path | ścieżka bezwzględna / względna | ścieżka bezwzględna (*absolute path*) | | |
| make public | upublicznić | — | | |
| ancestor module | przodek | — | | |
| re-export | reeksportować / reeksportowanie | reeksportowanie (*re-exporting*) | | |
| nested path | ścieżka zagnieżdżona | — | | |
| idiomatic | idiomatyczny | — | | |
| binding mode | tryb wiązania | — | | |
| dangling pointer | wiszący wskaźnik | — | | |
| clone-on-write | klonowanie przy zapisie | — | | |
| map | mapa | mapa (*map*) | | |
| vector | wektor | wektor (*vector*) | | |
| backtrace | ślad stosu | ślad stosu (*backtrace*) | | |
| unwinding / aborting | zwijanie stosu / przerwanie | zwijanie stosu (*unwinding*) | | |
| exception | wyjątek | — | | |
| call stack | stos wywołań | — | | |
| bug | błąd (bug, gdy trzeba odróżnić od *error*) | — | | |
| grapheme cluster | klaster grafemów | — | | |
| Unicode scalar value | wartość skalarna Unicode | — | | |
| wrapper | opakowanie | — | | |
| concatenate | łączyć | — | | |
| buffer overflow / overread | przepełnienie bufora / odczyt poza buforem | — | | |
| hashing function / hasher | funkcja haszująca / *hasher* | funkcja haszująca (*hashing function*) | | |
| hash table | tablica haszująca | — | | |
| key-value pair | para klucz–wartość | — | | |
| entry (mapa) | wpis | — | | |
| extract a function | wyodrębnić funkcję | — | | |
| duplication | powielanie kodu | — | | |
| feature (języka/narzędzia) | mechanizm / funkcjonalność | — | | nie „funkcja” (koliduje z *function*) |
| line (kodu) | wiersz | — | | „linia” tylko dla wyjścia programu |
| contract (funkcji) | kontrakt | — | | |
| validation | walidacja | — | | |
| vulnerability | podatność | — | | |
| type checking | sprawdzanie typów | — | | |
| monomorphization | monomorfizacja | monomorfizacja (*monomorphization*) | | |
| concrete type | typ konkretny | — | | |
| generic type parameter | generyczny parametr typu | — | | |
| file handle | uchwyt pliku | — | | |
| propagate (error) | propagować (błąd) | propagowanie (*propagating*) błędu | | |
| early return | wczesny powrót | — | | |
| method chaining | łączenie wywołań metod w łańcuch | — | | |
| question mark operator | operator `?` (znaku zapytania) | — | | |
| default implementation | implementacja domyślna | — | | |
| blanket implementation | implementacja zbiorcza | implementacja zbiorcza (*blanket implementation*) | | |
| coherence / orphan rule | spójność / reguła sieroty | reguła sieroty (*orphan rule*) | | |
| implementor | typ implementujący | — | | |
| where clause | klauzula `where` | — | | |
| subslice | podwycinek | — | | |
| denial-of-service (DoS) | atak DoS (odmowa usługi) | — | | |
| Pig Latin | świńska łacina | świńska łacina (*Pig Latin*) | | |
| test binary / test suite | testowy plik binarny / zestaw testów | — | | |
| flag (CLI) | flaga | — | | |
| capture (output) | przechwytywać | — | | |
| thread-safe | bezpieczny wątkowo | — | | |
| debug symbols | symbole debugowania | — | | |
| environment variable | zmienna środowiskowa | — | | |
| robust / reliable | solidny / niezawodny | — | | rozróżniamy |
| recover (from error) | obsłużyć błąd i kontynuować | — | | |
| lifetime annotation | adnotacja czasu życia | — | | |
| lifetime elision rules | reguły pomijania czasów życia | reguły pomijania czasów życia (*lifetime elision rules*) | | |
| input / output lifetime | wejściowy / wyjściowy czas życia | wejściowe czasy życia (*input lifetimes*) | | |
| static lifetime | statyczny czas życia | — | | |
| angle brackets | nawiasy ostre | — | | |
| doc test | test dokumentacyjny | — | | nie „test dokumentacji” |
| test coverage | pokrycie testami | — | | |
| helper function | funkcja pomocnicza | — | | |
| test runner / test harness | program uruchamiający testy / środowisko testowe | program uruchamiający testy (*test runner*) | | |
| test passes / fails | test przechodzi / kończy się niepowodzeniem | — | | |
| separation of concerns | rozdzielanie odpowiedzialności | rozdzielanie odpowiedzialności (*separation of concerns*) | | |
| side effect | efekt uboczny | — | | |
| exit status | kod wyjścia | — | | |
| parse / parser | parsować / parser | — | | |
| maintainer | osoba utrzymująca kod | — | | |
| test-driven development | programowanie sterowane testami (TDD) | programowanie sterowane testami (*test-driven development*, TDD) | | |
| poem (w rozdz. 12) | utwór | — | | „wiersz” zarezerwowany dla *line* |
| correctness | poprawność | — | | |
| filtering (testów) | filtrowanie | — | | |
| case-insensitive | bez rozróżniania wielkości liter | — | | |
| failing test | test kończący się niepowodzeniem | — | | |
| I/O | wejście-wyjście | — | | |
| stream (stdout) | strumień | — | | |
| iterator pattern | wzorzec iteratora | — | | |
| lazy | leniwy | leniwy (*lazy*) | | |
| consuming adapter | adapter konsumujący | adapter konsumujący (*consuming adapter*) | | |
| capture (environment) | przechwytywać (środowisko) | — | | |
| predicate | predykat | — | | |
| zero-overhead | zerowy narzut | zasada zerowego narzutu (*zero-overhead*) | | |
| runtime overhead | narzut w czasie działania | — | | |
| loop unrolling / bounds checking | rozwijanie pętli / sprawdzanie granic | — | | |
| top-level function | funkcja najwyższego poziomu | — | | |
| function traits | traity `Fn` / traity funkcyjne | — | | |
| halting problem | problem stopu | — | | |
| query (minigrep) | zapytanie | — | | |
| skeleton implementation | szkieletowa implementacja | — | | |
| binary / library target | cel binarny / cel biblioteczny | cel binarny (*binary target*) | | |
| subcommand | podpolecenie | — | | |
| optimization level | poziom optymalizacji | — | | |
| development profile | profil deweloperski | — | | |
| generic type | typ generyczny | typ generyczny (*generic type*) | | liczba pojedyncza; l.mn. → typy generyczne (*generics*) |
| toilet closure | „domknięcie-toaleta” | — | | |
| yank | wycofanie / wycofać | wycofanie (*yanking*) | | `cargo yank` jako kod |
| API token | token API | — | | |
| path dependency | zależność określona ścieżką | — | | |
| member (workspace) | członek przestrzeni roboczej | — | | |
| resolver (Cargo) | algorytm rozwiązywania zależności | — | | |
| dereference operator | operator dereferencji | — | | |
| wrapper type | typ opakowujący | — | | |
| cons list | lista cons | lista cons (*cons list*) | | |
| recursive type | typ rekurencyjny | typ rekurencyjny (*recursive type*) | | |
| indirection | pośredniość | pośredniość (*indirection*) | | |
| linked list | lista powiązana | — | | nie „lista połączona” |
| reference cycle | cykl referencji | — | | |
| memory leak | wyciek pamięci | — | | |
| multiple ownership | współwłasność | — | | |
| deep copy | głęboka kopia | — | | |
| data race | wyścig danych | — | | |
| destructor | destruktor | destruktor (*destructor*) | | |
| clean up | sprzątać / kod porządkujący | — | | |
| allocator | alokator | — | | |
| socket | gniazdo | — | | |
| strong / weak reference | silna / słaba referencja | silna referencja (*strong reference*) | | |
| reference count | licznik referencji | — | | |
| node / tree | węzeł / drzewo | — | | |
| stack overflow | przepełnienie stosu | — | | |
| test double / mock object | dubler testowy / atrapa | dubler testowy (*test double*) | | |
| static analysis | analiza statyczna | — | | |
| single-/multithreaded | jednowątkowy / wielowątkowy | — | | |
| main / spawned thread | wątek główny / nowy (utworzony) wątek | — | | |
| transmitter / receiver | nadajnik / odbiornik | — | | |
| producer / consumer | producent / konsument | — | | |
| actor | aktor | — | | |
| shared-state concurrency | współbieżność ze współdzielonym stanem | — | | |
| concurrency primitive | prymityw współbieżności | — | | |
| mutual exclusion | wzajemne wykluczanie | — | | |
| atomic | atomowy / typy atomowe | — | | |
| join handle | uchwyt wątku | — | | |
| thread safety | bezpieczeństwo wątkowe | — | | |
| marker trait | trait znacznikowy | trait znacznikowy (*marker trait*) | | |
| fearless concurrency | nieustraszona współbieżność | nieustraszona współbieżność (*fearless concurrency*) | | |
| process | proces | — | | |
| block (thread) | blokować / zablokowanie | — | | „blokada” zarezerwowana dla *lock* |
| asynchronous programming | programowanie asynchroniczne | programowanie asynchroniczne (*asynchronous programming*) | | |
| CPU-bound / I/O-bound | ograniczony przez procesor / przez wejście-wyjście | — | | |
| blocking / non-blocking | blokujący / nieblokujący | — | | |
| future (l.mn.) | future’y | — | | |
| subtask | podzadanie | — | | |
| parallelism | równoległość | równoległość (*parallelism*) | | |
| polling / poll | odpytywanie | odpytywanie (*polling*) | | |
| await (future) | oczekiwać na future’a | — | | `await` jako kod |
| await point | punkt oczekiwania | punkt oczekiwania (*await point*) | | |
| executor | egzekutor | egzekutor (*executor*) | | |
| state machine | maszyna stanów | — | | |
| async block / function | blok async / funkcja asynchroniczna | — | | „blok `async`”, gdy oryginał ma kod inline; nie „punkt await”, lecz „punkt oczekiwania” |
| starvation | zagłodzenie | — | | |
| yield control | oddawać sterowanie | — | | |
| cooperative multitasking | wielozadaniowość kooperacyjna | wielozadaniowość kooperacyjna (*cooperative multitasking*) | | |
| timeout | limit czasu | — | | |
| fair / fairness | sprawiedliwy / sprawiedliwość | — | | |
| bounded / unbounded channel | kanał ograniczony / nieograniczony | — | | |
| spawn (task) | utworzyć zadanie | — | | |
| shared-memory concurrency | współbieżność ze współdzieloną pamięcią | — | | |
| guard (mutex) | strzec | — | | |
| work stealing | kradzież pracy | kradzież pracy (*work stealing*) | | |
| fire and forget | „odpal i zapomnij” | — | | |
| embedded system | system wbudowany | — | | |
| object-oriented programming | programowanie obiektowe | programowanie obiektowe (*object-oriented programming*) | | |
| inheritance | dziedziczenie | dziedziczenie (*inheritance*) | | |
| polymorphism | polimorfizm | polimorfizm (*polymorphism*) | | |
| parent / child class | klasa nadrzędna / podrzędna | — | | |
| override | nadpisywać | — | | nie „przesłaniać” (shadowing) |
| design pattern | wzorzec projektowy | — | | |
| Gang of Four | Banda Czworga | — | | |
| static / dynamic dispatch | statyczne / dynamiczne wywoływanie | dynamiczne wywoływanie (*dynamic dispatch*) | | |
| dyn compatibility | zgodność z dyn | zgodność z dyn (*dyn compatibility*) | | |
| duck typing | typowanie kaczkowe | typowanie kaczkowe (*duck typing*) | | |
| downcast | rzutować w dół | — | | |
| GUI | graficzny interfejs użytkownika (GUI) | — | | |
| pin / pinning | przypiąć / przypinanie | przypiąć (*pin*) | | |
| self-referential | samoreferencyjny | — | | |
| state pattern / state object | wzorzec stanu / obiekt stanu | wzorzec stanu (*state pattern*) | | |
| delegate | delegować | — | | |
| extension trait | trait rozszerzający | — | | |
| virtual table | tablica metod wirtualnych | — | | |
| inlining | wstawianie w miejsce wywołania | wstawianie w miejsce wywołania (*inlining*) | | |
| match guard | strażnik dopasowania | strażnik dopasowania (*match guard*) | | |
| `@` binding | wiązanie `@` | — | | |
| inclusive range | zakres domknięty | — | | |
| design trade-off | kompromis projektowy | — | | |
| callback | funkcja zwrotna | — | | |
| asset | zasób | — | | |
| widget | widżet | — | | |
| serialization | serializacja | — | | |
| overloading | przeciążanie | — | | |
| marker type | typ znacznikowy | — | | |
| cast | rzutować | — | | |
| outlive | żyć dłużej niż | — | | |
| intermediate representation | reprezentacja pośrednia | — | | |
| refutability | odrzucalność | — | | |
| body (funkcji, pętli, bloku) | treść | — | | nie „ciało” |
| join handle (zadanie) | uchwyt zadania | — | | |
| web scraper | *web scraper* | *web scraper* (program pobierający dane ze stron internetowych) | | |
| compute-bound | ograniczony przez obliczenia | — | | |
| timer | timer | — | | |
| superpowers (unsafe) | supermoce | — | | |
| static variable / global variable | zmienna statyczna / globalna | — | | |
| union | unia | unia (*union*) | | |
| FFI | interfejs funkcji obcych (FFI) | interfejs funkcji obcych (*Foreign Function Interface*, FFI) | | |
| ABI | binarny interfejs aplikacji (ABI) | — | | |
| name mangling | dekorowanie nazw | dekorowanie nazw (*mangling*) | | |
| unsound | nieprawidłowy | nieprawidłowy (*unsound*) | | |
| newtype pattern / never type | wzorzec newtype / typ never | — | | |
| fully qualified syntax | w pełni kwalifikowana składnia | — | | |
| supertrait | supertrait | — | | |
| function pointer | wskaźnik na funkcję | — | | |
| operator overloading | przeciążanie operatorów | — | | |
| associated items | elementy powiązane | — | | |
| bounded parametric polymorphism | ograniczony polimorfizm parametryczny | — | | |
| single inheritance | dziedziczenie pojedyncze | — | | |
| struct field shorthand (wzorce) | skrócony zapis pól | — | | |

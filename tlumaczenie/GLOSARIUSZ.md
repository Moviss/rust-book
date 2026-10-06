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
| crate | crate | *crate* (jednostka kompilacji w Ruście) | `\bskrzyn\w*` | odmiana: crate’a, crate’y, crate’ów |
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

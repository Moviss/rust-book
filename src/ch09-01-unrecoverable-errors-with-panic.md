## Błędy nieodwracalne i `panic!` {#unrecoverable-errors-with-panic}

Czasem w kodzie dzieje się coś złego i nic nie da się z tym zrobić. Na takie
sytuacje Rust ma makro `panic!`. W praktyce panikę (*panic*) można wywołać na
dwa sposoby: wykonując działanie, które sprawia, że kod panikuje (na przykład
sięgając poza koniec tablicy), albo jawnie wywołując makro `panic!`. W obu
przypadkach program panikuje. Domyślnie panika wypisuje komunikat o błędzie,
zwija i czyści stos, a następnie kończy program. Za pomocą zmiennej
środowiskowej możesz też sprawić, że Rust w chwili paniki wyświetli stos
wywołań, co ułatwia odnalezienie jej źródła.

> ### Zwijanie stosu lub przerwanie programu w odpowiedzi na panikę {#unwinding-the-stack-or-aborting-in-response-to-a-panic}
>
> Domyślnie, gdy wystąpi panika, program zaczyna _zwijanie stosu_
> (*unwinding*), czyli Rust cofa się w górę stosu i czyści dane każdej
> napotkanej funkcji. Takie cofanie się i sprzątanie to jednak sporo pracy.
> Dlatego Rust pozwala wybrać alternatywę w postaci natychmiastowego _przerwania_
> (*aborting*), które kończy program bez sprzątania.
>
> Pamięć, której używał program, musi wtedy zostać zwolniona przez system
> operacyjny. Jeśli w projekcie zależy ci na tym, żeby wynikowy plik binarny był
> jak najmniejszy, możesz przy panice przełączyć się ze zwijania stosu na
> przerwanie, dodając `panic = 'abort'` do odpowiednich sekcji `[profile]` w
> pliku _Cargo.toml_. Jeśli na przykład chcesz przerywać program przy panice w
> trybie wydania, dodaj to:
>
> ```toml
> [profile.release]
> panic = 'abort'
> ```

Spróbujmy wywołać `panic!` w prostym programie:

<Listing file-name="src/main.rs">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-01-panic/src/main.rs}}
```

</Listing>

Po uruchomieniu programu zobaczysz coś takiego:

```console
{{#include ../listings/ch09-error-handling/no-listing-01-panic/output.txt}}
```

Komunikat o błędzie w dwóch ostatnich liniach pochodzi z wywołania `panic!`.
Pierwsza linia zawiera nasz komunikat paniki i miejsce w kodzie źródłowym, w
którym wystąpiła panika: _src/main.rs:2:5_ oznacza drugi wiersz, piąty znak
naszego pliku _src/main.rs_.

W tym przypadku wskazany wiersz należy do naszego kodu i jeśli do niego
zajrzymy, zobaczymy wywołanie makra `panic!`. W innych przypadkach wywołanie
`panic!` może się znajdować w kodzie wywoływanym przez nasz kod, a nazwa pliku i
numer wiersza w komunikacie o błędzie będą wskazywać cudzy kod, w którym
wywołano makro `panic!`, a nie wiersz naszego kodu, który ostatecznie
doprowadził do wywołania `panic!`.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-a-panic-backtrace"></a>

Aby ustalić, który fragment naszego kodu powoduje problem, możemy skorzystać ze
śladu stosu (*backtrace*) funkcji, z których pochodzi wywołanie `panic!`. Żeby
zrozumieć, jak korzystać ze śladu stosu `panic!`, przyjrzyjmy się kolejnemu
przykładowi i zobaczmy, jak to wygląda, gdy wywołanie `panic!` pochodzi z
biblioteki z powodu błędu w naszym kodzie, a nie z bezpośredniego wywołania
makra przez nasz kod. Listing 9-1 zawiera kod, który próbuje odczytać element
wektora o indeksie spoza zakresu poprawnych indeksów.

<Listing number="9-1" file-name="src/main.rs" caption="Próba dostępu do elementu za końcem wektora, która spowoduje wywołanie `panic!`">

```rust,should_panic,panics
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-01/src/main.rs}}
```

</Listing>

Próbujemy tu odczytać setny element wektora (o indeksie 99, bo indeksowanie
zaczyna się od zera), ale wektor ma tylko trzy elementy. W takiej sytuacji Rust
spanikuje. Użycie `[]` ma zwrócić element, ale jeśli podasz nieprawidłowy
indeks, Rust nie ma żadnego elementu, który mógłby tu poprawnie zwrócić.

W języku C próba odczytu poza końcem struktury danych jest niezdefiniowanym
zachowaniem (*undefined behavior*). Możesz dostać to, co akurat leży w pamięci w
miejscu, które odpowiadałoby temu elementowi struktury, mimo że ta pamięć do
niej nie należy. Nazywa się to odczytem poza buforem (*buffer overread*) i może
prowadzić do podatności bezpieczeństwa, jeśli atakujący zdoła tak manipulować
indeksem, żeby odczytać dane przechowywane za strukturą, do których nie
powinien mieć dostępu.

Aby chronić program przed tego rodzaju podatnością, przy próbie odczytu elementu o
nieistniejącym indeksie Rust zatrzyma wykonanie i odmówi kontynuowania.
Spróbujmy i zobaczmy:

```console
{{#include ../listings/ch09-error-handling/listing-09-01/output.txt}}
```

Ten błąd wskazuje wiersz 4 pliku _main.rs_, w którym próbujemy odczytać indeks
99 wektora w `v`.

Linia `note:` mówi nam, że możemy ustawić zmienną środowiskową `RUST_BACKTRACE`,
aby uzyskać ślad stosu pokazujący dokładnie, co doprowadziło do błędu. _Ślad
stosu_ to lista wszystkich funkcji wywołanych po drodze do tego miejsca. Ślady
stosu działają w Ruście tak samo jak w innych językach: kluczem do ich
odczytania jest czytanie od góry, aż natrafisz na pliki z własnego kodu.
To miejsce, w którym zaczął się problem. Linie powyżej to kod wywoływany przez
twój kod, a linie poniżej to kod, który wywołał twój kod. Mogą się wśród nich
znaleźć kod samego Rusta, kod biblioteki standardowej albo używane przez ciebie
crate’y. Spróbujmy uzyskać ślad stosu, ustawiając zmienną środowiskową
`RUST_BACKTRACE` na dowolną wartość oprócz `0`. Listing 9-2 pokazuje wynik
podobny do tego, który zobaczysz.

<!-- manual-regeneration
cd listings/ch09-error-handling/listing-09-01
RUST_BACKTRACE=1 cargo run
copy the backtrace output below
check the backtrace number mentioned in the text below the listing
-->

<Listing number="9-2" caption="Ślad stosu wygenerowany przez wywołanie `panic!`, wyświetlany po ustawieniu zmiennej środowiskowej `RUST_BACKTRACE`">

```console
$ RUST_BACKTRACE=1 cargo run
thread 'main' panicked at src/main.rs:4:6:
index out of bounds: the len is 3 but the index is 99
stack backtrace:
   0: rust_begin_unwind
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/std/src/panicking.rs:692:5
   1: core::panicking::panic_fmt
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:75:14
   2: core::panicking::panic_bounds_check
             at /rustc/4d91de4e48198da2e33413efdcd9cd2cc0c46688/library/core/src/panicking.rs:273:5
   3: <usize as core::slice::index::SliceIndex<[T]>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:274:10
   4: core::slice::index::<impl core::ops::index::Index<I> for [T]>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/slice/index.rs:16:9
   5: <alloc::vec::Vec<T,A> as core::ops::index::Index<I>>::index
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/alloc/src/vec/mod.rs:3361:9
   6: panic::main
             at ./src/main.rs:4:6
   7: core::ops::function::FnOnce::call_once
             at file:///home/.rustup/toolchains/1.85/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```

</Listing>

Sporo tego! Dokładny wynik może się u ciebie różnić w zależności od systemu
operacyjnego i wersji Rusta. Aby uzyskać ślady stosu z tymi informacjami,
muszą być włączone symbole debugowania. Są one włączone domyślnie, gdy używasz
`cargo build` lub `cargo run` bez flagi `--release`, tak jak tutaj.

W wyniku z listingu 9-2 linia 6 śladu stosu wskazuje wiersz naszego projektu,
który powoduje problem: wiersz 4 pliku _src/main.rs_. Jeśli nie chcemy, żeby
program panikował, powinniśmy zacząć dochodzenie od miejsca wskazanego przez
pierwszą linię wspominającą plik, który sami napisaliśmy. W listingu 9-1, w
którym celowo napisaliśmy kod powodujący panikę, sposobem na usunięcie paniki
jest niesięganie po element spoza zakresu indeksów wektora. Gdy w przyszłości
twój kod spanikuje, musisz ustalić, jakie działanie na jakich wartościach
wykonuje kod, że dochodzi do paniki, i co kod powinien robić zamiast tego.

Do `panic!` oraz do tego, kiedy należy, a kiedy nie należy używać `panic!` do
obsługi błędów, wrócimy w podrozdziale [„`panic!` czy nie
`panic!`?”][to-panic-or-not-to-panic]<!-- ignore --> w dalszej części tego
rozdziału. Teraz przyjrzymy się, jak obsłużyć błąd odwracalny za pomocą
`Result`.

{{#quiz ../quizzes/ch09-01-panic.toml}}

[to-panic-or-not-to-panic]: ch09-03-to-panic-or-not-to-panic.html#to-panic-or-not-to-panic

## Rozdzielanie modułów na osobne pliki {#separating-modules-into-different-files}

Dotąd wszystkie przykłady w tym rozdziale definiowały wiele modułów w jednym
pliku. Gdy moduły się rozrastają, możesz chcieć przenieść ich definicje do
osobnego pliku, aby łatwiej było poruszać się po kodzie.

Zacznijmy na przykład od kodu z listingu 7-17, który zawierał kilka modułów
restauracji. Wydzielimy moduły do plików, zamiast trzymać je wszystkie w pliku
korzenia *crate’a* (jednostki kompilacji w Ruście). W tym przypadku plikiem
korzenia crate’a (*crate root*) jest _src/lib.rs_, ale ta procedura działa też
w crate’ach binarnych, których plikiem korzenia jest _src/main.rs_.

Najpierw wydzielimy moduł `front_of_house` do osobnego pliku. Usuń kod wewnątrz
nawiasów klamrowych modułu `front_of_house`, zostawiając tylko deklarację
`mod front_of_house;`, tak aby _src/lib.rs_ zawierał kod pokazany w listingu
7-21. Zauważ, że ten kod się nie skompiluje, dopóki nie utworzymy pliku
_src/front_of_house.rs_ z listingu 7-22.

<Listing number="7-21" file-name="src/lib.rs" caption="Deklaracja modułu `front_of_house`, którego ciało znajdzie się w *src/front_of_house.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/lib.rs}}
```

</Listing>

Następnie umieść kod, który był w nawiasach klamrowych, w nowym pliku o nazwie
_src/front_of_house.rs_, jak pokazano w listingu 7-22. Kompilator wie, że ma
szukać w tym pliku, ponieważ natrafił w korzeniu crate’a na deklarację modułu o
nazwie `front_of_house`.

<Listing number="7-22" file-name="src/front_of_house.rs" caption="Definicje wewnątrz modułu `front_of_house` w *src/front_of_house.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-21-and-22/src/front_of_house.rs}}
```

</Listing>

Zauważ, że plik wystarczy wczytać za pomocą deklaracji `mod` _tylko raz_ w
całym drzewie modułów. Gdy kompilator już wie, że plik jest częścią projektu (i
wie, w którym miejscu drzewa modułów znajduje się kod, dzięki temu, gdzie
umieszczono instrukcję `mod`), inne pliki w projekcie powinny odwoływać się do
kodu wczytanego pliku przez ścieżkę do miejsca, w którym został zadeklarowany,
jak opisano w podrozdziale
[„Ścieżki do elementów w drzewie modułów”][paths]<!-- ignore -->. Innymi
słowy, `mod` _nie_ jest operacją dołączania pliku („include”), którą możesz
znać z innych języków programowania.

Teraz wydzielimy do osobnego pliku moduł `hosting`. Ten proces wygląda nieco
inaczej, ponieważ `hosting` jest dzieckiem modułu `front_of_house`, a nie
modułu głównego. Plik modułu `hosting` umieścimy w nowym katalogu, którego
nazwa będzie odpowiadać jego przodkom w drzewie modułów – w tym przypadku
_src/front_of_house_.

Aby zacząć przenoszenie modułu `hosting`, zmieniamy _src/front_of_house.rs_
tak, by zawierał tylko deklarację modułu `hosting`:

<Listing file-name="src/front_of_house.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house.rs}}
```

</Listing>

Następnie tworzymy katalog _src/front_of_house_ i plik _hosting.rs_, który
będzie zawierał definicje z modułu `hosting`:

<Listing file-name="src/front_of_house/hosting.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/no-listing-02-extracting-hosting/src/front_of_house/hosting.rs}}
```

</Listing>

Gdybyśmy zamiast tego umieścili _hosting.rs_ w katalogu _src_, kompilator
oczekiwałby, że kod z _hosting.rs_ należy do modułu `hosting` zadeklarowanego
w korzeniu crate’a, a nie zadeklarowanego jako dziecko modułu
`front_of_house`. Dzięki regułom kompilatora określającym, w których plikach
szukać kodu poszczególnych modułów, struktura katalogów i plików ściślej
odpowiada drzewu modułów.

> ### Alternatywne ścieżki plików {#alternate-file-paths}
>
> Dotąd omówiliśmy najbardziej idiomatyczne ścieżki plików, których używa
> kompilator Rusta, ale Rust obsługuje też starszy styl ścieżek. Dla modułu o
> nazwie `front_of_house` zadeklarowanego w korzeniu crate’a kompilator będzie
> szukał kodu modułu w plikach:
>
> - _src/front_of_house.rs_ (styl, który omówiliśmy);
> - _src/front_of_house/mod.rs_ (starszy styl, wciąż obsługiwana ścieżka).
>
> Dla modułu o nazwie `hosting`, który jest podmodułem `front_of_house`,
> kompilator będzie szukał kodu modułu w plikach:
>
> - _src/front_of_house/hosting.rs_ (styl, który omówiliśmy);
> - _src/front_of_house/hosting/mod.rs_ (starszy styl, wciąż obsługiwana
>   ścieżka).
>
> Jeśli użyjesz obu stylów dla tego samego modułu, dostaniesz błąd kompilatora.
> Mieszanie obu stylów dla różnych modułów w tym samym projekcie jest
> dozwolone, ale może dezorientować osoby poruszające się po twoim projekcie.
>
> Główną wadą stylu z plikami o nazwie _mod.rs_ jest to, że w projekcie może
> się znaleźć wiele plików o nazwie _mod.rs_, co bywa mylące, gdy masz je
> jednocześnie otwarte w edytorze.

Przenieśliśmy kod każdego modułu do osobnego pliku, a drzewo modułów pozostało
takie samo. Wywołania funkcji w `eat_at_restaurant` zadziałają bez żadnych
zmian, mimo że definicje znajdują się w różnych plikach. Ta technika pozwala
przenosić moduły do nowych plików, gdy się rozrastają.

Zauważ, że instrukcja `pub use crate::front_of_house::hosting` w _src/lib.rs_
również się nie zmieniła, a `use` nie ma żadnego wpływu na to, które pliki są
kompilowane jako część crate’a. Słowo kluczowe `mod` deklaruje moduły, a Rust
szuka kodu należącego do danego modułu w pliku o takiej samej nazwie jak ten
moduł.

{{#quiz ../quizzes/ch07-05-files.toml}}

## Podsumowanie {#summary}

Rust pozwala podzielić pakiet (*package*) na wiele crate’ów, a crate na moduły,
dzięki czemu możesz odwoływać się do elementów zdefiniowanych w jednym module z
innego modułu. Robisz to, podając ścieżki bezwzględne lub względne. Ścieżki te
możesz wprowadzić do zasięgu instrukcją `use`, aby przy wielokrotnym użyciu
elementu w tym zasięgu korzystać z krótszej ścieżki. Kod modułu jest domyślnie
prywatny, ale definicje możesz upublicznić, dodając słowo kluczowe `pub`.

W następnym rozdziale przyjrzymy się kilku strukturom danych z biblioteki
standardowej – kolekcjom – których możesz używać w swoim starannie
uporządkowanym kodzie.

[paths]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html

## Odczytywanie pliku {#reading-a-file}

Teraz dodamy funkcjonalność odczytu pliku wskazanego w argumencie `file_path`.
Najpierw potrzebujemy przykładowego pliku do testów: użyjemy pliku z niewielką
ilością tekstu w kilku wierszach i z kilkoma powtarzającymi się słowami. W
listingu 12-3 znajduje się utwór Emily Dickinson, który świetnie się do tego
nada! Utwórz plik o nazwie _poem.txt_ w katalogu głównym projektu i wpisz do
niego utwór „I’m Nobody! Who are you?”.

<Listing number="12-3" file-name="poem.txt" caption="Utwór Emily Dickinson jest dobrym przypadkiem testowym.">

```text
{{#include ../listings/ch12-an-io-project/listing-12-03/poem.txt}}
```

</Listing>

Gdy tekst jest już na miejscu, otwórz do edycji _src/main.rs_ i dodaj kod
odczytujący plik, tak jak w listingu 12-4.

<Listing number="12-4" file-name="src/main.rs" caption="Odczytywanie zawartości pliku wskazanego przez drugi argument">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/src/main.rs:here}}
```

</Listing>

Najpierw za pomocą instrukcji (*statement*) `use` wprowadzamy potrzebną część
biblioteki standardowej: do obsługi plików potrzebujemy `std::fs`.

W `main` nowa instrukcja `fs::read_to_string` przyjmuje `file_path`, otwiera
ten plik i zwraca wartość typu `std::io::Result<String>` z zawartością pliku.

Następnie znów dodajemy tymczasową instrukcję `println!`, która po odczytaniu
pliku wypisuje wartość `contents`, żeby sprawdzić, czy program jak dotąd
działa.

Uruchommy ten kod z dowolnym łańcuchem znaków (*string*) jako pierwszym
argumentem wiersza poleceń (ponieważ nie zaimplementowaliśmy jeszcze
wyszukiwania) i plikiem _poem.txt_ jako drugim argumentem:

```console
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-04/output.txt}}
```

Świetnie! Kod odczytał, a następnie wypisał zawartość pliku. Ma jednak kilka
wad. Funkcja `main` ma obecnie wiele zadań, a funkcje są zwykle czytelniejsze i
łatwiejsze w utrzymaniu, gdy każda z nich odpowiada tylko za jedną rzecz.
Drugi problem polega na tym, że nie obsługujemy błędów tak dobrze, jak
moglibyśmy. Program jest wciąż mały, więc te wady nie stanowią dużego problemu,
ale w miarę jego rozrastania się coraz trudniej będzie je elegancko naprawić.
Dobrą praktyką jest rozpoczęcie refaktoryzacji na wczesnym etapie tworzenia
programu, ponieważ znacznie łatwiej refaktoryzować mniejsze fragmenty kodu. Tym
zajmiemy się w następnej kolejności.

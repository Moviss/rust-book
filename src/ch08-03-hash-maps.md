## Przechowywanie kluczy z powiązanymi wartościami w mapach haszujących {#storing-keys-with-associated-values-in-hash-maps}

Ostatnią z naszych popularnych kolekcji jest mapa haszująca (*hash map*). Typ
`HashMap<K, V>` przechowuje odwzorowanie kluczy typu `K` na wartości typu `V`
za pomocą *funkcji haszującej* (*hashing function*), która decyduje, jak te
klucze i wartości zostaną umieszczone w pamięci. Wiele języków programowania
obsługuje taką strukturę danych, ale często pod inną nazwą, np. *hash*, *map*,
*object*, *hash table*, *dictionary* czy *associative array* – by wymienić
tylko kilka.

Mapy haszujące przydają się, gdy chcesz wyszukiwać dane nie za pomocą indeksu,
jak w wektorach (*vectors*), ale za pomocą klucza, który może być dowolnego
typu. Na przykład w grze możesz śledzić wynik każdej drużyny w mapie haszującej,
w której kluczem jest nazwa drużyny, a wartością jej wynik. Znając nazwę
drużyny, możesz odczytać jej wynik.

W tym podrozdziale omówimy podstawowe API map haszujących, ale w funkcjach
zdefiniowanych przez bibliotekę standardową dla `HashMap<K, V>` kryje się
znacznie więcej przydatnych rzeczy. Jak zawsze, więcej informacji znajdziesz w
dokumentacji biblioteki standardowej.

### Tworzenie nowej mapy haszującej {#creating-a-new-hash-map}

Jednym ze sposobów utworzenia pustej mapy haszującej jest użycie `new` i
dodawanie elementów za pomocą `insert`. W listingu 8-20 śledzimy wyniki dwóch
drużyn o nazwach *Blue* i *Yellow*. Drużyna Blue zaczyna z 10 punktami, a
drużyna Yellow z 50.

<Listing number="8-20" caption="Tworzenie nowej mapy haszującej i wstawianie do niej kluczy i wartości">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-20/src/main.rs:here}}
```

</Listing>

Zwróć uwagę, że najpierw musimy zaimportować za pomocą `use` typ `HashMap` z
części biblioteki standardowej poświęconej kolekcjom. Spośród naszych trzech
popularnych kolekcji ta jest używana najrzadziej, więc nie należy do elementów
automatycznie wprowadzanych do zasięgu (*scope*) przez *prelude* (zestaw
elementów importowanych automatycznie). Mapy haszujące mają też słabsze
wsparcie w bibliotece standardowej – nie ma na przykład wbudowanego makra do
ich tworzenia.

Podobnie jak wektory, mapy haszujące przechowują dane na stercie (*heap*). Ta
`HashMap` ma klucze typu `String` i wartości typu `i32`. Tak jak wektory, mapy
haszujące są jednorodne: wszystkie klucze muszą mieć ten sam typ i wszystkie
wartości muszą mieć ten sam typ.

### Dostęp do wartości w mapie haszującej {#accessing-values-in-a-hash-map}

Wartość z mapy haszującej możemy pobrać, przekazując jej klucz do metody `get`,
jak pokazano w listingu 8-21.

<Listing number="8-21" caption="Dostęp do wyniku drużyny Blue przechowywanego w mapie haszującej">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-21/src/main.rs:here}}
```

</Listing>

Tutaj `score` będzie miało wartość powiązaną z drużyną Blue, czyli `10`. Metoda
`get` zwraca `Option<&V>`; jeśli w mapie haszującej nie ma wartości dla danego
klucza, `get` zwróci `None`. Ten program obsługuje `Option`, wywołując
`copied`, aby otrzymać `Option<i32>` zamiast `Option<&i32>`, a następnie
`unwrap_or`, aby ustawić `score` na zero, jeśli w `scores` nie ma wpisu dla
tego klucza.

Po każdej parze klucz–wartość w mapie haszującej możemy iterować podobnie jak
po wektorach, używając pętli `for`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-03-iterate-over-hashmap/src/main.rs:here}}
```

Ten kod wypisze każdą parę w dowolnej kolejności:

```text
Yellow: 50
Blue: 10
```

<!-- Old headings. Do not remove or links may break. -->

<a id="hash-maps-and-ownership"></a>

### Zarządzanie własnością w mapach haszujących {#managing-ownership-in-hash-maps}

W przypadku typów implementujących *trait* (cecha typu, zbliżona do
interfejsu) `Copy`, takich jak `i32`, wartości są kopiowane do mapy
haszującej. Wartości będące właścicielami swoich danych, takie jak `String`,
zostaną przeniesione (*moved*), a mapa haszująca stanie się ich właścicielem,
co pokazuje listing 8-22.

<Listing number="8-22" caption="Pokazanie, że po wstawieniu klucze i wartości należą do mapy haszującej">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-22/src/main.rs:here}}
```

</Listing>

Nie możemy używać zmiennych `field_name` i `field_value` po tym, jak zostały
przeniesione do mapy haszującej wywołaniem `insert`.

Jeśli wstawimy do mapy haszującej referencje (*references*) do wartości, same
wartości nie zostaną do niej przeniesione. Wartości, na które wskazują
referencje, muszą być prawidłowe co najmniej tak długo, jak prawidłowa jest
mapa haszująca. Więcej o tych zagadnieniach powiemy w podrozdziale
[„Sprawdzanie poprawności referencji za pomocą czasów życia”][validating-references-with-lifetimes]<!-- ignore -->
w rozdziale 10.

### Aktualizowanie mapy haszującej {#updating-a-hash-map}

Choć liczba par kluczy i wartości może rosnąć, z każdym unikalnym kluczem może
być w danej chwili powiązana tylko jedna wartość (ale nie odwrotnie: na przykład
zarówno drużyna Blue, jak i drużyna Yellow mogłyby mieć wartość `10` zapisaną w
mapie haszującej `scores`).

Gdy chcesz zmienić dane w mapie haszującej, musisz zdecydować, jak obsłużyć
sytuację, w której klucz ma już przypisaną wartość. Możesz zastąpić starą
wartość nową, całkowicie ignorując starą. Możesz zachować starą wartość i
zignorować nową, dodając nową wartość tylko wtedy, gdy klucz *nie ma* jeszcze
wartości. Możesz też połączyć starą i nową wartość. Zobaczmy, jak zrobić każdą
z tych rzeczy!

#### Nadpisywanie wartości {#overwriting-a-value}

Jeśli wstawimy do mapy haszującej klucz i wartość, a potem wstawimy ten sam
klucz z inną wartością, wartość powiązana z tym kluczem zostanie zastąpiona.
Choć kod w listingu 8-23 wywołuje `insert` dwukrotnie, mapa haszująca będzie
zawierać tylko jedną parę klucz–wartość, ponieważ za każdym razem wstawiamy
wartość dla klucza drużyny Blue.

<Listing number="8-23" caption="Zastępowanie wartości zapisanej pod określonym kluczem">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-23/src/main.rs:here}}
```

</Listing>

Ten kod wypisze `{"Blue": 25}`. Pierwotna wartość `10` została nadpisana.

<!-- Old headings. Do not remove or links may break. -->

<a id="only-inserting-a-value-if-the-key-has-no-value"></a>

#### Dodawanie klucza i wartości tylko wtedy, gdy klucza nie ma {#adding-a-key-and-value-only-if-a-key-isnt-present}

Często sprawdza się, czy dany klucz już istnieje w mapie haszującej z jakąś
wartością, a następnie wykonuje się następujące działania: jeśli klucz istnieje
w mapie haszującej, dotychczasowa wartość powinna pozostać bez zmian; jeśli
klucza nie ma, należy go wstawić razem z wartością.

Mapy haszujące mają do tego specjalne API o nazwie `entry`, które przyjmuje jako
parametr klucz, który chcesz sprawdzić. Wartością zwracaną przez metodę `entry`
jest *enum* (typ wyliczeniowy) o nazwie `Entry`, reprezentujący wartość, która
może istnieć albo nie. Załóżmy, że chcemy sprawdzić, czy klucz drużyny Yellow
ma powiązaną wartość. Jeśli nie ma, chcemy wstawić wartość `50`; to samo dla
drużyny Blue. Z użyciem API `entry` kod wygląda jak w listingu 8-24.

<Listing number="8-24" caption="Użycie metody `entry`, aby wstawić wartość tylko wtedy, gdy klucz jeszcze jej nie ma">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-24/src/main.rs:here}}
```

</Listing>

Metoda `or_insert` typu `Entry` jest zdefiniowana tak, że zwraca mutowalną
(*mutable*) referencję do wartości dla danego klucza `Entry`, jeśli ten klucz
istnieje; jeśli nie, wstawia parametr jako nową wartość dla tego klucza i
zwraca mutowalną referencję do nowej wartości. Ta technika jest znacznie
czystsza niż samodzielne pisanie tej logiki, a do tego lepiej współpracuje z
*borrow checkerem* (mechanizmem sprawdzania pożyczeń).

Uruchomienie kodu z listingu 8-24 wypisze `{"Yellow": 50, "Blue": 10}`.
Pierwsze wywołanie `entry` wstawi klucz drużyny Yellow z wartością `50`,
ponieważ drużyna Yellow nie ma jeszcze wartości. Drugie wywołanie `entry` nie
zmieni mapy haszującej, ponieważ drużyna Blue ma już wartość `10`.

#### Aktualizowanie wartości na podstawie starej wartości {#updating-a-value-based-on-the-old-value}

Innym częstym zastosowaniem map haszujących jest wyszukanie wartości klucza i
zaktualizowanie jej na podstawie starej wartości. Na przykład listing 8-25
pokazuje kod, który liczy, ile razy każde słowo występuje w pewnym tekście.
Używamy mapy haszującej, w której kluczami są słowa, i zwiększamy wartość, aby
śledzić, ile razy widzieliśmy dane słowo. Jeśli widzimy słowo po raz pierwszy,
najpierw wstawimy wartość `0`.

<Listing number="8-25" caption="Liczenie wystąpień słów za pomocą mapy haszującej przechowującej słowa i liczniki">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-25/src/main.rs:here}}
```

</Listing>

Ten kod wypisze `{"world": 2, "hello": 1, "wonderful": 1}`. Te same pary
klucz–wartość mogą zostać wypisane w innej kolejności: jak pamiętasz z
podrozdziału [„Dostęp do wartości w mapie haszującej”][access]<!-- ignore -->,
iterowanie po mapie haszującej odbywa się w dowolnej kolejności.

Metoda `split_whitespace` zwraca iterator po podwycinkach wartości `text`
rozdzielonych białymi znakami. Metoda `or_insert` zwraca mutowalną referencję
(`&mut V`) do wartości dla podanego klucza. Tutaj zapisujemy tę mutowalną
referencję w zmiennej `count`, więc aby przypisać coś do tej wartości, musimy
najpierw wykonać dereferencję (*dereference*) `count` za pomocą gwiazdki (`*`).
Mutowalna referencja wychodzi z zasięgu na końcu pętli `for`, więc wszystkie te
zmiany są bezpieczne i dozwolone przez zasady pożyczania (*borrowing*).

### Funkcje haszujące {#hashing-functions}

Domyślnie `HashMap` używa funkcji haszującej o nazwie *SipHash*, która może
zapewnić odporność na ataki typu *denial-of-service* (DoS) wymierzone w tablice
haszujące[^siphash]<!-- ignore -->. Nie jest to najszybszy dostępny algorytm haszujący,
ale lepsze bezpieczeństwo jest warte spadku wydajności. Jeśli sprofilujesz swój
kod i okaże się, że domyślna funkcja haszująca jest dla twoich potrzeb zbyt
wolna, możesz przełączyć się na inną funkcję, określając inny *hasher*. *Hasher*
to typ implementujący trait `BuildHasher`. O traitach i sposobach ich
implementowania powiemy w [rozdziale 10][traits]<!-- ignore -->. Nie musisz koniecznie
implementować własnego hashera od zera; na
[crates.io](https://crates.io/)<!-- ignore --> są biblioteki udostępnione przez innych
użytkowników Rusta, które dostarczają hashery implementujące wiele popularnych
algorytmów haszujących.

[^siphash]: [https://en.wikipedia.org/wiki/SipHash](https://en.wikipedia.org/wiki/SipHash)

{{#quiz ../quizzes/ch08-03-hashmap.toml}}

## Podsumowanie {#summary}

Wektory, łańcuchy znaków (*strings*) i mapy haszujące zapewnią dużą część
funkcjonalności potrzebnej w programach, które muszą przechowywać dane,
uzyskiwać do nich dostęp i je modyfikować. Oto kilka ćwiczeń, które powinno
udać ci się teraz rozwiązać:

1. Mając listę liczb całkowitych, użyj wektora i zwróć medianę (wartość na
   środkowej pozycji po posortowaniu) oraz dominantę (wartość występującą
   najczęściej; przyda się tu mapa haszująca) tej listy.
1. Przekształć łańcuchy na świńską łacinę (*Pig Latin*). Pierwsza spółgłoska
   każdego słowa jest przenoszona na koniec słowa, po czym dodaje się *ay*,
   więc *first* staje się *irst-fay*. Do słów zaczynających się od samogłoski
   dodaje się na końcu *hay* (*apple* staje się *apple-hay*). Pamiętaj o
   szczegółach kodowania UTF-8!
1. Za pomocą mapy haszującej i wektorów utwórz interfejs tekstowy, który
   pozwoli użytkownikowi dodawać imiona pracowników do działów firmy, np.
   „Dodaj Sally do Inżynierii” albo „Dodaj Amira do Sprzedaży”. Następnie
   pozwól użytkownikowi pobrać alfabetycznie posortowaną listę wszystkich osób
   w dziale albo wszystkich osób w firmie według działów.

Dokumentacja API biblioteki standardowej opisuje metody wektorów, łańcuchów i
map haszujących, które przydadzą się w tych ćwiczeniach!

Przechodzimy do bardziej złożonych programów, w których operacje mogą się nie
powieść, więc to doskonały moment, by omówić obsługę błędów. Zrobimy to w
następnym rozdziale!

[validating-references-with-lifetimes]: ch10-03-lifetime-syntax.html#validating-references-with-lifetimes
[access]: #accessing-values-in-a-hash-map
[traits]: ch10-02-traits.html

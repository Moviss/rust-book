<!-- Old headings. Do not remove or links may break. -->

<a id="defining-modules-to-control-scope-and-privacy"></a>

## Kontrolowanie zasięgu i prywatności za pomocą modułów {#control-scope-and-privacy-with-modules}

W tym podrozdziale omówimy moduły i inne części systemu modułów, a mianowicie
_ścieżki_ (*paths*), które pozwalają nazywać elementy; słowo kluczowe
(*keyword*) `use`, które wprowadza ścieżkę do zasięgu (*scope*); oraz słowo
kluczowe `pub`, które czyni elementy publicznymi. Omówimy też słowo kluczowe
`as`, pakiety (*packages*) zewnętrzne i operator glob (*glob operator*).

### Ściąga z modułów {#modules-cheat-sheet}

Zanim przejdziemy do szczegółów modułów i ścieżek, podajemy tu krótkie
zestawienie tego, jak moduły, ścieżki, słowo kluczowe `use` i słowo kluczowe
`pub` działają w kompilatorze oraz jak większość programistów organizuje swój
kod. W dalszej części rozdziału omówimy przykłady każdej z tych reguł, ale to
dobre miejsce, do którego można wrócić, by przypomnieć sobie, jak działają
moduły.

- **Zacznij od korzenia crate’a**: podczas kompilowania *crate’a* (jednostki
  kompilacji w Ruście) kompilator najpierw szuka kodu do skompilowania w pliku
  korzenia crate’a (*crate root*) – zwykle _src/lib.rs_ dla crate’a
  bibliotecznego i _src/main.rs_ dla crate’a binarnego.
- **Deklarowanie modułów**: w pliku korzenia crate’a możesz deklarować nowe
  moduły; powiedzmy, że deklarujesz moduł „garden” za pomocą `mod garden;`.
  Kompilator będzie szukał kodu modułu w tych miejscach:
  - w miejscu deklaracji, w nawiasach klamrowych zastępujących średnik po
    `mod garden`;
  - w pliku _src/garden.rs_;
  - w pliku _src/garden/mod.rs_.
- **Deklarowanie podmodułów**: w każdym pliku innym niż korzeń crate’a możesz
  deklarować podmoduły. Na przykład możesz zadeklarować `mod vegetables;` w
  _src/garden.rs_. Kompilator będzie szukał kodu podmodułu w katalogu nazwanym
  tak jak moduł nadrzędny, w tych miejscach:
  - w miejscu deklaracji, bezpośrednio po `mod vegetables`, w nawiasach
    klamrowych zamiast średnika;
  - w pliku _src/garden/vegetables.rs_;
  - w pliku _src/garden/vegetables/mod.rs_.
- **Ścieżki do kodu w modułach**: gdy moduł jest już częścią twojego crate’a,
  możesz odwoływać się do kodu w tym module z dowolnego innego miejsca tego
  samego crate’a, o ile pozwalają na to reguły prywatności, używając ścieżki do
  kodu. Na przykład typ `Asparagus` w module warzyw z ogrodu znajdziesz pod
  ścieżką `crate::garden::vegetables::Asparagus`.
- **Prywatne a publiczne**: kod w module jest domyślnie prywatny dla modułów
  nadrzędnych. Aby uczynić moduł publicznym, zadeklaruj go za pomocą `pub mod`
  zamiast `mod`. Aby uczynić publicznymi także elementy w publicznym module,
  umieść `pub` przed ich deklaracjami.
- **Słowo kluczowe `use`**: w obrębie zasięgu słowo kluczowe `use` tworzy
  skróty do elementów, aby ograniczyć powtarzanie długich ścieżek. W każdym
  zasięgu, który może odwoływać się do `crate::garden::vegetables::Asparagus`,
  możesz utworzyć skrót za pomocą `use crate::garden::vegetables::Asparagus;`,
  a od tej pory wystarczy pisać `Asparagus`, by używać tego typu w tym zasięgu.

Utworzymy teraz crate binarny o nazwie `backyard`, który ilustruje te reguły.
Katalog crate’a, również nazwany _backyard_, zawiera następujące pliki i
katalogi:

```text
backyard
├── Cargo.lock
├── Cargo.toml
└── src
    ├── garden
    │   └── vegetables.rs
    ├── garden.rs
    └── main.rs
```

Plikiem korzenia crate’a jest tu _src/main.rs_, a jego zawartość wygląda tak:

<Listing file-name="src/main.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/main.rs}}
```

</Listing>

Wiersz `pub mod garden;` każe kompilatorowi dołączyć kod, który znajdzie w
_src/garden.rs_, czyli:

<Listing file-name="src/garden.rs">

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden.rs}}
```

</Listing>

Z kolei `pub mod vegetables;` oznacza, że dołączany jest także kod z
_src/garden/vegetables.rs_. Ten kod to:

```rust,noplayground,ignore
{{#rustdoc_include ../listings/ch07-managing-growing-projects/quick-reference-example/src/garden/vegetables.rs}}
```

Przejdźmy teraz do szczegółów tych reguł i pokażmy je w działaniu!

### Grupowanie powiązanego kodu w modułach {#grouping-related-code-in-modules}

_Moduły_ pozwalają nam organizować kod w obrębie crate’a tak, by był czytelny i
łatwy do ponownego użycia. Moduły pozwalają też kontrolować _prywatność_
(*privacy*) elementów, ponieważ kod w module jest domyślnie prywatny. Elementy
prywatne to wewnętrzne szczegóły implementacji, niedostępne do użytku z
zewnątrz. Możemy uczynić moduły i elementy w nich publicznymi, co udostępnia je
kodowi zewnętrznemu, by mógł ich używać i od nich zależeć.

Jako przykład napiszmy crate biblioteczny, który zapewnia funkcjonalność
restauracji. Zdefiniujemy sygnatury funkcji, ale ich ciała zostawimy puste, aby
skupić się na organizacji kodu, a nie na implementacji restauracji.

W branży restauracyjnej jedną część lokalu nazywa się salą, a drugą –
zapleczem. _Sala_ (*front of house*) to miejsce, w którym przebywają
klienci; obejmuje to miejsce, gdzie obsługa sadza gości, kelnerzy przyjmują
zamówienia i płatności, a barmani przygotowują napoje. _Zaplecze_ (*back of
house*) to miejsce, gdzie szefowie kuchni i kucharze pracują w kuchni,
zmywacze sprzątają, a kierownicy zajmują się pracą administracyjną.

Aby nadać naszemu crate’owi taką strukturę, możemy zorganizować jego funkcje w
zagnieżdżone moduły. Utwórz nową bibliotekę o nazwie `restaurant`, uruchamiając
`cargo new restaurant --lib`. Następnie wpisz kod z listingu 7-1 do
_src/lib.rs_, aby zdefiniować kilka modułów i sygnatur funkcji; ten kod
odpowiada sali.

<Listing number="7-1" file-name="src/lib.rs" caption="Moduł `front_of_house` zawierający inne moduły, które z kolei zawierają funkcje">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-01/src/lib.rs}}
```

</Listing>

Moduł definiujemy za pomocą słowa kluczowego `mod`, po którym następuje nazwa
modułu (tutaj `front_of_house`). Ciało modułu umieszczamy następnie w nawiasach
klamrowych. Wewnątrz modułów możemy umieszczać inne moduły, tak jak tutaj
moduły `hosting` i `serving`. Moduły mogą też zawierać definicje innych
elementów, takich jak struktury, enumy, stałe, traity oraz – jak w listingu 7-1
– funkcje.

Dzięki modułom możemy grupować powiązane definicje i nazywać to, co je łączy.
Programiści korzystający z tego kodu mogą poruszać się po nim według grup,
zamiast czytać wszystkie definicje, co ułatwia znalezienie tych, które są dla
nich istotne. Programiści dodający do tego kodu nową funkcjonalność będą
wiedzieć, gdzie ją umieścić, aby program pozostał uporządkowany.

Wspomnieliśmy wcześniej, że _src/main.rs_ i _src/lib.rs_ nazywa się _korzeniami
crate’a_. Nazwa ta bierze się stąd, że zawartość każdego z tych dwóch plików
tworzy moduł o nazwie `crate` w korzeniu struktury modułów crate’a, zwanej
_drzewem modułów_ (*module tree*).

Listing 7-2 pokazuje drzewo modułów dla struktury z listingu 7-1.

<Listing number="7-2" caption="Drzewo modułów dla kodu z listingu 7-1">

```text
crate
 └── front_of_house
     ├── hosting
     │   ├── add_to_waitlist
     │   └── seat_at_table
     └── serving
         ├── take_order
         ├── serve_order
         └── take_payment
```

</Listing>

To drzewo pokazuje, jak niektóre moduły zagnieżdżają się w innych modułach; na
przykład `hosting` jest zagnieżdżony w `front_of_house`. Drzewo pokazuje też, że
niektóre moduły są _rodzeństwem_ (*siblings*), co oznacza, że są zdefiniowane w
tym samym module; `hosting` i `serving` to rodzeństwo zdefiniowane w
`front_of_house`. Jeśli moduł A jest zawarty w module B, mówimy, że moduł A jest
_dzieckiem_ (*child*) modułu B, a moduł B jest _rodzicem_ (*parent*) modułu A.
Zauważ, że korzeniem całego drzewa modułów jest niejawny moduł o nazwie
`crate`.

Drzewo modułów może przypominać drzewo katalogów systemu plików na twoim
komputerze; to bardzo trafne porównanie! Tak jak katalogów w systemie plików,
modułów używasz do organizowania kodu. I tak jak w przypadku plików w
katalogu, potrzebujemy sposobu na odnajdywanie naszych modułów.

{{#quiz ../quizzes/ch07-02-modules.toml}}
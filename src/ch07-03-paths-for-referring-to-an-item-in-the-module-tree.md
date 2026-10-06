## Ścieżki do elementów w drzewie modułów {#paths-for-referring-to-an-item-in-the-module-tree}

Aby wskazać Rustowi, gdzie w drzewie modułów znajduje się dany element,
używamy ścieżki, tak samo jak podczas poruszania się po systemie plików. Aby
wywołać funkcję, musimy znać jej ścieżkę.

Ścieżka może mieć dwie postaci:

- _Ścieżka bezwzględna_ (*absolute path*) to pełna ścieżka zaczynająca się od
  korzenia crate’a (*crate root*; *crate* to jednostka kompilacji w Ruście); w
  przypadku kodu z zewnętrznego crate’a ścieżka bezwzględna zaczyna się od nazwy
  tego crate’a, a w przypadku kodu z bieżącego crate’a – od słowa `crate`.
- _Ścieżka względna_ (*relative path*) zaczyna się w bieżącym module i używa
  `self`, `super` lub identyfikatora z bieżącego modułu.

Zarówno ścieżka bezwzględna, jak i względna składa się dalej z jednego lub
więcej identyfikatorów oddzielonych podwójnymi dwukropkami (`::`).

Wróćmy do listingu 7-1 i załóżmy, że chcemy wywołać funkcję `add_to_waitlist`.
To tak, jakbyśmy zapytali: jaka jest ścieżka funkcji `add_to_waitlist`?
Listing 7-3 zawiera kod z listingu 7-1, z którego usunęliśmy część modułów i
funkcji.

Pokażemy dwa sposoby wywołania funkcji `add_to_waitlist` z nowej funkcji
`eat_at_restaurant`, zdefiniowanej w korzeniu crate’a. Te ścieżki są poprawne,
ale pozostaje jeszcze inny problem, przez który ten przykład w obecnej postaci
się nie skompiluje. Za chwilę wyjaśnimy dlaczego.

Funkcja `eat_at_restaurant` jest częścią publicznego API naszego crate’a
bibliotecznego, więc oznaczamy ją słowem kluczowym `pub`. Więcej o `pub` powiemy
w podrozdziale
[„Udostępnianie ścieżek za pomocą słowa kluczowego `pub`”][pub]<!-- ignore -->.

<Listing number="7-3" file-name="src/lib.rs" caption="Wywołanie funkcji `add_to_waitlist` za pomocą ścieżki bezwzględnej i względnej">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-03/src/lib.rs}}
```

</Listing>

Za pierwszym razem wywołujemy funkcję `add_to_waitlist` w `eat_at_restaurant`
za pomocą ścieżki bezwzględnej. Funkcja `add_to_waitlist` jest zdefiniowana w
tym samym crate’cie co `eat_at_restaurant`, więc ścieżkę bezwzględną możemy
zacząć od słowa kluczowego `crate`. Następnie wymieniamy kolejne moduły, aż
dotrzemy do `add_to_waitlist`. Wyobraź sobie system plików o takiej samej
strukturze: aby uruchomić program `add_to_waitlist`, podalibyśmy ścieżkę
`/front_of_house/hosting/add_to_waitlist`; zaczynanie od nazwy `crate`, by
wyjść od korzenia crate’a, przypomina użycie `/` w powłoce, by wyjść od
korzenia systemu plików.

Za drugim razem wywołujemy `add_to_waitlist` w `eat_at_restaurant` za pomocą
ścieżki względnej. Ścieżka zaczyna się od `front_of_house`, czyli nazwy modułu
zdefiniowanego na tym samym poziomie drzewa modułów co `eat_at_restaurant`.
Odpowiednikiem w systemie plików byłaby ścieżka
`front_of_house/hosting/add_to_waitlist`. Rozpoczęcie od nazwy modułu oznacza,
że ścieżka jest względna.

Wybór między ścieżką względną a bezwzględną zależy od projektu, a konkretnie od
tego, czy kod definiujący element będziesz raczej przenosić osobno, czy razem z
kodem, który go używa. Gdybyśmy na przykład przenieśli moduł `front_of_house` i
funkcję `eat_at_restaurant` do modułu o nazwie `customer_experience`,
musielibyśmy zaktualizować ścieżkę bezwzględną do `add_to_waitlist`, ale ścieżka
względna nadal byłaby poprawna. Gdybyśmy natomiast przenieśli samą funkcję
`eat_at_restaurant` do modułu o nazwie `dining`, ścieżka bezwzględna w
wywołaniu `add_to_waitlist` pozostałaby taka sama, ale ścieżkę względną
trzeba byłoby zaktualizować. Ogólnie wolimy podawać ścieżki bezwzględne, bo
częściej chcemy przenosić definicje i wywołania elementów niezależnie od
siebie.

Spróbujmy skompilować listing 7-3 i sprawdźmy, dlaczego jeszcze się nie
kompiluje! Otrzymane błędy pokazuje listing 7-4.

<Listing number="7-4" caption="Błędy kompilatora podczas budowania kodu z listingu 7-3">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-03/output.txt}}
```

</Listing>

Komunikaty o błędach mówią, że moduł `hosting` jest prywatny. Innymi słowy,
mamy poprawne ścieżki do modułu `hosting` i funkcji `add_to_waitlist`, ale Rust
nie pozwala ich użyć, bo nie ma dostępu do prywatnych części kodu. W Ruście
wszystkie elementy (funkcje, metody, struktury, enumy, moduły i stałe) są
domyślnie prywatne dla modułów nadrzędnych. Jeśli chcesz uczynić element, np.
funkcję lub strukturę, prywatnym, umieść go w module.

Elementy w module nadrzędnym nie mogą używać prywatnych elementów modułów
podrzędnych, ale elementy w modułach podrzędnych mogą używać elementów swoich
przodków. Wynika to z tego, że moduły podrzędne opakowują i ukrywają szczegóły
swojej implementacji, ale same widzą kontekst, w którym je zdefiniowano.
Trzymając się naszej metafory, wyobraź sobie reguły prywatności jako biuro na
zapleczu restauracji: to, co się tam dzieje, jest niedostępne dla klientów, ale
kierownicy widzą wszystko w prowadzonej przez siebie restauracji i mogą w niej
zrobić wszystko.

Rust zaprojektowano tak, by system modułów działał w ten sposób, a ukrywanie
wewnętrznych szczegółów implementacji było zachowaniem domyślnym. Dzięki temu
wiesz, które części kodu wewnętrznego możesz zmienić, nie psując kodu
zewnętrznego. Rust daje jednak możliwość udostępnienia wewnętrznych części kodu
modułów podrzędnych zewnętrznym modułom będącym ich przodkami: wystarczy słowem
kluczowym `pub` uczynić element publicznym.

### Udostępnianie ścieżek za pomocą słowa kluczowego `pub` {#exposing-paths-with-the-pub-keyword}

Wróćmy do błędu z listingu 7-4, który mówił, że moduł `hosting` jest prywatny.
Chcemy, aby funkcja `eat_at_restaurant` w module nadrzędnym miała dostęp do
funkcji `add_to_waitlist` w module podrzędnym, więc oznaczamy moduł `hosting`
słowem kluczowym `pub`, jak w listingu 7-5.

<Listing number="7-5" file-name="src/lib.rs" caption="Zadeklarowanie modułu `hosting` jako `pub`, by używać go w `eat_at_restaurant`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-05/src/lib.rs:here}}
```

</Listing>

Niestety kod z listingu 7-5 nadal powoduje błędy kompilatora, co pokazuje
listing 7-6.

<Listing number="7-6" caption="Błędy kompilatora podczas budowania kodu z listingu 7-5">

```console
{{#include ../listings/ch07-managing-growing-projects/listing-07-05/output.txt}}
```

</Listing>

Co się stało? Dodanie słowa kluczowego `pub` przed `mod hosting` czyni moduł
publicznym. Po tej zmianie, jeśli mamy dostęp do `front_of_house`, mamy też
dostęp do `hosting`. Jednak _zawartość_ modułu `hosting` jest nadal prywatna;
upublicznienie modułu nie upublicznia jego zawartości. Słowo kluczowe `pub`
przy module pozwala jedynie kodowi w modułach będących jego przodkami
odwoływać się do niego, ale nie daje dostępu do jego wnętrza. Moduły są kontenerami, więc samo
upublicznienie modułu niewiele daje; musimy pójść dalej i upublicznić także
jeden lub więcej elementów wewnątrz modułu.

Błędy z listingu 7-6 mówią, że funkcja `add_to_waitlist` jest prywatna. Reguły
prywatności dotyczą nie tylko modułów, ale też struktur, enumów, funkcji i
metod.

Upublicznijmy też funkcję `add_to_waitlist`, dodając słowo kluczowe `pub` przed
jej definicją, jak w listingu 7-7.

<Listing number="7-7" file-name="src/lib.rs" caption="Dodanie słowa kluczowego `pub` do `mod hosting` i `fn add_to_waitlist` pozwala wywołać funkcję z `eat_at_restaurant`.">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-07/src/lib.rs:here}}
```

</Listing>

Teraz kod się skompiluje! Aby zrozumieć, dlaczego dodanie słowa kluczowego
`pub` pozwala nam użyć tych ścieżek w `eat_at_restaurant` zgodnie z regułami
prywatności, przyjrzyjmy się ścieżce bezwzględnej i względnej.

W ścieżce bezwzględnej zaczynamy od `crate`, korzenia drzewa modułów naszego
crate’a. Moduł `front_of_house` jest zdefiniowany w korzeniu crate’a. Choć
`front_of_house` nie jest publiczny, funkcja `eat_at_restaurant` jest
zdefiniowana w tym samym module co `front_of_house` (czyli `eat_at_restaurant`
i `front_of_house` są rodzeństwem), więc możemy odwoływać się do
`front_of_house` z `eat_at_restaurant`. Następny jest moduł `hosting` oznaczony
jako `pub`. Mamy dostęp do rodzica modułu `hosting`, więc mamy dostęp do
`hosting`. Wreszcie funkcja `add_to_waitlist` jest oznaczona jako `pub`, a my
mamy dostęp do jej modułu nadrzędnego, więc to wywołanie funkcji działa!

W ścieżce względnej logika jest taka sama jak w bezwzględnej, z wyjątkiem
pierwszego kroku: zamiast od korzenia crate’a ścieżka zaczyna się od
`front_of_house`. Moduł `front_of_house` jest zdefiniowany w tym samym module
co `eat_at_restaurant`, więc ścieżka względna zaczynająca się od modułu, w
którym zdefiniowano `eat_at_restaurant`, działa. Następnie, ponieważ `hosting`
i `add_to_waitlist` są oznaczone jako `pub`, reszta ścieżki również działa i to
wywołanie funkcji jest poprawne!

Jeśli planujesz udostępnić swój crate biblioteczny, by inne projekty mogły
korzystać z twojego kodu, publiczne API jest twoją umową z użytkownikami
crate’a, określającą, w jaki sposób mogą korzystać z twojego kodu. Zarządzanie
zmianami w publicznym API tak, by innym łatwiej było polegać na twoim crate’cie,
wymaga wielu przemyśleń. Te zagadnienia wykraczają poza zakres tej książki;
jeśli cię interesują, zajrzyj do
[wytycznych dotyczących API w Ruście][api-guidelines].

> #### Dobre praktyki dla pakietów z crate’em binarnym i bibliotecznym {#best-practices-for-packages-with-a-binary-and-a-library}
>
> Wspomnieliśmy, że pakiet (*package*) może zawierać zarówno korzeń crate’a
> binarnego _src/main.rs_, jak i korzeń crate’a bibliotecznego _src/lib.rs_, a
> oba crate’y domyślnie noszą nazwę pakietu. Zazwyczaj pakiety zawierające w ten
> sposób zarówno crate biblioteczny, jak i binarny mają w crate’cie binarnym
> tylko tyle kodu, ile potrzeba do uruchomienia pliku wykonywalnego, który
> wywołuje kod zdefiniowany w crate’cie bibliotecznym. Dzięki temu inne projekty
> mogą w jak największym stopniu korzystać z funkcjonalności pakietu, bo kod
> crate’a bibliotecznego można współdzielić.
>
> Drzewo modułów należy zdefiniować w _src/lib.rs_. Wtedy wszystkich
> publicznych elementów można używać w crate’cie binarnym, zaczynając ścieżki od
> nazwy pakietu. Crate binarny staje się użytkownikiem crate’a bibliotecznego,
> tak jak zupełnie zewnętrzny crate: może używać tylko publicznego API. Pomaga
> to zaprojektować dobre API – jesteś nie tylko jego autorem, ale też klientem!
>
> W [rozdziale 12][ch12]<!-- ignore --> zademonstrujemy tę praktykę
> organizacyjną na przykładzie programu wiersza poleceń, który będzie zawierał
> zarówno crate binarny, jak i biblioteczny.

{{#quiz ../quizzes/ch07-03-paths-sec1.toml}}

### Ścieżki względne zaczynające się od `super` {#starting-relative-paths-with-super}

Możemy tworzyć ścieżki względne, które zaczynają się w module nadrzędnym, a nie
w bieżącym module czy w korzeniu crate’a, umieszczając na początku ścieżki
`super`. Przypomina to rozpoczęcie ścieżki w systemie plików od `..`, co
oznacza przejście do katalogu nadrzędnego. Użycie `super` pozwala odwołać się
do elementu, o którym wiemy, że znajduje się w module nadrzędnym. Ułatwia to
reorganizację drzewa modułów, gdy moduł jest ściśle powiązany ze swoim
rodzicem, ale ten rodzic może kiedyś zostać przeniesiony w inne miejsce drzewa
modułów.

Spójrz na kod z listingu 7-8, który modeluje sytuację, w której szef kuchni
poprawia błędne zamówienie i osobiście podaje je klientowi. Funkcja
`fix_incorrect_order`, zdefiniowana w module `back_of_house`, wywołuje funkcję
`deliver_order`, zdefiniowaną w module nadrzędnym, podając ścieżkę do
`deliver_order` zaczynającą się od `super`.

<Listing number="7-8" file-name="src/lib.rs" caption="Wywołanie funkcji za pomocą ścieżki względnej zaczynającej się od `super`">

```rust,noplayground,test_harness
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-08/src/lib.rs}}
```

</Listing>

Funkcja `fix_incorrect_order` znajduje się w module `back_of_house`, więc za
pomocą `super` możemy przejść do rodzica modułu `back_of_house`, którym w
tym przypadku jest `crate`, czyli korzeń. Tam szukamy `deliver_order` i
znajdujemy ją. Sukces! Uważamy, że moduł `back_of_house` i funkcja
`deliver_order` prawdopodobnie zachowają tę samą relację względem siebie i
zostaną przeniesione razem, jeśli zdecydujemy się przeorganizować drzewo
modułów crate’a. Dlatego użyliśmy `super`, aby w przyszłości, gdy ten kod
trafi do innego modułu, mieć mniej miejsc do aktualizacji.

### Upublicznianie struktur i enumów {#making-structs-and-enums-public}

Za pomocą `pub` możemy też oznaczać struktury i enumy jako publiczne, ale z
użyciem `pub` przy strukturach i enumach wiąże się kilka dodatkowych
szczegółów. Jeśli użyjemy `pub` przed definicją struktury, struktura stanie się
publiczna, ale jej pola nadal będą prywatne. O tym, czy dane pole ma być
publiczne, możemy decydować osobno dla każdego pola. W listingu 7-9
zdefiniowaliśmy publiczną strukturę `back_of_house::Breakfast` z publicznym
polem `toast` i prywatnym polem `seasonal_fruit`. Modeluje to sytuację w
restauracji, w której klient może wybrać rodzaj pieczywa podawanego do
posiłku, ale to szef kuchni decyduje, jakie owoce do niego dołączyć, w
zależności od sezonu i tego, co jest w magazynie. Dostępne owoce szybko się
zmieniają, więc klienci nie mogą wybrać owoców ani nawet zobaczyć, jakie
dostaną.

<Listing number="7-9" file-name="src/lib.rs" caption="Struktura z częścią pól publicznych i częścią prywatnych">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-09/src/lib.rs}}
```

</Listing>

Ponieważ pole `toast` w strukturze `back_of_house::Breakfast` jest publiczne,
w `eat_at_restaurant` możemy zapisywać i odczytywać pole `toast` za pomocą
notacji kropkowej. Zauważ, że w `eat_at_restaurant` nie możemy używać pola
`seasonal_fruit`, bo `seasonal_fruit` jest prywatne. Spróbuj odkomentować
wiersz modyfikujący wartość pola `seasonal_fruit` i zobacz, jaki błąd
otrzymasz!

Zwróć też uwagę, że ponieważ `back_of_house::Breakfast` ma prywatne pole,
struktura musi udostępniać publiczną funkcję powiązaną (*associated function*),
która tworzy instancję `Breakfast` (tutaj nazwaliśmy ją `summer`). Gdyby
`Breakfast` nie miała takiej funkcji, nie moglibyśmy utworzyć instancji
`Breakfast` w `eat_at_restaurant`, bo nie moglibyśmy ustawić wartości
prywatnego pola `seasonal_fruit` w `eat_at_restaurant`.

Natomiast gdy upublicznimy enum, wszystkie jego warianty również stają się
publiczne. Wystarczy `pub` przed słowem kluczowym `enum`, jak pokazuje listing
7-10.

<Listing number="7-10" file-name="src/lib.rs" caption="Oznaczenie enuma jako publicznego upublicznia wszystkie jego warianty.">

```rust,noplayground
{{#rustdoc_include ../listings/ch07-managing-growing-projects/listing-07-10/src/lib.rs}}
```

</Listing>

Ponieważ upubliczniliśmy enum `Appetizer`, możemy używać wariantów `Soup` i
`Salad` w `eat_at_restaurant`.

Enumy nie są zbyt przydatne, jeśli ich warianty nie są publiczne; oznaczanie
każdego wariantu enuma słowem `pub` za każdym razem byłoby uciążliwe, dlatego
warianty enumów są domyślnie publiczne. Struktury często są przydatne, nawet
gdy ich pola nie są publiczne, więc pola struktur podlegają ogólnej regule:
wszystko jest domyślnie prywatne, chyba że oznaczono je jako `pub`.

Jest jeszcze jedna sytuacja związana z `pub`, której nie omówiliśmy, a dotyczy
ona ostatniego mechanizmu systemu modułów: słowa kluczowego `use`. Najpierw
omówimy samo `use`, a potem pokażemy, jak łączyć `pub` z `use`.

{{#quiz ../quizzes/ch07-03-paths-sec2.toml}}

[pub]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[api-guidelines]: https://rust-lang.github.io/api-guidelines/
[ch12]: ch12-00-an-io-project.html

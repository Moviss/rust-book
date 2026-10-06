## Przechowywanie tekstu zakodowanego w UTF-8 w łańcuchach znaków {#storing-utf-8-encoded-text-with-strings}

O łańcuchach znaków (*string*) mówiliśmy już w rozdziale 4, ale teraz
przyjrzymy się im dokładniej. Początkujący rustowcy (*Rustaceans*) często
utykają na łańcuchach z trzech powodów naraz: skłonności Rusta do ujawniania
możliwych błędów, tego, że łańcuchy są bardziej skomplikowaną strukturą danych,
niż sądzi wielu programistów, oraz UTF-8. Razem te czynniki mogą sprawiać
trudność, gdy przychodzisz z innych języków programowania.

Omawiamy łańcuchy w kontekście kolekcji, ponieważ są one zaimplementowane jako
kolekcja bajtów oraz zestaw metod, które dostarczają przydatnej
funkcjonalności, gdy te bajty interpretujemy jako tekst. W tym podrozdziale
omówimy operacje na `String` wspólne dla wszystkich typów kolekcji, takie jak
tworzenie, aktualizowanie i odczytywanie. Omówimy też, czym `String` różni się
od innych kolekcji – a mianowicie to, że indeksowanie `String` komplikują
różnice w tym, jak ludzie i komputery interpretują dane typu `String`.

<!-- Old headings. Do not remove or links may break. -->

<a id="what-is-a-string"></a>

### Definicja łańcucha znaków {#defining-strings}

Najpierw zdefiniujmy, co rozumiemy przez termin _łańcuch znaków_. Rust ma w
rdzeniu języka tylko jeden typ łańcuchowy: wycinek łańcucha (*string slice*)
`str`, zwykle spotykany w formie pożyczonej, `&str`. W rozdziale 4 mówiliśmy o
wycinkach łańcuchów, czyli referencjach do danych łańcucha zakodowanych w UTF-8
i przechowywanych gdzie indziej. Na przykład literały łańcuchowe są
przechowywane w pliku binarnym programu, a zatem są wycinkami łańcuchów.

Typ `String`, dostarczany przez bibliotekę standardową Rusta, a nie wbudowany w
rdzeń języka, to rozszerzalny, mutowalny (*mutable*) typ łańcuchowy zakodowany
w UTF-8, będący właścicielem swoich danych. Gdy rustowcy mówią o „łańcuchach” w
Ruście, mogą mieć na myśli zarówno typ `String`, jak i wycinek łańcucha `&str`,
a nie tylko jeden z nich. Choć ten podrozdział dotyczy głównie `String`, oba
typy są intensywnie używane w bibliotece standardowej Rusta i zarówno `String`,
jak i wycinki łańcuchów są zakodowane w UTF-8.

### Tworzenie nowego łańcucha {#creating-a-new-string}

Wiele operacji dostępnych dla `Vec<T>` jest dostępnych również dla `String`,
ponieważ `String` jest w rzeczywistości zaimplementowany jako opakowanie wokół
wektora (*vector*) bajtów z dodatkowymi gwarancjami, ograniczeniami i
możliwościami. Przykładem funkcji, która działa tak samo dla `Vec<T>` i
`String`, jest funkcja `new` tworząca instancję, pokazana w listingu 8-11.

<Listing number="8-11" caption="Tworzenie nowego, pustego `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-11/src/main.rs:here}}
```

</Listing>

Ten wiersz tworzy nowy, pusty łańcuch o nazwie `s`, do którego możemy potem
wczytać dane. Często mamy jakieś dane początkowe, od których chcemy zacząć
łańcuch. Używamy wtedy metody `to_string`, dostępnej dla każdego typu
implementującego *trait* (cecha typu, zbliżona do interfejsu) `Display`, tak
jak literały łańcuchowe. Listing 8-12 pokazuje dwa przykłady.

<Listing number="8-12" caption="Użycie metody `to_string` do utworzenia `String` z literału łańcuchowego">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-12/src/main.rs:here}}
```

</Listing>

Ten kod tworzy łańcuch zawierający `initial contents`.

Do utworzenia `String` z literału łańcuchowego możemy też użyć funkcji
`String::from`. Kod z listingu 8-13 jest równoważny kodowi z listingu 8-12,
który używa `to_string`.

<Listing number="8-13" caption="Użycie funkcji `String::from` do utworzenia `String` z literału łańcuchowego">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-13/src/main.rs:here}}
```

</Listing>

Ponieważ łańcuchów używa się do tak wielu rzeczy, mamy do dyspozycji wiele
różnych generycznych API dla łańcuchów, co daje nam sporo możliwości. Niektóre
z nich mogą wydawać się zbędne, ale wszystkie mają swoje zastosowanie! W tym
przypadku `String::from` i `to_string` robią to samo, więc wybór między nimi to
kwestia stylu i czytelności.

Pamiętaj, że łańcuchy są zakodowane w UTF-8, więc możemy w nich umieścić
dowolne poprawnie zakodowane dane, jak pokazuje listing 8-14.

<Listing number="8-14" caption="Przechowywanie w łańcuchach powitań w różnych językach">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:here}}
```

</Listing>

Wszystkie te wartości są poprawnymi wartościami typu `String`.

### Aktualizowanie łańcucha {#updating-a-string}

`String` może rosnąć, a jego zawartość może się zmieniać – tak samo jak
zawartość `Vec<T>` – jeśli dopiszesz do niego więcej danych. Do łączenia
wartości `String` możesz też wygodnie używać operatora `+` albo makra
`format!`.

<!-- Old headings. Do not remove or links may break. -->

<a id="appending-to-a-string-with-push_str-and-push"></a>

#### Dopisywanie za pomocą `push_str` lub `push` {#appending-with-push_str-or-push}

`String` możemy wydłużyć, dopisując do niego wycinek łańcucha metodą
`push_str`, jak pokazuje listing 8-15.

<Listing number="8-15" caption="Dopisywanie wycinka łańcucha do `String` za pomocą metody `push_str`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-15/src/main.rs:here}}
```

</Listing>

Po wykonaniu tych dwóch wierszy `s` będzie zawierać `foobar`. Metoda
`push_str` przyjmuje wycinek łańcucha, ponieważ niekoniecznie chcemy przejmować
własność (*ownership*) parametru. Na przykład w kodzie z listingu 8-16 chcemy
móc użyć `s2` po dopisaniu jego zawartości do `s1`.

<Listing number="8-16" caption="Użycie wycinka łańcucha po dopisaniu jego zawartości do `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-16/src/main.rs:here}}
```

</Listing>

Gdyby metoda `push_str` przejmowała własność `s2`, nie moglibyśmy wypisać jego
wartości w ostatnim wierszu. Ten kod działa jednak zgodnie z oczekiwaniami!

Metoda `push` przyjmuje jako parametr pojedynczy znak i dodaje go do `String`.
Listing 8-17 dodaje literę _l_ do `String` za pomocą metody `push`.

<Listing number="8-17" caption="Dodawanie jednego znaku do wartości `String` za pomocą `push`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-17/src/main.rs:here}}
```

</Listing>

W rezultacie `s` będzie zawierać `lol`.

<!-- Old headings. Do not remove or links may break. -->

<a id="concatenation-with-the--operator-or-the-format-macro"></a>

#### Łączenie za pomocą `+` lub `format!` {#concatenating-with--or-format}

Często zechcesz połączyć dwa istniejące łańcuchy. Jednym ze sposobów jest
użycie operatora `+`, jak pokazuje listing 8-18.

<Listing number="8-18" caption="Użycie operatora `+` do połączenia dwóch wartości `String` w nową wartość `String`">

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-18/src/main.rs:here}}
```

</Listing>

Łańcuch `s3` będzie zawierać `Hello, world!`. To, że `s1` po dodawaniu nie jest
już poprawny, oraz to, że użyliśmy referencji (*reference*) do `s2`, wynika z
sygnatury metody wywoływanej, gdy używamy operatora `+`. Operator `+` korzysta z
metody `add`, której sygnatura wygląda mniej więcej tak:

```rust,ignore
fn add(self, s: &str) -> String {
```

W bibliotece standardowej zobaczysz, że `add` jest zdefiniowana przy użyciu
typów generycznych (*generics*) i typów powiązanych (*associated type*). Tutaj
podstawiliśmy typy konkretne – tak właśnie dzieje się, gdy wywołujemy tę metodę
z wartościami `String`. Typy generyczne omówimy w rozdziale 10. Ta sygnatura
daje nam wskazówki potrzebne do zrozumienia zawiłości operatora `+`.

Po pierwsze, `s2` ma `&`, co oznacza, że do pierwszego łańcucha dodajemy
referencję do drugiego. Wynika to z parametru `s` funkcji `add`: do `String`
możemy dodać tylko wycinek łańcucha; nie możemy dodać do siebie dwóch wartości
`String`. Ale chwileczkę – typem `&s2` jest `&String`, a nie `&str`, jak
określa drugi parametr `add`. Dlaczego więc listing 8-18 się kompiluje?

Możemy użyć `&s2` w wywołaniu `add`, ponieważ kompilator potrafi niejawnie
przekształcić argument `&String` w `&str`. Gdy wywołujemy metodę `add`, Rust
stosuje *deref coercion* (automatyczną konwersję przez dereferencję), która
zamienia tutaj `&s2` na `&s2[..]`. *Deref coercion* omówimy dokładniej w
rozdziale 15. Ponieważ `add` nie przejmuje własności parametru `s`, `s2` po tej
operacji nadal będzie poprawną wartością `String`.

<!-- BEGIN INTERVENTION: f1ab2171-96f0-4380-b16d-9055a9a00415 -->
Po drugie, w sygnaturze widać, że `add` przejmuje własność `self`, ponieważ
`self` *nie* ma `&`. Oznacza to, że `s1` z listingu 8-18 zostanie przeniesiony
(*moved*) do wywołania `add` i po nim nie będzie już poprawny. Choć więc
`let s3 = s1 + &s2;` wygląda tak, jakby kopiowało oba łańcuchy i tworzyło nowy,
ta instrukcja (*statement*) w rzeczywistości robi co innego:
1. `add` przejmuje własność `s1`;
2. dopisuje do `s1` kopię zawartości `s2`;
3. a następnie zwraca własność `s1`.

Jeśli `s1` ma wystarczającą pojemność, by pomieścić `s2`, nie dochodzi do żadnej alokacji pamięci. Jeśli jednak pojemność `s1` jest za mała dla `s2`, `s1` wewnętrznie wykona większą alokację pamięci, która zmieści oba łańcuchy.
<!-- END INTERVENTION -->

Gdy musimy połączyć wiele łańcuchów, zachowanie operatora `+` staje się
nieporęczne:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-01-concat-multiple-strings/src/main.rs:here}}
```

W tym momencie `s` będzie zawierać `tic-tac-toe`. Przy tych wszystkich znakach
`+` i `"` trudno dostrzec, co się dzieje. Do bardziej skomplikowanego łączenia
łańcuchów możemy zamiast tego użyć makra `format!`:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/no-listing-02-format/src/main.rs:here}}
```

Ten kod również ustawia `s` na `tic-tac-toe`. Makro `format!` działa jak
`println!`, ale zamiast wypisywać wynik na ekran, zwraca `String` z tą
zawartością. Wersja kodu z `format!` jest znacznie czytelniejsza, a kod
generowany przez makro `format!` używa referencji, więc to wywołanie nie
przejmuje własności żadnego ze swoich parametrów.

{{#quiz ../quizzes/ch08-02-string-sec1.toml}}

### Indeksowanie łańcuchów {#indexing-into-strings}

W wielu innych językach programowania dostęp do poszczególnych znaków łańcucha
przez odwołanie się do nich za pomocą indeksu jest poprawną i powszechną
operacją. Jeśli jednak spróbujesz w Ruście dostać się do fragmentów `String`
za pomocą składni indeksowania, otrzymasz błąd. Spójrz na niepoprawny kod z
listingu 8-19.

<Listing number="8-19" caption="Próba użycia składni indeksowania ze `String`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-19/src/main.rs:here}}
```

</Listing>

Ten kod spowoduje następujący błąd:

```console
{{#include ../listings/ch08-common-collections/listing-08-19/output.txt}}
```

Komunikat błędu mówi wszystko: łańcuchy w Ruście nie obsługują indeksowania.
Ale dlaczego? Aby odpowiedzieć na to pytanie, musimy omówić, jak Rust
przechowuje łańcuchy w pamięci.

#### Reprezentacja wewnętrzna {#internal-representation}

`String` to opakowanie wokół `Vec<u8>`. Przyjrzyjmy się kilku poprawnie
zakodowanym w UTF-8 przykładowym łańcuchom z listingu 8-14. Najpierw temu:

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:spanish}}
```

W tym przypadku `len` wyniesie `4`, co oznacza, że wektor przechowujący łańcuch
`"Hola"` ma długość 4 bajtów. Każda z tych liter zajmuje w kodowaniu UTF-8 1
bajt. Następny wiersz może cię jednak zaskoczyć (zauważ, że ten łańcuch
zaczyna się wielką cyrylicką literą _Ze_, a nie cyfrą 3):

```rust
{{#rustdoc_include ../listings/ch08-common-collections/listing-08-14/src/main.rs:russian}}
```

Na pytanie o długość tego łańcucha można by odpowiedzieć, że wynosi 12.
Odpowiedź Rusta to jednak 24: tyle bajtów potrzeba do zakodowania
„Здравствуйте” w UTF-8, ponieważ każda wartość skalarna Unicode w tym łańcuchu
zajmuje 2 bajty pamięci. Dlatego indeks w bajtach łańcucha nie zawsze będzie
odpowiadał poprawnej wartości skalarnej Unicode. Dla przykładu rozważ ten
niepoprawny kod w Ruście:

```rust,ignore,does_not_compile
let hello = "Здравствуйте";
let answer = &hello[0];
```

Wiesz już, że `answer` nie będzie równe `З`, czyli pierwszej literze. W
kodowaniu UTF-8 pierwszym bajtem `З` jest `208`, a drugim `151`, więc mogłoby
się wydawać, że `answer` powinno w istocie wynosić `208`, ale `208` samo w
sobie nie jest poprawnym znakiem. Zwrócenie `208` raczej nie jest tym, czego
chciałby użytkownik pytający o pierwszą literę tego łańcucha; są to jednak
jedyne dane, jakie Rust ma pod indeksem bajtu 0. Użytkownicy na ogół nie chcą
otrzymywać wartości bajtu, nawet jeśli łańcuch zawiera wyłącznie litery
łacińskie: gdyby `&"hi"[0]` było poprawnym kodem zwracającym wartość bajtu,
zwróciłoby `104`, a nie `h`.

Odpowiedź brzmi więc tak: aby uniknąć zwracania nieoczekiwanej wartości i
powodowania błędów, które mogłyby nie zostać od razu wykryte, Rust w ogóle nie
kompiluje tego kodu i zapobiega nieporozumieniom na wczesnym etapie
programowania.

<!-- Old headings. Do not remove or links may break. -->

<a id="bytes-and-scalar-values-and-grapheme-clusters-oh-my"></a>

#### Bajty, wartości skalarne i klastry grafemów {#bytes-scalar-values-and-grapheme-clusters}

Kolejna kwestia związana z UTF-8 jest taka, że z perspektywy Rusta istnieją w
rzeczywistości trzy istotne sposoby patrzenia na łańcuchy: jako na bajty,
wartości skalarne i klastry grafemów (najbliższe temu, co nazwalibyśmy
_literami_).

Słowo w języku hindi „नमस्ते”, zapisane pismem dewanagari, jest przechowywane
jako wektor wartości `u8`, który wygląda tak:

```text
[224, 164, 168, 224, 164, 174, 224, 164, 184, 224, 165, 141, 224, 164, 164,
224, 165, 135]
```

To 18 bajtów – tak ostatecznie komputery przechowują te dane. Jeśli spojrzymy
na nie jak na wartości skalarne Unicode, czyli to, czym jest typ `char` w
Ruście, te bajty wyglądają tak:

```text
['न', 'म', 'स', '्', 'त', 'े']
```

Mamy tu sześć wartości `char`, ale czwarta i szósta nie są literami: to znaki
diakrytyczne, które same w sobie nie mają sensu. Wreszcie, jeśli spojrzymy na
nie jak na klastry grafemów, otrzymamy to, co człowiek nazwałby czterema
literami tworzącymi to słowo w hindi:

```text
["न", "म", "स्", "ते"]
```

Rust udostępnia różne sposoby interpretowania surowych danych łańcuchowych
przechowywanych przez komputery, dzięki czemu każdy program może wybrać
potrzebną mu interpretację, bez względu na to, w jakim języku naturalnym są
zapisane dane.

Ostatni powód, dla którego Rust nie pozwala indeksować `String` w celu
pobrania znaku, jest taki, że od operacji indeksowania oczekuje się, że zawsze
zajmą stały czas (O(1)). Ze `String` nie da się jednak zagwarantować takiej
wydajności, ponieważ Rust musiałby przejść przez zawartość od początku aż do
indeksu, aby ustalić, ile było w niej poprawnych znaków.

### Tworzenie wycinków łańcuchów {#slicing-strings}

Indeksowanie łańcucha to często zły pomysł, ponieważ nie jest jasne, jakiego
typu powinien być wynik operacji indeksowania łańcucha: wartość bajtu, znak,
klaster grafemów czy wycinek łańcucha. Jeśli więc naprawdę musisz użyć indeksów
do utworzenia wycinków łańcuchów, Rust prosi cię o większą precyzję.

Zamiast indeksować za pomocą `[]` z pojedynczą liczbą, możesz użyć `[]` z
zakresem, aby utworzyć wycinek łańcucha zawierający konkretne bajty:

```rust
let hello = "Здравствуйте";

let s = &hello[0..4];
```

Tutaj `s` będzie wartością typu `&str` zawierającą pierwsze 4 bajty łańcucha.
Wspomnieliśmy wcześniej, że każdy z tych znaków zajmuje 2 bajty, co oznacza, że
`s` będzie równe `Зд`.

Gdybyśmy spróbowali utworzyć wycinek obejmujący tylko część bajtów znaku, np.
`&hello[0..1]`, Rust spanikowałby (*panic*) w czasie działania programu, tak
samo jak przy próbie dostępu do niepoprawnego indeksu w wektorze:

```console
{{#include ../listings/ch08-common-collections/output-only-01-not-char-boundary/output.txt}}
```

Zachowaj ostrożność przy tworzeniu wycinków łańcuchów za pomocą zakresów,
ponieważ może to doprowadzić do awarii programu.

<!-- Old headings. Do not remove or links may break. -->

<a id="methods-for-iterating-over-strings"></a>

### Iterowanie po łańcuchach {#iterating-over-strings}

Najlepszym sposobem operowania na fragmentach łańcuchów jest jawne określenie,
czy chcesz znaków, czy bajtów. Dla pojedynczych wartości skalarnych Unicode
użyj metody `chars`. Wywołanie `chars` na „Зд” rozdziela i zwraca dwie wartości
typu `char`, a po wyniku możesz iterować, aby uzyskać dostęp do każdego
elementu:

```rust
for c in "Зд".chars() {
    println!("{c}");
}
```

Ten kod wypisze:

```text
З
д
```

Alternatywnie metoda `bytes` zwraca każdy surowy bajt, co może być
odpowiednie w twojej dziedzinie:

```rust
for b in "Зд".bytes() {
    println!("{b}");
}
```

Ten kod wypisze 4 bajty, z których składa się ten łańcuch:

```text
208
151
208
180
```

Pamiętaj jednak, że poprawne wartości skalarne Unicode mogą składać się z
więcej niż 1 bajtu.

Wydobywanie klastrów grafemów z łańcuchów, jak w przypadku pisma dewanagari,
jest skomplikowane, dlatego biblioteka standardowa nie udostępnia tej
funkcjonalności. Jeśli jej potrzebujesz, na [crates.io](https://crates.io/)<!-- ignore -->
znajdziesz odpowiednie *crate*’y (jednostki kompilacji w Ruście).

<!-- Old headings. Do not remove or links may break. -->

<a id="strings-are-not-so-simple"></a>

### Radzenie sobie ze złożonością łańcuchów {#handling-the-complexities-of-strings}

Podsumowując: łańcuchy są skomplikowane. Różne języki programowania
podejmują różne decyzje co do tego, jak przedstawić tę złożoność
programiście. Rust postanowił, że poprawna obsługa danych typu `String` będzie
domyślnym zachowaniem we wszystkich programach w Ruście, co oznacza, że
programiści muszą od początku poświęcić więcej uwagi obsłudze danych w UTF-8.
Ten kompromis odsłania więcej złożoności łańcuchów, niż widać w innych
językach programowania, ale oszczędza ci obsługiwania błędów związanych ze
znakami spoza ASCII na późniejszym etapie tworzenia oprogramowania.

Dobra wiadomość jest taka, że biblioteka standardowa oferuje wiele
funkcjonalności zbudowanych na typach `String` i `&str`, które pomagają
poprawnie radzić sobie z tymi złożonymi sytuacjami. Koniecznie zajrzyj do
dokumentacji, gdzie znajdziesz przydatne metody, takie jak `contains` do
wyszukiwania w łańcuchu i `replace` do zastępowania fragmentów łańcucha innym
łańcuchem.

Przejdźmy do czegoś nieco mniej skomplikowanego: map haszujących (*hash map*)!

{{#quiz ../quizzes/ch08-02-string-sec2.toml}}

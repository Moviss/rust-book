## Niebezpieczny Rust {#unsafe-rust}

Cały omawiany dotąd kod podlegał gwarancjom bezpieczeństwa pamięci Rusta,
egzekwowanym w czasie kompilacji (*compile-time*). Rust kryje jednak w sobie
drugi język, który tych gwarancji nie egzekwuje: nazywa się on _niebezpiecznym
Rustem_ (*unsafe Rust*) i działa tak samo jak zwykły Rust, ale daje nam
dodatkowe supermoce.

Niebezpieczny Rust istnieje, ponieważ analiza statyczna jest z natury
zachowawcza. Gdy kompilator próbuje ustalić, czy kod dotrzymuje gwarancji,
lepiej, żeby odrzucił pewne poprawne programy, niż zaakceptował pewne
niepoprawne. Nawet jeśli kod _może_ być w porządku, kompilator Rusta odrzuci go,
jeśli nie ma dość informacji, by mieć pewność. W takich sytuacjach możesz użyć
niebezpiecznego kodu, by powiedzieć kompilatorowi: „Zaufaj mi, wiem, co robię”.
Pamiętaj jednak, że niebezpiecznego Rusta używasz na własne ryzyko: jeśli
użyjesz niebezpiecznego kodu niepoprawnie, mogą wystąpić problemy wynikające z
braku bezpieczeństwa pamięci, takie jak dereferencja (*dereference*) wskaźnika
null.

Drugi powód, dla którego Rust ma niebezpieczne alter ego, jest taki, że sprzęt
komputerowy, na którym wszystko działa, jest z natury niebezpieczny. Gdyby Rust
nie pozwalał na niebezpieczne operacje, niektórych zadań nie dałoby się
wykonać. Rust musi umożliwiać niskopoziomowe programowanie systemowe, takie jak
bezpośrednia interakcja z systemem operacyjnym, a nawet pisanie własnego
systemu operacyjnego. Niskopoziomowe programowanie systemowe jest jednym z
celów tego języka. Zobaczmy, co możemy zrobić w niebezpiecznym Ruście i jak to
zrobić.

<!-- Old headings. Do not remove or links may break. -->

<a id="unsafe-superpowers"></a>

### Korzystanie z niebezpiecznych supermocy {#performing-unsafe-superpowers}

Aby przełączyć się na niebezpieczny Rust, użyj słowa kluczowego (*keyword*)
`unsafe`, a następnie otwórz nowy blok zawierający niebezpieczny kod. W
niebezpiecznym Ruście możesz wykonać pięć działań, których nie da się wykonać w
bezpiecznym Ruście; nazywamy je _niebezpiecznymi supermocami_ (*unsafe
superpowers*). Te supermoce obejmują możliwość:

1. dereferencji surowego wskaźnika (*raw pointer*);
1. wywołania niebezpiecznej funkcji lub metody;
1. odczytu lub modyfikacji mutowalnej (*mutable*) zmiennej statycznej;
1. implementacji niebezpiecznego *traitu* (cechy typu, zbliżonej do
   interfejsu);
1. dostępu do pól unii (`union`).

Trzeba pamiętać, że `unsafe` nie wyłącza *borrow checkera* (mechanizmu
sprawdzania pożyczeń) ani żadnych innych kontroli bezpieczeństwa Rusta: jeśli
użyjesz referencji (*reference*) w niebezpiecznym kodzie, nadal zostanie ona
sprawdzona. Słowo kluczowe `unsafe` daje jedynie dostęp do tych pięciu
mechanizmów, których kompilator nie sprawdza potem pod kątem bezpieczeństwa
pamięci. Wewnątrz bloku unsafe nadal masz więc pewien stopień bezpieczeństwa.

Poza tym `unsafe` nie oznacza, że kod wewnątrz bloku jest koniecznie
niebezpieczny ani że na pewno będzie miał problemy z bezpieczeństwem pamięci:
chodzi o to, że to ty jako programista zadbasz o to, by kod wewnątrz bloku
`unsafe` odwoływał się do pamięci w prawidłowy sposób.

Ludzie są omylni i błędy się zdarzają, ale dzięki wymogowi umieszczania tych
pięciu niebezpiecznych operacji w blokach oznaczonych `unsafe` będziesz wiedzieć,
że wszelkie błędy związane z bezpieczeństwem pamięci muszą się znajdować w
którymś bloku `unsafe`. Dbaj o to, by bloki `unsafe` były małe; podziękujesz sobie
później, gdy będziesz szukać błędów pamięci.

Aby jak najbardziej odizolować niebezpieczny kod, najlepiej zamknąć go w
bezpiecznej abstrakcji i udostępnić bezpieczne API, o czym opowiemy w dalszej
części rozdziału, przy okazji niebezpiecznych funkcji i metod. Części
biblioteki standardowej są zaimplementowane jako bezpieczne abstrakcje nad
niebezpiecznym kodem, który przeszedł audyt. Opakowanie niebezpiecznego kodu w
bezpieczną abstrakcję zapobiega rozlewaniu się `unsafe` po wszystkich
miejscach, w których ty lub twoi użytkownicy chcielibyście korzystać z
funkcjonalności zaimplementowanej za pomocą kodu `unsafe`, ponieważ korzystanie
z bezpiecznej abstrakcji jest bezpieczne.

Przyjrzyjmy się po kolei każdej z pięciu niebezpiecznych supermocy. Zobaczymy
też kilka abstrakcji, które zapewniają bezpieczny interfejs do niebezpiecznego
kodu.

### Dereferencja surowego wskaźnika {#dereferencing-a-raw-pointer}

W podrozdziale [„Borrow checker wykrywa naruszenia uprawnień”][permission-violations]<!-- ignore --> w rozdziale 4
opisaliśmy, jak kompilator zapewnia, że referencje są zawsze prawidłowe.
Niebezpieczny Rust ma dwa nowe typy, zwane _surowymi wskaźnikami_, które są
podobne do referencji. Podobnie jak referencje, surowe wskaźniki mogą być
niemutowalne lub mutowalne i zapisuje się je
odpowiednio jako `*const T` i `*mut T`. Gwiazdka nie jest tu operatorem
dereferencji, lecz częścią nazwy typu. W kontekście surowych wskaźników
_niemutowalny_ oznacza, że po dereferencji wskaźnika nie można bezpośrednio
przypisać mu wartości.

W odróżnieniu od referencji i inteligentnych wskaźników (*smart pointers*)
surowe wskaźniki:

- mogą ignorować reguły pożyczania (*borrowing*), ponieważ dopuszczają
  jednoczesne istnienie niemutowalnych i mutowalnych wskaźników albo wielu
  mutowalnych wskaźników do tego samego miejsca;
- nie mają gwarancji, że wskazują na prawidłową pamięć;
- mogą mieć wartość null;
- nie implementują żadnego automatycznego sprzątania.

Rezygnując z egzekwowania tych gwarancji przez Rusta, możesz porzucić
zagwarantowane bezpieczeństwo w zamian za większą wydajność albo możliwość
współpracy z innym językiem lub sprzętem, których gwarancje Rusta nie
obejmują.

Listing 20-1 pokazuje, jak utworzyć niemutowalny i mutowalny surowy wskaźnik.

<Listing number="20-1" caption="Tworzenie surowych wskaźników za pomocą operatorów surowego pożyczania">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-01/src/main.rs:here}}
```

</Listing>

Zwróć uwagę, że w tym kodzie nie ma słowa kluczowego `unsafe`. Surowe
wskaźniki możemy tworzyć w bezpiecznym kodzie; nie możemy jedynie wykonywać
ich dereferencji poza blokiem unsafe, o czym przekonasz się za chwilę.

Utworzyliśmy surowe wskaźniki za pomocą operatorów surowego pożyczania (*raw
borrow operators*): `&raw const num` tworzy niemutowalny surowy wskaźnik
`*const i32`, a `&raw mut num` tworzy mutowalny surowy wskaźnik `*mut i32`.
Ponieważ utworzyliśmy je bezpośrednio ze zmiennej lokalnej, wiemy, że te
konkretne surowe wskaźniki są prawidłowe, ale nie możemy zakładać tego o
dowolnym surowym wskaźniku.

Aby to zademonstrować, utworzymy teraz surowy wskaźnik, którego prawidłowości
nie możemy być aż tak pewni – zamiast operatora surowego pożyczania użyjemy
słowa kluczowego `as` do rzutowania wartości. Listing 20-2 pokazuje, jak
utworzyć surowy wskaźnik do dowolnego miejsca w pamięci. Próba użycia dowolnej
pamięci jest niezdefiniowana: pod tym adresem mogą być dane albo może ich nie
być, kompilator może zoptymalizować kod tak, że w ogóle nie dojdzie do dostępu
do pamięci, a program może też zakończyć się błędem segmentacji. Zwykle nie ma
dobrego powodu, by pisać taki kod, zwłaszcza gdy można zamiast tego użyć
operatora surowego pożyczania, ale jest to możliwe.

<Listing number="20-2" caption="Tworzenie surowego wskaźnika do dowolnego adresu w pamięci">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-02/src/main.rs:here}}
```

</Listing>

Przypomnijmy: surowe wskaźniki możemy tworzyć w bezpiecznym kodzie, ale nie
możemy wykonywać ich dereferencji i odczytywać wskazywanych przez nie danych. W
listingu 20-3 używamy na surowym wskaźniku operatora dereferencji `*`, co
wymaga bloku `unsafe`.

<Listing number="20-3" caption="Dereferencja surowych wskaźników wewnątrz bloku `unsafe`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-03/src/main.rs:here}}
```

</Listing>

Samo utworzenie wskaźnika nie wyrządza szkody; dopiero przy próbie dostępu do
wartości, na którą wskazuje, możemy natrafić na nieprawidłową wartość.

Zauważ też, że w listingach 20-1 i 20-3 utworzyliśmy surowe wskaźniki
`*const i32` i `*mut i32`, które wskazywały na to samo miejsce w pamięci, w
którym przechowywana jest zmienna `num`. Gdybyśmy zamiast tego spróbowali
utworzyć niemutowalną i mutowalną referencję do `num`, kod by się nie
skompilował, ponieważ reguły własności (*ownership*) Rusta nie pozwalają na
istnienie mutowalnej referencji jednocześnie z jakąkolwiek niemutowalną. Za
pomocą surowych wskaźników możemy utworzyć mutowalny i niemutowalny wskaźnik
do tego samego miejsca i zmieniać dane przez wskaźnik mutowalny, potencjalnie
powodując wyścig danych. Uważaj!

Skoro wiąże się z tym tyle zagrożeń, po co w ogóle używać surowych wskaźników?
Jednym z głównych zastosowań jest współpraca z kodem w C, co zobaczysz w
następnym podrozdziale. Innym jest budowanie bezpiecznych abstrakcji, których
borrow checker nie rozumie. Najpierw przedstawimy niebezpieczne funkcje, a
potem przyjrzymy się przykładowi bezpiecznej abstrakcji korzystającej z
niebezpiecznego kodu.

### Wywoływanie niebezpiecznej funkcji lub metody {#calling-an-unsafe-function-or-method}

Drugim rodzajem operacji, które możesz wykonać w bloku unsafe, jest
wywoływanie niebezpiecznych funkcji. Niebezpieczne funkcje i metody wyglądają
dokładnie tak samo jak zwykłe funkcje i metody, ale przed resztą definicji mają
dodatkowe `unsafe`. Słowo kluczowe `unsafe` oznacza w tym kontekście, że
funkcja ma wymagania, których musimy dotrzymać przy jej wywołaniu, ponieważ
Rust nie może zagwarantować, że je spełniliśmy. Wywołując niebezpieczną
funkcję wewnątrz bloku `unsafe`, deklarujemy, że przeczytaliśmy jej
dokumentację i bierzemy odpowiedzialność za dotrzymanie jej kontraktów.

Oto niebezpieczna funkcja o nazwie `dangerous`, której treść nic nie robi:

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/no-listing-01-unsafe-fn/src/main.rs:here}}
```

Funkcję `dangerous` musimy wywołać w osobnym bloku `unsafe`. Jeśli spróbujemy
wywołać `dangerous` bez bloku `unsafe`, otrzymamy błąd:

```console
{{#include ../listings/ch20-advanced-features/output-only-01-missing-unsafe/output.txt}}
```

Blokiem `unsafe` zapewniamy Rusta, że przeczytaliśmy dokumentację funkcji,
rozumiemy, jak jej poprawnie używać, i sprawdziliśmy, że spełniamy jej
kontrakt.

Aby wykonać niebezpieczne operacje w treści funkcji `unsafe`, nadal musisz użyć
bloku `unsafe`, tak jak w zwykłej funkcji, a kompilator ostrzeże cię, jeśli o
tym zapomnisz. Pomaga nam to utrzymywać bloki `unsafe` tak małe, jak to
możliwe, bo niebezpieczne operacje mogą nie być potrzebne w całej treści
funkcji.

#### Tworzenie bezpiecznej abstrakcji nad niebezpiecznym kodem {#creating-a-safe-abstraction-over-unsafe-code}

To, że funkcja zawiera niebezpieczny kod, nie oznacza, że musimy oznaczyć całą
funkcję jako niebezpieczną. Opakowanie niebezpiecznego kodu w bezpieczną
funkcję to wręcz powszechna abstrakcja. Jako przykład przeanalizujmy funkcję
`split_at_mut` z biblioteki standardowej, która wymaga trochę niebezpiecznego
kodu. Zastanowimy się, jak można by ją zaimplementować. Ta bezpieczna metoda
jest zdefiniowana na mutowalnych wycinkach (*slices*): przyjmuje jeden wycinek
i dzieli go na dwa w miejscu indeksu podanego jako argument. Listing 20-4
pokazuje, jak używać `split_at_mut`.

<Listing number="20-4" caption="Użycie bezpiecznej funkcji `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-04/src/main.rs:here}}
```

</Listing>

Nie da się zaimplementować tej funkcji wyłącznie w bezpiecznym Ruście. Próba
mogłaby wyglądać mniej więcej tak jak w listingu 20-5, który się nie
skompiluje. Dla uproszczenia zaimplementujemy `split_at_mut` jako funkcję, a
nie metodę, i tylko dla wycinków wartości `i32`, a nie dla typu generycznego
(*generic type*) `T`.

<Listing number="20-5" caption="Próba implementacji `split_at_mut` wyłącznie w bezpiecznym Ruście">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-05/src/main.rs:here}}
```

</Listing>

Ta funkcja najpierw pobiera całkowitą długość wycinka. Następnie za pomocą
asercji sprawdza, czy indeks podany jako parametr mieści się w wycinku, czyli
czy jest mniejszy lub równy jego długości. Dzięki asercji, jeśli przekażemy
indeks większy niż długość, funkcja spanikuje, zanim spróbuje go użyć do
podziału wycinka.

Następnie zwracamy w krotce (*tuple*) dwa mutowalne wycinki: jeden od początku
oryginalnego wycinka do indeksu `mid`, a drugi od `mid` do końca wycinka.

Gdy spróbujemy skompilować kod z listingu 20-5, otrzymamy błąd:

```console
{{#include ../listings/ch20-advanced-features/listing-20-05/output.txt}}
```

Borrow checker Rusta nie rozumie, że pożyczamy różne części wycinka; wie tylko,
że dwukrotnie pożyczamy z tego samego wycinka. Pożyczanie różnych części
wycinka jest w gruncie rzeczy w porządku, ponieważ te dwa wycinki na siebie
nie nachodzą, ale Rust nie jest na tyle sprytny, by to wiedzieć. Gdy wiemy, że
kod jest w porządku, a Rust tego nie wie, przychodzi czas, by sięgnąć po
niebezpieczny kod.

Listing 20-6 pokazuje, jak za pomocą bloku `unsafe`, surowego wskaźnika i kilku
wywołań niebezpiecznych funkcji sprawić, by implementacja `split_at_mut`
działała.

<Listing number="20-6" caption="Użycie niebezpiecznego kodu w implementacji funkcji `split_at_mut`">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-06/src/main.rs:here}}
```

</Listing>

Przypomnij sobie z podrozdziału [„Typ wycinka”][the-slice-type]<!-- ignore --> w
rozdziale 4, że wycinek to wskaźnik na pewne dane i długość wycinka. Metody
`len` używamy do pobrania długości wycinka, a metody `as_mut_ptr` – do
uzyskania surowego wskaźnika wycinka. Ponieważ mamy mutowalny wycinek wartości
`i32`, `as_mut_ptr` zwraca surowy wskaźnik typu `*mut i32`, który zapisaliśmy
w zmiennej `ptr`.

Zachowujemy asercję, że indeks `mid` mieści się w wycinku. Następnie
przechodzimy do niebezpiecznego kodu: funkcja `slice::from_raw_parts_mut`
przyjmuje surowy wskaźnik i długość, a następnie tworzy wycinek. Używamy jej do
utworzenia wycinka, który zaczyna się od `ptr` i ma długość `mid` elementów.
Potem wywołujemy na `ptr` metodę `add` z argumentem `mid`, by uzyskać surowy
wskaźnik zaczynający się od `mid`, i tworzymy wycinek z użyciem tego wskaźnika
oraz liczby elementów pozostałych za `mid` jako długości.

Funkcja `slice::from_raw_parts_mut` jest niebezpieczna, ponieważ przyjmuje
surowy wskaźnik i musi ufać, że jest on prawidłowy. Metoda `add` na surowych
wskaźnikach również jest niebezpieczna, ponieważ musi ufać, że miejsce po
przesunięciu także jest prawidłowym wskaźnikiem. Dlatego musieliśmy umieścić
wywołania `slice::from_raw_parts_mut` i `add` w bloku `unsafe`, aby móc je
wywołać. Analizując kod i dodając asercję, że `mid` musi być mniejsze lub równe
`len`, możemy stwierdzić, że wszystkie surowe wskaźniki użyte w bloku `unsafe`
będą prawidłowymi wskaźnikami na dane wewnątrz wycinka. To dopuszczalne i
właściwe użycie `unsafe`.

Zwróć uwagę, że nie musimy oznaczać powstałej funkcji `split_at_mut` jako
`unsafe` i możemy ją wywoływać z bezpiecznego Rusta. Utworzyliśmy bezpieczną
abstrakcję nad niebezpiecznym kodem – implementację funkcji, która używa kodu
`unsafe` w bezpieczny sposób, ponieważ tworzy wyłącznie prawidłowe wskaźniki
na dane, do których ta funkcja ma dostęp.

Natomiast użycie `slice::from_raw_parts_mut` w listingu 20-7 najprawdopodobniej
doprowadziłoby do awarii przy próbie użycia wycinka. Ten kod bierze dowolne
miejsce w pamięci i tworzy wycinek o długości 10 000 elementów.

<Listing number="20-7" caption="Tworzenie wycinka z dowolnego miejsca w pamięci">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-07/src/main.rs:here}}
```

</Listing>

Pamięć w tym dowolnym miejscu nie należy do nas i nie ma gwarancji, że wycinek
tworzony przez ten kod zawiera prawidłowe wartości `i32`. Próba użycia `values`
tak, jakby był prawidłowym wycinkiem, skutkuje niezdefiniowanym zachowaniem
(*undefined behavior*).

#### Wywoływanie kodu zewnętrznego za pomocą funkcji `extern` {#using-extern-functions-to-call-external-code}

Czasami twój kod w Ruście musi współpracować z kodem napisanym w innym języku.
W tym celu Rust ma słowo kluczowe `extern`, które ułatwia tworzenie i
używanie _interfejsu funkcji obcych_ (*Foreign Function Interface*, FFI), czyli
sposobu, w jaki jeden język programowania definiuje funkcje i pozwala innemu
(obcemu) językowi programowania je wywoływać.

Listing 20-8 pokazuje, jak przygotować integrację z funkcją `abs` z biblioteki
standardowej C. Funkcje zadeklarowane w blokach `extern` są na ogół
niebezpieczne do wywołania z kodu w Ruście, więc bloki `extern` również muszą
być oznaczone jako `unsafe`. Powód jest taki, że inne języki nie egzekwują
reguł i gwarancji Rusta, a Rust nie może ich sprawdzić, więc odpowiedzialność
za bezpieczeństwo spada na programistę.

<Listing number="20-8" file-name="src/main.rs" caption="Deklarowanie i wywoływanie funkcji `extern` zdefiniowanej w innym języku">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-08/src/main.rs}}
```

</Listing>

W bloku `unsafe extern "C"` wymieniamy nazwy i sygnatury funkcji zewnętrznych
z innego języka, które chcemy wywołać. Część `"C"` określa, którego
_binarnego interfejsu aplikacji_ (*application binary interface*, ABI) używa
funkcja zewnętrzna: ABI definiuje, jak wywołać funkcję na poziomie asemblera.
ABI `"C"` jest najpopularniejszy i odpowiada ABI języka programowania C.
Informacje o wszystkich ABI obsługiwanych przez Rusta znajdziesz w
[dokumentacji Rust Reference][ABI].

Każdy element zadeklarowany w bloku `unsafe extern` jest niejawnie
niebezpieczny. Niektóre funkcje FFI *są* jednak bezpieczne do wywołania. Na
przykład funkcja `abs` z biblioteki standardowej C nie wiąże się z żadnymi
kwestiami bezpieczeństwa pamięci i wiemy, że można ją wywołać z dowolną
wartością `i32`. W takich przypadkach możemy użyć słowa kluczowego `safe`, by
zaznaczyć, że ta konkretna funkcja jest bezpieczna do wywołania, mimo że
znajduje się w bloku `unsafe extern`. Po tej zmianie jej wywołanie nie wymaga
już bloku `unsafe`, jak pokazuje listing 20-9.

<Listing number="20-9" file-name="src/main.rs" caption="Jawne oznaczenie funkcji jako `safe` w bloku `unsafe extern` i jej bezpieczne wywołanie">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-09/src/main.rs}}
```

</Listing>

Oznaczenie funkcji jako `safe` samo w sobie nie czyni jej bezpieczną! Jest to
raczej obietnica składana Rustowi, że funkcja jest bezpieczna. Dotrzymanie tej
obietnicy nadal jest twoim obowiązkiem!

#### Wywoływanie funkcji Rusta z innych języków {#calling-rust-functions-from-other-languages}

Za pomocą `extern` możemy też utworzyć interfejs, który pozwala innym językom
wywoływać funkcje napisane w Ruście. Zamiast tworzyć cały blok `extern`,
dodajemy słowo kluczowe `extern` i określamy ABI tuż przed słowem kluczowym
`fn` danej funkcji. Musimy też dodać adnotację `#[unsafe(no_mangle)]`, aby
powiedzieć kompilatorowi Rusta, żeby nie dekorował nazwy tej funkcji.
_Dekorowanie nazw_ (*mangling*) to zmiana przez kompilator nadanej przez nas
nazwy funkcji na inną nazwę, która zawiera więcej informacji dla innych etapów
kompilacji, ale jest mniej czytelna dla człowieka. Kompilator każdego języka
programowania dekoruje nazwy nieco inaczej, więc aby inne języki mogły
odwołać się do funkcji Rusta po nazwie, musimy wyłączyć dekorowanie nazw przez
kompilator Rusta. Jest to niebezpieczne, ponieważ bez wbudowanego dekorowania
mogą wystąpić kolizje nazw między bibliotekami, więc to naszym obowiązkiem jest
upewnić się, że wybrana nazwa może bezpiecznie zostać wyeksportowana bez
dekorowania.

W poniższym przykładzie udostępniamy funkcję `call_from_c` kodowi w C, po
skompilowaniu jej do biblioteki współdzielonej i skonsolidowaniu z kodem w C:

```
#[unsafe(no_mangle)]
pub extern "C" fn call_from_c() {
    println!("Just called a Rust function from C!");
}
```

Takie użycie `extern` wymaga `unsafe` tylko w atrybucie, a nie przy bloku
`extern`.

### Odczyt lub modyfikacja mutowalnej zmiennej statycznej {#accessing-or-modifying-a-mutable-static-variable}

W tej książce nie mówiliśmy jeszcze o zmiennych globalnych, które Rust
obsługuje, ale które mogą sprawiać problemy w połączeniu z regułami własności
Rusta. Jeśli dwa wątki odwołują się do tej samej mutowalnej zmiennej
globalnej, może to spowodować wyścig danych.

W Ruście zmienne globalne nazywa się zmiennymi _statycznymi_ (*static*).
Listing 20-10 pokazuje przykładową deklarację i użycie zmiennej statycznej,
której wartością jest wycinek łańcucha znaków (*string slice*).

<Listing number="20-10" file-name="src/main.rs" caption="Definiowanie i używanie niemutowalnej zmiennej statycznej">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-10/src/main.rs}}
```

</Listing>

Zmienne statyczne są podobne do stałych (*constants*), które omawialiśmy w
podrozdziale [„Deklarowanie stałych”][constants]<!-- ignore --> w rozdziale 3.
Zgodnie z konwencją nazwy zmiennych statycznych zapisuje się w stylu
`SCREAMING_SNAKE_CASE`. Zmienne statyczne mogą przechowywać wyłącznie
referencje z czasem życia (*lifetime*) `'static`, co oznacza, że kompilator
Rusta potrafi sam ustalić czas życia i nie musimy go jawnie oznaczać. Odczyt
niemutowalnej zmiennej statycznej jest bezpieczny.

Subtelna różnica między stałymi a niemutowalnymi zmiennymi statycznymi polega
na tym, że wartości w zmiennej statycznej mają stały adres w pamięci. Użycie
takiej wartości zawsze odwołuje się do tych samych danych. Stałe natomiast
mogą powielać swoje dane przy każdym użyciu. Kolejna różnica polega na tym, że
zmienne statyczne mogą być mutowalne. Odczyt i modyfikacja mutowalnych
zmiennych statycznych są _niebezpieczne_. Listing 20-11 pokazuje, jak
zadeklarować mutowalną zmienną statyczną o nazwie `COUNTER`, odczytać ją i
zmodyfikować.

<Listing number="20-11" file-name="src/main.rs" caption="Odczyt i zapis mutowalnej zmiennej statycznej są niebezpieczne.">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-11/src/main.rs}}
```

</Listing>

Podobnie jak w przypadku zwykłych zmiennych, mutowalność określamy za pomocą
słowa kluczowego `mut`. Każdy kod, który odczytuje lub zapisuje `COUNTER`,
musi się znajdować w bloku `unsafe`. Kod z listingu 20-11 kompiluje się i
wypisuje `COUNTER: 3`, tak jak można się spodziewać, ponieważ jest
jednowątkowy. Dostęp do `COUNTER` z wielu wątków prawdopodobnie prowadziłby do
wyścigów danych, więc jest to niezdefiniowane zachowanie. Dlatego musimy
oznaczyć całą funkcję jako `unsafe` i udokumentować ograniczenie dotyczące
bezpieczeństwa, aby każdy, kto ją wywołuje, wiedział, co wolno, a czego nie
wolno mu bezpiecznie robić.

Gdy piszemy niebezpieczną funkcję, idiomatyczne jest napisanie komentarza
zaczynającego się od `SAFETY` i wyjaśniającego, co wywołujący musi zrobić, aby
bezpiecznie wywołać funkcję. Podobnie, gdy wykonujemy niebezpieczną operację,
idiomatyczne jest napisanie komentarza zaczynającego się od `SAFETY`, który
wyjaśnia, w jaki sposób przestrzegane są reguły bezpieczeństwa.

Ponadto kompilator domyślnie odrzuca, za pomocą lintu (reguły ostrzeżeń
kompilatora), każdą próbę utworzenia referencji do mutowalnej zmiennej
statycznej. Musisz albo jawnie zrezygnować z ochrony tego lintu, dodając
adnotację `#[allow(static_mut_refs)]`, albo odwoływać się do mutowalnej
zmiennej statycznej przez surowy wskaźnik utworzony jednym z operatorów
surowego pożyczania. Dotyczy to również sytuacji, w których referencja
tworzona jest niejawnie, na przykład gdy zmienna jest użyta w `println!` w tym
listingu. Wymóg tworzenia referencji do mutowalnych zmiennych statycznych przez
surowe wskaźniki sprawia, że wymagania bezpieczeństwa związane z ich używaniem
stają się bardziej oczywiste.

Przy mutowalnych danych dostępnych globalnie trudno zapewnić, że nie wystąpią
wyścigi danych, i dlatego Rust uznaje mutowalne zmienne statyczne za
niebezpieczne. Tam, gdzie to możliwe, lepiej korzystać z technik współbieżności
(*concurrency*) i bezpiecznych wątkowo inteligentnych wskaźników omówionych w
rozdziale 16, aby kompilator sprawdzał, czy dostęp do danych z różnych wątków
odbywa się bezpiecznie.

### Implementacja niebezpiecznego traitu {#implementing-an-unsafe-trait}

Za pomocą `unsafe` możemy zaimplementować niebezpieczny trait. Trait jest niebezpieczny, gdy co najmniej jedna z jego
metod ma jakiś niezmiennik, którego kompilator nie może zweryfikować.
Deklarujemy, że trait jest `unsafe`, dodając słowo kluczowe `unsafe` przed
`trait` i oznaczając implementację traitu również jako `unsafe`, jak pokazano w
listingu 20-12.

<Listing number="20-12" caption="Definiowanie i implementacja niebezpiecznego traitu">

```rust
{{#rustdoc_include ../listings/ch20-advanced-features/listing-20-12/src/main.rs:here}}
```

</Listing>

Używając `unsafe impl`, obiecujemy, że dotrzymamy niezmienników, których
kompilator nie może zweryfikować.

Jako przykład przypomnij sobie traity znacznikowe (*marker traits*) `Send` i
`Sync`, które omawialiśmy w podrozdziale
[„Rozszerzalna współbieżność dzięki `Send` i `Sync`”][send-and-sync]<!-- ignore -->
w rozdziale 16: kompilator implementuje te traity automatycznie, jeśli nasze
typy składają się wyłącznie z innych typów implementujących `Send` i `Sync`.
Jeśli implementujemy typ, który zawiera typ nieimplementujący `Send` lub
`Sync`, na przykład surowe wskaźniki, i chcemy oznaczyć ten typ jako `Send` lub
`Sync`, musimy użyć `unsafe`. Rust nie może zweryfikować, że nasz typ
dotrzymuje gwarancji, że można go bezpiecznie przesyłać między wątkami lub
używać z wielu wątków; dlatego musimy przeprowadzić te kontrole ręcznie i
zaznaczyć to za pomocą `unsafe`.

### Dostęp do pól unii {#accessing-fields-of-a-union}

Ostatnią operacją, którą można wykonać tylko z `unsafe`, jest dostęp do pól
unii. *Unia* (*union*) przypomina `struct`, ale w danej instancji w danym
momencie używane jest tylko jedno z zadeklarowanych pól. Unie służą przede
wszystkim do współpracy z uniami w kodzie w C. Dostęp do pól unii jest
niebezpieczny, ponieważ Rust nie może zagwarantować typu danych
przechowywanych aktualnie w instancji unii. Więcej o uniach dowiesz się z
[dokumentacji Rust Reference][unions].

### Sprawdzanie niebezpiecznego kodu za pomocą Miri {#using-miri-to-check-unsafe-code}

Pisząc niebezpieczny kod, możesz chcieć sprawdzić, czy to, co napisano,
rzeczywiście jest bezpieczne i poprawne. Jednym z najlepszych sposobów jest
użycie Miri – oficjalnego narzędzia Rusta do wykrywania niezdefiniowanego
zachowania. Podczas gdy borrow checker jest narzędziem _statycznym_, które
działa w czasie kompilacji, Miri jest narzędziem _dynamicznym_, które działa w
czasie działania programu. Sprawdza kod, uruchamiając program lub jego zestaw
testów i wykrywając sytuacje, w których naruszasz znane mu reguły dotyczące
tego, jak Rust powinien działać.

Korzystanie z Miri wymaga wersji nightly Rusta (więcej o niej piszemy w
[dodatku G: Jak powstaje Rust i „Rust nightly”][nightly]<!-- ignore -->).
Zarówno Rust nightly, jak i narzędzie Miri możesz zainstalować, wpisując
`rustup +nightly component add miri`. Nie zmienia to wersji Rusta używanej w
projekcie; jedynie dodaje narzędzie do systemu, z którego możesz skorzystać,
kiedy zechcesz. Miri uruchomisz w projekcie, wpisując `cargo +nightly miri run` lub
`cargo +nightly miri test`.

Aby zobaczyć, jak bardzo może to być pomocne, sprawdźmy, co się stanie, gdy
uruchomimy je na kodzie z listingu 20-7.

```console
{{#include ../listings/ch20-advanced-features/listing-20-07/output.txt}}
```

Miri słusznie ostrzega, że rzutujemy liczbę całkowitą na wskaźnik, co może być
problemem, ale nie potrafi ustalić, czy problem faktycznie występuje, ponieważ
nie wie, skąd pochodzi wskaźnik. Następnie Miri zgłasza błąd w miejscu, w
którym listing 20-7 ma niezdefiniowane zachowanie, ponieważ mamy tam wiszący
wskaźnik. Dzięki Miri wiemy już, że istnieje ryzyko niezdefiniowanego
zachowania, i możemy zastanowić się, jak uczynić kod bezpiecznym. W niektórych
przypadkach Miri potrafi nawet zasugerować, jak naprawić błędy.

Miri nie wychwytuje wszystkiego, co możesz zrobić źle, pisząc niebezpieczny
kod. Jest narzędziem do analizy dynamicznej, więc wychwytuje problemy tylko w
kodzie, który faktycznie zostaje wykonany. Oznacza to, że aby zwiększyć
pewność co do napisanego niebezpiecznego kodu, musisz używać go razem z
dobrymi technikami testowania. Miri nie obejmuje też wszystkich możliwych
sposobów, w jakie kod może być nieprawidłowy (*unsound*).

Innymi słowy: jeśli Miri _wykryje_ problem, wiesz, że jest błąd, ale to, że
Miri _nie wykryje_ błędu, nie oznacza, że problemu nie ma. Mimo to potrafi
wychwycić naprawdę sporo. Spróbuj uruchomić je na pozostałych przykładach
niebezpiecznego kodu w tym rozdziale i zobacz, co zgłosi!

Więcej o Miri dowiesz się z [jego repozytorium na GitHubie][miri].

<!-- Old headings. Do not remove or links may break. -->

<a id="when-to-use-unsafe-code"></a>

### Poprawne używanie niebezpiecznego kodu {#using-unsafe-code-correctly}

Używanie `unsafe`, by skorzystać z jednej z pięciu omówionych właśnie
supermocy, nie jest złe ani nawet źle widziane, ale trudniej jest napisać
poprawny kod `unsafe`, ponieważ kompilator nie może pomóc w zapewnieniu
bezpieczeństwa pamięci. Gdy masz powód, by użyć kodu `unsafe`, możesz to
zrobić, a jawna adnotacja `unsafe` ułatwia namierzenie źródła problemów, gdy
już wystąpią. Za każdym razem, gdy piszesz niebezpieczny kod, możesz użyć
Miri, by zyskać większą pewność, że napisany kod przestrzega reguł Rusta.

Aby znacznie dogłębniej poznać skuteczną pracę z niebezpiecznym Rustem,
przeczytaj oficjalny przewodnik Rusta po `unsafe`, [The Rustonomicon][nomicon].

{{#quiz ../quizzes/ch19-01-unsafe-rust.toml}}

[permission-violations]: ch04-02-references-and-borrowing.html#the-borrow-checker-finds-permission-violations
[ABI]: https://doc.rust-lang.org/reference/items/external-blocks.html#abi
[the-slice-type]: ch04-04-slices.html#the-slice-type
[constants]: ch03-01-variables-and-mutability.html#declaring-constants
[send-and-sync]: ch16-04-extensible-concurrency-sync-and-send.html
[the-slice-type]: ch04-03-slices.html#the-slice-type
[unions]: https://doc.rust-lang.org/reference/items/unions.html
[miri]: https://github.com/rust-lang/miri
[editions]: appendix-05-editions.html
[nightly]: appendix-07-nightly-rust.html
[nomicon]: https://doc.rust-lang.org/nomicon/

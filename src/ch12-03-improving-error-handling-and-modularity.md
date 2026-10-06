## Refaktoryzacja w celu poprawy modułowości i obsługi błędów {#refactoring-to-improve-modularity-and-error-handling}

Aby ulepszyć nasz program, naprawimy cztery problemy związane z jego strukturą
i ze sposobem, w jaki obsługuje potencjalne błędy. Po pierwsze, nasza funkcja
`main` wykonuje teraz dwa zadania: parsuje argumenty i czyta pliki. W miarę
rozwoju programu liczba osobnych zadań obsługiwanych przez funkcję `main`
będzie rosła. Im więcej obowiązków spada na funkcję, tym trudniej zrozumieć jej
działanie, trudniej ją testować i trudniej ją zmieniać, nie psując żadnej z jej
części. Najlepiej rozdzielić funkcjonalność tak, aby każda funkcja odpowiadała
za jedno zadanie.

Ta kwestia wiąże się też z drugim problemem: choć `query` i `file_path` są
zmiennymi konfiguracyjnymi programu, zmienne takie jak `contents` służą do
realizacji jego logiki. Im dłuższa staje się funkcja `main`, tym więcej
zmiennych musimy wprowadzić do zasięgu (*scope*), a im więcej zmiennych jest w
zasięgu, tym trudniej śledzić, do czego służy każda z nich. Najlepiej zgrupować
zmienne konfiguracyjne w jednej strukturze, aby ich przeznaczenie było jasne.

Trzeci problem polega na tym, że użyliśmy `expect`, aby wypisać komunikat o
błędzie, gdy odczyt pliku się nie powiedzie, ale ten komunikat brzmi po prostu
`Should have been able to read the file`. Odczyt pliku może się nie udać na
wiele sposobów: na przykład pliku może brakować albo możemy nie mieć uprawnień
do jego otwarcia. W tej chwili niezależnie od sytuacji wypisalibyśmy ten sam
komunikat o błędzie, który nie dałby użytkownikowi żadnej informacji!

Po czwarte, używamy `expect` do obsługi błędu, a jeśli użytkownik uruchomi nasz
program bez podania wystarczającej liczby argumentów, dostanie od Rusta błąd
`index out of bounds`, który nie wyjaśnia jasno problemu. Najlepiej byłoby,
gdyby cały kod obsługi błędów znajdował się w jednym miejscu – wtedy przyszłe
osoby utrzymujące kod miałyby tylko jedno miejsce do sprawdzenia, gdyby logika
obsługi błędów wymagała zmian. Trzymanie całego kodu obsługi błędów w jednym
miejscu zapewni też, że wypisujemy komunikaty zrozumiałe dla naszych
użytkowników końcowych.

Rozwiążmy te cztery problemy, refaktoryzując nasz projekt.

<!-- Old headings. Do not remove or links may break. -->

<a id="separation-of-concerns-for-binary-projects"></a>

### Rozdzielanie odpowiedzialności w projektach binarnych {#separating-concerns-in-binary-projects}

Problem organizacyjny polegający na zrzucaniu na funkcję `main`
odpowiedzialności za wiele zadań występuje w wielu projektach binarnych.
Dlatego wielu programistów Rusta uważa za przydatne rozdzielanie
odpowiedzialności (*separation of concerns*) w programie binarnym, gdy funkcja
`main` zaczyna się rozrastać. Proces ten składa się z następujących kroków:

- Podziel program na plik _main.rs_ i plik _lib.rs_, a logikę programu przenieś
  do _lib.rs_.
- Dopóki logika parsowania wiersza poleceń jest niewielka, może pozostać w
  funkcji `main`.
- Gdy logika parsowania wiersza poleceń zaczyna się komplikować, wyodrębnij ją
  z funkcji `main` do innych funkcji lub typów.

Po tym procesie w funkcji `main` powinny pozostać jedynie następujące
obowiązki:

- wywołanie logiki parsowania wiersza poleceń z wartościami argumentów;
- przygotowanie pozostałej konfiguracji;
- wywołanie funkcji `run` z _lib.rs_;
- obsłużenie błędu, jeśli `run` zwróci błąd.

Ten wzorzec polega na rozdzieleniu odpowiedzialności: _main.rs_ zajmuje się
uruchomieniem programu, a _lib.rs_ obsługuje całą logikę bieżącego zadania.
Ponieważ funkcji `main` nie da się przetestować bezpośrednio, taka struktura
pozwala przetestować całą logikę programu dzięki przeniesieniu jej poza funkcję
`main`. Kod, który zostanie w funkcji `main`, będzie na tyle krótki, że jego
poprawność da się zweryfikować, czytając go. Przebudujmy nasz program, stosując
się do tego procesu.

#### Wyodrębnianie parsera argumentów {#extracting-the-argument-parser}

Wyodrębnimy funkcjonalność parsowania argumentów do funkcji, którą będzie
wywoływać `main`. Listing 12-5 pokazuje nowy początek funkcji `main`, która
wywołuje nową funkcję `parse_config`; zdefiniujemy ją w _src/main.rs_.

<Listing number="12-5" file-name="src/main.rs" caption="Wyodrębnienie funkcji `parse_config` z `main`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-05/src/main.rs:here}}
```

</Listing>

Nadal zbieramy argumenty wiersza poleceń do wektora (*vector*), ale zamiast w
funkcji `main` przypisywać wartość argumentu o indeksie 1 do zmiennej `query`,
a wartość argumentu o indeksie 2 do zmiennej `file_path`, przekazujemy cały
wektor do funkcji `parse_config`. Funkcja `parse_config` zawiera teraz logikę,
która ustala, który argument trafia do której zmiennej, i przekazuje wartości z
powrotem do `main`. Nadal tworzymy zmienne `query` i `file_path` w `main`, ale
`main` nie odpowiada już za ustalanie, jak argumenty wiersza poleceń odpowiadają
zmiennym.

Ta przeróbka może się wydawać przesadą jak na nasz mały program, ale
refaktoryzujemy małymi, stopniowymi krokami. Po wprowadzeniu tej zmiany uruchom
program ponownie, aby sprawdzić, czy parsowanie argumentów nadal działa. Warto
często sprawdzać postępy, bo pomaga to ustalić przyczynę problemów, gdy się
pojawią.

#### Grupowanie wartości konfiguracyjnych {#grouping-configuration-values}

Możemy zrobić kolejny mały krok, aby jeszcze ulepszyć funkcję `parse_config`.
Obecnie zwracamy krotkę (*tuple*), ale zaraz potem znów rozbijamy ją na
poszczególne części. To znak, że być może nie mamy jeszcze właściwej
abstrakcji.

Kolejną wskazówką, że jest tu pole do poprawy, jest człon `config` w nazwie
`parse_config`, sugerujący, że dwie zwracane wartości są ze sobą powiązane i
obie należą do jednej wartości konfiguracyjnej. Obecnie nie wyrażamy tego
znaczenia w strukturze danych inaczej niż przez zgrupowanie obu wartości w
krotce; zamiast tego umieścimy je w jednej strukturze (*struct*) i nadamy
każdemu z jej pól znaczącą nazwę. Dzięki temu przyszłym osobom utrzymującym ten
kod łatwiej będzie zrozumieć, jak poszczególne wartości są ze sobą powiązane i
do czego służą.

Listing 12-6 pokazuje ulepszenia funkcji `parse_config`.

<Listing number="12-6" file-name="src/main.rs" caption="Refaktoryzacja `parse_config` tak, by zwracała instancję struktury `Config`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-06/src/main.rs:here}}
```

</Listing>

Dodaliśmy strukturę o nazwie `Config` z polami `query` i `file_path`. Sygnatura
`parse_config` wskazuje teraz, że funkcja zwraca wartość `Config`. W ciele
`parse_config`, gdzie wcześniej zwracaliśmy wycinki łańcucha (*string slice*)
odwołujące się do wartości `String` w `args`, teraz definiujemy `Config` tak,
by zawierała wartości `String` będące właścicielami swoich danych. Zmienna
`args` w `main` jest właścicielem wartości argumentów i jedynie pozwala funkcji
`parse_config` je pożyczyć, co oznacza, że naruszylibyśmy zasady pożyczania
(*borrowing*) w Ruście, gdyby `Config` próbowała przejąć własność
(*ownership*) wartości w `args`.

Danymi typu `String` możemy zarządzać na kilka sposobów; najłatwiejszą, choć
nieco nieefektywną drogą jest wywołanie na wartościach metody `clone`. Utworzy
ona pełną kopię danych, której właścicielem będzie instancja `Config`, co
zajmuje więcej czasu i pamięci niż przechowywanie referencji (*reference*) do
danych łańcucha znaków (*string*). Klonowanie danych sprawia jednak, że nasz
kod jest bardzo prosty, bo nie musimy zarządzać czasami życia (*lifetime*)
referencji; w tych okolicznościach rezygnacja z odrobiny wydajności na rzecz
prostoty jest opłacalnym kompromisem.

> ### Kompromisy związane z używaniem `clone` {#the-trade-offs-of-using-clone}
>
> Wielu rustowców (*Rustaceans*) ma skłonność do unikania `clone` przy
> rozwiązywaniu problemów z własnością ze względu na koszt w czasie działania.
> W [rozdziale 13][ch13]<!-- ignore --> nauczysz się w takich sytuacjach
> stosować wydajniejsze metody. Na razie jednak można spokojnie skopiować kilka
> łańcuchów, aby dalej robić postępy, bo te kopie wykonasz tylko raz, a ścieżka
> pliku i szukany łańcuch są bardzo małe. Lepiej mieć działający, choć nieco
> nieefektywny program, niż próbować nadmiernie optymalizować kod przy
> pierwszym podejściu. Z doświadczeniem w Ruście łatwiej będzie od razu sięgać
> po najwydajniejsze rozwiązanie, ale na razie wywołanie `clone` jest
> całkowicie w porządku.

Zaktualizowaliśmy `main` tak, by umieszczała instancję `Config` zwróconą przez
`parse_config` w zmiennej o nazwie `config`, a kod, który wcześniej używał
osobnych zmiennych `query` i `file_path`, korzysta teraz zamiast nich z pól
struktury `Config`.

Teraz nasz kod wyraźniej przekazuje, że `query` i `file_path` są ze sobą
powiązane i że służą do konfigurowania działania programu. Każdy kod, który
używa tych wartości, wie, że znajdzie je w instancji `config`, w polach
nazwanych zgodnie z ich przeznaczeniem.

#### Tworzenie konstruktora dla `Config` {#creating-a-constructor-for-config}

Do tej pory wyodrębniliśmy z `main` logikę odpowiedzialną za parsowanie
argumentów wiersza poleceń i umieściliśmy ją w funkcji `parse_config`. Dzięki
temu zobaczyliśmy, że wartości `query` i `file_path` są powiązane i że ten
związek powinien być wyrażony w kodzie. Następnie dodaliśmy strukturę `Config`,
aby nazwać wspólne przeznaczenie `query` i `file_path` i móc zwracać nazwy
wartości jako nazwy pól struktury z funkcji `parse_config`.

Skoro więc zadaniem funkcji `parse_config` jest tworzenie instancji `Config`,
możemy zmienić `parse_config` ze zwykłej funkcji w funkcję o nazwie `new`
powiązaną ze strukturą `Config`. Ta zmiana uczyni kod bardziej idiomatycznym.
Instancje typów z biblioteki standardowej, takich jak `String`, możemy tworzyć,
wywołując `String::new`. Podobnie, zamieniając `parse_config` w funkcję `new`
powiązaną z `Config`, będziemy mogli tworzyć instancje `Config`, wywołując
`Config::new`. Listing 12-7 pokazuje zmiany, które musimy wprowadzić.

<Listing number="12-7" file-name="src/main.rs" caption="Zamiana `parse_config` w `Config::new`">

```rust,should_panic,noplayground
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-07/src/main.rs:here}}
```

</Listing>

Zaktualizowaliśmy `main` w miejscu, w którym wywoływaliśmy `parse_config`, tak
by zamiast tego wywoływała `Config::new`. Zmieniliśmy nazwę `parse_config` na
`new` i przenieśliśmy ją do bloku `impl`, który wiąże funkcję `new` z `Config`.
Spróbuj ponownie skompilować ten kod, aby upewnić się, że działa.

### Poprawianie obsługi błędów {#fixing-the-error-handling}

Teraz zajmiemy się poprawieniem obsługi błędów. Przypomnij sobie, że próba
dostępu do wartości w wektorze `args` pod indeksem 1 lub 2 spowoduje panikę
(*panic*) programu, jeśli wektor zawiera mniej niż trzy elementy. Spróbuj
uruchomić program bez żadnych argumentów; wynik będzie wyglądał tak:

```console
{{#include ../listings/ch12-an-io-project/listing-12-07/output.txt}}
```

Linia `index out of bounds: the len is 1 but the index is 1` to komunikat o
błędzie przeznaczony dla programistów. Nie pomoże on naszym użytkownikom
końcowym zrozumieć, co powinni zrobić zamiast tego. Naprawmy to teraz.

#### Ulepszanie komunikatu o błędzie {#improving-the-error-message}

W listingu 12-8 dodajemy w funkcji `new` sprawdzenie, które przed dostępem do
indeksów 1 i 2 zweryfikuje, czy wycinek (*slice*) jest wystarczająco długi.
Jeśli nie jest, program spanikuje i wyświetli lepszy komunikat o błędzie.

<Listing number="12-8" file-name="src/main.rs" caption="Dodanie sprawdzenia liczby argumentów">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-08/src/main.rs:here}}
```

</Listing>

Ten kod przypomina [funkcję `Guess::new`, którą napisaliśmy w listingu 9-13][ch9-custom-types]<!-- ignore -->,
gdzie wywoływaliśmy `panic!`, gdy argument `value` wykraczał poza zakres
poprawnych wartości. Tym razem zamiast sprawdzać zakres wartości, sprawdzamy,
czy długość `args` wynosi co najmniej `3`, a reszta funkcji może działać przy
założeniu, że ten warunek jest spełniony. Jeśli `args` ma mniej niż trzy
elementy, warunek będzie miał wartość `true` i wywołamy makro `panic!`, aby
natychmiast zakończyć program.

Mając w `new` tych kilka dodatkowych wierszy kodu, uruchommy program ponownie
bez żadnych argumentów, aby zobaczyć, jak teraz wygląda błąd:

```console
{{#include ../listings/ch12-an-io-project/listing-12-08/output.txt}}
```

Ten wynik jest lepszy: mamy teraz rozsądny komunikat o błędzie. Mamy jednak
również zbędne informacje, których nie chcemy pokazywać użytkownikom. Być może
technika z listingu 9-13 nie jest tu najlepsza: wywołanie `panic!` bardziej
pasuje do problemu programistycznego niż do problemu z użyciem programu,
[jak omówiliśmy w rozdziale 9][ch9-error-guidelines]<!-- ignore -->. Zamiast
tego użyjemy drugiej techniki poznanej w rozdziale 9 –
[zwracania `Result`][ch9-result]<!-- ignore -->, który oznacza albo sukces,
albo błąd.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-a-result-from-new-instead-of-calling-panic"></a>

#### Zwracanie `Result` zamiast wywoływania `panic!` {#returning-a-result-instead-of-calling-panic}

Zamiast tego możemy zwrócić wartość `Result`, która w razie powodzenia będzie
zawierać instancję `Config`, a w razie błędu opisze problem. Zmienimy też nazwę
funkcji z `new` na `build`, bo wielu programistów oczekuje, że funkcje `new`
nigdy nie zawodzą. Gdy `Config::build` komunikuje się z `main`, możemy użyć
typu `Result`, aby zasygnalizować, że wystąpił problem. Następnie możemy
zmienić `main` tak, by zamieniała wariant `Err` w bardziej praktyczny dla
użytkowników błąd, bez otaczającego tekstu o `thread 'main'` i
`RUST_BACKTRACE`, który pojawia się przy wywołaniu `panic!`.

Listing 12-9 pokazuje zmiany, które musimy wprowadzić w wartości zwracanej
funkcji, którą teraz nazywamy `Config::build`, oraz w jej ciele, aby zwracała
`Result`. Zauważ, że ten kod się nie skompiluje, dopóki nie zaktualizujemy
również `main`, co zrobimy w następnym listingu.

<Listing number="12-9" file-name="src/main.rs" caption="Zwracanie `Result` z `Config::build`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-09/src/main.rs:here}}
```

</Listing>

Nasza funkcja `build` zwraca `Result` z instancją `Config` w razie powodzenia
i literałem łańcuchowym w razie błędu. Nasze wartości błędów będą zawsze
literałami łańcuchowymi o czasie życia `'static`.

W ciele funkcji wprowadziliśmy dwie zmiany: zamiast wywoływać `panic!`, gdy
użytkownik nie przekaże wystarczającej liczby argumentów, zwracamy teraz
wartość `Err`, a zwracaną wartość `Config` opakowaliśmy w `Ok`. Dzięki tym
zmianom funkcja jest zgodna ze swoją nową sygnaturą typu.

Zwrócenie wartości `Err` z `Config::build` pozwala funkcji `main` obsłużyć
wartość `Result` zwróconą z funkcji `build` i w razie błędu zakończyć proces w
czystszy sposób.

<!-- Old headings. Do not remove or links may break. -->

<a id="calling-confignew-and-handling-errors"></a>

#### Wywoływanie `Config::build` i obsługa błędów {#calling-configbuild-and-handling-errors}

Aby obsłużyć przypadek błędu i wypisać przyjazny dla użytkownika komunikat,
musimy zaktualizować `main` tak, by obsługiwała `Result` zwracany przez
`Config::build`, jak pokazano w listingu 12-10. Zdejmiemy też z `panic!`
odpowiedzialność za zakończenie narzędzia wiersza poleceń z niezerowym kodem
błędu i zaimplementujemy to samodzielnie. Niezerowy kod wyjścia to konwencja
sygnalizująca procesowi, który wywołał nasz program, że program zakończył się
błędem.

<Listing number="12-10" file-name="src/main.rs" caption="Zakończenie z kodem błędu, jeśli zbudowanie `Config` się nie powiedzie">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-10/src/main.rs:here}}
```

</Listing>

W tym listingu użyliśmy metody, której jeszcze dokładnie nie omówiliśmy:
`unwrap_or_else`, zdefiniowanej w bibliotece standardowej dla `Result<T, E>`.
Użycie `unwrap_or_else` pozwala nam zdefiniować własną obsługę błędów,
niekorzystającą z `panic!`. Jeśli `Result` jest wartością `Ok`, ta metoda
zachowuje się podobnie do `unwrap`: zwraca wewnętrzną wartość opakowaną przez
`Ok`. Jeśli jednak wartość jest wartością `Err`, metoda wywołuje kod w
domknięciu (*closure*), czyli anonimowej funkcji, którą definiujemy i
przekazujemy jako argument do `unwrap_or_else`. Domknięcia omówimy dokładniej w
[rozdziale 13][ch13]<!-- ignore -->. Na razie wystarczy wiedzieć, że
`unwrap_or_else` przekaże wewnętrzną wartość `Err` – w tym przypadku statyczny
łańcuch `"not enough arguments"`, który dodaliśmy w listingu 12-9 – do naszego
domknięcia w argumencie `err`, widocznym między pionowymi kreskami. Kod w
domknięciu może następnie użyć wartości `err` podczas działania.

Dodaliśmy nowy wiersz `use`, aby wprowadzić do zasięgu `process` z biblioteki
standardowej. Kod w domknięciu, który zostanie uruchomiony w razie błędu, ma
tylko dwa wiersze: wypisujemy wartość `err`, a następnie wywołujemy
`process::exit`. Funkcja `process::exit` natychmiast zatrzyma program i zwróci
liczbę przekazaną jako kod wyjścia. Przypomina to obsługę opartą na
`panic!`, której użyliśmy w listingu 12-8, ale nie dostajemy już całego
dodatkowego wyjścia. Wypróbujmy to:

```console
{{#include ../listings/ch12-an-io-project/listing-12-10/output.txt}}
```

Świetnie! Ten wynik jest dużo przyjaźniejszy dla naszych użytkowników.

<!-- Old headings. Do not remove or links may break. -->

<a id="extracting-logic-from-the-main-function"></a>

### Wyodrębnianie logiki z `main` {#extracting-logic-from-main}

Skoro skończyliśmy refaktoryzować parsowanie konfiguracji, zajmijmy się logiką
programu. Jak zapowiedzieliśmy w podrozdziale [„Rozdzielanie odpowiedzialności w projektach binarnych”](#separation-of-concerns-for-binary-projects)<!-- ignore -->,
wyodrębnimy funkcję o nazwie `run`, która będzie zawierać całą logikę obecnie
znajdującą się w funkcji `main`, niezwiązaną z przygotowaniem konfiguracji ani
z obsługą błędów. Gdy skończymy, funkcja `main` będzie zwięzła i łatwa do
zweryfikowania na oko, a dla całej pozostałej logiki będziemy mogli napisać
testy.

Listing 12-11 pokazuje małe, stopniowe ulepszenie polegające na wyodrębnieniu
funkcji `run`.

<Listing number="12-11" file-name="src/main.rs" caption="Wyodrębnienie funkcji `run` zawierającej resztę logiki programu">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-11/src/main.rs:here}}
```

</Listing>

Funkcja `run` zawiera teraz całą pozostałą logikę z `main`, począwszy od
odczytu pliku. Funkcja `run` przyjmuje instancję `Config` jako argument.

<!-- Old headings. Do not remove or links may break. -->

<a id="returning-errors-from-the-run-function"></a>

#### Zwracanie błędów z `run` {#returning-errors-from-run}

Gdy pozostała logika programu jest już wydzielona do funkcji `run`, możemy
ulepszyć obsługę błędów, tak jak zrobiliśmy to z `Config::build` w listingu
12-9. Zamiast pozwalać programowi panikować przez wywołanie `expect`, funkcja
`run` zwróci `Result<T, E>`, gdy coś pójdzie nie tak. Pozwoli nam to jeszcze
bardziej skupić logikę obsługi błędów w `main` w sposób przyjazny dla
użytkownika. Listing 12-12 pokazuje zmiany, które musimy wprowadzić w sygnaturze
i ciele `run`.

<Listing number="12-12" file-name="src/main.rs" caption="Zmiana funkcji `run` tak, by zwracała `Result`">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-12/src/main.rs:here}}
```

</Listing>

Wprowadziliśmy tu trzy istotne zmiany. Po pierwsze, zmieniliśmy typ zwracany
funkcji `run` na `Result<(), Box<dyn Error>>`. Wcześniej ta funkcja zwracała
typ jednostkowy (*unit type*), `()`, i zachowujemy go jako wartość zwracaną w
przypadku `Ok`.

Jako typu błędu użyliśmy obiektu traitu (*trait object*) `Box<dyn Error>` (a
`std::error::Error` wprowadziliśmy do zasięgu instrukcją (*statement*) `use` na
początku pliku). Obiekty traitów omówimy w
[rozdziale 18][ch18]<!-- ignore -->. Na razie wystarczy wiedzieć, że
`Box<dyn Error>` oznacza, że funkcja zwróci typ implementujący *trait* (cecha
typu, zbliżona do interfejsu) `Error`, ale nie musimy określać, jakiego
konkretnie typu będzie zwracana wartość. Daje nam to elastyczność zwracania
wartości błędów, które w różnych przypadkach mogą być różnych typów. Słowo
kluczowe (*keyword*) `dyn` to skrót od _dynamic_ (dynamiczny).

Po drugie, usunęliśmy wywołanie `expect` na rzecz operatora `?`, o którym
mówiliśmy w [rozdziale 9][ch9-question-mark]<!-- ignore -->. Zamiast wywoływać
`panic!` w razie błędu, `?` zwróci wartość błędu z bieżącej funkcji, aby
obsłużył ją kod wywołujący.

Po trzecie, funkcja `run` zwraca teraz wartość `Ok` w razie powodzenia. W
sygnaturze zadeklarowaliśmy typ sukcesu funkcji `run` jako `()`, co oznacza, że
musimy opakować wartość typu jednostkowego w wartość `Ok`. Ta składnia `Ok(())`
może na początku wyglądać nieco dziwnie. Jednak takie użycie `()` to
idiomatyczny sposób zaznaczenia, że wywołujemy `run` wyłącznie dla jej efektów
ubocznych – nie zwraca ona wartości, której potrzebujemy.

Gdy uruchomisz ten kod, skompiluje się, ale wyświetli ostrzeżenie:

```console
{{#include ../listings/ch12-an-io-project/listing-12-12/output.txt}}
```

Rust mówi nam, że nasz kod zignorował wartość `Result`, a ta wartość `Result`
może oznaczać, że wystąpił błąd. My jednak nie sprawdzamy, czy błąd wystąpił, a
kompilator przypomina nam, że prawdopodobnie chcieliśmy mieć tu jakiś kod
obsługi błędów! Naprawmy teraz ten problem.

#### Obsługa błędów zwracanych z `run` w `main` {#handling-errors-returned-from-run-in-main}

Będziemy sprawdzać błędy i obsługiwać je techniką podobną do tej, której
użyliśmy z `Config::build` w listingu 12-10, ale z niewielką różnicą:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/no-listing-01-handling-errors-in-main/src/main.rs:here}}
```

Używamy `if let` zamiast `unwrap_or_else`, aby sprawdzić, czy `run` zwraca
wartość `Err`, i jeśli tak, wywołać `process::exit(1)`. Funkcja `run` nie
zwraca wartości, którą chcielibyśmy rozpakować za pomocą `unwrap`, tak jak
`Config::build` zwraca instancję `Config`. Ponieważ w razie powodzenia `run`
zwraca `()`, interesuje nas jedynie wykrycie błędu, więc nie potrzebujemy
`unwrap_or_else` do zwrócenia rozpakowanej wartości, która byłaby po prostu
`()`.

Ciała `if let` i funkcji `unwrap_or_else` są w obu przypadkach takie same:
wypisujemy błąd i kończymy program.

### Wydzielanie kodu do crate’a bibliotecznego {#splitting-code-into-a-library-crate}

Nasz projekt `minigrep` jak dotąd wygląda dobrze! Teraz podzielimy plik
_src/main.rs_ i umieścimy część kodu w pliku _src/lib.rs_. Dzięki temu
będziemy mogli testować kod, a plik _src/main.rs_ będzie miał mniej obowiązków.

Zdefiniujmy kod odpowiedzialny za przeszukiwanie tekstu w _src/lib.rs_ zamiast
w _src/main.rs_; pozwoli to nam (lub komukolwiek innemu, kto używa naszej
biblioteki `minigrep`) wywoływać funkcję wyszukującą w większej liczbie
kontekstów niż tylko w naszym pliku binarnym `minigrep`.

Najpierw zdefiniujmy w _src/lib.rs_ sygnaturę funkcji `search`, jak pokazano w
listingu 12-13, z ciałem wywołującym makro `unimplemented!`. Sygnaturę
wyjaśnimy dokładniej, gdy będziemy uzupełniać implementację.

<Listing number="12-13" file-name="src/lib.rs" caption="Definicja funkcji `search` w *src/lib.rs*">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-13/src/lib.rs}}
```

</Listing>

Użyliśmy słowa kluczowego `pub` w definicji funkcji, aby oznaczyć `search` jako
część publicznego API naszej biblioteki. Mamy teraz biblioteczny *crate*
(jednostka kompilacji w Ruście), którego możemy używać z naszego crate’a
binarnego i który możemy testować!

Teraz musimy wprowadzić kod zdefiniowany w _src/lib.rs_ do zasięgu crate’a
binarnego w _src/main.rs_ i go wywołać, jak pokazano w listingu 12-14.

<Listing number="12-14" file-name="src/main.rs" caption="Użycie funkcji `search` z crate’a bibliotecznego `minigrep` w *src/main.rs*">

```rust,ignore
{{#rustdoc_include ../listings/ch12-an-io-project/listing-12-14/src/main.rs:here}}
```

</Listing>

Dodajemy wiersz `use minigrep::search`, aby wprowadzić funkcję `search` z
crate’a bibliotecznego do zasięgu crate’a binarnego. Następnie w funkcji `run`
zamiast wypisywać zawartość pliku, wywołujemy funkcję `search` i przekazujemy
jej jako argumenty wartość `config.query` oraz `contents`. Potem `run` użyje
pętli `for`, aby wypisać każdy wiersz zwrócony z `search`, który pasuje do
zapytania. To także dobry moment, by usunąć z funkcji `main` wywołania
`println!`, które wyświetlały zapytanie i ścieżkę pliku, tak aby program
wypisywał tylko wyniki wyszukiwania (jeśli nie wystąpią błędy).

Zauważ, że funkcja wyszukująca zbierze wszystkie wyniki do zwracanego wektora,
zanim cokolwiek zostanie wypisane. Przy przeszukiwaniu dużych plików taka
implementacja może wolno wyświetlać wyniki, bo nie są one wypisywane w miarę
znajdowania; w rozdziale 13 omówimy możliwy sposób naprawienia tego za pomocą
iteratorów.

Uff! To było sporo pracy, ale przygotowaliśmy sobie grunt pod przyszły sukces.
Teraz dużo łatwiej obsługiwać błędy, a kod stał się bardziej modułowy. Od tej
pory niemal cała nasza praca będzie się odbywać w _src/lib.rs_.

Wykorzystajmy tę nowo zdobytą modułowość i zróbmy coś, co ze starym kodem byłoby
trudne, a z nowym jest łatwe: napiszemy kilka testów!

[ch13]: ch13-00-functional-features.html
[ch9-custom-types]: ch09-03-to-panic-or-not-to-panic.html#creating-custom-types-for-validation
[ch9-error-guidelines]: ch09-03-to-panic-or-not-to-panic.html#guidelines-for-error-handling
[ch9-result]: ch09-02-recoverable-errors-with-result.html
[ch18]: ch18-00-oop.html
[ch9-question-mark]: ch09-02-recoverable-errors-with-result.html#a-shortcut-for-propagating-errors-the--operator

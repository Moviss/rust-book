## `RefCell<T>` i wzorzec wewnętrznej mutowalności {#refcellt-and-the-interior-mutability-pattern}

_Wewnętrzna mutowalność_ (*interior mutability*) to wzorzec projektowy w
Ruście, który pozwala modyfikować dane nawet wtedy, gdy istnieją do nich
niemutowalne referencje (*reference*); zwykle reguły pożyczania (*borrowing*)
na to nie pozwalają. Aby zmodyfikować dane, wzorzec ten używa wewnątrz
struktury danych kodu `unsafe`, który nagina zwykłe reguły Rusta dotyczące
modyfikowania (*mutation*) i pożyczania. Niebezpieczny kod sygnalizuje
kompilatorowi, że sprawdzamy reguły ręcznie, zamiast polegać na tym, że
kompilator sprawdzi je za nas; niebezpieczny kod omówimy dokładniej w
rozdziale 20.

Typów korzystających ze wzorca wewnętrznej mutowalności możemy używać tylko
wtedy, gdy jesteśmy w stanie zapewnić, że reguły pożyczania będą przestrzegane
w czasie działania, mimo że kompilator nie może tego zagwarantować. Użyty kod
`unsafe` zostaje wtedy opakowany w bezpieczne API, a typ zewnętrzny nadal jest
niemutowalny.

Zbadajmy tę koncepcję, przyglądając się typowi `RefCell<T>`, który realizuje
wzorzec wewnętrznej mutowalności.

<!-- Old headings. Do not remove or links may break. -->

<a id="enforcing-borrowing-rules-at-runtime-with-refcellt"></a>

### Egzekwowanie reguł pożyczania w czasie działania {#enforcing-borrowing-rules-at-runtime}

W przeciwieństwie do `Rc<T>` typ `RefCell<T>` reprezentuje pojedynczą własność
(*ownership*) przechowywanych danych. Czym więc `RefCell<T>` różni się od typu
takiego jak `Box<T>`? Przypomnij sobie reguły pożyczania poznane w rozdziale 4:

- W dowolnym momencie możesz mieć _albo_ jedną mutowalną (*mutable*)
  referencję, albo dowolną liczbę niemutowalnych referencji (ale nie oba
  rodzaje naraz).
- Referencje zawsze muszą być prawidłowe.

W przypadku referencji i `Box<T>` niezmienniki reguł pożyczania są egzekwowane
w czasie kompilacji (*compile-time*). W przypadku `RefCell<T>` niezmienniki te
są egzekwowane _w czasie działania_. Jeśli złamiesz te reguły, używając
referencji, dostaniesz błąd kompilatora. Jeśli złamiesz je, używając
`RefCell<T>`, program spanikuje i zakończy działanie.

Zaletą sprawdzania reguł pożyczania w czasie kompilacji jest to, że błędy
zostaną wychwycone wcześniej w procesie tworzenia oprogramowania, a wydajność w
czasie działania nie ucierpi, ponieważ cała analiza jest wykonywana
zawczasu. Z tych powodów sprawdzanie reguł pożyczania w czasie kompilacji jest
najlepszym wyborem w większości przypadków i dlatego jest to domyślne
zachowanie Rusta.

Zaletą sprawdzania reguł pożyczania w czasie działania jest natomiast to, że
dozwolone stają się pewne scenariusze bezpieczne dla pamięci, które
zostałyby odrzucone przez sprawdzenia w czasie kompilacji. Analiza statyczna, taka jak ta
wykonywana przez kompilator Rusta, jest z natury zachowawcza. Niektórych
właściwości kodu nie da się wykryć, analizując kod: najsłynniejszym przykładem
jest problem stopu, który wykracza poza zakres tej książki, ale jest ciekawym
tematem do samodzielnego zgłębienia.

Ponieważ część analiz jest niemożliwa, kompilator Rusta, jeśli nie ma
pewności, że kod przestrzega reguł własności, może odrzucić poprawny program;
właśnie w tym sensie jest zachowawczy. Gdyby Rust akceptował niepoprawne
programy, użytkownicy nie mogliby ufać gwarancjom, które daje. Jeśli jednak
Rust odrzuci poprawny program, będzie to niedogodność dla programisty, ale nie
może wydarzyć się nic katastrofalnego. Typ `RefCell<T>` przydaje się, gdy masz
pewność, że twój kod przestrzega reguł pożyczania, ale kompilator nie jest w
stanie tego zrozumieć i zagwarantować.

Podobnie jak `Rc<T>`, `RefCell<T>` jest przeznaczony wyłącznie do scenariuszy
jednowątkowych i zgłosi błąd w czasie kompilacji, jeśli spróbujesz użyć go w
kontekście wielowątkowym. O tym, jak uzyskać funkcjonalność `RefCell<T>` w
programie wielowątkowym, porozmawiamy w rozdziale 16.

Oto podsumowanie powodów, dla których warto wybrać `Box<T>`, `Rc<T>` lub
`RefCell<T>`:

- `Rc<T>` pozwala, by te same dane miały wielu właścicieli; `Box<T>` i
  `RefCell<T>` mają jednego właściciela.
- `Box<T>` pozwala na niemutowalne lub mutowalne pożyczenia sprawdzane w
  czasie kompilacji; `Rc<T>` pozwala wyłącznie na niemutowalne pożyczenia
  sprawdzane w czasie kompilacji; `RefCell<T>` pozwala na niemutowalne lub
  mutowalne pożyczenia sprawdzane w czasie działania.
- Ponieważ `RefCell<T>` pozwala na mutowalne pożyczenia sprawdzane w czasie
  działania, możesz modyfikować wartość wewnątrz `RefCell<T>`, nawet gdy sam
  `RefCell<T>` jest niemutowalny.

Modyfikowanie wartości wewnątrz niemutowalnej wartości to właśnie wzorzec
wewnętrznej mutowalności. Przyjrzyjmy się sytuacji, w której wewnętrzna
mutowalność jest przydatna, i sprawdźmy, jak to w ogóle jest możliwe.

<!-- Old headings. Do not remove or links may break. -->

<a id="interior-mutability-a-mutable-borrow-to-an-immutable-value"></a>

### Korzystanie z wewnętrznej mutowalności {#using-interior-mutability}

Z reguł pożyczania wynika, że gdy masz niemutowalną wartość, nie możesz
pożyczyć jej mutowalnie. Na przykład ten kod się nie skompiluje:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/src/main.rs}}
```

Gdyby spróbować skompilować ten kod, pojawiłby się następujący błąd:

```console
{{#include ../listings/ch15-smart-pointers/no-listing-01-cant-borrow-immutable-as-mutable/output.txt}}
```

Zdarzają się jednak sytuacje, w których przydałoby się, aby wartość mogła
modyfikować samą siebie w swoich metodach, a jednocześnie dla pozostałego kodu
wyglądała na niemutowalną. Kod spoza metod tej wartości nie mógłby jej
modyfikować. Użycie `RefCell<T>` to jeden ze sposobów na uzyskanie wewnętrznej
mutowalności, ale `RefCell<T>` nie omija reguł pożyczania całkowicie:
*borrow checker* (mechanizm sprawdzania pożyczeń) w kompilatorze pozwala na tę
wewnętrzną mutowalność, a reguły pożyczania są zamiast tego sprawdzane w czasie
działania. Jeśli je naruszysz, zamiast błędu kompilatora dostaniesz `panic!`.

Przeanalizujmy praktyczny przykład, w którym możemy użyć `RefCell<T>` do
zmodyfikowania niemutowalnej wartości, i zobaczmy, dlaczego jest to przydatne.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-use-case-for-interior-mutability-mock-objects"></a>

#### Testowanie z użyciem atrap {#testing-with-mock-objects}

Czasami podczas testowania programista używa jednego typu w miejscu innego, aby
obserwować określone zachowanie i sprawdzić asercjami, że jest ono
zaimplementowane poprawnie. Taki typ zastępczy nazywa się _dublerem testowym_
(*test double*). Pomyśl o nim jak o dublerze w filmie, czyli osobie, która
zastępuje aktora w wyjątkowo trudnej scenie. Dublery testowe zastępują inne
typy podczas uruchamiania testów. _Atrapy_ (*mock objects*) to szczególny
rodzaj dublerów testowych, które rejestrują, co dzieje się w trakcie testu,
dzięki czemu możesz sprawdzić asercjami, że zostały wykonane właściwe
działania.

Rust nie ma obiektów w takim sensie, w jakim mają je inne języki, a jego
biblioteka standardowa, w przeciwieństwie do niektórych innych języków, nie
zawiera wbudowanej funkcjonalności atrap. Z całą pewnością możesz jednak
utworzyć strukturę (*struct*), która będzie spełniać te same zadania co
atrapa.

Oto scenariusz, który przetestujemy: utworzymy bibliotekę, która śledzi
wartość względem wartości maksymalnej i wysyła komunikaty w zależności od tego,
jak blisko maksimum jest bieżąca wartość. Taka biblioteka mogłaby posłużyć na
przykład do śledzenia limitu wywołań API, jakie może wykonać użytkownik.

Nasza biblioteka będzie zapewniać jedynie funkcjonalność śledzenia, jak blisko
maksimum jest wartość, oraz określania, jakie komunikaty i kiedy powinny zostać
wysłane. Od aplikacji korzystających z naszej biblioteki oczekuje się, że
dostarczą mechanizm wysyłania komunikatów: aplikacja może wyświetlić komunikat
bezpośrednio użytkownikowi, wysłać e-mail, wysłać SMS-a albo zrobić coś
innego. Biblioteka nie musi znać tego szczegółu. Potrzebuje jedynie czegoś, co
implementuje udostępniony przez nas *trait* (cechę typu, zbliżoną do
interfejsu) o nazwie `Messenger`. Listing 15-20 przedstawia kod biblioteki.

<Listing number="15-20" file-name="src/lib.rs" caption="Biblioteka śledząca, jak blisko wartości maksymalnej jest dana wartość, i ostrzegająca, gdy wartość osiągnie określone poziomy">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-20/src/lib.rs}}
```

</Listing>

Ważne w tym kodzie jest to, że trait `Messenger` ma jedną metodę o nazwie
`send`, która przyjmuje niemutowalną referencję do `self` oraz tekst
komunikatu. Ten trait stanowi interfejs, który nasza atrapa musi
zaimplementować, aby można jej było używać tak samo jak prawdziwego obiektu.
Druga ważna rzecz to fakt, że chcemy przetestować zachowanie metody
`set_value` typu `LimitTracker`. Możemy zmieniać to, co przekazujemy jako
parametr `value`, ale `set_value` nie zwraca niczego, co moglibyśmy sprawdzić
asercjami. Chcemy móc stwierdzić, że jeśli utworzymy `LimitTracker` z czymś,
co implementuje trait `Messenger`, i z określoną wartością `max`, to obiekt
wysyłający komunikaty otrzyma polecenie wysłania odpowiednich komunikatów, gdy
przekażemy różne liczby jako `value`.

Potrzebujemy atrapy, która po wywołaniu `send`, zamiast wysyłać e-mail czy
SMS-a, będzie jedynie zapamiętywać komunikaty, które kazano jej wysłać. Możemy
utworzyć nową instancję atrapy, utworzyć `LimitTracker` korzystający z tej
atrapy, wywołać metodę `set_value` na `LimitTracker`, a następnie sprawdzić,
czy atrapa ma oczekiwane komunikaty. Listing 15-21 przedstawia próbę
zaimplementowania takiej atrapy, na którą jednak nie pozwala borrow checker.

<Listing number="15-21" file-name="src/lib.rs" caption="Próba zaimplementowania `MockMessenger`, na którą nie pozwala borrow checker">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-21/src/lib.rs:here}}
```

</Listing>

Ten kod testowy definiuje strukturę `MockMessenger` z polem `sent_messages`
typu `Vec` wartości `String`, w którym zapisywane są komunikaty, które kazano
jej wysłać. Definiujemy też funkcję powiązaną (*associated function*) `new`,
aby wygodnie tworzyć nowe wartości `MockMessenger`, które na początku mają
pustą listę komunikatów. Następnie implementujemy trait `Messenger` dla `MockMessenger`,
aby móc przekazać `MockMessenger` do `LimitTracker`. W definicji metody `send`
bierzemy komunikat przekazany jako parametr i zapisujemy go w liście
`sent_messages` struktury `MockMessenger`.

W teście sprawdzamy, co się dzieje, gdy `LimitTracker` dostaje polecenie
ustawienia `value` na coś, co przekracza 75 procent wartości `max`. Najpierw
tworzymy nowy `MockMessenger`, który na początku ma pustą listę komunikatów.
Następnie tworzymy nowy `LimitTracker` i przekazujemy mu referencję do nowego
`MockMessenger` oraz wartość `max` równą `100`. Wywołujemy metodę `set_value`
na `LimitTracker` z wartością `80`, która przekracza 75 procent ze 100. Na
koniec sprawdzamy asercją, że lista komunikatów, którą prowadzi
`MockMessenger`, powinna teraz zawierać jeden komunikat.

Z tym testem jest jednak pewien problem, co widać tutaj:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-21/output.txt}}
```

Nie możemy zmodyfikować `MockMessenger`, aby zapamiętywał komunikaty, ponieważ
metoda `send` przyjmuje niemutowalną referencję do `self`. Nie możemy też
skorzystać z sugestii z komunikatu o błędzie, by użyć `&mut self` zarówno w
metodzie w bloku `impl`, jak i w definicji traitu. Nie chcemy zmieniać traitu
`Messenger` wyłącznie na potrzeby testów. Zamiast tego musimy znaleźć sposób,
aby nasz kod testowy działał poprawnie z dotychczasowym rozwiązaniem.

To sytuacja, w której wewnętrzna mutowalność może pomóc! Umieścimy
`sent_messages` w `RefCell<T>`, dzięki czemu metoda `send` będzie mogła
modyfikować `sent_messages`, aby zapisywać komunikaty, które widzieliśmy.
Listing 15-22 pokazuje, jak to wygląda.

<Listing number="15-22" file-name="src/lib.rs" caption="Użycie `RefCell<T>` do modyfikowania wartości wewnętrznej, podczas gdy wartość zewnętrzna jest uznawana za niemutowalną">

```rust,noplayground
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-22/src/lib.rs:here}}
```

</Listing>

Pole `sent_messages` ma teraz typ `RefCell<Vec<String>>` zamiast
`Vec<String>`. W funkcji `new` tworzymy nową instancję `RefCell<Vec<String>>`
opakowującą pusty wektor (*vector*).

W implementacji metody `send` pierwszy parametr nadal jest niemutowalnym
pożyczeniem `self`, co jest zgodne z definicją traitu. Wywołujemy
`borrow_mut` na `RefCell<Vec<String>>` w `self.sent_messages`, aby uzyskać
mutowalną referencję do wartości wewnątrz `RefCell<Vec<String>>`, czyli do
wektora. Następnie możemy wywołać `push` na mutowalnej referencji do wektora,
aby zapamiętać komunikaty wysłane podczas testu.

Ostatnia zmiana, którą musimy wprowadzić, dotyczy asercji: aby sprawdzić, ile
elementów jest w wewnętrznym wektorze, wywołujemy `borrow` na
`RefCell<Vec<String>>`, aby uzyskać niemutowalną referencję do wektora.

Skoro już wiesz, jak używać `RefCell<T>`, zobaczmy, jak to działa!

<!-- Old headings. Do not remove or links may break. -->

<a id="keeping-track-of-borrows-at-runtime-with-refcellt"></a>

#### Śledzenie pożyczeń w czasie działania {#tracking-borrows-at-runtime}

Do tworzenia niemutowalnych i mutowalnych referencji używamy odpowiednio
składni `&` i `&mut`. W przypadku `RefCell<T>` używamy metod `borrow` i
`borrow_mut`, które należą do bezpiecznego API typu `RefCell<T>`. Metoda
`borrow` zwraca inteligentny wskaźnik (*smart pointer*) typu `Ref<T>`, a
`borrow_mut` zwraca inteligentny wskaźnik typu `RefMut<T>`. Oba typy
implementują `Deref`, więc możemy traktować je jak zwykłe referencje.

`RefCell<T>` śledzi, ile inteligentnych wskaźników `Ref<T>` i `RefMut<T>` jest
w danej chwili aktywnych. Za każdym razem, gdy wywołujemy `borrow`,
`RefCell<T>` zwiększa licznik aktywnych niemutowalnych pożyczeń. Gdy wartość
`Ref<T>` wychodzi poza zasięg (*scope*), licznik niemutowalnych pożyczeń zmniejsza
się o 1. Podobnie jak reguły pożyczania sprawdzane w czasie kompilacji,
`RefCell<T>` pozwala nam w dowolnym momencie mieć wiele niemutowalnych
pożyczeń albo jedno mutowalne.

Jeśli spróbujemy naruszyć te reguły, to zamiast błędu kompilatora, jaki
dostalibyśmy w przypadku referencji, implementacja `RefCell<T>` spanikuje w
czasie działania. Listing 15-23 przedstawia zmodyfikowaną implementację `send`
z listingu 15-22. Celowo próbujemy utworzyć dwa mutowalne pożyczenia aktywne w
tym samym zasięgu, aby pokazać, że `RefCell<T>` nie pozwala nam na to w czasie
działania.

<Listing number="15-23" file-name="src/lib.rs" caption="Tworzenie dwóch mutowalnych referencji w tym samym zasięgu, aby przekonać się, że `RefCell<T>` spanikuje">

```rust,ignore,panics
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-23/src/lib.rs:here}}
```

</Listing>

Tworzymy zmienną `one_borrow` dla inteligentnego wskaźnika `RefMut<T>`
zwróconego przez `borrow_mut`. Następnie w ten sam sposób tworzymy kolejne
mutowalne pożyczenie w zmiennej `two_borrow`. W efekcie w tym samym zasięgu
istnieją dwie mutowalne referencje, co jest niedozwolone. Gdy uruchomimy testy
naszej biblioteki, kod z listingu 15-23 skompiluje się bez błędów, ale test
zakończy się niepowodzeniem:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-23/output.txt}}
```

Zwróć uwagę, że kod spanikował z komunikatem
`already borrowed: BorrowMutError`. W ten sposób `RefCell<T>` obsługuje
naruszenia reguł pożyczania w czasie działania.

Wychwytywanie błędów pożyczania w czasie działania zamiast w czasie
kompilacji, tak jak zrobiliśmy tutaj, oznacza, że błędy w kodzie możesz
znajdować później w procesie tworzenia oprogramowania – być może dopiero
wtedy, gdy kod trafi na produkcję. Ponadto kod poniesie niewielki koszt
wydajności w czasie działania, ponieważ pożyczenia są śledzone w czasie
działania, a nie w czasie kompilacji. Jednak `RefCell<T>` umożliwia napisanie
atrapy, która może modyfikować samą siebie, aby zapamiętywać komunikaty, które
widziała, mimo że używasz jej w kontekście, w którym dozwolone są wyłącznie
niemutowalne wartości. Mimo tych kompromisów możesz używać `RefCell<T>`, aby
uzyskać więcej funkcjonalności, niż dają zwykłe referencje.

<!-- Old headings. Do not remove or links may break. -->

<a id="having-multiple-owners-of-mutable-data-by-combining-rc-t-and-ref-cell-t"></a>
<a id="allowing-multiple-owners-of-mutable-data-with-rct-and-refcellt"></a>

### Wielu właścicieli mutowalnych danych {#allowing-multiple-owners-of-mutable-data}

Typowym sposobem używania `RefCell<T>` jest łączenie go z `Rc<T>`. Przypomnij
sobie, że `Rc<T>` pozwala, aby pewne dane miały wielu właścicieli, ale daje
do nich wyłącznie niemutowalny dostęp. Jeśli masz `Rc<T>` przechowujący
`RefCell<T>`, możesz uzyskać wartość, która może mieć wielu właścicieli _i_
którą możesz modyfikować!

Przypomnij sobie na przykład listę cons (*cons list*) z listingu 15-18, w
którym użyliśmy `Rc<T>`, aby pozwolić wielu listom współdzielić własność innej
listy. Ponieważ `Rc<T>` przechowuje wyłącznie niemutowalne wartości, po
utworzeniu list nie możemy zmienić żadnej z przechowywanych w nich wartości.
Dodajmy `RefCell<T>`, aby zyskać możliwość zmieniania wartości w listach.
Listing 15-24 pokazuje, że dzięki użyciu `RefCell<T>` w definicji `Cons` możemy
modyfikować wartość przechowywaną we wszystkich listach.

<Listing number="15-24" file-name="src/main.rs" caption="Użycie `Rc<RefCell<i32>>` do utworzenia typu `List`, który możemy modyfikować">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-24/src/main.rs}}
```

</Listing>

Tworzymy wartość będącą instancją `Rc<RefCell<i32>>` i zapisujemy ją w
zmiennej o nazwie `value`, aby móc później odwołać się do niej bezpośrednio.
Następnie tworzymy w `a` wartość typu `List` z wariantem `Cons`, który
przechowuje `value`. Musimy sklonować `value`, aby zarówno `a`, jak i `value`
były właścicielami wewnętrznej wartości `5`, zamiast przenosić własność z
`value` do `a` albo sprawiać, by `a` pożyczało od `value`.

Opakowujemy listę `a` w `Rc<T>`, aby po utworzeniu list `b` i `c` obie mogły
odwoływać się do `a`, tak jak zrobiliśmy to w listingu 15-18.

Po utworzeniu list w `a`, `b` i `c` chcemy dodać 10 do wartości w `value`.
Robimy to, wywołując `borrow_mut` na `value`, co korzysta z mechanizmu
automatycznej dereferencji (*dereference*), który omówiliśmy w rozdziale 4,
aby wykonać dereferencję `Rc<T>` do wewnętrznej wartości `RefCell<T>`. Metoda `borrow_mut` zwraca inteligentny wskaźnik `RefMut<T>`, a
my używamy na nim operatora dereferencji i zmieniamy wewnętrzną wartość.

Gdy wypiszemy `a`, `b` i `c`, zobaczymy, że wszystkie mają zmodyfikowaną
wartość `15` zamiast `5`:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-24/output.txt}}
```

Ta technika jest całkiem zgrabna! Dzięki `RefCell<T>` mamy wartość `List`,
która z zewnątrz jest niemutowalna. Możemy jednak używać metod `RefCell<T>`
dających dostęp do jego wewnętrznej mutowalności, aby modyfikować dane, gdy
zajdzie taka potrzeba. Sprawdzanie reguł pożyczania w czasie działania chroni
nas przed wyścigami danych, a czasami warto poświęcić odrobinę szybkości na
rzecz takiej elastyczności struktur danych. Pamiętaj, że `RefCell<T>` nie
działa w kodzie wielowątkowym! Bezpieczną wątkowo wersją `RefCell<T>` jest
`Mutex<T>`, a `Mutex<T>` omówimy w rozdziale 16.

{{#quiz ../quizzes/ch15-05-interior-mutability.toml}}

[wheres-the---operator]: ch05-03-method-syntax.html#wheres-the---operator

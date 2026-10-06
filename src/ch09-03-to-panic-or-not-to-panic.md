## `panic!` czy nie `panic!`? {#to-panic-or-not-to-panic}

Jak więc zdecydować, kiedy wywołać `panic!`, a kiedy zwrócić `Result`? Gdy w
kodzie wystąpi panika (*panic*), nie da się już z niej wyjść. Możesz wywoływać
`panic!` w każdej sytuacji błędu, niezależnie od tego, czy da się go jakoś
obsłużyć, ale wtedy to ty decydujesz za kod wywołujący, że sytuacja jest
nieodwracalna. Gdy zwracasz wartość `Result`, zostawiasz wybór kodowi
wywołującemu. Może on spróbować obsłużyć błąd w sposób odpowiedni do swojej
sytuacji albo uznać, że wartość `Err` jest w tym przypadku nieodwracalna, więc
wywołać `panic!` i zamienić twój błąd odwracalny (*recoverable error*) w
nieodwracalny. Dlatego zwracanie `Result` jest dobrym domyślnym wyborem, gdy
definiujesz funkcję, która może zakończyć się niepowodzeniem.

W przykładach, prototypach i testach lepiej jest pisać kod, który panikuje,
zamiast zwracać `Result`. Zobaczmy, dlaczego tak jest, a potem omówmy sytuacje,
w których kompilator nie potrafi stwierdzić, że niepowodzenie jest niemożliwe,
ale ty jako człowiek to potrafisz. Na koniec podamy ogólne wskazówki, jak
zdecydować, czy kod biblioteki powinien panikować.

### Przykłady, prototypy i testy {#examples-prototype-code-and-tests}

Gdy piszesz przykład ilustrujący jakieś pojęcie, dodanie do niego solidnej
obsługi błędów może sprawić, że stanie się mniej czytelny. W przykładach
przyjmuje się, że wywołanie metody takiej jak `unwrap`, która może spowodować
panikę, jest symbolem zastępczym (*placeholder*) dla sposobu, w jaki twoja
aplikacja ma obsługiwać błędy. Ten sposób może być różny w zależności od tego,
co robi reszta twojego kodu.

Podobnie metody `unwrap` i `expect` są bardzo przydatne podczas tworzenia
prototypu, gdy jeszcze nie wiesz, jak chcesz obsługiwać błędy.
Zostawiają w kodzie wyraźne znaczniki na chwilę, gdy zechcesz uczynić program
solidniejszym.

Jeśli w teście wywołanie metody zakończy się niepowodzeniem, chcesz, aby cały
test zakończył się niepowodzeniem, nawet jeśli ta metoda nie jest testowaną
funkcjonalnością. Ponieważ to `panic!` oznacza test jako nieudany, wywołanie
`unwrap` lub `expect` jest dokładnie tym, co powinno się stać.

<!-- Old headings. Do not remove or links may break. -->

<a id="cases-in-which-you-have-more-information-than-the-compiler"></a>

### Gdy wiesz więcej niż kompilator {#when-you-have-more-information-than-the-compiler}

Wywołanie `expect` jest również właściwe, gdy masz jakąś inną logikę, która
zapewnia, że `Result` będzie miał wartość `Ok`, ale kompilator tej logiki nie
rozumie. Nadal masz wartość `Result`, którą musisz obsłużyć: wywoływana operacja
w ogólnym przypadku wciąż może się nie powieść, nawet jeśli w twojej konkretnej
sytuacji jest to logicznie niemożliwe. Jeśli po ręcznym przejrzeniu kodu masz
pewność, że nigdy nie dostaniesz wariantu `Err`, to całkowicie w porządku
jest wywołać `expect` i w tekście argumentu udokumentować, dlaczego uważasz, że
wariant `Err` nigdy nie wystąpi. Oto przykład:

```rust
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-08-unwrap-that-cant-fail/src/main.rs:here}}
```

Tworzymy instancję `IpAddr`, parsując łańcuch znaków (*string*) wpisany na
sztywno. Widzimy, że `127.0.0.1` jest poprawnym adresem IP, więc użycie tutaj
`expect` jest dopuszczalne. Jednak to, że łańcuch jest wpisany na sztywno i
poprawny, nie zmienia typu zwracanego przez metodę `parse`: nadal dostajemy
wartość `Result`, a kompilator wciąż każe nam obsłużyć `Result` tak, jakby
wariant `Err` był możliwy, bo nie jest na tyle sprytny, aby zauważyć, że ten
łańcuch zawsze jest poprawnym adresem IP. Gdyby łańcuch z adresem IP pochodził
od użytkownika, a nie był wpisany na sztywno w program, i _rzeczywiście_ mógł
spowodować niepowodzenie, z pewnością chcielibyśmy obsłużyć `Result` w bardziej
solidny sposób. Wzmianka o założeniu, że adres IP jest wpisany na sztywno,
skłoni nas do zastąpienia `expect` lepszym kodem obsługi błędów, jeśli w
przyszłości będziemy musieli pobierać adres IP z innego źródła.

### Wskazówki dotyczące obsługi błędów {#guidelines-for-error-handling}

Warto, aby kod panikował, gdy może znaleźć się w złym stanie. W tym kontekście
_zły stan_ oznacza sytuację, w której złamano jakieś założenie, gwarancję,
kontrakt lub niezmiennik, na przykład gdy do kodu przekazano wartości
niepoprawne, sprzeczne lub brakujące – a do tego zachodzi co najmniej jeden z
poniższych warunków:

- Zły stan jest czymś nieoczekiwanym, a nie czymś, co prawdopodobnie zdarzy się
  od czasu do czasu, jak wprowadzenie przez użytkownika danych w złym formacie.
- Kod po tym miejscu musi polegać na tym, że nie znajduje się w złym stanie,
  zamiast sprawdzać problem na każdym kroku.
- Nie ma dobrego sposobu, aby zakodować tę informację w używanych typach.
  Przykład tego, co mamy na myśli, omówimy w podrozdziale
  [„Kodowanie stanów i zachowań jako typów”][encoding]<!-- ignore --> w
  rozdziale 18.

Jeśli ktoś wywołuje twój kod i przekazuje wartości, które nie mają sensu,
najlepiej, o ile to możliwe, zwrócić błąd, aby użytkownik biblioteki mógł sam
zdecydować, co chce w takim przypadku zrobić. Jednak gdy dalsze działanie
mogłoby być niebezpieczne lub szkodliwe, najlepszym wyborem może być wywołanie
`panic!` i ostrzeżenie osoby używającej twojej biblioteki o błędzie w jej
kodzie, aby mogła go naprawić w trakcie tworzenia programu. Podobnie `panic!`
jest często właściwe, gdy wywołujesz zewnętrzny kod, nad którym nie masz
kontroli, a ten zwraca niepoprawny stan, którego nie da się naprawić.

Gdy jednak niepowodzenie jest spodziewane, lepiej zwrócić `Result`, niż wywołać
`panic!`. Przykładem jest parser, który dostaje źle sformatowane dane, albo
żądanie HTTP, które zwraca status oznaczający przekroczenie limitu liczby
żądań. W takich przypadkach zwrócenie `Result` wskazuje, że niepowodzenie jest
spodziewaną możliwością i to kod wywołujący musi zdecydować, jak ją obsłużyć.

Gdy kod wykonuje operację, która wywołana z niepoprawnymi wartościami mogłaby
narazić użytkownika na niebezpieczeństwo, powinien najpierw sprawdzić, czy
wartości są poprawne, i spanikować, jeśli nie są. Chodzi tu głównie o
bezpieczeństwo: próba działania na niepoprawnych danych może narazić kod na
podatności. To główny powód, dla którego biblioteka standardowa wywołuje
`panic!`, gdy próbujesz uzyskać dostęp do pamięci poza zakresem: próba dostępu
do pamięci, która nie należy do bieżącej struktury danych, to częsty problem
bezpieczeństwa. Funkcje często mają _kontrakty_: ich zachowanie jest
gwarantowane tylko wtedy, gdy dane wejściowe spełniają określone wymagania.
Panikowanie przy naruszeniu kontraktu ma sens, ponieważ naruszenie kontraktu
zawsze oznacza błąd po stronie kodu wywołującego, a nie jest to rodzaj błędu,
który kod wywołujący powinien jawnie obsługiwać. W rzeczywistości kod
wywołujący nie ma rozsądnego sposobu, aby się z niego wydobyć; to
_programiści_ wywołujący funkcję muszą poprawić kod. Kontrakty funkcji,
zwłaszcza gdy ich naruszenie powoduje panikę, powinny być opisane w
dokumentacji API danej funkcji.

Jednak umieszczanie wielu sprawdzeń błędów we wszystkich funkcjach byłoby
rozwlekłe i uciążliwe. Na szczęście możesz wykorzystać system typów Rusta (a
więc sprawdzanie typów wykonywane przez kompilator), aby wiele z tych sprawdzeń
wykonał za ciebie. Jeśli parametr funkcji ma określony typ, możesz kontynuować
logikę kodu ze świadomością, że kompilator już zapewnił, że masz poprawną
wartość. Jeśli na przykład masz typ zamiast `Option`, program oczekuje, że
dostanie _coś_, a nie _nic_. Kod nie musi wtedy obsługiwać dwóch przypadków dla
wariantów `Some` i `None`: będzie miał tylko jeden przypadek, w którym wartość
na pewno istnieje. Kod, który próbuje przekazać do funkcji nic, nawet się nie
skompiluje, więc funkcja nie musi sprawdzać tego przypadku w czasie działania.
Innym przykładem jest użycie typu liczby całkowitej bez znaku, takiego jak
`u32`, który zapewnia, że parametr nigdy nie będzie ujemny.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-custom-types-for-validation"></a>

### Własne typy do walidacji {#custom-types-for-validation}

Rozwińmy pomysł wykorzystania systemu typów Rusta do zapewnienia poprawności
wartości i przyjrzyjmy się tworzeniu własnego typu do walidacji. Przypomnij
sobie grę w zgadywanie z rozdziału 2, w której kod prosił użytkownika o
odgadnięcie liczby od 1 do 100. Nigdy nie sprawdziliśmy, czy odpowiedź
użytkownika mieści się w tym przedziale, zanim porównaliśmy ją z sekretną
liczbą; sprawdzaliśmy tylko, czy jest dodatnia. W tamtym przypadku skutki nie
były zbyt poważne: komunikat „Too high” lub „Too low” i tak byłby poprawny.
Przydałoby się jednak naprowadzać użytkownika na poprawne odpowiedzi i inaczej
reagować, gdy poda liczbę spoza przedziału, a inaczej, gdy wpisze na przykład
litery.

Można to zrobić, parsując odpowiedź jako `i32` zamiast tylko `u32`, aby
dopuścić liczby ujemne, a następnie dodając sprawdzenie, czy liczba mieści się
w przedziale:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch09-error-handling/no-listing-09-guess-out-of-range/src/main.rs:here}}
```

</Listing>

Wyrażenie `if` sprawdza, czy wartość jest poza przedziałem, informuje
użytkownika o problemie i wywołuje `continue`, aby rozpocząć kolejną iterację
pętli i poprosić o następną odpowiedź. Za wyrażeniem `if` możemy przejść do
porównań `guess` z sekretną liczbą, wiedząc, że `guess` mieści się między 1 a
100.

Nie jest to jednak idealne rozwiązanie: gdyby było absolutnie kluczowe, aby
program działał wyłącznie na wartościach od 1 do 100, i miał wiele funkcji z
takim wymaganiem, umieszczanie takiego sprawdzenia w każdej funkcji byłoby
żmudne (i mogłoby wpłynąć na wydajność).

Zamiast tego możemy utworzyć nowy typ w osobnym module i umieścić walidację w
funkcji tworzącej instancję tego typu, zamiast powtarzać ją wszędzie. Dzięki
temu funkcje mogą bezpiecznie używać nowego typu w swoich sygnaturach i z
pełnym zaufaniem korzystać z otrzymanych wartości. Listing 9-13 pokazuje jeden
ze sposobów zdefiniowania typu `Guess`, który utworzy instancję `Guess` tylko
wtedy, gdy funkcja `new` otrzyma wartość od 1 do 100.

<Listing number="9-13" caption="Typ `Guess`, który pozwala kontynuować tylko z wartościami od 1 do 100" file-name="src/guessing_game.rs">

```rust
{{#rustdoc_include ../listings/ch09-error-handling/listing-09-13/src/guessing_game.rs}}
```

</Listing>

Zwróć uwagę, że ten kod w pliku *src/guessing_game.rs* wymaga dodania
deklaracji modułu `mod guessing_game;` w pliku *src/lib.rs*, której tutaj nie
pokazaliśmy. W pliku nowego modułu definiujemy strukturę (*struct*) o nazwie
`Guess` z polem `value` przechowującym `i32`. To w nim będzie przechowywana
liczba.

Następnie implementujemy dla `Guess` funkcję powiązaną (*associated function*)
o nazwie `new`, która tworzy instancje wartości `Guess`. Funkcja `new` ma jeden
parametr o nazwie `value` typu `i32` i zwraca `Guess`. Kod w ciele funkcji
`new` sprawdza, czy `value` mieści się między 1 a 100. Jeśli `value` nie
przejdzie tego testu, wywołujemy `panic!`, co ostrzeże programistę piszącego
kod wywołujący, że ma w kodzie błąd do naprawienia, ponieważ utworzenie `Guess`
z `value` spoza tego przedziału naruszyłoby kontrakt, na którym polega
`Guess::new`. Warunki, w których `Guess::new` może spanikować, powinny być
opisane w publicznej dokumentacji API; konwencje dokumentacji sygnalizujące
możliwość wywołania `panic!` w tworzonej przez ciebie dokumentacji API
omówimy w rozdziale 14. Jeśli `value` przejdzie test, tworzymy nową wartość
`Guess` z polem `value` ustawionym na wartość parametru `value` i zwracamy tę
wartość `Guess`.

Następnie implementujemy metodę o nazwie `value`, która pożycza (*borrows*)
`self`, nie ma innych parametrów i zwraca `i32`. Taką metodę nazywa się czasem
_getterem_ (*getter*, metoda dostępowa), ponieważ jej zadaniem jest pobranie
danych z pól i ich zwrócenie. Ta publiczna metoda jest potrzebna, ponieważ pole
`value` struktury `Guess` jest prywatne. Ważne jest, aby pole `value` było
prywatne, tak aby kod używający struktury `Guess` nie mógł ustawiać `value`
bezpośrednio: kod spoza modułu `guessing_game` _musi_ używać funkcji
`Guess::new` do tworzenia instancji `Guess`, co gwarantuje, że `Guess` nie
może mieć wartości `value`, która nie została sprawdzona przez warunki w
funkcji `Guess::new`.

Funkcja, która przyjmuje parametr lub zwraca wyłącznie liczby od 1 do 100,
mogłaby wtedy zadeklarować w swojej sygnaturze, że przyjmuje lub zwraca `Guess`
zamiast `i32`, i nie musiałaby wykonywać w swoim ciele żadnych dodatkowych
sprawdzeń.

{{#quiz ../quizzes/ch09-03-panic-or-not.toml}}

## Podsumowanie {#summary}

Mechanizmy obsługi błędów w Ruście mają pomagać w pisaniu
solidniejszego kodu. Makro `panic!` sygnalizuje, że program jest w stanie, z
którym nie potrafi sobie poradzić, i pozwala nakazać procesowi zatrzymanie się
zamiast kontynuowania z niepoprawnymi lub błędnymi wartościami. *Enum* (typ
wyliczeniowy) `Result` wykorzystuje system typów Rusta, aby wskazać, że
operacje mogą się nie powieść w sposób, z którego kod może się wydobyć. Możesz
użyć `Result`, aby przekazać kodowi, który wywołuje twój kod, że musi on
obsłużyć zarówno potencjalny sukces, jak i niepowodzenie. Używanie `panic!` i
`Result` w odpowiednich sytuacjach sprawi, że kod będzie bardziej niezawodny w
obliczu nieuniknionych problemów.

Skoro już wiesz, w jak użyteczny sposób biblioteka standardowa korzysta z typów
generycznych (*generics*) w enumach `Option` i `Result`, omówimy, jak działają
typy generyczne i jak możesz ich używać we własnym kodzie.

[encoding]: ch18-03-oo-design-patterns.html#encoding-states-and-behavior-as-types

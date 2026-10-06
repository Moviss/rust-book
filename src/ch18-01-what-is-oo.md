## Cechy języków obiektowych {#characteristics-of-object-oriented-languages}

W społeczności programistów nie ma zgody co do tego, jakie mechanizmy musi mieć
język, aby można go było uznać za obiektowy. Na Rusta wpłynęło wiele paradygmatów
programowania, w tym OOP; na przykład w rozdziale 13 omówiliśmy mechanizmy
zaczerpnięte z programowania funkcyjnego. Można argumentować, że języki OOP
mają pewne wspólne cechy – mianowicie obiekty, hermetyzację i dziedziczenie.
Przyjrzyjmy się, co oznacza każda z tych cech i czy Rust ją obsługuje.

### Obiekty zawierają dane i zachowanie {#objects-contain-data-and-behavior}

Książka _Design Patterns: Elements of Reusable Object-Oriented Software_
autorstwa Ericha Gammy, Richarda Helma, Ralpha Johnsona i Johna Vlissidesa
(Addison-Wesley, 1994), potocznie nazywana książką _Gang of Four_ („Bandy
Czworga”), to katalog obiektowych wzorców projektowych. Definiuje ona OOP w ten
sposób:

> Programy obiektowe składają się z obiektów. **Obiekt** łączy w sobie zarówno
> dane, jak i procedury, które na tych danych operują. Procedury te nazywa się
> zwykle **metodami** lub **operacjami**.

Według tej definicji Rust jest obiektowy: struktury (*struct*) i *enumy* (typy
wyliczeniowe) mają dane, a bloki `impl` dostarczają metod dla struktur i
enumów. Choć struktury i enumy z metodami nie są _nazywane_ obiektami, zgodnie
z definicją obiektów Bandy Czworga zapewniają tę samą funkcjonalność.

### Hermetyzacja, która ukrywa szczegóły implementacji {#encapsulation-that-hides-implementation-details}

Kolejnym aspektem często kojarzonym z OOP jest idea _hermetyzacji_, która
oznacza, że szczegóły implementacji obiektu nie są dostępne dla kodu, który
tego obiektu używa. Jedynym sposobem interakcji z obiektem jest więc jego
publiczne API; kod używający obiektu nie powinien mieć możliwości sięgania do
jego wnętrza i bezpośredniej zmiany danych lub zachowania. Dzięki temu
programista może zmieniać i refaktoryzować wnętrze obiektu bez konieczności
zmiany kodu, który z tego obiektu korzysta.

W rozdziale 7 omówiliśmy, jak sterować hermetyzacją: za pomocą słowa
kluczowego (*keyword*) `pub` możemy zdecydować, które moduły, typy, funkcje i
metody w naszym kodzie mają być publiczne, a wszystko inne jest domyślnie
prywatne. Możemy na przykład zdefiniować strukturę `AveragedCollection` z polem
zawierającym wektor (*vector*) wartości `i32`. Struktura może mieć też pole
przechowujące średnią wartości z wektora, dzięki czemu średniej nie trzeba
obliczać na żądanie za każdym razem, gdy ktoś jej potrzebuje. Innymi słowy,
`AveragedCollection` będzie przechowywać obliczoną średnią w pamięci podręcznej.
Listing 18-1 zawiera definicję struktury `AveragedCollection`.

<Listing number="18-1" file-name="src/lib.rs" caption="Struktura `AveragedCollection`, która przechowuje listę liczb całkowitych i średnią elementów kolekcji">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-01/src/lib.rs}}
```

</Listing>

Struktura jest oznaczona jako `pub`, aby mógł jej używać inny kod, ale pola
wewnątrz struktury pozostają prywatne. Jest to tutaj ważne, ponieważ chcemy
mieć pewność, że za każdym razem, gdy wartość zostanie dodana do listy lub z
niej usunięta, średnia również zostanie zaktualizowana. Osiągamy to,
implementując w strukturze metody `add`, `remove` i `average`, jak pokazano w
listingu 18-2.

<Listing number="18-2" file-name="src/lib.rs" caption="Implementacje publicznych metod `add`, `remove` i `average` w `AveragedCollection`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-02/src/lib.rs:here}}
```

</Listing>

Publiczne metody `add`, `remove` i `average` to jedyne sposoby odczytu lub
modyfikacji danych w instancji `AveragedCollection`. Gdy element zostaje dodany
do `list` metodą `add` lub usunięty metodą `remove`, implementacja każdej z
nich wywołuje także prywatną metodę `update_average`, która zajmuje się
aktualizacją pola `average`.

Pola `list` i `average` pozostawiamy prywatne, aby zewnętrzny kod nie mógł
bezpośrednio dodawać elementów do pola `list` ani ich z niego usuwać; w
przeciwnym razie pole `average` mogłoby przestać być zsynchronizowane ze zmianami
`list`. Metoda `average` zwraca wartość pola `average`, pozwalając zewnętrznemu
kodowi odczytać `average`, ale nie modyfikować go.

Ponieważ zhermetyzowaliśmy szczegóły implementacji struktury
`AveragedCollection`, możemy w przyszłości łatwo zmienić różne jej aspekty, na
przykład strukturę danych. Moglibyśmy na przykład użyć dla pola `list` typu
`HashSet<i32>` zamiast `Vec<i32>`. Dopóki sygnatury publicznych metod `add`,
`remove` i `average` pozostałyby takie same, kod używający `AveragedCollection`
nie musiałby się zmieniać. Gdybyśmy natomiast upublicznili pole `list`, nie
musiałoby tak być: `HashSet<i32>` i `Vec<i32>` mają różne metody dodawania i
usuwania elementów, więc zewnętrzny kod prawdopodobnie musiałby się zmienić,
gdyby modyfikował `list` bezpośrednio.

Jeśli hermetyzacja jest niezbędnym warunkiem uznania języka za obiektowy, to
Rust ten warunek spełnia. Możliwość decydowania, czy użyć `pub` dla różnych
części kodu, pozwala hermetyzować szczegóły implementacji.

### Dziedziczenie jako system typów i jako współdzielenie kodu {#inheritance-as-a-type-system-and-as-code-sharing}

_Dziedziczenie_ (*inheritance*) to mechanizm, dzięki któremu obiekt może
odziedziczyć elementy z definicji innego obiektu, zyskując w ten sposób dane i
zachowanie obiektu nadrzędnego bez konieczności ponownego ich definiowania.

Jeśli język musi mieć dziedziczenie, aby był obiektowy, to Rust takim językiem
nie jest. Nie da się zdefiniować struktury, która dziedziczy pola i
implementacje metod struktury nadrzędnej, bez użycia makra.

Jeśli jednak dziedziczenie to dla ciebie stały element programistycznego
warsztatu, możesz w Ruście skorzystać z innych rozwiązań – zależnie od tego, z
jakiego powodu w ogóle sięgasz po dziedziczenie.

Dziedziczenie wybiera się z dwóch głównych powodów. Pierwszym jest ponowne
użycie kodu: możesz zaimplementować określone zachowanie dla jednego typu, a
dziedziczenie pozwala ponownie użyć tej implementacji dla innego typu. W
ograniczonym zakresie możesz to zrobić w kodzie Rusta za pomocą domyślnych
implementacji metod *traitów* (cech typów, zbliżonych do interfejsów), które
widzieliśmy w listingu 10-14, gdy dodaliśmy domyślną implementację metody
`summarize` do traitu `Summary`. Każdy typ implementujący trait `Summary`
miałby dostępną metodę `summarize` bez żadnego dodatkowego kodu. Przypomina to
sytuację, w której klasa nadrzędna ma implementację metody, a dziedzicząca po
niej klasa podrzędna również ma implementację tej metody. Możemy też nadpisać
domyślną implementację metody `summarize`, gdy implementujemy trait `Summary`,
co przypomina nadpisywanie przez klasę podrzędną implementacji metody
odziedziczonej po klasie nadrzędnej.

Drugi powód używania dziedziczenia wiąże się z systemem typów: chodzi o to, aby
typu podrzędnego można było używać w tych samych miejscach co typu nadrzędnego.
Nazywa się to również _polimorfizmem_ (*polymorphism*), co oznacza, że w czasie
działania programu można zastępować jedne obiekty innymi, jeśli mają one
pewne wspólne cechy.

> ### Polimorfizm {#polymorphism}
>
> Dla wielu osób polimorfizm jest synonimem dziedziczenia. W rzeczywistości jest
> to jednak pojęcie ogólniejsze, odnoszące się do kodu, który może działać na
> danych wielu typów. W przypadku dziedziczenia tymi typami są zazwyczaj
> podklasy.
>
> Rust zamiast tego używa typów generycznych (*generics*) do abstrahowania od
> różnych możliwych typów oraz ograniczeń traitów (*trait bounds*) do nakładania
> wymagań co do tego, co te typy muszą zapewniać. Nazywa się to czasem
> _ograniczonym polimorfizmem parametrycznym_ (*bounded parametric
> polymorphism*).

Rezygnując z dziedziczenia, Rust wybrał inny zestaw kompromisów. Dziedziczenie
często niesie ryzyko współdzielenia większej ilości kodu, niż to konieczne.
Podklasy nie zawsze powinny współdzielić wszystkie cechy swojej klasy
nadrzędnej, a przy dziedziczeniu tak się dzieje. Może to zmniejszyć
elastyczność projektu programu. Wprowadza to również możliwość wywoływania na
podklasach metod, które nie mają sensu lub powodują błędy, ponieważ nie mają
zastosowania do danej podklasy. Ponadto niektóre języki pozwalają tylko na
_dziedziczenie pojedyncze_ (*single inheritance*; podklasa może dziedziczyć
tylko po jednej klasie), co dodatkowo ogranicza elastyczność projektu programu.

Z tych powodów Rust stosuje inne podejście: zamiast dziedziczenia używa
obiektów traitów (*trait objects*), aby osiągnąć polimorfizm w czasie działania
programu. Przyjrzyjmy się, jak działają obiekty traitów.

{{#quiz ../quizzes/ch17-01-what-is-oo.toml}}

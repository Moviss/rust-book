## Dodatek C: Traity wyprowadzalne {#appendix-c-derivable-traits}

W różnych miejscach książki omawialiśmy atrybut `derive`, który możesz
zastosować do definicji struktury (*struct*) lub *enuma* (typu wyliczeniowego).
Atrybut `derive` generuje kod, który implementuje *trait* (cechę typu, zbliżoną
do interfejsu) z jego własną domyślną implementacją dla typu oznaczonego
składnią `derive`.

W tym dodatku zebraliśmy wszystkie traity z biblioteki standardowej, których
możesz używać z `derive`. Każda sekcja omawia:

- jakie operatory i metody udostępnia wyprowadzenie (*derive*) danego traitu;
- co robi implementacja traitu dostarczana przez `derive`;
- co implementacja traitu mówi o typie;
- warunki, w których wolno lub nie wolno implementować trait;
- przykłady operacji, które wymagają tego traitu.

Jeśli chcesz uzyskać zachowanie inne niż to, które zapewnia atrybut `derive`,
zajrzyj do [dokumentacji biblioteki standardowej](../std/index.html)<!-- ignore -->
dotyczącej danego traitu, gdzie znajdziesz szczegóły ręcznej implementacji.

Wymienione tutaj traity są jedynymi traitami zdefiniowanymi w bibliotece
standardowej, które można zaimplementować dla własnych typów za pomocą `derive`.
Inne traity z biblioteki standardowej nie mają sensownego zachowania
domyślnego, więc to od ciebie zależy, jak je zaimplementujesz, aby miały sens w
kontekście tego, co chcesz osiągnąć.

Przykładem traitu, którego nie da się wyprowadzić, jest `Display`, który
odpowiada za formatowanie dla użytkowników końcowych. Zawsze warto się
zastanowić, jak odpowiednio wyświetlić typ użytkownikowi końcowemu. Które części
typu powinien móc zobaczyć? Które uzna za istotne? Jaki format danych będzie dla
niego najbardziej przydatny? Kompilator Rusta nie ma tej wiedzy, więc nie może
zapewnić za ciebie odpowiedniego zachowania domyślnego.

Lista traitów wyprowadzalnych podana w tym dodatku nie jest wyczerpująca:
biblioteki mogą implementować `derive` dla własnych traitów, przez co lista
traitów, których można używać z `derive`, jest w praktyce otwarta.
Implementacja `derive` wymaga użycia makra proceduralnego, które omawiamy w
podrozdziale [„Własne makra `derive`”][custom-derive-macros]<!-- ignore --> w
rozdziale 20.

### `Debug` do wypisywania dla programisty {#debug-for-programmer-output}

Trait `Debug` umożliwia formatowanie debugowania w łańcuchach formatujących,
które włączasz, dodając `:?` wewnątrz symboli zastępczych (*placeholder*) `{}`.

Trait `Debug` pozwala wypisywać instancje typu w celach debugowania, dzięki
czemu ty i inni programiści korzystający z twojego typu możecie podejrzeć
instancję w określonym momencie wykonania programu.

Trait `Debug` jest wymagany na przykład przy użyciu makra `assert_eq!`. To
makro wypisuje wartości instancji przekazanych jako argumenty, jeśli asercja
równości się nie powiedzie, aby programiści mogli zobaczyć, dlaczego te dwie
instancje nie były równe.

### `PartialEq` i `Eq` do porównań równości {#partialeq-and-eq-for-equality-comparisons}

Trait `PartialEq` pozwala porównywać instancje typu pod kątem równości i
umożliwia używanie operatorów `==` i `!=`.

Wyprowadzenie `PartialEq` implementuje metodę `eq`. Gdy `PartialEq` jest
wyprowadzony dla struktur, dwie instancje są równe tylko wtedy, gdy _wszystkie_
pola są równe, a instancje nie są równe, jeśli _którekolwiek_ pole się różni.
Gdy jest wyprowadzony dla enumów, każdy wariant jest równy samemu sobie i różny
od pozostałych wariantów.

Trait `PartialEq` jest wymagany na przykład przy użyciu makra `assert_eq!`,
które musi umieć porównać dwie instancje typu pod kątem równości.

Trait `Eq` nie ma metod. Jego celem jest zasygnalizowanie, że każda wartość
oznaczonego typu jest równa samej sobie. Trait `Eq` można zastosować tylko do
typów, które implementują również `PartialEq`, choć nie wszystkie typy
implementujące `PartialEq` mogą implementować `Eq`. Przykładem są typy liczb
zmiennoprzecinkowych: implementacja liczb zmiennoprzecinkowych stanowi, że dwie
instancje wartości „nie-liczba” (`NaN`) nie są sobie równe.

Przykładem sytuacji, w której wymagany jest `Eq`, są klucze w `HashMap<K, V>`,
dzięki czemu `HashMap<K, V>` może stwierdzić, czy dwa klucze są takie same.

### `PartialOrd` i `Ord` do porównań kolejności {#partialord-and-ord-for-ordering-comparisons}

Trait `PartialOrd` pozwala porównywać instancje typu na potrzeby sortowania.
Typu implementującego `PartialOrd` można używać z operatorami `<`, `>`, `<=` i
`>=`. Trait `PartialOrd` można zastosować tylko do typów, które implementują
również `PartialEq`.

Wyprowadzenie `PartialOrd` implementuje metodę `partial_cmp`, która zwraca
`Option<Ordering>` równe `None`, gdy podane wartości nie wyznaczają kolejności.
Przykładem wartości, która nie wyznacza kolejności, mimo że większość wartości
tego typu da się porównać, jest zmiennoprzecinkowa wartość `NaN`. Wywołanie
`partial_cmp` z dowolną liczbą zmiennoprzecinkową i zmiennoprzecinkową wartością
`NaN` zwróci `None`.

Gdy `PartialOrd` jest wyprowadzony dla struktur, porównuje dwie instancje,
porównując wartości kolejnych pól w takiej kolejności, w jakiej pola występują w
definicji struktury. Gdy jest wyprowadzony dla enumów, warianty zadeklarowane
wcześniej w definicji enuma są uznawane za mniejsze od wariantów wymienionych
później.

Trait `PartialOrd` jest wymagany na przykład przez metodę `gen_range` z
*crate’a* (jednostki kompilacji w Ruście) `rand`, która generuje losową wartość
z zakresu określonego wyrażeniem zakresu.

Trait `Ord` pozwala mieć pewność, że dla dowolnych dwóch wartości oznaczonego
typu istnieje prawidłowa kolejność. Trait `Ord` implementuje metodę `cmp`, która
zwraca `Ordering`, a nie `Option<Ordering>`, ponieważ prawidłowe uporządkowanie
jest zawsze możliwe. Trait `Ord` można zastosować tylko do typów, które
implementują również `PartialOrd` i `Eq` (a `Eq` wymaga `PartialEq`). Po
wyprowadzeniu dla struktur i enumów metoda `cmp` zachowuje się tak samo jak
wyprowadzona implementacja `partial_cmp` w `PartialOrd`.

Przykładem sytuacji, w której wymagany jest `Ord`, jest przechowywanie wartości
w `BTreeSet<T>` – strukturze danych, która przechowuje dane zgodnie z porządkiem
sortowania wartości.

### `Clone` i `Copy` do powielania wartości {#clone-and-copy-for-duplicating-values}

Trait `Clone` pozwala jawnie utworzyć głęboką kopię wartości, a proces
powielania może wymagać wykonania dowolnego kodu i kopiowania danych ze sterty
(*heap*).

Wyprowadzenie `Clone` implementuje metodę `clone`, która – zaimplementowana dla
całego typu – wywołuje `clone` na każdej z części typu. Oznacza to, że aby
wyprowadzić `Clone`, wszystkie pola lub wartości w typie także muszą
implementować `Clone`.

Przykładem sytuacji, w której wymagany jest `Clone`, jest wywołanie metody
`to_vec` na wycinku (*slice*). Wycinek nie jest właścicielem instancji typu,
które zawiera, ale wektor (*vector*) zwrócony przez `to_vec` musi być
właścicielem swoich instancji, więc `to_vec` wywołuje `clone` na każdym
elemencie. Dlatego typ przechowywany w wycinku musi implementować `Clone`.

Trait `Copy` pozwala powielić wartość przez samo skopiowanie bitów
przechowywanych na stosie (*stack*); żaden dowolny kod nie jest potrzebny.

Trait `Copy` nie definiuje żadnych metod, aby programiści nie mogli ich
przeciążać i łamać założenia, że nie jest wykonywany żaden dowolny kod. Dzięki
temu wszyscy programiści mogą zakładać, że skopiowanie wartości będzie bardzo
szybkie.

Możesz wyprowadzić `Copy` dla każdego typu, którego wszystkie części
implementują `Copy`. Typ implementujący `Copy` musi implementować również
`Clone`, ponieważ typ implementujący `Copy` ma trywialną implementację `Clone`,
która wykonuje to samo zadanie co `Copy`.

Trait `Copy` jest rzadko wymagany; typy implementujące `Copy` mają dostępne
optymalizacje, dzięki którym nie musisz wywoływać `clone`, co sprawia, że kod
jest bardziej zwięzły.

Wszystko, co jest możliwe z `Copy`, możesz osiągnąć również za pomocą `Clone`,
ale kod może być wolniejszy albo w niektórych miejscach będzie musiał używać
`clone`.

### `Hash` do odwzorowania wartości na wartość o stałym rozmiarze {#hash-for-mapping-a-value-to-a-value-of-fixed-size}

Trait `Hash` pozwala wziąć instancję typu o dowolnym rozmiarze i odwzorować ją
na wartość o stałym rozmiarze za pomocą funkcji haszującej (*hashing function*).
Wyprowadzenie `Hash` implementuje metodę `hash`. Wyprowadzona implementacja
metody `hash` łączy wyniki wywołania `hash` na każdej z części typu, co oznacza,
że aby wyprowadzić `Hash`, wszystkie pola lub wartości także muszą implementować
`Hash`.

Przykładem sytuacji, w której wymagany jest `Hash`, jest przechowywanie kluczy w
`HashMap<K, V>`, aby wydajnie przechowywać dane.

### `Default` do wartości domyślnych {#default-for-default-values}

Trait `Default` pozwala utworzyć wartość domyślną dla typu. Wyprowadzenie
`Default` implementuje funkcję `default`. Wyprowadzona implementacja funkcji
`default` wywołuje funkcję `default` na każdej części typu, co oznacza, że aby
wyprowadzić `Default`, wszystkie pola lub wartości w typie także muszą
implementować `Default`.

Funkcji `Default::default` często używa się w połączeniu ze składnią
aktualizacji struktury (*struct update syntax*) omówioną w podrozdziale
[„Tworzenie instancji za pomocą składni aktualizacji struktury”][creating-instances-from-other-instances-with-struct-update-syntax]<!--
ignore --> w rozdziale 5. Możesz dostosować kilka pól struktury, a dla
pozostałych pól ustawić i wykorzystać wartość domyślną, używając
`..Default::default()`.

Trait `Default` jest wymagany na przykład wtedy, gdy używasz metody
`unwrap_or_default` na instancjach `Option<T>`. Jeśli `Option<T>` ma wartość
`None`, metoda `unwrap_or_default` zwróci wynik `Default::default` dla typu `T`
przechowywanego w `Option<T>`.

[creating-instances-from-other-instances-with-struct-update-syntax]: ch05-01-defining-structs.html#creating-instances-from-other-instances-with-struct-update-syntax
[stack-only-data-copy]: ch04-01-what-is-ownership.html#stack-only-data-copy
[variables-and-data-interacting-with-clone]: ch04-01-what-is-ownership.html#variables-and-data-interacting-with-clone
[custom-derive-macros]: ch20-05-macros.html#custom-derive-macros

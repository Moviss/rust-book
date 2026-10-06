## Przetwarzanie serii elementów za pomocą iteratorów {#processing-a-series-of-items-with-iterators}

Wzorzec iteratora (*iterator pattern*) pozwala wykonywać jakieś zadanie
kolejno na każdym elemencie sekwencji. Iterator odpowiada za logikę
przechodzenia przez kolejne elementy i za ustalenie, kiedy sekwencja się
skończyła. Gdy używasz iteratorów, nie musisz sam implementować tej logiki od
nowa.

W Ruście iteratory są _leniwe_ (*lazy*), co oznacza, że nie mają żadnego
efektu, dopóki nie wywołasz metod, które konsumują iterator, czyli go
wyczerpują. Na przykład kod w listingu 13-10 tworzy iterator po elementach
wektora (*vector*) `v1`, wywołując metodę `iter` zdefiniowaną dla `Vec<T>`. Sam
w sobie ten kod nie robi nic użytecznego.

<Listing number="13-10" file-name="src/main.rs" caption="Tworzenie iteratora">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-10/src/main.rs:here}}
```

</Listing>

Iterator jest przechowywany w zmiennej `v1_iter`. Po utworzeniu iteratora
możemy go użyć na wiele sposobów. W listingu 3-5 iterowaliśmy po tablicy za
pomocą pętli `for`, aby wykonać jakiś kod na każdym z jej elementów. Pod
spodem pętla ta niejawnie tworzyła, a potem konsumowała iterator, ale aż do
teraz pomijaliśmy szczegóły tego, jak dokładnie to działa.

W przykładzie z listingu 13-11 oddzielamy utworzenie iteratora od jego użycia
w pętli `for`. Gdy pętla `for` zostaje wywołana z iteratorem z `v1_iter`, każdy
element iteratora jest używany w jednej iteracji pętli, która wypisuje każdą
wartość.

<Listing number="13-11" file-name="src/main.rs" caption="Używanie iteratora w pętli `for`">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-11/src/main.rs:here}}
```

</Listing>

W językach, których biblioteki standardowe nie udostępniają iteratorów,
prawdopodobnie zapisałbyś tę samą funkcjonalność, zaczynając od zmiennej
ustawionej na indeks 0, używając tej zmiennej do indeksowania wektora w celu
pobrania wartości i zwiększając jej wartość w pętli, aż osiągnie łączną liczbę
elementów w wektorze.

Iteratory obsługują całą tę logikę za ciebie, ograniczając powtarzalny kod, w
którym łatwo o pomyłkę. Dają też większą elastyczność: tej samej logiki możesz
używać z wieloma różnymi rodzajami sekwencji, a nie tylko ze strukturami
danych, które da się indeksować, takimi jak wektory. Przyjrzyjmy się, jak
iteratory to robią.

### Trait `Iterator` i metoda `next` {#the-iterator-trait-and-the-next-method}

Wszystkie iteratory implementują *trait* (cecha typu, zbliżona do interfejsu)
o nazwie `Iterator`, zdefiniowany w bibliotece standardowej. Definicja tego
traitu wygląda tak:

```rust
pub trait Iterator {
    type Item;

    fn next(&mut self) -> Option<Self::Item>;

    // methods with default implementations elided
}
```

Zwróć uwagę, że ta definicja używa nowej składni: `type Item` i `Self::Item`,
które definiują typ powiązany (*associated type*) z tym traitem. O typach
powiązanych powiemy szczegółowo w rozdziale 20. Na razie wystarczy wiedzieć, że
ten kod mówi, iż implementacja traitu `Iterator` wymaga zdefiniowania również
typu `Item`, a ten typ `Item` jest używany w typie zwracanym metody `next`.
Innymi słowy, typ `Item` będzie typem zwracanym przez iterator.

Trait `Iterator` wymaga od typów implementujących zdefiniowania tylko jednej
metody: metody `next`, która zwraca po jednym elemencie iteratora naraz,
opakowanym w `Some`, a gdy iteracja się zakończy, zwraca `None`.

Metodę `next` możemy wywoływać na iteratorach bezpośrednio; listing 13-12
pokazuje, jakie wartości zwracają kolejne wywołania `next` na iteratorze
utworzonym z wektora.

<Listing number="13-12" file-name="src/lib.rs" caption="Wywoływanie metody `next` na iteratorze">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-12/src/lib.rs:here}}
```

</Listing>

Zwróć uwagę, że musieliśmy uczynić `v1_iter` mutowalnym (*mutable*):
wywołanie metody `next` na iteratorze zmienia jego stan wewnętrzny, za pomocą
którego iterator śledzi, w którym miejscu sekwencji się znajduje. Innymi słowy,
ten kod _konsumuje_ iterator, czyli go wyczerpuje. Każde wywołanie `next`
zjada jeden element z iteratora. Nie musieliśmy czynić `v1_iter` mutowalnym,
gdy używaliśmy pętli `for`, ponieważ pętla przejęła własność (*ownership*)
`v1_iter` i za kulisami uczyniła go mutowalnym.

Zwróć też uwagę, że wartości, które otrzymujemy z wywołań `next`, są
niemutowalnymi referencjami (*reference*) do wartości w wektorze. Metoda
`iter` tworzy iterator po niemutowalnych referencjach. Jeśli chcemy utworzyć
iterator, który przejmuje własność `v1` i zwraca wartości będące
właścicielami swoich danych, możemy zamiast `iter` wywołać `into_iter`.
Podobnie, jeśli chcemy iterować po mutowalnych referencjach, możemy zamiast
`iter` wywołać `iter_mut`.

### Metody konsumujące iterator {#methods-that-consume-the-iterator}

Trait `Iterator` ma wiele różnych metod z implementacjami domyślnymi
dostarczanymi przez bibliotekę standardową; możesz się o nich dowiedzieć,
zaglądając do dokumentacji API biblioteki standardowej dla traitu `Iterator`.
Niektóre z tych metod wywołują w swojej definicji metodę `next`, dlatego przy
implementowaniu traitu `Iterator` trzeba zaimplementować metodę `next`.

Metody, które wywołują `next`, nazywamy _adapterami konsumującymi_
(*consuming adapters*), ponieważ ich wywołanie wyczerpuje iterator. Jednym z
przykładów jest metoda `sum`, która przejmuje własność iteratora i przechodzi
przez jego elementy, wielokrotnie wywołując `next`, a tym samym konsumując
iterator. Podczas przechodzenia dodaje każdy element do bieżącej sumy i zwraca
sumę po zakończeniu iteracji. Listing 13-13 zawiera test ilustrujący użycie
metody `sum`.

<Listing number="13-13" file-name="src/lib.rs" caption="Wywoływanie metody `sum`, aby otrzymać sumę wszystkich elementów iteratora">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-13/src/lib.rs:here}}
```

</Listing>

Po wywołaniu `sum` nie wolno nam już używać `v1_iter`, ponieważ `sum`
przejmuje własność iteratora, na którym ją wywołujemy.

### Metody tworzące inne iteratory {#methods-that-produce-other-iterators}

_Adaptery iteratora_ (*iterator adapters*) to metody zdefiniowane w traicie
`Iterator`, które nie konsumują iteratora. Zamiast tego tworzą inne iteratory,
zmieniając jakiś aspekt iteratora oryginalnego.

Listing 13-14 pokazuje przykład wywołania metody `map` będącej adapterem
iteratora; przyjmuje ona domknięcie (*closure*), które wywołuje na każdym
elemencie podczas przechodzenia przez elementy. Metoda `map` zwraca nowy
iterator, który daje zmodyfikowane elementy. Domknięcie tworzy tu nowy
iterator, w którym każdy element z wektora zostanie zwiększony o 1.

<Listing number="13-14" file-name="src/main.rs" caption="Wywoływanie adaptera iteratora `map` w celu utworzenia nowego iteratora">

```rust,not_desired_behavior
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-14/src/main.rs:here}}
```

</Listing>

Ten kod generuje jednak ostrzeżenie:

```console
{{#include ../listings/ch13-functional-features/listing-13-14/output.txt}}
```

Kod z listingu 13-14 nic nie robi; podane przez nas domknięcie nigdy nie
zostaje wywołane. Ostrzeżenie przypomina nam dlaczego: adaptery iteratora są
leniwe i musimy tu skonsumować iterator.

Aby usunąć to ostrzeżenie i skonsumować iterator, użyjemy metody `collect`,
której używaliśmy z `env::args` w listingu 12-1. Ta metoda konsumuje iterator
i zbiera wynikowe wartości w kolekcję.

W listingu 13-15 zbieramy do wektora wyniki iterowania po iteratorze
zwróconym z wywołania `map`. Ten wektor będzie ostatecznie zawierał każdy
element z oryginalnego wektora zwiększony o 1.

<Listing number="13-15" file-name="src/main.rs" caption="Wywoływanie metody `map` w celu utworzenia nowego iteratora, a następnie metody `collect` w celu skonsumowania nowego iteratora i utworzenia wektora">

```rust
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-15/src/main.rs:here}}
```

</Listing>

Ponieważ `map` przyjmuje domknięcie, możemy określić dowolną operację, którą
chcemy wykonać na każdym elemencie. To świetny przykład tego, jak domknięcia
pozwalają dostosować pewne zachowanie, a jednocześnie ponownie wykorzystać
zachowanie iterowania, które zapewnia trait `Iterator`.

Możesz łączyć w łańcuch wiele wywołań adapterów iteratora, aby w czytelny
sposób wykonywać złożone działania. Ponieważ jednak wszystkie iteratory są
leniwe, aby uzyskać wyniki wywołań adapterów iteratora, musisz wywołać jedną z
metod będących adapterami konsumującymi.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-closures-that-capture-their-environment"></a>

### Domknięcia przechwytujące swoje środowisko {#closures-that-capture-their-environment}

Wiele adapterów iteratora przyjmuje domknięcia jako argumenty i zazwyczaj
domknięcia, które będziemy przekazywać adapterom iteratora, będą domknięciami
przechwytującymi swoje środowisko.

W tym przykładzie użyjemy metody `filter`, która przyjmuje domknięcie.
Domknięcie otrzymuje element z iteratora i zwraca `bool`. Jeśli domknięcie
zwróci `true`, wartość zostanie uwzględniona w iteracji tworzonej przez
`filter`. Jeśli domknięcie zwróci `false`, wartość nie zostanie uwzględniona.

W listingu 13-16 używamy `filter` z domknięciem, które przechwytuje ze swojego
środowiska zmienną `shoe_size`, aby iterować po kolekcji instancji struktury
(*struct*) `Shoe`. Zwróci ono tylko buty o podanym rozmiarze.

<Listing number="13-16" file-name="src/lib.rs" caption="Używanie metody `filter` z domknięciem, które przechwytuje `shoe_size`">

```rust,noplayground
{{#rustdoc_include ../listings/ch13-functional-features/listing-13-16/src/lib.rs}}
```

</Listing>

Funkcja `shoes_in_size` przyjmuje jako parametry wektor butów, przejmując jego
własność, oraz rozmiar buta. Zwraca wektor zawierający tylko buty o podanym
rozmiarze.

W ciele `shoes_in_size` wywołujemy `into_iter`, aby utworzyć iterator, który
przejmuje własność wektora. Następnie wywołujemy `filter`, aby przekształcić
ten iterator w nowy iterator, zawierający tylko te elementy, dla których
domknięcie zwraca `true`.

Domknięcie przechwytuje ze środowiska parametr `shoe_size` i porównuje jego
wartość z rozmiarem każdego buta, zachowując tylko buty o podanym rozmiarze.
Na koniec wywołanie `collect` zbiera wartości zwracane przez przekształcony
iterator do wektora, który funkcja zwraca.

Test pokazuje, że gdy wywołujemy `shoes_in_size`, otrzymujemy z powrotem
tylko buty o takim samym rozmiarze jak podana przez nas wartość.

{{#quiz ../quizzes/ch13-02-iterators.toml}}

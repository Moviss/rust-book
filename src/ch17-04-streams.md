<!-- Old headings. Do not remove or links may break. -->

<a id="streams"></a>

## Strumienie: future’y w sekwencji {#streams-futures-in-sequence}

Przypomnij sobie, jak wcześniej w tym rozdziale, w podrozdziale
[„Przesyłanie danych między dwoma zadaniami za pomocą przekazywania komunikatów”][17-02-messages]<!-- ignore -->,
używaliśmy odbiornika naszego asynchronicznego kanału. Asynchroniczna metoda
`recv` z biegiem czasu dostarcza sekwencję elementów. To przykład znacznie
ogólniejszego wzorca, znanego jako strumień (*stream*). Wiele zjawisk w
naturalny sposób daje się przedstawić jako strumienie: elementy pojawiające się w kolejce, fragmenty
danych stopniowo pobierane z systemu plików, gdy cały zbiór danych jest zbyt
duży, by zmieścić się w pamięci komputera, albo dane napływające z czasem przez
sieć. Ponieważ strumienie są *future*’ami (wartościami, które będą gotowe
później), możemy ich używać z każdym innym rodzajem future’a i łączyć je na
ciekawe sposoby. Możemy na przykład grupować zdarzenia w paczki, aby uniknąć
zbyt wielu wywołań sieciowych, ustawiać limity czasu dla sekwencji
długotrwałych operacji albo ograniczać częstotliwość zdarzeń interfejsu
użytkownika, aby nie wykonywać niepotrzebnej pracy.

Sekwencję elementów widzieliśmy już w rozdziale 13, gdy w podrozdziale
[„Trait `Iterator` i metoda `next`”][iterator-trait]<!--
ignore --> przyglądaliśmy się *traitowi* (cesze typu, zbliżonej do
interfejsu) o nazwie Iterator, ale między iteratorami a odbiornikiem kanału
asynchronicznego są dwie różnice.
Pierwsza dotyczy czasu: iteratory są synchroniczne, a odbiornik kanału jest
asynchroniczny. Druga dotyczy API. Pracując bezpośrednio z `Iterator`,
wywołujemy jego synchroniczną metodę `next`. W przypadku strumienia
`trpl::Receiver` wywoływaliśmy natomiast asynchroniczną metodę `recv`. Poza tym
te API wydają się bardzo podobne i to podobieństwo nie jest przypadkowe.
Strumień przypomina asynchroniczną formę iteracji. O ile jednak
`trpl::Receiver` czeka konkretnie na odbiór komunikatów, o tyle API strumieni
ogólnego przeznaczenia jest znacznie szersze: dostarcza kolejny element tak jak
`Iterator`, ale asynchronicznie.

Podobieństwo między iteratorami a strumieniami w Ruście oznacza, że z każdego
iteratora możemy właściwie utworzyć strumień. Tak jak z iteratorem, ze
strumieniem możemy pracować, wywołując jego metodę `next` i oczekując na jej
wynik, jak w listingu 17-21, który na razie się nie skompiluje.

<Listing number="17-21" caption="Tworzenie strumienia z iteratora i wypisywanie jego wartości" file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-21/src/main.rs:stream}}
```

</Listing>

Zaczynamy od tablicy liczb, którą przekształcamy w iterator, a następnie
wywołujemy na nim `map`, aby podwoić wszystkie wartości. Potem przekształcamy
iterator w strumień za pomocą funkcji `trpl::stream_from_iter`. Następnie w
pętli `while let` przechodzimy po elementach strumienia, w miarę jak się
pojawiają.

Niestety, gdy próbujemy uruchomić ten kod, nie kompiluje się, a kompilator
zgłasza, że metoda `next` nie jest dostępna:

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-21
cargo build
copy only the error output
-->

```text
error[E0599]: no method named `next` found for struct `tokio_stream::iter::Iter` in the current scope
  --> src/main.rs:10:40
   |
10 |         while let Some(value) = stream.next().await {
   |                                        ^^^^
   |
   = help: items from traits can only be used if the trait is in scope
help: the following traits which provide `next` are implemented but not in scope; perhaps you want to import one of them
   |
1  + use crate::trpl::StreamExt;
   |
1  + use futures_util::stream::stream::StreamExt;
   |
1  + use std::iter::Iterator;
   |
1  + use std::str::pattern::Searcher;
   |
help: there is a method `try_next` with a similar name
   |
10 |         while let Some(value) = stream.try_next().await {
   |                                        ~~~~~~~~
```

Jak wyjaśnia ten komunikat, przyczyną błędu kompilatora jest to, że aby móc
użyć metody `next`, musimy mieć w zasięgu (*scope*) odpowiedni trait. Biorąc
pod uwagę dotychczasowe omówienie, można by się spodziewać, że chodzi o trait
`Stream`, ale w rzeczywistości jest to `StreamExt`. `Ext`, skrót od
_extension_ (rozszerzenie), to w społeczności Rusta popularny wzorzec
rozszerzania jednego traitu o inny.

Trait `Stream` definiuje niskopoziomowy interfejs, który w praktyce łączy
traity `Iterator` i `Future`. `StreamExt` dostarcza nad `Stream` zestaw API
wyższego poziomu, w tym metodę `next` oraz inne metody pomocnicze, podobne do
tych, które zapewnia trait `Iterator`. `Stream` i `StreamExt` nie są jeszcze
częścią biblioteki standardowej Rusta, ale większość *crate*’ów (jednostek
kompilacji w Ruście) w ekosystemie używa podobnych definicji.

Aby naprawić błąd kompilatora, wystarczy dodać instrukcję `use` dla
`trpl::StreamExt`, jak w listingu 17-22.

<Listing number="17-22" caption="Udane użycie iteratora jako podstawy strumienia" file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-22/src/main.rs:all}}
```

</Listing>

Po złożeniu wszystkich tych elementów kod działa tak, jak chcemy! Co więcej,
skoro mamy teraz w zasięgu `StreamExt`, możemy korzystać ze wszystkich jego
metod pomocniczych, tak jak w przypadku iteratorów.

{{#quiz ../quizzes/async-04-streams.toml}}

[17-02-messages]: ch17-02-concurrency-with-async.html#message-passing
[iterator-trait]: ch13-02-iterators.html#the-iterator-trait-and-the-next-method

<!-- Old headings. Do not remove or links may break. -->

<a id="digging-into-the-traits-for-async"></a>

## Bliższe spojrzenie na traity związane z async {#a-closer-look-at-the-traits-for-async}

W całym rozdziale na różne sposoby używaliśmy *traitów* (cech typów, zbliżonych
do interfejsów) `Future`, `Stream` i `StreamExt`. Dotąd jednak unikaliśmy
zagłębiania się w szczegóły tego, jak działają i jak do siebie pasują – i w
codziennej pracy z Rustem zwykle w zupełności to wystarcza. Czasem jednak
trafisz na sytuacje, w których trzeba będzie zrozumieć nieco więcej szczegółów
tych traitów, a także typ `Pin` i trait `Unpin`. W tym podrozdziale zagłębimy
się w nie na tyle, by pomóc w takich sytuacjach, a _naprawdę_ dogłębną analizę
zostawimy innej dokumentacji.

<!-- Old headings. Do not remove or links may break. -->

<a id="future"></a>

### Trait `Future` {#the-future-trait}

Zacznijmy od bliższego przyjrzenia się temu, jak działa trait `Future`. Oto jak
definiuje go Rust:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Ta definicja traitu zawiera sporo nowych typów, a także trochę składni, której
jeszcze nie widzieliśmy, więc omówmy ją kawałek po kawałku.

Po pierwsze, typ powiązany (*associated type*) `Output` traitu `Future` określa,
jaką wartość ostatecznie da *future* (wartość, która będzie gotowa później).
Jest to odpowiednik typu powiązanego `Item` w traicie `Iterator`. Po drugie,
`Future` ma metodę `poll`, która jako parametr `self` przyjmuje specjalną
referencję (*reference*) `Pin`, a także mutowalną (*mutable*) referencję do
typu `Context`, i zwraca `Poll<Self::Output>`. Więcej o `Pin` i `Context`
powiemy za chwilę. Na razie skupmy się na tym, co zwraca ta metoda, czyli na
typie `Poll`:

```rust
pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

Typ `Poll` przypomina `Option`. Ma jeden wariant zawierający wartość,
`Ready(T)`, i jeden bez wartości, `Pending`. `Poll` oznacza jednak coś zupełnie
innego niż `Option`! Wariant `Pending` wskazuje, że future ma jeszcze pracę do
wykonania, więc kod wywołujący będzie musiał sprawdzić go ponownie później.
Wariant `Ready` wskazuje, że `Future` zakończył pracę i wartość `T` jest
dostępna.

> Uwaga: rzadko trzeba wywoływać `poll` bezpośrednio, ale jeśli musisz to
> zrobić, pamiętaj, że w przypadku większości future’ów kod wywołujący nie
> powinien ponownie wywoływać `poll` po tym, jak future zwrócił `Ready`. Wiele
> future’ów spowoduje panikę (*panic*), jeśli zostaną ponownie odpytane
> (*polled*) po osiągnięciu gotowości. Future’y, które można bezpiecznie
> odpytywać ponownie, wyraźnie informują o tym w swojej dokumentacji. Podobnie
> zachowuje się `Iterator::next`.

Gdy widzisz kod używający `await`, Rust pod spodem kompiluje go do kodu
wywołującego `poll`. Jeśli wrócisz do listingu 17-4, w którym wypisywaliśmy
tytuł strony dla pojedynczego adresu URL, gdy tylko był dostępny, Rust kompiluje
go do czegoś mniej więcej (choć nie dokładnie) takiego:

```rust,ignore
match page_title(url).poll() {
    Ready(page_title) => match page_title {
        Some(title) => println!("The title for {url} was {title}"),
        None => println!("{url} had no title"),
    }
    Pending => {
        // But what goes here?
    }
}
```

Co powinniśmy zrobić, gdy future nadal jest w stanie `Pending`? Potrzebujemy
jakiegoś sposobu, by próbować znowu, i znowu, i znowu, aż future w końcu będzie
gotowy. Innymi słowy, potrzebujemy pętli:

```rust,ignore
let mut page_title_fut = page_title(url);
loop {
    match page_title_fut.poll() {
        Ready(value) => match page_title {
            Some(title) => println!("The title for {url} was {title}"),
            None => println!("{url} had no title"),
        }
        Pending => {
            // continue
        }
    }
}
```

Gdyby jednak Rust kompilował go dokładnie do takiego kodu, każde `await` byłoby
blokujące – a więc działałoby dokładnie odwrotnie, niż chcieliśmy! Zamiast tego
Rust dba o to, by pętla mogła przekazać sterowanie czemuś, co potrafi wstrzymać
pracę nad tym future’em, zająć się innymi future’ami, a później ponownie
sprawdzić ten. Jak już widzieliśmy, tym czymś jest asynchroniczne środowisko
uruchomieniowe (*runtime*), a takie planowanie i koordynowanie pracy to jedno z
jego głównych zadań.

W podrozdziale
[„Przesyłanie danych między dwoma zadaniami za pomocą przekazywania komunikatów”][message-passing]<!-- ignore -->
opisaliśmy oczekiwanie na `rx.recv`. Wywołanie `recv` zwraca
future’a, a oczekiwanie na niego oznacza jego odpytywanie. Zauważyliśmy, że
środowisko uruchomieniowe wstrzyma future’a, dopóki nie będzie on gotowy, dając
`Some(message)` albo – gdy kanał się zamknie – `None`. Teraz, gdy lepiej
rozumiemy trait `Future`, a w szczególności `Future::poll`, widzimy, jak to
działa. Środowisko uruchomieniowe wie, że future nie jest gotowy, gdy zwraca on
`Poll::Pending`. I odwrotnie: środowisko uruchomieniowe wie, że future _jest_
gotowy, i posuwa go naprzód, gdy `poll` zwraca `Poll::Ready(Some(message))` lub
`Poll::Ready(None)`.

Dokładne szczegóły tego, jak środowisko uruchomieniowe to robi, wykraczają poza
ramy tej książki, ale najważniejsze jest zrozumienie podstawowego mechanizmu
działania future’ów: środowisko uruchomieniowe _odpytuje_ każdy future, za który
odpowiada, i z powrotem usypia future’a, gdy ten nie jest jeszcze gotowy.

<!-- Old headings. Do not remove or links may break. -->

<a id="pinning-and-the-pin-and-unpin-traits"></a>
<a id="the-pin-and-unpin-traits"></a>

### Typ `Pin` i trait `Unpin` {#the-pin-type-and-the-unpin-trait}

W listingu 17-13 użyliśmy makra `trpl::join!`, by oczekiwać na trzy future’y.
Często jednak mamy kolekcję, na przykład wektor (*vector*), zawierającą pewną
liczbę future’ów, której nie znamy aż do czasu działania programu. Zmieńmy
listing 17-13 na kod z listingu 17-23, który umieszcza trzy future’y w wektorze
i zamiast tego wywołuje funkcję `trpl::join_all` – ten kod jeszcze się nie
skompiluje.

<Listing number="17-23" caption="Oczekiwanie na future’y w kolekcji"  file-name="src/main.rs">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch17-async-await/listing-17-23/src/main.rs:here}}
```

</Listing>

Każdy future umieszczamy w `Box`, by zrobić z nich _obiekty traitu_ (*trait
objects*), tak jak zrobiliśmy to w podrozdziale „Zwracanie błędów z `run`” w
rozdziale 12. (Obiekty traitu omówimy szczegółowo w rozdziale 18.) Dzięki
obiektom traitu możemy traktować każdy z anonimowych future’ów tworzonych przez
te typy jak ten sam typ, ponieważ wszystkie implementują trait `Future`.

Może to być zaskakujące. W końcu żaden z bloków async niczego nie zwraca, więc
każdy z nich tworzy `Future<Output = ()>`. Pamiętaj jednak, że `Future` to
trait, a kompilator tworzy unikalny *enum* (typ wyliczeniowy) dla każdego bloku
async, nawet jeśli mają identyczne typy wyjściowe. Tak jak nie możesz umieścić w
`Vec` dwóch różnych, ręcznie napisanych struktur (*struct*), tak nie możesz
mieszać enumów wygenerowanych przez kompilator.

Następnie przekazujemy kolekcję future’ów do funkcji `trpl::join_all` i
oczekujemy na wynik. Ten kod się jednak nie kompiluje; oto istotna część
komunikatów o błędach.

<!-- manual-regeneration
cd listings/ch17-async-await/listing-17-23
cargo build
copy *only* the final `error` block from the errors
-->

```text
error[E0277]: `dyn Future<Output = ()>` cannot be unpinned
  --> src/main.rs:48:33
   |
48 |         trpl::join_all(futures).await;
   |                                 ^^^^^ the trait `Unpin` is not implemented for `dyn Future<Output = ()>`
   |
   = note: consider using the `pin!` macro
           consider using `Box::pin` if you need to access the pinned value outside of the current scope
   = note: required for `Box<dyn Future<Output = ()>>` to implement `Future`
note: required by a bound in `futures_util::future::join_all::JoinAll`
  --> file:///home/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/futures-util-0.3.30/src/future/join_all.rs:29:8
   |
27 | pub struct JoinAll<F>
   |            ------- required by a bound in this struct
28 | where
29 |     F: Future,
   |        ^^^^^^ required by this bound in `JoinAll`
```

Notatka w tym komunikacie o błędzie mówi, że powinniśmy użyć makra `pin!`, by
_przypiąć_ (*pin*) wartości, czyli umieścić je w typie `Pin`, który gwarantuje,
że wartości nie zostaną przeniesione (*moved*) w pamięci. Według komunikatu o
błędzie przypięcie jest wymagane, ponieważ `dyn Future<Output = ()>` musi
implementować trait `Unpin`, a obecnie tego nie robi.

Funkcja `trpl::join_all` zwraca strukturę o nazwie `JoinAll`. Ta struktura jest
generyczna względem typu `F`, który musi implementować trait `Future`.
Bezpośrednie oczekiwanie na future’a za pomocą `await` niejawnie go przypina.
Dlatego nie musimy używać `pin!` wszędzie tam, gdzie chcemy oczekiwać na
future’y.

Tutaj jednak nie oczekujemy bezpośrednio na future’a. Zamiast tego tworzymy
nowy future, JoinAll, przekazując kolekcję future’ów do funkcji `join_all`.
Sygnatura `join_all` wymaga, by typy wszystkich elementów kolekcji
implementowały trait `Future`, a `Box<T>` implementuje `Future` tylko wtedy, gdy
opakowany przez niego `T` jest future’em implementującym trait `Unpin`.

Sporo do przyswojenia! Aby naprawdę to zrozumieć, zagłębmy się nieco bardziej w
to, jak faktycznie działa trait `Future`, zwłaszcza w kontekście przypinania.
Spójrz jeszcze raz na definicję traitu `Future`:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

pub trait Future {
    type Output;

    // Required method
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}
```

Parametr `cx` i jego typ `Context` są kluczem do tego, skąd środowisko
uruchomieniowe wie, kiedy sprawdzić dany future, a przy tym pozostaje leniwe
(*lazy*). Szczegóły tego, jak to działa, również wykraczają poza ramy tego
rozdziału i zwykle trzeba o tym myśleć tylko wtedy, gdy piszesz własną
implementację `Future`. Skupimy się zamiast tego na typie `self`, ponieważ po
raz pierwszy widzimy metodę, w której `self` ma adnotację typu. Adnotacja typu
dla `self` działa jak adnotacje typów innych parametrów funkcji, ale z dwiema
kluczowymi różnicami:

- mówi Rustowi, jakiego typu musi być `self`, aby można było wywołać metodę;
- nie może to być dowolny typ – musi to być typ, dla którego zaimplementowano
  metodę, referencja lub inteligentny wskaźnik (*smart pointer*) do tego typu
  albo `Pin` opakowujący referencję do tego typu.

Więcej o tej składni zobaczymy w [rozdziale 18][ch-18]<!-- ignore -->. Na razie
wystarczy wiedzieć, że jeśli chcemy odpytać future’a, by sprawdzić, czy jest w
stanie `Pending`, czy `Ready(Output)`, potrzebujemy mutowalnej referencji do
tego typu opakowanej w `Pin`.

`Pin` to opakowanie dla typów wskaźnikowych, takich jak `&`, `&mut`, `Box` i
`Rc`. (Technicznie rzecz biorąc, `Pin` działa z typami implementującymi traity
`Deref` lub `DerefMut`, ale w praktyce sprowadza się to do pracy wyłącznie z
referencjami i inteligentnymi wskaźnikami.) `Pin` sam nie jest wskaźnikiem i
nie ma własnego zachowania, takiego jak zliczanie referencji (*reference
counting*) w `Rc` i `Arc`; to wyłącznie narzędzie, za pomocą którego kompilator
może wymuszać ograniczenia dotyczące użycia wskaźników.

Pamiętając, że `await` jest zaimplementowane za pomocą wywołań `poll`,
zaczynamy rozumieć komunikat o błędzie, który widzieliśmy wcześniej, ale tamten
dotyczył `Unpin`, a nie `Pin`. Jaki więc dokładnie jest związek między `Pin` a
`Unpin` i dlaczego `Future` wymaga, by `self` było typu `Pin`, aby wywołać
`poll`?

Jak pamiętasz z wcześniejszej części rozdziału, seria punktów oczekiwania w
future’ze jest kompilowana do maszyny stanów, a kompilator pilnuje, by ta
maszyna stanów przestrzegała wszystkich zwykłych reguł bezpieczeństwa Rusta, w
tym zasad pożyczania (*borrowing*) i własności (*ownership*). Aby to działało,
Rust sprawdza, jakie dane są potrzebne między jednym punktem oczekiwania a
następnym punktem oczekiwania albo końcem bloku async. Następnie tworzy
odpowiadający temu wariant w skompilowanej maszynie stanów. Każdy wariant
otrzymuje taki dostęp do danych używanych w danym fragmencie kodu źródłowego,
jakiego potrzebuje – czy to przejmując własność tych danych, czy uzyskując do
nich mutowalną lub niemutowalną referencję.

Jak dotąd wszystko w porządku: jeśli popełnimy jakiś błąd dotyczący własności
lub referencji w danym bloku async, *borrow checker* (mechanizm sprawdzania
pożyczeń) nam o tym powie. Sprawy komplikują się, gdy chcemy przenosić future
odpowiadający temu blokowi – na przykład przenieść go do
`Vec`, by przekazać go do `join_all`.

Gdy przenosimy future’a – czy to umieszczając go w strukturze danych, by użyć
jej jako iteratora z `join_all`, czy zwracając go z funkcji – w rzeczywistości
oznacza to przeniesienie maszyny stanów, którą Rust dla nas tworzy. W
odróżnieniu od większości innych typów w Ruście, future’y tworzone przez Rusta
dla bloków async mogą zawierać w polach dowolnego wariantu referencje do samych
siebie, co pokazuje uproszczona ilustracja na rysunku 17-4.

<figure>

<img alt="Jednokolumnowa tabela o trzech wierszach przedstawiająca future fut1, który ma wartości 0 i 1 w dwóch pierwszych wierszach oraz strzałkę wskazującą z trzeciego wiersza z powrotem na drugi wiersz, co oznacza wewnętrzną referencję w obrębie future’a." src="img/trpl17-04.svg" class="center" />

<figcaption>Rysunek 17-4: Samoreferencyjny typ danych</figcaption>

</figure>

Domyślnie jednak przenoszenie dowolnego obiektu, który zawiera referencję do
samego siebie, jest niebezpieczne, ponieważ referencje zawsze wskazują na
faktyczny adres w pamięci tego, do czego się odnoszą (zob. rysunek 17-5). Jeśli
przeniesiesz samą strukturę danych, te wewnętrzne referencje nadal będą
wskazywać na stare miejsce. To miejsce w pamięci jest jednak teraz
nieprawidłowe. Po pierwsze, jego wartość nie będzie aktualizowana, gdy
wprowadzisz zmiany w strukturze danych. Po drugie – co ważniejsze – komputer
może teraz wykorzystać tę pamięć do innych celów! Mogłoby się skończyć tym, że
później odczytasz zupełnie niezwiązane dane.

<figure>

<img alt="Dwie tabele przedstawiające dwa future’y, fut1 i fut2, z których każda ma jedną kolumnę i trzy wiersze, co obrazuje skutek przeniesienia future’a z fut1 do fut2. Pierwsza, fut1, jest wyszarzona, a w każdym polu ma znak zapytania, co oznacza nieznaną zawartość pamięci. Druga, fut2, ma 0 i 1 w pierwszym i drugim wierszu oraz strzałkę wskazującą z trzeciego wiersza z powrotem na drugi wiersz fut1, co oznacza wskaźnik odwołujący się do starego miejsca w pamięci, w którym future znajdował się przed przeniesieniem." src="img/trpl17-05.svg" class="center" />

<figcaption>Rysunek 17-5: Niebezpieczny skutek przeniesienia samoreferencyjnego typu danych</figcaption>

</figure>

Teoretycznie kompilator Rusta mógłby próbować aktualizować każdą referencję do
obiektu za każdym razem, gdy ten zostaje przeniesiony, ale mogłoby to znacznie
obniżyć wydajność, zwłaszcza gdyby trzeba było aktualizować całą sieć
referencji. Gdybyśmy zamiast tego mogli zagwarantować, że dana struktura danych
_nie przemieszcza się w pamięci_, nie musielibyśmy aktualizować żadnych
referencji. Właśnie do tego służy *borrow checker* Rusta: w bezpiecznym kodzie
nie pozwala przenieść żadnego elementu, do którego istnieje aktywna referencja.

`Pin` bazuje na tym mechanizmie i daje nam dokładnie taką gwarancję, jakiej
potrzebujemy. Gdy _przypinamy_ wartość, opakowując wskaźnik do niej w `Pin`,
nie może się ona już przemieszczać. Jeśli więc masz `Pin<Box<SomeType>>`, w
rzeczywistości przypinasz wartość `SomeType`, _a nie_ wskaźnik `Box`. Ten
proces ilustruje rysunek 17-6.

<figure>

<img alt="Trzy prostokąty ułożone obok siebie. Pierwszy ma etykietę „Pin”, drugi „b1”, a trzeci „pinned”. Wewnątrz „pinned” znajduje się tabela z etykietą „fut”, z jedną kolumną; przedstawia ona future z komórkami dla poszczególnych części struktury danych. Pierwsza komórka ma wartość „0”, z drugiej wychodzi strzałka wskazująca na czwartą, ostatnią komórkę, która zawiera wartość „1”, a trzecia komórka ma przerywane linie i wielokropek, co oznacza, że struktura danych może mieć jeszcze inne części. Tabela „fut” jako całość przedstawia future, który jest samoreferencyjny. Strzałka wychodzi z prostokąta „Pin”, przechodzi przez prostokąt „b1” i kończy się wewnątrz prostokąta „pinned” na tabeli „fut”." src="img/trpl17-06.svg" class="center" />

<figcaption>Rysunek 17-6: Przypinanie `Box`, który wskazuje na samoreferencyjny typ future’a</figcaption>

</figure>

W rzeczywistości wskaźnik `Box` nadal może się swobodnie przemieszczać.
Pamiętaj: zależy nam na tym, by dane, do których ostatecznie się odwołujemy,
pozostały na miejscu. Jeśli wskaźnik się przemieszcza, _ale dane, na które
wskazuje_, pozostają w tym samym miejscu, jak na rysunku 17-7, nie ma żadnego
potencjalnego problemu. (W ramach samodzielnego ćwiczenia przejrzyj
dokumentację tych typów oraz modułu `std::pin` i spróbuj ustalić, jak zrobić to
z `Pin` opakowującym `Box`.) Najważniejsze jest to, że sam samoreferencyjny typ
nie może się przemieszczać, ponieważ nadal jest przypięty.

<figure>

<img alt="Cztery prostokąty ułożone w mniej więcej trzech kolumnach, identyczne jak na poprzednim diagramie, z wyjątkiem drugiej kolumny. Teraz w drugiej kolumnie są dwa prostokąty z etykietami „b1” i „b2”, „b1” jest wyszarzony, a strzałka z „Pin” przechodzi przez „b2” zamiast przez „b1”, co oznacza, że wskaźnik został przeniesiony z „b1” do „b2”, ale dane w „pinned” się nie przemieściły." src="img/trpl17-07.svg" class="center" />

<figcaption>Rysunek 17-7: Przenoszenie `Box`, który wskazuje na samoreferencyjny typ future’a</figcaption>

</figure>

Większość typów można jednak całkowicie bezpiecznie przenosić, nawet jeśli
akurat znajdują się za wskaźnikiem `Pin`. O przypinaniu musimy myśleć tylko
wtedy, gdy elementy zawierają wewnętrzne referencje. Wartości prymitywne, takie
jak liczby i wartości logiczne, są bezpieczne, ponieważ oczywiście nie mają
żadnych wewnętrznych referencji. Nie ma ich też większość typów, z którymi
zwykle pracujesz w Ruście. Możesz na przykład bez obaw przenosić `Vec`. Biorąc
pod uwagę to, co widzieliśmy do tej pory, mając `Pin<Vec<String>>`, trzeba by
robić wszystko za pomocą bezpiecznych, ale restrykcyjnych API
udostępnianych przez `Pin`, mimo że `Vec<String>` zawsze można bezpiecznie
przenieść, jeśli nie istnieją do niego żadne inne referencje. Potrzebujemy
sposobu, by powiedzieć kompilatorowi, że w takich przypadkach można swobodnie
przenosić elementy – i tu do gry wkracza `Unpin`.

`Unpin` to trait znacznikowy (*marker trait*), podobny do traitów `Send` i
`Sync`, które poznaliśmy w rozdziale 16, a więc sam nie ma żadnej
funkcjonalności. Traity znacznikowe istnieją wyłącznie po to, by poinformować
kompilator, że typu implementującego dany trait można bezpiecznie używać w
określonym kontekście. `Unpin` informuje kompilator, że dany typ _nie_ musi
zapewniać żadnych gwarancji co do tego, czy daną wartość można bezpiecznie
przenieść.

<!--
  The inline `<code>` in the next block is to allow the inline `<em>` inside it,
  matching what NoStarch does style-wise, and emphasizing within the text here
  that it is something distinct from a normal type.
-->

Podobnie jak w przypadku `Send` i `Sync`, kompilator automatycznie implementuje
`Unpin` dla wszystkich typów, dla których może udowodnić, że jest to
bezpieczne. Szczególnym przypadkiem, znów podobnie jak przy `Send` i `Sync`,
jest sytuacja, w której `Unpin` _nie_ jest zaimplementowany dla danego typu.
Zapisuje się to jako <code>impl !Unpin for <em>SomeType</em></code>, gdzie
<code><em>SomeType</em></code> to nazwa typu, który _musi_ zapewniać te
gwarancje, by był bezpieczny za każdym razem, gdy wskaźnik do tego typu jest
używany w `Pin`.

Innymi słowy, w związku między `Pin` a `Unpin` trzeba pamiętać o dwóch
rzeczach. Po pierwsze, `Unpin` to przypadek „normalny”, a `!Unpin` – przypadek
szczególny. Po drugie, to, czy typ implementuje `Unpin`, czy `!Unpin`, ma
znaczenie _tylko_ wtedy, gdy używasz przypiętego wskaźnika do tego typu, takiego
jak <code>Pin<&mut
<em>SomeType</em>></code>.

Aby to skonkretyzować, pomyśl o `String`: ma on długość i znaki Unicode, z
których się składa. Możemy opakować `String` w `Pin`, jak widać na rysunku
17-8. `String` automatycznie implementuje jednak `Unpin`, podobnie jak
większość innych typów w Ruście.

<figure>

<img alt="Prostokąt z etykietą „Pin” po lewej stronie ze strzałką prowadzącą do prostokąta z etykietą „String” po prawej. Prostokąt „String” zawiera dane 5usize, oznaczające długość łańcucha, oraz litery „h”, „e”, „l”, „l” i „o”, oznaczające znaki łańcucha „hello” przechowywanego w tej instancji String. Prostokąt „String” wraz z etykietą otacza kropkowana ramka, która nie obejmuje prostokąta „Pin”." src="img/trpl17-08.svg" class="center" />

<figcaption>Rysunek 17-8: Przypinanie `String`; kropkowana linia oznacza, że `String` implementuje trait `Unpin`, a więc nie jest przypięty</figcaption>

</figure>

Dzięki temu możemy robić rzeczy, które byłyby niedozwolone, gdyby `String`
zamiast tego implementował `!Unpin`, na przykład zastąpić jeden łańcuch znaków
(*string*) innym dokładnie w tym samym miejscu w pamięci, jak na rysunku 17-9.
Nie narusza to kontraktu `Pin`, ponieważ `String` nie ma wewnętrznych
referencji, które sprawiałyby, że jego przenoszenie byłoby niebezpieczne.
Właśnie dlatego implementuje `Unpin`, a nie `!Unpin`.

<figure>

<img alt="Te same dane łańcucha „hello” z poprzedniego przykładu, teraz z etykietą „s1” i wyszarzone. Prostokąt „Pin” z poprzedniego przykładu wskazuje teraz na inną instancję String, z etykietą „s2”, która jest prawidłowa, ma długość 7usize i zawiera znaki łańcucha „goodbye”. s2 otacza kropkowana ramka, ponieważ ta instancja również implementuje trait Unpin." src="img/trpl17-09.svg" class="center" />

<figcaption>Rysunek 17-9: Zastąpienie `String` zupełnie innym `String` w pamięci</figcaption>

</figure>

Wiemy już wystarczająco dużo, by zrozumieć błędy zgłoszone dla wywołania
`join_all` z listingu 17-23. Początkowo próbowaliśmy przenieść future’y
tworzone przez bloki async do `Vec<Box<dyn Future<Output = ()>>>`, ale jak
widzieliśmy, te future’y mogą zawierać wewnętrzne referencje, więc nie
implementują automatycznie `Unpin`. Gdy je przypniemy, możemy przekazać
powstały typ `Pin` do `Vec`, mając pewność, że dane wewnątrz future’ów _nie_
zostaną przeniesione. Listing 17-24 pokazuje, jak naprawić kod, wywołując makro
`pin!` w miejscu definicji każdego z trzech future’ów i dostosowując typ
obiektu traitu.

<Listing number="17-24" caption="Przypinanie future’ów, aby można je było przenieść do wektora">

```rust
{{#rustdoc_include ../listings/ch17-async-await/listing-17-24/src/main.rs:here}}
```

</Listing>

Ten przykład teraz się kompiluje i działa, a w czasie działania programu
moglibyśmy dodawać future’y do wektora lub je z niego usuwać i połączyć je
wszystkie.

`Pin` i `Unpin` mają znaczenie głównie przy tworzeniu bibliotek niższego
poziomu albo przy budowaniu samego środowiska uruchomieniowego, a nie w
codziennym kodzie w Ruście. Gdy jednak zobaczysz te traity w komunikatach o
błędach, będziesz już lepiej wiedzieć, jak naprawić swój kod!

> Uwaga: to połączenie `Pin` i `Unpin` umożliwia bezpieczne zaimplementowanie w
> Ruście całej klasy złożonych typów, które w przeciwnym razie byłyby trudne do
> zaimplementowania, ponieważ są samoreferencyjne. Typy wymagające `Pin`
> pojawiają się dziś najczęściej w asynchronicznym Ruście, ale od czasu do czasu
> możesz je spotkać także w innych kontekstach.
>
> Szczegóły działania `Pin` i `Unpin` oraz reguły, których muszą przestrzegać,
> są obszernie opisane w dokumentacji API modułu `std::pin`, więc jeśli chcesz
> dowiedzieć się więcej, to świetne miejsce na początek.
>
> Jeśli chcesz jeszcze dokładniej zrozumieć, jak to wszystko działa od środka,
> zajrzyj do rozdziałów [2][under-the-hood]<!-- ignore --> i
> [4][pinning]<!-- ignore --> książki
> [_Asynchronous Programming in Rust_][async-book].

### Trait `Stream` {#the-stream-trait}

Teraz, gdy lepiej rozumiesz traity `Future`, `Pin` i `Unpin`, możemy zająć się
traitem `Stream`. Jak wiesz z wcześniejszej części rozdziału, strumienie
(*stream*) przypominają asynchroniczne iteratory. W odróżnieniu od `Iterator` i
`Future`, `Stream` w chwili pisania tej książki nie ma jednak definicji w
bibliotece standardowej, ale _istnieje_ bardzo popularna definicja z *crate*’a
(jednostki kompilacji w Ruście) `futures`, używana w całym ekosystemie.

Przypomnijmy definicje traitów `Iterator` i `Future`, zanim przyjrzymy się temu,
jak trait `Stream` mógłby je połączyć. Z `Iterator` bierzemy ideę sekwencji:
jego metoda `next` dostarcza `Option<Self::Item>`. Z `Future` bierzemy ideę
gotowości w czasie: jego metoda `poll` dostarcza `Poll<Self::Output>`. Aby
reprezentować sekwencję elementów, które z czasem stają się gotowe, definiujemy
trait `Stream`, który łączy obie te idee:

```rust
use std::pin::Pin;
use std::task::{Context, Poll};

trait Stream {
    type Item;

    fn poll_next(
        self: Pin<&mut Self>,
        cx: &mut Context<'_>
    ) -> Poll<Option<Self::Item>>;
}
```

Trait `Stream` definiuje typ powiązany o nazwie `Item`, określający typ
elementów produkowanych przez strumień. Przypomina to `Iterator`, w którym może
być od zera do wielu elementów, a różni się od `Future`, w którym zawsze jest
dokładnie jeden `Output`, nawet jeśli jest to typ jednostkowy (*unit type*)
`()`.

`Stream` definiuje też metodę do pobierania tych elementów. Nazywamy ją
`poll_next`, by było jasne, że odpytuje w ten sam sposób co `Future::poll` i
produkuje sekwencję elementów w ten sam sposób co `Iterator::next`. Jej typ
zwracany łączy `Poll` z `Option`. Typem zewnętrznym jest `Poll`, ponieważ trzeba
sprawdzać jego gotowość, tak jak w przypadku future’a. Typem wewnętrznym jest
`Option`, ponieważ musi on sygnalizować, czy są kolejne komunikaty, tak jak
robi to iterator.

Coś bardzo podobnego do tej definicji najprawdopodobniej trafi w końcu do
biblioteki standardowej Rusta. Tymczasem jest to część zestawu narzędzi
większości środowisk uruchomieniowych, więc możesz na tym polegać, a wszystko,
co omówimy dalej, powinno zasadniczo mieć zastosowanie!

W przykładach z podrozdziału [„Strumienie: future’y w sekwencji”][streams]<!--
ignore --> nie używaliśmy jednak `poll_next` _ani_ `Stream`, tylko `next` i
`StreamExt`. _Moglibyśmy_ oczywiście pracować bezpośrednio z API `poll_next`,
ręcznie pisząc własne maszyny stanów dla `Stream`, tak samo jak _moglibyśmy_
pracować z future’ami bezpośrednio za pomocą ich metody `poll`. Używanie
`await` jest jednak znacznie wygodniejsze, a trait `StreamExt` dostarcza metodę
`next`, dzięki której możemy właśnie tak robić:

```rust
{{#rustdoc_include ../listings/ch17-async-await/no-listing-stream-ext/src/lib.rs:here}}
```

<!--
TODO: update this if/when tokio/etc. update their MSRV and switch to using async functions
in traits, since the lack thereof is the reason they do not yet have this.
-->

> Uwaga: faktyczna definicja, której używaliśmy wcześniej w tym rozdziale,
> wygląda nieco inaczej, ponieważ obsługuje wersje Rusta, które nie pozwalały
> jeszcze używać funkcji asynchronicznych w traitach. W rezultacie wygląda tak:
>
> ```rust,ignore
> fn next(&mut self) -> Next<'_, Self> where Self: Unpin;
> ```
>
> Typ `Next` to `struct`, który implementuje `Future` i pozwala nazwać czas
> życia (*lifetime*) referencji do `self` za pomocą `Next<'_, Self>`, tak aby
> `await` mogło działać z tą metodą.

Trait `StreamExt` jest też miejscem, w którym znajdują się wszystkie ciekawe
metody dostępne do pracy ze strumieniami. `StreamExt` jest automatycznie
implementowany dla każdego typu implementującego `Stream`, ale te traity są
zdefiniowane osobno, aby społeczność mogła rozwijać wygodne API bez wpływu na
podstawowy trait.

W wersji `StreamExt` używanej w crate’cie `trpl` trait nie tylko definiuje
metodę `next`, ale też dostarcza domyślną implementację `next`, która poprawnie
obsługuje szczegóły wywoływania `Stream::poll_next`. Oznacza to, że nawet gdy
musisz napisać własny strumieniowy typ danych, wystarczy, że zaimplementujesz
_tylko_ `Stream`, a wtedy każdy, kto używa twojego typu danych, będzie mógł
automatycznie używać z nim `StreamExt` i jego metod.

To wszystko, co omówimy na temat niskopoziomowych szczegółów tych traitów. Na
zakończenie zastanówmy się, jak future’y (w tym strumienie), zadania i wątki
współgrają ze sobą!

{{#quiz ../quizzes/async-05-traits-for-async.toml}}

[message-passing]: ch17-02-concurrency-with-async.md#sending-data-between-two-tasks-using-message-passing
[ch-18]: ch18-00-oop.html
[async-book]: https://rust-lang.github.io/async-book/
[under-the-hood]: https://rust-lang.github.io/async-book/02_execution/01_chapter.html
[pinning]: https://rust-lang.github.io/async-book/04_pinning/01_chapter.html
[first-async]: ch17-01-futures-and-syntax.html#our-first-async-program
[any-number-futures]: ch17-03-more-futures.html#working-with-any-number-of-futures
[streams]: ch17-04-streams.html

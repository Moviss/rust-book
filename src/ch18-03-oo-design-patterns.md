## Implementacja obiektowego wzorca projektowego {#implementing-an-object-oriented-design-pattern}

_Wzorzec stanu_ (*state pattern*) to obiektowy wzorzec projektowy. Jego istota
polega na tym, że definiujemy zbiór stanów, w których wewnętrznie może się
znajdować dana wartość. Stany są reprezentowane przez zbiór _obiektów stanu_
(*state objects*), a zachowanie wartości zmienia się w zależności od jej stanu.
Przeanalizujemy przykład struktury (*struct*) reprezentującej wpis na blogu,
która ma pole przechowujące jej stan – obiekt stanu ze zbioru „szkic”,
„recenzja” lub „opublikowany”.

Obiekty stanu współdzielą funkcjonalność – w Ruście oczywiście zamiast obiektów
i dziedziczenia (*inheritance*) używamy struktur i *traitów* (cech typów,
zbliżonych do interfejsów). Każdy obiekt stanu odpowiada za własne zachowanie i
za decyzję, kiedy powinien przejść w inny stan. Wartość przechowująca obiekt
stanu nie wie nic o różnych zachowaniach stanów ani o tym, kiedy przechodzić
między nimi.

Zaletą wzorca stanu jest to, że gdy zmienią się wymagania biznesowe wobec
programu, nie trzeba będzie zmieniać kodu wartości przechowującej stan ani kodu,
który z tej wartości korzysta. Wystarczy zaktualizować kod w jednym z obiektów
stanu, aby zmienić jego reguły, ewentualnie dodać kolejne obiekty stanu.

Najpierw zaimplementujemy wzorzec stanu w bardziej tradycyjny, obiektowy sposób.
Potem zastosujemy podejście nieco bardziej naturalne dla Rusta. Zabierzmy się
do stopniowej implementacji procesu publikacji wpisu na blogu z użyciem wzorca
stanu.

Docelowa funkcjonalność będzie wyglądać tak:

1. Wpis na blogu zaczyna jako pusty szkic.
1. Gdy szkic jest gotowy, wysyłana jest prośba o recenzję wpisu.
1. Gdy wpis zostanie zatwierdzony, zostaje opublikowany.
1. Tylko opublikowane wpisy zwracają treść do wyświetlenia, dzięki czemu
   niezatwierdzone wpisy nie mogą zostać przypadkowo opublikowane.

Wszelkie inne próby zmiany wpisu nie powinny przynosić żadnego efektu. Jeśli na
przykład spróbujemy zatwierdzić szkic wpisu, zanim poprosimy o recenzję, wpis
powinien pozostać nieopublikowanym szkicem.

<!-- Old headings. Do not remove or links may break. -->

<a id="a-traditional-object-oriented-attempt"></a>

### Próba w tradycyjnym stylu obiektowym {#attempting-traditional-object-oriented-style}

Kod rozwiązujący ten sam problem można ustrukturyzować na nieskończenie wiele
sposobów, a każdy z nich wiąże się z innymi kompromisami. Implementacja z tego
podrozdziału jest napisana raczej w tradycyjnym stylu obiektowym, który da się
zastosować w Ruście, ale który nie wykorzystuje niektórych mocnych stron Rusta.
Później pokażemy inne rozwiązanie, które nadal korzysta z obiektowego wzorca
projektowego, ale jest zbudowane w sposób, który programistom z doświadczeniem
w programowaniu obiektowym może się wydać mniej znajomy. Porównamy oba
rozwiązania, aby przekonać się, jakie kompromisy wiążą się z projektowaniem kodu
w Ruście inaczej niż w innych językach.

Listing 18-11 przedstawia ten proces w postaci kodu – to przykładowe użycie API,
które zaimplementujemy w bibliotecznym *crate’cie* (jednostce kompilacji w
Ruście) o nazwie `blog`. Ten kod jeszcze się nie skompiluje, bo nie
zaimplementowaliśmy crate’a `blog`.

<Listing number="18-11" file-name="src/main.rs" caption="Kod pokazujący pożądane zachowanie crate’a `blog`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:all}}
```

</Listing>

Chcemy, aby użytkownik mógł utworzyć nowy szkic wpisu za pomocą `Post::new`.
Chcemy też umożliwić dodawanie tekstu do wpisu. Jeśli spróbujemy pobrać treść
wpisu od razu, przed zatwierdzeniem, nie powinniśmy dostać żadnego tekstu, bo
wpis jest wciąż szkicem. Dla celów demonstracyjnych dodaliśmy do kodu
`assert_eq!`. Doskonałym testem jednostkowym byłoby tu sprawdzenie, że szkic
wpisu zwraca z metody `content` pusty łańcuch znaków (*string*), ale w tym
przykładzie nie będziemy pisać testów.

Następnie chcemy umożliwić wysłanie prośby o recenzję wpisu i chcemy, aby
`content` zwracała pusty łańcuch, dopóki wpis czeka na recenzję. Gdy wpis
zostanie zatwierdzony, powinien zostać opublikowany, co oznacza, że wywołanie
`content` zwróci tekst wpisu.

Zwróć uwagę, że jedynym typem z crate’a, z którym wchodzimy w interakcję, jest
typ `Post`. Ten typ będzie korzystał ze wzorca stanu i będzie przechowywał
wartość będącą jednym z trzech obiektów stanu reprezentujących możliwe stany
wpisu – szkic, recenzję lub publikację. Zmiana jednego stanu w inny będzie
zarządzana wewnętrznie w typie `Post`. Stany zmieniają się w odpowiedzi na
metody wywoływane przez użytkowników naszej biblioteki na instancji `Post`, ale
użytkownicy nie muszą bezpośrednio zarządzać zmianami stanu. Nie mogą też
popełnić błędu związanego ze stanami, takiego jak opublikowanie wpisu przed
recenzją.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-post-and-creating-a-new-instance-in-the-draft-state"></a>

#### Definicja `Post` i tworzenie nowej instancji {#defining-post-and-creating-a-new-instance}

Zacznijmy implementować bibliotekę! Wiemy, że potrzebujemy publicznej struktury
`Post` przechowującej jakąś treść, więc zaczniemy od definicji tej struktury i
publicznej funkcji powiązanej (*associated function*) `new` tworzącej instancję
`Post`, jak pokazano w listingu 18-12. Utworzymy też prywatny trait `State`, który będzie
definiował zachowanie wymagane od wszystkich obiektów stanu dla `Post`.

Następnie `Post` będzie przechowywać obiekt traitu (*trait object*)
`Box<dyn State>` wewnątrz `Option<T>` w prywatnym polu o nazwie `state`, aby
przechowywać obiekt stanu. Za chwilę zobaczysz, dlaczego `Option<T>` jest
potrzebne.

<Listing number="18-12" file-name="src/lib.rs" caption="Definicja struktury `Post` i funkcji `new` tworzącej nową instancję `Post`, traitu `State` oraz struktury `Draft`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-12/src/lib.rs}}
```

</Listing>

Trait `State` definiuje zachowanie współdzielone przez różne stany wpisu.
Obiektami stanu są `Draft`, `PendingReview` i `Published` – wszystkie będą
implementować trait `State`. Na razie trait nie ma żadnych metod, a zaczniemy od
zdefiniowania tylko stanu `Draft`, bo to w nim wpis ma rozpoczynać istnienie.

Gdy tworzymy nowy `Post`, ustawiamy jego pole `state` na wartość `Some`
przechowującą `Box`. Ten `Box` wskazuje na nową instancję struktury `Draft`.
Dzięki temu każda nowa instancja `Post` zaczyna jako szkic. Ponieważ pole
`state` w `Post` jest prywatne, nie da się utworzyć `Post` w żadnym innym
stanie! W funkcji `Post::new` ustawiamy pole `content` na nowy, pusty `String`.

#### Przechowywanie tekstu treści wpisu {#storing-the-text-of-the-post-content}

W listingu 18-11 widzieliśmy, że chcemy mieć możliwość wywołania metody o
nazwie `add_text` i przekazania jej wartości `&str`, która zostanie dodana jako
treść tekstowa wpisu na blogu. Implementujemy to jako metodę, zamiast udostępniać
pole `content` jako `pub`, aby później móc zaimplementować metodę kontrolującą
sposób odczytu danych z pola `content`. Metoda `add_text` jest dość prosta, więc
dodajmy implementację z listingu 18-13 do bloku `impl Post`.

<Listing number="18-13" file-name="src/lib.rs" caption="Implementacja metody `add_text` dodającej tekst do pola `content` wpisu">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-13/src/lib.rs:here}}
```

</Listing>

Metoda `add_text` przyjmuje mutowalną (*mutable*) referencję (*reference*) do
`self`, bo zmieniamy instancję `Post`, na której wywołujemy `add_text`.
Następnie wywołujemy `push_str` na wartości `String` w `content` i przekazujemy
argument `text`, aby dodać go do zapisanej treści `content`. To zachowanie nie
zależy od stanu, w jakim jest wpis, więc nie jest częścią wzorca stanu. Metoda
`add_text` w ogóle nie korzysta z pola `state`, ale należy do zachowania, które
chcemy obsługiwać.

<!-- Old headings. Do not remove or links may break. -->

<a id="ensuring-the-content-of-a-draft-post-is-empty"></a>

#### Zapewnienie, że treść szkicu jest pusta {#ensuring-that-the-content-of-a-draft-post-is-empty}

Nawet po wywołaniu `add_text` i dodaniu treści do wpisu chcemy, aby metoda
`content` zwracała pusty wycinek łańcucha (*string slice*), bo wpis jest wciąż
w stanie szkicu, jak pokazuje pierwsze `assert_eq!` w listingu 18-11. Na razie
zaimplementujmy metodę `content` w najprostszy sposób, który spełni ten
wymóg: niech zawsze zwraca pusty wycinek łańcucha. Zmienimy to później, gdy
zaimplementujemy możliwość zmiany stanu wpisu, tak aby dało się go opublikować.
Na razie wpisy mogą być tylko w stanie szkicu, więc ich treść powinna być zawsze
pusta. Listing 18-14 przedstawia tę tymczasową implementację.

<Listing number="18-14" file-name="src/lib.rs" caption="Dodanie tymczasowej implementacji metody `content` w `Post`, która zawsze zwraca pusty wycinek łańcucha">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-14/src/lib.rs:here}}
```

</Listing>

Po dodaniu metody `content` wszystko w listingu 18-11 aż do pierwszego
`assert_eq!` działa zgodnie z zamierzeniem.

<!-- Old headings. Do not remove or links may break. -->

<a id="requesting-a-review-of-the-post-changes-its-state"></a>
<a id="requesting-a-review-changes-the-posts-state"></a>

#### Prośba o recenzję, która zmienia stan wpisu {#requesting-a-review-which-changes-the-posts-state}

Następnie musimy dodać funkcjonalność wysyłania prośby o recenzję wpisu, która
powinna zmienić jego stan z `Draft` na `PendingReview`. Listing 18-15 pokazuje
ten kod.

<Listing number="18-15" file-name="src/lib.rs" caption="Implementacja metod `request_review` w `Post` i w traicie `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-15/src/lib.rs:here}}
```

</Listing>

Dajemy `Post` publiczną metodę o nazwie `request_review`, która przyjmuje
mutowalną referencję do `self`. Następnie wywołujemy wewnętrzną metodę
`request_review` na bieżącym stanie `Post`, a ta druga metoda `request_review`
konsumuje bieżący stan i zwraca nowy.

Dodajemy metodę `request_review` do traitu `State`; wszystkie typy
implementujące ten trait będą teraz musiały zaimplementować metodę
`request_review`. Zwróć uwagę, że zamiast `self`, `&self` czy `&mut self` jako
pierwszy parametr metody mamy `self: Box<Self>`. Ta składnia oznacza, że metoda
jest poprawna tylko wtedy, gdy zostanie wywołana na `Box` przechowującym dany
typ. Ta składnia przejmuje własność (*ownership*) `Box<Self>`, unieważniając
stary stan, dzięki czemu wartość stanu w `Post` może się przekształcić w nowy
stan.

Aby skonsumować stary stan, metoda `request_review` musi przejąć własność
wartości stanu. Tu przydaje się `Option` w polu `state` struktury `Post`:
wywołujemy metodę `take`, aby wyjąć wartość `Some` z pola `state` i zostawić na
jej miejscu `None`, ponieważ Rust nie pozwala na niewypełnione pola w
strukturach. Dzięki temu możemy przenieść (*move*) wartość `state` z `Post`,
zamiast ją pożyczać (*borrow*). Następnie ustawiamy wartość `state` wpisu na
wynik tej operacji.

Musimy tymczasowo ustawić `state` na `None`, zamiast ustawiać je bezpośrednio
kodem w rodzaju `self.state = self.state.request_review();`, aby uzyskać
własność wartości `state`. Dzięki temu `Post` nie może użyć starej wartości
`state` po tym, jak przekształciliśmy ją w nowy stan.

Metoda `request_review` w `Draft` zwraca nową instancję nowej struktury
`PendingReview` opakowaną w *box* (wskaźnik na dane umieszczone na stercie);
struktura ta reprezentuje stan, w którym wpis czeka na recenzję. Struktura
`PendingReview` również implementuje metodę `request_review`, ale nie wykonuje
żadnych przekształceń. Zwraca samą siebie, bo jeśli poprosimy o recenzję wpisu,
który jest już w stanie `PendingReview`, powinien on pozostać w stanie
`PendingReview`.

Teraz zaczynamy dostrzegać zalety wzorca stanu: metoda `request_review` w
`Post` jest taka sama niezależnie od wartości `state`. Każdy stan odpowiada za
własne reguły.

Metodę `content` w `Post` zostawimy bez zmian – nadal zwraca pusty wycinek
łańcucha. Teraz `Post` może być zarówno w stanie `PendingReview`, jak i w
stanie `Draft`, ale w stanie `PendingReview` chcemy takiego samego zachowania.
Listing 18-11 działa teraz aż do drugiego wywołania `assert_eq!`!

<!-- Old headings. Do not remove or links may break. -->

<a id="adding-the-approve-method-that-changes-the-behavior-of-content"></a>
<a id="adding-approve-to-change-the-behavior-of-content"></a>

#### Dodanie `approve` w celu zmiany zachowania `content` {#adding-approve-to-change-contents-behavior}

Metoda `approve` będzie podobna do metody `request_review`: ustawi `state` na
wartość, którą według bieżącego stanu powinno ono mieć po zatwierdzeniu, jak
pokazano w listingu 18-16.

<Listing number="18-16" file-name="src/lib.rs" caption="Implementacja metody `approve` w `Post` i w traicie `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-16/src/lib.rs:here}}
```

</Listing>

Dodajemy metodę `approve` do traitu `State` oraz nową strukturę implementującą
`State` – stan `Published`.

Podobnie jak w przypadku `request_review` w `PendingReview`, wywołanie metody
`approve` na `Draft` nie przyniesie żadnego efektu, bo `approve` zwróci `self`.
Gdy wywołamy `approve` na `PendingReview`, zwróci ona nową instancję struktury
`Published` opakowaną w box. Struktura `Published` implementuje trait `State`, a
zarówno metoda `request_review`, jak i metoda `approve` zwracają w niej samą
strukturę, bo w takich przypadkach wpis powinien pozostać w stanie `Published`.

Teraz musimy zaktualizować metodę `content` w `Post`. Chcemy, aby wartość
zwracana z `content` zależała od bieżącego stanu `Post`, więc `Post` będzie
delegować wywołanie do metody `content` zdefiniowanej na jego `state`, jak
pokazano w listingu 18-17.

<Listing number="18-17" file-name="src/lib.rs" caption="Zmiana metody `content` w `Post` tak, aby delegowała wywołanie do metody `content` w `State`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch18-oop/listing-18-17/src/lib.rs:here}}
```

</Listing>

Ponieważ chcemy, aby wszystkie te reguły znajdowały się w strukturach
implementujących `State`, wywołujemy metodę `content` na wartości w `state` i
przekazujemy jako argument instancję wpisu (czyli `self`). Następnie zwracamy
wartość zwróconą przez metodę `content` wywołaną na wartości `state`.

Wywołujemy metodę `as_ref` na `Option`, bo chcemy uzyskać referencję do
wartości wewnątrz `Option`, a nie własność tej wartości. Ponieważ `state` jest
typu `Option<Box<dyn State>>`, wywołanie `as_ref` zwraca
`Option<&Box<dyn State>>`. Gdybyśmy nie wywołali `as_ref`, dostalibyśmy błąd,
bo nie możemy przenieść `state` z pożyczonego `&self` będącego parametrem funkcji.

Następnie wywołujemy metodę `unwrap`, o której wiemy, że nigdy nie spowoduje
paniki (*panic*), bo wiemy, że metody `Post` gwarantują, iż po ich zakończeniu
`state` zawsze będzie zawierać wartość `Some`. To jeden z przypadków, o których
mówiliśmy w podrozdziale [„Gdy wiesz więcej niż
kompilator”][more-info-than-rustc]<!-- ignore --> w rozdziale 9: wiemy, że
wartość `None` nigdy nie wystąpi, mimo że kompilator nie jest w stanie tego
zrozumieć.

W tym momencie, gdy wywołujemy `content` na `&Box<dyn State>`, na `&` i `Box`
zadziała *deref coercion* (automatyczna konwersja przez dereferencję), dzięki
czemu metoda `content` zostanie ostatecznie wywołana na typie implementującym
trait `State`. Oznacza to, że musimy dodać `content` do definicji traitu
`State` – i to tam umieścimy logikę decydującą o tym, jaką treść zwrócić w
zależności od bieżącego stanu, jak pokazano w listingu 18-18.

<Listing number="18-18" file-name="src/lib.rs" caption="Dodanie metody `content` do traitu `State`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-18/src/lib.rs:here}}
```

</Listing>

Dodajemy implementację domyślną metody `content`, która zwraca pusty wycinek
łańcucha. Dzięki temu nie musimy implementować `content` w strukturach `Draft` i
`PendingReview`. Struktura `Published` nadpisze metodę `content` i zwróci
wartość z `post.content`. Choć to wygodne, to fakt, że metoda `content` w
`State` decyduje o treści `Post`, zaciera granicę między odpowiedzialnością
`State` a odpowiedzialnością `Post`.

Zwróć uwagę, że ta metoda wymaga adnotacji czasu życia (*lifetime*), jak
omawialiśmy w rozdziale 10. Przyjmujemy jako argument referencję do `post` i
zwracamy referencję do części tego `post`, więc czas życia zwracanej referencji
jest powiązany z czasem życia argumentu `post`.

I gotowe – cały listing 18-11 działa! Zaimplementowaliśmy wzorzec stanu z
regułami procesu publikacji wpisu na blogu. Logika związana z tymi regułami
znajduje się w obiektach stanu, zamiast być rozproszona po całym `Post`.

> ### Dlaczego nie enum? {#why-not-an-enum}
>
> Być może zastanawiasz się, dlaczego nie użyliśmy *enuma* (typu
> wyliczeniowego), którego wariantami byłyby możliwe stany wpisu. To z pewnością
> możliwe rozwiązanie – wypróbuj je i porównaj końcowe efekty, aby przekonać
> się, które wolisz! Wadą użycia enuma jest to, że każde miejsce sprawdzające
> wartość enuma będzie potrzebować wyrażenia (*expression*) `match` lub
> podobnego, aby obsłużyć każdy możliwy wariant. Może to prowadzić do większej
> liczby powtórzeń niż rozwiązanie z obiektami traitów.

<!-- Old headings. Do not remove or links may break. -->

<a id="trade-offs-of-the-state-pattern"></a>

#### Ocena wzorca stanu {#evaluating-the-state-pattern}

Pokazaliśmy, że Rust pozwala zaimplementować obiektowy wzorzec stanu, aby
hermetyzować różne rodzaje zachowań, jakie wpis powinien mieć w poszczególnych
stanach. Metody w `Post` nie wiedzą nic o tych różnych zachowaniach. Dzięki
sposobowi zorganizowania kodu wystarczy zajrzeć w jedno miejsce, aby poznać
różne sposoby zachowania opublikowanego wpisu: do implementacji traitu `State`
dla struktury `Published`.

Gdybyśmy utworzyli alternatywną implementację bez wzorca stanu, moglibyśmy
zamiast tego użyć wyrażeń `match` w metodach `Post`, a nawet w kodzie `main`,
które sprawdzałyby stan wpisu i w tych miejscach zmieniały zachowanie.
Oznaczałoby to, że aby zrozumieć wszystkie konsekwencje tego, że wpis jest w
stanie opublikowanym, musielibyśmy zaglądać w kilka miejsc.

Przy wzorcu stanu metody `Post` ani miejsca, w których używamy `Post`, nie
potrzebują wyrażeń `match`, a aby dodać nowy stan, wystarczyłoby dodać nową
strukturę i zaimplementować metody traitu dla tej jednej struktury w jednym
miejscu.

Implementację korzystającą ze wzorca stanu łatwo rozszerzyć o nową
funkcjonalność. Aby przekonać się, jak łatwo utrzymywać kod korzystający ze
wzorca stanu, wypróbuj kilka z poniższych propozycji:

- Dodaj metodę `reject`, która zmienia stan wpisu z `PendingReview` z powrotem
  na `Draft`.
- Wymagaj dwóch wywołań `approve`, zanim stan będzie mógł się zmienić na
  `Published`.
- Pozwól użytkownikom dodawać treść tekstową tylko wtedy, gdy wpis jest w stanie
  `Draft`. Wskazówka: niech obiekt stanu odpowiada za to, co może się zmienić w
  treści, ale nie za modyfikowanie `Post`.

Jedną z wad wzorca stanu jest to, że skoro stany implementują przejścia między
stanami, niektóre z nich są ze sobą powiązane. Gdybyśmy dodali kolejny stan
między `PendingReview` a `Published`, na przykład `Scheduled`, musielibyśmy
zmienić kod w `PendingReview`, aby przechodził do `Scheduled`. Byłoby mniej
pracy, gdyby `PendingReview` nie musiał się zmieniać po dodaniu nowego stanu,
ale oznaczałoby to przejście na inny wzorzec projektowy.

Kolejną wadą jest to, że powieliliśmy część logiki. Aby usunąć część
powtórzeń, moglibyśmy spróbować utworzyć w traicie `State` domyślne
implementacje metod `request_review` i `approve`, które zwracają `self`. To
jednak by nie zadziałało: gdy używamy `State` jako obiektu traitu, trait nie wie,
czym dokładnie będzie konkretne `self`, więc typ zwracany nie jest znany w
czasie kompilacji (*compile-time*). (To jedna ze wspomnianych wcześniej reguł
zgodności z dyn (*dyn compatibility*)).

Inne powtórzenia to podobne implementacje metod `request_review` i `approve` w
`Post`. Obie metody używają `Option::take` na polu `state` struktury `Post`, a
jeśli `state` jest `Some`, delegują wywołanie do implementacji tej samej metody
w opakowanej wartości i ustawiają nową wartość pola `state` na wynik. Gdybyśmy
mieli w `Post` wiele metod działających według tego schematu, moglibyśmy
rozważyć zdefiniowanie makra, aby wyeliminować powtórzenia (zob. podrozdział
[„Makra”][macros]<!-- ignore --> w rozdziale 20).

Implementując wzorzec stanu dokładnie tak, jak definiuje się go dla języków
obiektowych, nie wykorzystujemy mocnych stron Rusta tak w pełni, jak moglibyśmy.
Przyjrzyjmy się zmianom, które możemy wprowadzić w crate’cie `blog`, aby
nieprawidłowe stany i przejścia stały się błędami kompilacji.

### Kodowanie stanów i zachowań jako typów {#encoding-states-and-behavior-as-types}

Pokażemy, jak inaczej podejść do wzorca stanu, aby uzyskać inny zestaw
kompromisów. Zamiast całkowicie hermetyzować stany i przejścia tak, by kod
zewnętrzny nic o nich nie wiedział, zakodujemy stany w postaci różnych typów. W
efekcie system sprawdzania typów w Ruście uniemożliwi używanie szkiców wpisów
tam, gdzie dozwolone są tylko opublikowane wpisy, zgłaszając błąd kompilatora.

Przyjrzyjmy się pierwszej części `main` z listingu 18-11:

<Listing file-name="src/main.rs">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-11/src/main.rs:here}}
```

</Listing>

Nadal umożliwiamy tworzenie nowych wpisów w stanie szkicu za pomocą `Post::new`
oraz dodawanie tekstu do treści wpisu. Ale zamiast metody `content` w szkicu
wpisu, która zwraca pusty łańcuch, sprawimy, że szkice wpisów w ogóle nie będą
miały metody `content`. Dzięki temu, jeśli spróbujemy pobrać treść szkicu,
dostaniemy błąd kompilatora informujący, że taka metoda nie istnieje. W
rezultacie nie będziemy mogli przypadkowo wyświetlić treści szkicu w
środowisku produkcyjnym, bo taki kod nawet się nie skompiluje. Listing 18-19 przedstawia
definicję struktury `Post` i struktury `DraftPost` oraz metody każdej z nich.

<Listing number="18-19" file-name="src/lib.rs" caption="Struktura `Post` z metodą `content` i struktura `DraftPost` bez metody `content`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-19/src/lib.rs}}
```

</Listing>

Zarówno struktura `Post`, jak i `DraftPost` mają prywatne pole `content`, które
przechowuje tekst wpisu na blogu. Struktury nie mają już pola `state`, bo
przenosimy kodowanie stanu do typów struktur. Struktura `Post` będzie
reprezentować opublikowany wpis i ma metodę `content`, która zwraca `content`.

Nadal mamy funkcję `Post::new`, ale zamiast instancji `Post` zwraca ona
instancję `DraftPost`. Ponieważ `content` jest prywatne i nie ma żadnych
funkcji zwracających `Post`, na razie nie da się utworzyć instancji `Post`.

Struktura `DraftPost` ma metodę `add_text`, więc możemy dodawać tekst do
`content` tak jak wcześniej, ale zwróć uwagę, że `DraftPost` nie ma
zdefiniowanej metody `content`! Program gwarantuje więc teraz, że wszystkie
wpisy zaczynają jako szkice, a treść szkiców nie jest dostępna do wyświetlenia.
Każda próba obejścia tych ograniczeń zakończy się błędem kompilatora.

<!-- Old headings. Do not remove or links may break. -->

<a id="implementing-transitions-as-transformations-into-different-types"></a>

Jak więc uzyskać opublikowany wpis? Chcemy wymusić regułę, zgodnie z którą szkic
wpisu musi zostać zrecenzowany i zatwierdzony, zanim będzie mógł zostać
opublikowany. Wpis oczekujący na recenzję nadal nie powinien wyświetlać żadnej
treści. Zaimplementujmy te ograniczenia, dodając kolejną strukturę,
`PendingReviewPost`, definiując w `DraftPost` metodę `request_review`, która
zwraca `PendingReviewPost`, oraz definiując w `PendingReviewPost` metodę
`approve`, która zwraca `Post`, jak pokazano w listingu 18-20.

<Listing number="18-20" file-name="src/lib.rs" caption="Struktura `PendingReviewPost` tworzona przez wywołanie `request_review` na `DraftPost` oraz metoda `approve`, która zamienia `PendingReviewPost` w opublikowany `Post`">

```rust,noplayground
{{#rustdoc_include ../listings/ch18-oop/listing-18-20/src/lib.rs:here}}
```

</Listing>

Metody `request_review` i `approve` przejmują własność `self`, konsumując w ten
sposób instancje `DraftPost` i `PendingReviewPost` i przekształcając je
odpowiednio w `PendingReviewPost` i opublikowany `Post`. Dzięki temu po
wywołaniu `request_review` nie zostaną nam żadne zbędne instancje `DraftPost`
(i analogicznie w pozostałych przypadkach). Struktura `PendingReviewPost` nie
ma zdefiniowanej metody `content`, więc próba odczytania jej treści kończy się błędem kompilatora, tak samo jak w przypadku
`DraftPost`. Ponieważ jedynym sposobem uzyskania opublikowanej instancji `Post`,
która ma zdefiniowaną metodę `content`, jest wywołanie metody `approve` na
`PendingReviewPost`, a jedynym sposobem uzyskania `PendingReviewPost` jest
wywołanie metody `request_review` na `DraftPost`, zakodowaliśmy proces
publikacji wpisu na blogu w systemie typów.

Musimy jednak wprowadzić też drobne zmiany w `main`. Metody `request_review` i
`approve` zwracają nowe instancje, zamiast modyfikować strukturę, na której są
wywoływane, więc musimy dodać więcej przypisań `let post =` korzystających z
przesłaniania (*shadowing*), aby zapisać zwrócone instancje. Nie możemy też
zachować asercji sprawdzających, że treść szkicu i wpisu oczekującego na
recenzję to puste łańcuchy, ale też ich nie potrzebujemy: kodu, który próbuje
użyć treści wpisów w tych stanach, nie da się już skompilować. Zaktualizowany
kod w `main` pokazano w listingu 18-21.

<Listing number="18-21" file-name="src/main.rs" caption="Zmiany w `main` pozwalające użyć nowej implementacji procesu publikacji wpisu na blogu">

```rust,ignore
{{#rustdoc_include ../listings/ch18-oop/listing-18-21/src/main.rs}}
```

</Listing>

Zmiany, które musieliśmy wprowadzić w `main`, aby ponownie przypisywać `post`,
oznaczają, że ta implementacja nie jest już do końca zgodna z obiektowym
wzorcem stanu: przekształcenia między stanami nie są już w całości
hermetyzowane w implementacji `Post`. Zyskujemy jednak to, że nieprawidłowe
stany są teraz niemożliwe dzięki systemowi typów i sprawdzaniu typów
odbywającemu się w czasie kompilacji! Dzięki temu pewne błędy, takie jak
wyświetlenie treści nieopublikowanego wpisu, zostaną wykryte, zanim trafią na
produkcję.

Wypróbuj zadania zaproponowane na początku tego podrozdziału na crate’cie `blog`
w wersji z listingu 18-21, aby ocenić projekt tej wersji kodu. Zwróć uwagę, że
niektóre z tych zadań mogą być w tym projekcie już wykonane.

Przekonaliśmy się, że choć Rust pozwala implementować obiektowe wzorce
projektowe, dostępne są w nim również inne wzorce, takie jak kodowanie stanu w
systemie typów. Te wzorce wiążą się z różnymi kompromisami. Choć wzorce obiektowe
mogą być ci bardzo dobrze znane, przemyślenie problemu na nowo tak, aby
wykorzystać mechanizmy Rusta, może przynieść korzyści, takie jak zapobieganie
niektórym błędom już w czasie kompilacji. Wzorce obiektowe nie zawsze będą
najlepszym rozwiązaniem w Ruście ze względu na pewne mechanizmy, takie jak
własność, których języki obiektowe nie mają.

## Podsumowanie {#summary}

Niezależnie od tego, czy po lekturze tego rozdziału uważasz Rusta za język
obiektowy, wiesz już, że za pomocą obiektów traitów możesz uzyskać w Ruście
niektóre mechanizmy obiektowe. Dynamiczne wywoływanie (*dynamic dispatch*) może dać
twojemu kodowi pewną elastyczność kosztem odrobiny wydajności w czasie
działania. Tę elastyczność możesz wykorzystać do implementowania wzorców
obiektowych, które mogą ułatwić utrzymanie kodu. Rust ma też inne mechanizmy,
takie jak własność, których języki obiektowe nie mają. Wzorzec obiektowy nie
zawsze będzie najlepszym sposobem na wykorzystanie mocnych stron Rusta, ale jest
dostępną opcją.

Teraz przyjrzymy się wzorcom (*patterns*), kolejnemu mechanizmowi Rusta, który
zapewnia dużą elastyczność. Pokrótce przyglądaliśmy się im w różnych miejscach
książki, ale nie poznaliśmy jeszcze ich pełnych możliwości. Do dzieła!

{{#quiz ../quizzes/ch17-03-oo-design-patterns.toml}}

[more-info-than-rustc]: ch09-03-to-panic-or-not-to-panic.html#cases-in-which-you-have-more-information-than-the-compiler
[macros]: ch20-05-macros.html#macros

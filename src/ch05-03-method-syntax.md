## Metody {#methods}

Metody (*methods*) przypominają funkcje: deklarujemy je słowem kluczowym
(*keyword*) `fn` i nazwą, mogą mieć parametry i wartość zwracaną, a ich kod jest
wykonywany, gdy metoda zostanie gdzieś wywołana. W odróżnieniu od funkcji metody
definiuje się w kontekście struktury (*struct*) (albo *enuma* (typu
wyliczeniowego) lub obiektu traitu (*trait object*), które omawiamy odpowiednio
w [rozdziale 6][enums]<!-- ignore --> i
[rozdziale 18][trait-objects]<!-- ignore -->), a ich pierwszym parametrem jest
zawsze `self`, czyli instancja struktury, na której wywołano metodę.

<!-- Old headings. Do not remove or links may break. -->

<a id="defining-methods"></a>

### Składnia metod {#method-syntax}

Zmieńmy funkcję `area`, która przyjmuje jako parametr instancję `Rectangle`, w
metodę `area` zdefiniowaną dla struktury `Rectangle`, jak pokazuje listing 5-13.

<Listing number="5-13" file-name="src/main.rs" caption="Definicja metody `area` dla struktury `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-13/src/main.rs}}
```

</Listing>

Aby zdefiniować funkcję w kontekście `Rectangle`, otwieramy blok `impl` (od
*implementation*, implementacja) dla `Rectangle`. Wszystko w tym bloku `impl`
będzie powiązane z typem `Rectangle`. Następnie przenosimy funkcję `area` do
nawiasów klamrowych `impl` i zmieniamy pierwszy (a w tym przypadku jedyny)
parametr na `self` – zarówno w sygnaturze, jak i w całym ciele funkcji. W
`main`, gdzie wywoływaliśmy funkcję `area` i przekazywaliśmy `rect1` jako
argument, możemy zamiast tego użyć _składni metod_ (*method syntax*), aby
wywołać metodę `area` na naszej instancji `Rectangle`. Składnię metod zapisujemy
po instancji: dodajemy kropkę, a po niej nazwę metody, nawiasy i ewentualne
argumenty.

W sygnaturze `area` używamy `&self` zamiast `rectangle: &Rectangle`. Zapis
`&self` to w rzeczywistości skrót od `self: &Self`. Wewnątrz bloku `impl` typ
`Self` jest aliasem typu, dla którego napisano ten blok `impl`. Pierwszym
parametrem metody musi być parametr o nazwie `self` typu `Self`, dlatego Rust
pozwala skrócić ten zapis do samej nazwy `self` na pierwszym miejscu. Zwróć
uwagę, że przed skrótem `self` wciąż musimy napisać `&`, aby wskazać, że metoda
pożycza (*borrow*) instancję `Self`, tak jak w przypadku
`rectangle: &Rectangle`. Metody mogą przejmować własność (*ownership*) `self`,
pożyczać `self` niemutowalnie, jak tutaj, albo pożyczać `self` mutowalnie
(*mutable*) – tak samo jak każdy inny parametr.

Wybraliśmy tu `&self` z tego samego powodu, dla którego w wersji funkcyjnej
użyliśmy `&Rectangle`: nie chcemy przejmować własności, chcemy tylko odczytać dane
ze struktury, a nie je zapisywać. Gdybyśmy w ramach działania metody chcieli
zmienić instancję, na której ją wywołano, użylibyśmy jako pierwszego parametru
`&mut self`. Metoda, która przejmuje własność instancji, bo ma jako pierwszy
parametr samo `self`, to rzadkość. Tej techniki używa się zwykle wtedy, gdy
metoda przekształca `self` w coś innego, a chcesz uniemożliwić wywołującemu
użycie pierwotnej instancji po tym przekształceniu.

Główny powód, dla którego używa się metod zamiast funkcji – poza samą składnią
metod i brakiem konieczności powtarzania typu `self` w sygnaturze każdej metody
– to organizacja kodu. Umieściliśmy wszystko, co można zrobić z instancją typu,
w jednym bloku `impl`, zamiast zmuszać przyszłych użytkowników naszego kodu do
szukania możliwości `Rectangle` w różnych miejscach udostępnianej przez nas
biblioteki.

Zauważ, że możemy nadać metodzie taką samą nazwę jak jednemu z pól struktury.
Możemy na przykład zdefiniować dla `Rectangle` metodę, która także nazywa się
`width`:

<Listing file-name="src/main.rs">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-06-method-field-interaction/src/main.rs:here}}
```

</Listing>

W tym przykładzie metoda `width` zwraca `true`, jeśli wartość w polu `width`
instancji jest większa od `0`, i `false`, jeśli wynosi `0`: pola o tej samej
nazwie co metoda możemy w niej użyć w dowolnym celu. Gdy w `main` po
`rect1.width` piszemy nawiasy, Rust wie, że chodzi o metodę `width`. Gdy
nawiasów nie ma, Rust wie, że chodzi o pole `width`.

Często, choć nie zawsze, gdy nadajemy metodzie taką samą nazwę jak polu, chcemy,
by tylko zwracała wartość tego pola i nic więcej nie robiła. Takie metody nazywa
się _getterami_ (*getters*, metody dostępowe) i Rust, w przeciwieństwie do
niektórych innych języków, nie generuje ich automatycznie dla pól struktur.
Gettery są przydatne, bo pozwalają uczynić pole prywatnym, a metodę publiczną, i
w ten sposób udostępnić to pole tylko do odczytu w ramach publicznego API typu.
Czym jest publiczność i prywatność oraz jak oznaczyć pole lub metodę jako
publiczne bądź prywatne, omówimy w [rozdziale 7][public]<!-- ignore -->.

### Metody z większą liczbą parametrów {#methods-with-more-parameters}

Poćwiczmy używanie metod, implementując drugą metodę dla struktury `Rectangle`.
Tym razem chcemy, by instancja `Rectangle` przyjmowała inną instancję
`Rectangle` i zwracała `true`, jeśli ten drugi `Rectangle` mieści się całkowicie
w `self` (pierwszym `Rectangle`), a w przeciwnym razie `false`. Innymi słowy, po
zdefiniowaniu metody `can_hold` chcemy móc napisać program pokazany w listingu
5-14.

<Listing number="5-14" file-name="src/main.rs" caption="Użycie jeszcze nienapisanej metody `can_hold`">

```rust,ignore
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-14/src/main.rs}}
```

</Listing>

Oczekiwany wynik wyglądałby tak jak poniżej, bo oba wymiary `rect2` są mniejsze
od wymiarów `rect1`, ale `rect3` jest szerszy niż `rect1`:

```text
Can rect1 hold rect2? true
Can rect1 hold rect3? false
```

Wiemy, że chcemy zdefiniować metodę, więc znajdzie się ona w bloku
`impl Rectangle`. Metoda będzie się nazywać `can_hold` i przyjmie jako parametr
niemutowalne pożyczenie innego `Rectangle`. Typ parametru możemy odczytać z
kodu, który wywołuje metodę: `rect1.can_hold(&rect2)` przekazuje `&rect2`, czyli
niemutowalne pożyczenie `rect2`, instancji `Rectangle`. Ma to sens, bo musimy
tylko odczytać `rect2` (a nie zapisywać, do czego potrzebne byłoby pożyczenie
mutowalne), a chcemy, żeby `main` zachowało własność `rect2`, abyśmy mogli użyć
go ponownie po wywołaniu metody `can_hold`. Wartością zwracaną przez `can_hold`
będzie wartość logiczna, a implementacja sprawdzi, czy szerokość i wysokość
`self` są większe odpowiednio od szerokości i wysokości drugiego `Rectangle`.
Dodajmy nową metodę `can_hold` do bloku `impl` z listingu 5-13, jak pokazuje
listing 5-15.

<Listing number="5-15" file-name="src/main.rs" caption="Implementacja metody `can_hold` dla `Rectangle`, która przyjmuje jako parametr inną instancję `Rectangle`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-15/src/main.rs:here}}
```

</Listing>

Gdy uruchomimy ten kod z funkcją `main` z listingu 5-14, otrzymamy oczekiwany
wynik. Metody mogą przyjmować wiele parametrów, które dodajemy do sygnatury po
parametrze `self`, a parametry te działają tak samo jak parametry funkcji.


### Funkcje powiązane {#associated-functions}

Wszystkie funkcje zdefiniowane w bloku `impl` nazywamy _funkcjami powiązanymi_
(*associated functions*), bo są powiązane z typem podanym po `impl`. Możemy
definiować funkcje powiązane, które nie mają `self` jako pierwszego parametru (a
zatem nie są metodami), bo do działania nie potrzebują instancji typu.
Używaliśmy już jednej takiej funkcji: funkcji `String::from` zdefiniowanej dla
typu `String`.

Funkcje powiązane, które nie są metodami, często służą jako konstruktory
zwracające nową instancję struktury. Zwykle nazywają się `new`, ale `new` nie
jest specjalną nazwą i nie jest wbudowane w język. Moglibyśmy na przykład
udostępnić funkcję powiązaną o nazwie `square`, która miałaby jeden parametr
wymiaru i używała go zarówno jako szerokości, jak i wysokości. Ułatwiłoby to
tworzenie kwadratowego `Rectangle` bez podawania dwa razy tej samej wartości:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/no-listing-03-associated-functions/src/main.rs:here}}
```

Słowa kluczowe `Self` w typie zwracanym i w ciele funkcji są aliasami typu,
który występuje po słowie kluczowym `impl`, czyli w tym przypadku `Rectangle`.

Aby wywołać tę funkcję powiązaną, używamy składni `::` z nazwą struktury, na
przykład `let sq = Rectangle::square(3);`. Ta funkcja należy do przestrzeni nazw
struktury: składni `::` używa się zarówno dla funkcji powiązanych, jak i dla
przestrzeni nazw tworzonych przez moduły. Moduły omówimy w
[rozdziale 7][modules]<!-- ignore -->.

### Wiele bloków `impl` {#multiple-impl-blocks}

Każda struktura może mieć wiele bloków `impl`. Na przykład listing 5-15 jest
równoważny kodowi z listingu 5-16, w którym każda metoda ma własny blok `impl`.

<Listing number="5-16" caption="Listing 5-15 przepisany z użyciem wielu bloków `impl`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-16/src/main.rs:here}}
```

</Listing>

Nie ma tu powodu, by rozdzielać te metody na wiele bloków `impl`, ale taka
składnia jest poprawna. Przypadek, w którym wiele bloków `impl` się przydaje,
zobaczymy w rozdziale 10, gdzie omówimy typy generyczne (*generics*) i *traity*
(cechy typów, zbliżone do interfejsów).

### Wywołania metod są lukrem składniowym dla wywołań funkcji {#method-calls-are-syntactic-sugar-for-function-calls}

Korzystając z poznanych dotąd pojęć, możemy teraz zobaczyć, że wywołania metod są lukrem składniowym (*syntactic sugar*) dla wywołań funkcji. Załóżmy na przykład, że mamy strukturę prostokąta z metodą `area` i metodą `set_width`:

```rust,ignore
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn set_width(&mut self, width: u32) {
        self.width = width;
    }
}
```

Załóżmy też, że mamy prostokąt `r`. Wtedy wywołania metod `r.area()` i `r.set_width(2)` są równoważne temu kodowi:

```rust
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
# impl Rectangle {
#     fn area(&self) -> u32 {
#        self.width * self.height
#      }
# 
#     fn set_width(&mut self, width: u32) {
#         self.width = width;
#     }
# }
# 
# fn main() {
let mut r = Rectangle { 
    width: 1,
    height: 2
};
let area1 = r.area();
let area2 = Rectangle::area(&r);
assert_eq!(area1, area2);

r.set_width(2);
Rectangle::set_width(&mut r, 2);
# }
```

Wywołanie metody `r.area()` staje się wywołaniem `Rectangle::area(&r)`. Nazwą funkcji jest funkcja powiązana `Rectangle::area`. Argumentem funkcji jest parametr `&self`. Rust automatycznie wstawia operator pożyczenia `&`.

> *Uwaga:* jeśli znasz C lub C++, to dwie różne składnie wywołań metod są ci dobrze znane: `r.area()` i `r->area()`. Rust nie ma odpowiednika operatora strzałki `->`. Gdy używasz operatora kropki, Rust automatycznie tworzy referencję (*reference*) do odbiorcy metody albo wykonuje na nim dereferencję (*dereference*).

Wywołanie metody `r.set_width(2)` analogicznie staje się wywołaniem `Rectangle::set_width(&mut r, 2)`. Ta metoda oczekuje `&mut self`, więc pierwszym argumentem jest mutowalne pożyczenie `&mut r`. Drugi argument pozostaje dokładnie taki sam – to liczba 2.

Jak opisaliśmy w podrozdziale 4.2 [„Dereferencja wskaźnika daje dostęp do jego danych”](ch04-02-references-and-borrowing.html#dereferencing-a-pointer-accesses-its-data), Rust wstawi tyle referencji i dereferencji, ile trzeba, by typy zgadzały się z parametrem `self`. Oto na przykład dwa równoważne wywołania `area` dla mutowalnej referencji do prostokąta w *boxie* (wskaźniku na dane umieszczone na stercie):

```rust
# struct Rectangle {
#     width: u32,
#     height: u32,
# }
# 
# impl Rectangle {
#     fn area(&self) -> u32 {
#        self.width * self.height
#      }
# 
#     fn set_width(&mut self, width: u32) {
#         self.width = width;
#     }
# }
# fn main() {
let r = &mut Box::new(Rectangle { 
    width: 1,
    height: 2
});
let area1 = r.area();
let area2 = Rectangle::area(&**r);
assert_eq!(area1, area2);
# }
```

Rust doda dwie dereferencje (jedną dla mutowalnej referencji, jedną dla boxa), a potem jedno niemutowalne pożyczenie, bo `area` oczekuje `&Rectangle`. Zwróć uwagę, że to także sytuacja, w której mutowalna referencja zostaje „zdegradowana” do referencji współdzielonej, co omawialiśmy w [podrozdziale 4.2](ch04-02-references-and-borrowing.html#mutable-references-provide-unique-and-non-owning-access-to-data). Z kolei nie wolno wywołać `set_width` na wartości typu `&Rectangle` ani `&Box<Rectangle>`.

{{#quiz ../quizzes/ch05-03-method-syntax-sec1.toml}}


### Metody i własność {#methods-and-ownership}

Jak omawialiśmy w podrozdziale 4.2 [„Referencje i pożyczanie”](ch04-02-references-and-borrowing.html), metody można wywoływać tylko na strukturach, które mają odpowiednie uprawnienia (*permissions*). W przykładach będziemy używać tych trzech metod, które przyjmują odpowiednio `&self`, `&mut self` i `self`.

```rust,ignore
impl Rectangle {    
    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn set_width(&mut self, width: u32) {
        self.width = width;
    }

    fn max(self, other: Rectangle) -> Rectangle {
        Rectangle { 
            width: self.width.max(other.width),
            height: self.height.max(other.height),
        }
    }
}
```

#### Odczyt i zapis przez `&self` i `&mut self` {#reads-and-writes-with-self-and-mut-self}

Jeśli za pomocą `let rect = Rectangle { ... }` utworzymy prostokąt, którego właścicielem jest zmienna, to `rect` ma uprawnienia @Perm{read} i @Perm{own}, czyli R (*read*, odczyt) i O (*own*, własność). Z tymi uprawnieniami można wywołać metody `area` i `max`:

```aquascope,permissions,boundaries,stepper
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
println!("{}", rect.area());`{}`

let other_rect = Rectangle { width: 1, height: 1 };
let max_rect = rect.max(other_rect);`{}`
#}
```

Jeśli jednak spróbujemy wywołać `set_width`, zabraknie nam uprawnienia @Perm{write}, czyli W (*write*, zapis):

```aquascope,permissions,boundaries,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};
rect.set_width(0);`{}`
#}
```

Rust odrzuci ten program z następującym błędem:

```text
error[E0596]: cannot borrow `rect` as mutable, as it is not declared as mutable
  --> test.rs:28:1
   |
24 | let rect = Rectangle {
   |     ---- help: consider changing this to be mutable: `mut rect`
...
28 | rect.set_width(0);
   | ^^^^^^^^^^^^^^^^^ cannot borrow as mutable
```

Podobny błąd dostaniemy, jeśli spróbujemy wywołać `set_width` na niemutowalnej referencji do `Rectangle`, nawet jeśli sam prostokąt jest mutowalny:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
// Added the mut keyword to the let-binding
let mut rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
rect.set_width(1);`{}`     // this is now ok

let rect_ref = &rect;`(focus,rxpaths:^\*rect_ref$)`
rect_ref.set_width(2);`{}` // but this is still not ok
#}
```

#### Przeniesienia przez `self` {#moves-with-self}

Wywołanie metody, która oczekuje `self`, przenosi (*move*) strukturę wejściową (chyba że struktura implementuje `Copy`). Nie możemy na przykład użyć `Rectangle` po przekazaniu go do `max`:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
#impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
#}
#fn main() {
let rect = Rectangle {
    width: 0,
    height: 0
};`(focus,rxpaths:^rect$)`
let other_rect = Rectangle { 
    width: 1, 
    height: 1 
};
let max_rect = rect.max(other_rect);`(focus,rxpaths:^rect$)`
println!("{}", rect.area());`{}`
#}
```

Gdy wywołamy `rect.max(..)`, przenosimy `rect` i tracimy wszystkie uprawnienia do niego. Próba skompilowania tego programu da następujący błąd:

```text
error[E0382]: borrow of moved value: `rect`
  --> test.rs:33:16
   |
24 | let rect = Rectangle {
   |     ---- move occurs because `rect` has type `Rectangle`, which does not implement the `Copy` trait
...
32 | let max_rect = rect.max(other_rect);
   |                     --------------- `rect` moved due to this method call
33 | println!("{}", rect.area());
   |                ^^^^^^^^^^^ value borrowed here after move
```

Podobna sytuacja zachodzi, gdy próbujemy wywołać metodę przyjmującą `self` na referencji. Załóżmy na przykład, że chcemy napisać metodę `set_to_max`, która przypisuje do `self` wynik `self.max(..)`:

```aquascope,permissions,boundaries,stepper,shouldFail
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {    
#  fn area(&self) -> u32 {
#    self.width * self.height
#  }
#
#  fn set_width(&mut self, width: u32) {
#    self.width = width;
#  }
#
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {`(focus,rxpaths:^\*self$)`
        *self = self.max(other);`{}`
    }
}
```

Widać wtedy, że w operacji `self.max(..)` brakuje `self` uprawnienia @Perm{own}. Rust odrzuca więc ten program z następującym błędem:

```text
error[E0507]: cannot move out of `*self` which is behind a mutable reference
  --> test.rs:23:17
   |
23 |         *self = self.max(other);
   |                 ^^^^^----------
   |                 |    |
   |                 |    `*self` moved due to this method call
   |                 move occurs because `*self` has type `Rectangle`, which does not implement the `Copy` trait
   |
```

To ten sam rodzaj błędu, który omawialiśmy w podrozdziale 4.3 [„Kopiowanie a przenoszenie z kolekcji”](ch04-03-fixing-ownership-errors.html#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection).

#### Dobre i złe przeniesienia {#good-moves-and-bad-moves}

Możesz się zastanawiać: dlaczego to ważne, czy przenosimy wartość spod `*self`? W rzeczywistości w przypadku `Rectangle` przeniesienie spod `*self` jest bezpieczne, mimo że Rust na to nie pozwala. Jeśli na przykład zasymulujemy program, który wywołuje odrzuconą metodę `set_to_max`, zobaczysz, że nie dzieje się nic niebezpiecznego:

```aquascope,interpreter,shouldFail,horizontal
#struct Rectangle {
#    width: u32,
#    height: u32,
#}
impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {
        let max = self.max(other);`[]`
        *self = max;
    }
}

fn main() {
    let mut rect = Rectangle { width: 0, height: 1 };
    let other_rect = Rectangle { width: 1, height: 0 };`[]`
    rect.set_to_max(other_rect);`[]`
}
```

Przeniesienie spod `*self` jest bezpieczne, bo `Rectangle` nie jest właścicielem żadnych danych na stercie (*heap*).
Możemy nawet sprawić, że Rust skompiluje `set_to_max`, dodając po prostu `#[derive(Copy, Clone)]` do definicji `Rectangle`:

```aquascope,permissions,boundaries,stepper
\#[derive(Copy, Clone)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {`(focus,rxpaths:^\*self$)`
        *self = self.max(other);`{}`
    }
}
```

Zauważ, że w odróżnieniu od poprzedniej wersji `self.max(other)` nie wymaga już uprawnienia @Perm{own} do `*self` ani do `other`. Pamiętaj, że `self.max(other)` po usunięciu lukru składniowego to `Rectangle::max(*self, other)`. Dereferencja `*self` nie wymaga własności `*self`, jeśli `Rectangle` da się kopiować.

Możesz się zastanawiać: dlaczego Rust nie wyprowadza (*derive*) automatycznie `Copy` dla `Rectangle`? Rust nie wyprowadza automatycznie `Copy`, aby zachować stabilność przy zmianach API. Wyobraź sobie, że autor typu `Rectangle` postanowił dodać pole `name: String`. Wtedy cały kod klientów, który zakłada, że `Rectangle` jest `Copy`, nagle zostałby odrzucony przez kompilator. Aby tego uniknąć, autorzy API muszą jawnie dodać `#[derive(Copy)]`, sygnalizując, że ich struktura ma zawsze być `Copy`.

Aby lepiej zrozumieć problem, uruchommy symulację. Załóżmy, że dodaliśmy do `Rectangle` pole `name: String`. Co by się stało, gdyby Rust pozwolił skompilować `set_to_max`?

```aquascope,interpreter,shouldFail,horizontal
struct Rectangle {
    width: u32,
    height: u32,
    name: String,
}

impl Rectangle {    
#  fn max(self, other: Self) -> Self {
#    let w = self.width.max(other.width);
#    let h = self.height.max(other.height);
#    Rectangle { 
#      width: w,
#      height: h,
#      name: String::from("max")
#    }
#  }
    fn set_to_max(&mut self, other: Rectangle) {
        `[]`let max = self.max(other);`[]`
        drop(*self);`[]` // This is usually implicit,
                         // but added here for clarity.
        *self = max;
    }
}

fn main() {
    let mut r1 = Rectangle { 
        width: 9, 
        height: 9, 
        name: String::from("r1") 
    };
    let r2 = Rectangle {
        width: 16,
        height: 16,
        name: String::from("r2")
    };
    r1.set_to_max(r2);
}
```

W tym programie wywołujemy `set_to_max` z dwoma prostokątami: `r1` i `r2`. `self` jest mutowalną referencją do `r1`, a `other` to przeniesienie `r2`. Po wywołaniu `self.max(other)` metoda `max` przejmuje własność obu prostokątów. Gdy `max` kończy działanie, Rust dealokuje oba łańcuchy znaków (*strings*), „r1” i „r2”, na stercie. Zwróć uwagę na problem: w miejscu L2 `*self` powinno dać się odczytywać i zapisywać. Tymczasem `(*self).name` (a właściwie `r1.name`) zostało już zdealokowane.

Dlatego gdy wykonujemy `*self = max`, dochodzi do niezdefiniowanego zachowania (*undefined behavior*). Gdy nadpisujemy `*self`, Rust niejawnie zwalnia (*drop*) dane, które wcześniej były w `*self`. Aby uczynić to zachowanie jawnym, dodaliśmy `drop(*self)`. Po wywołaniu `drop(*self)` Rust próbuje po raz drugi zwolnić `(*self).name`. To podwójne zwolnienie (*double-free*), czyli niezdefiniowane zachowanie.

Zapamiętaj więc: gdy widzisz błąd w rodzaju „cannot move out of `*self`”, to zwykle dlatego, że próbujesz wywołać metodę przyjmującą `self` na referencji takiej jak `&self` czy `&mut self`. Rust chroni cię wtedy przed podwójnym zwolnieniem.


## Podsumowanie {#summary}

Struktury pozwalają tworzyć własne typy, które mają znaczenie w twojej
dziedzinie. Dzięki nim możesz trzymać powiązane ze sobą fragmenty danych razem i
nadać każdemu z nich nazwę, by kod był czytelny. W blokach `impl` możesz
definiować funkcje powiązane z twoim typem, a metody to rodzaj funkcji
powiązanych, które pozwalają określić zachowanie instancji twoich struktur.

Struktury nie są jednak jedynym sposobem tworzenia własnych typów: przyjrzyjmy
się teraz enumom w Ruście, aby dodać do swojego zestawu kolejne narzędzie.

{{#quiz ../quizzes/ch05-03-method-syntax-sec2.toml}}

[enums]: ch06-00-enums.html
[trait-objects]: ch18-02-trait-objects.md
[public]: ch07-03-paths-for-referring-to-an-item-in-the-module-tree.html#exposing-paths-with-the-pub-keyword
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html

## Definiowanie struktur i tworzenie ich instancji {#defining-and-instantiating-structs}

Struktury (*struct*) są podobne do krotek (*tuple*), omówionych w podrozdziale
[„Typ krotki”][tuples]<!--
ignore -->, ponieważ jedne i drugie przechowują wiele powiązanych wartości.
Podobnie jak w krotkach, elementy struktury mogą mieć różne typy. W odróżnieniu
od krotek w strukturze nazywasz każdy element danych, więc jasne jest, co
oznaczają poszczególne wartości. Dzięki tym nazwom struktury są bardziej
elastyczne niż krotki: nie musisz polegać na kolejności danych, żeby podać
wartości instancji albo się do nich odwołać.

Żeby zdefiniować strukturę, wpisujemy słowo kluczowe (*keyword*) `struct` i
nadajemy nazwę całej strukturze. Nazwa struktury powinna opisywać znaczenie
grupowanych razem elementów danych. Następnie w nawiasach klamrowych definiujemy
nazwy i typy elementów danych, które nazywamy _polami_. Na przykład listing 5-1
pokazuje strukturę przechowującą informacje o koncie użytkownika.

<Listing number="5-1" file-name="src/main.rs" caption="Definicja struktury `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-01/src/main.rs:here}}
```

</Listing>

Żeby użyć struktury po jej zdefiniowaniu, tworzymy _instancję_ tej struktury,
podając konkretne wartości dla każdego z pól. Instancję tworzymy, podając nazwę
struktury, a po niej nawiasy klamrowe zawierające pary _`key:
value`_ (klucz: wartość), w których kluczami są nazwy pól, a wartościami dane,
które chcemy w tych polach przechować. Nie musimy podawać pól w tej samej
kolejności, w jakiej zadeklarowaliśmy je w strukturze. Innymi słowy, definicja
struktury jest jak ogólny szablon typu, a instancje wypełniają ten szablon
konkretnymi danymi, tworząc wartości tego typu. Na przykład możemy zadeklarować
konkretnego użytkownika tak jak w listingu 5-2.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
    let user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };`[]`
}
```

Żeby pobrać konkretną wartość ze struktury, używamy notacji kropkowej. Na
przykład, żeby odczytać adres e-mail tego użytkownika, piszemy `user1.email`.
Jeśli instancja jest mutowalna (*mutable*), możemy zmienić wartość, używając
notacji kropkowej i przypisując nową wartość do wybranego pola. Listing 5-3
pokazuje, jak zmienić wartość pola `email` w mutowalnej instancji `User`.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
    let mut user1 = User {
        email: String::from("someone@example.com"),
        username: String::from("someusername123"),
        active: true,
        sign_in_count: 1,
    };`[]`

    user1.email = String::from("anotheremail@example.com");`[]`
}
```

Zwróć uwagę, że mutowalna musi być cała instancja; Rust nie pozwala oznaczyć
jako mutowalnych tylko wybranych pól. Jak w przypadku każdego wyrażenia
(*expression*), możemy utworzyć nową instancję struktury jako ostatnie wyrażenie
w ciele funkcji, żeby niejawnie zwrócić tę nową instancję.

Listing 5-4 pokazuje funkcję `build_user`, która zwraca instancję `User` z
podanym adresem e-mail i nazwą użytkownika. Pole `active` dostaje wartość
`true`, a `sign_in_count` – wartość `1`.

<Listing number="5-4" file-name="src/main.rs" caption="Funkcja `build_user`, która przyjmuje adres e-mail i nazwę użytkownika, a zwraca instancję `User`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-04/src/main.rs:here}}
```

</Listing>

Nazwanie parametrów funkcji tak samo jak pól struktury jest rozsądne, ale
konieczność powtarzania nazw pól i zmiennych `email` oraz `username` jest nieco
żmudna. Gdyby struktura miała więcej pól, powtarzanie każdej nazwy byłoby
jeszcze bardziej irytujące. Na szczęście istnieje wygodny skrót!

<!-- Old headings. Do not remove or links may break. -->

<a id="using-the-field-init-shorthand-when-variables-and-fields-have-the-same-name"></a>

### Skrócona inicjalizacja pól {#using-the-field-init-shorthand}

Ponieważ w listingu 5-4 nazwy parametrów i nazwy pól struktury są dokładnie
takie same, możemy użyć składni _skróconej inicjalizacji pól_ (*field init
shorthand*), żeby przepisać `build_user` tak, by działała dokładnie tak samo,
ale bez powtarzania `username` i `email`, jak pokazuje listing 5-5.

<Listing number="5-5" file-name="src/main.rs" caption="Funkcja `build_user` używająca skróconej inicjalizacji pól, ponieważ parametry `username` i `email` mają takie same nazwy jak pola struktury">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-05/src/main.rs:here}}
```

</Listing>

Tworzymy tu nową instancję struktury `User`, która ma pole o nazwie `email`.
Chcemy ustawić wartość pola `email` na wartość parametru `email` funkcji
`build_user`. Ponieważ pole `email` i parametr `email` mają tę samą nazwę,
wystarczy napisać `email` zamiast `email: email`.

<!-- Old headings. Do not remove or links may break. -->

<a id="creating-instances-from-other-instances-with-struct-update-syntax"></a>

### Tworzenie instancji za pomocą składni aktualizacji struktury {#creating-instances-with-struct-update-syntax}

Często przydaje się utworzenie nowej instancji struktury, która zawiera
większość wartości z innej instancji tego samego typu, ale niektóre z nich
zmienia. Możesz to zrobić za pomocą składni aktualizacji struktury (*struct
update syntax*).

Najpierw w listingu 5-6 pokazujemy, jak utworzyć nową instancję `User` w `user2`
w zwykły sposób, bez składni aktualizacji. Ustawiamy nową wartość `email`, a
poza tym używamy tych samych wartości z `user1`, które utworzyliśmy w listingu
5-2.

```aquascope,interpreter
#struct User {
#    active: bool,
#    username: String,
#    email: String,
#    sign_in_count: u64,
#}
fn main() {
#   let user1 = User {
#      email: String::from("someone@example.com"),
#      username: String::from("someusername123"),
#      active: true,
#      sign_in_count: 1,
#   };
    // --snip--

    let user2 = User {
        active: user1.active,
        username: user1.username,
        email: String::from("another@example.com"),
        sign_in_count: user1.sign_in_count,
    };`[]`
}
```

<span class="caption">Listing 5-6: Tworzenie nowej instancji `User` z użyciem wszystkich
wartości z `user1` z wyjątkiem jednej</span>

Za pomocą składni aktualizacji struktury możemy osiągnąć ten sam efekt przy
mniejszej ilości kodu, jak pokazuje listing 5-7. Składnia `..` oznacza, że
pozostałe pola, których nie ustawiono jawnie, mają mieć te same wartości co
pola w podanej instancji.

<Listing number="5-7" file-name="src/main.rs" caption="Użycie składni aktualizacji struktury do ustawienia nowej wartości `email` w instancji `User` przy zachowaniu pozostałych wartości z `user1`">

```rust
{{#rustdoc_include ../listings/ch05-using-structs-to-structure-related-data/listing-05-07/src/main.rs:here}}
```

</Listing>

Kod z listingu 5-7 również tworzy w `user2` instancję, która ma inną wartość
`email`, ale te same wartości pól `username`, `active` i `sign_in_count` co
`user1`. Zapis `..user1` musi być na końcu, żeby wskazać, że wszystkie pozostałe
pola mają dostać wartości z odpowiadających im pól `user1`. Możemy jednak podać
wartości dowolnej liczby pól w dowolnej kolejności, niezależnie od kolejności
pól w definicji struktury.

Zwróć uwagę, że składnia aktualizacji struktury używa `=` jak przypisanie.
Wynika to z tego, że przenosi ona dane, tak jak widzieliśmy w podrozdziale [„Czym jest własność?”][move]<!-- ignore -->. W tym przykładzie po utworzeniu `user2` zmienna `user1` staje się częściowo nieważna, ponieważ `String` z pola
`username` w `user1` został przeniesiony (*move*) do `user2`. Gdybyśmy nadali
`user2` nowe wartości `String` zarówno dla `email`, jak i dla `username`, i tym
samym użyli z `user1` tylko wartości `active` i `sign_in_count`, `user1`
pozostałaby w pełni ważna po utworzeniu `user2`. Pola `active` i `sign_in_count`
mają typy implementujące *trait* `Copy` (cecha typu, zbliżona do interfejsu),
więc zastosowanie miałoby zachowanie omówione w podrozdziale
[„Kopiowanie a przenoszenie z kolekcji”][copy]<!-- ignore -->.

<!-- Old headings. Do not remove or links may break. -->

<a id="using-tuple-structs-without-named-fields-to-create-different-types"></a>

### Tworzenie różnych typów za pomocą struktur krotkowych {#creating-different-types-with-tuple-structs}

Rust obsługuje też struktury podobne do krotek, zwane _strukturami krotkowymi_
(*tuple structs*). Struktury krotkowe mają dodatkowe znaczenie, które nadaje im
nazwa struktury, ale ich pola nie mają nazw – mają tylko typy. Struktury
krotkowe przydają się, gdy chcesz nadać nazwę całej krotce i sprawić, by była
innego typu niż pozostałe krotki, a nazywanie każdego pola jak w zwykłej
strukturze byłoby rozwlekłe lub zbędne.

Żeby zdefiniować strukturę krotkową, zacznij od słowa kluczowego `struct` i
nazwy struktury, a po nich podaj typy w krotce. Na przykład tutaj definiujemy i
używamy dwóch struktur krotkowych o nazwach `Color` i `Point`:

<Listing file-name="src/main.rs">

```aquascope,interpreter
struct Color(i32, i32, i32);
struct Point(i32, i32, i32);

fn main() {
    let black = Color(0, 0, 0);
    let origin = Point(0, 0, 0);`[]`
}
```

</Listing>

Zwróć uwagę, że wartości `black` i `origin` mają różne typy, ponieważ są
instancjami różnych struktur krotkowych. Każda zdefiniowana struktura jest
osobnym typem, nawet jeśli pola w strukturach mają te same typy. Na przykład
funkcja przyjmująca parametr typu `Color` nie może przyjąć jako argumentu
wartości `Point`, choć oba typy składają się z trzech wartości `i32`. Poza tym
instancje struktur krotkowych przypominają krotki: można je poddać
destrukturyzacji na poszczególne elementy, a do pojedynczej wartości można się
odwołać za pomocą `.` i indeksu. W odróżnieniu od krotek struktury krotkowe
wymagają podania nazwy typu struktury podczas destrukturyzacji. Na przykład,
żeby rozłożyć wartości z punktu `origin` na zmienne o nazwach `x`, `y` i `z`,
napisalibyśmy `let Point(x, y, z) = origin;`.

<!-- Old headings. Do not remove or links may break. -->

<a id="unit-like-structs-without-any-fields"></a>

### Definiowanie struktur jednostkowych {#defining-unit-like-structs}

Możesz też definiować struktury, które nie mają żadnych pól! Nazywamy je
_strukturami jednostkowymi_ (*unit-like structs*), ponieważ zachowują się
podobnie do `()`, czyli typu jednostkowego (*unit type*), o którym wspomnieliśmy
w podrozdziale [„Typ krotki”][tuples]<!-- ignore -->. Struktury jednostkowe mogą się
przydać, gdy musisz zaimplementować trait dla jakiegoś typu, ale nie masz
żadnych danych, które chcesz przechowywać w samym typie. Traity omówimy w
rozdziale 10. Oto przykład deklaracji struktury jednostkowej o nazwie
`AlwaysEqual` i utworzenia jej instancji:

```aquascope,interpreter
struct AlwaysEqual;

fn main() {
    let subject = AlwaysEqual;`[]`
}
```

Żeby zdefiniować `AlwaysEqual`, używamy słowa kluczowego `struct`, wybranej
nazwy i średnika. Nie potrzeba nawiasów klamrowych ani okrągłych! Następnie
możemy w podobny sposób uzyskać instancję `AlwaysEqual` w zmiennej `subject`:
używając zdefiniowanej nazwy, bez nawiasów klamrowych czy okrągłych. Wyobraź
sobie, że później zaimplementujemy dla tego typu zachowanie, w którym każda
instancja `AlwaysEqual` jest zawsze równa każdej instancji dowolnego innego
typu, na przykład po to, by uzyskać znany wynik na potrzeby testów. Do
zaimplementowania takiego zachowania nie potrzebowalibyśmy żadnych danych! W
rozdziale 10 zobaczysz, jak definiować traity i implementować je dla dowolnego
typu, w tym dla struktur jednostkowych.

> ### Własność danych struktury {#ownership-of-struct-data}
>
> W definicji struktury `User` w listingu 5-1 użyliśmy typu `String`, który jest
> właścicielem swoich danych, a nie typu wycinka łańcucha (*string slice*)
> `&str`. To celowy wybór, ponieważ chcemy, by każda instancja tej struktury
> była właścicielem wszystkich swoich danych i by te dane były ważne tak długo,
> jak ważna jest cała struktura.
>
> Struktury mogą też przechowywać referencje (*reference*) do danych, których
> właścicielem jest coś innego, ale wymaga to użycia _czasów życia_
> (*lifetimes*) – mechanizmu Rusta, który omówimy w rozdziale 10. Czasy życia
> gwarantują, że dane, do których odwołuje się struktura, są ważne tak długo
> jak sama struktura. Załóżmy, że spróbujesz przechować w strukturze
> referencję bez określania czasów życia, jak poniżej w pliku *src/main.rs*; to
> nie zadziała:
>
> <Listing file-name="src/main.rs">
>
> <!-- CAN'T EXTRACT SEE https://github.com/rust-lang/mdBook/issues/1127 -->
>
> ```rust,ignore,does_not_compile
> struct User {
>     active: bool,
>     username: &str,
>     email: &str,
>     sign_in_count: u64,
> }
>
> fn main() {
>     let user1 = User {
>         active: true,
>         username: "someusername123",
>         email: "someone@example.com",
>         sign_in_count: 1,
>     };
> }
> ```
>
> </Listing>
>
> Kompilator zgłosi, że potrzebuje specyfikatorów czasu życia:
>
> ```console
> $ cargo run
>    Compiling structs v0.1.0 (file:///projects/structs)
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:3:15
>   |
> 3 |     username: &str,
>   |               ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 ~     username: &'a str,
>   |
>
> error[E0106]: missing lifetime specifier
>  --> src/main.rs:4:12
>   |
> 4 |     email: &str,
>   |            ^ expected named lifetime parameter
>   |
> help: consider introducing a named lifetime parameter
>   |
> 1 ~ struct User<'a> {
> 2 |     active: bool,
> 3 |     username: &str,
> 4 ~     email: &'a str,
>   |
>
> For more information about this error, try `rustc --explain E0106`.
> error: could not compile `structs` (bin "structs") due to 2 previous errors
> ```
>
> W rozdziale 10 omówimy, jak naprawić te błędy, żeby móc przechowywać
> referencje w strukturach. Na razie będziemy naprawiać takie błędy, używając
> typów będących właścicielami swoich danych, takich jak `String`, zamiast
> referencji takich jak `&str`.

### Pożyczanie pól struktury {#borrowing-fields-of-a-struct}

Podobnie jak w podrozdziale [„Modyfikowanie różnych pól krotki”][differentfields], *borrow checker* (mechanizm sprawdzania pożyczeń) Rusta śledzi uprawnienia (*permissions*) wynikające z własności (*ownership*)
zarówno na poziomie struktury, jak i na poziomie pól. Na przykład jeśli pożyczymy (*borrow*) pole `x` struktury `Point`, to zarówno `p`, jak i `p.x` tymczasowo tracą swoje uprawnienia (ale `p.y` ich nie traci):

```aquascope,permissions,stepper,boundaries
#fn main() {
struct Point { x: i32, y: i32 }

let mut p = Point { x: 0, y: 0 };`(focus,paths:p)`
let x = &mut p.x;`(focus,paths:p)`
*x += 1;`(focus,paths:p)`
println!("{}, {}", p.x, p.y);
#}
```

W rezultacie, jeśli spróbujemy użyć `p`, gdy `p.x` jest pożyczone mutowalnie, jak tutaj:

```aquascope,permissions,stepper,boundaries,shouldFail
struct Point { x: i32, y: i32 }

fn print_point(p: &Point) {
    println!("{}, {}", p.x, p.y);
}

fn main() {
    let mut p = Point { x: 0, y: 0 };`(focus,paths:p)`
    let x = &mut p.x;`(focus,paths:p)`
    print_point(&p);`{}`
    *x += 1;`(focus,paths:p)`
}
```

to kompilator odrzuci nasz program z następującym błędem:

```text
error[E0502]: cannot borrow `p` as immutable because it is also borrowed as mutable
  --> test.rs:10:17
   |
9  |     let x = &mut p.x;
   |             -------- mutable borrow occurs here
10 |     print_point(&p);
   |                 ^^ immutable borrow occurs here
11 |     *x += 1;
   |     ------- mutable borrow later used here
```

Ogólniej: jeśli napotkasz błąd własności dotyczący struktury, zastanów się, które pola twojej struktury
mają być pożyczone i z jakimi uprawnieniami. Pamiętaj jednak o ograniczeniach borrow checkera – Rust może czasem
zakładać, że pożyczonych jest więcej pól, niż jest w rzeczywistości.

{{#quiz ../quizzes/ch05-01-structs.toml}}


<!-- manual-regeneration
for the error above
after running update-rustc.sh:
pbcopy < listings/ch05-using-structs-to-structure-related-data/no-listing-02-reference-in-struct/output.txt
paste above
add `> ` before every line -->

[tuples]: ch03-02-data-types.html#the-tuple-type
[move]: ch04-01-what-is-ownership.html
[copy]: ch04-03-fixing-ownership-errors.html#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection
[differentfields]: ch04-03-fixing-ownership-errors.html#fixing-a-safe-program-mutating-different-tuple-fields

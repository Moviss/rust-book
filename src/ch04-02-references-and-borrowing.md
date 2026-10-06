## Referencje i pożyczanie {#references-and-borrowing}

Własność (*ownership*), *boxy* (wskaźniki na dane umieszczone na stercie) i przeniesienia (*move*) dają podstawę do bezpiecznego programowania z użyciem sterty (*heap*). API oparte wyłącznie na przeniesieniach bywa jednak niewygodne. Załóżmy na przykład, że chcesz dwukrotnie odczytać kilka łańcuchów znaków (*string*):

```aquascope,interpreter,shouldFail,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");
    greet(m1, m2);`[]`
    let s = format!("{} {}", m1, m2);`[]` // Error: m1 and m2 are moved
}

fn greet(g1: String, g2: String) {
    println!("{} {}!", g1, g2);`[]`
}
```

W tym przykładzie wywołanie `greet` przenosi dane z `m1` i `m2` do parametrów `greet`. Oba łańcuchy zostają zwolnione (*drop*) na końcu `greet`, więc nie można ich użyć w `main`. Gdybyśmy spróbowali je odczytać, jak w operacji `format!(..)`, byłoby to niezdefiniowane zachowanie (*undefined behavior*). Dlatego kompilator Rusta odrzuca ten program z tym samym błędem, który widzieliśmy w poprzednim podrozdziale:

```text
error[E0382]: borrow of moved value: `m1`
 --> test.rs:5:30
 (...rest of the error...)
```

Takie zachowanie przy przeniesieniu jest wyjątkowo niewygodne. Programy często muszą użyć łańcucha więcej niż raz. Alternatywna wersja `greet` mogłaby zwracać własność łańcuchów, o tak:

```aquascope,interpreter,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");`[]`
    let (m1_again, m2_again) = greet(m1, m2);
    let s = format!("{} {}", m1_again, m2_again);`[]`
}

fn greet(g1: String, g2: String) -> (String, String) {
    println!("{} {}!", g1, g2);
    (g1, g2)
}
```

Taki styl programowania jest jednak dość rozwlekły. Rust oferuje zwięzły sposób odczytu i zapisu bez przeniesień: referencje (*references*).

### Referencje to wskaźniki, które nie są właścicielami {#references-are-non-owning-pointers}

**Referencja** to rodzaj wskaźnika. Oto przykład referencji, dzięki której program `greet` da się zapisać wygodniej:

```aquascope,interpreter,horizontal
fn main() {
    let m1 = String::from("Hello");
    let m2 = String::from("world");`[]`
    greet(&m1, &m2);`[]` // note the ampersands
    let s = format!("{} {}", m1, m2);
}

fn greet(g1: &String, g2: &String) { // note the ampersands
    `[]`println!("{} {}!", g1, g2);
}
```

Wyrażenie (*expression*) `&m1` używa operatora ampersand, by utworzyć referencję do `m1` (czyli ją „pożyczyć”). Typ parametru `g1` funkcji `greet` zmienia się na `&String`, co oznacza „referencję do `String`”.

<!-- At runtime, the references look like this:

<img src="img/experiment/ch04-02-stack1.jpg" class="center" width="350" /> -->

Zauważ, że w punkcie L2 droga od `g1` do łańcucha „Hello” prowadzi przez dwa kroki. `g1` jest referencją wskazującą na `m1` na stosie (*stack*), a `m1` jest wartością typu String zawierającą box, który wskazuje na „Hello” na stercie.

Właścicielem danych „Hello” na stercie jest `m1`, ale `g1` _nie_ jest właścicielem ani `m1`, ani „Hello”. Dlatego gdy `greet` się kończy i program dochodzi do punktu L3, żadne dane na stercie nie zostają zdealokowane. Znika tylko ramka stosu (*stack frame*) `greet`. Jest to zgodne z naszą *zasadą dealokacji boxa*. Ponieważ `g1` nie było właścicielem „Hello”, Rust nie zdealokował „Hello” w imieniu `g1`.

Referencje są **wskaźnikami niebędącymi właścicielami** (*non-owning pointers*), ponieważ nie są właścicielami danych, na które wskazują.

### Dereferencja wskaźnika daje dostęp do jego danych {#dereferencing-a-pointer-accesses-its-data}

Poprzednie przykłady z boxami i łańcuchami nie pokazywały, jak Rust „podąża” za wskaźnikiem do jego danych. Na przykład makro `println!` w tajemniczy sposób działało zarówno dla łańcuchów posiadanych na własność, typu `String`, jak i dla referencji do łańcuchów, typu `&String`. Mechanizmem, który za tym stoi, jest operator **dereferencji** (*dereference*), zapisywany gwiazdką (`*`). Oto na przykład program, który na kilka sposobów używa dereferencji:

```aquascope,interpreter
# fn main() {
let mut x: Box<i32> = Box::new(1);
let a: i32 = *x;         // *x reads the heap value, so a = 1
*x += 1;                 // *x on the left-side modifies the heap value,
                         //     so x points to the value 2

let r1: &Box<i32> = &x;  // r1 points to x on the stack
let b: i32 = **r1;       // two dereferences get us to the heap value

let r2: &i32 = &*x;      // r2 points to the heap value directly
let c: i32 = *r2;`[]`    // so only one dereference is needed to read it
# }
```

Zwróć uwagę na różnicę: `r1` wskazuje na `x` na stosie, a `r2` na wartość `2` na stercie.

Czytając kod w Ruście, raczej rzadko zobaczysz operator dereferencji. W niektórych sytuacjach, na przykład przy wywoływaniu metody operatorem kropki, Rust niejawnie wstawia dereferencje i referencje. Ten program pokazuje na przykład dwa równoważne sposoby wywołania funkcji [`i32::abs`](https://doc.rust-lang.org/std/primitive.i32.html#method.abs) (wartość bezwzględna) i [`str::len`](https://doc.rust-lang.org/std/primitive.str.html#method.len) (długość łańcucha):

```rust,ignore
# fn main()  {
let x: Box<i32> = Box::new(-1);
let x_abs1 = i32::abs(*x); // explicit dereference
let x_abs2 = x.abs();      // implicit dereference
assert_eq!(x_abs1, x_abs2);

let r: &Box<i32> = &x;
let r_abs1 = i32::abs(**r); // explicit dereference (twice)
let r_abs2 = r.abs();       // implicit dereference (twice)
assert_eq!(r_abs1, r_abs2);

let s = String::from("Hello");
let s_len1 = str::len(&s); // explicit reference
let s_len2 = s.len();      // implicit reference
assert_eq!(s_len1, s_len2);
# }
```

Ten przykład pokazuje niejawne konwersje na trzy sposoby:
1. Funkcja `i32::abs` oczekuje argumentu typu `i32`. Żeby wywołać `abs` z wartością `Box<i32>`, możesz jawnie wykonać dereferencję boxa: `i32::abs(*x)`. Możesz też wykonać ją niejawnie, używając składni wywołania metody: `x.abs()`. Składnia z kropką jest lukrem składniowym dla składni wywołania funkcji.

2. Ta niejawna konwersja działa dla wielu poziomów wskaźników. Na przykład wywołanie `abs` na referencji do boxa `r: &Box<i32>` wstawi dwie dereferencje.

3. Konwersja działa też w przeciwnym kierunku. Funkcja `str::len` oczekuje referencji `&str`. Jeśli wywołasz `len` na posiadanym na własność `String`, Rust wstawi jeden operator pożyczenia. (W rzeczywistości zachodzi tu jeszcze jedna konwersja, z `String` na `str`!)

O wywołaniach metod i niejawnych konwersjach powiemy więcej w kolejnych rozdziałach. Na razie najważniejsze jest to, że takie konwersje zachodzą przy wywołaniach metod i w niektórych makrach, takich jak `println`. Chcemy rozwikłać całą „magię” Rusta, żeby dać ci jasny model myślowy tego, jak działa Rust.

{{#quiz ../quizzes/ch04-02-references-sec1-basics.toml}}

### Rust nie dopuszcza jednoczesnego aliasowania i modyfikowania {#rust-avoids-simultaneous-aliasing-and-mutation}

Wskaźniki to potężny i niebezpieczny mechanizm, ponieważ umożliwiają **aliasowanie** (*aliasing*). Aliasowanie to dostęp do tych samych danych przez różne zmienne. Samo w sobie aliasowanie jest nieszkodliwe. W połączeniu z **modyfikowaniem** (*mutation*) daje jednak przepis na katastrofę. Jedna zmienna może na wiele sposobów „wyciągnąć dywan spod nóg” innej, na przykład:

- dealokując współdzielone dane, przez co druga zmienna wskazuje na zdealokowaną pamięć;
- modyfikując współdzielone dane, przez co przestają obowiązywać właściwości, których druga zmienna oczekuje w czasie działania programu;
- modyfikując współdzielone dane _współbieżnie_, co powoduje wyścig danych z niedeterministycznym zachowaniem drugiej zmiennej.

W kolejnych przykładach będziemy przyglądać się programom używającym struktury danych zwanej wektorem, [`Vec`]. W odróżnieniu od tablic, które mają stałą długość, wektory mają zmienną długość, bo przechowują elementy na stercie. Na przykład [`Vec::push`] dodaje element na koniec wektora, o tak:

```aquascope,interpreter,horizontal
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];`[]`
v.push(4);`[]`
#}
```

Makro `vec!` tworzy wektor z elementów podanych w nawiasach kwadratowych. Wektor `v` ma typ `Vec<i32>`. Składnia `<i32>` oznacza, że elementy wektora mają typ `i32`.

Ważnym szczegółem implementacji jest to, że `v` alokuje na stercie tablicę o określonej *pojemności* (*capacity*). Możemy zajrzeć do wnętrza `Vec` i sami zobaczyć ten szczegół:

```aquascope,interpreter,horizontal,concreteTypes
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];`[]`
#}
```

> *Uwaga:* kliknij ikonę lornetki w prawym górnym rogu diagramu, by w dowolnym diagramie pamięci przełączyć ten szczegółowy widok.

Zauważ, że wektor ma długość (`len`) 3 i pojemność (`cap`) 3. Wektor jest zapełniony. Dlatego przy wywołaniu `push` musi utworzyć nową alokację o większej pojemności, skopiować do niej wszystkie elementy i zdealokować pierwotną tablicę na stercie. Na diagramie powyżej tablica `1 2 3 4` znajduje się (potencjalnie) w innym miejscu pamięci niż pierwotna tablica `1 2 3`.

Żeby powiązać to z bezpieczeństwem pamięci, dorzućmy do tego referencje. Załóżmy, że utworzyliśmy referencję do danych wektora na stercie. Wtedy wywołanie push może unieważnić tę referencję, co symuluje poniższy przykład:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];`[]`
v.push(4);`[]`
println!("Third element is {}", *num);`[]`
#}
```

Na początku `v` wskazuje na tablicę z 3 elementami na stercie. Następnie tworzymy `num` jako referencję do trzeciego elementu, co widać w punkcie L1. Operacja `v.push(4)` zmienia jednak rozmiar `v`. Zmiana rozmiaru dealokuje poprzednią tablicę i alokuje nową, większą. W efekcie `num` wskazuje na nieprawidłową pamięć. Dlatego w punkcie L3 dereferencja `*num` odczytuje nieprawidłową pamięć, co powoduje niezdefiniowane zachowanie.

Mówiąc bardziej abstrakcyjnie, problem polega na tym, że wektor `v` jest jednocześnie aliasowany (przez referencję `num`) i modyfikowany (przez operację `v.push(4)`). Żeby unikać takich problemów, Rust przestrzega podstawowej zasady:

> **Zasada bezpieczeństwa wskaźników:** dane nigdy nie powinny być jednocześnie aliasowane i modyfikowane.

Dane mogą być aliasowane. Dane mogą być modyfikowane. Ale dane nie mogą być _jednocześnie_ aliasowane _i_ modyfikowane. Na przykład w przypadku boxów (wskaźników będących właścicielami) Rust egzekwuje tę zasadę, zabraniając aliasowania. Przypisanie boxa z jednej zmiennej do drugiej przenosi własność i unieważnia poprzednią zmienną. Do danych posiadanych na własność można sięgać tylko przez ich właściciela &mdash; bez aliasów.

Referencje są jednak wskaźnikami niebędącymi właścicielami, więc potrzebują innych reguł niż boxy, żeby zapewnić przestrzeganie *zasady bezpieczeństwa wskaźników*. Referencje z założenia służą do tymczasowego tworzenia aliasów. W dalszej części tego podrozdziału wyjaśnimy podstawy tego, jak Rust zapewnia bezpieczeństwo referencji za pomocą ***borrow checkera*** (mechanizmu sprawdzania pożyczeń).

### Referencje zmieniają uprawnienia do miejsc {#references-change-permissions-on-places}

Podstawowa idea działania *borrow checkera* polega na tym, że zmienne mają trzy rodzaje **uprawnień** (*permissions*) do swoich danych:

- **R** (*read*, odczyt), @Perm{read}: dane można skopiować w inne miejsce;
- **W** (*write*, zapis), @Perm{write}: dane można modyfikować;
- **O** (*own*, własność), @Perm{own}: dane można przenieść lub zwolnić.

Te uprawnienia nie istnieją w czasie działania programu, tylko w kompilatorze. Opisują, jak kompilator „myśli” o twoim programie, zanim ten zostanie wykonany.

Domyślnie zmienna ma do swoich danych uprawnienia odczytu i własności (@Perm{read}@Perm{own}). Jeśli zmienna jest zadeklarowana przez `let mut`, ma też uprawnienie zapisu (@Perm{write}). Kluczowa idea polega na tym, że
**referencje mogą tymczasowo odbierać te uprawnienia.**

Żeby to zilustrować, przyjrzyjmy się uprawnieniom w wariancie powyższego programu, który faktycznie jest bezpieczny. Wywołanie `push` zostało przesunięte za `println!`. Uprawnienia w tym programie przedstawiamy na nowym rodzaju diagramu. Diagram pokazuje zmiany uprawnień w każdej linii.

```aquascope,permissions,stepper
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];
println!("Third element is {}", *num);
v.push(4);
#}
```

Przejdźmy przez kolejne linie:

1. Po `let mut v = (...)` zmienna `v` zostaje zainicjalizowana (wskazuje na to ikona <i class="fa fa-arrow-turn-up"></i>). Zyskuje uprawnienia @Perm[gained]{read}@Perm[gained]{write}@Perm[gained]{own} (znak plus oznacza zyskanie).
2. Po `let num = &v[2]` dane w `v` zostają **pożyczone** przez `num` (wskazuje na to ikona <i class="fa fa-arrow-right"></i>). Dzieją się trzy rzeczy:
   - Pożyczenie odbiera `v` uprawnienia @Perm[lost]{write}@Perm[lost]{own} (ukośnik oznacza utratę). `v` nie można zapisywać ani posiadać na własność, ale wciąż można je odczytywać.
   - Zmienna `num` zyskuje uprawnienia @Perm{read}@Perm{own}. `num` nie jest zapisywalne (brak uprawnienia @Perm{write} pokazano kreską <span class="perm write">‒</span>), ponieważ nie zostało zadeklarowane przez `let mut`.
   - **Miejsce** (*place*) `*num` zyskuje uprawnienie @Perm{read}.
3. Po `println!(...)` zmienna `num` przestaje być używana, więc `v` przestaje być pożyczone. Dlatego:
   - `v` odzyskuje uprawnienia @Perm{write}@Perm{own} (wskazuje na to ikona <i class="fa fa-rotate-left"></i>);
   - `num` i `*num` tracą wszystkie uprawnienia (wskazuje na to ikona <i class="fa fa-arrow-turn-down"></i>).
4. Po `v.push(4)` zmienna `v` przestaje być używana i traci wszystkie uprawnienia.

Przyjrzyjmy się teraz kilku niuansom diagramu. Po pierwsze, dlaczego widać zarówno `num`, jak i `*num`? Ponieważ dostęp do danych przez referencję to coś innego niż operowanie na samej referencji. Załóżmy na przykład, że zadeklarowaliśmy referencję do liczby przez `let mut`:

```aquascope,permissions,stepper
#fn main() {
let x = 0;
let mut x_ref = &x;
# println!("{x_ref} {x}");
#}
```

Zauważ, że `x_ref` ma uprawnienie @Perm{write}, a `*x_ref` go nie ma. Oznacza to, że możemy przypisać zmiennej `x_ref` inną referencję (np. `x_ref = &y`), ale nie możemy modyfikować danych, na które wskazuje (np. `*x_ref += 1`).

Mówiąc ogólniej, uprawnienia są zdefiniowane dla **miejsc**, a nie tylko dla zmiennych. Miejsce to wszystko, co może stać po lewej stronie przypisania. Miejscami są:

- zmienne, np. `a`;
- dereferencje miejsc, np. `*a`;
- dostępy do elementów tablicy w miejscach, np. `a[0]`;
- pola miejsc, np. `a.0` dla krotek (*tuples*) lub `a.field` dla struktur (*structs*), omówionych w następnym rozdziale;
- dowolne połączenia powyższych, np. `*((*a)[0].1)`.


Po drugie, dlaczego miejsca tracą uprawnienia, gdy przestają być używane? Ponieważ niektóre uprawnienia wzajemnie się wykluczają. Jeśli napiszesz `num = &v[2]`, to `v` nie może być modyfikowane ani zwolnione, dopóki `num` jest w użyciu. Nie znaczy to jednak, że ponowne użycie `num` jest niedozwolone. Jeśli na przykład dodamy do powyższego programu kolejne `println!`, to `num` po prostu straci uprawnienia jedną linię później:

```aquascope,permissions,stepper
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];
println!("Third element is {}", *num);
println!("Again, the third element is {}", *num);
v.push(4);
#}
```

Problem pojawia się dopiero wtedy, gdy spróbujesz użyć `num` ponownie *po* zmodyfikowaniu `v`. Przyjrzyjmy się temu dokładniej.


### Borrow checker wykrywa naruszenia uprawnień {#the-borrow-checker-finds-permission-violations}

Przypomnij sobie *zasadę bezpieczeństwa wskaźników*: dane nie powinny być jednocześnie aliasowane i modyfikowane. Celem uprawnień jest zagwarantowanie, że dane nie mogą być modyfikowane, jeśli są aliasowane. Utworzenie referencji do danych (czyli ich „pożyczenie”) sprawia, że dane te są tymczasowo tylko do odczytu, dopóki referencja jest w użyciu.

Rust korzysta z tych uprawnień w swoim **borrow checkerze**. *Borrow checker* szuka potencjalnie niebezpiecznych operacji z udziałem referencji. Wróćmy do niebezpiecznego programu, który widzieliśmy wcześniej, gdzie `push` unieważnia referencję. Tym razem dodamy do diagramu uprawnień jeszcze jeden element:

```aquascope,permissions,boundaries,stepper,shouldFail
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &i32 = &v[2];`{}`
v.push(4);`{}`
println!("Third element is {}", *num);
#}
```

Za każdym razem, gdy miejsce jest używane, Rust oczekuje, że będzie ono miało określone uprawnienia, zależnie od operacji. Na przykład pożyczenie `&v[2]` wymaga, by `v` dało się odczytać. Dlatego między operacją `&` a miejscem `v` widać uprawnienie @Perm{read}. Litera jest wypełniona, ponieważ w tej linii `v` ma uprawnienie odczytu.

Natomiast modyfikująca operacja `v.push(4)` wymaga, by `v` dało się odczytać i zapisać. Widoczne są zarówno @Perm{read}, jak i @Perm{write}. `v` nie ma jednak uprawnienia zapisu (jest pożyczone przez `num`). Dlatego litera @Perm[missing]{write} jest pusta w środku, co oznacza, że uprawnienie zapisu jest *oczekiwane*, ale `v` go nie ma.

Jeśli spróbujesz skompilować ten program, kompilator Rusta zgłosi następujący błąd:

```text
error[E0502]: cannot borrow `v` as mutable because it is also borrowed as immutable
 --> test.rs:4:1
  |
3 | let num: &i32 = &v[2];
  |                  - immutable borrow occurs here
4 | v.push(4);
  | ^^^^^^^^^ mutable borrow occurs here
5 | println!("Third element is {}", *num);
  |                                 ---- immutable borrow later used here
```

Komunikat o błędzie wyjaśnia, że `v` nie może być modyfikowane, dopóki referencja `num` jest w użyciu. To powód widoczny na powierzchni &mdash; problem leżący u podstaw polega na tym, że `push` mógłby unieważnić `num`. Rust wychwytuje to potencjalne naruszenie bezpieczeństwa pamięci.


### Referencje mutowalne zapewniają unikalny dostęp do danych bez własności {#mutable-references-provide-unique-and-non-owning-access-to-data}

Referencje, które widzieliśmy dotąd, to referencje tylko do odczytu, czyli **referencje niemutowalne** (*immutable references*), nazywane też **referencjami współdzielonymi** (*shared references*). Referencje niemutowalne pozwalają na aliasowanie, ale nie na modyfikowanie. Przydaje się jednak także możliwość tymczasowego udostępnienia danych do modyfikacji bez ich przenoszenia.

Służą do tego **referencje mutowalne** (*mutable references*), nazywane też **referencjami unikalnymi** (*unique references*). Oto prosty przykład referencji mutowalnej wraz z towarzyszącymi zmianami uprawnień:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &mut i32 = &mut v[2];
*num += 1;
println!("Third element is {}", *num);
println!("Vector is now {:?}", v);
#}
```

<blockquote><div style="margin-block-start: 1em; margin-block-end: 1em"><i>Uwaga:</i> gdy oczekiwane uprawnienia nie mają w danym przykładzie istotnego znaczenia, będziemy je skracać do kropek, np. <div class="permission-stack stack-size-2"><div class="perm read"><div class="small">•</div><div class="big">R</div></div><div class="perm write"><div class="small">•</div><div class="big">W</div></div></div>. Najedź myszą na kółka (albo dotknij ich na ekranie dotykowym), by zobaczyć odpowiadające im litery uprawnień.</div></blockquote>

Referencję mutowalną tworzy się operatorem `&mut`. Typ `num` zapisujemy jako `&mut i32`. W porównaniu z referencjami niemutowalnymi w uprawnieniach widać dwie ważne różnice:

1. Gdy `num` było referencją niemutowalną, `v` wciąż miało uprawnienie @Perm{read}. Teraz, gdy `num` jest referencją mutowalną, `v` traci _wszystkie_ uprawnienia na czas, gdy `num` jest w użyciu.
2. Gdy `num` było referencją niemutowalną, miejsce `*num` miało tylko uprawnienie @Perm{read}. Teraz, gdy `num` jest referencją mutowalną, `*num` zyskało też uprawnienie @Perm{write}.

Pierwsza obserwacja sprawia, że referencje mutowalne są *bezpieczne*. Referencje mutowalne pozwalają na modyfikowanie, ale zapobiegają aliasowaniu. Pożyczonego miejsca `v` tymczasowo nie można używać, więc w praktyce nie jest ono aliasem.

Druga obserwacja sprawia, że referencje mutowalne są *przydatne*. `v[2]` można modyfikować przez `*num`. Na przykład `*num += 1` modyfikuje `v[2]`. Zauważ, że `*num` ma uprawnienie @Perm{write}, ale `num` go nie ma. `num` oznacza samą referencję mutowalną, np. `num` nie można przypisać *innej* referencji mutowalnej.

Referencje mutowalne można też tymczasowo „zdegradować” do referencji tylko do odczytu. Na przykład:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut v: Vec<i32> = vec![1, 2, 3];
let num: &mut i32 = &mut v[2];`(focus,paths:*num)`
let num2: &i32 = &*num;`(focus,paths:*num)`
println!("{} {}", *num, *num2);
#}
```

> *Uwaga:* gdy zmiany uprawnień nie mają znaczenia w danym przykładzie, będziemy je ukrywać. Ukryte kroki możesz wyświetlić, klikając „»”, a ukryte uprawnienia w obrębie kroku – klikając „● ● ●”.

W tym programie pożyczenie `&*num` odbiera `*num` uprawnienie @Perm{write}, ale _nie_ uprawnienie @Perm{read}, więc `println!(..)` może odczytać zarówno `*num`, jak i `*num2`.


### Uprawnienia wracają na końcu czasu życia referencji {#permissions-are-returned-at-the-end-of-a-references-lifetime}

Napisaliśmy wyżej, że referencja zmienia uprawnienia, dopóki jest „w użyciu”. Określenie „w użyciu” opisuje **czas życia** (*lifetime*) referencji, czyli fragment kodu od jej narodzin (gdzie referencja zostaje utworzona) do jej śmierci (ostatniego użycia lub ostatnich użyć referencji).

Na przykład w tym programie czas życia `y` zaczyna się od `let y = &x`, a kończy na `let z = *y`:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut x = 1;
let y = &x;`(focus,paths:x)`
let z = *y;`(focus,paths:x)`
x += z;
#}
```

Uprawnienie @Perm{write} wraca do `x` po zakończeniu czasu życia `y`, tak jak widzieliśmy już wcześniej.

W poprzednich przykładach czas życia był ciągłym fragmentem kodu. Gdy jednak pojawia się przepływ sterowania (*control flow*), nie musi tak być. Oto na przykład funkcja, która zamienia na wielką literę pierwszy znak w wektorze znaków ASCII:

```aquascope,permissions,stepper,boundaries
fn ascii_capitalize(v: &mut Vec<char>) {
    let c = &v[0];`(focus,paths:*v)`
    if c.is_ascii_lowercase() {
        let up = c.to_ascii_uppercase();`(focus,paths:*v)`
        v[0] = up;
    } else {`(focus,paths:*v)`
        println!("Already capitalized: {:?}", v);
    }
}
```

Zmienna `c` ma w każdej gałęzi instrukcji if inny czas życia. W bloku then `c` jest używane w wyrażeniu `c.to_ascii_uppercase()`. Dlatego `*v` odzyskuje uprawnienie @Perm{write} dopiero po tej linii.

W bloku else `c` nie jest natomiast używane. `*v` odzyskuje uprawnienie @Perm{write} od razu po wejściu do bloku else.

{{#quiz ../quizzes/ch04-02-references-sec2-perms.toml}}


### Dane muszą żyć dłużej niż wszystkie referencje do nich {#data-must-outlive-all-of-its-references}

W ramach *zasady bezpieczeństwa wskaźników* *borrow checker* pilnuje, by **dane żyły dłużej niż wszystkie referencje do nich.** Rust egzekwuje tę właściwość na dwa sposoby. Pierwszy dotyczy referencji, które są tworzone i zwalniane w zasięgu (*scope*) jednej funkcji. Załóżmy na przykład, że próbujemy zwolnić łańcuch, trzymając referencję do niego:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let s = String::from("Hello world");
let s_ref = &s;`(focus,rxpaths:s$)`
drop(s);`{}`
println!("{}", s_ref);
#}
```

Do wychwytywania takich błędów Rust używa omówionych już uprawnień. Pożyczenie `&s` odbiera `s` uprawnienie @Perm{own}. `drop` oczekuje jednak uprawnienia @Perm{own}, co prowadzi do niezgodności uprawnień.

Kluczowe jest to, że w tym przykładzie Rust wie, jak długo żyje `s_ref`. Gdy jednak nie wie, jak długo żyje referencja, potrzebuje innego mechanizmu egzekwowania. Dotyczy to konkretnie referencji, które są danymi wejściowymi funkcji albo jej wynikiem. Oto na przykład bezpieczna funkcja, która zwraca referencję do pierwszego elementu wektora:

```aquascope,permissions,boundaries,showFlows
fn first(strings: &Vec<String>) -> &String {
    let s_ref = &strings[0];
    s_ref`{}`
}
```

Ten fragment wprowadza nowy rodzaj uprawnienia: F (*flow*, przepływ), oznaczane @Perm{flow}. Uprawnienie @Perm{flow} jest oczekiwane zawsze wtedy, gdy wyrażenie używa referencji wejściowej (jak `&strings[0]`) albo zwraca referencję wyjściową (jak `return s_ref`).

W odróżnieniu od uprawnień @Perm{read}@Perm{write}@Perm{own} uprawnienie @Perm{flow} nie zmienia się w obrębie ciała funkcji. Referencja ma uprawnienie @Perm{flow}, jeśli wolno jej zostać użytej (czyli *przepłynąć*) w danym wyrażeniu. Załóżmy na przykład, że zmienimy `first` w nową funkcję `first_or`, która ma parametr `default`:

```aquascope,permissions,boundaries,showFlows,shouldFail
fn first_or<'a, 'b, 'c>(strings: &'a Vec<String>, default: &'b String) -> &'c String {
    if strings.len() > 0 {
        &strings[0]`{}`
    } else {
        default`{}`
    }
}
```

Ta funkcja już się nie kompiluje, ponieważ wyrażenia `&strings[0]` i `default` nie mają uprawnienia @Perm{flow} potrzebnego do zwrócenia ich z funkcji. Ale dlaczego? Rust zgłasza następujący błąd:

```text
error[E0106]: missing lifetime specifier
 --> test.rs:1:57
  |
1 | fn first_or(strings: &Vec<String>, default: &String) -> &String {
  |                      ------------           -------     ^ expected named lifetime parameter
  |
  = help: this function's return type contains a borrowed value, but the signature does not say whether it is borrowed from `strings` or `default`
```

Komunikat „missing lifetime specifier” jest dość zagadkowy, ale komunikat pomocy podaje przydatny kontekst. Jeśli Rust patrzy *tylko* na sygnaturę funkcji, nie wie, czy wynik `&String` jest referencją do `strings`, czy do `default`. Żeby zrozumieć, dlaczego to ważne, załóżmy, że użyliśmy `first_or` w ten sposób:

```rust,ignore
fn main() {
    let strings = vec![];
    let default = String::from("default");
    let s = first_or(&strings, &default);
    drop(default);
    println!("{}", s);
}
```

Ten program jest niebezpieczny, jeśli `first_or` pozwala, by `default` *przepłynęło* do wartości zwracanej. Podobnie jak w poprzednim przykładzie `drop` mógłby unieważnić `s`. Rust pozwoliłby skompilować ten program tylko wtedy, gdyby miał *pewność*, że `default` nie może przepłynąć do wartości zwracanej.

Do określania, czy `default` może zostać zwrócone, Rust udostępnia mechanizm zwany *parametrami czasu życia*. Wyjaśnimy go później, w podrozdziale 10.3 [„Sprawdzanie poprawności referencji za pomocą czasów życia”](ch10-03-lifetime-syntax.html). Na razie wystarczy wiedzieć, że: (1) referencje wejściowe i wyjściowe są traktowane inaczej niż referencje w ciele funkcji oraz (2) do sprawdzania bezpieczeństwa tych referencji Rust używa innego mechanizmu, czyli uprawnienia @Perm{flow}.

Żeby zobaczyć uprawnienie @Perm{flow} w innym kontekście, załóżmy, że próbujesz zwrócić referencję do zmiennej na stosie, o tak:

```aquascope,permissions,boundaries,showFlows,shouldFail
fn return_a_string() -> &String {
    let s = String::from("Hello world");
    let s_ref = &s;
    s_ref`{}`
}
```

Ten program jest niebezpieczny, ponieważ referencja `&s` zostanie unieważniona, gdy `return_a_string` zwróci wartość. Rust odrzuci ten program z podobnym błędem `missing lifetime specifier`. Teraz już rozumiesz, że ten błąd oznacza, iż `s_ref` nie ma odpowiednich uprawnień przepływu.


{{#quiz ../quizzes/ch04-02-references-sec3-safety.toml}}


### Podsumowanie {#summary}

Referencje pozwalają odczytywać i zapisywać dane bez przejmowania ich na własność. Referencje tworzy się przez pożyczenie (`&` i `&mut`), a używa przez dereferencję (`*`), często niejawną.

Referencji łatwo jednak użyć niewłaściwie. *Borrow checker* Rusta egzekwuje system uprawnień, który gwarantuje, że referencje są używane bezpiecznie:

- Wszystkie zmienne mogą odczytywać swoje dane, być ich właścicielami i (opcjonalnie) je zapisywać.
- Utworzenie referencji przenosi uprawnienia z pożyczonego miejsca na referencję.
- Uprawnienia wracają, gdy kończy się czas życia referencji.
- Dane muszą żyć dłużej niż wszystkie referencje, które na nie wskazują.

Pewnie masz wrażenie, że w tym podrozdziale opisaliśmy więcej tego, czego Rust _nie_ potrafi, niż tego, co _potrafi_. To celowe! Jedną z podstawowych cech Rusta jest to, że pozwala używać wskaźników bez odśmiecania pamięci (*garbage collection*), a jednocześnie unikać niezdefiniowanego zachowania. Zrozumienie tych reguł bezpieczeństwa teraz pomoże ci uniknąć frustracji w zmaganiach z kompilatorem później.

[`String::push_str`]: https://doc.rust-lang.org/std/string/struct.String.html#method.push_str
[`Vec`]: https://doc.rust-lang.org/std/vec/struct.Vec.html
[`Vec::push`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.push
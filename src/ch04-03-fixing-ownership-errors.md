## Naprawianie błędów własności {#fixing-ownership-errors}

Naprawianie błędów związanych z własnością (*ownership*) to jedna z podstawowych umiejętności w Ruście. Co zrobić, gdy *borrow checker* (mechanizm sprawdzania pożyczeń) odrzuci twój kod? W tym podrozdziale omówimy kilka studiów przypadków typowych błędów własności. W każdym z nich pokażemy funkcję odrzuconą przez kompilator. Następnie wyjaśnimy, dlaczego Rust ją odrzuca, i pokażemy kilka sposobów, by ją naprawić.

Powracającym motywem będzie ustalanie, czy funkcja jest *naprawdę* bezpieczna, czy niebezpieczna. Rust zawsze odrzuci niebezpieczny program[^safe-subset]. Czasem jednak Rust odrzuci również program bezpieczny. Te studia przypadków pokażą, jak reagować na błędy w obu sytuacjach.

<!-- The last two sections have shown how a Rust program can be **unsafe** if it triggers undefined behavior. The ownership guarantee is that Rust will reject all unsafe programs. However, Rust will also reject *some* safe programs. Fixing an ownership error will depend on whether your program is *actually* safe or unsafe. -->

### Naprawianie niebezpiecznego programu: zwracanie referencji do stosu {#fixing-an-unsafe-program-returning-a-reference-to-the-stack}

Pierwsze studium przypadku dotyczy zwracania referencji (*reference*) do stosu (*stack*), tak jak omawialiśmy w poprzednim podrozdziale w części [„Dane muszą żyć dłużej niż wszystkie referencje do nich”](ch04-02-references-and-borrowing.html#data-must-outlive-all-of-its-references). Oto funkcja, którą tam oglądaliśmy:

```rust,ignore,does_not_compile
fn return_a_string() -> &String {
    let s = String::from("Hello world");
    &s
}
```

Zastanawiając się, jak naprawić tę funkcję, musimy zapytać: **dlaczego ten program jest niebezpieczny?** Problem dotyczy tu czasu życia (*lifetime*) danych, do których odnosi się referencja. Jeśli chcesz przekazywać dalej referencję do łańcucha znaków (*string*), musisz zadbać o to, by sam łańcuch żył wystarczająco długo. 

W zależności od sytuacji możesz wydłużyć czas życia łańcucha na cztery sposoby. Pierwszy to przeniesienie (*move*) własności łańcucha poza funkcję przez zamianę `&String` na `String`:

```rust
fn return_a_string() -> String {
    let s = String::from("Hello world");
    s
}
```

Inną możliwością jest zwrócenie literału łańcuchowego, który żyje wiecznie (wskazuje na to `'static`). To rozwiązanie sprawdza się, jeśli nigdy nie zamierzamy zmieniać łańcucha – wtedy alokacja na stercie (*heap*) jest zbędna:

```rust
fn return_a_string() -> &'static str {
    "Hello world"    
}
```

Kolejną możliwością jest odłożenie sprawdzania pożyczeń do czasu działania programu dzięki odśmiecaniu pamięci (*garbage collection*). Możesz na przykład użyć [wskaźnika ze zliczaniem referencji][rc]:

```rust
use std::rc::Rc;
fn return_a_string() -> Rc<String> {
    let s = Rc::new(String::from("Hello world"));
    Rc::clone(&s)
}
```

Zliczanie referencji (*reference counting*) omówimy dokładniej w podrozdziale 15.4 [„`Rc<T>`, inteligentny wskaźnik ze zliczaniem referencji”](ch15-04-rc.html). W skrócie: `Rc::clone` klonuje tylko wskaźnik do `s`, a nie same dane. W czasie działania `Rc` sprawdza, kiedy zostaje zwolniony ostatni `Rc` wskazujący na dane, i wtedy dealokuje dane.

Jeszcze inną możliwością jest to, by wywołujący zapewnił „miejsce” na łańcuch w postaci referencji mutowalnej (*mutable*):

```rust
fn return_a_string(output: &mut String) {
    output.replace_range(.., "Hello world");
}
```

W tej strategii to wywołujący odpowiada za przygotowanie miejsca na łańcuch. Taki styl bywa rozwlekły, ale może też oszczędzać pamięć, jeśli wywołujący musi dokładnie kontrolować, kiedy następują alokacje.

Która strategia jest najwłaściwsza, zależy od twojej aplikacji. Kluczowe jest jednak rozpoznanie podstawowego problemu, który kryje się pod powierzchownym błędem własności. Jak długo powinien żyć mój łańcuch? Kto powinien odpowiadać za jego dealokację? Gdy masz jasne odpowiedzi na te pytania, pozostaje już tylko dopasować do nich API.


### Naprawianie niebezpiecznego programu: za mało uprawnień {#fixing-an-unsafe-program-not-enough-permissions}

Innym częstym problemem jest próba modyfikowania danych tylko do odczytu albo próba zwolnienia (*drop*) danych schowanych za referencją. Załóżmy na przykład, że próbujemy napisać funkcję `stringify_name_with_title`. Ma ona utworzyć pełne imię i nazwisko osoby z wektora jego części, dodając na końcu tytuł.

```aquascope,permissions,stepper,boundaries,shouldFail
fn stringify_name_with_title(name: &Vec<String>) -> String {
    name.push(String::from("Esq."));`{}`
    let full = name.join(" ");
    full
}

// ideally: ["Ferris", "Jr."] => "Ferris Jr. Esq."
```

*Borrow checker* odrzuca ten program, ponieważ `name` jest niemutowalną referencją, a `name.push(..)` wymaga uprawnienia (*permission*) @Perm{write} (*write*, zapis). Ten program jest niebezpieczny, ponieważ `push` mogłoby unieważnić inne referencje do `name` poza `stringify_name_with_title`, na przykład tak:

```aquascope,interpreter,shouldFail,horizontal
#fn stringify_name_with_title(name: &Vec<String>) -> String {
#    name.push(String::from("Esq."));
#    let full = name.join(" ");
#    full
#}
fn main() {
    let name = vec![String::from("Ferris")];
    let first = &name[0];`[]`
    stringify_name_with_title(&name);`[]`
    println!("{}", first);`[]`
}
```

W tym przykładzie przed wywołaniem `stringify_name_with_title` tworzona jest referencja `first` do `name[0]`. Funkcja `name.push(..)` realokuje zawartość `name`, co unieważnia `first`, przez co `println` odczytuje zdealokowaną pamięć.

Jak więc naprawić to API? Jednym z prostych rozwiązań jest zmiana typu `name` z `&Vec<String>` na `&mut Vec<String>`:

```rust,ignore
fn stringify_name_with_title(name: &mut Vec<String>) -> String {
    name.push(String::from("Esq."));
    let full = name.join(" ");
    full
}
```

To jednak nie jest dobre rozwiązanie! **Funkcje nie powinny modyfikować swoich danych wejściowych, jeśli wywołujący by się tego nie spodziewał.** Osoba wywołująca `stringify_name_with_title` raczej nie oczekuje, że ta funkcja zmodyfikuje jej wektor. Od innej funkcji, np. `add_title_to_name`, można by oczekiwać modyfikacji danych wejściowych, ale nie od naszej.

Inną opcją jest przejęcie własności imienia przez zamianę `&Vec<String>` na `Vec<String>`:

```rust,ignore
fn stringify_name_with_title(mut name: Vec<String>) -> String {
    name.push(String::from("Esq."));
    let full = name.join(" ");
    full
}
```

To również nie jest dobre rozwiązanie! **Funkcje w Ruście bardzo rzadko przejmują własność struktur danych będących właścicielami danych na stercie, takich jak `Vec` i `String`.**  Ta wersja `stringify_name_with_title` uniemożliwiłaby dalsze użycie wejściowego `name`, co jest bardzo uciążliwe dla wywołującego, jak omawialiśmy na początku podrozdziału [„Referencje i pożyczanie”](ch04-02-references-and-borrowing.html).

Wybór `&Vec` jest więc w rzeczywistości dobry i *nie* chcemy go zmieniać. Zamiast tego możemy zmienić ciało funkcji. Istnieje wiele możliwych poprawek, które różnią się zużyciem pamięci. Jedną z możliwości jest sklonowanie wejściowego `name`:

```rust,ignore
fn stringify_name_with_title(name: &Vec<String>) -> String {
    let mut name_clone = name.clone();
    name_clone.push(String::from("Esq."));
    let full = name_clone.join(" ");
    full
}
```

Dzięki sklonowaniu `name` możemy modyfikować lokalną kopię wektora. Klonowanie kopiuje jednak każdy łańcuch z danych wejściowych. Zbędnych kopii unikniemy, jeśli dodamy przyrostek później:

```rust,ignore
fn stringify_name_with_title(name: &Vec<String>) -> String {
    let mut full = name.join(" ");
    full.push_str(" Esq.");
    full
}
```

To rozwiązanie działa, ponieważ [`slice::join`] i tak kopiuje dane z `name` do łańcucha `full`.

Ogólnie rzecz biorąc, pisanie funkcji w Ruście wymaga starannego wyważenia, by prosić o *właściwy* poziom uprawnień. W tym przykładzie najbardziej idiomatyczne jest oczekiwanie wyłącznie uprawnienia do odczytu `name`.

{{#quiz ../quizzes/ch04-03-fixing-ownership-errors-sec1-idioms.toml}}

### Naprawianie niebezpiecznego programu: aliasowanie i modyfikowanie struktury danych {#fixing-an-unsafe-program-aliasing-and-mutating-a-data-structure}

Inną niebezpieczną operacją jest używanie referencji do danych na stercie, które zostają zdealokowane przez inny alias. Oto na przykład funkcja, która pobiera referencję do najdłuższego łańcucha w wektorze, a potem używa jej, modyfikując wektor:

```aquascope,permissions,stepper,boundaries,shouldFail
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {`(focus,paths:*dst)`
    let largest: &String = 
      dst.iter().max_by_key(|s| s.len()).unwrap();`(focus,paths:*dst)`
    for s in src {
        if s.len() > largest.len() {
            dst.push(s.clone());`{}`
        }
    }
}
```

> *Uwaga:* ten przykład używa [iteratorów][iterators] i [domknięć][closures] (*closures*), by zwięźle znaleźć referencję do najdłuższego łańcucha. Omówimy je w dalszych rozdziałach, a na razie przybliżymy intuicyjnie, jak działają w tym przykładzie.

*Borrow checker* odrzuca ten program, ponieważ `let largest = ..` odbiera `dst` uprawnienia @Perm{write}. Tymczasem `dst.push(..)` wymaga uprawnienia @Perm{write}. Znowu powinniśmy zapytać: **dlaczego ten program jest niebezpieczny?** Ponieważ `dst.push(..)` mogłoby zdealokować zawartość `dst`, unieważniając referencję `largest`.

Kluczem do naprawienia programu jest spostrzeżenie, że musimy skrócić czas życia `largest` tak, by nie nakładał się na `dst.push(..)`. Jedną z możliwości jest sklonowanie `largest`:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest: String = dst.iter().max_by_key(|s| s.len()).unwrap().clone();
    for s in src {
        if s.len() > largest.len() {
            dst.push(s.clone());
        }
    }
}
```

Może to jednak obniżyć wydajność z powodu alokowania i kopiowania danych łańcucha.

Inną możliwością jest wykonanie najpierw wszystkich porównań długości, a dopiero potem zmodyfikowanie `dst`:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest: &String = dst.iter().max_by_key(|s| s.len()).unwrap();
    let to_add: Vec<String> = 
        src.iter().filter(|s| s.len() > largest.len()).cloned().collect();
    dst.extend(to_add);
}
```

To jednak również obniża wydajność, tym razem z powodu alokacji wektora `to_add`.

Ostatnią możliwością jest skopiowanie samej długości `largest`, ponieważ tak naprawdę nie potrzebujemy zawartości `largest`, a jedynie jej długości. 
To rozwiązanie jest prawdopodobnie najbardziej idiomatyczne i najwydajniejsze:

```rust
fn add_big_strings(dst: &mut Vec<String>, src: &[String]) {
    let largest_len: usize = dst.iter().max_by_key(|s| s.len()).unwrap().len();
    for s in src {
        if s.len() > largest_len {
            dst.push(s.clone());
        }
    }
}
```

Wszystkie te rozwiązania łączy ta sama kluczowa idea: skrócenie czasu życia pożyczeń `dst` tak, by nie nakładały się na modyfikację `dst`.

### Naprawianie niebezpiecznego programu: kopiowanie a przenoszenie z kolekcji {#fixing-an-unsafe-program-copying-vs-moving-out-of-a-collection}

Osoby uczące się Rusta często mają kłopot z kopiowaniem danych z kolekcji, np. z wektora. Oto na przykład bezpieczny program, który kopiuje liczbę z wektora:

```aquascope,permissions,stepper,boundaries
#fn main() {
let v: Vec<i32> = vec![0, 1, 2];
let n_ref: &i32 = &v[0];`(focus,paths:*n_ref)`
let n: i32 = *n_ref;`{}`
#}
```

Operacja dereferencji (*dereference*) `*n_ref` oczekuje jedynie uprawnienia @Perm{read} (*read*, odczyt), które ścieżka `*n_ref` ma. Co się jednak stanie, jeśli zmienimy typ elementów wektora z `i32` na `String`? Okazuje się, że wtedy nie mamy już potrzebnych uprawnień:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let v: Vec<String> = 
  vec![String::from("Hello world")];
let s_ref: &String = &v[0];`(focus,paths:*s_ref)`
let s: String = *s_ref;`[]``{}`
#}
```

Pierwszy program się skompiluje, ale drugi już nie. Rust zgłasza następujący komunikat o błędzie:

```text
error[E0507]: cannot move out of `*s_ref` which is behind a shared reference
 --> test.rs:4:9
  |
4 | let s = *s_ref;
  |         ^^^^^^
  |         |
  |         move occurs because `*s_ref` has type `String`, which does not implement the `Copy` trait
```

Problem polega na tym, że łańcuch „Hello world” należy do wektora `v`. Gdy wykonujemy dereferencję `s_ref`, próbujemy przejąć własność łańcucha od wektora. Referencje są jednak wskaźnikami niebędącymi właścicielami – nie możemy przejąć własności *przez* referencję. Dlatego Rust zgłasza, że nie można przenieść wartości spod współdzielonej referencji („cannot move out of \[...\] a shared reference”).

Ale dlaczego to jest niebezpieczne? Problem możemy zilustrować, symulując odrzucony program:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let v: Vec<String> = 
  vec![String::from("Hello world")];
let s_ref: &String = &v[0];`(focus,paths:*s_ref)`
let s: String = *s_ref;`[]``{}`

// These drops are normally implicit, but we've added them for clarity.
drop(s);`[]`
drop(v);`[]`
#}
```

Dochodzi tu do **podwójnego zwolnienia** (*double free*). Po wykonaniu `let s = *s_ref` zarówno `v`, jak i `s` uważają, że są właścicielami „Hello world”. Po zwolnieniu `s` łańcuch „Hello world” zostaje zdealokowany. Potem zostaje zwolnione `v` i przy drugim zwolnieniu łańcucha dochodzi do niezdefiniowanego zachowania (*undefined behavior*).

> *Uwaga:* po wykonaniu `s = *s_ref` nie musimy nawet używać `v` ani `s`, by doprowadzić do niezdefiniowanego zachowania przez podwójne zwolnienie. Gdy tylko przeniesiemy łańcuch spod `s_ref`, niezdefiniowane zachowanie nastąpi w chwili zwolnienia elementów.

Do takiego niezdefiniowanego zachowania nie dochodzi jednak, gdy wektor zawiera elementy typu `i32`. Różnica polega na tym, że skopiowanie `String` kopiuje wskaźnik do danych na stercie. Skopiowanie `i32` – nie.
Mówiąc technicznie, Rust określa, że typ `i32` implementuje *trait* (cecha typu, zbliżona do interfejsu) `Copy`, a `String` nie implementuje `Copy` (traity omówimy w jednym z dalszych rozdziałów).

Podsumowując: **jeśli wartość nie posiada danych na stercie, można ją skopiować bez przenoszenia.** Na przykład:

* `i32` **nie** posiada danych na stercie, więc **można** go skopiować bez przenoszenia. 
* `String` **posiada** dane na stercie, więc **nie można** go skopiować bez przenoszenia.
* `&String` **nie** posiada danych na stercie, więc **można** go skopiować bez przenoszenia.

> *Uwaga:* jednym z wyjątków od tej reguły są mutowalne referencje. Na przykład `&mut i32` nie jest typem kopiowalnym. Jeśli więc napiszesz coś takiego:
> ```rust,ignore
> let mut n = 0;
> let a = &mut n;
> let b = a;
> ```
> to po przypisaniu do `b` nie można już używać `a`. Zapobiega to jednoczesnemu używaniu dwóch mutowalnych referencji do tych samych danych.

Skoro mamy wektor typów, które nie są `Copy`, jak `String`, to jak bezpiecznie uzyskać dostęp do jego elementu? Oto kilka bezpiecznych sposobów. Po pierwsze, możesz nie przejmować własności łańcucha i użyć po prostu niemutowalnej referencji:

```rust,ignore
# fn main() {
let v: Vec<String> = vec![String::from("Hello world")];
let s_ref: &String = &v[0];
println!("{s_ref}!");
# }
```

Po drugie, możesz sklonować dane, jeśli chcesz uzyskać własność łańcucha, nie ruszając wektora:

```rust,ignore
# fn main() {
let v: Vec<String> = vec![String::from("Hello world")];
let mut s: String = v[0].clone();
s.push('!');
println!("{s}");
# }
```

Wreszcie możesz użyć metody takiej jak [`Vec::remove`], by przenieść łańcuch z wektora:

```rust,ignore
# fn main() {
let mut v: Vec<String> = vec![String::from("Hello world")];
let mut s: String = v.remove(0);
s.push('!');
println!("{s}");
assert!(v.len() == 0);
# }
```


### Naprawianie bezpiecznego programu: modyfikowanie różnych pól krotki {#fixing-a-safe-program-mutating-different-tuple-fields}

Powyższe przykłady to przypadki, w których program jest niebezpieczny. Rust może jednak odrzucać także programy bezpieczne. Częstym problemem jest to, że Rust stara się śledzić uprawnienia bardzo szczegółowo, ale czasem może potraktować dwa różne miejsca (*places*) jak jedno i to samo miejsce. 
 
Spójrzmy najpierw na przykład szczegółowego śledzenia uprawnień, który przechodzi przez *borrow checker*. Ten program pokazuje, że można pożyczyć jedno pole krotki (*tuple*) i zapisywać do innego pola tej samej krotki:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut name = (
    String::from("Ferris"), 
    String::from("Rustacean")
);`(focus,paths:name)`
let first = &name.0;`(focus,paths:name)`
name.1.push_str(", Esq.");`{}`
println!("{first} {}", name.1);
#}
```

Instrukcja (*statement*) `let first = &name.0` pożycza `name.0`. To pożyczenie odbiera `name.0` uprawnienia @Perm{write}@Perm{own} (*own*, własność). Odbiera też uprawnienia @Perm{write}@Perm{own} zmiennej `name`. (Nie można by na przykład przekazać `name` do funkcji, która przyjmuje wartość typu `(String, String)`). Jednak `name.1` nadal ma uprawnienie @Perm{write}, więc `name.1.push_str(...)` jest poprawną operacją.

Rust może jednak stracić rozeznanie, które dokładnie miejsca są pożyczone. Załóżmy na przykład, że wydzielamy wyrażenie (*expression*) `&name.0` do funkcji `get_first`. Zwróć uwagę, że po wywołaniu `get_first(&name)` Rust odbiera teraz uprawnienie @Perm{write} również `name.1`:

```aquascope,permissions,stepper,boundaries,shouldFail
fn get_first(name: &(String, String)) -> &String {
    &name.0
}

fn main() {
    let mut name = (
        String::from("Ferris"), 
        String::from("Rustacean")
    );
    let first = get_first(&name);`(focus,paths:name)`
    name.1.push_str(", Esq.");`{}`
    println!("{first} {}", name.1);
}
```

Teraz nie możemy wykonać `name.1.push_str(..)`! Rust zgłosi taki błąd:

```text
error[E0502]: cannot borrow `name.1` as mutable because it is also borrowed as immutable
  --> test.rs:11:5
   |
10 |     let first = get_first(&name);
   |                           ----- immutable borrow occurs here
11 |     name.1.push_str(", Esq.");
   |     ^^^^^^^^^^^^^^^^^^^^^^^^^ mutable borrow occurs here
12 |     println!("{first} {}", name.1);
   |                ----- immutable borrow later used here
```

To dziwne, bo przed zmianą program był bezpieczny. Nasza zmiana w istocie nie wpływa na zachowanie programu w czasie działania. Dlaczego więc ma znaczenie, że umieściliśmy `&name.0` w funkcji?

Problem polega na tym, że decydując, co pożycza `get_first(&name)`, Rust nie zagląda do implementacji `get_first`. Patrzy tylko na sygnaturę typu, która mówi jedynie, że „jakiś `String` z danych wejściowych zostaje pożyczony”. Rust zachowawczo uznaje więc, że pożyczone są zarówno `name.0`, jak i `name.1`, i odbiera obu uprawnienia do zapisu i własności. 

Pamiętaj, że kluczowe jest to, iż **powyższy program jest bezpieczny.** Nie ma w nim niezdefiniowanego zachowania! Przyszła wersja Rusta może być na tyle sprytna, by go skompilować, ale dziś zostaje odrzucony. Jak więc obejść dziś *borrow checker*? Jedną z możliwości jest wstawienie wyrażenia `&name.0` bezpośrednio w miejscu użycia, jak w pierwotnym programie. Inną jest odłożenie sprawdzania pożyczeń do czasu działania za pomocą [komórek][cells] (*cells*), które omówimy w dalszych rozdziałach.

### Naprawianie bezpiecznego programu: modyfikowanie różnych elementów tablicy {#fixing-a-safe-program-mutating-different-array-elements}

Podobny problem pojawia się, gdy pożyczamy elementy tablicy. Zobacz na przykład, jakie miejsca zostają pożyczone, gdy tworzymy mutowalną referencję do tablicy:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1];`(focus,paths:a[_])`
*x += 1;`(focus,paths:a[_])`
println!("{a:?}");
#}
```

*Borrow checker* Rusta nie ma osobnych miejsc dla `a[0]`, `a[1]` itd. Używa jednego miejsca `a[_]`, które reprezentuje *wszystkie* indeksy `a`. Rust robi tak, ponieważ nie zawsze potrafi ustalić wartość indeksu. Wyobraź sobie na przykład bardziej złożony scenariusz:

```rust,ignore
let idx = a_complex_function();
let x = &mut a[idx];
```

Jaka jest wartość `idx`? Rust nie będzie zgadywał, więc zakłada, że `idx` może być czymkolwiek. Załóżmy na przykład, że próbujemy odczytać jeden indeks tablicy, jednocześnie zapisując do innego:

```aquascope,permissions,boundaries,stepper,shouldFail
#fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1];`(focus,paths:a[_])`
let y = &a[2];`{}`
*x += *y;
#}
```

Rust odrzuci jednak ten program, ponieważ `a` oddało swoje uprawnienie do odczytu zmiennej `x`. Komunikat o błędzie kompilatora mówi to samo:

```text
error[E0502]: cannot borrow `a[_]` as immutable because it is also borrowed as mutable
 --> test.rs:4:9
  |
3 | let x = &mut a[1];
  |         --------- mutable borrow occurs here
4 | let y = &a[2];
  |         ^^^^^ immutable borrow occurs here
5 | *x += *y;
  | -------- mutable borrow later used here
```

<!-- However, Rust will reject this program because `a` gave its read permission to `x`. -->


Ponownie: **ten program jest bezpieczny.** W takich przypadkach Rust często udostępnia w bibliotece standardowej funkcję, która pozwala obejść *borrow checker*. Moglibyśmy na przykład użyć [`slice::split_at_mut`][split_at_mut]:

```rust,ignore
# fn main() {
let mut a = [0, 1, 2, 3];
let (a_l, a_r) = a.split_at_mut(2);
let x = &mut a_l[1];
let y = &a_r[0];
*x += *y;
# }
```

Możesz się zastanawiać, jak w takim razie zaimplementowano `split_at_mut`. W niektórych bibliotekach Rusta, zwłaszcza w typach podstawowych, takich jak `Vec` czy `slice`, często znajdziesz **bloki `unsafe`**. Bloki `unsafe` pozwalają używać „surowych” wskaźników (*raw pointers*), których bezpieczeństwa *borrow checker* nie sprawdza. Moglibyśmy na przykład wykonać nasze zadanie w bloku unsafe:

```rust,ignore
# fn main() {
let mut a = [0, 1, 2, 3];
let x = &mut a[1] as *mut i32;
let y = &a[2] as *const i32;
unsafe { *x += *y; } // DO NOT DO THIS unless you know what you're doing!
# }
```

Niebezpieczny kod bywa czasem niezbędny, by obejść ograniczenia *borrow checkera*. Ogólna strategia wygląda tak: jeśli *borrow checker* odrzuca program, który twoim zdaniem jest w rzeczywistości bezpieczny, poszukaj funkcji z biblioteki standardowej (takich jak `split_at_mut`), które zawierają bloki `unsafe` i rozwiązują twój problem. Niebezpieczny kod omówimy dokładniej w [rozdziale 20][unsafe]. Na razie wystarczy wiedzieć, że niebezpieczny kod to sposób, w jaki Rust implementuje pewne wzorce, które inaczej byłyby niemożliwe.

{{#quiz ../quizzes/ch04-03-fixing-ownership-errors-sec2-safety.toml}}

### Podsumowanie {#summary}

Naprawiając błąd własności, zadaj sobie pytanie: czy mój program jest naprawdę niebezpieczny? Jeśli tak, musisz zrozumieć podstawową przyczynę tego niebezpieczeństwa. Jeśli nie, musisz zrozumieć ograniczenia *borrow checkera*, aby je obejść.

[rc]: https://doc.rust-lang.org/std/rc/index.html
[cells]: https://doc.rust-lang.org/std/cell/index.html
[split_at_mut]: https://doc.rust-lang.org/std/primitive.slice.html#method.split_at_mut
[unsafe]: ch19-01-unsafe-rust.html
[`Vec::remove`]: https://doc.rust-lang.org/std/vec/struct.Vec.html#method.remove
[`slice::join`]: https://doc.rust-lang.org/std/primitive.slice.html#method.join
[iterators]: ch13-02-iterators.html
[closures]: ch13-01-closures.html

[^safe-subset]: Ta gwarancja dotyczy programów napisanych w „bezpiecznym podzbiorze” Rusta. Jeśli używasz kodu `unsafe` albo wywołujesz niebezpieczne komponenty (np. bibliotekę w C), musisz szczególnie uważać, by uniknąć niezdefiniowanego zachowania.

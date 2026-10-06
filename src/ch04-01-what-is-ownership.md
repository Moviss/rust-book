## Czym jest własność? {#what-is-ownership}

Własność (*ownership*) to dyscyplina, która zapewnia **bezpieczeństwo** programów w Ruście. Żeby zrozumieć własność, musimy najpierw zrozumieć, co sprawia, że program w Ruście jest bezpieczny (albo niebezpieczny).

### Bezpieczeństwo to brak niezdefiniowanego zachowania {#safety-is-the-absence-of-undefined-behavior}

Zacznijmy od przykładu. Ten program można bezpiecznie wykonać:

```rust
fn read(y: bool) {
    if y {
        println!("y is true!");
    }
}

fn main() {
    let x = true;
    read(x);
}
```

Możemy sprawić, że jego wykonanie stanie się niebezpieczne, jeśli przeniesiemy wywołanie `read` przed definicję `x`:

```rust,ignore,does_not_compile
fn read(y: bool) {
    if y {
        println!("y is true!");
    }
}

fn main() {
    read(x); // oh no! x isn't defined!
    let x = true;
}
```

> *Uwaga*: w tym rozdziale pokażemy wiele przykładów kodu, które się nie kompilują. Jeśli nie masz pewności, czy dany program powinien się skompilować, szukaj kraba ze znakiem zapytania.

Drugi program jest niebezpieczny, ponieważ `read(x)` oczekuje, że `x` będzie mieć wartość typu `bool`, a `x` nie ma jeszcze żadnej wartości.

Gdyby taki program wykonywał interpreter, odczyt `x` przed jego zdefiniowaniem zgłosiłby wyjątek, na przykład [`NameError`] w Pythonie albo [`ReferenceError`] w JavaScripcie. Wyjątki mają jednak swoją cenę. Za każdym razem, gdy interpretowany program odczytuje zmienną, interpreter musi sprawdzić, czy ta zmienna jest zdefiniowana.

Celem Rusta jest kompilowanie programów do wydajnych plików binarnych, które wymagają jak najmniej sprawdzeń w czasie działania. Dlatego Rust nie sprawdza *w czasie działania* (*runtime*), czy zmienna została zdefiniowana przed użyciem. Sprawdza to *w czasie kompilacji* (*compile-time*). Jeśli spróbujesz skompilować niebezpieczny program, dostaniesz taki błąd:

```text
error[E0425]: cannot find value `x` in this scope
 --> src/main.rs:8:10
  |
8 |     read(x); // oh no! x isn't defined!
  |          ^ not found in this scope
```

Pewnie intuicyjnie czujesz, że to dobrze, iż Rust pilnuje, by zmienne były zdefiniowane przed użyciem. Ale dlaczego? Żeby uzasadnić tę regułę, musimy zadać pytanie: **co by się stało, gdyby Rust pozwolił skompilować odrzucony program?**

Zobaczmy najpierw, jak kompiluje się i wykonuje bezpieczny program. Na komputerze z procesorem o architekturze [x86](https://en.wikipedia.org/wiki/X86) Rust generuje dla funkcji `main` w bezpiecznym programie następujący kod asemblera ([pełny kod asemblera znajdziesz tutaj](https://rust.godbolt.org/z/xnT1fzsqv)):

```x86asm
main:
    ; ...
    mov     edi, 1
    call    read
    ; ...
```

> _Uwaga_: jeśli nie znasz asemblera, nic nie szkodzi! W tym podrozdziale jest kilka przykładów asemblera tylko po to, by pokazać, jak Rust naprawdę działa pod spodem. Do zrozumienia Rusta zwykle nie musisz znać asemblera.

Ten kod asemblera:

- przenosi liczbę 1, reprezentującą `true`, do „rejestru” (czegoś w rodzaju zmiennej asemblera) o nazwie `edi`;
- wywołuje funkcję `read`, która oczekuje, że jej pierwszy argument `y` będzie w rejestrze `edi`.

Gdyby niebezpieczną funkcję dało się skompilować, jej kod asemblera mógłby wyglądać tak:

```x86asm
main:
    ; ...
    call    read
    mov     edi, 1    ; mov is after call
    ; ...
```

Ten program jest niebezpieczny, ponieważ `read` oczekuje, że `edi` będzie wartością logiczną, czyli liczbą `0` albo `1`. Tymczasem w `edi` może być cokolwiek: `2`, `100`, `0x1337BEEF`. Gdy `read` zechce do czegokolwiek użyć swojego argumentu `y`, natychmiast wywoła _**NIEZDEFINIOWANE ZACHOWANIE!**_ (*undefined behavior*)

Rust nie określa, co się stanie, jeśli spróbujesz wykonać `if y { .. }`, gdy `y` nie jest ani `true`, ani `false`. To *zachowanie*, czyli to, co dzieje się po wykonaniu instrukcji, jest *niezdefiniowane*. Coś się wydarzy, na przykład:

- kod wykona się bez awarii i nikt nie zauważy problemu;
- kod natychmiast się wysypie z powodu [błędu segmentacji](https://en.wikipedia.org/wiki/Segmentation_fault) albo innego błędu systemu operacyjnego;
- kod będzie działał bez awarii, dopóki ktoś o złych zamiarach nie przygotuje odpowiednich danych wejściowych, żeby usunąć twoją produkcyjną bazę danych, nadpisać kopie zapasowe i ukraść ci pieniądze na obiad.

**Podstawowym celem Rusta jest zapewnienie, że twoje programy nigdy nie mają niezdefiniowanego zachowania.** Właśnie to oznacza „bezpieczeństwo”. Niezdefiniowane zachowanie jest szczególnie groźne w programach niskopoziomowych z bezpośrednim dostępem do pamięci. Około [70% zgłaszanych luk bezpieczeństwa](https://msrc.microsoft.com/blog/2019/07/a-proactive-approach-to-more-secure-code/) w systemach niskopoziomowych wynika z uszkodzenia pamięci, które jest jedną z postaci niezdefiniowanego zachowania.

Drugim celem Rusta jest zapobieganie niezdefiniowanemu zachowaniu _w czasie kompilacji_, a nie _w czasie działania_. Ten cel ma dwa uzasadnienia:

1. Wyłapanie błędów w czasie kompilacji oznacza, że nie trafią one na produkcję, co zwiększa niezawodność twojego oprogramowania.
2. Wyłapanie błędów w czasie kompilacji oznacza mniej sprawdzeń tych błędów w czasie działania, co zwiększa wydajność twojego oprogramowania.

Rust nie zapobiegnie wszystkim błędom. Jeśli aplikacja udostępnia publiczny endpoint `/delete-production-database` bez uwierzytelniania, napastnik nie potrzebuje podejrzanej instrukcji if, żeby usunąć bazę danych. Mimo to zabezpieczenia Rusta najpewniej sprawiają, że programy są bezpieczniejsze niż w języku z mniejszą liczbą zabezpieczeń, co stwierdził na przykład [zespół Androida w Google](https://security.googleblog.com/2022/12/memory-safe-languages-in-android-13.html).

### Własność jako dyscyplina bezpieczeństwa pamięci {#ownership-as-a-discipline-for-memory-safety}

Skoro bezpieczeństwo to brak niezdefiniowanego zachowania, a własność służy bezpieczeństwu, musimy rozumieć własność przez pryzmat niezdefiniowanych zachowań, którym zapobiega. Dokumentacja Rust Reference zawiera długą listę [„zachowań uznawanych za niezdefiniowane”](https://doc.rust-lang.org/reference/behavior-considered-undefined.html). Na razie skupimy się na jednej kategorii: operacjach na pamięci.

Pamięć to przestrzeń, w której przechowywane są dane podczas wykonywania programu. O pamięci można myśleć na wiele sposobów:

- Jeśli nie znasz programowania systemowego, możesz myśleć o pamięci wysokopoziomowo, np. „pamięć to RAM w moim komputerze” albo „pamięć to coś, czego zaczyna brakować, gdy wczytam za dużo danych”.
- Jeśli znasz programowanie systemowe, możesz myśleć o pamięci niskopoziomowo, np. „pamięć to tablica bajtów” albo „pamięć to wskaźniki, które dostaję z `malloc`”.

Oba te modele pamięci są _poprawne_, ale nie są _przydatne_ do myślenia o tym, jak działa Rust. Model wysokopoziomowy jest zbyt abstrakcyjny, by wyjaśnić działanie Rusta – trzeba na przykład rozumieć pojęcie wskaźnika. Model niskopoziomowy jest zbyt konkretny, by wyjaśnić działanie Rusta – Rust nie pozwala na przykład interpretować pamięci jako tablicy bajtów.

Rust proponuje określony sposób myślenia o pamięci. Własność to dyscyplina bezpiecznego korzystania z pamięci w ramach tego sposobu myślenia. W dalszej części rozdziału wyjaśnimy model pamięci Rusta.

### Zmienne żyją na stosie {#variables-live-in-the-stack}

Oto program podobny do tego z podrozdziału 3.3, który definiuje liczbę `n` i wywołuje na `n` funkcję `plus_one`. Pod programem jest nowy rodzaj diagramu. Pokazuje on zawartość pamięci podczas wykonywania programu w trzech zaznaczonych punktach.

```aquascope,interpreter,horizontal
fn main() {
    let n = 5;`[]`
    let y = plus_one(n);`[]`
    println!("The value of y is: {y}");
}

fn plus_one(x: i32) -> i32 {
    `[]`x + 1
}
```

Zmienne żyją w **ramkach** (*frames*). Ramka to odwzorowanie zmiennych na wartości w obrębie jednego zasięgu (*scope*), takiego jak funkcja. Na przykład:

- ramka `main` w punkcie L1 zawiera `n = 5`;
- ramka `plus_one` w punkcie L2 zawiera `x = 5`;
- ramka `main` w punkcie L3 zawiera `n = 5; y = 6`.

Ramki są zorganizowane w **stos** (*stack*) aktualnie wywołanych funkcji. Na przykład w punkcie L2 ramka `main` leży nad ramką wywołanej funkcji `plus_one`. Gdy funkcja się zakończy, Rust dealokuje jej ramkę. (Dealokację nazywa się też **zwalnianiem** (*freeing* lub *dropping*) – używamy tych określeń zamiennie.) Ten ciąg ramek nazywa się stosem, ponieważ ostatnio dodana ramka zawsze jest zwalniana jako następna.

> _Uwaga:_ ten model pamięci nie opisuje w pełni, jak naprawdę działa Rust! Jak widzieliśmy wcześniej w kodzie asemblera, kompilator Rusta może umieścić `n` albo `x` w rejestrze, a nie w ramce stosu. To rozróżnienie jest jednak szczegółem implementacji. Nie powinno zmieniać twojego rozumienia bezpieczeństwa w Ruście, więc możemy skupić się na prostszym przypadku, w którym zmienne są tylko w ramkach.

Gdy wyrażenie (*expression*) odczytuje zmienną, jej wartość jest kopiowana z jej miejsca w ramce stosu. Na przykład, jeśli uruchomimy ten program:

```aquascope,interpreter,horizontal
#fn main() {
let a = 5;`[]`
let mut b = a;`[]`
b += 1;`[]`
#}
```

Wartość `a` zostaje skopiowana do `b`, a sama zmienna `a` pozostaje niezmieniona, nawet po zmianie `b`.

### Boxy żyją na stercie {#boxes-live-in-the-heap}

Kopiowanie danych może jednak zajmować dużo pamięci. Oto na przykład nieco inny program. Kopiuje on tablicę o milionie elementów:

```aquascope,interpreter
#fn main() {
let a = [0; 1_000_000];`[]`
let b = a;`[]`
#}
```

Zauważ, że skopiowanie `a` do `b` sprawia, że ramka `main` zawiera 2 miliony elementów.

Żeby przekazać dostęp do danych bez ich kopiowania, Rust używa **wskaźników**. Wskaźnik to wartość, która opisuje miejsce w pamięci. Wartość, na którą wskaźnik wskazuje, nazywamy **wartością wskazywaną** (*pointee*). Jednym z typowych sposobów utworzenia wskaźnika jest zaalokowanie pamięci na **stercie** (*heap*). Sterta to oddzielny obszar pamięci, w którym dane mogą żyć dowolnie długo. Dane na stercie nie są związane z żadną konkretną ramką stosu. Do umieszczania danych na stercie Rust udostępnia konstrukcję o nazwie [`Box`](https://doc.rust-lang.org/std/boxed/index.html), czyli *box* (wskaźnik na dane umieszczone na stercie). Możemy na przykład opakować tablicę o milionie elementów w `Box::new` w ten sposób:

```aquascope,interpreter
#fn main() {
let a = Box::new([0; 1_000_000]);`[]`
let b = a;`[]`
#}
```

Zauważ, że teraz w każdej chwili istnieje tylko jedna tablica. W punkcie L1 wartością `a` jest wskaźnik (przedstawiony jako kropka ze strzałką) na tablicę na stercie. Instrukcja (*statement*) `let b = a` kopiuje wskaźnik z `a` do `b`, ale danych, na które wskazuje, nie kopiuje. Zwróć uwagę, że `a` jest teraz wyszarzone, ponieważ zostało *przeniesione* – za chwilę zobaczymy, co oznacza przeniesienie (*move*).

{{#quiz ../quizzes/ch04-01-ownership-sec1-stackheap.toml}}

### Rust nie pozwala ręcznie zarządzać pamięcią {#rust-does-not-permit-manual-memory-management}

Zarządzanie pamięcią to proces alokowania i dealokowania pamięci. Innymi słowy, to proces znajdowania nieużywanej pamięci i późniejszego oddawania jej, gdy przestaje być potrzebna. Ramkami stosu Rust zarządza automatycznie. Gdy funkcja zostaje wywołana, Rust alokuje dla niej ramkę stosu. Gdy wywołanie się kończy, Rust dealokuje tę ramkę.

Jak widzieliśmy wyżej, dane na stercie są alokowane przy wywołaniu `Box::new(..)`. Ale kiedy są dealokowane? Wyobraź sobie, że Rust ma funkcję `free()`, która zwalnia alokację na stercie, i że programista może wywołać `free`, kiedy tylko zechce. Takie „ręczne” zarządzanie pamięcią łatwo prowadzi do błędów. Moglibyśmy na przykład odczytać wskaźnik na zwolnioną pamięć:

```aquascope,interpreter,shouldFail
#fn free<T>(_t: T) {}
#fn main() {
let b = Box::new([0; 100]);`[]`
free(b);`[]`
assert!(b[0] == 0);`[]`
#}
```

> *Uwaga:* możesz się zastanawiać, jak wykonujemy ten program w Ruście, skoro się nie kompiluje. W celach dydaktycznych używamy [specjalnych narzędzi](https://github.com/cognitive-engineering-lab/aquascope), które symulują Rusta tak, jakby *borrow checker* (mechanizm sprawdzania pożyczeń) był wyłączony. Dzięki temu możemy odpowiadać na pytania typu „co by było, gdyby”, na przykład: co by było, gdyby Rust pozwolił skompilować ten niebezpieczny program?

Alokujemy tu tablicę na stercie. Potem wywołujemy `free(b)`, które dealokuje pamięć `b` na stercie. Wartość `b` jest więc wskaźnikiem na nieprawidłową pamięć, co przedstawiamy ikoną „⦻”. Niezdefiniowane zachowanie jeszcze nie wystąpiło! W punkcie L2 program jest nadal bezpieczny. Sam nieprawidłowy wskaźnik niekoniecznie jest problemem.

Niezdefiniowane zachowanie pojawia się, gdy próbujemy *użyć* wskaźnika, odczytując `b[0]`. To byłaby próba dostępu do nieprawidłowej pamięci, która mogłaby spowodować awarię programu. Albo, co gorsza, program mógłby się nie wysypać i zwrócić dowolne dane. Dlatego ten program jest **niebezpieczny**.

Rust nie pozwala programom ręcznie dealokować pamięci. Ta zasada pozwala uniknąć niezdefiniowanych zachowań takich jak pokazane wyżej.

### Właściciel boxa zarządza dealokacją {#a-boxs-owner-manages-deallocation}

Zamiast tego Rust _automatycznie_ zwalnia pamięć boxa na stercie. Oto _prawie_ poprawny opis zasady, według której Rust zwalnia boxy:

> **Zasada dealokacji boxa (prawie poprawna):** jeśli zmienna jest związana z boxem, to gdy Rust dealokuje ramkę tej zmiennej, dealokuje też pamięć boxa na stercie.

Prześledźmy na przykład program, który alokuje i zwalnia box:

```aquascope,interpreter,horizontal
fn main() {
    let a_num = 4;`[]`
    make_and_drop();`[]`
}

fn make_and_drop() {
    let a_box = Box::new(5);`[]`
}
```

W punkcie L1, przed wywołaniem `make_and_drop`, pamięć składa się tylko z ramki stosu `main`. Następnie w punkcie L2, w trakcie wywołania `make_and_drop`, `a_box` wskazuje na `5` na stercie. Gdy `make_and_drop` się zakończy, Rust dealokuje jej ramkę stosu. `make_and_drop` zawiera zmienną `a_box`, więc Rust dealokuje też dane na stercie w `a_box`. Dlatego w punkcie L3 sterta jest pusta.

Zarządzanie pamięcią boxa na stercie zadziałało poprawnie. Ale co, jeśli nadużyjemy tego systemu? Wróćmy do wcześniejszego przykładu: co się stanie, gdy zwiążemy z boxem dwie zmienne?

```rust,ignore
# fn main() {
let a = Box::new([0; 1_000_000]);
let b = a;
# }
```

Tablica w boxie jest teraz związana zarówno z `a`, jak i z `b`. Według naszej „prawie poprawnej” zasady Rust próbowałby zwolnić pamięć boxa na stercie *dwukrotnie* – raz za każdą ze zmiennych. To również jest niezdefiniowane zachowanie!

Żeby uniknąć takiej sytuacji, dochodzimy wreszcie do własności. Gdy `a` zostaje związane z `Box::new([0; 1_000_000])`, mówimy, że `a` **jest właścicielem** boxa. Instrukcja `let b = a` **przenosi** własność boxa z `a` do `b`. Mając te pojęcia, zasadę zwalniania boxów w Ruście można opisać dokładniej:

> **Zasada dealokacji boxa (w pełni poprawna):** jeśli zmienna jest właścicielem boxa, to gdy Rust dealokuje ramkę tej zmiennej, dealokuje też pamięć boxa na stercie.

W powyższym przykładzie właścicielem tablicy w boxie jest `b`. Dlatego gdy zasięg się kończy, Rust dealokuje box tylko raz – w imieniu `b`, a nie `a`.


### Kolekcje używają boxów {#collections-use-boxes}

Boxów używają struktury danych Rusta[^boxed-data-structures], takie jak [`Vec`](https://doc.rust-lang.org/std/vec/struct.Vec.html), [`String`](https://doc.rust-lang.org/std/string/struct.String.html) i [`HashMap`](https://doc.rust-lang.org/std/collections/struct.HashMap.html), żeby przechowywać zmienną liczbę elementów. Oto na przykład program, który tworzy, przenosi i modyfikuje łańcuch znaków (*string*):

```aquascope,interpreter,horizontal
fn main() {
    let first = String::from("Ferris");`[]`
    let full = add_suffix(first);`[]`
    println!("{full}");
}

fn add_suffix(mut name: String) -> String {
    `[]`name.push_str(" Jr.");`[]`
    name
}
```

Ten program jest bardziej złożony, więc prześledź uważnie każdy krok:

1. W punkcie L1 łańcuch „Ferris” został zaalokowany na stercie. Jego właścicielem jest `first`.
2. W punkcie L2 została wywołana funkcja `add_suffix(first)`. Przenosi to własność łańcucha z `first` do `name`. Dane łańcucha nie są kopiowane – kopiowany jest wskaźnik na te dane.
3. W punkcie L3 funkcja `name.push_str(" Jr.")` zmienia rozmiar alokacji łańcucha na stercie. Robi przy tym trzy rzeczy. Po pierwsze tworzy nową, większą alokację. Po drugie zapisuje w niej „Ferris Jr.”. Po trzecie zwalnia pierwotną pamięć na stercie. `first` wskazuje teraz na zdealokowaną pamięć.
4. W punkcie L4 ramki `add_suffix` już nie ma. Ta funkcja zwróciła `name`, przekazując własność łańcucha do `full`.


### Zmiennych nie można używać po przeniesieniu {#variables-cannot-be-used-after-being-moved}

Program z łańcuchem pomaga zilustrować kluczową zasadę bezpieczeństwa związaną z własnością. Wyobraź sobie, że `first` zostało użyte w `main` po wywołaniu `add_suffix`. Możemy zasymulować taki program i zobaczyć, do jakiego niezdefiniowanego zachowania prowadzi:

```aquascope,interpreter,shouldFail
fn main() {
    let first = String::from("Ferris");
    let full = add_suffix(first);
    println!("{full}, originally {first}");`[]` // first is now used here
}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    name
}
```

Po wywołaniu `add_suffix` zmienna `first` wskazuje na zdealokowaną pamięć. Odczytanie `first` w `println!` byłoby więc naruszeniem bezpieczeństwa pamięci (niezdefiniowanym zachowaniem). Pamiętaj: problemem nie jest to, że `first` wskazuje na zdealokowaną pamięć. Problemem jest to, że próbowaliśmy *użyć* `first` po tym, jak stało się nieprawidłowe.

Na szczęście Rust odmówi skompilowania tego programu i zgłosi następujący błąd:

```text
error[E0382]: borrow of moved value: `first`
 --> test.rs:4:35
  |
2 |     let first = String::from("Ferris");
  |         ----- move occurs because `first` has type `String`, which does not implement the `Copy` trait
3 |     let full = add_suffix(first);
  |                           ----- value moved here
4 |     println!("{full}, originally {first}"); // first is now used here
  |                                   ^^^^^ value borrowed here after move
```

Przejdźmy przez kolejne części tego błędu. Rust mówi, że `first` zostaje przeniesione, gdy w wierszu 3 wywołujemy `add_suffix(first)`. Błąd wyjaśnia, że `first` jest przenoszone, ponieważ ma typ `String`, który nie implementuje `Copy`. Wkrótce omówimy `Copy` – w skrócie: tego błędu by nie było, gdyby zamiast `String` użyć `i32`. Na koniec błąd mówi, że używamy `first` po przeniesieniu (jest „pożyczane” – pożyczanie (*borrowing*) omówimy w następnym podrozdziale).

Jeśli więc przeniesiesz zmienną, Rust nie pozwoli ci później jej użyć. Ogólniej mówiąc, kompilator egzekwuje następującą zasadę:

> **Zasada przeniesionych danych na stercie:** jeśli zmienna `x` przenosi własność danych na stercie do innej zmiennej `y`, to po przeniesieniu nie można używać `x`.

Teraz zaczynasz pewnie dostrzegać związek między własnością, przeniesieniami i bezpieczeństwem. Przenoszenie własności danych na stercie zapobiega niezdefiniowanemu zachowaniu wynikającemu z odczytu zdealokowanej pamięci.

### Klonowanie pozwala uniknąć przeniesień {#cloning-avoids-moves}

Jednym ze sposobów uniknięcia przeniesienia danych jest ich *sklonowanie* metodą `.clone()`. Możemy na przykład naprawić problem z bezpieczeństwem w poprzednim programie za pomocą klonu:

```aquascope,interpreter
fn main() {
    let first = String::from("Ferris");
    let first_clone = first.clone();`[]`
    let full = add_suffix(first_clone);`[]`
    println!("{full}, originally {first}");
}

fn add_suffix(mut name: String) -> String {
    name.push_str(" Jr.");
    name
}
```

Zauważ, że w punkcie L1 `first_clone` nie skopiowało „płytko” wskaźnika z `first`, lecz skopiowało „głęboko” dane łańcucha do nowej alokacji na stercie. Dlatego w punkcie L2, choć `first_clone` zostało przeniesione i unieważnione przez `add_suffix`, pierwotna zmienna `first` pozostaje bez zmian. Można dalej bezpiecznie używać `first`.

{{#quiz ../quizzes/ch04-01-ownership-sec2-moves.toml}}

### Podsumowanie {#summary}

Własność to przede wszystkim dyscyplina zarządzania stertą:[^pointer-management]

- Wszystkie dane na stercie muszą mieć jako właściciela dokładnie jedną zmienną.
- Rust dealokuje dane na stercie, gdy ich właściciel wychodzi poza zasięg.
- Własność można przekazać przez przeniesienia, które następują przy przypisaniach i wywołaniach funkcji.
- Do danych na stercie można się dostać tylko przez ich bieżącego właściciela, a nie przez poprzedniego.

Podkreślaliśmy nie tylko, _jak_ działają zabezpieczenia Rusta, ale też _dlaczego_ zapobiegają niezdefiniowanemu zachowaniu. Gdy dostajesz komunikat o błędzie od kompilatora Rusta, łatwo się zirytować, jeśli nie rozumiesz, na co Rust się skarży. Te podstawy koncepcyjne powinny pomóc ci w interpretowaniu komunikatów o błędach Rusta. Powinny też pomóc ci projektować API bardziej w duchu Rusta.

[^boxed-data-structures]: Te struktury danych nie używają dosłownie typu `Box`. Na przykład `String` jest zaimplementowany za pomocą `Vec`, a `Vec` za pomocą [`RawVec`](https://doc.rust-lang.org/nomicon/vec/vec-raw.html), a nie `Box`. Typy takie jak `RawVec` przypominają jednak boxy: są właścicielami pamięci na stercie.

[^pointer-management]: W innym sensie własność jest dyscypliną zarządzania *wskaźnikami*. Nie opisaliśmy jednak jeszcze, jak tworzyć wskaźniki do miejsc innych niż sterta. Dojdziemy do tego w następnym podrozdziale.

[`NameError`]: https://docs.python.org/3/library/exceptions.html#NameError
[`ReferenceError`]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/ReferenceError

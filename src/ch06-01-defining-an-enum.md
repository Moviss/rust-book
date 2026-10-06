## Definiowanie enuma {#defining-an-enum}

Struktury (*struct*) pozwalają grupować powiązane pola i dane, jak `Rectangle`
z polami `width` i `height`, a enumy (*enum*, typy wyliczeniowe) pozwalają
powiedzieć, że wartość jest jedną z możliwego zbioru wartości. Na przykład
możemy chcieć wyrazić, że `Rectangle` to jeden z możliwych kształtów, do których
należą też `Circle` i `Triangle`. Rust pozwala zapisać te możliwości jako enum.

Przyjrzyjmy się sytuacji, którą moglibyśmy chcieć wyrazić w kodzie, i zobaczmy,
dlaczego enumy są w niej przydatne i lepiej się nadają niż struktury. Załóżmy,
że musimy pracować z adresami IP. Obecnie używa się dwóch głównych standardów
adresów IP: wersji czwartej i wersji szóstej. Ponieważ to jedyne rodzaje adresów
IP, z jakimi zetknie się nasz program, możemy _wyliczyć_ wszystkie możliwe
warianty – i właśnie od tego pochodzi nazwa typu wyliczeniowego.

Każdy adres IP może być adresem w wersji czwartej albo szóstej, ale nie obiema
naraz. Ta właściwość adresów IP sprawia, że enum jest odpowiednią strukturą
danych, bo wartość enuma może być tylko jednym z jego wariantów. Adresy w wersji
czwartej i szóstej to wciąż w gruncie rzeczy adresy IP, więc kod obsługujący
sytuacje dotyczące dowolnego rodzaju adresu IP powinien traktować je jako ten
sam typ.

Możemy wyrazić tę koncepcję w kodzie, definiując enum `IpAddrKind` i wymieniając
możliwe rodzaje adresu IP: `V4` i `V6`. To są warianty tego enuma:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:def}}
```

`IpAddrKind` jest teraz własnym typem danych, którego możemy używać w innych
miejscach kodu.

### Wartości enumów {#enum-values}

Instancje każdego z dwóch wariantów `IpAddrKind` możemy utworzyć tak:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:instance}}
```

Zwróć uwagę, że warianty enuma należą do przestrzeni nazw (*namespace*) jego
identyfikatora i oddzielamy je od niego podwójnym dwukropkiem. To przydatne, bo
teraz obie wartości, `IpAddrKind::V4` i `IpAddrKind::V6`, mają ten sam typ:
`IpAddrKind`. Możemy więc na przykład zdefiniować funkcję, która przyjmuje
dowolny `IpAddrKind`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn}}
```

I możemy wywołać tę funkcję z dowolnym wariantem:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-01-defining-enums/src/main.rs:fn_call}}
```

Enumy mają jeszcze więcej zalet. Zastanówmy się dłużej nad naszym typem adresu
IP: na razie nie mamy jak przechować faktycznych _danych_ adresu IP, wiemy tylko,
jakiego jest _rodzaju_. Skoro struktury znasz już z rozdziału 5, możesz mieć
ochotę rozwiązać ten problem za ich pomocą, jak w listingu 6-1.

```aquascope,interpreter
#fn main() {
enum IpAddrKind {
    V4,
    V6,
}

struct IpAddr {
    kind: IpAddrKind,
    address: String,
}

let home = IpAddr {
    kind: IpAddrKind::V4,
    address: String::from("127.0.0.1"),
};

let loopback = IpAddr {
    kind: IpAddrKind::V6,
    address: String::from("::1"),
};`[]`
#}
```

Zdefiniowaliśmy tu strukturę `IpAddr` z dwoma polami: polem `kind` typu
`IpAddrKind` (enuma, którego zdefiniowaliśmy wcześniej) i polem `address` typu
`String`. Mamy dwie instancje tej struktury. Pierwsza to `home` – jej `kind` ma
wartość `IpAddrKind::V4`, a powiązane z nią dane adresu to `127.0.0.1`. Druga
instancja to `loopback`. Jej wartością `kind` jest drugi wariant `IpAddrKind`,
czyli `V6`, a powiązany z nią adres to `::1`. Użyliśmy struktury, żeby połączyć
wartości `kind` i `address`, więc teraz wariant jest powiązany z wartością.

Tę samą koncepcję można jednak wyrazić zwięźlej za pomocą samego enuma: zamiast
umieszczać enum w strukturze, możemy umieścić dane bezpośrednio w każdym
wariancie enuma. Ta nowa definicja enuma `IpAddr` mówi, że oba warianty, `V4` i
`V6`, będą miały powiązane wartości `String`:

```aquascope,interpreter
#fn main() {    
enum IpAddr {
    V4(String),
    V6(String),
}

let home = IpAddr::V4(String::from("127.0.0.1"));

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}
```

Dołączamy dane bezpośrednio do każdego wariantu enuma, więc dodatkowa struktura
nie jest potrzebna. Łatwiej tu też dostrzec inny szczegół działania enumów: nazwa
każdego zdefiniowanego wariantu enuma staje się zarazem funkcją, która tworzy
instancję enuma. Innymi słowy, `IpAddr::V4()` to wywołanie funkcji, która
przyjmuje argument typu `String` i zwraca instancję typu `IpAddr`. Tę funkcję
konstruującą dostajemy automatycznie w wyniku zdefiniowania enuma.

Enum ma nad strukturą jeszcze jedną przewagę: każdy wariant może mieć powiązane
dane innego typu i w innej ilości. Adresy IP w wersji czwartej zawsze składają
się z czterech liczb o wartościach od 0 do 255. Gdybyśmy chcieli przechowywać
adresy `V4` jako cztery wartości `u8`, a adresy `V6` nadal wyrażać jako jedną
wartość `String`, nie dalibyśmy rady zrobić tego za pomocą struktury. Enumy
radzą sobie z tym bez trudu:

```aquascope,interpreter
#fn main() {
enum IpAddr {
    V4(u8, u8, u8, u8),
    V6(String),
}

let home = IpAddr::V4(127, 0, 0, 1);

let loopback = IpAddr::V6(String::from("::1"));`[]`
#}

```

Pokazaliśmy kilka sposobów definiowania struktur danych do przechowywania adresów
IP w wersji czwartej i szóstej. Okazuje się jednak, że przechowywanie adresów IP
wraz z informacją o ich rodzaju jest tak powszechne, że
[biblioteka standardowa ma definicję, której możemy użyć!][IpAddr]<!-- ignore -->
Zobaczmy, jak biblioteka standardowa definiuje `IpAddr`. Ma dokładnie taki enum
i takie warianty, jakie zdefiniowaliśmy i jakich użyliśmy, ale dane adresu
umieszcza w wariantach w postaci dwóch różnych struktur, zdefiniowanych inaczej
dla każdego wariantu:

```rust
struct Ipv4Addr {
    // --snip--
}

struct Ipv6Addr {
    // --snip--
}

enum IpAddr {
    V4(Ipv4Addr),
    V6(Ipv6Addr),
}
```

Ten kod pokazuje, że w wariancie enuma można umieścić dane dowolnego rodzaju, na
przykład łańcuchy znaków (*string*), typy liczbowe albo struktury. Można nawet
umieścić w nim inny enum! Poza tym typy z biblioteki standardowej często nie są
dużo bardziej skomplikowane od tego, co można by wymyślić samodzielnie.

Zwróć uwagę, że choć biblioteka standardowa zawiera definicję `IpAddr`, wciąż
możemy bez konfliktu utworzyć i używać własnej definicji, bo nie wprowadziliśmy
definicji z biblioteki standardowej do naszego zasięgu (*scope*). Więcej o
wprowadzaniu typów do zasięgu powiemy w rozdziale 7.

Przyjrzyjmy się kolejnemu przykładowi enuma w listingu 6-2: ten ma w swoich
wariantach osadzone wartości bardzo różnych typów.

<Listing number="6-2" caption="Enum `Message`, którego warianty przechowują wartości różnych typów w różnej liczbie">

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/listing-06-02/src/main.rs:here}}
```

</Listing>

Ten enum ma cztery warianty różnych typów:

- `Quit`: nie ma żadnych powiązanych danych;
- `Move`: ma nazwane pola, tak jak struktura;
- `Write`: zawiera pojedynczy `String`;
- `ChangeColor`: zawiera trzy wartości `i32`.

Zdefiniowanie enuma z wariantami takimi jak w listingu 6-2 przypomina
zdefiniowanie różnych rodzajów struktur, z tą różnicą, że enum nie używa słowa
kluczowego (*keyword*) `struct`, a wszystkie warianty są zgrupowane w typie
`Message`. Te same dane, które przechowują warianty powyższego enuma, mogłyby
przechowywać następujące struktury:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-04-structs-similar-to-message-enum/src/main.rs:here}}
```

Gdybyśmy jednak użyli różnych struktur, z których każda ma własny typ, nie
moglibyśmy tak łatwo zdefiniować funkcji przyjmującej dowolny z tych rodzajów
komunikatów, jak w przypadku enuma `Message` z listingu 6-2, który jest
pojedynczym typem.

Enumy i struktury mają jeszcze jedno podobieństwo: tak jak możemy definiować
metody na strukturach za pomocą `impl`, możemy też definiować metody na enumach.
Oto metoda o nazwie `call`, którą moglibyśmy zdefiniować na naszym enumie
`Message`:

```rust
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-05-methods-on-enums/src/main.rs:here}}
```

Ciało metody użyłoby `self`, żeby dostać wartość, na której wywołaliśmy metodę.
W tym przykładzie utworzyliśmy zmienną `m` o wartości
`Message::Write(String::from("hello"))` i to właśnie ona będzie wartością `self`
w ciele metody `call`, gdy wykona się `m.call()`.

Przyjrzyjmy się innemu enumowi z biblioteki standardowej, który jest bardzo
powszechny i przydatny: `Option`.

<!-- Old headings. Do not remove or links may break. -->

<a id="the-option-enum-and-its-advantages-over-null-values"></a>

### Enum `Option` {#the-option-enum}

W tym podrozdziale przeanalizujemy przypadek `Option` – kolejnego enuma
zdefiniowanego w bibliotece standardowej. Typ `Option` wyraża bardzo częsty
scenariusz, w którym wartość może być czymś albo może być niczym.

Na przykład, jeśli zażądasz pierwszego elementu niepustej listy, dostaniesz
wartość. Jeśli zażądasz pierwszego elementu pustej listy, nie dostaniesz nic.
Wyrażenie tej koncepcji w kategoriach systemu typów (*type system*) oznacza, że
kompilator może sprawdzić, czy obsłużono wszystkie przypadki, które powinny
zostać obsłużone. Ta funkcjonalność może zapobiec błędom niezwykle częstym w
innych językach programowania.

O projektowaniu języka programowania często myśli się w kategoriach tego, jakie
funkcjonalności się w nim umieszcza, ale funkcjonalności pominięte też są ważne.
Rust nie ma znanego z wielu innych języków mechanizmu null. _Null_ to wartość
oznaczająca, że żadnej wartości tam nie ma. W językach z null zmienne zawsze
mogą być w jednym z dwóch stanów: null albo nie-null.

W swoim wystąpieniu z 2009 roku „Null References: The Billion Dollar Mistake”
Tony Hoare, twórca null, powiedział:

> Nazywam to swoim błędem wartym miliard dolarów. W tamtym czasie projektowałem
> pierwszy kompleksowy system typów dla referencji w języku obiektowym. Moim
> celem było zapewnienie, że każde użycie referencji będzie absolutnie
> bezpieczne, a sprawdzanie będzie wykonywane automatycznie przez kompilator.
> Nie mogłem się jednak oprzeć pokusie dodania referencji null, po prostu
> dlatego, że tak łatwo było ją zaimplementować. Doprowadziło to do
> niezliczonych błędów, podatności i awarii systemów, które w ciągu ostatnich
> czterdziestu lat spowodowały zapewne szkody i cierpienia warte miliard
> dolarów.

Problem z wartościami null polega na tym, że jeśli spróbujesz użyć wartości null
tak, jakby nie była null, dostaniesz jakiś błąd. Ponieważ ta właściwość bycia
null albo nie-null jest wszechobecna, niezwykle łatwo popełnić taki błąd.

Koncepcja, którą null próbuje wyrazić, jest jednak nadal przydatna: null to
wartość, która z jakiegoś powodu jest obecnie nieprawidłowa albo nieobecna.

Problem nie leży właściwie w samej koncepcji, tylko w konkretnej implementacji.
Dlatego Rust nie ma wartości null, ale ma enum, który potrafi wyrazić to, że
wartość jest obecna albo jej brak. Tym enumem jest `Option<T>`, a
[biblioteka standardowa definiuje go][option]<!-- ignore --> następująco:

```rust
enum Option<T> {
    None,
    Some(T),
}
```

Enum `Option<T>` jest tak przydatny, że znajduje się nawet w *prelude* (zestaw
elementów importowanych automatycznie), więc nie musisz jawnie wprowadzać go do
zasięgu. Jego warianty również są w prelude: możesz używać `Some` i `None`
bezpośrednio, bez prefiksu `Option::`. Enum `Option<T>` to mimo wszystko zwykły
enum, a `Some(T)` i `None` to nadal warianty typu `Option<T>`.

Składnia `<T>` to element Rusta, którego jeszcze nie omawialiśmy. To generyczny
parametr typu, a typy generyczne (*generics*) omówimy dokładniej w rozdziale
10. Na razie wystarczy ci wiedzieć, że `<T>` oznacza, iż wariant `Some` enuma
`Option` może przechowywać jedną wartość dowolnego typu, a każdy konkretny typ
użyty w miejsce `T` sprawia, że cały typ `Option<T>` staje się innym typem. Oto
kilka przykładów użycia wartości `Option` do przechowywania liczb i znaków:

```aquascope,interpreter
#fn main() {
let some_number = Some(5);
let some_char = Some('e');

let absent_number: Option<i32> = None;`[]`
#}
```

Typem `some_number` jest `Option<i32>`. Typem `some_char` jest `Option<char>`,
czyli inny typ. Rust potrafi wywnioskować te typy, bo podaliśmy wartość wewnątrz
wariantu `Some`. W przypadku `absent_number` Rust wymaga od nas adnotacji
całego typu `Option`: kompilator nie wywnioskuje, jakiego typu wartość
przechowywałby odpowiadający wariant `Some`, patrząc tylko na wartość `None`. Mówimy tu
Rustowi, że `absent_number` ma być typu `Option<i32>`.

Gdy mamy wartość `Some`, wiemy, że wartość jest obecna i jest przechowywana w
`Some`. Gdy mamy wartość `None`, w pewnym sensie oznacza to to samo co null: nie
mamy prawidłowej wartości. Dlaczego więc `Option<T>` jest w ogóle lepszy od
null?

Krótko mówiąc: ponieważ `Option<T>` i `T` (gdzie `T` może być dowolnym typem)
to różne typy, kompilator nie pozwoli nam użyć wartości `Option<T>` tak, jakby
na pewno była prawidłową wartością. Na przykład ten kod się nie skompiluje, bo
próbuje dodać `i8` do `Option<i8>`:

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/src/main.rs:here}}
```

Jeśli uruchomimy ten kod, dostaniemy komunikat o błędzie podobny do tego:

```console
{{#include ../listings/ch06-enums-and-pattern-matching/no-listing-07-cant-use-option-directly/output.txt}}
```

Brzmi groźnie! W praktyce ten komunikat oznacza, że Rust nie wie, jak dodać
`i8` i `Option<i8>`, bo to różne typy. Gdy w Ruście mamy wartość typu takiego
jak `i8`, kompilator zapewni, że zawsze jest to prawidłowa wartość. Możemy
śmiało działać dalej bez sprawdzania, czy przed użyciem tej wartości nie jest
ona null. Dopiero gdy mamy `Option<i8>` (albo inny typ wartości, z którą
pracujemy), musimy się martwić, że wartości może nie być, a kompilator dopilnuje,
żebyśmy obsłużyli ten przypadek przed jej użyciem.

Innymi słowy, musisz przekonwertować `Option<T>` na `T`, zanim wykonasz na tej
wartości operacje właściwe dla `T`. Na ogół pomaga to wychwycić jeden z
najczęstszych problemów z null: założenie, że coś nie jest null, gdy w
rzeczywistości jest.

Wyeliminowanie ryzyka błędnego założenia, że wartość nie jest null, pozwala ci
pewniej czuć się z własnym kodem. Żeby mieć wartość, która może być null, musisz
świadomie się na to zdecydować, nadając jej typ `Option<T>`. Potem, używając tej
wartości, musisz jawnie obsłużyć przypadek, w którym jest ona null. Wszędzie
tam, gdzie wartość ma typ inny niż `Option<T>`, _możesz_ bezpiecznie założyć, że
nie jest null. To przemyślana decyzja projektowa Rusta, która ma ograniczyć
wszechobecność null i zwiększyć bezpieczeństwo kodu w Ruście.

Jak więc wydobyć wartość `T` z wariantu `Some`, gdy masz wartość typu
`Option<T>`, żeby móc jej użyć? Enum `Option<T>` ma wiele metod przydatnych w
najróżniejszych sytuacjach; możesz je przejrzeć w
[jego dokumentacji][docs]<!-- ignore -->. Poznanie metod `Option<T>` bardzo się
przyda w twojej przygodzie z Rustem.

Ogólnie rzecz biorąc, żeby użyć wartości `Option<T>`, potrzebujesz kodu, który
obsłuży każdy wariant. Potrzebujesz kodu, który uruchomi się tylko wtedy, gdy
masz wartość `Some(T)`, i ten kod może używać wewnętrznej wartości `T`.
Potrzebujesz też innego kodu, który uruchomi się tylko wtedy, gdy masz wartość
`None`, i ten kod nie ma dostępu do wartości `T`. Wyrażenie `match` to
konstrukcja przepływu sterowania (*control flow*), która użyta z enumami robi
właśnie to: uruchamia różny kod w zależności od tego, jaki wariant enuma
otrzyma, a ten kod może używać danych wewnątrz dopasowanej wartości.

{{#quiz ../quizzes/ch06-01-defining-an-enum.toml}}

[IpAddr]: https://doc.rust-lang.org/std/net/enum.IpAddr.html
[option]: https://doc.rust-lang.org/std/option/enum.Option.html
[docs]: https://doc.rust-lang.org/std/option/enum.Option.html

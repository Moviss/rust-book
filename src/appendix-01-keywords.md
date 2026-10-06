## Dodatek A: Słowa kluczowe {#appendix-a-keywords}

Poniższe listy zawierają słowa kluczowe (*keyword*), które język Rust rezerwuje
do obecnego lub przyszłego użytku. Z tego powodu nie można ich używać jako
identyfikatorów (z wyjątkiem surowych identyfikatorów, które omawiamy w
podrozdziale [„Surowe identyfikatory”][raw-identifiers]<!-- ignore -->).
_Identyfikatory_ to nazwy funkcji, zmiennych, parametrów, pól struktur
(*struct*), modułów, *crate’ów* (jednostek kompilacji w Ruście), stałych
(*constant*), makr, wartości statycznych, atrybutów, typów, *traitów* (cech
typów, zbliżonych do interfejsów) i czasów życia (*lifetime*).

[raw-identifiers]: #raw-identifiers

### Obecnie używane słowa kluczowe {#keywords-currently-in-use}

Poniżej znajduje się lista obecnie używanych słów kluczowych wraz z opisem ich
działania.

- **`as`**: wykonuje rzutowanie typów prymitywnych, jednoznacznie wskazuje
  trait zawierający dany element albo zmienia nazwy elementów w instrukcjach `use`.
- **`async`**: zwraca `Future` zamiast blokować bieżący wątek.
- **`await`**: wstrzymuje wykonanie, dopóki wynik `Future` nie będzie gotowy.
- **`break`**: natychmiast kończy pętlę.
- **`const`**: definiuje stałe lub stałe surowe wskaźniki (*raw pointer*).
- **`continue`**: przechodzi do następnej iteracji pętli.
- **`crate`**: w ścieżce modułu oznacza korzeń crate’a (*crate root*).
- **`dyn`**: dynamiczne wywoływanie (*dynamic dispatch*) na obiekcie traitu
  (*trait object*).
- **`else`**: alternatywna gałąź w konstrukcjach przepływu sterowania
  (*control flow*) `if` i `if let`.
- **`enum`**: definiuje *enum* (typ wyliczeniowy).
- **`extern`**: łączy z zewnętrzną funkcją lub zmienną.
- **`false`**: literał logiczny oznaczający fałsz.
- **`fn`**: definiuje funkcję lub typ wskaźnika na funkcję (*function
  pointer*).
- **`for`**: iteruje po elementach z iteratora, implementuje trait albo określa
  czas życia wyższego rzędu.
- **`if`**: rozgałęzienie zależne od wyniku wyrażenia warunkowego.
- **`impl`**: implementuje funkcjonalność własną typu lub funkcjonalność
  traitu.
- **`in`**: część składni pętli `for`.
- **`let`**: wiąże zmienną.
- **`loop`**: pętla bezwarunkowa.
- **`match`**: dopasowuje wartość do wzorców.
- **`mod`**: definiuje moduł.
- **`move`**: sprawia, że domknięcie (*closure*) przejmuje własność
  (*ownership*) wszystkich przechwyconych wartości.
- **`mut`**: oznacza mutowalność (*mutability*) w referencjach (*reference*),
  surowych wskaźnikach lub wiązaniach we wzorcach.
- **`pub`**: oznacza publiczną widoczność pól struktur, bloków `impl` lub
  modułów.
- **`ref`**: wiąże przez referencję.
- **`return`**: powrót z funkcji.
- **`Self`**: alias typu dla typu, który definiujemy lub implementujemy.
- **`self`**: odbiorca metody lub bieżący moduł.
- **`static`**: zmienna globalna lub czas życia trwający przez całe wykonanie
  programu.
- **`struct`**: definiuje strukturę.
- **`super`**: moduł nadrzędny bieżącego modułu.
- **`trait`**: definiuje trait.
- **`true`**: literał logiczny oznaczający prawdę.
- **`type`**: definiuje alias typu lub typ powiązany (*associated type*).
- **`union`**: definiuje [unię][union]<!-- ignore --> (*union*); jest słowem
  kluczowym tylko w deklaracji unii.
- **`unsafe`**: oznacza niebezpieczny kod, niebezpieczne funkcje, traity lub
  implementacje.
- **`use`**: wprowadza symbole do zasięgu (*scope*).
- **`where`**: oznacza klauzule ograniczające typ.
- **`while`**: pętla warunkowa zależna od wyniku wyrażenia.

[union]: https://doc.rust-lang.org/reference/items/unions.html

### Słowa kluczowe zarezerwowane na przyszłość {#keywords-reserved-for-future-use}

Poniższe słowa kluczowe nie mają jeszcze żadnej funkcjonalności, ale Rust
rezerwuje je na potencjalny przyszły użytek:

- `abstract`
- `become`
- `box`
- `do`
- `final`
- `gen`
- `macro`
- `override`
- `priv`
- `try`
- `typeof`
- `unsized`
- `virtual`
- `yield`

### Surowe identyfikatory {#raw-identifiers}

_Surowe identyfikatory_ to składnia, która pozwala używać słów kluczowych tam,
gdzie normalnie nie byłyby dozwolone. Surowego identyfikatora używasz,
poprzedzając słowo kluczowe prefiksem `r#`.

Na przykład `match` jest słowem kluczowym. Jeśli spróbujesz skompilować
poniższą funkcję, która ma nazwę `match`:

<span class="filename">Plik: src/main.rs</span>

```rust,ignore,does_not_compile
fn match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}
```

otrzymasz taki błąd:

```text
error: expected identifier, found keyword `match`
 --> src/main.rs:4:4
  |
4 | fn match(needle: &str, haystack: &str) -> bool {
  |    ^^^^^ expected identifier, found keyword
```

Błąd pokazuje, że nie możesz użyć słowa kluczowego `match` jako identyfikatora
funkcji. Aby użyć `match` jako nazwy funkcji, musisz zastosować składnię
surowych identyfikatorów, o tak:

<span class="filename">Plik: src/main.rs</span>

```rust
fn r#match(needle: &str, haystack: &str) -> bool {
    haystack.contains(needle)
}

fn main() {
    assert!(r#match("foo", "foobar"));
}
```

Ten kod skompiluje się bez żadnych błędów. Zwróć uwagę na prefiks `r#` przed
nazwą funkcji zarówno w jej definicji, jak i w miejscu jej wywołania w `main`.

Surowe identyfikatory pozwalają użyć jako identyfikatora dowolnie wybranego
słowa, nawet jeśli jest ono zarezerwowanym słowem kluczowym. Daje nam to
większą swobodę w wyborze nazw identyfikatorów, a także umożliwia integrację z
programami napisanymi w języku, w którym te słowa nie są słowami kluczowymi.
Ponadto surowe identyfikatory pozwalają korzystać z bibliotek napisanych w innej
edycji (*edition*) Rusta niż ta, której używa twój crate. Na przykład `try` nie
jest słowem kluczowym w edycji 2015, ale jest nim w edycjach 2018, 2021 i 2024.
Jeśli twój kod zależy od biblioteki napisanej w edycji 2015, która ma funkcję
`try`, to aby wywołać tę funkcję ze swojego kodu w późniejszych edycjach,
musisz użyć składni surowych identyfikatorów – w tym przypadku `r#try`. Więcej
informacji o edycjach znajdziesz w [dodatku E][appendix-e]<!-- ignore -->.

[appendix-e]: appendix-05-editions.html

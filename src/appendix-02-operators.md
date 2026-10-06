## Dodatek B: Operatory i symbole {#appendix-b-operators-and-symbols}

Ten dodatek zawiera słowniczek składni Rusta, w tym operatory i inne symbole,
które występują samodzielnie lub w kontekście ścieżek, typów generycznych
(*generics*), ograniczeń traitów (*trait bound*), makr, atrybutów, komentarzy,
krotek (*tuple*) i nawiasów.

### Operatory {#operators}

Tabela B-1 zawiera operatory Rusta, przykład użycia każdego z nich w kontekście,
krótkie objaśnienie oraz informację, czy dany operator można przeciążać. Jeśli
operator jest przeciążalny, podano trait, którego należy użyć, aby go
przeciążyć.

<span class="caption">Tabela B-1: Operatory</span>

| Operator                  | Przykład                                                | Objaśnienie                                                                    | Przeciążalny?  |
| ------------------------- | ------------------------------------------------------- | ------------------------------------------------------------------------------ | -------------- |
| `!`                       | `ident!(...)`, `ident!{...}`, `ident![...]`             | Rozwinięcie makra                                                              |                |
| `!`                       | `!expr`                                                 | Negacja bitowa lub logiczna                                                    | `Not`          |
| `!=`                      | `expr != expr`                                          | Porównanie nierówności                                                         | `PartialEq`    |
| `%`                       | `expr % expr`                                           | Reszta z dzielenia                                                             | `Rem`          |
| `%=`                      | `var %= expr`                                           | Reszta z dzielenia z przypisaniem                                              | `RemAssign`    |
| `&`                       | `&expr`, `&mut expr`                                    | Pożyczenie                                                                     |                |
| `&`                       | `&type`, `&mut type`, `&'a type`, `&'a mut type`        | Typ wskaźnika pożyczonego                                                      |                |
| `&`                       | `expr & expr`                                           | Bitowe AND                                                                     | `BitAnd`       |
| `&=`                      | `var &= expr`                                           | Bitowe AND z przypisaniem                                                      | `BitAndAssign` |
| `&&`                      | `expr && expr`                                          | Logiczne AND ze skróconym obliczaniem                                          |                |
| `*`                       | `expr * expr`                                           | Mnożenie arytmetyczne                                                          | `Mul`          |
| `*=`                      | `var *= expr`                                           | Mnożenie arytmetyczne z przypisaniem                                           | `MulAssign`    |
| `*`                       | `*expr`                                                 | Dereferencja                                                                   | `Deref`        |
| `*`                       | `*const type`, `*mut type`                              | Surowy wskaźnik                                                                |                |
| `+`                       | `trait + trait`, `'a + trait`                           | Złożone ograniczenie typu                                                      |                |
| `+`                       | `expr + expr`                                           | Dodawanie arytmetyczne                                                         | `Add`          |
| `+=`                      | `var += expr`                                           | Dodawanie arytmetyczne z przypisaniem                                          | `AddAssign`    |
| `,`                       | `expr, expr`                                            | Separator argumentów i elementów                                               |                |
| `-`                       | `- expr`                                                | Negacja arytmetyczna                                                           | `Neg`          |
| `-`                       | `expr - expr`                                           | Odejmowanie arytmetyczne                                                       | `Sub`          |
| `-=`                      | `var -= expr`                                           | Odejmowanie arytmetyczne z przypisaniem                                        | `SubAssign`    |
| `->`                      | `fn(...) -> type`, <code>&vert;...&vert; -> type</code> | Typ zwracany funkcji i domknięcia                                              |                |
| `.`                       | `expr.ident`                                            | Dostęp do pola                                                                 |                |
| `.`                       | `expr.ident(expr, ...)`                                 | Wywołanie metody                                                               |                |
| `.`                       | `expr.0`, `expr.1` itd.                                 | Indeksowanie krotki                                                            |                |
| `..`                      | `..`, `expr..`, `..expr`, `expr..expr`                  | Literał zakresu prawostronnie otwartego                                        | `PartialOrd`   |
| `..=`                     | `..=expr`, `expr..=expr`                                | Literał zakresu prawostronnie domkniętego                                      | `PartialOrd`   |
| `..`                      | `..expr`                                                | Składnia aktualizacji w literale struktury                                     |                |
| `..`                      | `variant(x, ..)`, `struct_type { x, .. }`               | Wiązanie „i reszta” we wzorcu                                                  |                |
| `...`                     | `expr...expr`                                           | (Przestarzałe, zamiast tego użyj `..=`) We wzorcu: wzorzec zakresu domkniętego |                |
| `/`                       | `expr / expr`                                           | Dzielenie arytmetyczne                                                         | `Div`          |
| `/=`                      | `var /= expr`                                           | Dzielenie arytmetyczne z przypisaniem                                          | `DivAssign`    |
| `:`                       | `pat: type`, `ident: type`                              | Ograniczenia                                                                   |                |
| `:`                       | `ident: expr`                                           | Inicjalizator pola struktury                                                   |                |
| `:`                       | `'a: loop {...}`                                        | Etykieta pętli                                                                 |                |
| `;`                       | `expr;`                                                 | Zakończenie instrukcji i elementu                                              |                |
| `;`                       | `[...; len]`                                            | Część składni tablicy o stałym rozmiarze                                       |                |
| `<<`                      | `expr << expr`                                          | Przesunięcie bitowe w lewo                                                     | `Shl`          |
| `<<=`                     | `var <<= expr`                                          | Przesunięcie bitowe w lewo z przypisaniem                                      | `ShlAssign`    |
| `<`                       | `expr < expr`                                           | Porównanie „mniejsze niż”                                                      | `PartialOrd`   |
| `<=`                      | `expr <= expr`                                          | Porównanie „mniejsze lub równe”                                                | `PartialOrd`   |
| `=`                       | `var = expr`, `ident = type`                            | Przypisanie/równoważność                                                       |                |
| `==`                      | `expr == expr`                                          | Porównanie równości                                                            | `PartialEq`    |
| `=>`                      | `pat => expr`                                           | Część składni ramienia dopasowania                                             |                |
| `>`                       | `expr > expr`                                           | Porównanie „większe niż”                                                       | `PartialOrd`   |
| `>=`                      | `expr >= expr`                                          | Porównanie „większe lub równe”                                                 | `PartialOrd`   |
| `>>`                      | `expr >> expr`                                          | Przesunięcie bitowe w prawo                                                    | `Shr`          |
| `>>=`                     | `var >>= expr`                                          | Przesunięcie bitowe w prawo z przypisaniem                                     | `ShrAssign`    |
| `@`                       | `ident @ pat`                                           | Wiązanie we wzorcu                                                             |                |
| `^`                       | `expr ^ expr`                                           | Bitowe XOR (alternatywa wykluczająca)                                          | `BitXor`       |
| `^=`                      | `var ^= expr`                                           | Bitowe XOR (alternatywa wykluczająca) z przypisaniem                           | `BitXorAssign` |
| <code>&vert;</code>       | <code>pat &vert; pat</code>                             | Alternatywy we wzorcu                                                          |                |
| <code>&vert;</code>       | <code>expr &vert; expr</code>                           | Bitowe OR                                                                      | `BitOr`        |
| <code>&vert;=</code>      | <code>var &vert;= expr</code>                           | Bitowe OR z przypisaniem                                                       | `BitOrAssign`  |
| <code>&vert;&vert;</code> | <code>expr &vert;&vert; expr</code>                     | Logiczne OR ze skróconym obliczaniem                                           |                |
| `?`                       | `expr?`                                                 | Propagowanie błędów                                                            |                |

### Symbole niebędące operatorami {#non-operator-symbols}

Poniższe tabele zawierają wszystkie symbole, które nie działają jak operatory,
czyli nie zachowują się jak wywołanie funkcji lub metody.

Tabela B-2 pokazuje symbole, które występują samodzielnie i są poprawne w wielu
różnych miejscach.

<span class="caption">Tabela B-2: Składnia samodzielna</span>

| Symbol                                                                    | Objaśnienie                                                                                   |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| `'ident`                                                                  | Nazwany czas życia lub etykieta pętli                                                         |
| Cyfry, po których bezpośrednio następuje `u8`, `i32`, `f64`, `usize` itd. | Literał liczbowy określonego typu                                                             |
| `"..."`                                                                   | Literał łańcuchowy                                                                            |
| `r"..."`, `r#"..."#`, `r##"..."##` itd.                                   | Surowy literał łańcuchowy; sekwencje ucieczki nie są przetwarzane                             |
| `b"..."`                                                                  | Bajtowy literał łańcuchowy; tworzy tablicę bajtów zamiast łańcucha znaków                     |
| `br"..."`, `br#"..."#`, `br##"..."##` itd.                                | Surowy bajtowy literał łańcuchowy; połączenie literału surowego i bajtowego                   |
| `'...'`                                                                   | Literał znakowy                                                                               |
| `b'...'`                                                                  | Literał bajtowy ASCII                                                                         |
| <code>&vert;...&vert; expr</code>                                         | Domknięcie                                                                                    |
| `!`                                                                       | Zawsze pusty typ dolny dla funkcji rozbieżnych                                                |
| `_`                                                                       | „Ignorowane” wiązanie we wzorcu; służy też do poprawy czytelności literałów liczb całkowitych |

Tabela B-3 pokazuje symbole, które występują w kontekście ścieżki prowadzącej
przez hierarchię modułów do elementu.

<span class="caption">Tabela B-3: Składnia związana ze ścieżkami</span>

| Symbol                                  | Objaśnienie                                                                                                |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `ident::ident`                          | Ścieżka w przestrzeni nazw                                                                                 |
| `::path`                                | Ścieżka względem korzenia crate’a (czyli jawnie bezwzględna)                                               |
| `self::path`                            | Ścieżka względem bieżącego modułu (czyli jawnie względna)                                                  |
| `super::path`                           | Ścieżka względem rodzica bieżącego modułu                                                                  |
| `type::ident`, `<type as trait>::ident` | Powiązane stałe, funkcje i typy                                                                            |
| `<type>::...`                           | Element powiązany typu, którego nie można nazwać bezpośrednio (na przykład `<&T>::...`, `<[T]>::...` itd.) |
| `trait::method(...)`                    | Ujednoznacznienie wywołania metody przez podanie nazwy traitu, który ją definiuje                          |
| `type::method(...)`                     | Ujednoznacznienie wywołania metody przez podanie nazwy typu, dla którego jest zdefiniowana                 |
| `<type as trait>::method(...)`          | Ujednoznacznienie wywołania metody przez podanie nazwy traitu i typu                                       |

Tabela B-4 pokazuje symbole, które występują w kontekście używania generycznych
parametrów typu.

<span class="caption">Tabela B-4: Typy generyczne</span>

| Symbol                         | Objaśnienie                                                                                                                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------ |
| `path<...>`                    | Określa parametry typu generycznego w typie (na przykład `Vec<u8>`)                                                                  |
| `path::<...>`, `method::<...>` | Określa parametry typu generycznego, funkcji lub metody w wyrażeniu; często nazywane _turbofish_ (na przykład `"42".parse::<i32>()`) |
| `fn ident<...> ...`            | Definicja funkcji generycznej                                                                                                        |
| `struct ident<...> ...`        | Definicja struktury generycznej                                                                                                      |
| `enum ident<...> ...`          | Definicja generycznego typu wyliczeniowego                                                                                           |
| `impl<...> ...`                | Definicja implementacji generycznej                                                                                                  |
| `for<...> type`                | Ograniczenia czasów życia wyższego rzędu                                                                                             |
| `type<ident=type>`             | Typ generyczny, w którym co najmniej jeden typ powiązany ma przypisany konkretny typ (na przykład `Iterator<Item=T>`)                |

Tabela B-5 pokazuje symbole, które występują w kontekście ograniczania
generycznych parametrów typu za pomocą ograniczeń traitów.

<span class="caption">Tabela B-5: Ograniczenia traitów</span>

| Symbol                        | Objaśnienie                                                                                                                                                     |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `T: U`                        | Parametr generyczny `T` ograniczony do typów implementujących `U`                                                                                               |
| `T: 'a`                       | Typ generyczny `T` musi żyć dłużej niż czas życia `'a` (co oznacza, że typ nie może przechodnio zawierać żadnych referencji o czasach życia krótszych niż `'a`) |
| `T: 'static`                  | Typ generyczny `T` nie zawiera pożyczonych referencji innych niż `'static`                                                                                      |
| `'b: 'a`                      | Generyczny czas życia `'b` musi żyć dłużej niż czas życia `'a`                                                                                                  |
| `T: ?Sized`                   | Pozwala, by generyczny parametr typu był typem o dynamicznym rozmiarze                                                                                          |
| `'a + trait`, `trait + trait` | Złożone ograniczenie typu                                                                                                                                       |

Tabela B-6 pokazuje symbole, które występują w kontekście wywoływania lub
definiowania makr oraz określania atrybutów elementu.

<span class="caption">Tabela B-6: Makra i atrybuty</span>

| Symbol                                      | Objaśnienie           |
| ------------------------------------------- | --------------------- |
| `#[meta]`                                   | Atrybut zewnętrzny    |
| `#![meta]`                                  | Atrybut wewnętrzny    |
| `$ident`                                    | Podstawienie w makrze |
| `$ident:kind`                               | Metazmienna makra     |
| `$(...)...`                                 | Powtórzenie w makrze  |
| `ident!(...)`, `ident!{...}`, `ident![...]` | Wywołanie makra       |

Tabela B-7 pokazuje symbole tworzące komentarze.

<span class="caption">Tabela B-7: Komentarze</span>

| Symbol     | Objaśnienie                                 |
| ---------- | ------------------------------------------- |
| `//`       | Komentarz liniowy                           |
| `//!`      | Wewnętrzny liniowy komentarz dokumentacyjny |
| `///`      | Zewnętrzny liniowy komentarz dokumentacyjny |
| `/*...*/`  | Komentarz blokowy                           |
| `/*!...*/` | Wewnętrzny blokowy komentarz dokumentacyjny |
| `/**...*/` | Zewnętrzny blokowy komentarz dokumentacyjny |

Tabela B-8 pokazuje konteksty, w których używa się nawiasów okrągłych.

<span class="caption">Tabela B-8: Nawiasy okrągłe</span>

| Symbol            | Objaśnienie                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------- |
| `()`              | Pusta krotka (inaczej wartość jednostkowa), zarówno literał, jak i typ                                    |
| `(expr)`          | Wyrażenie w nawiasach                                                                                     |
| `(expr,)`         | Wyrażenie krotki jednoelementowej                                                                         |
| `(type,)`         | Typ krotki jednoelementowej                                                                               |
| `(expr, ...)`     | Wyrażenie krotki                                                                                          |
| `(type, ...)`     | Typ krotki                                                                                                |
| `expr(expr, ...)` | Wyrażenie wywołania funkcji; służy też do inicjalizacji struktur krotkowych `struct` i krotkowych wariantów `enum` |

Tabela B-9 pokazuje konteksty, w których używa się nawiasów klamrowych.

<span class="caption">Tabela B-9: Nawiasy klamrowe</span>

| Kontekst     | Objaśnienie       |
| ------------ | ----------------- |
| `{...}`      | Wyrażenie blokowe |
| `Type {...}` | Literał struktury |

Tabela B-10 pokazuje konteksty, w których używa się nawiasów kwadratowych.

<span class="caption">Tabela B-10: Nawiasy kwadratowe</span>

| Kontekst                                           | Objaśnienie                                                                                                                          |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `[...]`                                            | Literał tablicy                                                                                                                      |
| `[expr; len]`                                      | Literał tablicy zawierającej `len` kopii `expr`                                                                                      |
| `[type; len]`                                      | Typ tablicy zawierającej `len` instancji `type`                                                                                      |
| `expr[expr]`                                       | Indeksowanie kolekcji; przeciążalne (`Index`, `IndexMut`)                                                                            |
| `expr[..]`, `expr[a..]`, `expr[..b]`, `expr[a..b]` | Indeksowanie kolekcji udające wycinanie fragmentu kolekcji, z użyciem `Range`, `RangeFrom`, `RangeTo` lub `RangeFull` jako „indeksu” |

## Odrzucalność: czy wzorzec może nie pasować {#refutability-whether-a-pattern-might-fail-to-match}

Wzorce występują w dwóch postaciach: odrzucalnej (*refutable*) i
nieodrzucalnej (*irrefutable*). Wzorce, które pasują do każdej możliwej
przekazanej wartości, są _nieodrzucalne_. Przykładem jest `x` w instrukcji
(*statement*) `let x = 5;`, ponieważ `x` pasuje do wszystkiego, a więc nie może
nie pasować. Wzorce, które dla jakiejś możliwej wartości mogą nie pasować, są
_odrzucalne_. Oto kilka przykładów:

<!-- BEGIN INTERVENTION: 3c29eb2d-cbe9-4a2c-99b8-aa5c6467c8b4 -->
* W wyrażeniu (*expression*) `if let Some(x) = a_value` wzorzec `Some(x)` jest odrzucalny. Jeśli wartością zmiennej `a_value` jest `None`, a nie
`Some`, wzorzec `Some(x)` nie zostanie dopasowany. 
* W wyrażeniu `if let &[x, ..] = a_slice` wzorzec `&[x, ..]` jest odrzucalny. Jeśli wartość w zmiennej `a_slice` nie ma żadnych elementów, wzorzec `&[x, ..]` nie zostanie dopasowany.
<!-- END INTERVENTION: 3c29eb2d-cbe9-4a2c-99b8-aa5c6467c8b4 -->

Parametry funkcji, instrukcje `let` i pętle `for` mogą przyjmować tylko wzorce
nieodrzucalne, ponieważ program nie jest w stanie zrobić nic sensownego, gdy
wartości nie pasują. Wyrażenia `if let` i `while let` oraz instrukcja
`let...else` przyjmują wzorce odrzucalne i nieodrzucalne, ale kompilator
ostrzega przed wzorcami nieodrzucalnymi, ponieważ z definicji konstrukcje te
służą do obsługi możliwej porażki: sens instrukcji warunkowej polega na tym, że
może ona działać różnie w zależności od powodzenia lub porażki.

Zasadniczo nie musisz przejmować się rozróżnieniem między wzorcami odrzucalnymi
i nieodrzucalnymi. Musisz jednak znać pojęcie odrzucalności, aby umieć
zareagować, gdy zobaczysz je w komunikacie o błędzie. W takich przypadkach
trzeba będzie zmienić albo wzorzec, albo konstrukcję, w której go używasz, w
zależności od zamierzonego działania kodu.

Przyjrzyjmy się przykładowi tego, co się dzieje, gdy próbujemy użyć wzorca
odrzucalnego tam, gdzie Rust wymaga wzorca nieodrzucalnego, i odwrotnie.
Listing 19-8 pokazuje instrukcję `let`, w której jako wzorzec podaliśmy
`Some(x)`, czyli wzorzec odrzucalny. Jak można się spodziewać, ten kod się nie
skompiluje.

<Listing number="19-8" caption="Próba użycia wzorca odrzucalnego z `let`">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-08/src/main.rs:here}}
```

</Listing>

Gdyby `some_option_value` miało wartość `None`, nie pasowałoby do wzorca
`Some(x)`, co oznacza, że wzorzec jest odrzucalny. Instrukcja `let` przyjmuje
jednak tylko wzorce nieodrzucalne, ponieważ kod nie może zrobić nic poprawnego
z wartością `None`. W czasie kompilacji (*compile-time*) Rust zgłosi, że
próbowaliśmy użyć wzorca odrzucalnego tam, gdzie wymagany jest wzorzec
nieodrzucalny:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-08/output.txt}}
```

Ponieważ wzorzec `Some(x)` nie obejmuje (i nie mógłby objąć!) wszystkich
poprawnych wartości, Rust słusznie zgłasza błąd kompilatora.

Jeśli mamy wzorzec odrzucalny tam, gdzie potrzebny jest nieodrzucalny, możemy
to naprawić, zmieniając kod, który używa wzorca: zamiast `let` możemy użyć
`let...else`. Wtedy, jeśli wzorzec nie pasuje, wartością zajmie się kod w
nawiasach klamrowych. Listing 19-9 pokazuje, jak poprawić kod z listingu 19-8.

<Listing number="19-9" caption="Użycie `let...else` i bloku z wzorcami odrzucalnymi zamiast `let`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-09/src/main.rs:here}}
```

</Listing>

Daliśmy kodowi wyjście awaryjne! Ten kod jest całkowicie poprawny, choć oznacza
to, że nie możemy użyć wzorca nieodrzucalnego bez otrzymania ostrzeżenia. Jeśli
przekażemy `let...else` wzorzec, który zawsze pasuje, na przykład `x`, jak w
listingu 19-10, kompilator zgłosi ostrzeżenie.

<Listing number="19-10" caption="Próba użycia wzorca nieodrzucalnego z `let...else`">

```rust
{{#rustdoc_include ../listings/ch19-patterns-and-matching/listing-19-10/src/main.rs:here}}
```

</Listing>

Rust zgłasza, że używanie `let...else` z wzorcem nieodrzucalnym nie ma sensu:

```console
{{#include ../listings/ch19-patterns-and-matching/listing-19-10/output.txt}}
```

Z tego powodu ramiona (*arms*) dopasowania muszą używać wzorców odrzucalnych, z
wyjątkiem ostatniego ramienia, które powinno dopasowywać wszystkie pozostałe
wartości wzorcem nieodrzucalnym. Rust pozwala użyć wzorca nieodrzucalnego w
`match` z tylko jednym ramieniem, ale taka składnia nie jest szczególnie
przydatna i można by ją zastąpić prostszą instrukcją `let`.

Teraz, gdy wiesz, gdzie używać wzorców i czym różnią się wzorce odrzucalne od
nieodrzucalnych, omówmy całą składnię, za pomocą której możemy tworzyć wzorce.

{{#quiz ../quizzes/ch18-02-refutability.toml}}

# Kompromisy projektowe {#design-trade-offs}

Ten podrozdział dotyczy **kompromisów projektowych** w Ruście. Aby skutecznie programować w Ruście, nie wystarczy wiedzieć, jak Rust działa. Trzeba też decydować, które z wielu narzędzi Rusta pasują do danego zadania. W tym podrozdziale damy ci serię quizów sprawdzających, jak rozumiesz kompromisy projektowe w Ruście. Po każdym quizie szczegółowo wyjaśnimy uzasadnienie każdego pytania.

Oto przykład, jak będzie wyglądać pytanie. Zaczyna się od opisu studium przypadku z oprogramowania wraz z przestrzenią możliwych rozwiązań:

> **Kontekst:** projektujesz aplikację z globalną konfiguracją, np. zawierającą flagi wiersza poleceń.
>
> **Funkcjonalność:** aplikacja musi przekazywać niemutowalne referencje (*immutable references*) do tej konfiguracji w całym programie.
>
> **Rozwiązania:** poniżej znajduje się kilka proponowanych rozwiązań realizujących tę funkcjonalność.
>
> ```rust,ignore
> use std::rc::Rc;
> use std::sync::Arc;
>
> struct Config { 
>     flags: Flags,
>     // .. more fields ..
> }
> 
> // Option 1: use a reference
> struct ConfigRef<'a>(&'a Config);
> 
> // Option 2: use a reference-counted pointer
> struct ConfigRef(Rc<Config>);
> 
> // Option 3: use an atomic reference-counted pointer
> struct ConfigRef(Arc<Config>);
> ```

Jeśli znamy tylko kontekst i kluczową funkcjonalność, wszystkie trzy rozwiązania są potencjalnymi kandydatami.
Aby zdecydować, które z nich mają największy sens, potrzebujemy więcej informacji o celach systemu.
Dlatego podajemy nowe wymaganie:

> Zaznacz każdą opcję projektową, która spełnia następujące wymaganie:
>
> **Wymaganie:** referencję do konfiguracji musi dać się współdzielić między wieloma wątkami.
>
> **Odpowiedź:**
>
> <input type="checkbox" checked disabled> Opcja 1 <br>
> <input type="checkbox" disabled> Opcja 2 <br>
> <input type="checkbox" checked disabled> Opcja 3 <br>

Formalnie oznacza to, że `ConfigRef` implementuje [`Send`] i [`Sync`].
Przy założeniu `Config: Send + Sync` zarówno `&Config`, jak i `Arc<Config>` spełniają to wymaganie,
ale [`Rc`] go nie spełnia (ponieważ nieatomowe wskaźniki ze zliczaniem referencji nie są bezpieczne wątkowo). Opcja 2 nie spełnia więc wymagania, a opcja 3 – tak.

Może też kusić wniosek, że opcja 1 nie spełnia wymagania, ponieważ funkcje takie jak [`thread::spawn`] wymagają, by wszystkie dane przenoszone do wątku zawierały wyłącznie referencje z czasem życia (*lifetime*) `'static`. Nie wyklucza to jednak opcji 1 z dwóch powodów:
1.  `Config` mógłby być przechowywany w globalnej zmiennej statycznej (np. za pomocą [`OnceLock`]), dzięki czemu dałoby się tworzyć referencje `&'static Config`.
2. Nie wszystkie mechanizmy współbieżności (*concurrency*) wymagają czasów życia `'static`, np. [`thread::scope`].

Wymaganie w obecnym brzmieniu wyklucza więc tylko typy, które nie implementują [`Send`], i za poprawne odpowiedzi uznajemy opcje 1 i 3.

[`thread::spawn`]: https://doc.rust-lang.org/std/thread/fn.spawn.html
[`Send`]: https://doc.rust-lang.org/std/marker/trait.Send.html
[`Sync`]: https://doc.rust-lang.org/std/marker/trait.Sync.html
[`Rc`]: https://doc.rust-lang.org/std/rc/struct.Rc.html
[`OnceLock`]: https://doc.rust-lang.org/std/sync/struct.OnceLock.html
[`thread::scope`]: https://doc.rust-lang.org/std/thread/fn.scope.html

<hr>

Teraz twoja kolej – spróbuj odpowiedzieć na poniższe pytania! Każda sekcja zawiera quiz skupiony na jednym scenariuszu. Rozwiąż quiz i koniecznie przeczytaj objaśnienie odpowiedzi po każdym quizie.
 <!-- These questions are both experimental and opinionated &mdash; please leave us feedback via the bug button 🐞 if you disagree with our answers. -->

Przy każdym quizie podajemy też linki do popularnych *crate’ów* (jednostek kompilacji w Ruście), które posłużyły jako inspiracja dla quizu.

## Referencje {#references}

*Inspiracja:* [zasoby w Bevy][Bevy assets], [indeksy węzłów w Petgraph][Petgraph node indices], [jednostki w Cargo][Cargo units]

{{#quiz ../quizzes/ch17-05-design-challenge-references.toml}}


[Bevy assets]: https://docs.rs/bevy/0.11.2/bevy/asset/struct.Assets.html
[Petgraph node indices]: https://docs.rs/petgraph/0.6.4/petgraph/graph/struct.NodeIndex.html
[Cargo units]: https://docs.rs/cargo/0.73.1/cargo/core/compiler/struct.Unit.html

## Drzewa traitów {#trait-trees}

*Inspiracja:* [komponenty w Yew][Yew components], [widżety w Druid][Druid widgets]

{{#quiz ../quizzes/ch17-05-design-challenge-trait-trees.toml}}

[Yew components]: https://docs.rs/yew/0.20.0/yew/html/trait.Component.html
[Druid widgets]: https://docs.rs/druid/0.8.3/druid/trait.Widget.html

## Wywoływanie metod {#dispatch}

*Inspiracja:* [systemy w Bevy][Bevy systems], [zapytania w Diesel][Diesel queries], [funkcje obsługi w Axum][Axum handlers]

{{#quiz ../quizzes/ch17-05-design-challenge-dispatch.toml}}

[Bevy systems]: https://docs.rs/bevy_ecs/0.11.2/bevy_ecs/system/trait.IntoSystem.html
[Diesel queries]: https://docs.diesel.rs/2.1.x/diesel/query_dsl/trait.BelongingToDsl.html
[Axum handlers]: https://docs.rs/axum/0.6.20/axum/handler/trait.Handler.html

## Reprezentacje pośrednie {#intermediates}

*Inspiracja:* [Serde] i [miniserde]

{{#quiz ../quizzes/ch17-05-design-challenge-intermediates.toml}}

[Serde]: https://docs.rs/serde/1.0.188/serde/trait.Serialize.html
[miniserde]: https://docs.rs/miniserde/0.1.34/miniserde/trait.Serialize.html
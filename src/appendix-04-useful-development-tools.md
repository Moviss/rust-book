## Dodatek D: Przydatne narzędzia programistyczne {#appendix-d-useful-development-tools}

W tym dodatku omówimy kilka przydatnych narzędzi programistycznych, które
udostępnia Projekt Rust. Przyjrzymy się automatycznemu formatowaniu, szybkim
sposobom stosowania poprawek ostrzeżeń, linterowi oraz integracji ze
środowiskami IDE.

### Automatyczne formatowanie za pomocą `rustfmt` {#automatic-formatting-with-rustfmt}

Narzędzie `rustfmt` formatuje kod zgodnie ze stylem kodu przyjętym przez
społeczność. Wiele wspólnych projektów używa `rustfmt`, aby uniknąć sporów o
to, jakiego stylu używać przy pisaniu w Ruście: każdy formatuje swój kod tym
narzędziem.

Instalacje Rusta domyślnie zawierają `rustfmt`, więc programy `rustfmt` i
`cargo-fmt` powinny już być w twoim systemie. Te dwa polecenia są analogiczne do
`rustc` i `cargo`: `rustfmt` pozwala na dokładniejszą kontrolę, a `cargo-fmt`
rozumie konwencje projektu korzystającego z Cargo. Aby sformatować dowolny
projekt Cargo, wpisz:

```console
$ cargo fmt
```

Uruchomienie tego polecenia formatuje cały kod w Ruście w bieżącym *crate’cie*
(jednostce kompilacji w Ruście). Powinno to zmienić jedynie styl kodu, a nie
jego semantykę. Więcej informacji o `rustfmt` znajdziesz w
[jego dokumentacji][rustfmt].

### Poprawianie kodu za pomocą `rustfix` {#fix-your-code-with-rustfix}

Narzędzie `rustfix` jest dołączane do instalacji Rusta i potrafi automatycznie
naprawiać te ostrzeżenia kompilatora, które mają jasny sposób rozwiązania
problemu, prawdopodobnie zgodny z twoimi intencjami. Zapewne zdarzyło ci się już
widzieć ostrzeżenia kompilatora. Weźmy na przykład taki kod:

<span class="filename">Plik: src/main.rs</span>

```rust
fn main() {
    let mut x = 42;
    println!("{x}");
}
```

Definiujemy tu zmienną `x` jako mutowalną (*mutable*), ale nigdy jej nie
modyfikujemy. Rust nas przed tym ostrzega:

```console
$ cargo build
   Compiling myprogram v0.1.0 (file:///projects/myprogram)
warning: variable does not need to be mutable
 --> src/main.rs:2:9
  |
2 |     let mut x = 0;
  |         ----^
  |         |
  |         help: remove this `mut`
  |
  = note: `#[warn(unused_mut)]` on by default
```

Ostrzeżenie sugeruje usunięcie słowa kluczowego (*keyword*) `mut`. Możemy
automatycznie zastosować tę sugestię za pomocą narzędzia `rustfix`, uruchamiając
polecenie `cargo fix`:

```console
$ cargo fix
    Checking myprogram v0.1.0 (file:///projects/myprogram)
      Fixing src/main.rs (1 fix)
    Finished dev [unoptimized + debuginfo] target(s) in 0.59s
```

Gdy ponownie zajrzymy do _src/main.rs_, zobaczymy, że `cargo fix` zmieniło kod:

<span class="filename">Plik: src/main.rs</span>

```rust
fn main() {
    let x = 42;
    println!("{x}");
}
```

Zmienna `x` jest teraz niemutowalna, a ostrzeżenie już się nie pojawia.

Polecenia `cargo fix` możesz też użyć do przeniesienia kodu między różnymi
edycjami (*edition*) Rusta. Edycje omawiamy w [dodatku E][editions]<!--
ignore -->.

### Więcej lintów dzięki Clippy {#more-lints-with-clippy}

Narzędzie Clippy to zbiór lintów (reguł analizy statycznej) sprawdzających kod,
dzięki którym możesz wyłapywać typowe błędy i ulepszać swój kod w Ruście. Clippy
jest dołączane do standardowych instalacji Rusta.

Aby uruchomić linty Clippy na dowolnym projekcie Cargo, wpisz:

```console
$ cargo clippy
```

Załóżmy na przykład, że piszesz program, który używa przybliżenia stałej
(*constant*) matematycznej, takiej jak pi, tak jak ten program:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = 3.1415;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Uruchomienie `cargo clippy` na tym projekcie skutkuje takim błędem:

```text
error: approximate value of `f{32, 64}::consts::PI` found
 --> src/main.rs:2:13
  |
2 |     let x = 3.1415;
  |             ^^^^^^
  |
  = note: `#[deny(clippy::approx_constant)]` on by default
  = help: consider using the constant directly
  = help: for further information visit https://rust-lang.github.io/rust-clippy/master/index.html#approx_constant
```

Ten błąd informuje, że Rust ma już zdefiniowaną dokładniejszą stałą `PI` i że
twój program byłby bardziej poprawny, gdyby jej użył. Należałoby wtedy zmienić
kod tak, aby korzystał ze stałej `PI`.

Poniższy kod nie powoduje żadnych błędów ani ostrzeżeń Clippy:

<Listing file-name="src/main.rs">

```rust
fn main() {
    let x = std::f64::consts::PI;
    let r = 8.0;
    println!("the area of the circle is {}", x * r * r);
}
```

</Listing>

Więcej informacji o Clippy znajdziesz w [jego dokumentacji][clippy].

### Integracja z IDE za pomocą `rust-analyzer` {#ide-integration-using-rust-analyzer}

Aby ułatwić integrację ze środowiskami IDE, społeczność Rusta zaleca używanie
[`rust-analyzer`][rust-analyzer]<!-- ignore -->. Jest to zestaw narzędzi
opartych na kompilatorze, które obsługują [Language Server Protocol][lsp]<!--
ignore -->, czyli specyfikację komunikacji między środowiskami IDE a językami
programowania. Z `rust-analyzer` mogą korzystać różne klienty, na przykład
[wtyczka Rust analyzer dla Visual Studio Code][vscode].

Odwiedź [stronę główną][rust-analyzer]<!-- ignore --> projektu `rust-analyzer`,
aby poznać instrukcje instalacji, a następnie zainstaluj obsługę serwera
języka w swoim IDE. Twoje IDE zyska takie możliwości jak autouzupełnianie,
przechodzenie do definicji i wyświetlanie błędów bezpośrednio w kodzie.

[rustfmt]: https://github.com/rust-lang/rustfmt
[editions]: appendix-05-editions.md
[clippy]: https://github.com/rust-lang/rust-clippy
[rust-analyzer]: https://rust-analyzer.github.io
[lsp]: http://langserver.org/
[vscode]: https://marketplace.visualstudio.com/items?itemName=rust-lang.rust-analyzer

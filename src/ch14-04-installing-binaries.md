<!-- Old headings. Do not remove or links may break. -->

<a id="installing-binaries-from-cratesio-with-cargo-install"></a>

## Instalowanie plików binarnych za pomocą `cargo install` {#installing-binaries-with-cargo-install}

Polecenie `cargo install` pozwala instalować i używać lokalnie crate’ów
binarnych (*crate* to jednostka kompilacji w Ruście). Nie ma ono zastępować
pakietów systemowych; to po prostu wygodny sposób, w jaki programiści Rusta
mogą instalować narzędzia udostępnione przez innych na
[crates.io](https://crates.io/)<!-- ignore -->. Pamiętaj, że możesz instalować
tylko pakiety, które mają cele binarne. _Cel binarny_ (*binary target*) to
program dający się uruchomić, który powstaje, gdy crate ma plik _src/main.rs_
lub inny plik wskazany jako binarny – w przeciwieństwie do celu bibliotecznego,
którego nie da się uruchomić samodzielnie, ale który nadaje się do dołączania
do innych programów. Zwykle crate’y zawierają w pliku README informację o tym,
czy crate jest biblioteką, ma cel binarny, czy jedno i drugie.

Wszystkie pliki binarne zainstalowane za pomocą `cargo install` trafiają do
folderu _bin_ w katalogu głównym instalacji. Jeśli Rust został zainstalowany za
pomocą _rustup.rs_ i nie masz żadnej niestandardowej konfiguracji, będzie to
katalog *$HOME/.cargo/bin*. Upewnij się, że ten katalog jest w twoim `$PATH`,
aby móc uruchamiać programy zainstalowane za pomocą `cargo install`.

Na przykład w rozdziale 12 wspomnieliśmy, że istnieje napisana w Ruście
implementacja narzędzia `grep` do przeszukiwania plików, o nazwie `ripgrep`.
Aby zainstalować `ripgrep`, możemy uruchomić następujące polecenie:

<!-- manual-regeneration
cargo install something you don't have, copy relevant output below
-->

```console
$ cargo install ripgrep
    Updating crates.io index
  Downloaded ripgrep v14.1.1
  Downloaded 1 crate (213.6 KB) in 0.40s
  Installing ripgrep v14.1.1
--snip--
   Compiling grep v0.3.2
    Finished `release` profile [optimized + debuginfo] target(s) in 6.73s
  Installing ~/.cargo/bin/rg
   Installed package `ripgrep v14.1.1` (executable `rg`)
```

Przedostatnia linia wyjścia pokazuje położenie i nazwę zainstalowanego pliku
binarnego, którym w przypadku `ripgrep` jest `rg`. Jeśli tylko katalog
instalacji jest w twoim `$PATH`, jak wspomnieliśmy wcześniej, możesz uruchomić
`rg --help` i zacząć używać szybszego, bardziej rustowego narzędzia do
przeszukiwania plików!

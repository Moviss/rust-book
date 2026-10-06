## Rozszerzanie Cargo o własne polecenia {#extending-cargo-with-custom-commands}

Cargo zaprojektowano tak, aby można go było rozszerzać o nowe podpolecenia bez
konieczności modyfikowania go. Jeśli plik binarny w twoim `$PATH` nazywa się
`cargo-something`, możesz go uruchomić tak, jakby był podpoleceniem Cargo,
wpisując `cargo something`. Takie własne polecenia pojawiają się też na liście
po uruchomieniu `cargo --list`. Możliwość instalowania rozszerzeń za pomocą
`cargo install` i uruchamiania ich tak samo jak wbudowanych narzędzi Cargo to
niezwykle wygodna zaleta tego, jak zaprojektowano Cargo!

## Podsumowanie {#summary}

Udostępnianie kodu za pomocą Cargo i [crates.io](https://crates.io/)<!-- ignore -->
to jeden z powodów, dla których ekosystem Rusta przydaje się do tak wielu
różnych zadań. Biblioteka standardowa Rusta jest mała i stabilna, ale *crate’y*
(jednostki kompilacji w Ruście) łatwo udostępniać, używać i ulepszać w rytmie
niezależnym od rozwoju języka. Nie krępuj się udostępniać kodu, który jest
przydatny dla ciebie, na [crates.io](https://crates.io/)<!-- ignore
-->; całkiem możliwe, że przyda się też komuś innemu!

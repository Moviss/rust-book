## Dostosowywanie kompilacji za pomocą profili wydania {#customizing-builds-with-release-profiles}

W Ruście _profile wydania_ (*release profiles*) to predefiniowane profile o
różnych konfiguracjach, które można dostosowywać i które dają programiście
większą kontrolę nad różnymi opcjami kompilacji kodu. Każdy profil konfiguruje
się niezależnie od pozostałych.

Cargo ma dwa główne profile: profil `dev`, którego Cargo używa, gdy uruchamiasz
`cargo build`, oraz profil `release`, którego Cargo używa, gdy uruchamiasz
`cargo build --release`. Profil `dev` ma ustawienia domyślne dobrane pod kątem
programowania, a profil `release` – pod kątem wersji wydaniowych.

Nazwy tych profili mogą być ci znane z wyjścia kompilacji:

<!-- manual-regeneration
anywhere, run:
cargo build
cargo build --release
and ensure output below is accurate
-->

```console
$ cargo build
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.00s
$ cargo build --release
    Finished `release` profile [optimized] target(s) in 0.32s
```

`dev` i `release` to właśnie te różne profile, których używa kompilator.

Dla każdego z profili Cargo ma ustawienia domyślne, które obowiązują, jeśli w
pliku _Cargo.toml_ projektu nie dodano jawnie żadnych sekcji `[profile.*]`.
Dodając sekcje `[profile.*]` dla profili, które chcesz dostosować, nadpisujesz
dowolny podzbiór ustawień domyślnych. Oto na przykład domyślne wartości
ustawienia `opt-level` dla profili `dev` i `release`:

<span class="filename">Plik: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 0

[profile.release]
opt-level = 3
```

Ustawienie `opt-level` określa, ile optymalizacji Rust zastosuje do twojego
kodu, w zakresie od 0 do 3. Więcej optymalizacji wydłuża czas kompilacji,
więc jeśli rozwijasz program i często kompilujesz kod, zależy ci na mniejszej
liczbie optymalizacji, aby kompilacja trwała krócej, nawet jeśli wynikowy kod
działa wolniej. Dlatego domyślny `opt-level` dla `dev` to `0`. Gdy kod jest
gotowy do wydania, najlepiej poświęcić więcej czasu na kompilację. W trybie
wydania skompilujesz program tylko raz, ale uruchomisz go wiele razy, więc
tryb wydania zamienia dłuższy czas kompilacji na szybciej działający kod.
Właśnie dlatego domyślny `opt-level` dla profilu `release` to `3`.

Ustawienie domyślne możesz nadpisać, podając dla niego inną wartość w
_Cargo.toml_. Jeśli na przykład chcemy używać poziomu optymalizacji 1 w
profilu deweloperskim, możemy dodać te dwa wiersze do pliku _Cargo.toml_
naszego projektu:

<span class="filename">Plik: Cargo.toml</span>

```toml
[profile.dev]
opt-level = 1
```

Ten kod nadpisuje domyślne ustawienie `0`. Teraz, gdy uruchomimy `cargo build`,
Cargo użyje ustawień domyślnych profilu `dev` wraz z naszą zmianą `opt-level`.
Ponieważ ustawiliśmy `opt-level` na `1`, Cargo zastosuje więcej optymalizacji
niż domyślnie, ale nie tyle, ile w wersji wydaniowej.

Pełną listę opcji konfiguracji i ustawień domyślnych każdego profilu znajdziesz
w [dokumentacji Cargo](https://doc.rust-lang.org/cargo/reference/profiles.html).

{{#quiz ../quizzes/ch14-01-release-profiles.toml}}

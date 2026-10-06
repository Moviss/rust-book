## Dodatek E: Edycje {#appendix-e-editions}

W rozdziale 1 widzieliśmy, że `cargo new` dodaje do pliku _Cargo.toml_ trochę
metadanych dotyczących edycji (*edition*). W tym dodatku wyjaśniamy, co to
oznacza!

Język Rust i jego kompilator mają sześciotygodniowy cykl wydawniczy, co oznacza,
że użytkownicy otrzymują nieustanny strumień nowych funkcjonalności. Inne języki
programowania wydają większe zmiany rzadziej; Rust wydaje mniejsze aktualizacje
częściej. Po pewnym czasie wszystkie te drobne zmiany się sumują. Jednak z
perspektywy pojedynczych wydań trudno spojrzeć wstecz i powiedzieć: „Ależ Rust
się zmienił między wersją 1.10 a 1.31!”.

Mniej więcej co trzy lata zespół Rusta przygotowuje nową _edycję_ Rusta. Każda
edycja zbiera funkcjonalności, które w tym czasie trafiły do języka, w spójną
całość z w pełni zaktualizowaną dokumentacją i narzędziami. Nowe edycje są
wydawane w ramach zwykłego sześciotygodniowego procesu wydawniczego.

Edycje służą różnym celom dla różnych osób:

- Dla aktywnych użytkowników Rusta nowa edycja zbiera stopniowe zmiany w łatwą
  do zrozumienia całość.
- Dla osób, które Rusta nie używają, nowa edycja jest sygnałem, że pojawiły się
  istotne usprawnienia, dla których być może warto przyjrzeć się Rustowi
  ponownie.
- Dla osób rozwijających Rusta nowa edycja jest punktem zbornym dla całego
  projektu.

W chwili pisania tej książki dostępne są cztery edycje Rusta: Rust 2015, Rust
2018, Rust 2021 i Rust 2024. Ta książka została napisana z użyciem idiomów
edycji Rust 2024.

Klucz `edition` w pliku _Cargo.toml_ określa, której edycji kompilator powinien
używać dla twojego kodu. Jeśli klucz nie istnieje, Rust ze względu na
zgodność wsteczną używa jako wartości edycji `2015`.

Każdy projekt może wybrać edycję inną niż domyślna edycja 2015. Edycje mogą
zawierać niezgodne zmiany, takie jak dodanie nowego słowa kluczowego
(*keyword*), które koliduje z identyfikatorami w kodzie. Jednak dopóki nie
zdecydujesz się na te zmiany, twój kod będzie się nadal kompilował, nawet gdy
zaktualizujesz używaną wersję kompilatora Rusta.

Wszystkie wersje kompilatora Rusta obsługują każdą edycję, która istniała przed
wydaniem danego kompilatora, i potrafią łączyć ze sobą *crate’y* (jednostki
kompilacji w Ruście) w dowolnych obsługiwanych edycjach. Zmiany wprowadzane przez
edycje wpływają jedynie na to, jak kompilator początkowo parsuje kod. Dlatego
jeśli używasz Rusta 2015, a jedna z twoich zależności używa Rusta 2018, twój
projekt skompiluje się i będzie mógł korzystać z tej zależności. Sytuacja
odwrotna, gdy twój projekt używa Rusta 2018, a zależność Rusta 2015, również
działa.

Dla jasności: większość funkcjonalności będzie dostępna we wszystkich
edycjach. Programiści używający dowolnej edycji Rusta będą nadal otrzymywać
usprawnienia wraz z kolejnymi stabilnymi wydaniami. Jednak w niektórych
przypadkach, głównie gdy dodawane są nowe słowa kluczowe, niektóre nowe
funkcjonalności mogą być dostępne tylko w późniejszych edycjach. Jeśli zechcesz
z nich skorzystać, trzeba będzie zmienić edycję.

Więcej szczegółów znajdziesz w [_The Rust Edition Guide_][edition-guide]. To
kompletna książka, która wylicza różnice między edycjami i wyjaśnia, jak
automatycznie zaktualizować kod do nowej edycji za pomocą `cargo fix`.

[edition-guide]: https://doc.rust-lang.org/stable/edition-guide

## Pakiety i crate’y {#packages-and-crates}

Pierwsze elementy systemu modułów, które omówimy, to pakiety i crate’y.

_Crate_ (jednostka kompilacji w Ruście) to najmniejsza porcja kodu, jaką
kompilator Rusta rozpatruje naraz. Nawet jeśli uruchomisz `rustc` zamiast
`cargo` i przekażesz mu pojedynczy plik z kodem źródłowym (jak zrobiliśmy to
dawno temu w podrozdziale [„Podstawy programu w Ruście”][basics]<!-- ignore
--> w rozdziale 1), kompilator traktuje ten plik jako crate. Crate’y mogą
zawierać moduły, a moduły mogą być zdefiniowane w innych plikach, kompilowanych
razem z crate’em, jak zobaczymy w kolejnych podrozdziałach.

Crate może mieć jedną z dwóch postaci: crate binarny albo crate biblioteczny.
_Crate’y binarne_ to programy, które możesz skompilować do pliku
wykonywalnego i uruchomić, na przykład program wiersza poleceń albo serwer.
Każdy z nich musi mieć funkcję o nazwie `main`, która określa, co się dzieje po
uruchomieniu pliku wykonywalnego. Wszystkie crate’y, które do tej pory
utworzyliśmy, były crate’ami binarnymi.

_Crate’y biblioteczne_ nie mają funkcji `main` i nie kompilują się do pliku
wykonywalnego. Zamiast tego definiują funkcjonalność przeznaczoną do
współdzielenia przez wiele projektów. Na przykład crate `rand`, którego
używaliśmy w [rozdziale 2][rand]<!-- ignore -->, udostępnia funkcjonalność
generowania liczb losowych. Najczęściej, gdy rustowcy (*Rustaceans*) mówią
„crate”, mają na myśli crate biblioteczny i używają słowa „crate” zamiennie z
ogólnym programistycznym pojęciem „biblioteki”.

_Korzeń crate’a_ (*crate root*) to plik źródłowy, od którego kompilator Rusta
zaczyna pracę i który tworzy moduł główny twojego crate’a (moduły szczegółowo
wyjaśnimy w podrozdziale
[„Kontrolowanie zasięgu i prywatności za pomocą modułów”][modules]<!-- ignore -->).

_Pakiet_ (*package*) to zestaw jednego lub więcej crate’ów, który zapewnia
pewną funkcjonalność. Pakiet zawiera plik _Cargo.toml_ opisujący, jak zbudować
te crate’y. Samo Cargo jest w rzeczywistości pakietem zawierającym crate
binarny narzędzia wiersza poleceń, którego używasz do budowania swojego kodu.
Pakiet Cargo zawiera też crate biblioteczny, od którego zależy ten crate
binarny. Inne projekty mogą zależeć od crate’a bibliotecznego Cargo, żeby
korzystać z tej samej logiki, której używa narzędzie wiersza poleceń Cargo.

Pakiet może zawierać dowolnie wiele crate’ów binarnych, ale co najwyżej jeden
crate biblioteczny. Pakiet musi zawierać co najmniej jeden crate – biblioteczny
lub binarny.

Prześledźmy, co się dzieje, gdy tworzymy pakiet. Najpierw wpisujemy polecenie
`cargo new my-project`:

```console
$ cargo new my-project
     Created binary (application) `my-project` package
$ ls my-project
Cargo.toml
src
$ ls my-project/src
main.rs
```

Po uruchomieniu `cargo new my-project` używamy `ls`, żeby zobaczyć, co utworzyło
Cargo. W katalogu _my-project_ znajduje się plik _Cargo.toml_, który czyni z
niego pakiet. Jest tam też katalog _src_ zawierający plik _main.rs_. Otwórz
_Cargo.toml_ w edytorze tekstu i zwróć uwagę, że nie ma tam żadnej wzmianki o
_src/main.rs_. Cargo przyjmuje konwencję, zgodnie z którą _src/main.rs_ jest
korzeniem crate’a binarnego o tej samej nazwie co pakiet. Podobnie Cargo wie,
że jeśli katalog pakietu zawiera _src/lib.rs_, to pakiet zawiera crate
biblioteczny o tej samej nazwie co pakiet, a _src/lib.rs_ jest jego korzeniem.
Cargo przekazuje pliki będące korzeniami crate’ów do `rustc`, żeby zbudować
bibliotekę lub plik binarny.

W tym przykładzie mamy pakiet zawierający tylko _src/main.rs_, co oznacza, że
zawiera on tylko crate binarny o nazwie `my-project`. Jeśli pakiet zawiera
_src/main.rs_ i _src/lib.rs_, ma dwa crate’y: binarny i biblioteczny, oba o tej
samej nazwie co pakiet. Pakiet może mieć wiele crate’ów binarnych – wystarczy
umieścić pliki w katalogu _src/bin_: każdy plik będzie osobnym crate’em
binarnym.

{{#quiz ../quizzes/ch07-01-packages-and-crates.toml}}

[basics]: ch01-02-hello-world.html#rust-program-basics
[modules]: ch07-02-defining-modules-to-control-scope-and-privacy.html
[rand]: ch02-00-guessing-game-tutorial.html#generating-a-random-number

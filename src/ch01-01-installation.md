## Instalacja {#installation}

Pierwszym krokiem jest instalacja Rusta. Pobierzemy go za pomocą `rustup` –
narzędzia wiersza poleceń do zarządzania wersjami Rusta i powiązanymi
narzędziami. Do pobrania potrzebne będzie połączenie z internetem.

> Uwaga: Jeśli z jakiegoś powodu wolisz nie używać `rustup`, zajrzyj na
> [stronę z innymi metodami instalacji Rusta][otherinstall], gdzie znajdziesz
> więcej możliwości.

Poniższe kroki instalują najnowszą stabilną wersję kompilatora Rusta. Gwarancje
stabilności Rusta zapewniają, że wszystkie przykłady z tej książki, które się
kompilują, będą się kompilować także w nowszych wersjach Rusta. Wyniki mogą się
nieznacznie różnić między wersjami, ponieważ Rust często ulepsza komunikaty o
błędach i ostrzeżenia. Innymi słowy, każda nowsza, stabilna wersja Rusta
zainstalowana według tych kroków powinna działać zgodnie z treścią tej książki.

> ### Notacja wiersza poleceń {#command-line-notation}
>
> W tym rozdziale i w całej książce pokażemy niektóre polecenia wpisywane w
> terminalu. Wszystkie linie, które należy wpisać w terminalu, zaczynają się od
> `$`. Nie musisz wpisywać znaku `$` – to znak zachęty wiersza poleceń,
> pokazywany na początku każdego polecenia. Linie, które nie zaczynają się od
> `$`, zwykle pokazują wynik poprzedniego polecenia. Ponadto przykłady
> specyficzne dla PowerShella będą używać `>` zamiast `$`.

### Instalacja `rustup` w systemie Linux lub macOS {#installing-rustup-on-linux-or-macos}

Jeśli używasz Linuksa lub macOS, otwórz terminal i wpisz następujące polecenie:

```console
$ curl --proto '=https' --tlsv1.2 https://sh.rustup.rs -sSf | sh
```

Polecenie pobiera skrypt i rozpoczyna instalację narzędzia `rustup`, które
instaluje najnowszą stabilną wersję Rusta. Instalator może poprosić o hasło.
Jeśli instalacja się powiedzie, pojawi się następująca linia:

```text
Rust is installed now. Great!
```

Potrzebny będzie też _linker_ (konsolidator), czyli program, którego Rust używa
do łączenia skompilowanych wyników w jeden plik. Najprawdopodobniej już go masz.
Jeśli pojawią się błędy linkera, zainstaluj kompilator C, który zwykle zawiera
linker. Kompilator C przydaje się też dlatego, że niektóre popularne pakiety
(*packages*) Rusta zależą od kodu w C i wymagają kompilatora C.

W macOS kompilator C możesz zainstalować, uruchamiając:

```console
$ xcode-select --install
```

Użytkownicy Linuksa powinni zazwyczaj zainstalować GCC lub Clang zgodnie z
dokumentacją swojej dystrybucji. Na przykład w Ubuntu możesz zainstalować pakiet
`build-essential`.

### Instalacja `rustup` w systemie Windows {#installing-rustup-on-windows}

W systemie Windows wejdź na [https://www.rust-lang.org/tools/install][install]<!-- ignore
--> i postępuj zgodnie z instrukcjami instalacji Rusta. W pewnym momencie
instalacji pojawi się prośba o zainstalowanie Visual Studio. Zapewnia ono linker
i natywne biblioteki potrzebne do kompilowania programów. Jeśli potrzebujesz
więcej pomocy przy tym kroku, zajrzyj na
[https://rust-lang.github.io/rustup/installation/windows-msvc.html][msvc]<!--
ignore -->.

W dalszej części książki używamy poleceń, które działają zarówno w _cmd.exe_, jak
i w PowerShellu. Jeśli wystąpią konkretne różnice, wyjaśnimy, którego użyć.

### Rozwiązywanie problemów {#troubleshooting}

Aby sprawdzić, czy Rust jest poprawnie zainstalowany, otwórz powłokę i wpisz tę
linię:

```console
$ rustc --version
```

Powinien pojawić się numer wersji, hash commita i data commita najnowszej
wydanej wersji stabilnej, w następującym formacie:

```text
rustc x.y.z (abcabcabc yyyy-mm-dd)
```

Jeśli widzisz te informacje, Rust został zainstalowany pomyślnie! Jeśli ich nie
widzisz, sprawdź w następujący sposób, czy Rust znajduje się w zmiennej
systemowej `PATH`.

W Windows CMD użyj:

```console
> echo %PATH%
```

W PowerShellu użyj:

```powershell
> echo $env:Path
```

W systemach Linux i macOS użyj:

```console
$ echo $PATH
```

Jeśli wszystko się zgadza, a Rust nadal nie działa, jest wiele miejsc, w których
możesz uzyskać pomoc. Na [stronie społeczności][community] dowiesz się, jak
skontaktować się z innymi rustowcami (*Rustaceans*) – tak żartobliwie nazywamy
samych siebie.

### Aktualizacja i odinstalowanie {#updating-and-uninstalling}

Gdy Rust jest już zainstalowany za pomocą `rustup`, aktualizacja do nowo wydanej
wersji jest prosta. W powłoce uruchom następujący skrypt aktualizacji:

```console
$ rustup update
```

Aby odinstalować Rusta i `rustup`, uruchom w powłoce następujący skrypt
deinstalacji:

```console
$ rustup self uninstall
```

<!-- Old headings. Do not remove or links may break. -->
<a id="local-documentation"></a>

### Czytanie lokalnej dokumentacji {#reading-the-local-documentation}

Instalacja Rusta obejmuje też lokalną kopię dokumentacji, dzięki czemu możesz ją
czytać offline. Uruchom `rustup doc`, aby otworzyć lokalną dokumentację w
przeglądarce.

Zawsze gdy biblioteka standardowa udostępnia typ lub funkcję, a nie masz
pewności, co robi lub jak jej użyć, sprawdź to w dokumentacji API!

<!-- Old headings. Do not remove or links may break. -->
<a id="text-editors-and-integrated-development-environments"></a>

### Korzystanie z edytorów tekstu i IDE {#using-text-editors-and-ides}

Ta książka nie zakłada niczego na temat narzędzi, których używasz do pisania
kodu w Ruście. Wystarczy niemal dowolny edytor tekstu! Wiele edytorów tekstu i
zintegrowanych środowisk programistycznych (IDE) ma jednak wbudowaną obsługę
Rusta. Dość aktualną listę wielu edytorów i IDE zawsze znajdziesz na
[stronie z narzędziami][tools] w serwisie Rusta.

### Praca offline z tą książką {#working-offline-with-this-book}

W kilku przykładach użyjemy pakietów Rusta spoza biblioteki standardowej. Aby
przerobić te przykłady, potrzebujesz połączenia z internetem albo wcześniej
pobranych zależności. Aby pobrać zależności z wyprzedzeniem, możesz uruchomić
poniższe polecenia. (Później szczegółowo wyjaśnimy, czym jest `cargo` i co
robi każde z tych poleceń).

```console
$ cargo new get-dependencies
$ cd get-dependencies
$ cargo add rand@0.8.5 trpl@0.2.0
```

Spowoduje to zapisanie pobranych pakietów w pamięci podręcznej, więc nie trzeba
będzie pobierać ich później. Po uruchomieniu tego polecenia nie musisz
zachowywać folderu `get-dependencies`. Jeśli je uruchomisz, w dalszej części
książki możesz używać flagi `--offline` we wszystkich poleceniach `cargo`, aby
korzystać z zapisanych wersji zamiast łączyć się z siecią.

{{#quiz ../quizzes/ch01-01-installation.toml}}

[otherinstall]: https://forge.rust-lang.org/infra/other-installation-methods.html
[install]: https://www.rust-lang.org/tools/install
[msvc]: https://rust-lang.github.io/rustup/installation/windows-msvc.html
[community]: https://www.rust-lang.org/community
[tools]: https://www.rust-lang.org/tools

## Dodatek G: Jak powstaje Rust i „Rust nightly” {#appendix-g---how-rust-is-made-and-nightly-rust}

Ten dodatek opowiada o tym, jak powstaje Rust i jak wpływa to na ciebie jako
programistę Rusta.

### Stabilność bez stagnacji {#stability-without-stagnation}

Jako język Rust _bardzo_ dba o stabilność twojego kodu. Chcemy, aby Rust był
solidnym jak skała fundamentem, na którym możesz budować, a gdyby wszystko
nieustannie się zmieniało, byłoby to niemożliwe. Jednocześnie, jeśli nie
będziemy mogli eksperymentować z nowymi funkcjonalnościami, możemy odkryć
poważne wady dopiero po ich wydaniu, gdy nie da się już niczego zmienić.

Nasze rozwiązanie tego problemu nazywamy „stabilnością bez stagnacji”, a naszą
zasadą przewodnią jest to, że nigdy nie musisz obawiać się aktualizacji do nowej
wersji stabilnego Rusta. Każda aktualizacja powinna być bezbolesna, ale też
przynosić nowe funkcjonalności, mniej błędów i krótszy czas kompilacji.

### Ciuf, ciuf! Kanały wydań i jazda pociągami {#choo-choo-release-channels-and-riding-the-trains}

Rozwój Rusta działa według _rozkładu jazdy pociągów_ (*train schedule*). Oznacza
to, że cała praca rozwojowa odbywa się w głównej gałęzi repozytorium Rusta.
Wydania przebiegają według modelu pociągu wydań oprogramowania, stosowanego
przez Cisco IOS i inne projekty programistyczne. Rust ma trzy _kanały wydań_ (*release
channels*):

- nightly;
- beta;
- stable.

Większość programistów Rusta korzysta głównie z kanału stable, ale ci, którzy
chcą wypróbować eksperymentalne nowe funkcjonalności, mogą używać kanału
nightly lub beta.

Oto przykład działania procesu rozwoju i wydawania: załóżmy, że zespół Rusta
pracuje nad wydaniem Rusta 1.5. To wydanie ukazało się w grudniu 2015 roku, ale
pozwoli nam posłużyć się realistycznymi numerami wersji. Do Rusta zostaje dodana
nowa funkcjonalność: nowy commit trafia do głównej gałęzi. Każdej nocy powstaje
nowa wersja nightly Rusta. Każdy dzień jest dniem wydania, a te wydania są
tworzone automatycznie przez naszą infrastrukturę wydawniczą. Z upływem czasu
nasze wydania wyglądają więc tak, jedno co noc:

```text
nightly: * - - * - - *
```

Co sześć tygodni przychodzi czas na przygotowanie nowego wydania! Gałąź `beta`
repozytorium Rusta odgałęzia się od głównej gałęzi używanej przez nightly.
Teraz są dwa wydania:

```text
nightly: * - - * - - *
                     |
beta:                *
```

Większość użytkowników Rusta nie korzysta aktywnie z wydań beta, ale testuje
swój kod z wersją beta w systemie CI, aby pomóc Rustowi wykryć ewentualne
regresje. W międzyczasie wciąż co noc pojawia się wydanie nightly:

```text
nightly: * - - * - - * - - * - - *
                     |
beta:                *
```

Załóżmy, że wykryto regresję. Dobrze, że mieliśmy trochę czasu na
przetestowanie wydania beta, zanim regresja przedostała się do wydania
stabilnego! Poprawka trafia do głównej gałęzi, dzięki czemu wydanie nightly
zostaje naprawione, a następnie poprawka jest przenoszona wstecz (*backport*)
do gałęzi `beta` i powstaje nowe wydanie beta:

```text
nightly: * - - * - - * - - * - - * - - *
                     |
beta:                * - - - - - - - - *
```

Sześć tygodni po utworzeniu pierwszej wersji beta przychodzi czas na wydanie
stabilne! Gałąź `stable` powstaje z gałęzi `beta`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |
beta:                * - - - - - - - - *
                                       |
stable:                                *
```

Hura! Rust 1.5 jest gotowy! Zapomnieliśmy jednak o jednym: ponieważ minęło
sześć tygodni, potrzebujemy też nowej wersji beta _kolejnej_ wersji Rusta, 1.6.
Po tym, jak `stable` odgałęzi się od `beta`, kolejna wersja `beta` ponownie
odgałęzia się od `nightly`:

```text
nightly: * - - * - - * - - * - - * - - * - * - *
                     |                         |
beta:                * - - - - - - - - *       *
                                       |
stable:                                *
```

Nazywamy to „modelem pociągu”, ponieważ co sześć tygodni wydanie „odjeżdża ze
stacji”, ale musi jeszcze odbyć podróż przez kanał beta, zanim dotrze na miejsce
jako wydanie stabilne.

Rust wydaje nową wersję co sześć tygodni, jak w zegarku. Jeśli znasz datę
jednego wydania Rusta, znasz też datę następnego: sześć tygodni później. Zaletą
wydań planowanych co sześć tygodni jest to, że następny pociąg przyjeżdża
wkrótce. Jeśli jakaś funkcjonalność nie zdąży na dane wydanie, nie ma się czym
martwić: kolejne nastąpi niedługo! Zmniejsza to presję, by tuż przed terminem
wydania przemycać do niego funkcjonalności, które mogą być niedopracowane.

Dzięki temu procesowi zawsze możesz pobrać kolejną kompilację Rusta i
samodzielnie sprawdzić, czy aktualizacja do niej jest łatwa: jeśli wydanie beta
nie działa zgodnie z oczekiwaniami, możesz zgłosić to zespołowi i doprowadzić do
naprawy przed kolejnym wydaniem stabilnym! Usterki w wydaniu beta zdarzają się
stosunkowo rzadko, ale `rustc` to wciąż oprogramowanie, a błędy się zdarzają.

### Okres wsparcia {#maintenance-time}

Projekt Rust wspiera najnowszą wersję stabilną. Gdy zostaje wydana nowa wersja
stabilna, stara wersja osiąga koniec wsparcia (*end of life*, EOL). Oznacza to,
że każda wersja jest wspierana przez sześć tygodni.

### Funkcjonalności niestabilne {#unstable-features}

Ten model wydań ma jeszcze jeden haczyk: funkcjonalności niestabilne. Rust
używa techniki zwanej „flagami funkcjonalności”, aby określić, które
funkcjonalności są włączone w danym wydaniu. Jeśli nowa funkcjonalność jest
aktywnie rozwijana, trafia do głównej gałęzi, a zatem do nightly, ale ukryta za
_flagą funkcjonalności_ (*feature flag*). Jeśli jako użytkownik chcesz
wypróbować funkcjonalność, nad którą wciąż trwają prace, możesz to zrobić, ale
musisz używać wydania nightly Rusta i oznaczyć swój kod źródłowy odpowiednią
flagą, aby ją włączyć.

Jeśli używasz wydania beta lub stabilnego Rusta, nie możesz używać żadnych flag
funkcjonalności. To właśnie pozwala nam praktycznie korzystać z nowych
funkcjonalności, zanim ogłosimy je stabilnymi na zawsze. Kto chce korzystać z
najnowszych nowinek, może to zrobić, a kto chce mieć solidne jak skała
doświadczenie, może pozostać przy wersji stabilnej i mieć pewność, że jego kod
się nie zepsuje. Stabilność bez stagnacji.

Ta książka zawiera wyłącznie informacje o funkcjonalnościach stabilnych,
ponieważ funkcjonalności w trakcie rozwoju wciąż się zmieniają i z pewnością
będą wyglądać inaczej w chwili, gdy zostaną włączone w stabilnych kompilacjach,
niż w chwili pisania tej książki. Dokumentację funkcjonalności dostępnych
wyłącznie w nightly znajdziesz w internecie.

### Rustup i rola Rusta nightly {#rustup-and-the-role-of-rust-nightly}

Rustup ułatwia przełączanie się między różnymi kanałami wydań Rusta, globalnie
lub osobno dla każdego projektu. Domyślnie masz zainstalowanego stabilnego
Rusta. Aby zainstalować na przykład wersję nightly, wpisz:

```console
$ rustup toolchain install nightly
```

Za pomocą `rustup` możesz też wyświetlić wszystkie zainstalowane _zestawy
narzędzi_ (*toolchains*, czyli wydania Rusta wraz z powiązanymi komponentami).
Oto przykład z komputera z systemem Windows jednego z autorów:

```powershell
> rustup toolchain list
stable-x86_64-pc-windows-msvc (default)
beta-x86_64-pc-windows-msvc
nightly-x86_64-pc-windows-msvc
```

Jak widać, domyślny jest stabilny zestaw narzędzi. Większość użytkowników Rusta
przez większość czasu używa wersji stabilnej. Możesz chcieć przez większość
czasu używać wersji stabilnej, ale w konkretnym projekcie korzystać z nightly,
bo zależy ci na najnowszej funkcjonalności. W tym celu możesz użyć
`rustup override` w katalogu tego projektu, aby ustawić zestaw narzędzi nightly
jako ten, którego `rustup` ma używać, gdy jesteś w tym katalogu:

```console
$ cd ~/projects/needs-nightly
$ rustup override set nightly
```

Teraz za każdym razem, gdy wywołasz `rustc` lub `cargo` wewnątrz
_~/projects/needs-nightly_, `rustup` zadba o to, aby używany był Rust nightly,
a nie domyślny stabilny Rust. Przydaje się to, gdy masz wiele projektów w
Ruście!

### Proces RFC i zespoły {#the-rfc-process-and-teams}

Jak więc dowiedzieć się o tych nowych funkcjonalnościach? Model rozwoju Rusta
opiera się na _procesie RFC (Request For Comments)_. Jeśli chcesz, aby w Ruście
pojawiło się jakieś usprawnienie, możesz napisać propozycję, zwaną RFC.

Każdy może pisać RFC, aby ulepszyć Rusta, a propozycje są przeglądane i
omawiane przez zespół Rusta, który składa się z wielu podzespołów tematycznych.
Pełną listę zespołów znajdziesz [na stronie internetowej Rusta](https://www.rust-lang.org/governance); obejmuje ona zespoły
dla każdego obszaru projektu: projektowania języka, implementacji kompilatora,
infrastruktury, dokumentacji i innych. Odpowiedni zespół czyta propozycję i
komentarze, dodaje własne komentarze, a w końcu osiąga konsensus co do
przyjęcia lub odrzucenia funkcjonalności.

Jeśli funkcjonalność zostanie przyjęta, w repozytorium Rusta otwierane jest
zgłoszenie (*issue*) i ktoś może ją zaimplementować. Osoba, która ją
implementuje, wcale nie musi być tą samą osobą, która tę funkcjonalność
zaproponowała! Gdy implementacja jest gotowa, trafia do głównej gałęzi za
bramką funkcjonalności (*feature gate*), jak omówiliśmy w podrozdziale
[„Funkcjonalności niestabilne”](#unstable-features)<!-- ignore -->.

Po pewnym czasie, gdy programiści Rusta korzystający z wydań nightly zdążą
wypróbować nową funkcjonalność, członkowie zespołu omawiają ją i to, jak
sprawdziła się w nightly, a następnie decydują, czy powinna trafić do
stabilnego Rusta. Jeśli decyzja jest pozytywna, bramka funkcjonalności zostaje
usunięta, a funkcjonalność jest od tej chwili uznawana za stabilną! Wsiada do
pociągu i jedzie do nowego stabilnego wydania Rusta.

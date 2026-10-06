# Wprowadzenie {#introduction}

> Uwaga: to wydanie książki jest takie samo jak książka
> [The Rust Programming Language][nsprust] dostępna w wersji drukowanej i jako
> e-book w wydawnictwie [No Starch Press][nsp].

[nsprust]: https://nostarch.com/rust-programming-language-3rd-edition
[nsp]: https://nostarch.com/

Witaj w _The Rust Programming Language_, wprowadzającej książce o Ruście. Język
programowania Rust pomaga pisać szybsze i bardziej niezawodne oprogramowanie.
Wysokopoziomowa ergonomia i niskopoziomowa kontrola często stoją ze sobą
w sprzeczności przy projektowaniu języków programowania; Rust rzuca wyzwanie tej
sprzeczności. Dzięki zrównoważeniu dużych możliwości technicznych z wygodą pracy
programisty Rust daje ci kontrolę nad szczegółami niskiego poziomu (takimi jak
użycie pamięci) bez całego kłopotu, który tradycyjnie wiąże się z taką
kontrolą.

## Dla kogo jest Rust {#who-rust-is-for}

Rust jest idealny dla wielu osób z różnych powodów. Przyjrzyjmy się kilku
najważniejszym grupom.

### Zespoły programistów {#teams-of-developers}

Rust okazuje się produktywnym narzędziem do współpracy w dużych zespołach
programistów o różnym poziomie wiedzy z zakresu programowania systemowego. Kod
niskiego poziomu jest podatny na rozmaite subtelne błędy, które w większości
innych języków można wychwycić tylko dzięki rozbudowanym testom i starannemu
przeglądowi kodu przez doświadczonych programistów. W Ruście kompilator pełni
rolę strażnika: odmawia skompilowania kodu z takimi trudnymi do wykrycia
błędami, w tym z błędami współbieżności (*concurrency*). Współpracując
z kompilatorem, zespół może poświęcić czas na logikę programu, zamiast tropić
błędy.

Rust wnosi też do świata programowania systemowego nowoczesne narzędzia dla
programistów:

- Cargo, dołączony menedżer zależności i narzędzie do budowania, sprawia, że
  dodawanie, kompilowanie i zarządzanie zależnościami jest bezbolesne i spójne
  w całym ekosystemie Rusta.
- Narzędzie do formatowania `rustfmt` zapewnia spójny styl kodu u wszystkich
  programistów.
- Rust Language Server zapewnia integrację ze zintegrowanymi środowiskami
  programistycznymi (IDE), dostarczając podpowiedzi kodu i komunikaty o błędach
  bezpośrednio w edytorze.

Dzięki tym i innym narzędziom z ekosystemu Rusta programiści mogą pracować
produktywnie, pisząc kod na poziomie systemowym.

### Studenci {#students}

Rust jest dla studentów i wszystkich, którzy chcą poznać zagadnienia
systemowe. Z pomocą Rusta wiele osób zgłębiło takie tematy jak tworzenie
systemów operacyjnych. Społeczność jest bardzo przyjazna i chętnie odpowiada na
pytania studentów. Poprzez inicjatywy takie jak ta książka zespoły Rusta chcą
udostępnić zagadnienia systemowe większej liczbie osób, zwłaszcza tym, które
dopiero zaczynają programować.

### Firmy {#companies}

Setki firm, dużych i małych, używają Rusta produkcyjnie do rozmaitych zadań,
w tym do narzędzi wiersza poleceń, usług sieciowych, narzędzi DevOps, urządzeń
wbudowanych, analizy i transkodowania audio i wideo, kryptowalut,
bioinformatyki, wyszukiwarek, aplikacji Internetu rzeczy, uczenia maszynowego,
a nawet dużych części przeglądarki Firefox.

### Twórcy open source {#open-source-developers}

Rust jest dla osób, które chcą rozwijać język programowania Rust, jego
społeczność, narzędzia programistyczne i biblioteki. Chętnie przyjmiemy twój
wkład w rozwój języka Rust.

### Osoby, które cenią szybkość i stabilność {#people-who-value-speed-and-stability}

Rust jest dla osób, które oczekują od języka szybkości i stabilności. Przez
szybkość rozumiemy zarówno to, jak szybko może działać kod w Ruście, jak i to,
jak szybko Rust pozwala pisać programy. Mechanizmy sprawdzające kompilatora
Rusta zapewniają stabilność przy dodawaniu nowych funkcji i refaktoryzacji. To
przeciwieństwo kruchego, zastanego kodu w językach bez takich mechanizmów, którego
programiści często boją się modyfikować. Dążąc do abstrakcji o zerowym koszcie
(*zero-cost abstractions*) – funkcji wyższego poziomu, które kompilują się do
kodu niższego poziomu równie szybkiego jak kod napisany ręcznie – Rust stara
się, by bezpieczny kod był zarazem szybkim kodem.

Rust chce służyć również wielu innym użytkownikom; wymienione
tu grupy to tylko niektórzy z największych interesariuszy. Ogólnie rzecz
biorąc, największą ambicją Rusta jest wyeliminowanie kompromisów, które
programiści akceptowali od dziesięcioleci, przez zapewnienie bezpieczeństwa _i_
produktywności, szybkości _i_ ergonomii. Wypróbuj Rusta i sprawdź, czy jego
rozwiązania ci odpowiadają.

## Dla kogo jest ta książka {#who-this-book-is-for}

Ta książka zakłada, że masz już za sobą pisanie kodu w innym języku
programowania, ale nie zakłada, w którym. Staraliśmy się, aby materiał był
przystępny dla osób o bardzo różnym doświadczeniu programistycznym. Nie
poświęcamy wiele czasu na omawianie tego, czym _jest_ programowanie ani jak
o nim myśleć. Jeśli programowanie jest dla ciebie zupełną nowością, lepiej
sięgnąć po książkę, która stanowi wprowadzenie do programowania.

## Jak korzystać z tej książki {#how-to-use-this-book}

Ogólnie ta książka zakłada, że czytasz ją po kolei, od początku do końca.
Późniejsze rozdziały opierają się na pojęciach z wcześniejszych, a wcześniejsze
rozdziały mogą nie zagłębiać się w szczegóły danego tematu, tylko wrócić do
niego w którymś z późniejszych rozdziałów.

W tej książce znajdziesz dwa rodzaje rozdziałów: rozdziały koncepcyjne
i rozdziały projektowe. W rozdziałach koncepcyjnych poznasz jakiś aspekt Rusta.
W rozdziałach projektowych wspólnie napiszemy małe programy, stosując to, czego
udało ci się do tej pory nauczyć. Rozdziały 2, 12 i 21 są projektowe; pozostałe
są koncepcyjne.

**Rozdział 1** wyjaśnia, jak zainstalować Rusta, jak napisać program
„Hello, world!” i jak używać Cargo, menedżera pakietów i systemu budowania
Rusta. **Rozdział 2** to praktyczne wprowadzenie do pisania programu w Ruście,
w którym zbudujesz grę w zgadywanie liczby. Omawiamy tam pojęcia ogólnie,
a późniejsze rozdziały dostarczą więcej szczegółów. Jeśli chcesz od razu
zakasać rękawy, rozdział 2 jest do tego właściwym miejscem. Jeśli zaś należysz
do szczególnie skrupulatnych osób, które wolą poznać każdy szczegół, zanim
przejdą dalej, możesz pominąć rozdział 2 i przejść od razu do **rozdziału 3**,
który omawia te elementy Rusta, które są podobne do elementów innych języków
programowania; potem możesz wrócić do rozdziału 2, gdy zechcesz popracować nad
projektem, stosując poznane szczegóły.

W **rozdziale 4** poznasz system własności (*ownership*) w Ruście. **Rozdział
5** omawia struktury (*struct*) i metody. **Rozdział 6** obejmuje *enum* (typ
wyliczeniowy), wyrażenia `match` oraz konstrukcje sterujące `if let`
i `let...else`. Struktur i enumów będziesz używać do tworzenia własnych typów.

W **rozdziale 7** poznasz system modułów Rusta oraz zasady prywatności służące
do organizowania kodu i jego publicznego interfejsu programistycznego
aplikacji (API). **Rozdział 8** omawia kilka popularnych struktur danych typu
kolekcja, które dostarcza biblioteka standardowa: wektory, łańcuchy znaków
(*string*) i mapy haszujące (*hash map*). **Rozdział 9** przedstawia filozofię
i techniki obsługi błędów w Ruście.

**Rozdział 10** zagłębia się w typy generyczne (*generics*), *traity* (cechy
typów, zbliżone do interfejsów) i czasy życia (*lifetime*), które pozwalają
definiować kod działający dla wielu typów. **Rozdział 11** w całości dotyczy
testowania, które nawet przy gwarancjach bezpieczeństwa Rusta jest niezbędne,
by upewnić się, że logika programu jest poprawna. W **rozdziale 12** napiszemy
własną implementację części funkcjonalności narzędzia wiersza poleceń `grep`,
które wyszukuje tekst w plikach. Wykorzystamy w tym celu wiele pojęć omówionych
w poprzednich rozdziałach.

**Rozdział 13** omawia domknięcia (*closure*) i iteratory: elementy Rusta
wywodzące się z funkcyjnych języków programowania. W **rozdziale 14** przyjrzymy
się dokładniej Cargo i omówimy dobre praktyki udostępniania bibliotek innym.
**Rozdział 15** omawia inteligentne wskaźniki (*smart pointer*) dostarczane
przez bibliotekę standardową oraz traity, które umożliwiają ich działanie.

W **rozdziale 16** przejdziemy przez różne modele programowania współbieżnego
i omówimy, jak Rust pomaga bez obaw programować z użyciem wielu wątków.
W **rozdziale 17** rozwijamy ten temat, omawiając składnię async i await
w Ruście, a także zadania, *future* (wartość, która będzie gotowa później),
strumienie (*stream*) i lekki model współbieżności, który umożliwiają.

**Rozdział 18** pokazuje, jak idiomy Rusta mają się do znanych ci być może zasad
programowania obiektowego. **Rozdział 19** to kompendium wiedzy o wzorcach
i dopasowywaniu wzorców (*pattern matching*), czyli potężnych sposobach
wyrażania idei w programach w Ruście. **Rozdział 20** zawiera mieszankę
interesujących zagadnień zaawansowanych, w tym niebezpieczny Rust (*unsafe
Rust*), makra oraz więcej informacji o czasach życia, traitach, typach,
funkcjach i domknięciach.

W **rozdziale 21** zrealizujemy projekt, w którym zaimplementujemy
niskopoziomowy, wielowątkowy serwer WWW!

Na koniec kilka dodatków zawiera przydatne informacje o języku w formie
bardziej zbliżonej do dokumentacji. **Dodatek A** omawia słowa kluczowe Rusta,
**dodatek B** – operatory i symbole Rusta, **dodatek C** – traity, które można
wyprowadzić (*derive*), dostarczane przez bibliotekę standardową, **dodatek D**
– kilka przydatnych narzędzi programistycznych, a **dodatek E** wyjaśnia, czym
są edycje (*edition*) Rusta. W **dodatku F** znajdziesz tłumaczenia książki,
a w **dodatku G** opiszemy, jak powstaje Rust i czym jest Rust nightly.

Nie ma złego sposobu czytania tej książki: jeśli chcesz przeskoczyć dalej,
śmiało! Jeśli coś okaże się niejasne, być może trzeba będzie wrócić do
wcześniejszych rozdziałów. Rób jednak to, co ci odpowiada.

<span id="ferris"></span>

Ważną częścią nauki Rusta jest nauczenie się czytania komunikatów o błędach
wyświetlanych przez kompilator: to one poprowadzą cię do działającego kodu.
Dlatego pokażemy wiele przykładów, które się nie kompilują, razem z komunikatem
o błędzie, jaki kompilator wyświetli w każdej z tych sytuacji. Pamiętaj, że
jeśli wpiszesz i uruchomisz losowy przykład, może się on nie skompilować!
Koniecznie przeczytaj otaczający tekst, aby sprawdzić, czy przykład, który
próbujesz uruchomić, ma kończyć się błędem. W większości przypadków
doprowadzimy cię do poprawnej wersji każdego kodu, który się nie kompiluje.
Ferris pomoże ci też odróżnić kod, który nie ma działać:

| Ferris                                                                                                           | Znaczenie                                        |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| <img src="img/ferris/does_not_compile.svg" class="ferris-explain" alt="Ferris ze znakiem zapytania"/>            | Ten kod się nie kompiluje!                       |
| <img src="img/ferris/panics.svg" class="ferris-explain" alt="Ferris wyrzucający ręce w górę"/>                   | Ten kod panikuje!                                |
| <img src="img/ferris/not_desired_behavior.svg" class="ferris-explain" alt="Ferris z jednymi szczypcami w górze, wzruszający ramionami"/> | Ten kod nie działa zgodnie z oczekiwaniami. |

W większości przypadków doprowadzimy cię do poprawnej wersji każdego kodu,
który się nie kompiluje.

## Kod źródłowy {#source-code}

Pliki źródłowe, z których generowana jest ta książka, znajdziesz na
[GitHubie][book].

[book]: https://github.com/rust-lang/book/tree/main/src

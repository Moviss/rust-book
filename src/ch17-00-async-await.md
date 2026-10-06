# Podstawy programowania asynchronicznego: async, await, future’y i strumienie {#fundamentals-of-asynchronous-programming-async-await-futures-and-streams}

Wiele operacji, które zlecamy komputerowi, może trwać dość długo. Dobrze by
było, gdybyśmy mogli robić coś innego, czekając na zakończenie tych
długotrwałych procesów. Współczesne komputery oferują dwie techniki pracy nad
więcej niż jedną operacją naraz: równoległość (*parallelism*) i współbieżność
(*concurrency*). Logikę naszych programów piszemy jednak w sposób w większości
liniowy. Chcielibyśmy móc określić operacje, które program ma wykonać, oraz
miejsca, w których funkcja mogłaby się wstrzymać, a zamiast niej mogłaby
działać inna część programu – bez konieczności ustalania z góry, w jakiej
dokładnie kolejności i w jaki sposób ma się wykonać każdy fragment kodu.
_Programowanie asynchroniczne_ (*asynchronous programming*) to abstrakcja,
która pozwala wyrażać kod w kategoriach potencjalnych punktów wstrzymania i
wyników dostępnych w przyszłości, a szczegółami koordynacji zajmuje się za nas.

Ten rozdział rozwija wykorzystanie wątków do równoległości i współbieżności z
rozdziału 16, przedstawiając alternatywne podejście do pisania kodu: *future*’y
(wartości, które będą gotowe później) i strumienie (*stream*) w Ruście,
składnię `async` i `await`, która pozwala wyrazić, że operacje mogą być
asynchroniczne, oraz zewnętrzne *crate*’y (jednostki kompilacji w Ruście)
implementujące asynchroniczne środowiska uruchomieniowe (*runtime*), czyli kod,
który zarządza wykonywaniem operacji asynchronicznych i je koordynuje.

Rozważmy przykład. Załóżmy, że eksportujesz nagrany przez siebie film z
rodzinnej uroczystości – operacja ta może trwać od kilku minut do kilku godzin.
Eksport wideo wykorzysta tyle mocy procesora (CPU) i karty graficznej (GPU), ile
tylko zdoła. Gdyby twój komputer miał tylko jeden rdzeń procesora, a system
operacyjny nie przerywał eksportu aż do jego zakończenia – czyli gdyby
wykonywał eksport _synchronicznie_ – nie dałoby się robić na komputerze niczego
innego, dopóki to zadanie by trwało. Byłoby to dość frustrujące. Na szczęście
system operacyjny twojego komputera potrafi – i tak właśnie robi – niezauważalnie
przerywać eksport na tyle często, że w tym samym czasie możesz wykonywać inną
pracę.

Teraz załóżmy, że pobierasz film udostępniony przez kogoś innego. To również
może chwilę potrwać, ale nie zajmuje tyle czasu procesora. W tym przypadku
procesor musi czekać, aż dane nadejdą z sieci. Co prawda możesz zacząć odczytywać
dane, gdy tylko zaczną napływać, ale zanim pojawią się wszystkie, może minąć
trochę czasu. Nawet gdy wszystkie dane są już na miejscu, wczytanie ich w
całości – jeśli film jest dość duży – może zająć co najmniej sekundę lub dwie.
Może to nie brzmieć jak wiele, ale dla współczesnego procesora, który potrafi
wykonać miliardy operacji na sekundę, to bardzo długo. I tym razem system
operacyjny niezauważalnie przerwie twój program, aby procesor mógł wykonywać
inną pracę, czekając na zakończenie wywołania sieciowego.

Eksport wideo to przykład operacji _ograniczonej przez procesor_ (*CPU-bound*)
lub _ograniczonej przez obliczenia_ (*compute-bound*). Ogranicza ją potencjalna
szybkość przetwarzania danych przez procesor lub kartę graficzną komputera oraz
to, jaką część tej szybkości można poświęcić tej operacji. Pobieranie wideo to
przykład operacji _ograniczonej przez wejście-wyjście_ (*I/O-bound*), ponieważ
ogranicza ją szybkość _wejścia i wyjścia_ komputera; może przebiegać tylko tak
szybko, jak szybko dane da się przesłać przez sieć.

W obu tych przykładach niezauważalne przerwania systemu operacyjnego zapewniają
pewną formę współbieżności. Ta współbieżność zachodzi jednak tylko na poziomie
całego programu: system operacyjny przerywa jeden program, aby inne programy
mogły wykonać swoją pracę. W wielu przypadkach, ponieważ rozumiemy nasze
programy znacznie dokładniej niż system operacyjny, możemy dostrzec okazje do
współbieżności, których system operacyjny nie widzi.

Jeśli na przykład budujemy narzędzie do zarządzania pobieraniem plików,
powinniśmy móc napisać program tak, aby rozpoczęcie jednego pobierania nie
blokowało interfejsu użytkownika, a użytkownicy mogli uruchomić wiele pobrań
jednocześnie. Wiele API systemu operacyjnego do komunikacji z siecią jest
jednak _blokujących_ (*blocking*), to znaczy wstrzymują one postęp programu, aż
przetwarzane przez nie dane będą w pełni gotowe.

> Uwaga: jeśli się nad tym zastanowić, tak właśnie działa _większość_ wywołań
> funkcji. Określenie _blokujący_ zwykle rezerwuje się jednak dla wywołań
> funkcji, które komunikują się z plikami, siecią lub innymi zasobami
> komputera, bo właśnie w takich przypadkach pojedynczy program zyskałby na
> tym, że operacja jest *nie*blokująca.

Moglibyśmy uniknąć blokowania wątku głównego, uruchamiając osobny wątek do
pobierania każdego pliku. Narzut zasobów systemowych zużywanych przez te wątki
stałby się jednak w końcu problemem. Lepiej byłoby, gdyby wywołanie w ogóle nie
blokowało, a zamiast tego moglibyśmy zdefiniować szereg zadań, które program ma
wykonać, i pozwolić środowisku uruchomieniowemu wybrać najlepszą kolejność i
sposób ich wykonania.

Dokładnie to daje nam w Ruście abstrakcja _async_ (skrót od _asynchronous_,
czyli asynchroniczny). W tym rozdziale dowiesz się wszystkiego o async;
omówimy następujące tematy:

- jak używać składni `async` i `await` w Ruście i wykonywać funkcje
  asynchroniczne za pomocą środowiska uruchomieniowego;
- jak użyć modelu async do rozwiązania niektórych z tych samych problemów, które
  omawialiśmy w rozdziale 16;
- jak wielowątkowość i async zapewniają uzupełniające się rozwiązania, które w
  wielu przypadkach można łączyć.

Zanim jednak zobaczymy, jak async działa w praktyce, musimy zrobić krótką
dygresję i omówić różnice między równoległością a współbieżnością.

## Równoległość i współbieżność {#parallelism-and-concurrency}

Dotąd traktowaliśmy równoległość i współbieżność jako w dużej mierze zamienne.
Teraz musimy rozróżnić je precyzyjniej, bo różnice dadzą o sobie znać, gdy
zabierzemy się do pracy.

Pomyśl o różnych sposobach, w jakie zespół mógłby podzielić pracę nad projektem
programistycznym. Możesz przydzielić jednej osobie wiele zadań, przydzielić
każdej osobie jedno zadanie albo połączyć oba podejścia.

Gdy jedna osoba pracuje nad kilkoma różnymi zadaniami, zanim którekolwiek z
nich zostanie ukończone, jest to _współbieżność_. Jeden ze sposobów realizacji
współbieżności przypomina sytuację, w której masz na komputerze pobrane dwa
różne projekty, a gdy jeden cię znudzi albo utkniesz, przełączasz się na drugi.
Jesteś tylko jedną osobą, więc nie możesz posuwać naprzód obu zadań dokładnie w
tym samym czasie, ale możesz pracować wielozadaniowo, robiąc postępy w jednym
zadaniu naraz i przełączając się między nimi (zob. rysunek 17-1).

<figure>

<img src="img/trpl17-01.svg" class="center" alt="Diagram z ułożonymi jeden pod drugim prostokątami podpisanymi Task A i Task B, zawierającymi romby oznaczające podzadania. Strzałki prowadzą od A1 do B1, od B1 do A2, od A2 do B2, od B2 do A3, od A3 do A4 i od A4 do B3. Strzałki między podzadaniami przechodzą między prostokątami Task A i Task B." />

<figcaption>Rysunek 17-1: Współbieżny przebieg pracy z przełączaniem między zadaniem A a zadaniem B</figcaption>

</figure>

Gdy zespół dzieli grupę zadań w ten sposób, że każda osoba bierze jedno zadanie
i pracuje nad nim sama, jest to _równoległość_. Każda osoba w zespole może robić
postępy dokładnie w tym samym czasie (zob. rysunek 17-2).

<figure>

<img src="img/trpl17-02.svg" class="center" alt="Diagram z ułożonymi jeden pod drugim prostokątami podpisanymi Task A i Task B, zawierającymi romby oznaczające podzadania. Strzałki prowadzą od A1 do A2, od A2 do A3, od A3 do A4, od B1 do B2 i od B2 do B3. Żadne strzałki nie przechodzą między prostokątami Task A i Task B." />

<figcaption>Rysunek 17-2: Równoległy przebieg pracy, w którym praca nad zadaniem A i zadaniem B odbywa się niezależnie</figcaption>

</figure>

W obu tych przebiegach pracy może być konieczna koordynacja między różnymi
zadaniami. Może ci się wydawało, że zadanie przydzielone jednej osobie jest
całkowicie niezależne od pracy wszystkich pozostałych, a w rzeczywistości
wymaga, aby inna osoba z zespołu najpierw ukończyła swoje zadanie. Część pracy dało się wykonać
równolegle, ale część była w istocie _sekwencyjna_: mogła się odbywać tylko po
kolei, jedno zadanie po drugim, jak na rysunku 17-3.

<figure>

<img src="img/trpl17-03.svg" class="center" alt="Diagram z ułożonymi jeden pod drugim prostokątami podpisanymi Task A i Task B, zawierającymi romby oznaczające podzadania. W zadaniu A strzałki prowadzą od A1 do A2, od A2 do pary grubych pionowych kresek przypominających symbol „pauzy” i od tego symbolu do A3. W zadaniu B strzałki prowadzą od B1 do B2, od B2 do B3, od B3 do A3 i od B3 do B4." />

<figcaption>Rysunek 17-3: Częściowo równoległy przebieg pracy, w którym praca nad zadaniem A i zadaniem B odbywa się niezależnie, dopóki zadanie A3 nie zostanie zablokowane w oczekiwaniu na wyniki zadania B3.</figcaption>

</figure>

Podobnie możesz zauważyć, że jedno z twoich zadań zależy od innego twojego
zadania. Wtedy twoja współbieżna praca również staje się sekwencyjna.

Równoległość i współbieżność mogą się też przenikać. Jeśli dowiesz się, że
ktoś z zespołu utknął i czeka, aż skończysz jedno ze swoich zadań,
prawdopodobnie skupisz wszystkie wysiłki na tym zadaniu, aby tę osobę
„odblokować”. Ty i ta osoba nie możecie już wtedy pracować równolegle, a ty
nie możesz już też pracować współbieżnie nad własnymi zadaniami.

Te same podstawowe mechanizmy działają w przypadku oprogramowania i sprzętu. Na
maszynie z jednym rdzeniem procesora procesor może wykonywać tylko jedną
operację naraz, ale nadal może pracować współbieżnie. Dzięki narzędziom takim
jak wątki, procesy i async komputer może wstrzymać jedną czynność i przełączyć
się na inne, by w końcu wrócić do tej pierwszej. Na maszynie z wieloma rdzeniami
procesora może też wykonywać pracę równolegle. Jeden rdzeń może wykonywać jedno
zadanie, podczas gdy inny rdzeń wykonuje zupełnie z nim niezwiązane, a te
operacje faktycznie zachodzą w tym samym czasie.

Kod asynchroniczny w Ruście zwykle wykonuje się współbieżnie. W zależności od
sprzętu, systemu operacyjnego i używanego asynchronicznego środowiska
uruchomieniowego (więcej o nich za chwilę) ta współbieżność może pod spodem
wykorzystywać także równoległość.

Przejdźmy teraz do tego, jak naprawdę działa programowanie asynchroniczne w
Ruście.

# Nieustraszona współbieżność {#fearless-concurrency}

Bezpieczna i wydajna obsługa programowania współbieżnego to kolejny z głównych
celów Rusta. _Programowanie współbieżne_ (*concurrent programming*), w którym
różne części programu wykonują się niezależnie od siebie, oraz _programowanie
równoległe_ (*parallel programming*), w którym różne części programu wykonują
się w tym samym czasie, zyskują na znaczeniu, w miarę jak coraz więcej
komputerów korzysta z wielu procesorów. Programowanie w tych warunkach było
dotąd trudne i podatne na błędy. Rust ma nadzieję to zmienić.

Początkowo zespół Rusta uważał, że zapewnienie bezpieczeństwa pamięci i
zapobieganie problemom ze współbieżnością (*concurrency*) to dwa odrębne
wyzwania, które trzeba rozwiązywać różnymi metodami. Z czasem zespół odkrył, że
systemy własności (*ownership*) i typów stanowią potężny zestaw narzędzi
pomagających radzić sobie z problemami zarówno bezpieczeństwa pamięci, _jak i_
współbieżności! Dzięki wykorzystaniu własności i sprawdzania typów wiele błędów
współbieżności w Ruście to błędy wykrywane w czasie kompilacji (*compile-time*),
a nie w czasie działania. Nie musisz więc spędzać mnóstwa czasu na próbach
odtworzenia dokładnych okoliczności, w których występuje błąd współbieżności w
czasie działania: niepoprawny kod po prostu się nie skompiluje, a kompilator
wyświetli błąd wyjaśniający problem. W rezultacie możesz poprawić kod jeszcze w
trakcie pracy nad nim, a nie dopiero po wdrożeniu go na produkcję. Ten aspekt
Rusta nazwaliśmy _nieustraszoną współbieżnością_ (*fearless concurrency*).
Nieustraszona współbieżność pozwala pisać kod wolny od subtelnych błędów i łatwy
do refaktoryzacji bez wprowadzania nowych błędów.

> Uwaga: dla uproszczenia wiele problemów będziemy nazywać _współbieżnymi_,
> zamiast precyzyjniej mówić _współbieżne i/lub równoległe_. W tym rozdziale w
> myślach zastępuj słowo _współbieżny_ wyrażeniem _współbieżny i/lub
> równoległy_. W następnym rozdziale, w którym to rozróżnienie ma większe
> znaczenie, będziemy bardziej precyzyjni.

Wiele języków dogmatycznie podchodzi do oferowanych rozwiązań problemów
współbieżności. Na przykład Erlang ma eleganckie mechanizmy współbieżności
opartej na przekazywaniu komunikatów (*message passing*), ale tylko mało
przejrzyste sposoby współdzielenia stanu między wątkami. Obsługa tylko
podzbioru możliwych rozwiązań to rozsądna strategia dla języków wyższego
poziomu, ponieważ język wyższego poziomu obiecuje korzyści płynące z oddania
części kontroli w zamian za abstrakcje. Od języków niższego poziomu oczekuje
się jednak, że w każdej sytuacji zapewnią rozwiązanie o najlepszej wydajności i
będą miały mniej abstrakcji nad sprzętem. Dlatego Rust oferuje różnorodne
narzędzia do modelowania problemów w sposób odpowiedni dla twojej sytuacji i
wymagań.

Oto tematy, które omówimy w tym rozdziale:

- tworzenie wątków, aby uruchamiać wiele fragmentów kodu jednocześnie;
- współbieżność oparta na _przekazywaniu komunikatów_, w której kanały
  przesyłają komunikaty między wątkami;
- współbieżność ze _współdzielonym stanem_ (*shared state*), w której wiele
  wątków ma dostęp do tych samych danych;
- *traity* (cechy typów, zbliżone do interfejsów) `Sync` i `Send`, które
  rozszerzają gwarancje współbieżności Rusta na typy zdefiniowane przez
  użytkownika, a także na typy z biblioteki standardowej.

# Inteligentne wskaźniki {#smart-pointers}

Wskaźnik to ogólne pojęcie oznaczające zmienną, która zawiera adres w pamięci.
Ten adres odnosi się do innych danych – „wskazuje” na nie. Najczęściej używanym
rodzajem wskaźnika w Ruście jest referencja (*reference*), omówiona w
rozdziale 4. Referencje oznaczamy symbolem `&`; pożyczają one wartość, na którą
wskazują. Poza odnoszeniem się do danych nie mają żadnych specjalnych
możliwości i nie wiąże się z nimi żaden narzut.

Z kolei _inteligentne wskaźniki_ (*smart pointers*) to struktury danych, które
zachowują się jak wskaźnik, ale mają też dodatkowe metadane i możliwości.
Koncepcja inteligentnych wskaźników nie jest unikalna dla Rusta: wywodzą się
one z C++ i istnieją także w innych językach. Rust ma w bibliotece
standardowej wiele inteligentnych wskaźników, które dają możliwości wykraczające
poza to, co oferują referencje. Aby zbadać tę ogólną koncepcję, przyjrzymy się
kilku przykładom inteligentnych wskaźników, w tym typowi inteligentnego
wskaźnika ze _zliczaniem referencji_ (*reference counting*). Taki wskaźnik
pozwala danym mieć wielu właścicieli: śledzi ich liczbę, a gdy nie zostaje już
żaden właściciel, sprząta dane.

W Ruście, z jego koncepcją własności (*ownership*) i pożyczania (*borrowing*),
referencje i inteligentne wskaźniki różnią się jeszcze w jednym: referencje
tylko pożyczają dane, a inteligentne wskaźniki w wielu przypadkach _są
właścicielami_ danych, na które wskazują.

Inteligentne wskaźniki są zwykle implementowane za pomocą struktur (*struct*).
W odróżnieniu od zwykłej struktury inteligentne wskaźniki implementują
*traity* (cechy typu, zbliżone do interfejsu) `Deref` i `Drop`. Trait `Deref`
pozwala instancji struktury inteligentnego wskaźnika zachowywać się jak
referencja, dzięki czemu możesz pisać kod działający zarówno z referencjami,
jak i z inteligentnymi wskaźnikami. Trait `Drop` pozwala dostosować kod
uruchamiany wtedy, gdy instancja inteligentnego wskaźnika wychodzi poza zasięg
(*scope*). W tym rozdziale omówimy oba te traity i pokażemy, dlaczego są ważne
dla inteligentnych wskaźników.

Wzorzec inteligentnego wskaźnika jest ogólnym wzorcem projektowym, często
używanym w Ruście, więc ten rozdział nie obejmie wszystkich istniejących
inteligentnych wskaźników. Wiele bibliotek ma własne inteligentne wskaźniki, a
możesz nawet napisać własne. Omówimy najczęściej używane inteligentne wskaźniki
z biblioteki standardowej:

- `Box<T>` – do alokowania wartości na stercie (*heap*);
- `Rc<T>` – typ ze zliczaniem referencji, który umożliwia współwłasność;
- `Ref<T>` i `RefMut<T>`, dostępne przez `RefCell<T>` – typ, który egzekwuje
  reguły pożyczania w czasie działania zamiast w czasie kompilacji.

Ponadto omówimy wzorzec _wewnętrznej mutowalności_ (*interior mutability*), w
którym niemutowalny (*immutable*) typ udostępnia API do modyfikowania wartości
znajdującej się w jego wnętrzu. Omówimy też cykle referencji: jak mogą
powodować wycieki pamięci i jak im zapobiegać.

Zaczynajmy!

<!-- Old headings. Do not remove or links may break. -->

<a id="comparing-performance-loops-vs-iterators"></a>

## Wydajność pętli i iteratorów {#performance-in-loops-vs-iterators}

Aby zdecydować, czy używać pętli, czy iteratorów, musisz wiedzieć, która
implementacja jest szybsza: wersja funkcji `search` z jawną pętlą `for` czy
wersja z iteratorami.

Przeprowadziliśmy test wydajności (*benchmark*), wczytując całą treść _Przygód
Sherlocka Holmesa_ sir Arthura Conana Doyle’a do wartości `String` i szukając w
niej słowa _the_. Oto wyniki testu wydajności dla wersji `search` z pętlą `for`
i wersji z iteratorami:

```text
test bench_search_for  ... bench:  19,620,300 ns/iter (+/- 915,700)
test bench_search_iter ... bench:  19,234,900 ns/iter (+/- 657,200)
```

Obie implementacje mają podobną wydajność! Nie będziemy tu objaśniać kodu testu
wydajności, bo nie chodzi o to, by udowodnić, że obie wersje są równoważne, ale
by zorientować się ogólnie, jak te dwie implementacje wypadają pod względem
wydajności.

W bardziej wszechstronnym teście wydajności warto sprawdzić różne teksty o
różnych rozmiarach jako `contents`, różne słowa i słowa o różnej długości jako
`query` oraz wszelkie inne warianty. Chodzi o to, że iteratory, choć są
wysokopoziomową abstrakcją, kompilują się do mniej więcej takiego samego kodu,
jaki napisałbyś samodzielnie na niższym poziomie. Iteratory to jedna z
_abstrakcji o zerowym koszcie_ (*zero-cost abstractions*) w Ruście, co oznacza,
że użycie tej abstrakcji nie nakłada żadnego dodatkowego narzutu w czasie
działania. Jest to analogiczne do tego, jak Bjarne Stroustrup, pierwotny
projektant i twórca implementacji C++, definiuje zasadę zerowego narzutu
(*zero-overhead*) w swoim wykładzie „Foundations of C++” wygłoszonym na
konferencji ETAPS w 2012 roku:

> Ogólnie implementacje C++ przestrzegają zasady zerowego narzutu: za to, czego
> nie używasz, nie płacisz. A ponadto: tego, czego używasz, nie dałoby się
> lepiej napisać ręcznie.

W wielu przypadkach kod w Ruście używający iteratorów kompiluje się do takiego
samego kodu asemblera, jaki napisałbyś ręcznie. Optymalizacje takie jak
rozwijanie pętli i eliminowanie sprawdzania granic przy dostępie do tablicy
zostają zastosowane i sprawiają, że wynikowy kod jest niezwykle wydajny. Skoro
już to wiesz, możesz bez obaw używać iteratorów i domknięć (*closures*)!
Sprawiają, że kod wygląda na bardziej wysokopoziomowy, ale nie wiąże się to z
utratą wydajności w czasie działania.

## Podsumowanie {#summary}

Domknięcia i iteratory to mechanizmy Rusta inspirowane ideami z funkcyjnych
języków programowania. Przyczyniają się do tego, że Rust potrafi jasno wyrażać
wysokopoziomowe idee przy wydajności typowej dla kodu niskopoziomowego.
Domknięcia i iteratory są zaimplementowane tak, by nie wpływały na wydajność w
czasie działania. To część dążenia Rusta do zapewniania abstrakcji o zerowym
koszcie.

Skoro poprawiliśmy wyrazistość naszego projektu wejścia/wyjścia, przyjrzyjmy
się kolejnym mechanizmom `cargo`, które pomogą nam udostępnić projekt światu.

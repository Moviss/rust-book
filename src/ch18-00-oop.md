# Mechanizmy programowania obiektowego {#object-oriented-programming-features}

<!-- Old headings. Do not remove or links may break. -->

<a id="object-oriented-programming-features-of-rust"></a>

Programowanie obiektowe (OOP) to jeden ze sposobów modelowania programów.
Obiekty jako pojęcie programistyczne pojawiły się w języku Simula w latach 60.
XX wieku. Zainspirowały one architekturę programów Alana Kaya, w której obiekty
przekazują sobie nawzajem komunikaty. Na określenie tej architektury Kay ukuł
w 1967 roku termin _programowanie obiektowe_ (*object-oriented programming*).
Istnieje wiele konkurujących ze sobą definicji OOP; według niektórych z nich
Rust jest językiem obiektowym, a według innych nie. W tym rozdziale przyjrzymy
się pewnym cechom powszechnie uważanym za obiektowe i temu, jak przekładają się
one na idiomatyczny Rust. Następnie pokażemy, jak zaimplementować w Ruście
obiektowy wzorzec projektowy, i omówimy kompromisy takiego podejścia w
porównaniu z rozwiązaniem wykorzystującym mocne strony Rusta.

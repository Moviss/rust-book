# Czym ta książka się różni? {#whats-different-about-this-book}

<div style="display: flex; gap: 2em"> 

Ta książka jest eksperymentalnym forkiem [*The Rust Programming Language*](http://doc.rust-lang.org/book/), stworzonym przez badaczy z <a href="https://cel.cs.brown.edu/">Cognitive Engineering Lab</a> na Uniwersytecie Browna. Jeśli cię to ciekawi, na tej stronie wyjaśniamy, czym ta książka różni się od oryginalnej TRPL. Jeśli jednak chcesz po prostu zacząć naukę Rusta, możesz śmiało pominąć tę stronę i wrócić do niej później.

<div style="display: flex; flex-direction: column; justify-content: center">
  <img src="img/experiment/brown-logo.png" style="min-width: 150px" />
</div>

</div>


## Elementy interaktywne {#interactive-mechanics}

Ta książka wprowadza mechanizmy, dzięki którym podczas nauki aktywnie pracujesz z Rustem. Po pierwsze, zobaczysz quizy takie jak ten poniżej. Wypróbuj go, klikając „Start”.

{{#quiz ../quizzes/example-quiz.toml}}

Jeśli odpowiesz na pytanie błędnie, możesz albo rozwiązać quiz ponownie, albo zobaczyć poprawne odpowiedzi. Zachęcamy do ponawiania quizu, aż zdobędziesz 100% – przed kolejną próbą możesz śmiało wrócić do treści. Pamiętaj, że po wyświetleniu poprawnych odpowiedzi nie można już ponowić quizu.

Po drugie, możesz dodawać adnotacje do dowolnego fragmentu tekstu, aby zapisać swoje przemyślenia na jego temat. Gdy zaznaczysz tekst, kliknij przycisk ✏️ i opcjonalnie zostaw komentarz.

👉 Spróbuj zaznaczyć ten tekst! 👈

> **Uwaga:** twoje zaznaczenia znikną, jeśli zmienimy treść, którą zaznaczono. Zaznaczenia są też przechowywane w pliku cookie. Jeśli blokujesz pliki cookie albo zmienisz przeglądarkę, nie zobaczysz wcześniejszych zaznaczeń.

## Zmiany w treści {#content-changes}

Treść tej książki jest w większości podobna do TRPL, a obie książki synchronizujemy co kilka miesięcy. Największa różnica dotyczy rozdziału [Zrozumienie własności][understanding-ownership]. Ta książka wyjaśnia własność (*ownership*) za pomocą pojęć i wizualizacji, które – jak wykazały nasze badania – lepiej niż oryginalna książka pomagają zrozumieć Rusta. Zobaczysz wiele diagramów takich jak poniższe, które za pomocą narzędzia [Aquascope][aquascope] przedstawiają zachowanie Rusta w czasie kompilacji (*compile-time*) i w czasie działania (*run-time*):

```aquascope,interpreter,horizontal
#fn main() {
let mut s = String::from("Hello world");`[]`
let hello = &s[0..5];`[]`
s.push_str("!");`[]`
drop(s);`[]`
#}
```

Poza własnością wprowadziliśmy w książce wiele drobnych poprawek, które mają rozprawić się z błędnymi wyobrażeniami zaobserwowanymi w odpowiedziach na quizy. Jeśli zauważysz problem w quizie albo w innej części książki, możesz zgłosić go w naszym repozytorium na GitHubie: <https://github.com/cognitive-engineering-lab/rust-book>

_Chcesz wziąć udział w innych eksperymentach, które mają ułatwić naukę i używanie Rusta? Zapisz się tutaj:_ <https://forms.gle/U3jEUkb2fGXykp1DA>


## Publikacje {#publications}

Do tej pory eksperyment zaowocował dwiema publikacjami w otwartym dostępie. Zajrzyj do nich, jeśli chcesz poznać badania naukowe, na których opiera się ta książka:

* [„Profiling Programming Language Learning”](https://dl.acm.org/doi/10.1145/3649812) <br />
  [Will Crichton][will] i [Shriram Krishnamurthi][shriram]. OOPSLA 2024. (Wyróżnienie Distinguished Paper).

* [„A Grounded Conceptual Model for Ownership Types in Rust”](https://dl.acm.org/doi/10.1145/3622841) <br />
  [Will Crichton][will], [Gavin Gray][gavin] i [Shriram Krishnamurthi][shriram]. OOPSLA 2023. (Wyróżnienia SIGPLAN Research Highlight oraz Communications of the ACM Research Highlight).

## Podziękowania {#acknowledgments}

Ta praca była częściowo finansowana przez DARPA w ramach umowy nr HR00112420354, częściowo przez NSF w ramach grantu nr CCF-2227863, a częściowo przez Amazon Web Services. Wszelkie opinie, ustalenia, wnioski i zalecenia zawarte w tym materiale są opiniami autorów i nie odzwierciedlają stanowiska naszych sponsorów. Dziękujemy Carol Nichols i Rust Foundation za pomoc w nagłośnieniu eksperymentu. TRPL to owoc ciężkiej pracy wielu osób, wykonanej jeszcze przed rozpoczęciem naszego eksperymentu.

[understanding-ownership]: ch04-00-understanding-ownership.html
[aquascope]: https://cognitive-engineering-lab.github.io/aquascope/
[will]: https://willcrichton.net/
[gavin]: https://gavinleroy.com/
[shriram]: https://cs.brown.edu/people/sk/
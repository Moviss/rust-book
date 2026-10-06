## Komentarze {#comments}

Wszyscy programiści starają się pisać kod łatwy do zrozumienia, ale czasem
potrzebne jest dodatkowe wyjaśnienie. Wtedy zostawiają w kodzie źródłowym
_komentarze_, które kompilator ignoruje, a które mogą się przydać
osobom czytającym kod.

Oto prosty komentarz:

```rust
// hello, world
```

W Ruście idiomatyczny komentarz zaczyna się od dwóch ukośników i trwa do końca
linii. Jeśli komentarz zajmuje więcej niż jedną linię, musisz umieścić `//` na
początku każdej z nich, w ten sposób:

```rust
// So we're doing something complicated here, long enough that we need
// multiple lines of comments to do it! Whew! Hopefully, this comment will
// explain what's going on.
```

Możesz też użyć składni komentarza wielolinijkowego z `/*` i `*/`:

```rust
/* So we’re doing something complicated here, long enough that we need
   multiple lines of comments to do it! Whew! Hopefully, this comment will
   explain what’s going on. */
```

Komentarze można też umieszczać na końcu linii zawierających kod:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-24-comments-end-of-line/src/main.rs}}
```

Częściej jednak zobaczysz je w takiej postaci, z komentarzem w osobnej linii nad
kodem, którego dotyczy:

<span class="filename">Plik: src/main.rs</span>

```rust
{{#rustdoc_include ../listings/ch03-common-programming-concepts/no-listing-25-comments-above-line/src/main.rs}}
```

Rust ma też inny rodzaj komentarzy, komentarze dokumentacyjne, które omówimy w
podrozdziale [„Publikowanie crate’a w Crates.io”][publishing]<!-- ignore -->
rozdziału 14.

[publishing]: ch14-02-publishing-to-crates-io.html

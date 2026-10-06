## Podsumowanie własności {#ownership-recap}

W tym rozdziale wprowadziliśmy wiele nowych pojęć, takich jak własność (*ownership*), pożyczanie (*borrowing*) i wycinki (*slices*).
Jeśli nie masz doświadczenia z programowaniem systemowym, rozdział ten wprowadził też pojęcia takie jak alokacja pamięci, stos (*stack*) i sterta (*heap*), wskaźniki oraz niezdefiniowane zachowanie (*undefined behavior*). Zanim przejdziemy do dalszej części Rusta, zatrzymajmy się na chwilę i złapmy oddech. Powtórzymy i przećwiczymy najważniejsze pojęcia z tego rozdziału.

### Własność a odśmiecanie pamięci {#ownership-versus-garbage-collection}

Aby umieścić własność w szerszym kontekście, warto omówić **odśmiecanie pamięci** (*garbage collection*).
Większość języków programowania, takich jak Python, JavaScript, Java i Go, zarządza pamięcią za pomocą mechanizmu odśmiecania pamięci (*garbage collector*). Taki mechanizm pracuje w czasie działania programu, obok niego (przynajmniej w przypadku odśmiecania ze śledzeniem, *tracing collector*). Przeszukuje pamięć w poszukiwaniu danych, które nie są już używane &mdash; czyli takich, do których działający program nie może już dotrzeć z żadnej zmiennej lokalnej funkcji. Następnie dealokuje nieużywaną pamięć, aby można jej było użyć ponownie.

Główną zaletą odśmiecania pamięci jest to, że zapobiega ono niezdefiniowanemu zachowaniu (na przykład użyciu zwolnionej pamięci), które może wystąpić w C lub C++. Odśmiecanie pamięci zwalnia też z potrzeby stosowania złożonego systemu typów, który wykrywa niezdefiniowane zachowanie, jak w Ruście. Ma ono jednak kilka wad. Oczywistą wadą jest wydajność: odśmiecanie pamięci wiąże się albo z częstymi małymi narzutami (przy zliczaniu referencji, jak w Pythonie i Swifcie), albo z rzadkimi dużymi narzutami (przy śledzeniu, jak we wszystkich pozostałych językach z odśmiecaniem pamięci).

Inną, mniej oczywistą wadą jest to, że **odśmiecanie pamięci bywa nieprzewidywalne**. Aby to zilustrować, załóżmy, że implementujemy typ `Document`, który reprezentuje mutowalną (*mutable*) listę słów. W języku z odśmiecaniem pamięci, takim jak Python, moglibyśmy zaimplementować `Document` w taki sposób:

```python
class Document:     
    def __init__(self, words: List[str]):
        """Create a new document"""
        self.words = words

    def add_word(self, word: str):
        """Add a word to the document"""
        self.words.append(word)
        
    def get_words(self) -> List[str]:  
        """Get a list of all the words in the document"""
        return self.words
```

Oto jeden ze sposobów użycia klasy `Document`: tworzymy dokument `d`, kopiujemy go do nowego dokumentu `d2`, a następnie modyfikujemy `d2`.

```python
words = ["Hello"]
d = Document(words)

d2 = Document(d.get_words())
d2.add_word("world")
```

Rozważ dwa kluczowe pytania dotyczące tego przykładu:

1. **Kiedy zostanie zdealokowana tablica słów?**
Ten program utworzył trzy wskaźniki na tę samą tablicę. Zmienne `words`, `d` i `d2` zawierają wskaźnik na tablicę słów zaalokowaną na stercie. Dlatego Python zdealokuje tablicę słów dopiero wtedy, gdy wszystkie trzy zmienne wyjdą poza zasięg (*scope*). Mówiąc ogólniej, samo czytanie kodu źródłowego często nie wystarcza, by przewidzieć, gdzie dane zostaną usunięte przez mechanizm odśmiecania pamięci.

2. **Co zawiera dokument `d`?**
Ponieważ `d2` zawiera wskaźnik na tę samą tablicę słów co `d`, wywołanie `d2.add_word("world")` modyfikuje również dokument `d`. W tym przykładzie słowa w `d` to więc `["Hello", "world"]`. Dzieje się tak, ponieważ `d.get_words()` zwraca mutowalną referencję do tablicy słów w `d`. Wszechobecne, niejawne mutowalne referencje łatwo prowadzą do nieprzewidywalnych błędów, gdy struktury danych mogą ujawniać na zewnątrz swoje wnętrze[^ownership-originally]. Zmiana `d2` wpływająca na `d` raczej nie jest tu zamierzonym zachowaniem.

Ten problem nie dotyczy wyłącznie Pythona &mdash; podobne zachowanie możesz spotkać w C#, Javie, JavaScripcie i innych językach. Właściwie większość języków programowania ma pojęcie wskaźnika. Różnią się tylko tym, jak udostępniają wskaźniki programiście. Odśmiecanie pamięci utrudnia dostrzeżenie, która zmienna wskazuje na które dane. Na przykład nie było oczywiste, że `d.get_words()` zwraca wskaźnik na dane wewnątrz `d`.

Model własności w Ruście natomiast stawia wskaźniki na pierwszym planie. Widać to, gdy przełożymy typ `Document` na strukturę danych w Ruście. Normalnie użylibyśmy struktury (`struct`), ale jeszcze ich nie omówiliśmy, więc posłużymy się aliasem typu:

```rust
type Document = Vec<String>;

fn new_document(words: Vec<String>) -> Document {
    words
}

fn add_word(this: &mut Document, word: String) {
    this.push(word);
}

fn get_words(this: &Document) -> &[String] {
    this.as_slice()
}
```

To API w Ruście różni się od API w Pythonie w kilku kluczowych kwestiach:

* Funkcja `new_document` przejmuje własność wektora wejściowego `words`. Oznacza to, że `Document` *jest właścicielem* wektora słów. Wektor słów zostanie zdealokowany w przewidywalny sposób, gdy będący jego właścicielem `Document` wyjdzie poza zasięg.

* Funkcja `add_word` wymaga mutowalnej referencji `&mut Document`, aby móc zmodyfikować dokument. Przejmuje też własność wejściowego `word`, co oznacza, że nikt inny nie może modyfikować poszczególnych słów dokumentu.

* Funkcja `get_words` zwraca jawną niemutowalną referencję do łańcuchów znaków wewnątrz dokumentu. Jedynym sposobem utworzenia nowego dokumentu z tego wektora słów jest głębokie skopiowanie jego zawartości, na przykład tak:

```rust,ignore
fn main() {
    let words = vec!["hello".to_string()];
    let d = new_document(words);

    // .to_vec() converts &[String] to Vec<String> by cloning each string
    let words_copy = get_words(&d).to_vec();
    let mut d2 = new_document(words_copy);
    add_word(&mut d2, "world".to_string());

    // The modification to `d2` does not affect `d`
    assert!(!get_words(&d).contains(&"world".into()));
}
```

Ten przykład ma pokazać, że jeśli Rust nie jest twoim pierwszym językiem, to masz już doświadczenie w pracy z pamięcią i wskaźnikami! Rust po prostu czyni te pojęcia jawnymi. Daje to podwójną korzyść: (1) poprawia wydajność w czasie działania programu, bo nie ma odśmiecania pamięci, oraz (2) zwiększa przewidywalność, bo zapobiega przypadkowym „wyciekom” danych.

### Pojęcia związane z własnością {#the-concepts-of-ownership}

Teraz powtórzmy pojęcia związane z własnością. Ta powtórka będzie krótka &mdash; jej celem jest przypomnienie ci najważniejszych pojęć. Jeśli zauważysz, że jakieś pojęcie umknęło ci z pamięci albo nie było dla ciebie jasne, podamy linki do odpowiednich podrozdziałów, do których możesz wrócić.

#### Własność w czasie działania programu {#ownership-at-runtime}

Zacznijmy od przypomnienia, jak Rust korzysta z pamięci w czasie działania programu:
* Rust alokuje zmienne lokalne w ramkach stosu (*frames*), które są alokowane w chwili wywołania funkcji i dealokowane, gdy wywołanie się kończy.
* Zmienne lokalne mogą przechowywać albo dane (takie jak liczby, wartości logiczne, krotki itp.), albo wskaźniki.
* Wskaźniki można tworzyć albo za pomocą boxów (wskaźników będących właścicielami danych na stercie), albo referencji (wskaźników niebędących właścicielami).

Ten diagram pokazuje, jak każde z tych pojęć wygląda w czasie działania programu:

```aquascope,interpreter,horizontal
fn main() {
  let mut a_num = 0;
  inner(&mut a_num);`[]`
}

fn inner(x: &mut i32) {
  let another_num = 1;
  let a_stack_ref = &another_num;

  let a_box = Box::new(2);  
  let a_box_stack_ref = &a_box;
  let a_box_heap_ref = &*a_box;`[]`

  *x += 5;
}
```

Przeanalizuj ten diagram i upewnij się, że rozumiesz każdą jego część. Na przykład powinno ci się udać odpowiedzieć na pytania:
* Dlaczego `a_box_stack_ref` wskazuje na stos, a `a_box_heap_ref` na stertę?
* Dlaczego w punkcie L2 wartości `2` nie ma już na stercie?
* Dlaczego w punkcie L2 `a_num` ma wartość `5`?

Jeśli chcesz powtórzyć wiadomości o boxach, przeczytaj ponownie [podrozdział 4.1][ch04-01]. Jeśli chcesz powtórzyć wiadomości o referencjach, przeczytaj ponownie [podrozdział 4.2][ch04-02]. Jeśli chcesz zobaczyć studia przypadków z boxami i referencjami, przeczytaj ponownie [podrozdział 4.3][ch04-03].

Wycinki to szczególny rodzaj referencji, które odwołują się do ciągłej sekwencji danych w pamięci. Ten diagram pokazuje, jak wycinek odwołuje się do podciągu znaków w łańcuchu:

```aquascope,interpreter
fn main() {
  let s = String::from("abcdefg");
  let s_slice = &s[2..5];`[]`
}
```

Jeśli chcesz powtórzyć wiadomości o wycinkach, przeczytaj ponownie [podrozdział 4.4][ch04-04].


#### Własność w czasie kompilacji {#ownership-at-compile-time}

Rust śledzi dla każdej zmiennej uprawnienia (*permissions*) @Perm{read} (*read*, odczyt), @Perm{write} (*write*, zapis) i @Perm{own} (*own*, własność). Rust wymaga, by zmienna miała odpowiednie uprawnienia do wykonania danej operacji. Prosty przykład: jeśli zmienna nie jest zadeklarowana jako `let mut`, to brakuje jej uprawnienia @Perm{write} i nie można jej modyfikować:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
  let n = 0;
  n += 1;
}
```

Uprawnienia zmiennej mogą się zmienić, jeśli zostanie ona **przeniesiona** lub **pożyczona**. Przeniesienie (*move*) zmiennej typu, którego nie da się kopiować (np. `Box<T>` lub `String`), wymaga uprawnień @Perm{read}@Perm{own}, a samo przeniesienie odbiera zmiennej wszystkie uprawnienia. Ta reguła zapobiega używaniu przeniesionych zmiennych:

```aquascope,permissions,stepper,boundaries,shouldFail
fn main() {
  let s = String::from("Hello world");
  consume_a_string(s);
  println!("{s}"); // can't read `s` after moving it
}

fn consume_a_string(_s: String) {
  // om nom nom
}
```

Jeśli chcesz powtórzyć, jak działa przenoszenie, przeczytaj ponownie [podrozdział 4.1][ch04-01].

Pożyczenie zmiennej (utworzenie referencji do niej) tymczasowo odbiera jej część uprawnień. Niemutowalne pożyczenie tworzy niemutowalną referencję, a przy tym uniemożliwia modyfikowanie lub przenoszenie pożyczonych danych. Na przykład wypisanie niemutowalnej referencji jest w porządku:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;
println!("{s_ref}");
println!("{s}");
#}
```

Ale modyfikowanie danych przez niemutowalną referencję nie jest w porządku:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;`(focus,paths:*s_ref)`
s_ref.push_str(" world");
println!("{s}");
#}
```

Modyfikowanie danych pożyczonych niemutowalnie również nie jest w porządku:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");`(focus)`
let s_ref = &s;`(focus,rxpaths:s$)`
s.push_str(" world");
println!("{s_ref}");
#}
```

Nie jest też w porządku przenoszenie danych z referencji:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &s;`(focus,paths:*s_ref)`
let s2 = *s_ref;
println!("{s}");
#}
```

Mutowalne pożyczenie tworzy mutowalną referencję, która uniemożliwia odczytywanie, zapisywanie i przenoszenie pożyczonych danych. Na przykład modyfikowanie danych przez mutowalną referencję jest w porządku:

```aquascope,permissions,stepper,boundaries
#fn main() {
let mut s = String::from("Hello");
let s_ref = &mut s;
s_ref.push_str(" world");
println!("{s}");
#}
```

Ale dostęp do danych pożyczonych mutowalnie nie jest w porządku:

```aquascope,permissions,stepper,boundaries,shouldFail
#fn main() {
let mut s = String::from("Hello");
let s_ref = &mut s;`(focus,rxpaths:s$)`
println!("{s}");
s_ref.push_str(" world");
#}
```

Jeśli chcesz powtórzyć wiadomości o uprawnieniach i referencjach, przeczytaj ponownie [podrozdział 4.2][ch04-02].

#### Łączenie własności w czasie kompilacji i w czasie działania programu {#connecting-ownership-between-compile-time-and-runtime}

Uprawnienia w Ruście mają zapobiegać niezdefiniowanemu zachowaniu. Jednym z rodzajów niezdefiniowanego zachowania jest na przykład **użycie po zwolnieniu** (*use-after-free*), czyli odczyt lub zapis zwolnionej pamięci. Niemutowalne pożyczenia odbierają uprawnienie @Perm{write}, aby zapobiec użyciu po zwolnieniu, jak w tym przypadku:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let mut v = vec![1, 2, 3];
let n = &v[0];`[]`
v.push(4);`[]`
println!("{n}");`[]`
#}
```

Innym rodzajem niezdefiniowanego zachowania jest **podwójne zwolnienie** (*double-free*), czyli dwukrotne zwolnienie tej samej pamięci. Dereferencje (*dereferences*) referencji do danych, których nie da się kopiować, nie mają uprawnienia @Perm{own}, aby zapobiec podwójnemu zwolnieniu, jak w tym przypadku:

```aquascope,interpreter,shouldFail,horizontal
#fn main() {
let v = vec![1, 2, 3];
let v_ref: &Vec<i32> = &v;
let v2 = *v_ref;`[]`
drop(v2);`[]`
drop(v);`[]`
#}
```

Jeśli chcesz powtórzyć wiadomości o niezdefiniowanym zachowaniu, przeczytaj ponownie [podrozdział 4.1][ch04-01] i [podrozdział 4.3][ch04-03].


### Pozostałe aspekty własności {#the-rest-of-ownership}

Gdy będziemy wprowadzać kolejne mechanizmy, takie jak struktury, enumy i traity, okaże się, że każdy z nich w szczególny sposób współdziała z własnością. Ten rozdział daje niezbędne podstawy do zrozumienia tych zależności &mdash; pojęcia pamięci, wskaźników, niezdefiniowanego zachowania i uprawnień pomogą nam omawiać bardziej zaawansowane elementy Rusta w kolejnych rozdziałach.

I nie zapomnij rozwiązać quizów, jeśli chcesz sprawdzić, jak dobrze rozumiesz materiał!

{{#quiz ../quizzes/ch04-05-ownership-recap.toml}}



[^ownership-originally]: W rzeczywistości pierwotny pomysł typów własności (*ownership types*) w ogóle nie dotyczył bezpieczeństwa pamięci. Chodziło w nim o zapobieganie wyciekom mutowalnych referencji do wnętrza struktur danych w językach podobnych do Javy. Jeśli chcesz dowiedzieć się więcej o historii typów własności, zajrzyj do artykułu [„Ownership Types for Flexible Alias Protection”](https://dl.acm.org/doi/abs/10.1145/286936.286947) (Clarke i in., 1998).

[ch04-01]: ch04-01-what-is-ownership.html
[ch04-02]: ch04-02-references-and-borrowing.html
[ch04-03]: ch04-03-fixing-ownership-errors.html
[ch04-04]: ch04-04-slices.html

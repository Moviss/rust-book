## Inwentaryzacja własności #1 {#ownership-inventory-1}

Inwentaryzacja własności to seria quizów, które sprawdzają, jak rozumiesz własność (*ownership*) w realistycznych scenariuszach. Scenariusze te są inspirowane częstymi pytaniami o Rusta na StackOverflow. Za pomocą tych pytań możesz sprawdzić, jak dobrze rozumiesz już własność.

### Nowa technologia: IDE w przeglądarce {#a-new-technology-the-in-browser-ide}

W tych pytaniach pojawią się programy w Ruście korzystające z funkcji, których jeszcze nie znasz. Dlatego użyjemy eksperymentalnej technologii, która udostępnia funkcje IDE w przeglądarce. IDE pozwala uzyskać informacje o nieznanych funkcjach i typach. Wykonaj na przykład następujące czynności w poniższym programie:

* Najedź kursorem myszy na `replace`, aby zobaczyć typ i opis tej metody.
* Najedź kursorem myszy na `s2`, aby zobaczyć wywnioskowany typ tej zmiennej.

---------


<pre>
<code class="ide">
/// Turns a string into a far more exciting string
fn make_exciting(s: &str) -> String {
  let s2 = s.replace(".", "!");
  let s3 = s2.replace("?", "‽");
  s3
}
</code>
</pre>

---------

Kilka ważnych zastrzeżeń dotyczących tej eksperymentalnej technologii:

**ZGODNOŚĆ Z PLATFORMAMI:** IDE w przeglądarce nie działa na ekranach dotykowych. Zostało przetestowane tylko w Google Chrome 109 i Firefoksie 107. Może nie działać w starszych wersjach Safari.

**ZUŻYCIE PAMIĘCI:** IDE w przeglądarce korzysta z wersji [rust-analyzera](https://github.com/rust-lang/rust-analyzer) skompilowanej do [WebAssembly](https://rustwasm.github.io/book/), która może zajmować sporo pamięci. Każda instancja IDE zajmuje, jak się wydaje, około 300 MB. (Uwaga: dostaliśmy też kilka zgłoszeń o zużyciu pamięci przekraczającym 10 GB).

**PRZEWIJANIE:** IDE w przeglądarce „pożera” kursor, jeśli podczas przewijania kursor znajdzie się nad edytorem. Jeśli masz problem z przewijaniem strony, przesuń kursor na pasek przewijania po prawej stronie.

**CZAS ŁADOWANIA:** inicjalizacja IDE dla nowego programu może trwać do 15 sekund. W tym czasie podczas pracy z kodem w edytorze wyświetla się komunikat „Loading...”.

### Quiz {#the-quiz}

{{#quiz ../quizzes/ch06-04-inventory.toml}}

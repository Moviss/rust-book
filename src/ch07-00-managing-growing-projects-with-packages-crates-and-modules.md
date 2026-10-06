<!-- Old headings. Do not remove or links may break. -->

<a id="managing-growing-projects-with-packages-crates-and-modules"></a>

# Pakiety, crate’y i moduły {#packages-crates-and-modules}

Im większe programy piszesz, tym ważniejsza staje się organizacja kodu.
Grupując powiązaną funkcjonalność i oddzielając kod odpowiedzialny za różne
funkcjonalności, jasno pokazujesz, gdzie szukać kodu implementującego daną
funkcjonalność i gdzie zajrzeć, żeby zmienić jej działanie.

Programy, które do tej pory napisaliśmy, mieściły się w jednym module w jednym
pliku. Gdy projekt rośnie, warto uporządkować kod, dzieląc go na wiele modułów,
a następnie na wiele plików. Pakiet (*package*) może zawierać wiele crate’ów
binarnych i opcjonalnie jeden crate biblioteczny (*crate* – jednostka
kompilacji w Ruście). W miarę rozrostu pakietu możesz wydzielać jego części do
osobnych crate’ów, które staną się zależnościami zewnętrznymi. Ten rozdział
omawia wszystkie te techniki. Dla bardzo dużych projektów, składających się z
zestawu powiązanych pakietów rozwijanych razem, Cargo udostępnia przestrzenie
robocze (*workspaces*), które omówimy w podrozdziale
[„Przestrzenie robocze Cargo”][workspaces]<!-- ignore --> w rozdziale 14.

Omówimy też hermetyzację szczegółów implementacji, która pozwala ponownie
wykorzystywać kod na wyższym poziomie: gdy już zaimplementujesz jakąś operację,
inny kod może wywoływać twój kod przez jego publiczny interfejs, nie wiedząc,
jak działa implementacja. To, jak piszesz kod, określa, które jego części są
publiczne i dostępne dla innego kodu, a które są prywatnymi szczegółami
implementacji, które zastrzegasz sobie prawo zmieniać. To kolejny sposób na
ograniczenie liczby szczegółów, które musisz trzymać w głowie.

Pokrewnym pojęciem jest zasięg (*scope*): zagnieżdżony kontekst, w którym
piszesz kod, ma zbiór nazw zdefiniowanych jako „w zasięgu”. Podczas czytania,
pisania i kompilowania kodu programiści i kompilatory muszą wiedzieć, czy dana
nazwa w danym miejscu odnosi się do zmiennej, funkcji, struktury, enuma,
modułu, stałej czy innego elementu i co ten element oznacza. Możesz tworzyć
zasięgi i zmieniać, które nazwy są w zasięgu, a które poza nim. Nie można mieć
dwóch elementów o tej samej nazwie w tym samym zasięgu; istnieją narzędzia do
rozwiązywania konfliktów nazw.

Rust ma wiele mechanizmów, które pozwalają zarządzać organizacją kodu, m.in. tym,
które szczegóły są udostępniane, które są prywatne i jakie nazwy są w każdym
zasięgu w twoich programach. Do tych mechanizmów, nazywanych czasem łącznie
_systemem modułów_ (*module system*), należą:

* **pakiety**: mechanizm Cargo, który pozwala budować, testować i udostępniać
  crate’y;
* **crate’y**: drzewo modułów, z którego powstaje biblioteka lub plik
  wykonywalny;
* **moduły i use**: pozwalają kontrolować organizację, zasięg i prywatność
  ścieżek;
* **ścieżki**: sposób nazywania elementu, takiego jak struktura, funkcja czy
  moduł.

W tym rozdziale omówimy wszystkie te mechanizmy, pokażemy, jak ze sobą
współdziałają, i wyjaśnimy, jak za ich pomocą zarządzać zasięgiem. Po jego
lekturze system modułów nie będzie miał przed tobą tajemnic, a z zasięgami
poradzisz sobie jak zawodowiec!

[workspaces]: ch14-03-cargo-workspaces.html

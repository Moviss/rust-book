# Zaawansowane mechanizmy {#advanced-features}

Znasz już najczęściej używane elementy języka programowania Rust. Zanim w
rozdziale 21 zrealizujemy jeszcze jeden projekt, przyjrzymy się kilku aspektom
języka, na które możesz czasem natrafić, ale których raczej nie będziesz używać
na co dzień. Możesz traktować ten rozdział jako punkt odniesienia, gdy
napotkasz coś nieznanego. Omawiane tu mechanizmy przydają się w bardzo
konkretnych sytuacjach. Choć być może nie będziesz po nie często sięgać, chcemy
mieć pewność, że znasz wszystkie mechanizmy, jakie oferuje Rust.

W tym rozdziale omówimy:

- niebezpieczny Rust (*unsafe Rust*): jak zrezygnować z niektórych gwarancji
  Rusta i samodzielnie wziąć odpowiedzialność za ich dotrzymanie;
- zaawansowane *traity* (cechy typów, zbliżone do interfejsów): typy powiązane
  (*associated types*), domyślne parametry typów, w pełni kwalifikowaną
  składnię, supertraity i wzorzec newtype w odniesieniu do traitów;
- zaawansowane typy: więcej o wzorcu newtype, aliasy typów, typ never i typy o
  dynamicznym rozmiarze (*dynamically sized types*);
- zaawansowane funkcje i domknięcia (*closures*): wskaźniki na funkcje
  (*function pointers*) i zwracanie domknięć;
- makra: sposoby definiowania kodu, który w czasie kompilacji (*compile-time*)
  definiuje kolejny kod.

To prawdziwa mozaika mechanizmów Rusta – każdy znajdzie tu coś dla siebie!
Zaczynajmy!

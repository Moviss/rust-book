## Uruchamianie kodu przy sprzątaniu za pomocą traitu `Drop` {#running-code-on-cleanup-with-the-drop-trait}

Drugim *traitem* (cecha typu, zbliżona do interfejsu) ważnym dla wzorca
inteligentnego wskaźnika (*smart pointer*) jest `Drop`, który pozwala dostosować
to, co się dzieje, gdy wartość ma wyjść poza zasięg (*scope*). Implementację
traitu `Drop` możesz dostarczyć dla dowolnego typu, a jej kod może posłużyć do
zwalniania zasobów, takich jak pliki czy połączenia sieciowe.

Omawiamy `Drop` w kontekście inteligentnych wskaźników, ponieważ
funkcjonalność traitu `Drop` jest używana niemal zawsze przy implementowaniu
inteligentnego wskaźnika. Na przykład gdy *box* (wskaźnik na dane umieszczone
na stercie) `Box<T>` zostaje zwolniony (*drop*), dealokuje miejsce na stercie
(*heap*), na które wskazuje.

W niektórych językach, dla niektórych typów, programista musi wywołać kod
zwalniający pamięć lub zasoby za każdym razem, gdy skończy używać instancji
takiego typu. Przykładami są uchwyty plików, gniazda i blokady. Jeśli
programista o tym zapomni, system może zostać przeciążony i ulec awarii. W
Ruście możesz określić, że dany fragment kodu ma zostać uruchomiony za każdym
razem, gdy wartość wychodzi poza zasięg, a kompilator wstawi ten kod
automatycznie. Dzięki temu nie musisz pilnować, by umieszczać kod porządkujący
w każdym miejscu programu, w którym instancja danego typu przestaje być
potrzebna – a mimo to nie dojdzie do wycieku zasobów!

Kod, który ma zostać uruchomiony, gdy wartość wychodzi poza zasięg, określasz,
implementując trait `Drop`. Trait `Drop` wymaga zaimplementowania jednej metody
o nazwie `drop`, która przyjmuje mutowalną (*mutable*) referencję (*reference*)
do `self`. Aby zobaczyć, kiedy Rust wywołuje `drop`, zaimplementujmy na razie
`drop` z instrukcjami `println!`.

Listing 15-14 pokazuje strukturę (*struct*) `CustomSmartPointer`, której jedyną
własną funkcjonalnością jest wypisanie `Dropping CustomSmartPointer!`, gdy
instancja wychodzi poza zasięg. Pokazuje to, kiedy Rust uruchamia metodę
`drop`.

<Listing number="15-14" file-name="src/main.rs" caption="Struktura `CustomSmartPointer` implementująca trait `Drop`, w którym umieścilibyśmy kod porządkujący">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-14/src/main.rs}}
```

</Listing>

Trait `Drop` należy do *prelude* (zestaw elementów importowanych
automatycznie), więc nie musimy wprowadzać go do zasięgu. Implementujemy trait
`Drop` dla `CustomSmartPointer` i dostarczamy implementację metody `drop`, która
wywołuje `println!`. W ciele metody `drop` umieszczasz logikę, która ma zostać
wykonana, gdy instancja twojego typu wychodzi poza zasięg. Tutaj wypisujemy
tekst, żeby pokazać, kiedy Rust wywoła `drop`.

W `main` tworzymy dwie instancje `CustomSmartPointer`, a następnie wypisujemy
`CustomSmartPointers created`. Na końcu `main` nasze instancje
`CustomSmartPointer` wyjdą poza zasięg, a Rust wywoła kod umieszczony przez nas
w metodzie `drop`, wypisując nasz ostatni komunikat. Zauważ, że nie musieliśmy
jawnie wywoływać metody `drop`.

Po uruchomieniu programu zobaczymy następujące wyjście:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-14/output.txt}}
```

Rust automatycznie wywołał za nas `drop`, gdy nasze instancje wyszły poza
zasięg, uruchamiając określony przez nas kod. Zmienne są zwalniane w kolejności
odwrotnej do kolejności ich utworzenia, więc `d` zostało zwolnione przed `c`.
Celem tego przykładu jest pokazanie, jak działa metoda `drop`; zwykle zamiast
komunikatu do wypisania określasz kod porządkujący, którego potrzebuje twój typ.

<!-- Old headings. Do not remove or links may break. -->

<a id="dropping-a-value-early-with-std-mem-drop"></a>

Niestety wyłączenie automatycznego wywoływania `drop` nie jest proste.
Wyłączanie `drop` zwykle nie jest potrzebne – cały sens traitu `Drop` polega na
tym, że wszystko dzieje się automatycznie. Czasem jednak możesz chcieć
posprzątać wartość wcześniej. Przykładem jest używanie inteligentnych wskaźników zarządzających
blokadami: możesz chcieć wymusić wywołanie metody `drop`, która zwalnia
blokadę, aby inny kod w tym samym zasięgu mógł ją uzyskać. Rust nie pozwala
ręcznie wywołać metody `drop` traitu `Drop`; jeśli chcesz wymusić zwolnienie
wartości przed końcem jej zasięgu, musisz zamiast tego wywołać funkcję
`std::mem::drop` dostarczaną przez bibliotekę standardową.

Próba ręcznego wywołania metody `drop` traitu `Drop` przez zmodyfikowanie
funkcji `main` z listingu 15-14 nie zadziała, co pokazuje listing 15-15.

<Listing number="15-15" file-name="src/main.rs" caption="Próba ręcznego wywołania metody `drop` z traitu `Drop` w celu wcześniejszego posprzątania">

```rust,ignore,does_not_compile
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-15/src/main.rs:here}}
```

</Listing>

Gdy spróbujemy skompilować ten kod, otrzymamy taki błąd:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-15/output.txt}}
```

Ten komunikat o błędzie mówi, że nie wolno nam jawnie wywoływać `drop`.
Komunikat używa terminu _destruktor_ (*destructor*), czyli ogólnego terminu
programistycznego oznaczającego funkcję, która sprząta po instancji.
_Destruktor_ jest odpowiednikiem _konstruktora_, który tworzy instancję. Funkcja
`drop` w Ruście jest jednym z rodzajów destruktora.

Rust nie pozwala nam jawnie wywołać `drop`, ponieważ i tak automatycznie
wywołałby `drop` dla tej wartości na końcu `main`. Spowodowałoby to błąd
podwójnego zwolnienia (*double free*), ponieważ Rust próbowałby posprzątać tę
samą wartość dwukrotnie.

Nie możemy wyłączyć automatycznego wstawiania `drop`, gdy wartość wychodzi poza
zasięg, ani jawnie wywołać metody `drop`. Jeśli więc musimy wymusić wcześniejsze
posprzątanie wartości, używamy funkcji `std::mem::drop`.

Funkcja `std::mem::drop` różni się od metody `drop` w traicie `Drop`.
Wywołujemy ją, przekazując jako argument wartość, której zwolnienie chcemy
wymusić. Funkcja należy do prelude, więc możemy zmodyfikować `main` z listingu
15-15 tak, by wywoływała funkcję `drop`, jak pokazuje listing 15-16.

<Listing number="15-16" file-name="src/main.rs" caption="Wywołanie `std::mem::drop` w celu jawnego zwolnienia wartości, zanim wyjdzie ona poza zasięg">

```rust
{{#rustdoc_include ../listings/ch15-smart-pointers/listing-15-16/src/main.rs:here}}
```

</Listing>

Uruchomienie tego kodu wypisze:

```console
{{#include ../listings/ch15-smart-pointers/listing-15-16/output.txt}}
```

Tekst ``Dropping CustomSmartPointer with data `some data`!`` zostaje wypisany
między tekstem `CustomSmartPointer created` a tekstem
`CustomSmartPointer dropped before the end of main`, co pokazuje, że kod metody
`drop` zostaje wywołany w tym miejscu, by zwolnić `c`.

Kod określony w implementacji traitu `Drop` możesz wykorzystać na wiele
sposobów, by sprzątanie było wygodne i bezpieczne: możesz na przykład użyć go do
stworzenia własnego alokatora pamięci! Dzięki traitowi `Drop` i systemowi
własności (*ownership*) w Ruście nie musisz pamiętać o sprzątaniu, ponieważ Rust
robi to automatycznie.

Nie musisz się też martwić problemami wynikającymi z przypadkowego posprzątania
wartości, które są wciąż w użyciu: system własności, który gwarantuje, że
referencje są zawsze poprawne, zapewnia również, że `drop` zostanie wywołane
tylko raz, gdy wartość przestanie być używana.

Skoro przyjrzeliśmy się już `Box<T>` i niektórym właściwościom inteligentnych
wskaźników, przyjrzyjmy się kilku innym inteligentnym wskaźnikom zdefiniowanym w
bibliotece standardowej.

{{#quiz ../quizzes/ch15-03-drop.toml}}

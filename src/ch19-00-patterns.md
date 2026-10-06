# Wzorce i dopasowywanie {#patterns-and-matching}

Wzorce to w Ruście specjalna składnia służąca do dopasowywania struktury typów,
zarówno złożonych, jak i prostych. Używanie wzorców razem z wyrażeniami
(*expressions*) `match` i innymi konstrukcjami daje większą kontrolę nad
przepływem sterowania (*control flow*) programu. Wzorzec składa się z jakiejś
kombinacji następujących elementów:

- literałów;
- destrukturyzowanych tablic, *enumów* (typów wyliczeniowych), struktur
  (*structs*) lub krotek (*tuples*);
- zmiennych;
- symboli wieloznacznych;
- symboli zastępczych (*placeholders*).

Przykładowe wzorce to `x`, `(a, 3)` i `Some(Color::Red)`. W kontekstach, w
których wzorce są dozwolone, te elementy opisują kształt danych. Program
dopasowuje następnie wartości do wzorców, aby ustalić, czy dane mają właściwy
kształt, by kontynuować wykonywanie określonego fragmentu kodu.

Aby użyć wzorca, porównujemy go z jakąś wartością. Jeśli wzorzec pasuje do
wartości, używamy części tej wartości w naszym kodzie. Przypomnij sobie
wyrażenia `match` z rozdziału 6, które korzystały ze wzorców, choćby w
przykładzie z maszyną sortującą monety. Jeśli wartość pasuje do kształtu wzorca,
możemy używać nazwanych fragmentów. Jeśli nie pasuje, kod powiązany ze wzorcem
się nie wykona.

Ten rozdział to kompendium wszystkiego, co dotyczy wzorców. Omówimy miejsca, w
których można używać wzorców, różnicę między wzorcami odrzucalnymi
(*refutable*) i nieodrzucalnymi (*irrefutable*) oraz różne rodzaje składni
wzorców, które możesz spotkać. Pod koniec rozdziału będziesz wiedzieć, jak
używać wzorców, by w przejrzysty sposób wyrażać wiele koncepcji.

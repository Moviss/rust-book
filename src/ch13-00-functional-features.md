# Mechanizmy funkcyjne: iteratory i domknięcia {#functional-language-features-iterators-and-closures}

Projektując Rusta, czerpano inspirację z wielu istniejących języków i technik,
a jednym z istotnych wpływów jest _programowanie funkcyjne_. Programowanie w
stylu funkcyjnym często polega na używaniu funkcji jako wartości: przekazywaniu
ich w argumentach, zwracaniu z innych funkcji, przypisywaniu do zmiennych w celu
późniejszego wykonania i tak dalej.

W tym rozdziale nie będziemy rozstrzygać, czym programowanie funkcyjne jest, a
czym nie jest. Zamiast tego omówimy kilka mechanizmów Rusta podobnych do
mechanizmów wielu języków, które często nazywa się funkcyjnymi.

Dokładniej rzecz biorąc, omówimy:

- _domknięcia_ (*closures*), czyli konstrukcje podobne do funkcji, które można
  przechowywać w zmiennej;
- _iteratory_, czyli sposób przetwarzania ciągu elementów;
- sposób użycia domknięć i iteratorów do ulepszenia projektu wejścia/wyjścia z
  rozdziału 12;
- wydajność domknięć i iteratorów (uwaga, spoiler: są szybsze, niż mogłoby się
  wydawać!).

Omówiliśmy już kilka innych mechanizmów Rusta, takich jak dopasowywanie wzorców
(*pattern matching*) i *enumy* (typy wyliczeniowe), na które również wpłynął
styl funkcyjny. Ponieważ opanowanie domknięć i iteratorów jest ważną częścią
pisania szybkiego, idiomatycznego kodu w Ruście, poświęcimy im cały ten
rozdział.

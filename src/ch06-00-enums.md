# Enumy i dopasowywanie wzorców {#enums-and-pattern-matching}

W tym rozdziale przyjrzymy się typom wyliczeniowym, nazywanym też _enumami_
(*enum*). Enumy pozwalają zdefiniować typ przez wyliczenie jego możliwych
wariantów. Najpierw zdefiniujemy enum i użyjemy go, żeby pokazać, jak enum może
wyrażać znaczenie razem z danymi. Następnie omówimy szczególnie przydatny enum o
nazwie `Option`, który wyraża, że wartość może być czymś albo niczym. Potem
zobaczymy, jak dopasowywanie wzorców (*pattern matching*) w wyrażeniu `match`
ułatwia uruchamianie różnego kodu dla różnych wartości enuma. Na koniec
pokażemy, że konstrukcja `if let` to kolejny wygodny i zwięzły idiom do obsługi
enumów w kodzie.

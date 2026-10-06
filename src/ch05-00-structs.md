# Grupowanie powiązanych danych za pomocą struktur {#using-structs-to-structure-related-data}

_Struktura_ (*struct*, *structure*) to własny typ danych, który pozwala
zebrać razem i nazwać wiele powiązanych wartości tworzących sensowną całość.
Jeśli znasz język obiektowy, struktura przypomina atrybuty danych obiektu. W tym
rozdziale porównamy krotki ze strukturami, żeby oprzeć się na tym, co już
wiesz, i pokazać, kiedy struktury są lepszym sposobem grupowania danych.

Pokażemy, jak definiować struktury i tworzyć ich instancje. Omówimy, jak
definiować funkcje powiązane (*associated functions*), zwłaszcza ich szczególny
rodzaj zwany _metodami_, żeby określić zachowanie związane z typem struktury.
Struktury i *enumy* (typy wyliczeniowe, omówione w rozdziale 6) są
podstawowymi elementami do tworzenia nowych typów w dziedzinie twojego programu,
które pozwalają w pełni wykorzystać sprawdzanie typów w czasie kompilacji
(*compile-time*) w Ruście.

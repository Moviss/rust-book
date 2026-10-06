# Obsługa błędów {#error-handling}

Błędy są w oprogramowaniu codziennością, dlatego Rust ma szereg mechanizmów do
obsługi sytuacji, w których coś idzie nie tak. W wielu przypadkach Rust wymaga,
żebyś uwzględnił możliwość wystąpienia błędu i jakoś na nią zareagował, zanim
kod się skompiluje. Dzięki temu wymaganiu program jest solidniejszy: masz
pewność, że wykryjesz błędy i odpowiednio je obsłużysz, zanim wdrożysz kod na
produkcję!

Rust dzieli błędy na dwie główne kategorie: odwracalne i nieodwracalne. W
przypadku błędu odwracalnego (*recoverable error*), takiego jak błąd _nie
znaleziono pliku_, najczęściej chcemy po prostu zgłosić problem użytkownikowi i
ponowić operację. Błędy nieodwracalne (*unrecoverable errors*) są zawsze
objawami bugów, takich jak próba dostępu do miejsca za końcem tablicy, więc
chcemy wtedy natychmiast zatrzymać program.

Większość języków nie rozróżnia tych dwóch rodzajów błędów i obsługuje oba w
ten sam sposób, za pomocą mechanizmów takich jak wyjątki. Rust nie ma wyjątków.
Zamiast tego ma typ `Result<T, E>` dla błędów odwracalnych oraz makro `panic!`,
które zatrzymuje wykonanie, gdy program napotka błąd nieodwracalny. W tym
rozdziale najpierw omówimy wywoływanie `panic!`, a potem zwracanie wartości
`Result<T, E>`. Zastanowimy się też, co brać pod uwagę, decydując, czy próbować
naprawić sytuację po błędzie, czy zatrzymać wykonanie.

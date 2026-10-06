# Zrozumieć własność {#understanding-ownership}

Własność (*ownership*) to najbardziej wyjątkowa cecha Rusta, która ma głębokie
konsekwencje dla reszty języka. Dzięki niej Rust może gwarantować
bezpieczeństwo pamięci bez mechanizmu odśmiecania pamięci (*garbage
collector*), dlatego ważne jest, by zrozumieć, jak działa własność. W tym
rozdziale omówimy własność oraz kilka powiązanych z nią mechanizmów: pożyczanie
(*borrowing*), wycinki (*slices*) i sposób, w jaki Rust rozmieszcza dane w
pamięci.

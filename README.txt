Wojciech Żukrowski — archiwum pisarza

Podgląd lokalny:
  python3 -m http.server 8000 --bind 127.0.0.1
  http://127.0.0.1:8000

Edycja treści:
- content/books.json: bibliografia, opisy, okładki i powiązane materiały.
- content/pages/: treści stron i zachowane artykuły archiwalne.
- content/pages.json: adresy, tytuły i przypisanie stron do nawigacji.
- templates/page.html: wspólny szablon strony, nawigacja i stopka.
- styles.css: wygląd i układ responsywny.
- site.js: wyszukiwanie w bibliografii (pozostałe treści działają bez JavaScript).

Po zmianie treści lub szablonu uruchom:
  python3 scripts/build.py

Generator używa wyłącznie standardowej biblioteki Pythona. Pliki HTML w katalogu
 głównym i podkatalogach są gotowe do publikacji na GitHub Pages. Edytuj źródła
w content/ zamiast wygenerowanych plików. Dotychczasowe adresy są zachowane.

Informacje o książkach pochodzą z istniejącej bibliografii. Rok wpisu nie musi
opisywać wydania widocznego na okładce. Nie dopisano nieznanych wydawców ani dat
fotografii. Karty z niewielką ilością danych można uzupełniać w books.json.

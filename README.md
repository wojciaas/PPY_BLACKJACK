# PROJEKT ZALICZENIOWY BLACKJACK W PYTHON

Interaktywna gra karciana Blackjack w Pythonie, stworzona na zajęcia z programowania. Projekt demonstruje zaawansowane koncepcje programistyczne w terminalu z menu i rozgrywką wieloosobową.

## Opis projektu

Gra Blackjack pozwala na interaktywną rozgrywkę w terminalu z menu głównym, obsługą wielu graczy oraz krupierem sterowanym algorytmem. Zawiera pełną logikę talii kart, obliczanie wartości rąk (z asami), sprawdzanie bustów, blackjacka i porównywanie wyników. Zaprojektowana do prezentacji na zajęciach, podkreśla umiejętności w strukturach danych, pętlach, warunkach i modułowej architekturze kodu.

## Funkcje

- Menu startowe z opcjami: nowa gra, liczba graczy, zasady.
- Rozgrywka wieloosobowa (gracze vs krupier).
- Krupier z podstawowym algorytmem (hit do 17, stand na 17+).
- Obsługa asów (wartość 1/11), figur (10 pkt).
- Wizualizacja rąk kart w terminalu.
- Licznik wygranych/przegranych i powrót do menu.

Projekt wykorzystuje większość koncepcji z przedmiotu: klasy/obiekty (opcjonalnie), listy/słowniki dla talii, funkcje modularne, obsługa wejścia/wyjścia, pętle While/For.
## Instalacja i uruchomienie

1. Sklonuj repozytorium: `git clone https://github.com/wojciaas/PPY_BLACKJACK.git`
2. Przejdź do folderu: `cd PPY_BLACKJACK`
3. Uruchom: `python main.py` (lub nazwa głównego pliku, np. `blackjack.py`).

## Zasady gry

- Cel: zbliżyć się do 21 bez przekroczenia.
- Gracz: hit/stand (opcjonalnie double/split w rozszerzeniu).
- Krupier: hit poniżej 17.
- Blackjack (21 na 2 karty) wygrywa automatycznie.

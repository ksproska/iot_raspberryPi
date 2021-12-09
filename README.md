# Podstawy Internetu rzeczy - Raspberry Pi

## L09

### [Zad1](L09/Zad1.py) - Regulacja jasności świecenia diody enkoderem

Napisz program, który pozwala regulować przy pomocy enkodera jasność świecenia diody LED 1
w module niebieskich diod świecących. Do obsługi enkodera wykorzystaj zdarzenia (events).

### [Zad2](L09/Zad2.py) - Odczyt parametrów środowiskowych z czujników DS18B20 oraz BME280 i ich wizualizacja poprzez diody WS2812

Napisz program, który wykorzystuje linijkę diod WS2812 do wizualizacji parametrów środowiskowych,
odczytanych z czujników DS18B20 oraz BME280, według schematu podanego przez Prowadzącego zajęcia.
Program może wykorzystywać interakcje przez konsolę tekstową i być sterowany poprzez przełączniki
przyciskane i enkoder.

## L10

### [Zad1](L10/Zad1.py) - Wyświetlanie na wyświetlaczu OLED wartości parametrów środowiskowych

Przygotuj program, który będzie odczytywał z czujnika BME280 wartości parametrów środowiskowych, 
które ten czujnik mierzy, i będzie wyświetlał je na ekranie OLED. Zilustruj wartości parametrów 
nie tylko jako wartości liczbowe, ale i za pomocą niewielkich symboli graﬁcznych, na przykład, 
piktogramów.

### [Zad2](L10/Zad2.py) - Rejestracja użycia kart RFID

Przygotuj program, który będzie reagował na przyłożenie karty do czytnika RFID, identyﬁkował 
tą kartę i rejestrował dokładny czas jej przyłożenia do czytnika. Zadbaj, aby karta przyłożona 
jednokrotnie, była zarejestrowana jeden raz, niezależnie jak długo pozostawała przyłożona do 
czytnika. O fakcie zarejestrowania przyłożenia karty poinformuj sygnałem dźwiękowym
z buzzera i wizualnym, na przykład, diodami programowalnymi LED WS2812.

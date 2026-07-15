# FNF Roblox Autoplayer (Beta)

Toto je automatizační skript pro hru FNF na platformě Roblox. Bot funguje na principu analýzy pixelů v reálném čase a simuluje stisky kláves.

**Stav projektu:** Beta (ve vývoji)

## Jak to funguje
Skript snímá konkrétní pixely na obrazovce. Pokud barva pixelu odpovídá barvě šipky, bot stiskne příslušnou klávesu. 

## Požadavky
* **Python** (doporučeno 3.10+)
* Knihovny: `mss`, `keyboard` (nainstaluješ přes `pip install mss keyboard`)
* **Důležité:** Skript musí být spuštěn s **právy správce (Administrator)**, jinak Windows nedovolí simulaci stisků kláves v prostředí hry.

## Návod k použití
1. Spusť skript.
2. Po spuštění se otevře menu.
3. Stiskni **F6** pro kalibraci:
    * Program tě vyzve k nastavení každého směru (Left, Down, Up, Right).
    * Najeď myší na cíl a stiskni **MEZERNÍK**.
4. Po dokončení kalibrace stiskni **Pravý Shift** pro spuštění bota.

## Tipy pro perfektní nastavení (Tuning)
Protože jde o pixel-bot, přesnost kalibrace určuje tvé skóre (Sick/Good/Bad).
* **Pozice snímání:** Pro dosažení "Sick" hodnocení zamiř kurzorem **těsně pod střed šipky**.
* **Hitbox:** Pokud bot netrefuje, ujisti se, že souřadnice jsou stále v aktivním poli noty.
* **Dlouhé noty:** Pokud bot dlouhé noty drží příliš krátce nebo dlouho, je nutné si s pozicí snímání "pohrát". Čím přesněji najdeš ideální bod v poli, tím lépe bude bot reagovat.
* **Omezení:** Kalibrace je vázaná na konkrétní okno hry. Pokud se změní pozice okna nebo rozlišení, je nutná re-kalibrace pomocí F6.

## Plány pro budoucí verze
* [ ] Ukládání kalibrace do JSON souboru (aby nebylo nutné nastavovat při každém spuštění).
* [ ] Optimalizace detekce dlouhých not.
* [ ] Vylepšení uživatelského rozhraní v konzoli.

---
*Projekt vytvořil Luno.*

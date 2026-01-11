**Dokumentace projektu: Správa přestupového trhu**

**1\. Základní informace**  
Název projektu: Správa přestupového trhu

Autor: Max Herich

Kontakt: max.herich@gmail.com

Datum vypracování: 6\. 1\. 2026

Název školy: SPŠE Ječná

Poznámka: Jedná se o školní projekt.

**2\. Specifikace požadavků (Use Case)**  
Cílem projektu je vytvoření informačního systému pro správu fotbalového přestupového trhu. Aplikace umožňuje evidenci klíčových entit fotbalového prostředí a realizaci procesů spojených s přestupy hráčů.

Klíčové případy užití (Use Cases):

Evidence entit: Přidávání a mazání hráčů, klubů, lig a majitelů. Import dat z csv souborů

Realizace přestupu: Proces převedení hráče z Klubu A do Klubu B, včetně kontroly rozpočtu.

Vyhledávání: Seznam všech přestupů, hráčů, klubů, lig a majitelů.

**3\. Architektura aplikace**  
Aplikace je navržena jako klient-server (nebo desktopová aplikace/konzolová aplikace nad databází). Architektura je rozdělena do vrstev:

Prezentační vrstva: Uživatelské rozhraní pro interakci s uživatelem.

Aplikační logika: Zpracování požadavků, validace vstupů.

Datová vrstva: Relační databáze uchovávající veškerá data.

**4\. Popis chování (Behaviorální diagramy)**  
Chod aplikace v klíčovém procesu "Realizace přestupu" lze popsat následovně:

Zahájení: Uživatel vybere hráče, cílový klub a cenu přestupu.

Validace: Systém ověří, zda má cílový klub dostatek financí.

Transakce: Provede se databázová transakce (odečtení peněz, změna klub\_id u hráče).

Stav Jednání: Pokud podmínky projdou, vytvoří se záznam o přestupu.

Ukončení: Pokud vše proběhne bez chyby, přestup se uloží do historie a hráč je převeden. V případě chyby se transakce vrátí (ROLLBACK).

**5\. Databázový model (E-R Model)**  
Jádrem projektu je relační databáze. Níže jsou uvedeny hlavní entity a jejich atributy.

Tabulky a entity:  
HRACI

id (PK, int): ID hráče.

jmeno (varchar): Jméno.

príjmeni(varchar): Příjmení.

cislo\_dresu(int): Číslo dresu.

pozice (enum): brankář, obránce, záložník, útočník.

id\_klubu (FK): Odkaz na aktuální klub.

KLUBY

id (PK, int): ID klubu.

nazev (varchar): Název klubu.

liga\_id (FK): Odkaz na ligu klubu

majitel\_id (FK): Odkaz na majitele klubu

LIGA

id (PK, int): ID ligy.

nazev (varchar): Název ligy.

zeme (varchar): Země ve které se liga hraje

uroven (enum): 1\. liga, 2\. liga, 3\. liga

MAJITELE

jmeno (varchar): Jméno.

príjmeni(varchar): Příjmení.

email (varchar): email majitele.

rozpocet (int): rozpočet majitele.

aktivni(bool): jestli majitel prave vlastni nejaky klub.

PRESTUPY

id (PK, int): ID přestupu.

hrac\_id (FK): Kdo přestupuje.

kupujici\_klub\_id (FK): Kam.

cena (float): Částka přestupu.

datum (date): Kdy se přestup stal.

**6\. Import dat**  
Data si po spuštění programu může uživatel importovat pomocí souboru csv

Formát csv: hodnota,hodnota,hodnota

**7\. Konfigurace aplikace**  
Konfigurace připojení k databázi se nachází v souboru config.json

**8\. Instalace a spuštění**  
Podrobný postup je uveden v souboru README.txt v kořenovém adresáři.

Stručný postup:

Ujistěte se, že máte nainstalován databázový server MYSQL

Spusťte SQL skript skript.sql pro vytvoření tabulek.

Nastavte přihlašovací údaje v konfiguračním souboru.

Stáhněte požadavky z requirements pomocí příkazu: py \-m pip install \-r requirements.txt

Spusťte aplikaci pomocí souboru run.bat

9\. Ošetření chybových stavů  
Aplikace ošetřuje kritické stavy a vypisuje chybové hlášky s kódy:

ERR-001 (Connection Failed): Nepodařilo se připojit k databázi. Zkontrolujte config soubor.

ERR-002 (Insufficient Funds): Majitel nemá dostatek prostředků na nákup hráče. Transakce zamítnuta.

ERR-003 (Invalid Data): Pokus o vložení záporné ceny nebo neexistujícího data. Ošetřeno databázovými CHECK constrainty.

ERR-004 (Duplicate Key): Pokus o vložení entity s již existujícím ID.

**10\. Použité knihovny třetích stran**  
Projekt využívá následující externí knihovny:

Databázový ovladač: mysql.connector \- pro komunikaci s DB.

UI Framework: Tkinter \- pro vykreslení rozhraní.

json a csv \- pro načítání souborů

(Pokud žádné, uveďte: "Projekt nevyužívá žádné nestandardní knihovny, pouze standardní knihovnu jazyka X.")

**11\. Závěr**  
Projekt "Správa přestupového trhu" naplnil stanovené požadavky. Byla vytvořena normalizovaná databáze a aplikace umožňující její správu. Systém úspěšně simuluje základní ekonomiku fotbalového trhu, kontroluje rozpočty a eviduje historii.
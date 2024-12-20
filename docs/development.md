# Kehittäjäohje

## Arkkitehtuuri

Kisapalvelu, Kipa, on puhdas web-applikaatio. Laskenta on toteutettu
Pythonilla. Web näkymät on rakennettu Django-ohjelmistokehyksen päälle,
joka on toteuttu pythonilla. Kaikki syötteet tallennetaan sqlite-kantaan,
jonka yhteydet hoitaa Django. SQLite-toiminnalisuus tulee Pythonin mukana.
Web-palvelimena on käytetty Apachea sekä djangon kehitysserveriä, mutta ei
pitäisi olla esteitä toteuttaa toiminnallisuutta millä tahansa
web-palvelimella joka tukee Pythonin suorittamista. Django tukee myös
MySQL- sekä PostegreSQL-kantoja, pienellä muutoksella settings.py
tiedostoon. Mikäli haluat rakentaa julkisen verkkopalvelun jossa voluumi
voi olla kovempi kannattaa tämä pitää mielessä.

## Suorituskyky ja skaalautuvuus

Normaalikäytössä ei Kipa nosta mainittavasti koneen CPU-kuormaa. Yhdellä
kannettavalla voidaan hyvin ajaa kisatoimiston palveluja. Piikkittäisiä
kuormituksia syntyy ainoastaan tulosten laskemisesta, isohkoissa
kilpailussa, jossa on tuhansia syötteitä, vie kaavojen parsiminen ja
laskenta isoille sarjoille joissain tapauksissa joitain sekunteja. Testien
mukaan kuorma kuitenkin säikeistyy käytössä olevien threadien määrän
mukaan - kuitenkin vain yksi per istunto.

Alkuperäisessä Kehitysvaiheessa on testejä ajettu pitkään (muinaisella)
850Mhz Pentiumilla jossa 128Mt muistia - tälläiselläkään koneella ei
suorituskykyongelmia tule muuta kuin hetkellisesti laskennassa.

Testimielessä Kipan kantaan on ajettu yhtäaikaa parikymmentä kilpailua
kokonaisuudessaan, jolloin syötteiden määrä on noussut tuhansiin, tällä ei
kuitenkaan ole nähty olevan vaikutusta suorituskykyyn.

## Paikallisen kehitysympäristön pystytys

* Luo Kipalle virtuaaliympäristö jonnekkin: `python -m venv /tmp/venv`
* Ota virtuaaliympäristö käyttöön: `source /tmp/venv/bin/activate`
* Asenna riippuvuudet: `pip install -r requirements.txt`
* Luo jonnekkin väliaikainen hakemisto tietokannalle: `mkdir /tmp/tietokanta`
* Kopioi kehitystietokanta: `cp docs/initial.db /tmp/tietokanta/kipa.db`
* `cp ./web/settings/local.py.example ./web/settings/local.py`
* Muokkaa edellisessä luotuun asetustiedostoon tietokantatiedostolle polku
  `/tmp/tietokanta/kipa.db`
* `cd web`
* `python manage.py migrate --fake-initial --noinput`
* `python manage.py runserver`

## Yksikkötestien ajaminen

* `cd web`
* `python manage.py test`

Kipaa voi myös käyttää testipalvelimen kanssa, joka on muuten samanlainen
kuin runserver, paitsi että se käyttää virtuaalista tietokantaa muistissa.
Ei tee mitään muutoksia tiedostoihin. Turvallinen erilaisiin kokeiluihin.
Voidaan täyttää halutulla tietokantapohjalla (fixture). esim.

```
python manage.py testserver fixtures/tests/katuu.xml
```

## Päästä päähän -testien ajaminen

* Käynnistä Kipan kehityspalvelin
* `python -m venv ./robot-venv`
* `source ./robot-venv/bin/activate`
* `pip install robotframework robotframework-seleniumlibrary`
* `robot --outputdir /tmp/test-report --variable BROWSER:headlessfirefox \
  --exitonfailure ./web/robot/perustoiminnot.robot`

Hakemistosta `./web/roobt` löytyy myös toinen robot-tiedosto nimeltään
`autentikointi.txt`, mutta sen ajaminen ei taida onnistua, ellei ensin
toteuta Kipaan suunniteltua kirjautumista.

## Python-koodin ja Django-templaattien formatointi

Koodi noudattaa Black-autoformatterin vesion 24.10.0 mukaista tyyliä.
Blackille annetaan lippu `--target-version py312`. Templaatit formatoidaan
käyttäen [djLint:tiä](https://www.djlint.com/), joka ajetaan seuraavasti:
`djlint --reformat --profile=django .`. Toisin kuin Black, djLint ei takaa
tiedostojen ehjänä pysymistä, joten muutosten tarkastaminen manuaalisesti
formatoinnin jälkeen voi olla tarpeen. Formatoinnit tarkastetaan osana
CI-putkea.

## Lintterit

Lintterit ajetaan osana CI-putkea, ja niiden löytämät ongelmat tulee
korjata ennen PR:ien mergeämistä tai avaamista katselmoitavaksi.

Django-templaattien tarkistamiseen käytetään lintteriä nimeltä djLint. Osa
säännöistä on poistettu käytöstä:

* H006: img-elementtien width- ja height-attribuutit
* H013: img-elementtien alt-attribuutti
* H030: sivujen metatiedot
* H031: sivujen avainsanat
* D018: {% url ... %} templaateissa
* T003: nimetyt endblock tagit templaateissa

## Selityksiä lähdekooditiedostoista

* `web/tupa/`
  - `admin.py`
    * Djangon luoman admin sivun määritely.
  - `AritmeettinenLaskin.py`
    * Laskin joka laskee matemaattisia lauekeita merkkijonosta jossa on
      merkejä +-/\*() sekä numeroita.
  - `duplicate.py`
    * Tiedon monistaminen. Tehtävien kopiointi, XML-tietokantatiedoston
      luonti.
  - `formit.py`
    * Perus formien määritys. Formeja käytetään näkymissä (views.py)
  - `logger.py`
    * Kirjaus, ja nauhoitus. Kirjaa laskimen välivaiheita. Nauhoittaa post
      dataa.
  - `models.py`
    * Django datamalli. Koko systeemin ydin.
    * Datamalliin pohjatuu sekä tietokanta että näkymät.
    * Myös laskin käyttää datamallia tiedon haussa.
  - `TehatavanMaaritys.py`
    * Tehtävän määrityksen formit.
  - `tests.py`
    * Yksikkötestit, Testaa järjestelmää erilaisilla testeillä.
      - Aritmeettisen laskimen perustoimitukset.
      - Sarjakohtaisten tulosten testaus.
      - Kaikkien näkymien avautuminen testidatalla.
      - Tiedon tallentuminen näkymillä.
  - `Tuloslaskin.py`
    * Laskee tulokset tietokannan tietojen pohjalta.
  - `urls.py`
    * Näkymien hakemistopolut.
  - `views.py`
    * Näkymät, jokaisen sivun aivot.
* `web/tupa/templates/`
  - `404.html`
  - `500.html`
  - `base.html`
* `web/tupa/templates/tupa/`
  - Näkymien templaatit
* `web/tupa/templates/tupa/forms/`
  - lomakekohtaiset templaatit
* `web/media/`
  - kuvat
  - css
  - yms. tiedostot

# Kehittäjäohje

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

## Python-koodin formatointi

Koodi noudattaa Black-autoformatterin vesion 24.10.0 mukaista tyyliä.
Blackille annetaan lippu `--target-version py312`. Formatointi tarkastetaan
osana CI-putkea.

# Kipa

Kipa-ohjelmisto, jota käytetään partiotaitokilpailujen tuloslaskentaan. 

Asennusohjeet löytyvät [wikistä](https://github.com/partio-scout/kipa/wiki).

## Lisenssi

Tämä ohjelma on vapaa; tätä ohjelmaa on sallittu levittää edelleen ja muuttaa GNU yleisen lisenssin (GPL-lisenssin) ehtojen mukaan sellaisina kuin Free Software Foundation on ne julkaissut Lisenssin version 3 mukaisesti.

Tätä ohjelmaa levitetään siinä toivossa, että se olisi hyödyllinen, mutta ilman mitään takuuta; ilman edes hiljaista takuuta kaupallisesti hyväksyttävästä laadusta tai soveltuvuudesta tiettyyn tarkoitukseen. Katso GPL-lisenssistä lisää yksityiskohtia.

Tämän ohjelman mukana pitäisi tulla kopio GPL-lisenssistä; jos näin ei ole, kirjoita osoitteeseen Free Software Foundation Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.


## Kehittäminen

### Paikallisen kehitysympäristön pystytys

* Luo jonnekkin väliaikainen hakemisto tietokannalle: `mkdir /tmp/tietokanta`
* Kopioi kehitystietokanta: `cp docs/initial.db /tmp/tietokanta/kipa.db`
* `cp ./web/settings/local.py.example ./web/settings/local.py`
* Muokkaa edellisessä luotuun asetustiedostoon tietokantatiedostolle polku `/tmp/tietokanta/kipa.db`
* `cd web`
* `python manage.py migrate --fake-initial --noinput`
* `python manage.py runserver`

### Yksikkötestien ajaminen

* `cd web`
* `python manage.py test`

### E2E-testien ajaminen

* Käynnistä Kipan kehityspalvelin
* `python3 -m venv ./robot-venv`
* `source ./robot-venv/bin/activate`
* `pip install robotframework robotframework-seleniumlibrary`
* `robot --outputdir /tmp/test-report --variable BROWSER:headlessfirefox --exitonfailure ./web/robot/perustoiminnot.robot`

Hakemistosta `./web/roobt` löytyy myös toinen robot-tiedosto nimeltään
`autentikointi.txt`, mutta sen ajaminen ei taida onnistua, ellei ensin toteuta
Kipaan suunniteltua kirjautumista.

### Python-koodin formatointi

Koodi noudattaa Black-autoformatterin vesion 24.10.0 mukaista tyyliä. Blackille annetaan lippu `--target-version py312`. Formatointi tarkastetaan osana CI-putkea.

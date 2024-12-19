# Asennusohjeet

## Kipan verkkoasennus

### Lähiverkko

Kaikkien tietokoneiden pitää olla samassa verkossa niin että niillä on
verkkoyhteys palvelimelle johon Kipa on asennettu. Palvelimelle tarvitaan
käytetty TCP-portti auki http-liikennöintiä varten. Jos kisatoimistosta ei
ole pääsyä Internettiin kannattaa harkita palomuurin sammuttamista
palvelimelta.

### Internet

On myös mahdollista asentaa Kipa julkisesti Internettiin jolloin kaikki
kisat ovat verkossa näkyvillä kaikille, tällöin kannattaa miettiä onko
turvallisuusriskinä, että kuka tahansa, jolla on osoite, voi mennä
muokkamaan kisan määrittelyitä ja tehtäviä. Lisäturvana kannattaa harkita
käyttäjäautentikoitia osoitteeseen jossa Kipa pyörii. Samoin rajoituksia
voi tulla syrjäseuduilla toimiville kisatoimistoille, joihin ei saada
riittävän hyvää verkkoyhteyttä.

## Docker-asennus

Suositeltu tapa ajaa Kipaa on Docker-kontissa ajaminen. Ainoa
ennakkovaatimus Kipa-koneelle on toimiva Docker-asennus tai vastaava.
Aloittelijaystävällisin tapa on Docker Desktop, jonka asennusohjeet
löytyy [täältä](https://docs.docker.com/desktop/).

Dockerin avulla Kipa-palvelin saadaan "eristettyä" omaksi kokonaisuudekseen
niin, ettei se häiritse muita koneen toimintoja. Kontti, johon Kipa on
valmiiksi asennettu, on saatavilla [GitHubin konttirekisteristä]
(https://github.com/partio-scout/kipa/pkgs/container/kipa).

Kipan saa käymään yksinkertaisimmillaan komennolla
`docker run -p 8000:80 --name kipa -d --volume kipa-volume:/db ghcr.io/partio-scout/kipa:latest`,
jonka jälkeen Kipan pitäisi löytyä selaimella osoitteesta
http://localhost:8000/kipa. Kipan käyttämä tietokanta tallennetaan
Docker-volumeen, eli Kipan kontin sammutaminen tai uudelleenkäynnistäminen
ei aiheuta tietokannan häviämistä.

Kipan sammuttaminen tapahtuu esimerkiksi komennolla `docker stop kipa`.
Uudelleenkäynnistys voidaan tämän jälkeen tehdä komennolla
`docker start kipa` tai sitten Kipa-kontti voidaan poistaa komennolla
`docker rm kipa`.

Mikäli haluaa käynnistää Kipasta kehitysversion se tapahtuu vaihtamalla
tagin `latest` tilalle `develop`.

## Asennus Nginx-proxyn taakse

Paremmin konfikuroitava ja joustavampi tapa ajaa Kipaa on ajaa sitä
WSGI-palvelin Gunicornin avulla käyttäen http-palvelin Nginx:ää proxynä.
Paikallisesti ajettuna Kipan SQLite-tietokannan sijainnin voi asettaa
johonkin sopivaksi katsottuun paikkaan: luo asetushakemistoon
`web/settings/` local.py, jossa asetetaan tietokannan polku. Tietokantana
voi myös käyttää jotakin muuta Djangon tukemaa tietokantaa.

Asennuksen vaiheet:

1. Asenna Nginx.
2. Asenna Kipan tukema Python.
3. Luo jonnekkin virtuaaliympäristö: `python -m venv /polku/venv`
4. Aktivoi virtuaaliympäristö: `source /polku/venv/bin/activate`
5. Asenna riippuvuudet: `pip install -r requirements.txt`
6. Siirry Kipan `web`-hakemistoon.
7. Aja Kipa gunicornin avulla:
   `gunicorn --daemon --bind unix:/tmp/kipa.sock wsgi`
   * Muilla kuin *unix pohjaisilla järjestelmillä voi bindata soketin
     sijasta oletusarvoiseen http-porttiin 8000: `gunicorn --daemon wsgi`
8. Konfiguroi Nginx ohjaamaan liikenne valitusta portista Gunicornin
   luomaan sokettiin tai sen kuuntelemaan TCP-porttiin.
9. Luo Nginx:än konfiguraatioon esim. alias, joka palvelee staattisten
   tiedostojen kyselyjä (`/kipamedia/*`) hakemistosta `web/media/`,
   varmista että Nginx-prosessin käyttäjällä on lukuoikeus kyseiseen
   hakemistoon.

Esimerkki Nginx:än konfikuraatiosta löytyy repositorion juuresta tai
sitten [Gunicornin dokumentaatiosta](https://docs.gunicorn.org/en/latest/deploy.html).

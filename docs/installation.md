# Asennusohjeet

## Kipan verkkoasennus

### Lähiverkko

Kaikkien tietokoneiden pitää olla samassa verkossa niin että niillä on
verkkoyhteys palvelimelle johon Kipa on asennettu. Yhteyden toimivuutta voi
kokeilla vaikka ping \<IP osoite\> komennolla. Palvelimelle tarvitaan
portti 80 auki http-liikennöintiä varten. Jos kisatoimistosta ei ole pääsy
Internettiin kannattaa harkita palomuurin sammuttamisesta palvelimelta.

### Internet

On myös mahdollista asentaa Kipa julkisesti Internettiin jolloin kaikki
kisat ovat verkossa näkyvillä kaikille, tällöin kannattaa miettiä onko
turvallisuusriskinä, että kuka tahansa, jolla on osoite, voi mennä
muokkamaan kisan määrittelyitä ja tehtäviä. Lisäturvana kannattaa harkita
käyttäjäautentikoitia osoitteeseen jossa Kipa pyörii. Samoin rajoituksia
voi tulla syrjäseuduilla toimiville kisatoimistoille, joihin ei saada
riittävän hyvää verkkoyhteyttä.

## Docker-asennus

1. Luo itsellesi GitHubin personal access
   token [täältä](https://github.com/settings/tokens) jakirjaudu
   Docker-clientillä sisään GitHubin pakettivarantoon esimerkiksi
   komennolla `docker login ghcr.io`
2. Aja komento `docker run -d -p 3000:3000 -v kipa_db:/app/db --name kipa -d ghcr.io/partio-scout/kipa:latest`
    * Halutessasi voit myös käyttää kehitysversiota vaihtamalla `latest`-tagin sijaan `develop`in.
3. Mene selaimella osoitteeseen http://localhost:3000/kipa/ – voilá!

Yllä opastettu ajotapa käyttää kipa_db-nimisessä Docker-volumessa olevaa
SQLite-kantaa. Sen sijaan voit käyttää esimerkiksi MySQL-kantaa
mounttaamalla erillisen local.py-tiedoston tähän tapaan:
`-v /home/user/kipa/local.py:/app/web/settings/local.py`. Voit myös yliajaa
muita settings/__init__.py:ssä olevia määrityksiä em. tavalla, esimerkiksi
ottaa käyttöön välimuistituksen.

## macOS-asennus

Toimivaksi todettu macOS Montereylla (12.0), luultavasti toimii myös
uudemmilla käyttöjärjestelmillä. Huom! Tämä ohje asentaa Kipan
kehityspalvelimen (development server).

macOS sisältää valmiiksi kaiken muun, paitsi itse Djangon. Sen asennus on
hyvin yksinkertainen ja onnistuu keneltä tahansa pääkäyttäjän oikeuksilla.

1. Avaa Terminal klikkaamalla oikeasta yläkulmasta suurennuslasia ja
   kirjoittamalla hakukenttään Terminal
2. Asenna Django kirjoittamalla terminaaliin
   `sudo easy_install django==1.3.1`  
   Anna salasanasi, jos terminaali sitä kysyy. Tämä asentaa Djangon
   uusimman saatavilla olevan version.
3. Hae Kipa GitHubista kirjoittamalla  
   `git clone https://github.com/partio-scout/kipa.git`  
   Jos et ole aiemmin käyttänyt Gittiä, tulee näytölle varmistus Command
   Line Developer Toolsin asentamisesta. Hyväksy asennus ja aja käsky
   uudelleen.
4. Hyväksy terminaalin mahdollinen kysymys palvelimen sertifikaatista.
5. Siirry Kipan web-hakemistoon kirjoittamalla `cd kipa/web`
6. Käynnistä Django ja Kipa `sudo python manage.py runserver`
7. Jos saat ilmoitukseksi “Development server is running at...”, voit avata
   selaimen (esim. Safari) ja kirjoittaa osoitteeksi 127.0.0.1:8000/kipa/

Kun lopetat Kipan käytön, siirry terminaaliin ja paina Ctrl+C, joka
pysäyttää Djangon.

## Linux-asennus

Pohjalle tarvitaan moderni Linux-käyttöjärjestelmä, testattu Ubuntu
20.04:lla

Huom! Ohjeessa {{kipa_asennus}} viittaa kansioon, johon Kipa on asennettu
(eli 2. Kohdassa .zip tiedosto purettu).

1. Lataa Kipa
   lähdekoodi [GitHubista](https://github.com/partio-scout/kipa/archive/refs/heads/master.zip)
2. Pura .zip tiedosto kansioon, johon haluat asentaa Kipa
3. Asenna tarvittavat paketit komennolla
   `sudo apt install apache2 python libapache2-mod-python mysql-server libmysqlclient-dev python-dev build-essential`

* Pythonin asennuksen jälkeen asenna pip, katso esim.
  ohjeet: https://stackoverflow.com/a/66719099
* Pip:n asennuksen jälkeen asenna vaadittava versio Djangosta ajamalla
  kipa-kansiossa komento pip install -r requirements.txt

4. Lisää /etc/apache2/apache2.conf tiedoston loppuun seuraavat rivit

        <Location "/kipa/">
          SetHandler python-program
          PythonHandler django.core.handlers.modpython
          SetEnv DJANGO_SETTINGS_MODULE web.settings
          PythonDebug On
          PythonPath "['{{kipa_asennus}}/kipa', '{{kipa_asennus}}/kipa/web'] + sys.path"
        </Location>

5. Aja seuraavat komennot

        chown www-data {{kipa_asennus}}/kipa/web
        chown www-data {{kipa_asennus}}/kipa/web/tupa.db
        ln -s {{kipa_asennus}}/kipa/web/media /var/www/html/kipamedia

6. Käynnistä apache2 uudestaan komennolla `sudo systemctl restart apache2`
7. Kipa pitäisi toimia nyt osoitteessa localhost://kipa/

## Windows-asennus

Lataa [asennustiedosto](https://github.com/partio-scout/kipa/releases/tag/1.6.2)
ja aja se. Testattu toimivaksi Windows 10 ja Windows XP.
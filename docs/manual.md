![](images/title.png)

# Kisapalvelu KIPA - Käyttöohje

## Näin pääset alkuun

Tervetuloa tutustumaan 2010-luvun partiotaitokilpailujen
tuloslaskentaohjelmistoon. Mikäli olet uusi Kipalle kokonaisuudessan
suosittelemme lukemaan vähintään kohdat asennus sekä tehtävien määritys.

Monet toiminnallisuudet ovat intuitiivisia ja ne on helppo päätellä,
toisaalta monessa paikassa voi olla apua lukea tämä ohje kattavasti läpi,
erityisesti tehtävien määritys menee jouhevammin, mikäli malttaa tutustua
dokumentaatioon ensin. Kipa tarjoaa monipuolisen tavan toteuttaa laskentaa
ja moni asia voidaan laskea helpommin koneellisesti, mitä aiemmin on
laskettu käsin.

Riemukkaita laskentahetkiä!

## Mikä on Kipa ja mitä sillä voi tehdä

### Yleistä

Kipa eli Kisapalvelu on partiokilpailujen tuloslaskentaa helpottamaan tehty
ohjelmisto. Kipa on helppokäyttöinen ja se on vapaasti levitettävissä sekä
muokattavissa. Ohjelmisto kehittyy edelleen joten tarkista aina uusimman
version saatavuus.

### Ominaisuudet

* **Selainkäyttö**: Kisatoimistossa koneet joilta tuloksia syötetään ei
  vaadi ohjelmien asentamista, Kipaa voi käyttää Internet-selaimella.
* **Monen käyttäjän tuki**: Kisatoimistossa voi syöttää usealla koneilla
  esimerkiksi eri sarjoja tai eri tehtäviä.
* **Tuomarineuvostofunktio**: Lasketun tuloksen voi korvata "kovalla
  arvolla" jos laskettu tulos ei jostain syystä kelpaa.
* **Tulokset Exceliin**: Tulokset saa ulos CSV-tiedostona joka helpottaa
  printtien yms. tekemistä.
* **Monta yhtäaikaista kilpailua**: Yhdelle palvelimille voidaan asentaa
  käytännössä ääretön määrä kilpailuja joita voivat muut koneet käyttää.
* **Tulosten syöttö kahteen kertaan**: Erityisesti SM-kilpailuita varten
  toteutettu ominaisuus jolla voidaan eliminoida kirjoitusvirheiden
  vaikutus.
* **Tuloslaskennen tilannenäkymä**: Graafinen näkymä helpottaa
  tuloslaskennan ja tarkastuksen etenemisen hahmottamista.
* **Ilmainen ja vapaasti kehitettävä**: Kipaa saa vapaasti levittää ja
  muokata kunhan edelleen kehitetyt versiot ovat vapaasti saatavilla myös
  muille.
* **Vapaa kaava**: Tehtävän kaava voidaan määrittää matemaattisesti lähes
  millaiseksi tahansa.
* **Valmiit tehtävämallit**: Yleisimpiä tehtäviä kuten suorasumma,
  interpolointi tai aikaväli varten on valmiit pohjat jotka nopeuttavat
  käyttöä.
* **Tehtävien kopiointi**: Sarjasta toiseen tai sarjan sisällä tehtävien
  kopiointi.
* **Windows- ja Linux-tuki**: Palvelin voidaan asentaa sekä Windows- &
  Linux-koneille, myös pilotoitu OS X -koneille.
* **Varmuuskopiointi**: Kilpailun tulokset voidaan tuoda XML-varmuuskopiona
  tai siirtää toiselle koneelle.
* **Tupan ominaisuudet**: Perinteikkään Tupan ominaisuudet on pyritty
  tuomaan mahdollisimman pitkälti myös Kipaan.

## Referenssit

Esimerkkejä kisoista, joita on laskettu Kipalla:

* Punkku 2009 - Harmaa Sarja
* Päpa Piirin kevät kisat 2010
* Peikon Puikaus 2010
* Letto \'10
* Punkku 2010
* Järvi-Suomen piirin Syyskisat 2011

## Miten Kipa toimii

Kipa asennetaan yhdelle tietokoneelle, jolta käsin voidaan syöttää
kilpailun tiedot ja tulokset. Kipan hienoutena on kuitenkin että samaa
kisaa voidaan verkon yli käyttää myös muilta päätteiltä, jotka voivat
periaatteessa olla mitä tahansa laitteitta, joissa on Internet-selain.
Kone, jolle Kipa on asennettu toimii palvelimena. Kaikki kisan tiedot
pidetään tallessa keskitetysti palvelinkoneella, jonka pitää luonnollisesti
olla päällä jotta muut koneet voivat olla siihen yhteydessä.

![](images/01.png)

Tyypillisesti Kipa asentuu Apache-ohjelmiston päälle, joka käynnistyy
samalla kun tietokone käynnistetään.

## Kipan käyttö

Kipa on kokonaisuudessaan web-applikaatio joten sen käytössä kannattaa
huomioida joitain yleisiä käyttöä helpottavia tekijöitä.

* Kun teet muutoksia Kipan tehtäviin, syötteisiin vartioihin yms. muista
  painaa aina lopuksi "Tallenna" sillä muuten menetät tekemäsi muutokset.
* Navigoidessa suosittelemme käyttämään mieluummin Kipan valikoita kuin
  selaimen takaisin tai eteenpäin nappuloita.

### Kisan luominen

Avaa Kipa auki http://localhost/kipa/ osoitteesta jos Kipa on asennettu
omalle koneellesi. Jos tulostoimistossa on monta konetta jotka syöttävät
samaa kilpailua katso kohta verkkokäyttö.

Valitse "Uusi Kisa"

Määrittele kisalle nimi ja ainakin yksi sarja.

Tallenna.

### Määritä vartiot

Valitse sarja.

Syötä vartion tiedot:

* **Nro**: Vartion numero
* **Nimi**: Vartion nimi
* **Keskeyttänyt**: Jos vartio keskeyttää, kirjataan ensimmäisen tekemättä
  jätetyn tehtävän tehtävänumero.
* **Ulkopuolella**: Jos vartio siirtyy kisan ulkopuolelle, kirjataan
  ensimmäisen kisan ulkopuolella suoritetun tehtävän numero. Kirjataan "1",
  mikäli vartio kisaa kisan ulkopuolella kisan alusta asti.
* **Poista**: Pistä ruksi jos haluat poistaa vartion (ei tarvitse tehdä
  tyhjille)

Paina lopuksi "Tallenna"

Huom! Mikäli vartio jossain vaiheessa keskeyttää tai siirtyy kilpailun
ulkopuolelta muista palata tänne määrittelemään tämä tieto.

### Tulosten syöttö

Tulosten syötössä syötetään jokaiseen tehtävään sen osatehtävien syötteet.
Kipa syöttää itse tiedon, mikäli vartio on kilpailun ulkopuolella tai
keskeyttänyt ja tällöin ei vartion syötteitä tarvitse tässä huomioida.
Muista merkitä vartiot ulkopuolelle / keskeyttäneeksi.

![](images/02.png)

Yllä olevassa kuvassa näkyy tehtävän, osatehtävien syötekentät. Vasemmalla
on ensimmäisen osatehtävän syötekentät, joihin syötetään raakapisteitä ja
oikealle puolelle jos vartio on ylittänyt ajan (-1 piste). Yllä on "
tarkistettu"-ruutu. Kun tämä ruutu on ruksittu ja tiedot tallennettu näkyy
laskennan tilanne alla että nämä tulokset on tarkistettu. Tätä voidaan
hyödyntää kisatoimistoissa, jossa käytetään kaksia silmiä tarkistamaan
syötteiden oikeellisuus.

![](images/03.png)

Mikäli vartion suoritus on hylätty syötetään h-kirjain vartion tulokseksi.
Ajan syötössä käyteään syötemuotoa HH:MM:SS kuten yllä näkyy.

### Tuplasyöte

Etusivun valikosta löytyy toiminto tuplasyöte. Tälle toiminnallisuudella on
käyttöä kilpailuissa joissa tulosten oikeellisuus pitää varmistaa
syöttämällä luvut kahteen kertaan kirjoitusvirheiden varalta.

Ensin syötetään tulokset normaalisti. Kun tehtävän tulokset on syötetty
kertaalleen voidaan tuloksia alkaa syöttämään toiseen kertaan. Painetaan "
Tallenna" kun syöttäminen on valmis.

![](images/04.png)

Järjestelmä näyttää punaisella solut, joiden syöte ei täsmää ensimmäisellä
kerralla syötettyyn.

### Tuomarineuvostyökalu

Työkalulla voi syöttää tuloksia vartioille joiden tulosta ei syystä tai
toisesta voida laskea normaalisti vaan se pitää syöttää "kovana arvona".
Jos tuloksissa näkyy yllättäviä arvoja, kannattaa tarkistaa, ettei
tuomarineuvostotyökaluun ole epähuomiossa syötetty arvoja.

![](images/05.png)

### Varmuuskopiointi / Vieminen / Palauttaminen

Kisan tiedot on mahdollista viedä talteen yhtenä XML-dumppina. Tälle voi
olla tarvetta, mikäli haluaa esimerkiksi tehdä jotain testailuja olemassa
olevaan konfiguraatioon, ottaa varmuuskopion tai viedä jollekkin toiselle
koneelle kilpailun kaikki tiedot.

![](images/06.png)

Tallenna kisa -toiminnolla saa XML-tiedoston, jonka voi tallentaa koneelle.
Palauta kisa -toiminnolla taas voidaan XML-tiedostosta palauttaa kisa.

### Laskennan tilanne

Laskennan tilanne -näkymästä näkee minkä tehtävien syötteet on syötetty
kokonaan/osittain/ei ollenkaan. Värit kertovat yhdessä näkymässä jokaisesta
sarjasta, miten pitkällä tehtävien syöttö on.

![](images/07.png)

![](images/08.png)

### Tulosten vienti CSV-tiedostoon

Jos tuloksia on tarvetta muokata, suodattaa tai tulostusnäkymää jalostaa on
helpointa viedä tulokset CSV-muotoon jolloin niitä voidaan muokata
esimerkiksi Excel-ohjelmalla. Tulosnäkymä sivulta löytyy jokaisen sarjan
tuloksille "Tulokset CSV tiedostoon"-painike, josta painettaessa ohjelma
antaa sarjan tulokset ulos yhtenä tiedostona.

![](images/09.png)

## Tehtävät yleistä

Ennen kuin tekee tehtävän määrittelyä on hyvä ymmärtää lyhyt oppimäärä
miten Kipa laskee tuloksia.

Kipassa on jokaisessa sarjassa erilliset tehtävät, tehtävät tulee
numeroida. Tehtävien numeroinnin tulee vastata järjestystä jossa sarjan
vartiot suorittavat tehtäviä. Jokainen tehtävä koostuu osatehtävistä, jotka
on nimetty a - z. Viittaukset osatehtävien nimiin syntyvät automaattisesti.
Tehtävän kaava on koostuu osatehtävien viittauksista. Jokainen osatehtävä
koostuu syötteistä joille tulee syöttää kuvaus tehtävän
määrittelyvaiheessa (esim. juoksuaika).

Kun selaa tehtäviä näkyvät tehtävänumerot ja numerot. Kun katsoo tehtävän
"ylätason" tietoja nähdään vastaavasti osatehtävien nimet ja niiden kaava.
Osatehtävillä on taas omat syötteensä ja kaavansa

![](images/10.png)

### Määritä tehtävät, yleisnäkymä

Jokaisella sarjalla on omat tehtävät. Saman nimisiä tehtäviä voi olla eri
sarjoissa ja kisoissa, mutta ne ovat laskennassa täysin irrallisia
toisistaan. Tulosten laskennassa esimerkiksi interpoloinnit menee sarjojen
sisällä.

Tehtäviä (nimi+määrittelyt) voi kopioida toisesta sarjasta. Kannattaa ensin
tehdä tehtävät yhteen sarjaan ja sen jälkeen kopioida ne muihin sarjoihin.
Yleisesti kannattaa tehdä ensin yksi sarja jossa on eniten tehtäviä ja sen
jälkeen duplikoida sarjan tehtävät myös muihin sarjoihin ja muuttaa
sopivilta osin mikäli tarvetta.

Valitse "Lisää tehtävä", kun olet tekemässä uutta tehtävää.

Kun haluat kopioida sarjan toisesta sarjasta, valitset ensin sarjan mihin
haluat kopioida, sen jälkeen valitse kopioi tehtävä ja sitten voit valita
mitkä tehtävät haluat kopioida sarjaasi.

![](images/11.png)

### Tehtävän kaavan määrittely

Syötä Nimi-kenttään vartion nimi ja Järjestysnumero-kenttään tehtävän
järjestysnumero, on tärkeää laittaa tehtävät oikeaan järjestykseen - muuten
kisan ulkopuolelle siirtyvät / keskeyttäneet vartiot ovat väärin mukana
tehtävien järjestyksessä. Järjestysnumeron pitää kuvata sitä järjestystä,
jossa vartiot kiertävät rataa.

![](images/12.png)

Tehtävän kaava on oletuksena ss (suorasumma) ja osatehtävien määrä on yksi.
Jos tehtävässä on yksi osatehtävä on silloin on ensimmäinen osatehtävän
nimi a. Kun osatehtävien määrä kasvaa aakkosjärjestyksessä osatehtävien
nimen viittaus tapahtuu kirjaimilla a -- z. Osatehtävät tulee näkyviin
allekkain a -- z.

Suurin osa tehtävistä lasketaan kaavalla ss - tällöin esimerkiksi ajasta
sekä kätevyydestä saadut pisteet lasketaan yhteen.

Esimerkkejä kehittyneemmistä kaavoista:

* `a-b` - Lasketaan esimerkiksi ajan pisteet, josta vähennetään
  sakkopisteet. Määritellään kaksi osatehtävää.
* `(a+b)/c` - Lasketaan yhteen kaksi kätevyyttä ja niiden summa jaetaan
  aikasakolla. Määritellään kolme osatehtävää.
* `b*2+a/c` - tehtävän pisteet\*2 + aika/sakolla

![](images/13.png)

Ja monimutkaisempaa laskentaa

![](images/14.png)

### Yleistä pistetyypistä interpolointi vs. kiinteät arvot

Interpoloinnnisa vartioiden suorituksia verrataan toisiinsa. Kiinteissä
arvoissa taas verrataan vartion suoritusta etukäteen järjestejien
asettamiin arvoihin tai maksimi/minimi arvoihin.

Interpolointitehtävissä, joissa paras suoritus on
mahdollisimman pieni arvo käytetään nollasuorituksen arvona
useimmiten 0.5 kertaa keskimmäinen suoritus. Vastaavasti jos suoritus on
sitä parempi, mitä suurempi tulos on, käytetään usein 1.5 kertaa
keskimmäinen suoritus arvoa.

Kipa tukee myös vaihtoista interpolointikerrointa. Kerroin voi olla
vaikka 0.9 jolloin jos vartio jää keskimmäisestä suorituksesta 10%
annetaan suoritukseksi nolla pistettä. Interpolointi kerrointa voi
muuttaa sen mukaan miten paljon odotetaan että vartioiden välillä on
hajontaa. Mikäli interpolointi kerroin on lähellä ykköstä on suuri
hajonta, kun kerroin kauempana luvusta 1 on pienempi hajonta vartioiden
välillä.

Kisan ulkopuolella olevia vartiota ei huomioida interpoloinnissa.

### Arviointi

Jossain tehtävätyypeissä on käytössä lisäksi arviointi. Tätä
käytetään silloin, kun vartioiden tehtävä on arvioida esimerkiksi puun
korkeutta, aikaa tms. Arviointia käytettäessä laitetaan ruksi
Arviointi-kenttään ja syötetään oikea vastaus.

![](images/15.png)

## Kipan osatehtävien määrittely

### Kisapisteiden määrittely

Kisapiste on kaikista yksinkertaisin pistetyyppi. Mikäli tehtävästä saa
esimerikiksi kuusi pistettä syötetään suoraan valmiita pisteitä väliltä
0 -- 6 syötteinä. Mikäli on tarvetta käyttää desimaalieroitinta on sekä
pilkun että pisteen käyttö mahdollista, esim 4,5 tai 4.50 tarkoittavat
samaa. Esimerkkinä tehtävästä on Ensiapu, jossa annetaan suoraan pisteitä
0-5 välillä. Kisapisteitä kuten kaikkia muitakin osatehtävätyyppejä voi
käyttää yksin tai yhdessä.

Kisapisteitä määritellessä syötetään vain kuvaus tehtävän määrittelyyn.

![](images/16.png)

### Raakapisteet

Raakapisteitä käytetään kun esimerkiksi kun vartio vastaa 30 kohdan
tietovisaan ja tarjolla on korkeintaan neljä pistettä. Silloin
muunnetaan että 4 kisapistettä saa 30 oikealla vastauksella. Samoin
raakapisteitä voidaan käyttää kun vartio heittää esimerkiksi keihästä.
Tällöin parhaat pisteet saa pisimmälle heittävä vartio, eikä etukäteen
voida määrittää maksimiarvoa johon vartion suoritusta verrattaisiin.

![](images/17.png)

### Raakapisteiden määrittely -- kiinteä

Esimerkki tehtävä, vartio vastaa 30 osaiseen tietovisaan. Maksimipisteet
4p.

Syötteen kuvaus kenttään laitetaan tässä tapauksessa oikeat vastaukset.

Parhaat pisteet saa kiinteä ja arvoksi valitaan 30 eli maksimi oikeat
vastaukset.

Kisapisteitä jaetaan 4.

Nollapistettä tulee kiinteällä suorituksella, eli 0 pistettä jos
halutaan että arviointi on lineaarinen välillä 0 -- 30.

### Raakapisteiden määrittely -- interpolointi

Esimerkki tehtävä, keihäänheitto. Vartion tehtävänä on heittää
mahdollisimman pitkälle keihästä. Maksipisteet 6p. 0.5 keskimmäinen
suoritus on 0p.

Syötteen kuvaus on heiton pituus. Parhaat pisteet saa suurin.
Kisapisteitä jaetaan 6p. Nollasuoritus on 0.5 kerroin.

### Kokonaisaika

Kokonaisaikaa käytetään silloin kun annettu aika on suoritusaika
sinänsä, eikä sitä tarvitse laskea aikojen erotuksesta. Esimerkiksi aika
jonka vartio jaksaa roikkua leuanvetotangossa joka on otettu
ajanottokellolla on kokonaisaikaa kun taas vartion saapumisaika maaliin
-- lähtöaika on aikaväli.

Ajansyöttömuoto on aina HH:MM:SS -- esimerkiksi 13:23:55.

Kipa tukee myös aikaformaatteja jotka ylittää vuorokauden - esimerkiksi
45:23:12. Tämä mahdollistaa, että vartioiden koko radan kiertoaikaa
voidaan mitata.

![](images/18.png)

### Kokonaisaika - kiinteät arvot

Esimerkki tehtävä, vartion pitää roikkua tangossa 5 minuuttia.
Maksimipisteet 10p.

Syötteen kuvaus on roikkumisaika. Maksimisuoritus on kiinteä -- 00:05:00.
Kisapisteitä jaetaan 10. Nollasuoritus kiinteä 00:00:00.

### Kokonaisaika -- interpolointi

Esimerkki tehtävä, vartion pitää läpäistä esterata mahdollisimman
nopeasti. Maksimipisteet 6p. 1.5\*keskimmäinen suoritus on 0p.

Syötteen kuvaus on suoritusaika. Parhaat pisteet saa pienin.
Kisapisteitä jaetaan 6p. Nollapisteen saa 1.5 kertoimella.

### Aikaväli

Aikavälin määrittäminen toimii samalla tavalla kuin kokonaisaika on
kuvailtu yllä. Ainoa ero määrittelyssa on, että tulee määritellä kaksi
syötettä. Useimmissa tapauksissa syötteet ovat alkuaika ja loppuaika.
Tällöin laskentalogiikka toimii täysin samoin kuin kuvattu
kokonaisajassa -- järjestelmä vain laskee lisäksi kokonaisajan aikavälin
syötteistä.

Kipa osaa huomioida myös vuorokauden ylittymisen.

### Vapaa kaava

Vapaa kaava mahdollistaa laskennallisesti monimutkaiset tehtävät.
Tärkeää vapaa kaavan kannalta on tietää, että aikojen yksikkö on
sekunti.

#### Esimerkki:

Yliaika kisapisteeseen vapaakaavassa \
pisteitä jaossa 5 \
20 minuutin suorituksella tulee 0 pistettä \
Syötteet:

* a=piste "Suorituspisteet"
* b=aika "Yliaika"

Vartion suorituksen kaava = `a*(1-b/(60*20))` \
Maksimisuoritus, kaava = `5` \
Maksimisuoritus, Montako kisapistettä jaetaan = `5` \
Nollasuoritus, kaava = `0`

![](images/19.png)

## Testausohjeita

### Yleistä

Kaikki ohjelmistot sisältävät virheitä ja emme suinkaan loukkaannu jos
ilmoitat löytäneesi bugin Kipasta -päinvastoin: koska projektin resurssit
ovat rajalliset, otamme erittäin mielellämme vastaan virheraportteja kuin
myös kehitysideoita. Muistathan vain sen, että kyseessä on
vapaaehtoisprojekti, jonka tekijät tekevät projektille työtä
vapaaehtoisesti ja omalla vapaa-ajallaan.

Virheraportitteja ja kehitysideoita voi toimittaa kehittäjille GitHubin
"issue"-toiminnon avulla. Issuen tekemiseen tarvitset toimivat
GitHub-tunnukset. Issueen on hyvä kirjoittaa kattava kuvaus ongelmasta tai
ideasta ja jakaa mahdollisimman paljon taustatietoa. Jos GitHubin käyttö ei
onnistu, voi kehittäjiin ottaa yhteyttä myös jollain muulla tavalla.

Virheet voidaan karkeasti jakaa laskimen ja käyttöliittymän kesken, alla
ohjeet kumpaakin tapausta varten:

### Virhe laskimessa

Tarkoittaen esimerkiksi sitä että huomaat Kipan laskevan tuloksia väärin.

1. Tee lyhyt kisa jossa esiintyy nimenomainen laskentaongelma. Nimeä kisa
   kuvaavasti.
2. Käytä Kipan toimintoa "Määrittele testituloksia", jonka löydät
   pääsivulta kohdasta "Kisan Määritykset". Kirjaa ylös oikeat
   laskentatulosket tehtävään.
3. Tallenna kisa XML-tiedostoksi toiminnolla "Tallenna kisa", jonka löydät
   pääsivulta, kohdasta "Ylläpito".
4. Toimita tallentamasi XML-tiedosto GitHub-issuen liitteenä, lisäämme
   kyseisen tiedoston testitapaukseksi automaattisiin yksikkötesteihin.

### Virhe käyttöliittymässä

1. Mieti hetki mitä olit tekemässä kun virhe tapahtui, yritä toistaa
   kyseinen tilanne.
2. Jos pystyt ja osaat, ota ruutukaappaus tilanteesta
3. Tallenna kisa XML-tiedostoksi kohdassa "Virhe laskimessa" annetuilla
   ohjeilla.
4. Tee GitHub-issue ja yritä kuvailla mitä olit tekemässä ja mitä tapahtui,
   kerro ainakin seuraavat asiat:
    - Käyttämäsi käyttöjärjestelmä (Windows, macOS, Linux...)
    - Käyttämäsi Internet-selain (Firefox, Chrome, Safari...)
    - ohjeet miten kyseisen vikatilanteen saa toistettua
    - kisatiedosto

## Verkkokäyttö

Kisapalvelu on suunniteltu tukemaan tuloslaskentatoimistoja, joissa on
useita henkilöitä syöttämässä ja tarkastamassa syötteitä samanaikaisesti.
Tällöin Kipa asennetaan vain yhdelle koneelle ja muut koneet käyttävät
selaimella yhdellä koneella pyörivää Kipaa verkon yli.

### Edut

* Samaa sarjaa voi syöttää vaikka kymmenen henkeä yhtäaikaa.
* Ohjelma asennetaan vain yhdelle koneelle.
* Clientit voivat olla mitä vain koneita, joissa on Internet-selain ja
  verkkoyhteys.
* Mahdollisuus näyttää joltain koneelta tuloksia sitä mukaan kun niitä
  syötetään muilta koneilta.

### Vaatimukset

* Lähiverkko, jossa tietokoneet ovat kiinni.
* Yksi tietokone johon on asennettu Kipa (palvelin). Palomuurin tulee
  sallia http-liikenne porttiin 80.
* n+1 kappaletta tietokoneita, joissa on Internet-selain (client).

### Tunnettuja ongelmia

* Verkkokäytössä jos useampi kuin yksi henkilö syöttää samaa tehtävää
  samalle sarjalle yhtä aikaa vain myöhemmin tallennettu syöttö
  tallentuu. Myöhemmin tallennettu korvaa aiemmin tallennetun.
* Tietokoneilla on esimerkiksi mokkula- ja WLAN-yhteys päällä yhtäaikaa
  ja siksi tietokone hakee palvelint väärää yhteyttä käyttäen.


## Lisenssi

Kipa on kokonaisuudessaan julkaistu GNU GPLv3 -lisenssin alla. Tämä
tarkoittaa, että kuka tahansa saa käyttää ilmaiseksi Kipaa niin ilmaisessa
kuin kaupallisessakin tarkoituksessa. Mikäli haluaa kuitenkin kehittää
järjestelmää eteenpäin vaadimme kunnioittamaan GNU GPLv3 -lisenssiä.

## Kaavat

### Lineaarinen interpolointi

Lineaarinen interpolointi tehdään kaavalla

![](images/20.png)

, jossa

```
x1 = nollat antava suoritus
y1 = 0
x2 = täydet antava suoritus
y2 = jaettavat pisteet
x = suoritus
```

, jolloin se sievenee muotoon

![](images/21.png)

, jonka toteuttaa pikafunktio: `interpoloi(x,x2,y2,x1)`.

### Osatehtävän kaavapohja

Jokaisen osatehtävän (poislukien kisapiste jonka kaava on `a`)
määritys pohjautuu samaan kaavapohjaan jonka parametrit vain vaihtelevat:

```
interpoloi(arvio(vartion_kaava-oikea),
    parhaan_haku(arvio(parhaan_kaava-oikea)),
    jaettavat,
    nollan_kerroin*tapa(arvio(nollan_kaava-oikea)))
```

### Kaavan syntaksi

Kaavoissa voi käyttää matematiikan perusoperaattoreita +-\*/, sulkuja sekä
Kipaan määritettyjä funktioita. Laskujärjestyksessä noudatetaan
matematiikan sääntöjä. Osatehtävän syötteisiin viitataan niiden nimillä
(a - z), jolloin ne tarkoittavat laskennassa kulloinkin olevan vartion
kyseistä syötettä. Hierarkiassa voi liikkua ylöspäin lisäämällä muuttujan
eteen pisteen. Esim. `.a` tarkoittaa kaikkien saman sarjan vartioiden
kyseisen suorituksen lukujoukkoa. Hierarkiassa voi liikkua mihin tahansa
tehtävään saman sarjan sisällä. Interpoloinneissa voidaan käyttää `muk`
lukujoukkoa suodatettamaan ulkopuoliset vartiot pois. (esim `.a*muk`)

Esimerkkejä:
```
(a+b+c)/3
.a
min(.a)
.a*muk
(.a+.b)*muk
..a.b
...ampuhmahaava.d.a
max(...pidempi:piipeli.a)
```

### Funktiot

* `min(lukujoukko)` hakee lukujoukon pienimmän arvon
* `max(lukujoukko)` hakee lukujoukon suurimman arvon
* `med(lukujoukko)` hakee lukujoukon mediaanin
* `avg(lukujoukko)` hakee lukujoukon keskiarvon
* `abs(luku)` laskee luvun itseisarvon
* `interpoloi(x,x2,y2,x1[,y1])` lineaarinen interpolointi
* `aikavali(alku,loppu)` kahden kellonajan välinen aika
* `sum(lukujoukko)` lukujoukon summa

### Parametrit

Parametrit ovat yksittäisiä palikoita, joiden avulla on helppo muokata
käyttöliittymästä haluttuja kaavan osia. Jokainen parametri on merkkijono,
jonka nimeä vastaava kohta kaavassa korvataan. Kaikki parametrit tulee
määrittää, joten käyttämättömät parametrit määritetään tyhjiksi.
Seuraavassa peruskaavan parametrit ja niiden arvovaihtoehdot.

- **arvio** - Arvionti käytössä:
    * `abs` (kaikki paitsi aikaväli)
    * "" eli tyhjä merkkijono (ei käytössä)
- **oikea** - Arviontitehtävän oikea vastaus
    * Desimaaliluku
    * `()` (ei käytössä)
- **vartions_kaava** - Vartion suorituksen laskentakaava
    * `a` (raakapiste, kokonaisaika)
    * `aikavali(a,b)` (alku- ja loppuaika)
    * Vapaamuotoinen kaava (vapaa kaava)
- **parhaan_haku** - Hakufunktio jos haetaan parasta suoritusta
    * `min` lukujoukon pienin (kaikki)
    * `max` lukujoukon suurin (kaikki)
- **parhaan_kaava** - Parhaan suorituksen kaava
    * `suor*muk` (kaikki) Kaikkien sarjassa mukana olevien vartioiden
      suoritusten lukujoukko.
    * vapaamuotoinen kaava (vapaa kaava)
- **jaettavat** - Tehtävässä jaettavat pisteet.
    * desimaaliluku (kaikki)
- **nollan_kerroin** - Kerroin interpoloinnin nollasuoritukselle
    * desimaaliluku (kaikki)
    * `1` (ei käytössä)
- **tapa** - keskimmäinen suorituksen laskutapa nollasuoritukselle.
    * `med` lukujoukon mediaani (kaikki)
    * `avg` lukujoukon keskiarvo (kaikki)
    * "" eli tyhjä merkkijono (ei käytössä)
- **nollan_kaava** - Nollasuorituksen kaava
    * `suor\*muk` (kaikk) Kaikkien sarjassa mukana olevien vartioiden
      suoritusten **vartion_kaava**-parametrillä laskettu lukujoukko.
    * vapaamuotoinen kaava (vapaa kaava)

`suor` = kaavalla lasketut kaikkien vartioiden suoritukset



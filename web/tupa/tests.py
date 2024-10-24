# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentaj�rjestelm� partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from __future__ import absolute_import
from __future__ import print_function
from decimal import Decimal
import sys
import unittest

from .taulukkolaskin import laske
from django.test import TestCase
from django.test.runner import DiscoverRunner
from .models import Kisa, OsaTehtava, Parametri, Sarja, Syote, Tehtava, TestausTulos
from .views import (
    kisa,
    kopioiTehtavia,
    korvaaKisa,
    laskennanTilanne,
    maaritaKisa,
    maaritaTehtava,
    maaritaValitseTehtava,
    maaritaVartiot,
    poistaKisa,
    sarjanTuloksetCSV,
    syotaKisa,
    syotaTehtava,
    tallennaKisa,
    tehtavanVaiheet,
    testiTulos,
    tulosta,
    tulostaSarja,
    tulostaSarjaHTML,
)
import os
from django.test.client import Client
from django.http import HttpRequest
import re
import settings


def is_number(s):
    if not s:
        return False
    try:
        float(s)
    except ValueError:
        return False
    return True


class aritmeettinen_laskin_test(unittest.TestCase):
    """
    Peruslaskimen unit testit
    """

    def testYhteenlasku(self):
        assert laske("5+5") == Decimal("10")

    def testYhteenlasku_spacet(self):
        assert laske(" 5 + 5 ") == Decimal("10")

    def testDesimaaliluku(self):
        assert Decimal(laske("0.5*2+10.5000")) == Decimal("11.5000")

    def testMuuttujavirhe(self):
        assert laske("tyhja_muuttuja*5") == "S"

    def testSulkulauseke(self):
        assert laske("2*(1+9)") == Decimal("20")

    def testSulut_sisakkain(self):
        assert laske("10*((1+2)+(5*10))") == Decimal("530")

    def testSulut_vaarinpain(self):
        assert laske("10*)(1+2)+(5*10))") == None

    def testSulut_vaaramaara(self):
        assert laske("10*(1+2)+(5*10))") == None

    def testNollallajako(self):
        assert laske("10/0") == None

    def testTyhjasyote(self):
        assert laske("") == None

    def testEiaritmtetiikkaa(self):
        assert laske("a+ b-c*d") == "S"

    def testkaksikertomerkkia(self):  # (potenssi)
        assert laske("5+2**5") == Decimal("37")

    def testkaksiplusmerkkia(self):
        assert laske("5+2++5") == Decimal("12")

    def testkaksimiinusmerkkia(self):
        assert laske("5+2--5") == Decimal("12")

    def testplusmiinus(self):
        assert laske("5+2+-5") == Decimal("2")

    def testkertojako(self):
        assert laske("5+2*/5") == None

    def testLaskettuNegatiivinenOperandi(self):
        assert laske("3*(1-5)") == Decimal("-12")

    def testPitkadesimaali(self):
        assert not laske("-0.008333333333333333333333333333*0.0") == None

    def testPerusmuuttuja(self):
        assert laske("a", {"a": 1}) == Decimal("1")

    def testPerusFunktio(self):
        assert laske("log(a)", {"a": Decimal("100")}) == Decimal("2")

    def testMinimiFunktio(self):
        assert laske("min(a)", {"a": Decimal("4")}) == Decimal("4")

    def testMedFunktio(self):
        assert laske("med(a)", {"a": Decimal("4")}) == Decimal("4")

    # def testMedFunktio2(self):
    #    assert laske('med(a)', {'a': {'a' : Decimal("4"),'b' : Decimal("5"),'c' : Decimal("6")} }) == Decimal("5")
    # Poistettu, koska nykyinen toteutsu ei toimi n�in, muutetaan vastaavaksi joskus...
    def testListaFunktio(self):
        assert laske("min([a,3,1])", {"a": Decimal("100")}) == Decimal("1")

    def testAbsMiinusparametri(self):
        assert laske("abs(-1)") == Decimal("1")

    def testSulkuMiinus(self):
        assert laske("(2)-1") == Decimal("1")


def haeTulos(tuloksetSarjalle, vartio, tehtava):
    # Mukana olevat
    sarjanTulokset = tuloksetSarjalle[0]
    for vart_nro in range(1, len(sarjanTulokset)):
        va = None
        for teht_nro in range(2, len(sarjanTulokset[vart_nro])):
            tul = sarjanTulokset[vart_nro][teht_nro]
            va = sarjanTulokset[vart_nro][0]
            if va == vartio and sarjanTulokset[0][teht_nro] == tehtava:
                return tul
    # Ulkopuoliset
    for vart_nro in range(0, len(tuloksetSarjalle[1])):
        va = None
        for teht_nro in range(2, len(tuloksetSarjalle[1][vart_nro])):
            tul = tuloksetSarjalle[1][vart_nro][teht_nro]
            va = tuloksetSarjalle[1][vart_nro][0]
            if va == vartio and tuloksetSarjalle[0][0][teht_nro] == tehtava:
                return tul


def ViewSanityCheck(fixture_name):
    """
    Luo testcasen tarkistamaan sen, ett� kaikki n�kym�t toimivat kaatumatta.
    fixture name = tietokantafixtuurin nimi jolle testi luodaan.
    palauttaa TestCase:n
    """

    class testi(TestCase):
        fixtures = [fixture_name]

        def testSanity(self):
            """
            Ajaa jokaisen n�kym�n testidatalla
            Testi antaa virheen jos jokin n�kuma kaatuu.
            """
            kisat = Kisa.objects.all()
            sarjat = Sarja.objects.all()
            tehtavat = Tehtava.objects.all()
            virheet = []
            request = HttpRequest()
            maaritaKisa(request)
            korvaaKisa(request)
            for k in kisat:  # Kisakohtaiset n�kym�t
                kisa_nimi = k.nimi
                kisa(request, kisa_nimi=kisa_nimi)
                maaritaKisa(request, kisa_nimi=kisa_nimi)
                maaritaValitseTehtava(request, kisa_nimi=kisa_nimi)
                maaritaVartiot(request, kisa_nimi=kisa_nimi)
                testiTulos(request, kisa_nimi=kisa_nimi)
                syotaKisa(request, kisa_nimi=kisa_nimi)
                laskennanTilanne(request, kisa_nimi=kisa_nimi)
                tulosta(request, kisa_nimi=kisa_nimi)
                tallennaKisa(request, kisa_nimi=kisa_nimi)
                poistaKisa(request, kisa_nimi=kisa_nimi)
            for s in sarjat:  # Sarjakohtaiset n�kym�t
                sarja_id = s.id
                kisa_nimi = s.kisa.nimi
                maaritaTehtava(request, kisa_nimi=kisa_nimi, sarja_id=sarja_id)
                kopioiTehtavia(request, kisa_nimi=kisa_nimi, sarja_id=sarja_id)
                tulostaSarja(request, kisa_nimi=kisa_nimi, sarja_id=sarja_id)
                sarjanTuloksetCSV(request, kisa_nimi=kisa_nimi, sarja_id=sarja_id)
                tulostaSarjaHTML(request, kisa_nimi=kisa_nimi, sarja_id=sarja_id)
            for t in tehtavat:  # teht�v�kohtaiset n�kym�t
                tehtava_id = t.id
                kisa_nimi = t.sarja.kisa.nimi
                maaritaTehtava(request, kisa_nimi=kisa_nimi, tehtava_id=tehtava_id)
                syotaTehtava(request, kisa_nimi=kisa_nimi, tehtava_id=tehtava_id)
                tehtavanVaiheet(request, kisa_nimi=kisa_nimi, tehtava_id=tehtava_id)

    return testi


def TulosTestFactory(fixture_name):
    """
    Tekee tulostestin halutulle tietokanta fixtuurille.
    fixture_name = fixtuurin nimi jolle testi tehd��n.
    palauttaa TestCase:n
    """

    class testi(TestCase):
        fixtures = [fixture_name]

        def testTulokset(self):
            """
            Iteroi jokaisen sarjan ja tehtavan.
            Laskee tulokset ja vertaa tuloksia maariteltyihin testituloksiin.
            Tunnistaa laskennan kaatavia virheita.
            Tunnistaa v��rat tulokset.
            Vaarien tulosten kohdalla tulostaa yhteenvedon.
            """
            settings.DEBUG = False
            self.sarjat = Sarja.objects.select_related().all()
            virheet = []
            settings.TAUSTALASKENTA = False
            settings.CACHE_TULOKSET = False
            settings.CACHE_BACKEND = "dummy:///"  # No cache in use
            for s in self.sarjat:
                virheilmoitus = unicode("")
                for f in self.fixtures:
                    virheilmoitus = virheilmoitus + f + " "

                virheilmoitus = virheilmoitus + "\nSarja: " + s.nimi + ""
                self.testausTulokset = TestausTulos.objects.select_related().filter(
                    tehtava__sarja=s
                )
                tulokset = s.laskeTulokset()
                for t in self.testausTulokset:
                    tulos = haeTulos(tulokset, t.vartio, t.tehtava)
                    vaadittava = t.pisteet
                    if not tulos == None and is_number(tulos):
                        tulos = Decimal(tulos)
                    if not vaadittava == None and is_number(vaadittava):
                        vaadittava = Decimal(vaadittava)
                    if vaadittava == None:
                        vaadittava = "None"
                    if tulos == None:
                        tulos = "None"
                    if not tulos == vaadittava or tulos == "None":
                        ilmoitus = virheilmoitus
                        ilmoitus = ilmoitus + "\nTehtava: " + t.tehtava.nimi
                        ilmoitus = ilmoitus + "\nKaava: " + t.tehtava.kaava
                        ilmoitus = ilmoitus + "\nOstatehtavien kaavat: "
                        for k in OsaTehtava.objects.filter(tehtava=t.tehtava):
                            ilmoitus = ilmoitus + "\n" + k.nimi + "=" + k.kaava + " "
                            ilmoitus = ilmoitus + "\n  Parametrit: "
                            for p in Parametri.objects.filter(osa_tehtava=k):
                                ilmoitus = (
                                    ilmoitus + "\n    " + p.nimi + "=" + p.arvo + " "
                                )
                            ilmoitus = ilmoitus + "\nSyotteet: "
                            for syo in Syote.objects.filter(
                                maarite__osa_tehtava=k
                            ).filter(vartio=t.vartio):

                                ilmoitus = (
                                    ilmoitus + syo.maarite.nimi + "=" + syo.arvo + " "
                                )
                        ilmoitus = ilmoitus + "\nVartio: " + t.vartio.nimi
                        ilmoitus = (
                            ilmoitus
                            + "\nTulos: "
                            + str(tulos)
                            + " != "
                            + str(vaadittava)
                        )
                        virheet.append(ilmoitus)
                for t in s.tehtava_set.all():
                    for v in s.vartio_set.all():
                        tulos = haeTulos(tulokset, v, t)
                        if tulos == None or tulos == "None":
                            ilmoitus = virheilmoitus
                            ilmoitus = ilmoitus + "\nTehtava: " + t.nimi
                            ilmoitus = ilmoitus + "\nTulos: " + str(tulos)
                            virheet.append(ilmoitus)

            virhe = str(len(virheet)) + " errors"
            for v in virheet:
                virhe = virhe + "\n--------------------------------\n" + v
            self.failUnless(
                len(virheet) == 0, unicode(virhe).encode("ascii", "replace")
            )
            sys.stdout.flush()

        def testTehtavanUudelleenTallennus(self):
            """
            Tallettaa jokaisen teht�v�n uudestaan.
            Tarkistaa ett� tulokset lasketaan t�m�nkin j�lkeen oikein.
            """
            # Kytket��n taustalaskenta pois p��lt� testin ajaki
            settings.DEBUG = False
            self.TAUSTALASKENTA = settings.TAUSTALASKENTA
            settings.TAUSTALASKENTA = None
            posti_vapaa = {}
            posti_puhdas = {}
            for s in Sarja.objects.select_related().all():
                for t in s.tehtava_set.all():
                    # Parsitaan post data html sivusta:
                    posti = {}
                    c = Client()
                    osoite = (
                        "/kipa/" + s.kisa.nimi + "/maarita/tehtava/" + str(t.id) + "/"
                    )
                    page = str(c.get(osoite).content)
                    page = page.replace("\n", "")
                    page = re.sub("\s+", " ", page)
                    all = re.findall(
                        '<input.*?type="(text|checkbox|radio)"+?(.*?)(>)', page
                    )
                    if all:
                        for i in all:
                            value = re.search("value=[\"'](.*?)[\"']", i[1])
                            name = re.search("name=[\"'](.*?)[\"']", i[1])
                            check = re.search("checked=[\"'](checked)[\"']", i[1])
                            if name and value:
                                if i[0] == "text":
                                    posti[name.group(1)] = value.group(1)
                                elif check:
                                    posti[name.group(1)] = value.group(1)

                    all = re.findall(
                        r'<select\s*?name=["\'](.*?)["\'].*?>(.*?)</select>', page
                    )
                    if all:
                        for i in all:
                            j = re.search(
                                "<(\s*?option.*?selected=[\"']selected[\"'].*?)>", i[1]
                            )
                            if j:
                                value = re.search("value=[\"'](.*?)[\"']", j.group(1))
                                if value:
                                    posti[i[0]] = value.group(1)
                    c.post(osoite, posti)
            self.testTulokset()
            settings.TAUSTALASKENTA = self.TAUSTALASKENTA

    return testi


def PostTestFactory(fixture_name):
    """
    Testi joka ajaa n�kymi� ennalta m��ritellyill� testdatoilla.
    """
    from xml.dom.minidom import parse

    class testi(TestCase):
        fixtures = [fixture_name]

        def testPost(self):
            doc = parse(fixture_name)
            post_requests = doc.getElementsByTagName("post_request")
            for p in post_requests:
                osoite = "/"
                if p.hasAttribute("address"):
                    osoite = p.getAttribute("address")
                inputs = p.getElementsByTagName("input")
                data = []
                for i in inputs:
                    if i.hasAttribute("name"):
                        param = [i.getAttribute("name"), None]
                        if i.hasAttribute("value"):
                            param[1] = i.getAttribute("value")
                        data.append(param)
                c = Client()
                posti = dict(data)
                c.post(osoite, posti)

    return testi


class TasapisteTesti(TestCase):
    """
    Testaa tasapisteissä määräävien tehtävien toimintaa.
    """

    fixtures = ["fixtures/tests/tasapisteet.xml"]

    def testJarjestys(self):
        sarja = Sarja.objects.get(nimi="tiukka")
        tulokset = sarja.laskeTulokset()
        assert tulokset[0][1][0].nro == 1
        assert tulokset[0][2][0].nro == 2
        assert tulokset[0][3][0].nro == 3
        assert tulokset[0][4][0].nro == 4
        assert tulokset[0][5][0].nro == 5
        assert tulokset[0][6][0].nro == 6


class CustomTestRunner(DiscoverRunner):
    def run_tests(
        self,
        test_labels=None,
        extra_tests=None,
        verbosity=1,
        interactive=True,
        failfast=True,
        **kwargs
    ):
        return run_one_fixture(test_labels, verbosity, interactive, extra_tests)


def run_one_fixture(test_labels, verbosity=1, interactive=True, extra_tests=[]):
    # ajetaan vain haluttu fixtuuri
    # Nollataan fixturet

    from django.test.utils import setup_test_environment, teardown_test_environment

    setup_test_environment()

    settings.DEBUG = False

    testit = [aritmeettinen_laskin_test]

    if test_labels:
        # print test_labels[0]
        # Jos testilabeliksi asetettu 'kisat', käytetään kisat-kansiota
        if test_labels[0] == "kisat":
            print("\n***Ajetaan kisa fixtuurit***\n")
            test_fixtures = []
            test_labels = ""

            for f in os.listdir(os.curdir + "/fixtures/tests/kisat/"):
                if not f.find(".xml") == -1:
                    print("Löytyi: %s\n" % f)
                    test_fixtures.append("fixtures/tests/kisat/" + f)
                    sys.stdout.flush()
                    # print ('Testataan fixtuurit: %s\n' %test_fixtures)

        # Jos testilabeliksi asetettu 'perus' ajetaan ainoastaan fixtures kansiosta löytyvät testit
        elif test_labels[0] == "perus":
            print("\n***Ajetaan perusfixtuurit***\n")
            test_fixtures = []

            for f in os.listdir(os.curdir + "/fixtures/tests/"):
                if not f.find(".xml") == -1:
                    print("Löytyi: %s\n" % f)
                    test_fixtures.append("fixtures/tests/" + f)
                    sys.stdout.flush()

        # Jos label on määritelty, muttei ole perus tai kisat, oletetaan sen olevan
        # ajettavaksi haluttu yksittäinen fixtuuri
        else:
            # Ajetaan vain yksi, annettu fixtuuri
            print("\n***Ajetaan yksi fixtuuri***\n")
            print("%s.xml\n" % test_labels[0])
            test_fixtures = []
            test_fixtures.extend(test_labels)
            for item in range(len(test_fixtures)):
                if test_fixtures[item].endswith(".xml"):
                    test_fixtures[item] = "%s/fixtures/tests/%s" % (
                        os.curdir,
                        test_fixtures[item],
                    )
                else:
                    test_fixtures[item] = "%s/fixtures/tests/%s.xml" % (
                        os.curdir,
                        test_fixtures[item],
                    )

    # Jos testilabelia ei ole määritelty ajetaan kaikki mahdolliset testit
    else:
        # Testeissä käytettävät fixturet:
        # haetaan kaikki xml fixtuurien nimet.
        print("\n***Ajetaan kaikki testifixtuurit***\n")
        test_fixtures = []
        print("\n***Ajetaan perusfixtuurit***\n")
        for f in os.listdir(os.curdir + "/fixtures/tests/"):
            if not f.find(".xml") == -1:
                print("Löytyi: %s\n" % f)
                test_fixtures.append("fixtures/tests/" + f)
                sys.stdout.flush()

        print("\n***Ajetaan kisa fixtuurit***\n")
        test_labels = ""
        for f in os.listdir(os.curdir + "/fixtures/tests/kisat/"):
            if not f.find(".xml") == -1:
                print("Löytyi: %s\n" % f)
                test_fixtures.append("fixtures/tests/kisat/" + f)
                sys.stdout.flush()

    # Tasapisteiss� m��r��v�t teht�v�t testi
    testit.append(TasapisteTesti)

    # luodaan Post testit tekstitiedostoista
    for t in test_fixtures:
        testit.append(PostTestFactory(t))

    # luodaan tulostestit fixtuureista.
    for t in test_fixtures:
        testit.append(TulosTestFactory(t))

    # luodaan viewtestit fixtuureista.
    for t in test_fixtures:
        testit.append(ViewSanityCheck(t))

    # suite = reorder_suite(suite, (TestCase,))
    suites = []
    for t in testit:
        suites.append(unittest.TestLoader().loadTestsFromTestCase(t))
    suite = unittest.TestSuite(suites)

    old_name = settings.DATABASES["default"]["NAME"]
    from django.db import connection

    connection.creation.create_test_db(verbosity, autoclobber=not interactive)
    result = unittest.TextTestRunner(verbosity=verbosity).run(suite)
    connection.creation.destroy_test_db(old_name, verbosity)

    teardown_test_environment()

    return len(result.failures) + len(result.errors)

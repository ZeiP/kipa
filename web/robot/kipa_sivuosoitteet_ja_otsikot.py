"""Kisan alasivujen URLit ja sivujen otsikot"""
# -*- coding: utf-8 -*-

# Testikisan nimimääritys, oletusarvona: testikisa
TESTIKISA = "testikisa"

# Kipa pääsivu

KIPA_OTSIKKO = "Kipa - kaikki kisat"
KIPA_URL = "http://127.0.0.1:8000/kipa"

# Suoritusten syöttö

TULOSTEN_SYOTTO_OTSIKKO = "Kipa - Syötä tuloksia"
TULOSTEN_SYOTTO_URL = "syota"

TULOSTEN_SYOTTO_TARKISTUS_OTSIKKO = "Kipa - Syötä\
 tuloksia - tarkistussyötteet"
TULOSTEN_SYOTTO_TARKISTUS_URL = "syota/tarkistus"

# Tulokset

TULOSTEN_TARKISTUS_OTSIKKO = "Kipa - Tulokset sarjoittain"
TULOSTEN_TARKISTUS_URL = "tulosta/normaali"

TUOMARINEUVOSTO_OTSIKKO = "Kipa - Tuomarineuvoston antamien\
 tulosten määritys"
TUOMARINEUVOSTO_URL = "maarita/tuomarineuvos"

LASKENNAN_TILANNE_OTSIKKO = "Kipa - Tulokset sarjoittain"
LASKENNAN_TILANNE_URL = "tulosta/tilanne"


# Kisan Määritykset

KISAN_MAARITYS_OTSIKKO = "Kipa - Määritä kisa"
KISAN_MAARITYS_URL = "maarita"

VARTIOIDEN_MAARITYS_OTSIKKO = "Kipa - Määritä vartiot"
VARTIOIDEN_MAARITYS_URL = "maarita/vartiot"

TEHTAVAN_MAARITYS_OTSIKKO = "Kipa - Muokkaa tehtävää"
TEHTAVAN_MAARITYS_URL = "maarita/tehtava"

TESTITULOKSIEN_MAARITYS_OTSIKKO = "Kipa - Testituloksien määritys"
TESTITULOKSIEN_MAARITYS_URL = "maarita/testitulos"

# Ylläpito

# huom Listaa kaikki kisat linkki vie pääsivulle
KAIKKI_KISAT_OTSIKKO = "Kipa - kaikki kisat"
KAIKKI_KISAT_URL = KIPA_OTSIKKO

# Tallenna kisa, ei vielä osaamista filen vastaanottoon, TBD
# "http://127.0.0.1:8000/kipa/testi_kisa/tallenna/

# Kisan tuonti tiedostosta, tod.näk helppoa käyttämällä fixtuuria.TBD
KISAN_TUONTI_URL = "korvaa"
KISAN_TUONTI_OTSIKKO = "Kipa - Korvaa kisa tiedostosta"

# Poista Kisa
KISAN_POISTO_OTSIKKO = "Kipa - Poista kisa"
KISAN_POISTO_URL = "poista"

# Autentikointi
admin_tunnus = "admin"
admin_salasana = "admin"

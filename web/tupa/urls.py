from __future__ import absolute_import
from functools import partial
from django.conf import settings
from django.urls import path
from django.views.static import serve

from .views import (
    apua,
    etusivu,
    heijasta,
    kisa,
    kopioiTehtavia,
    korvaaKisa,
    laskennanTilanne,
    loginSivu,
    logoutSivu,
    luoTestiTulokset,
    maaritaKisa,
    maaritaTehtava,
    maaritaValitseTehtava,
    maaritaVartiot,
    piirit,
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
    tuomarineuvos,
)

urlpatterns = [
    path("apua/", apua),
    path("", etusivu),
    path("<kisa_nimi>/tallenna/", tallennaKisa),
    path("login/", loginSivu),
    path("logout/", logoutSivu),
    path("lisaaKisa/", korvaaKisa),
    path("<kisa_nimi>/", kisa),
    path("uusiKisa/maarita/", maaritaKisa),
    path("<kisa_nimi>/korvaa/", korvaaKisa),
    path("<kisa_nimi>/poista/", poistaKisa),
    path("<kisa_nimi>/maarita/", maaritaKisa),
    path(
        "<kisa_nimi>/maarita/talletettu/", partial(maaritaKisa, talletettu="talletettu")
    ),
    path("<kisa_nimi>/maarita/tehtava/", maaritaValitseTehtava),
    path("<kisa_nimi>/maarita/tehtava/uusi/sarja/<int:sarja_id>/", maaritaTehtava),
    path("<kisa_nimi>/maarita/tehtava/<int:tehtava_id>/", maaritaTehtava),
    path(
        "<kisa_nimi>/maarita/tehtava/<int:tehtava_id>/talletettu/",
        partial(maaritaTehtava, talletettu="talletettu"),
    ),
    path("<kisa_nimi>/maarita/vaiheet/<int:tehtava_id>/", tehtavanVaiheet),
    path(
        "<kisa_nimi>/maarita/vaiheet/<int:tehtava_id>/<int:vartio_id>/", tehtavanVaiheet
    ),
    path("<kisa_nimi>/maarita/vartiot/", maaritaVartiot),
    path(
        "<kisa_nimi>/maarita/vartiot/talletettu/",
        partial(maaritaVartiot, talletettu="talletettu"),
    ),
    path("<kisa_nimi>/maarita/tehtava/kopioi/sarjaan/<sarja_id>/", kopioiTehtavia),
    path("<kisa_nimi>/maarita/testitulos/", testiTulos),
    path(
        "<kisa_nimi>/maarita/testitulos/talletettu/",
        partial(testiTulos, talletettu="talletettu"),
    ),
    path("<kisa_nimi>/luo/sarja/<sarja_id>/testitulokset/", luoTestiTulokset),
    path("<kisa_nimi>/maarita/tuomarineuvos/", tuomarineuvos),
    path(
        "<kisa_nimi>/maarita/tuomarineuvos/talletettu/",
        partial(tuomarineuvos, talletettu="talletettu"),
    ),
    path("<kisa_nimi>/syota/", syotaKisa),
    path("<kisa_nimi>/syota/tarkistus/", partial(syotaKisa, tarkistus=True)),
    path("<kisa_nimi>/syota/tehtava/<int:tehtava_id>/", syotaTehtava),
    path(
        "<kisa_nimi>/syota/tehtava/<int:tehtava_id>/talletettu/",
        partial(syotaTehtava, talletettu="talletettu"),
    ),
    path(
        "<kisa_nimi>/syota/tarkistus/tehtava/<int:tehtava_id>/",
        partial(syotaTehtava, tarkistus=True),
    ),
    path(
        "<kisa_nimi>/syota/tarkistus/tehtava/<int:tehtava_id>/talletettu/",
        partial(syotaTehtava, tarkistus=True, talletettu="talletettu"),
    ),
    path("<kisa_nimi>/tulosta/normaali/", tulosta),
    path("<kisa_nimi>/tulosta/normaali/sarja/<int:sarja_id>/", tulostaSarja),
    path("<kisa_nimi>/tulosta/tilanne/", laskennanTilanne),
    path("<kisa_nimi>/tulosta/heijasta/sarja/<int:sarja_id>/", heijasta),
    path("<kisa_nimi>/tulosta/heijasta/", heijasta),
    path("<kisa_nimi>/tulosta/tuloste/sarja/<int:sarja_id>/", tulostaSarjaHTML),
    path("<kisa_nimi>/tulosta/tuloste/", tulosta),
    path("<kisa_nimi>/tulosta/csv/sarja/<int:sarja_id>/", sarjanTuloksetCSV),
    path("<kisa_nimi>/tulosta/csv/", tulosta),
    path("<kisa_nimi>/tulosta/piirit/", piirit),
]

if settings.DEBUG:
    urlpatterns += [
        path(
            "kipamedia/<path>",
            serve,
            {"document_root": settings.STATIC_DOC_ROOT},
        ),
    ]

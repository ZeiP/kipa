# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from __future__ import absolute_import
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

from .views import *

tal = r"(?P<talletettu>(talletettu)?)/?$"

urlpatterns = [
    url(r"^apua/", apua),
    url(r"^$", etusivu),
    url(r"^post_txt/(?P<parametrit>[^/]+)/$", post_txt),
    url(r"^(?P<kisa_nimi>[^/]+)/tallenna/$", tallennaKisa),
    url(r"^login/$", loginSivu),
    url(r"^logout/$", logoutSivu),
    url(r"^lisaaKisa/$", korvaaKisa),
    url(r"^(?P<kisa_nimi>[^/]+)/$", kisa),
    url(r"^uusiKisa/maarita/$", maaritaKisa),
    url(r"^(?P<kisa_nimi>[^/]+)/korvaa/$", korvaaKisa),
    url(r"^(?P<kisa_nimi>[^/]+)/poista/$", poistaKisa),
    url(r"^(?P<kisa_nimi>[^/]+)/maarita/" + tal, maaritaKisa),
    url(r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/$", maaritaValitseTehtava),
    url(
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/uusi/sarja/(?P<sarja_id>\d+)/$",
        maaritaTehtava,
    ),
    url(
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/(?P<tehtava_id>\d+)/" + tal,
        maaritaTehtava,
    ),
    url(
        r"^(?P<kisa_nimi>[^/]+)/maarita/vaiheet/(?P<tehtava_id>\d+)/(?P<vartio_id>\d*)/?",
        tehtavanVaiheet,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/maarita/vartiot/" + tal, maaritaVartiot),
    url(
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/kopioi/sarjaan/(?P<sarja_id>\d+)/$",
        kopioiTehtavia,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/maarita/testitulos/" + tal, testiTulos),
    url(
        r"^(?P<kisa_nimi>[^/]+)/luo/sarja/(?P<sarja_id>\d+)/testitulokset/$",
        luoTestiTulokset,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/maarita/tuomarineuvos/" + tal, tuomarineuvos),
    url(r"^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)$", syotaKisa),
    url(
        r"^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)tehtava/(?P<tehtava_id>\d+)/"
        + tal,
        syotaTehtava,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/normaali/$", tulosta),
    url(
        r"^(?P<kisa_nimi>[^/]+)/tulosta/normaali/sarja/(?P<sarja_id>\d+)/$",
        tulostaSarja,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/tilanne/$", laskennanTilanne),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/sarja/(?P<sarja_id>\d+)/$", heijasta),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/$", heijasta),
    url(
        r"^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/sarja/(?P<sarja_id>\d+)/$",
        tulostaSarjaHTML,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/$", tulosta),
    url(
        r"^(?P<kisa_nimi>[^/]+)/tulosta/csv/sarja/(?P<sarja_id>\d+)/$",
        sarjanTuloksetCSV,
    ),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/csv/$", tulosta),
    url(r"^(?P<kisa_nimi>[^/]+)/tulosta/piirit/$", piirit),
]

if settings.DEBUG:
    urlpatterns += [
        url(
            r"^kipamedia/(?P<path>.*)$",
            serve,
            {"document_root": settings.STATIC_DOC_ROOT},
        ),
    ]

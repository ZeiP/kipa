# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from django.conf.urls import patterns
from models import *
from django.conf import settings

tal = r"(?P<talletettu>(talletettu)?)/?$"

urlpatterns = patterns(
    "tupa.views",
    (r"^apua/", "apua"),
    (r"^$", "etusivu"),
    (r"^post_txt/(?P<parametrit>[^/]+)/$", "post_txt"),
    (r"^(?P<kisa_nimi>[^/]+)/tallenna/$", "tallennaKisa"),
    (r"^login/$", "loginSivu"),
    (r"^logout/$", "logoutSivu"),
    (r"^lisaaKisa/$", "korvaaKisa"),
    (r"^(?P<kisa_nimi>[^/]+)/$", "kisa"),
    (r"^uusiKisa/maarita/$", "maaritaKisa"),
    (r"^(?P<kisa_nimi>[^/]+)/korvaa/$", "korvaaKisa"),
    (r"^(?P<kisa_nimi>[^/]+)/poista/$", "poistaKisa"),
    (r"^(?P<kisa_nimi>[^/]+)/maarita/" + tal, "maaritaKisa"),
    (r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/$", "maaritaValitseTehtava"),
    (
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/uusi/sarja/(?P<sarja_id>\d+)/$",
        "maaritaTehtava",
    ),
    (
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/(?P<tehtava_id>\d+)/" + tal,
        "maaritaTehtava",
    ),
    (
        r"^(?P<kisa_nimi>[^/]+)/maarita/vaiheet/(?P<tehtava_id>\d+)/(?P<vartio_id>\d*)/?",
        "tehtavanVaiheet",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/maarita/vartiot/" + tal, "maaritaVartiot"),
    (
        r"^(?P<kisa_nimi>[^/]+)/maarita/tehtava/kopioi/sarjaan/(?P<sarja_id>\d+)/$",
        "kopioiTehtavia",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/maarita/testitulos/" + tal, "testiTulos"),
    (
        r"^(?P<kisa_nimi>[^/]+)/luo/sarja/(?P<sarja_id>\d+)/testitulokset/$",
        "luoTestiTulokset",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/maarita/tuomarineuvos/" + tal, "tuomarineuvos"),
    (r"^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)$", "syotaKisa"),
    (
        r"^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)tehtava/(?P<tehtava_id>\d+)/"
        + tal,
        "syotaTehtava",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/normaali/$", "tulosta"),
    (
        r"^(?P<kisa_nimi>[^/]+)/tulosta/normaali/sarja/(?P<sarja_id>\d+)/$",
        "tulostaSarja",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/tilanne/$", "laskennanTilanne"),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/sarja/(?P<sarja_id>\d+)/$", "heijasta"),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/heijasta/$", "heijasta"),
    (
        r"^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/sarja/(?P<sarja_id>\d+)/$",
        "tulostaSarjaHTML",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/tuloste/$", "tulosta"),
    (
        r"^(?P<kisa_nimi>[^/]+)/tulosta/csv/sarja/(?P<sarja_id>\d+)/$",
        "sarjanTuloksetCSV",
    ),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/csv/$", "tulosta"),
    (r"^(?P<kisa_nimi>[^/]+)/tulosta/piirit/$", "piirit"),
)

if settings.DEBUG:
    urlpatterns += patterns(
        "",
        (
            r"^kipamedia/(?P<path>.*)$",
            "django.views.static.serve",
            {"document_root": settings.STATIC_DOC_ROOT},
        ),
    )

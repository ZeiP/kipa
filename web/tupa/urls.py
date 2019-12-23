# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi


from django.conf.urls import url
from django.conf import settings
from . import views

urlpatterns = [
        url(r'^apua/', views.apua, name='apua'),
        url(r'^$', views.etusivu, name='etusivu'),
        url(r'^post_txt/(?P<parametrit>[^/]+)/$', views.post_txt, name='post_txt'), 
        url(r'^(?P<kisa_nimi>[^/]+)/tallenna/$', views.tallennaKisa, name='tallennaKisa'), 
        url(r'^login/$', views.loginSivu, name='loginSivu'), 
        url(r'^logout/$', views.logoutSivu, name='logoutSivu'),
        url(r'^lisaaKisa/$', views.korvaaKisa, name='korvaaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/$', views.kisa, name='kisa'),
        url(r'^uusiKisa/maarita/$', views.maaritaKisa, name='maaritaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/korvaa/$', views.korvaaKisa, name='korvaaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/poista/$', views.poistaKisa, name='poistaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/$', views.maaritaKisa, name='maaritaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/$', views.maaritaValitseTehtava, name='maaritaValitseTehtava'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/uusi/sarja/(?P<sarja_id>\d+)/$', views.maaritaTehtava, name='maaritaTehtava'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/(?P<tehtava_id>\d+)/$' , views.maaritaTehtava, name='maaritaTehtava'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/vaiheet/(?P<tehtava_id>\d+)/(?P<vartio_id>\d*)/?' ,  views.tehtavanVaiheet, name='tehtavanVaiheet'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/vartiot/$',  views.maaritaVartiot, name='maaritaVartiot'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/tehtava/kopioi/sarjaan/(?P<sarja_id>\d+)/$', views.kopioiTehtavia, name='kopioiTehtavia'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/testitulos/$', views.testiTulos, name='testiTulos'),
        url(r'^(?P<kisa_nimi>[^/]+)/luo/sarja/(?P<sarja_id>\d+)/testitulokset/$', views.luoTestiTulokset, name='luoTestiTulokset'),
        url(r'^(?P<kisa_nimi>[^/]+)/maarita/tuomarineuvos/$' , views.tuomarineuvos, name='tuomarineuvos'),
        url(r'^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)$', views.syotaKisa, name='syotaKisa'),
        url(r'^(?P<kisa_nimi>[^/]+)/syota/(?P<tarkistus>(tarkistus/)?)tehtava/(?P<tehtava_id>\d+)/$', views.syotaTehtava, name='syotaTehtava'),
        url(r'^(?P<kisa_nimi>[^/]+)/nayta/tilanne/$', views.laskennanTilanne, name='laskennanTilanne'),
        url(r'^(?P<kisa_nimi>[^/]+)/nayta/(?P<muotoilu>[^/]+)/$', views.naytaValitse, name='nayta'),
        url(r'^(?P<kisa_nimi>[^/]+)/nayta/(?P<muotoilu>[^/]+)/piirit/$', views.piirinTulokset, name='piirit'),
        url(r'^(?P<kisa_nimi>[^/]+)/nayta/(?P<muotoilu>[^/]+)/(?P<sarja_id>\d+)/$', views.naytaSarja, name='naytaSarja'),
        ]


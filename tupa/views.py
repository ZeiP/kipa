# coding: latin-1
from models import *
from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
import operator
from decimal import *
from django import forms
import django.template
from logger import lokkeri

import re
from formit import *
from apina import *

def kisa(request,kisa_nimi) :
      kisa = get_object_or_404(Kisa, nimi=kisa_nimi) 
      return render_to_response('tupa/kisa.html', {'kisa' : kisa })

def tulosta(request,kisa_nimi):
      sarjat = Sarja.objects.filter(kisa__nimi=kisa_nimi)
      return render_to_response('tupa/tulosta.html', {'sarja_list': sarjat })

def maaritaKisa(request, kisa_nimi=None):
     # Tietokantahaku:
     kisa = None
     if kisa_nimi:
         kisa = get_object_or_404(Kisa, nimi=kisa_nimi)
     # Post data
     posti=None
     if request.method == 'POST':
          posti=request.POST
     # Kisa formi
     kisaForm = KisaForm(posti,instance=kisa)
     if kisaForm.is_valid():
         kisa=kisaForm.save()
     # Sarja formset
     sarjaFormit=SarjaFormSet(posti,instance=kisa)
     if sarjaFormit.is_valid():
         sarjaFormit.save()
     sarjaFormit.label="Sarjat"
     # Annetaan tiedot templatelle:
     if request.method == 'POST' and sarjaFormit.is_valid() and kisaForm.is_valid() :
         return HttpResponseRedirect("/tupa/"+kisa.nimi+"/maarita/")
     else :
         return render_to_response('tupa/maarita.html', 
                                      { 'heading' : "Määrita Kisa" ,
                                      'taakse' : "../" ,
                                      'forms' : (kisaForm,) ,
                                      'formsets' : ( sarjaFormit,) })

def maaritaValitseTehtava(request,kisa_nimi):
      sarjat = Sarja.objects.filter(kisa__nimi=kisa_nimi)
      taulukko = []
      for s in sarjat :
           taulut = Tehtava.objects.filter(sarja = s )
           for taulu in taulut:
               taulu.linkki = str(taulu.id)+"/"
               taulu.nimi = str(taulu.nimi)
           taulut.otsikko=s.nimi
           taulut.id=s.id
           taulukko.append(taulut)
      return render_to_response('tupa/maaritaValitseTehtava.html', { 'taulukko' : taulukko,
                                                                  'heading' : "Valitse tehtävä",
                                                                  'taakse' : "../" })
def maaritaVartiot(request,kisa_nimi):
      sarjat = Sarja.objects.filter(kisa__nimi=kisa_nimi)
      sarjaVartiot=[]
      posti=None
      post_ok=True
      taulukko=[]
      if request.method == 'POST':
          posti=request.POST
      for s in sarjat :
         vartioFormit=VartioFormSet(posti,instance=s,prefix=s.nimi )
         if vartioFormit.is_valid():
             vartioFormit.save() 
         else :
             post_ok=False
         vartioFormit.otsikko=s.nimi
         vartioFormit.id=s.id
         taulukko.append( vartioFormit )
      if posti and post_ok:
         return HttpResponseRedirect(reverse('web.tupa.views.maaritaVartiot', args=(kisa_nimi,)))
      else:
         return render_to_response('tupa/valitse_formset.html', { 'taulukko' : taulukko ,
                                                                  'heading' : "Määritä vartiot",
                                                                  'taakse' : "../../" })

def maaritaTehtava(request, kisa_nimi, tehtava_id=None, sarja_id=None):
    tehtava = None
    sarja = None
    if tehtava_id:
         tehtava=get_object_or_404(Tehtava, id=tehtava_id)
         sarja= tehtava.sarja
    else :
         sarja=get_object_or_404(Sarja, id=sarja_id)
    # Post Data
    posti=None
    if request.method == 'POST':
          posti=request.POST
    # Tehtävä
    tehtavaForm = TehtavaForm( posti,instance=tehtava,sarja=sarja )
    if tehtavaForm.is_valid() :
       tehtava=tehtavaForm.save()
    # Osapiste
    osaForm= kisapiste(tehtava, posti, prefix="osapiste")
    if osaForm.is_valid() :
       osaForm.save()
    osaForm.label="Kisapiste generaatio:"
    # Interpolointi
    interForm= interpoloi(tehtava, posti, prefix="interpoloi")
    if interForm.is_valid() :
       interForm.save()
    interForm.label="Interpolinti generaatio:"
    # Määritteet
    maariteFormit=MaariteFormSet(posti,instance=tehtava,prefix="maarite")
    if maariteFormit.is_valid() :
         maariteFormit.save() 
    maariteFormit.label="Syöteiden Määritteet"
    # Osapisteiden kaavat:
    kaavaFormit = KaavaFormSet(posti,instance=tehtava,prefix="kaava")
    if kaavaFormit.is_valid() :
         kaavaFormit.save()    
    kaavaFormit.label="Osapisteiden Kaavat"
    # Selaimelle:
 
    if posti and tehtavaForm.is_valid() :
       return HttpResponseRedirect("/tupa/"+kisa_nimi+"/maarita/tehtava/"+str(tehtava.id)+'/' )
    else:
       return render_to_response('tupa/maarita.html', 
                                      { 'heading' : "Maarita Tehtava" ,
                                      'taakse' : "../../../" ,
                                      'forms' : (tehtavaForm,osaForm,interForm,) ,
                                      'formsets' : ( maariteFormit,kaavaFormit,)})

def syotaKisa(request, kisa_nimi):
      sarjat = Sarja.objects.filter(kisa__nimi=kisa_nimi)
      taulukko = []
      for s in sarjat :
          tehtavat = s.tehtava_set.all()
          for t in tehtavat:
              t.linkki = "tehtava/"+str(t.id)+"/" 
          tehtavat.id=s.id
          tehtavat.otsikko=s.nimi
          taulukko.append( tehtavat )
      return render_to_response('tupa/valitse_linkki.html', { 'taulukko' : taulukko,
                                                                  'heading' : "Valitse tehtävä",
                                                                  'taakse' : "../" })

def syotaTehtava(request, kisa_nimi , tehtava_id) :
      tehtava = Tehtava.objects.filter(id=tehtava_id)[0]
      maaritteet = SyoteMaarite.objects.filter(tehtava=tehtava)
      vartiot = Vartio.objects.filter(sarja = tehtava.sarja )
      syoteFormit = []
      posti=None
      if request.method == 'POST':
          posti=request.POST

      for v in vartiot :
         rivi=[]
         for m in maaritteet :
              syotteet = Syote.objects.filter(vartio = v ).filter(maarite=m)
              syote=None
              formi=None
              if syotteet:
                  syote=syotteet[0]
              formi = SyoteForm(m,v,posti,instance=syote,prefix=v.nimi+m.nimi,)
              if formi.is_valid() :
                 formi.save()
              
              rivi.append( formi )
         syoteFormit.append( (v,rivi))

      return render_to_response('tupa/syota_tehtava.html', 
             { 'tehtava' : tehtava ,
               'maaritteet' : maaritteet ,
               'syotteet' : syoteFormit } )

def tulostaSarja(request, kisa_nimi, sarja_id) :
      sarja = Sarja.objects.get(id=sarja_id)
      lokkeri.clearLog()
      tulokset= sarja.laskeTulokset()
      return render_to_response('tupa/tulokset2.html', {'tulos_taulukko' : tulokset }  )

def sarja(request,sarja_id) :
      sarja= Kisa.objects.get(id=sarja_id)
      return render_to_response('tupa/sarja.html', {'sarja_object': sarja })

def piirit(request,kisa_nimi) :
      return HttpResponse(kisa_nimi + " PIIRIN TULOSTUS" )

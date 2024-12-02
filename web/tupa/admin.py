# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from __future__ import absolute_import
from django.contrib import admin
from .formit import KisaForm
from .models import (
    Kisa,
    OsaTehtava,
    Parametri,
    Sarja,
    Syote,
    SyoteMaarite,
    Tehtava,
    TestausTulos,
    TuomarineuvosTulos,
    Vartio,
)


class SarjaInline(admin.TabularInline):
    model = Sarja
    extra = 1


class ParametriInline(admin.TabularInline):
    model = Parametri
    extra = 1


class SyoteMaariteInline(admin.TabularInline):
    model = SyoteMaarite
    extra = 1


class OsaTehtavaInline(admin.TabularInline):
    model = OsaTehtava
    extra = 1


class KisaAdmin(admin.ModelAdmin):
    form = KisaForm
    inlines = [SarjaInline]


class KaavaInline(admin.TabularInline):
    model = OsaTehtava
    extra = 1


class TehtavaAdmin(admin.ModelAdmin):
    inlines = [OsaTehtavaInline]


class OsaTehtavaAdmin(admin.ModelAdmin):
    inlines = [ParametriInline, SyoteMaariteInline]


admin.site.register(Kisa, KisaAdmin)
admin.site.register(Sarja)
admin.site.register(Tehtava, TehtavaAdmin)
admin.site.register(Vartio)
admin.site.register(Syote)
admin.site.register(SyoteMaarite)
admin.site.register(TuomarineuvosTulos)
admin.site.register(TestausTulos)
admin.site.register(OsaTehtava, OsaTehtavaAdmin)
admin.site.register(Parametri)

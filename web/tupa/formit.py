from __future__ import absolute_import
from django.forms.models import modelformset_factory
from django import forms
from .models import (
    Kisa,
    OsaTehtava,
    Sarja,
    Syote,
    SyoteMaarite,
    Tehtava,
    TestausTulos,
    TuomarineuvosTulos,
    Vartio,
)
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from decimal import Decimal
import re
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class VartioForm(ModelForm):
    ulkopuolella = forms.IntegerField(
        widget=forms.TextInput(attrs={"size": "2"}), required=False
    )
    keskeyttanyt = forms.IntegerField(
        label="Keskeyttänyt",
        widget=forms.TextInput(attrs={"size": "2"}),
        required=False,
    )
    nro = forms.IntegerField(label="Nro", widget=forms.TextInput(attrs={"size": "4"}))

    class Meta:
        model = Vartio
        fields = [
            "nro",
            "nimi",
            "lippukunta",
            "piiri",
            "ulkopuolella",
            "keskeyttanyt",
        ]


VartioFormSet = inlineformset_factory(
    Sarja,
    Vartio,
    extra=30,
    form=VartioForm,
)

MaariteFormSet = inlineformset_factory(
    OsaTehtava, SyoteMaarite, extra=3, fields="__all__"
)


class SarjaForm(ModelForm):
    nimi = forms.CharField(label="Nimi")
    tasapiste_teht1 = forms.IntegerField(
        label="Tasapisteissä määräävät tehtävät: 1:",
        widget=forms.TextInput(attrs={"size": "3"}),
        initial=1,
    )
    tasapiste_teht2 = forms.IntegerField(
        label="2:", widget=forms.TextInput(attrs={"size": "3"}), initial=2
    )
    tasapiste_teht3 = forms.IntegerField(
        label="3:", widget=forms.TextInput(attrs={"size": "3"}), initial=3
    )
    vartion_maksimikoko = forms.IntegerField(widget=forms.HiddenInput, required=False)
    vartion_minimikoko = forms.IntegerField(widget=forms.HiddenInput, required=False)


SarjaFormSet = inlineformset_factory(
    Kisa,
    Sarja,
    extra=8,
    form=SarjaForm,
    fields=[
        "nimi",
        "tasapiste_teht1",
        "tasapiste_teht2",
        "tasapiste_teht3",
    ],
)
SarjaFormSet.helppiteksti = mark_safe(
    '<span onmouseover="tooltip.show(\'Sarjan <strong>nimet</strong> voivat sis&auml;lt&auml;&auml; &auml;&auml;kk&ouml;si&auml; ja v&auml;lily&ouml;ntej&auml;.<br><strong>Tasapisteiss&auml; m&auml;&auml;r&auml;&auml;v&auml;t teht&auml;v&auml;t</strong> -kohdat kertovat tasapisteiss&auml; m&auml;&auml;r&auml;&auml;vien teht&auml;vien numerot. Palaa t&auml;ytt&auml;m&auml;&auml;n ne m&auml;&auml;ritelty&auml;si kyseiset teht&auml;v&auml;t.\');" onmouseout="tooltip.hide();"><img src="/kipamedia/help_small.png" /></span>'
)


class TuhoaTehtavaForm(ModelForm):
    nimi = forms.CharField(widget=forms.HiddenInput, required=False)
    tehtavaryhma = forms.CharField(widget=forms.HiddenInput, required=False)
    tehtavaluokka = forms.CharField(widget=forms.HiddenInput, required=False)
    rastikasky = forms.CharField(widget=forms.HiddenInput, required=False)
    jarjestysnro = forms.CharField(widget=forms.HiddenInput, required=False)
    kaava = forms.CharField(widget=forms.HiddenInput, required=False)
    sarja = forms.ModelChoiceField(
        queryset=Sarja.objects.all(), widget=forms.HiddenInput, required=False
    )
    tarkistettu = forms.BooleanField(widget=forms.HiddenInput, required=False)
    lyhenne = forms.CharField(widget=forms.HiddenInput, required=False)
    maksimipisteet = forms.CharField(widget=forms.HiddenInput, required=False)
    svirhe = forms.BooleanField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Tehtava
        fields = []


tuhoaTehtaviaFormset = modelformset_factory(
    Tehtava, can_delete=True, extra=0, form=TuhoaTehtavaForm
)


class TehtavaLinkkilistaFormset(tuhoaTehtaviaFormset):
    def __str__(self):
        piirto = str(self.management_form)
        for form in self.forms:
            linkki = ""
            nimi = ""
            if form.instance:
                linkki = str(form.instance.id) + "/"
                nimi = str(form.instance.jarjestysnro) + ". " + str(form.instance.nimi)
            piirto = (
                piirto
                + "<a href="
                + linkki
                + ">"
                + nimi
                + "</a>  "
                + form.as_p()
                + "<br>"
            )
            piirto = piirto.replace("<p>", "").replace("</p>", "")
        return mark_safe(piirto)


class HelpWidget(forms.TextInput):
    """
    Help widget for help text labels
    """

    def __init__(self, helptext, *argcv):
        super(HelpWidget, self).__init__(*argcv)
        self.helptext = helptext

    def render(self, name, value=None, attrs=None, renderer=None):
        return mark_safe(
            super(HelpWidget, self).render(name, value, attrs, renderer)
            + "<span onmouseover=\"tooltip.show('"
            + self.helptext
            + '\');" onmouseout="tooltip.hide();"><img src="/kipamedia/help_small.png" /></span>'
        )


class AikaWidget(forms.TextInput):
    """
    Text input widget, exept for value formatting field values are converted from total seconds to "hh:mm:ss"
    """

    def render(self, name, value, attrs=None, renderer=None):
        newValue = value
        if newValue:
            try:
                float(newValue)
                arvo = Decimal(newValue)
                h = int(divmod(arvo, 60 * 60)[0])
                min = int(divmod(arvo, 60)[0] - h * 60)
                sec = int(arvo - (h * 60 * 60) - (min * 60))
                if h < 10:
                    h = "0" + str(h)
                if min < 10:
                    min = "0" + str(min)
                if sec < 10:
                    sec = "0" + str(sec)
                newValue = str(h) + ":" + str(min) + ":" + str(sec)
            except ValueError:
                pass
        return super(AikaWidget, self).render(name, newValue, attrs, renderer)


class PisteField(forms.CharField):
    """
    Decimal field accepting "kesk",h and ,/. as decimal delimiter
    """

    def clean(self, value):
        value = value.strip()
        haku = re.match(r"^((\d*)[,.]?\d+)$", value)
        if haku:
            merkkijono = "0" + haku.group(0)
            return str(Decimal(merkkijono.replace(",", ".")))
        if value == "kesk":
            return value
        elif value == "h":
            return "h"
        elif value == "H":
            return "h"
        elif value == "e":
            return "e"
        elif value == "E":
            return "e"
        elif value == "":
            return value
        else:
            raise forms.ValidationError("Anna desimaaliluku!")


class AikaField(forms.CharField):
    """
    Validates field input as "hh:mm:ss"
    Converts input to an string number, time in seconds.
    """

    def clean(self, value):
        value = value.strip()
        super(AikaField, self).clean(value)
        haku = re.match(r"^(\d+):(\d+):(\d+)$", value)
        if haku:
            return str(
                int(haku.group(1)) * 60 * 60
                + int(haku.group(2)) * 60
                + int(haku.group(3))
            )
        elif not value:
            return None
        elif value == "kesk":
            return value
        elif value == "h":
            return "h"
        elif value == "H":
            return "h"
        elif value == "e":
            return "e"
        elif value == "E":
            return "e"
        else:
            raise forms.ValidationError("Syötä aikaa muodossa: hh:mm:ss")


def initPisteSyote(self, fieldName):
    kesk = self.vartio.keskeyttanyt
    nro = self.maarite.osa_tehtava.tehtava.jarjestysnro
    if not kesk == None and not nro == None:
        if kesk <= nro:  # Keskeyttänyt
            self.fields[fieldName].widget.attrs["class"] = "kesk"
            self.fields[fieldName].widget.attrs["readonly"] = "readonly"
            self.initial[fieldName] = "kesk"


def savePisteSyote(self, syote, field, fieldName, alternateName):
    syote.maarite = self.maarite
    syote.vartio = self.vartio
    if self.cleaned_data[fieldName] or self.cleaned_data[alternateName]:
        field = self.cleaned_data[fieldName]
        syote.save()
    elif syote.id:
        syote.delete()


class PisteSyoteForm(ModelForm):
    arvo = PisteField(
        required=False, widget=forms.TextInput(attrs={"size": "16", "class": "numeric"})
    )
    tarkistus = PisteField(required=False, widget=forms.HiddenInput)

    def __init__(self, maarite, vartio, *argv, **argkw):
        super(ModelForm, self).__init__(*argv, **argkw)
        self.maarite = maarite
        self.vartio = vartio
        initPisteSyote(self, "arvo")

    def save(self):
        syote = super(ModelForm, self).save(commit=False)
        savePisteSyote(self, syote, syote.arvo, "arvo", "tarkistus")

    class Meta:
        exclude = ("maarite", "vartio")
        model = Syote


class PisteTarkistusForm(ModelForm):
    tarkistus = PisteField(
        required=False, widget=forms.TextInput(attrs={"size": "16", "class": "numeric"})
    )
    arvo = PisteField(required=False, widget=forms.HiddenInput)

    def __init__(self, maarite, vartio, *argv, **argkw):
        super(ModelForm, self).__init__(*argv, **argkw)
        self.maarite = maarite
        self.vartio = vartio
        initPisteSyote(self, "tarkistus")

    def save(self):
        syote = super(ModelForm, self).save(commit=False)
        savePisteSyote(self, syote, syote.tarkistus, "tarkistus", "arvo")

    class Meta:
        exclude = ("maarite", "vartio")
        model = Syote


class AikaSyoteForm(PisteSyoteForm):
    arvo = AikaField(
        required=False, widget=AikaWidget(attrs={"class": "time", "value": ""})
    )


class AikaTarkistusForm(PisteTarkistusForm):
    tarkistus = AikaField(
        required=False, widget=AikaWidget(attrs={"class": "time", "value": ""})
    )


def SyoteForm(*argv, **argkw):
    if argv[0].tyyppi == "aika":
        return AikaSyoteForm(*argv, **argkw)
    else:
        return PisteSyoteForm(*argv, **argkw)


def TarkistusSyoteForm(*argv, **argkw):
    if argv[0].tyyppi == "aika":
        return AikaTarkistusForm(*argv, **argkw)
    else:
        return PisteTarkistusForm(*argv, **argkw)


###############################################################
############## Tuomarineuvos ja TestiTulos ####################
###############################################################


def tulostauluFormFactory(tauluTyyppi):
    class tulostauluForm:
        def __init__(self, posti, vartio, tehtava, *argv, **argkw):
            self.taulu = None
            self.posti = posti
            self.errors = ""
            self.id = "tuomarineuvos_" + str(vartio.id) + "_" + str(tehtava.id)
            try:
                self.taulu = tauluTyyppi.objects.get(vartio=vartio, tehtava=tehtava)
            except tauluTyyppi.DoesNotExist:
                pass
            self.vartio = vartio
            self.tehtava = tehtava

        def is_valid(self):
            if self.posti and self.id in self.posti.keys():
                self.pisteet = self.posti[self.id]
                return 1
            else:
                return None

        def save(self):
            tulos = None
            if self.pisteet == None or len(self.pisteet) == 0 and self.taulu:
                self.taulu.delete()
            if self.pisteet and len(self.pisteet):
                tulos, created = tauluTyyppi.objects.get_or_create(
                    vartio=self.vartio, tehtava=self.tehtava
                )
                tulos.pisteet = self.pisteet
                tulos.save()
                self.taulu = tulos
            return tulos

        def __str__(self):
            formidata = {
                "name": self.id,
                "id": self.id,
                "value": "",
                "errors": self.errors,
            }
            if self.taulu:
                formidata["value"] = self.taulu.pisteet
            return render_to_string("tupa/forms/tulostaulu.html", dict(formidata))

    return tulostauluForm


TuomarineuvosForm = tulostauluFormFactory(TuomarineuvosTulos)
TestiTulosForm = tulostauluFormFactory(TestausTulos)

####################################################################


class KisaForm(ModelForm):
    nimi = forms.CharField(
        label="Nimi",
        widget=HelpWidget(
            helptext="Kisan yksil&ouml;llinen <strong>nimi</strong>. Ei saa sis&auml;lt&auml;&auml; erikoismerkkej&auml; eik&auml; v&auml;lily&ouml;ntej&auml;. &Auml;&auml;kk&ouml;set eiv&auml;t v&auml;ltt&auml;m&auml;tt&auml; toimi, jos Kipaa k&auml;ytet&auml;&auml;n Internet Explorerilla.<br><strong>Aika</strong> ja <strong>paikka</strong> ovat lis&auml;tietoja, jotka tulostuvat kisan tuloksiin."
        ),
    )

    def clean_nimi(self):
        nimi = self.cleaned_data["nimi"]
        nimi = re.sub(r"\s", "_", nimi)
        kisat = Kisa.objects.all()
        for k in kisat:
            if k.nimi == nimi and self.instance and not self.instance == k:
                raise forms.ValidationError("Nimi on jo käytössä")
        return nimi

    class Meta:
        model = Kisa
        fields = "__all__"


class UploadFileForm(forms.Form):
    file = forms.FileField()


class UploadFileNameForm(forms.Form):
    file = forms.FileField()
    name = forms.CharField(label="Tallennetaan nimelle")

    def clean_name(self):
        nimi = self.cleaned_data["name"]
        nimi = re.sub(r"\s", "_", nimi)
        kisat = Kisa.objects.all()
        for k in kisat:
            if k.nimi == nimi:
                raise forms.ValidationError("Nimi on jo käytössä")
        return nimi

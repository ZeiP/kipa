# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from __future__ import absolute_import
from django.template.loader import render_to_string
import re
import string
import operator
from decimal import Decimal

from .taulukkolaskin import laskeTaulukko
from .TulosLaskin import luoOsatehtavanKaava

# Lataamista varten:
from .models import OsaTehtava, Parametri, SyoteMaarite, Tehtava
from django.core import serializers

# Tehtävätyyppien kaavapohja:
maksimisuoritus = "parhaan_haku(arvio(parhaan_kaava-oikea))"
nollasuoritus = "nollan_kerroin*tapa(arvio(nollan_kaava-oikea))"
suoritus = "parhaan_haku([arvio(vartion_kaava-oikea)," + nollasuoritus + "])"
peruskaava = (
    "max(interpoloi("
    + suoritus
    + ","
    + maksimisuoritus
    + ",jaettavat,"
    + nollasuoritus
    + "))"
)


""" This file is made with no explainable logic. It has only been made to work. Most propably the best way to improveis simply rewriting. Anyway the task is not simple. Strongly recommend of using the already defined database syntax. See developement documentation for the actual syntax definition.
"""

#########################
# Validiointi funktiot: #
#########################
def is_number(s):
    if not s:
        return False
    try:
        float(s)
    except ValueError:
        return False
    return True


def is_string(s):
    if re.match("^\w+$", s.replace(" ", "_")):
        return True
    else:
        return False


def is_unicode_string(s):
    return True


def is_time(s):
    if re.match(r"^(\d+):(\d+):(\d+)$", s):
        return True
    else:
        return False


def is_kaava(s):
    if s == "":
        return False
    else:
        muuttujat = {}
        kaava = s.replace(".", "")
        haku = re.finditer("([a-zA-Z]+)(?!\w*[(])", kaava)
        numero = 1
        for h in haku:
            muuttujat[h.group(1)] = Decimal(numero)
            # numero+=1
        tulos = laskeTaulukko([[kaava]], muuttujat)
        if tulos[0][0] == None or tulos[0][0] == "S":
            return False
        else:
            return True


def validate(posti, field_name, testFunctions, prefix=""):
    id = prefix + "_" + field_name
    value = ""
    if posti and id in posti.keys():
        value = posti[id]
    valid = True
    for f in testFunctions:
        if f(value) == False:
            valid = False
            break
    return valid


####################
# Muunnosfunktiot: #
####################


def aika_numeroksi(s):
    haku = re.match(r"^(\d+):(\d+):(\d+)$", s)
    if haku:
        return str(
            int(haku.group(1)) * 60 * 60 + int(haku.group(2)) * 60 + int(haku.group(3))
        )
    else:
        return s


def numero_ajaksi(n):
    newValue = n
    if newValue:
        try:
            float(newValue)
            arvo = Decimal(newValue)
            h = divmod(arvo, 60 * 60)[0]
            min = divmod(arvo, 60)[0] - h * 60
            sec = arvo - (h * 60 * 60) - (min * 60)
            if h < 10:
                h = "0" + str(h)
            if min < 10:
                min = "0" + str(min)
            if sec < 10:
                sec = "0" + str(sec)
            newValue = str(h) + ":" + str(min) + ":" + str(sec)
        except ValueError:
            pass
    return newValue


###################
# Pohjapalikoita: #
###################
def syotteen_tyyppi_field(posti, data, prefix, syote_id, tyyppi):
    nimi = string.ascii_letters[syote_id]
    id = prefix + "_" + tyyppi + "_" + nimi + "_tyyppi"
    field_name = "tyyppi_" + nimi
    value = "piste"

    validi = True
    if "valid" in data.keys() and data["valid"] == False:
        validi = False

    # formin taytto
    if data["tyyppi"] == tyyppi or (not posti and (tyyppi == "vk" or tyyppi == "pk")):
        maarite_index = 0
        maaritteet = []
        for k, v in data["maaritteet"].items():
            maaritteet.append((v["nimi"], k))
        for m in sorted(maaritteet, key=operator.itemgetter(0)):
            k = m[1]
            v = data["maaritteet"][k]
            if maarite_index == syote_id:
                if "tyyppi" in v.keys():
                    value = v["tyyppi"]

                if posti and id in posti.keys():
                    value = value = posti[id]
                data["maaritteet"][k]["tyyppi"] = value

            maarite_index += 1
    # tilan tallennus
    formi = {field_name: {"id": id, "name": id, "value": value}}
    return formi


def field(posti, field_name, prefix, errors=""):
    id = prefix + "_" + field_name
    value = ""
    if posti and id in posti.keys():
        value = posti[id]
    return {field_name: {"id": id, "name": id, "value": value, "errors": errors}}


def save_data(data, data_path, data_nimi, data_field, value):
    pos = data
    for p in data_path:
        if not p in pos.keys():
            pos[p] = {}
        pos = pos[p]
        uusi = True
        for k, v in pos.items():
            if v["nimi"] == data_nimi:
                pos = pos[k]
                uusi = False
        if uusi:
            pos["#" + data_nimi] = {}
            pos["#" + data_nimi][data_field] = value
            pos["#" + data_nimi]["nimi"] = data_nimi
        else:
            pos[data_field] = value
            pos["nimi"] = data_nimi


def saveField(posti, data, field_name, data_path, nimi, field, prefix="", muunnos=None):
    id = prefix + "_" + field_name
    if posti and id in posti.keys():
        value = posti[id]
        if muunnos:
            value = muunnos(value)
        save_data(data, data_path, nimi, field, value)


def loadField(
    state, data, field_name, data_path, nimi, field, prefix=None, muunnos=None
):
    if prefix:
        id = prefix + "_" + field_name
    else:
        id = field_name
    pos = data
    for p in data_path:
        if not p in pos.keys():
            break
        pos = pos[p]
        for k, v in pos.items():
            if v["nimi"] == nimi:
                pos = pos[k]
    if "arvo" in pos.keys():
        if muunnos:
            state[id] = muunnos(pos["arvo"])
        else:
            state[id] = pos["arvo"]


def syotteen_kuvaus_field(posti, data, prefix, syote_id, tyyppi):
    formi = None
    errors = ""
    nimi = string.ascii_letters[syote_id]
    id = prefix + "_" + tyyppi + "_" + nimi
    value = ""
    field_name = "kali_vihje_" + nimi
    if posti and id in posti.keys():
        value = posti[id]

    if (
        posti
        and prefix in posti.keys()
        and posti[prefix] == tyyppi
        or not posti
        and (data["tyyppi"] == tyyppi or tyyppi == "pk" or tyyppi == "vk")
    ):
        # Formin data:
        if not "maaritteet" in data.keys():
            data["maaritteet"] = {}
        maarite_index = 0

        maaritteet = []
        for k, v in data["maaritteet"].items():
            maaritteet.append((v["nimi"], k))
        for m in sorted(maaritteet, key=operator.itemgetter(0)):
            k = m[1]
            v = data["maaritteet"][k]
            if maarite_index == syote_id:
                value = v["kali_vihje"]
                if posti and id in posti.keys():
                    value = posti[id]
                if value == "":
                    data["valid"] = False
                    errors = "Anna merkkijono!"
                formi = {
                    field_name: {"id": id, "name": id, "value": value, "errors": errors}
                }
                if not k in data["maaritteet"].keys():
                    data["maaritteet"][k] = {}
                data["maaritteet"][k]["nimi"] = nimi
                data["maaritteet"][k]["kali_vihje"] = value
            maarite_index += 1

        # Luonti jos puuttuu:
        if not formi:

            if posti and id in posti.keys():
                value = posti[id]
            formi = {
                field_name: {"id": id, "name": id, "value": value, "errors": errors}
            }
            data["maaritteet"]["#" + str(syote_id)] = {
                "nimi": nimi,
                "kali_vihje": value,
            }
    else:
        # valitsematon tyyppi
        if posti and id in posti.keys():
            value = posti[id]

        formi = {field_name: {"id": id, "name": id, "value": value, "errors": errors}}
    if not formi[field_name]["value"]:
        formi[field_name]["value"] = ""
    return formi


def poistaYlimaaraisetMaaritteet(posti, data, prefix, tyyppi, tarvittava_maara):
    if posti and prefix in posti.keys() and posti[prefix] == tyyppi:
        index = 0
        for k, v in data["maaritteet"].items():
            if index >= tarvittava_maara:
                if k > 0:
                    data["maaritteet"][-k] = v
                    del data["maaritteet"][k]
            index += 1


def lataa_parametrit(state, data, prefix, ot_tyyppi, muunnos=None):
    if "tyyppi" in data.keys() and (
        data["tyyppi"] == ot_tyyppi[1:]
        or (ot_tyyppi[1:] == "vk" and not data["tyyppi"] == "pk")
        or ot_tyyppi[1:] == "pk"
    ):
        loadField(
            state,
            data,
            "kiintea",
            ["parametrit"],
            "parhaan_kaava",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state,
            data,
            "jaettavat",
            ["parametrit"],
            "jaettavat",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state,
            data,
            "parhaan_haku",
            ["parametrit"],
            "parhaan_haku",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state,
            data,
            "nollan_kerroin",
            ["parametrit"],
            "nollan_kerroin",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state,
            data,
            "nollan_kaava",
            ["parametrit"],
            "nollan_kaava",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state, data, "oikea", ["parametrit"], "oikea", "arvo", prefix + ot_tyyppi
        )
        loadField(
            state,
            data,
            "kaava",
            ["parametrit"],
            "vartion_kaava",
            "arvo",
            prefix + ot_tyyppi,
        )
        loadField(
            state, data, "arvio", ["parametrit"], "arvio", "arvo", prefix + ot_tyyppi
        )

        if (
            ot_tyyppi[1:] == "pk" and not data["tyyppi"] == "pk"
        ):  # Puhdaskaavan generointi muista tyypeistä
            parametrit = {}
            loadField(
                parametrit,
                data,
                "parhaan_kaava",
                ["parametrit"],
                "parhaan_kaava",
                "arvo",
            )
            loadField(
                parametrit, data, "jaettavat", ["parametrit"], "jaettavat", "arvo"
            )
            loadField(
                parametrit, data, "parhaan_haku", ["parametrit"], "parhaan_haku", "arvo"
            )
            loadField(
                parametrit,
                data,
                "nollan_kerroin",
                ["parametrit"],
                "nollan_kerroin",
                "arvo",
            )
            loadField(
                parametrit, data, "nollan_kaava", ["parametrit"], "nollan_kaava", "arvo"
            )
            loadField(parametrit, data, "oikea", ["parametrit"], "oikea", "arvo")
            loadField(
                parametrit,
                data,
                "vartion_kaava",
                ["parametrit"],
                "vartion_kaava",
                "arvo",
            )
            loadField(parametrit, data, "arvio", ["parametrit"], "arvio", "arvo")
            loadField(parametrit, data, "tapa", ["parametrit"], "tapa", "arvo")
            state[prefix + ot_tyyppi + "_kaava"] = luoOsatehtavanKaava(
                peruskaava, parametrit
            )
        try:
            if not state[prefix + ot_tyyppi + "_parhaan_haku"] == "":
                state[prefix + ot_tyyppi + "_kiintea"] = ""
            else:
                if muunnos:
                    value = muunnos(state[prefix + ot_tyyppi + "_kiintea"])
                    state[prefix + ot_tyyppi + "_kiintea"] = value
        except:
            pass
        try:
            if not state[prefix + ot_tyyppi + "_nollan_kerroin"] == "1":
                state[prefix + ot_tyyppi + "_nollan_kaava"] = ""
            else:
                if muunnos:
                    value = muunnos(state[prefix + ot_tyyppi + "_nollan_kaava"])
                    state[prefix + ot_tyyppi + "_nollan_kaava"] = value
        except:
            pass
        try:
            kerroin = state[prefix + ot_tyyppi + "_nollan_kerroin"]
            if not kerroin == "1" and not kerroin == "1.5" and not kerroin == "0.5":
                state[prefix + ot_tyyppi + "_muu_kerroin"] = state[
                    prefix + ot_tyyppi + "_nollan_kerroin"
                ]
        except:
            pass
        try:
            if state[prefix + ot_tyyppi + "_arvio"] == "":
                state[prefix + ot_tyyppi + "_oikea"] = ""
            else:
                if muunnos:
                    value = muunnos(state[prefix + ot_tyyppi + "_oikea"])
                    state[prefix + ot_tyyppi + "_oikea"] = value

        except:
            pass


####################################
# Yleiset osatehtävien parametrit: #
####################################
def maksimisuoritus(
    state,
    data,
    prefix,
    ot_tyyppi,
    formi,
    validiointi=[[is_number], "Syötä numeroita!"],
    muunnos=None,
):
    # Valinnat:
    if prefix in state.keys() and state[prefix] == ot_tyyppi[1:]:
        saveField(
            state,
            data,
            "parhaan_haku",
            ["parametrit"],
            "parhaan_haku",
            "arvo",
            prefix + ot_tyyppi,
        )
    formi.update(field(state, "parhaan_haku", prefix + ot_tyyppi))
    # pienin/suurin:
    errors = ""
    if (
        state
        and prefix in state.keys()
        and state[prefix] == ot_tyyppi[1:]
        and state[prefix + ot_tyyppi + "_parhaan_haku"] == ""
    ):
        if not validate(state, "kiintea", validiointi[0], prefix + ot_tyyppi):
            data["valid"] = False
            errors = validiointi[1]
        else:
            saveField(
                state,
                data,
                "kiintea",
                ["parametrit"],
                "parhaan_kaava",
                "arvo",
                prefix + ot_tyyppi,
                muunnos,
            )

    try:
        if not state[prefix + ot_tyyppi + "_parhaan_haku"] == "":
            save_data(data, ["parametrit"], "parhaan_kaava", "arvo", "suor*muk")
    except:
        pass
    formi.update(field(state, "kiintea", prefix + ot_tyyppi, errors))
    # Jaettavat pisteet:
    errors = ""
    if state and prefix in state.keys() and state[prefix] == ot_tyyppi[1:]:
        if not validate(state, "jaettavat", [is_number], prefix + ot_tyyppi):
            errors = "Syötä numeroita!"
            data["valid"] = False
        else:
            saveField(
                state,
                data,
                "jaettavat",
                ["parametrit"],
                "jaettavat",
                "arvo",
                prefix + ot_tyyppi,
            )
    formi.update(field(state, "jaettavat", prefix + ot_tyyppi, errors))


def nollasuoritus(
    state,
    data,
    prefix,
    ot_tyyppi,
    formi,
    validiointi=[[is_number], "Syötä numeroita!"],
    muunnos=None,
):
    # Kiintea nolla
    errors = ""
    if (
        state
        and prefix in state.keys()
        and state[prefix] == ot_tyyppi[1:]
        and state[prefix + ot_tyyppi + "_nollan_kerroin"] == "1"
    ):
        if not validate(state, "nollan_kaava", validiointi[0], prefix + ot_tyyppi):
            data["valid"] = False
            errors = validiointi[1]
        else:
            saveField(
                state,
                data,
                "nollan_kaava",
                ["parametrit"],
                "nollan_kaava",
                "arvo",
                prefix + ot_tyyppi,
                muunnos,
            )
    formi.update(field(state, "nollan_kaava", prefix + ot_tyyppi, errors))
    # Kerroin valinnat:
    if state and prefix in state.keys() and state[prefix] == ot_tyyppi[1:]:
        kerroin = state[prefix + ot_tyyppi + "_nollan_kerroin"]
        save_data(data, ["parametrit"], "tapa", "arvo", "")
        if kerroin == "1.5" or kerroin == "0.5" or kerroin == "1":
            saveField(
                state,
                data,
                "nollan_kerroin",
                ["parametrit"],
                "nollan_kerroin",
                "arvo",
                prefix + ot_tyyppi,
            )
        if kerroin == "1.5" or kerroin == "0.5" or kerroin == "m":
            save_data(data, ["parametrit"], "tapa", "arvo", "med")
            save_data(data, ["parametrit"], "nollan_kaava", "arvo", "suor*muk")

    formi.update(field(state, "nollan_kerroin", prefix + ot_tyyppi))
    # Muu kerroin
    errors = ""
    if (
        state
        and prefix in state.keys()
        and state[prefix] == ot_tyyppi[1:]
        and state[prefix + ot_tyyppi + "_nollan_kerroin"] == "m"
    ):
        if not validate(state, "muu_kerroin", [is_number], prefix + ot_tyyppi):
            data["valid"] = False
            errors = "Syötä numeroita!"
        else:
            saveField(
                state,
                data,
                "muu_kerroin",
                ["parametrit"],
                "nollan_kerroin",
                "arvo",
                prefix + ot_tyyppi,
            )
    formi.update(field(state, "muu_kerroin", prefix + ot_tyyppi, errors))


def arviointi(
    state,
    data,
    prefix,
    ot_tyyppi,
    formi,
    validiointi=[[is_number], "Syötä numeroita!"],
    muunnos=None,
):
    # Arviointi
    errors = ""
    if state and prefix in state.keys() and state[prefix] == ot_tyyppi[1:]:
        saveField(
            state, data, "arvio", ["parametrit"], "arvio", "arvo", prefix + ot_tyyppi
        )
        if (
            prefix + ot_tyyppi + "_arvio" in state.keys()
            and state[prefix + ot_tyyppi + "_arvio"] == "abs"
        ):
            if not validate(state, "oikea", validiointi[0], prefix + ot_tyyppi):
                errors = validiointi[1]
                data["valid"] = False
            else:
                saveField(
                    state,
                    data,
                    "oikea",
                    ["parametrit"],
                    "oikea",
                    "arvo",
                    prefix + ot_tyyppi,
                    muunnos,
                )
        else:
            save_data(data, ["parametrit"], "arvio", "arvo", "")
            save_data(data, ["parametrit"], "oikea", "arvo", "0")
    formi.update(field(state, "oikea", prefix + ot_tyyppi, errors))
    formi.update(field(state, "arvio", prefix + ot_tyyppi))


###################################
# Osatehtäväkohtaiset kokoonpanot #
###################################
def kisaPisteForm(posti, data, prefix):
    formi = syotteen_kuvaus_field(posti, data, prefix, 0, "kp")
    poistaYlimaaraisetMaaritteet(posti, data, prefix, "kp", 1)
    if posti and prefix in posti.keys() and posti[prefix] == "kp":
        for k, v in data["maaritteet"].items():
            v["tyyppi"] = "piste"
        data["kaava"] = "a"
    return render_to_string("tupa/forms/kisa_piste.html", formi)


def raakaPisteForm(posti, data, prefix):
    formi = syotteen_kuvaus_field(posti, data, prefix, 0, "rp")
    poistaYlimaaraisetMaaritteet(posti, data, prefix, "rp", 1)
    if posti and prefix in posti.keys() and posti[prefix] == "rp":
        for k, v in data["maaritteet"].items():
            v["tyyppi"] = "piste"
        save_data(data, ["parametrit"], "vartion_kaava", "arvo", "a")
        data["kaava"] = peruskaava

    state = None
    # Aloitusarvot kannasta
    if not posti:
        state = {}
        lataa_parametrit(state, data, prefix, "_rp")
    else:
        state = posti.copy()
    formi.update(field(state, "parhaan_haku", prefix + "_rp"))

    maksimisuoritus(state, data, prefix, "_rp", formi)
    nollasuoritus(state, data, prefix, "_rp", formi)
    arviointi(state, data, prefix, "_rp", formi)

    return render_to_string("tupa/forms/raaka_piste.html", formi)


def kokonaisAikaForm(posti, data, prefix):
    formi = syotteen_kuvaus_field(posti, data, prefix, 0, "ka")
    poistaYlimaaraisetMaaritteet(posti, data, prefix, "ka", 1)
    if posti and prefix in posti.keys() and posti[prefix] == "ka":
        for k, v in data["maaritteet"].items():
            v["tyyppi"] = "aika"
        save_data(data, ["parametrit"], "vartion_kaava", "arvo", "a")
        data["kaava"] = peruskaava
    # Aloitusarvot kannasta
    if not posti:
        state = {}
        lataa_parametrit(state, data, prefix, "_ka", muunnos=numero_ajaksi)
    else:
        state = posti.copy()
    formi.update(field(state, "parhaan_haku", prefix + "_ka"))

    maksimisuoritus(
        state,
        data,
        prefix,
        "_ka",
        formi,
        validiointi=[[is_time], "Syötä hh:mm:ss!"],
        muunnos=aika_numeroksi,
    )
    nollasuoritus(
        state,
        data,
        prefix,
        "_ka",
        formi,
        validiointi=[[is_time], "Syötä hh:mm:ss!"],
        muunnos=aika_numeroksi,
    )
    arviointi(
        state,
        data,
        prefix,
        "_ka",
        formi,
        validiointi=[[is_time], "Syötä hh:mm:ss!"],
        muunnos=aika_numeroksi,
    )
    return render_to_string("tupa/forms/kokonais_aika.html", formi)


def aikaValiForm(posti, data, prefix):
    formi = syotteen_kuvaus_field(posti, data, prefix, 0, "ala")
    formi.update(syotteen_kuvaus_field(posti, data, prefix, 1, "ala"))
    poistaYlimaaraisetMaaritteet(posti, data, prefix, "ala", 2)
    if posti and prefix in posti.keys() and posti[prefix] == "ala":
        save_data(data, ["parametrit"], "arvio", "arvo", "")
        save_data(data, ["parametrit"], "oikea", "arvo", "0")
        for k, v in data["maaritteet"].items():
            v["tyyppi"] = "aika"
        save_data(data, ["parametrit"], "vartion_kaava", "arvo", "aikavali(a,b)")
        data["kaava"] = peruskaava
    # Aloitusarvot kannasta
    state = None
    if not posti:
        state = {}
        lataa_parametrit(state, data, prefix, "_ala", muunnos=numero_ajaksi)
    else:
        state = posti.copy()
    maksimisuoritus(
        state,
        data,
        prefix,
        "_ala",
        formi,
        validiointi=[[is_time], "Syötä hh:mm:ss!"],
        muunnos=aika_numeroksi,
    )
    nollasuoritus(
        state,
        data,
        prefix,
        "_ala",
        formi,
        validiointi=[[is_time], "Syötä hh:mm:ss!"],
        muunnos=aika_numeroksi,
    )
    return render_to_string("tupa/forms/aika_vali.html", formi)


def vapaaKaavaForm(posti, data, prefix):
    maara = 5
    if "maaritteet" in data.keys():  # Määritteet:
        maara = int(len(data["maaritteet"]))
        if posti and prefix + "_maaritteita" in posti.keys():
            maara = int(posti[prefix + "_maaritteita"])
        if maara > int(maara / 5) * 5:
            maara = int(maara / 5) * 5 + 5
        else:
            maara = int(maara / 5) * 5
    if posti and "lisaa_maaritteita" in posti.keys():
        maara = int(posti[prefix + "_maaritteita"]) + 5
    formit = []
    for i in range(maara):
        validi = True
        if "valid" in data.keys() and data["valid"] == False:
            validi = False
        formia = list(syotteen_kuvaus_field(posti, data, prefix, i, "vk").items())[0]
        formib = list(syotteen_tyyppi_field(posti, data, prefix, i, "vk").items())[0]
        if validi and "valid" in data.keys() and data["valid"] == False:
            del data["valid"]
        formit.append(
            {
                "kali_vihje": formia[1],
                "nimi": string.ascii_letters[i],
                "tyyppi": formib[1],
            }
        )

    if posti and prefix in posti.keys() and posti[prefix] == "vk":
        if "maaritteet" in data.keys():
            maaritteet = list(data["maaritteet"].copy().items())
            for i in range(maara):
                if maaritteet[i][1]["kali_vihje"] == "":
                    if type(maaritteet[i][0]) == str and maaritteet[i][0][:1] == "#":
                        del data["maaritteet"][maaritteet[i][0]]
                    else:
                        data["maaritteet"][-maaritteet[i][0]] = maaritteet[i][1]
                        del data["maaritteet"][maaritteet[i][0]]
        data["kaava"] = peruskaava

    poistaYlimaaraisetMaaritteet(posti, data, prefix, "vk", maara)

    formi = {
        "vapaa": True,
        "maaritteet": formit,
        "maaritteita": {"value": maara, "name": prefix + "_maaritteita"},
    }
    # Aloitusarvot kannasta
    if not posti:
        state = {}
        lataa_parametrit(state, data, prefix, "_vk")
    else:
        state = posti.copy()
    formi.update(field(state, "parhaan_haku", prefix + "_vk"))

    errors = ""
    if state and prefix in state.keys() and state[prefix] == "vk":
        if not validate(state, "kaava", [is_kaava], prefix + "_vk"):
            errors = "Kaava ei toimi!"
            data["valid"] = False
        saveField(
            state,
            data,
            "kaava",
            ["parametrit"],
            "vartion_kaava",
            "arvo",
            prefix + "_vk",
        )
    formi.update(field(state, "kaava", prefix + "_vk", errors=errors))

    maksimisuoritus(
        state, data, prefix, "_vk", formi, validiointi=[[is_kaava], "Kaava ei toimi!"]
    )
    nollasuoritus(
        state, data, prefix, "_vk", formi, validiointi=[[is_kaava], "Kaava ei toimi!"]
    )
    arviointi(
        state, data, prefix, "_vk", formi, validiointi=[[is_kaava], "Kaava ei toimi!"]
    )

    return render_to_string("tupa/forms/vapaa_kaava.html", formi)


################
# Puhdas kaava #
################
def puhdasKaavaForm(posti, data, prefix):
    maara = 5
    if "maaritteet" in data.keys():
        maara = int(len(data["maaritteet"]))
        if posti and prefix + "_maaritteita" in posti.keys():
            maara = int(posti[prefix + "_maaritteita"])
        if maara > int(maara / 5) * 5:
            maara = int(maara / 5) * 5 + 5
        else:
            maara = int(maara / 5) * 5
    if posti and "lisaa_maaritteita" in posti.keys():
        maara = int(posti[prefix + "_maaritteita"]) + 5
    formit = []
    for i in range(maara):
        validi = True
        if "valid" in data.keys() and data["valid"] == False:
            validi = False
        formia = list(syotteen_kuvaus_field(posti, data, prefix, i, "pk").items())[0]
        formib = list(syotteen_tyyppi_field(posti, data, prefix, i, "pk").items())[0]
        if validi and "valid" in data.keys() and data["valid"] == False:
            del data["valid"]
        formit.append(
            {
                "kali_vihje": formia[1],
                "nimi": string.ascii_letters[i],
                "tyyppi": formib[1],
            }
        )

    if posti and prefix in posti.keys() and posti[prefix] == "pk":
        if "maaritteet" in data.keys():
            maaritteet = list(data["maaritteet"].copy().items())
            for i in range(maara):
                if maaritteet[i][1]["kali_vihje"] == "":
                    if type(maaritteet[i][0]) == str and maaritteet[i][0][:1] == "#":
                        del data["maaritteet"][maaritteet[i][0]]
                    else:
                        data["maaritteet"][-maaritteet[i][0]] = maaritteet[i][1]
                        del data["maaritteet"][maaritteet[i][0]]
        data["kaava"] = "vartion_kaava"

    poistaYlimaaraisetMaaritteet(posti, data, prefix, "pk", maara)

    formi = {
        "vapaa": True,
        "maaritteet": formit,
        "maaritteita": {"value": maara, "name": prefix + "_maaritteita"},
    }

    # Aloitusarvot kannasta
    if not posti:
        state = {}
        lataa_parametrit(state, data, prefix, "_pk")
    else:
        state = posti.copy()
    # formi.update( field(state,"parhaan_haku",prefix+"_pk")  )

    errors = ""
    if state and prefix in state.keys() and state[prefix] == "pk":
        if not validate(state, "kaava", [is_kaava], prefix + "_pk"):
            errors = "Kaava ei toimi!"
            data["valid"] = False
        saveField(
            state,
            data,
            "kaava",
            ["parametrit"],
            "vartion_kaava",
            "arvo",
            prefix + "_pk",
        )
    formi.update(field(state, "kaava", prefix + "_pk", errors=errors))

    return render_to_string("tupa/forms/puhdas_kaava.html", formi)


##########################
# Osatehtävän kokoonpano #
##########################
def osaTehtavaForm(posti, data, prefix=""):
    # valitse tyyppi formi
    id = prefix + "_tyyppi"
    if posti and id in posti.keys():
        data["tyyppi"] = posti[id]
    otForm = {"id": id, "nimi": id, "value": data["tyyppi"]}
    if posti and data["tyyppi"] == "":
        data["valid"] = False
        otForm["errors"] = "valitse tyyppi"

    # tabit :
    taulukko = [
        {
            "id": data["nimi"] + "_kp",
            "otsikko": "Kisapiste",
            "tyyppi": "kp",
            "form": kisaPisteForm(posti, data, id),
        },
        {
            "id": data["nimi"] + "_rp",
            "otsikko": "Raakapiste",
            "tyyppi": "rp",
            "form": raakaPisteForm(posti, data, id),
        },
        {
            "id": data["nimi"] + "_ka",
            "otsikko": "Kokonaisaika",
            "tyyppi": "ka",
            "form": kokonaisAikaForm(posti, data, id),
        },
        {
            "id": data["nimi"] + "_ala",
            "otsikko": "Aikaväli",
            "tyyppi": "ala",
            "form": aikaValiForm(posti, data, id),
        },
        {
            "id": data["nimi"] + "_vk",
            "otsikko": "Vapaakaava",
            "tyyppi": "vk",
            "form": vapaaKaavaForm(posti, data, id),
        },
        {
            "id": data["nimi"] + "_pk",
            "otsikko": "Puhdaskaava",
            "tyyppi": "pk",
            "form": puhdasKaavaForm(posti, data, id),
        },
    ]

    return render_to_string(
        "tupa/forms/osa_tehtava.html",
        {
            "tab_id": data["nimi"],
            "nimi": data["nimi"],
            "taulukko": taulukko,
            "tyyppi": data["tyyppi"],
            "osatehtava": otForm,
        },
    )


#####################
# Tehtävän määritys #
#####################
def tehtavanMaaritysForm(
    posti, data, sarja_id, suurin_jarjestysnro=0, prefix="tehtava_", tags={}
):
    formidata = []
    # luodaan uusi tehtava jos vanhaa ei loydy
    if len(data.items()) == 0:
        """
        if not posti:
                data['#1']={'sarja' : sarja_id,
                                        'kaava': 'ss' ,
                                        'nimi': '' ,
                                        'jarjestysnro':suurin_jarjestysnro+1,
                                        'osa_tehtavat' : { '#1': { "nimi": "a","tyyppi": "" }  } }
        else :
        """
        data["#1"] = {
            "sarja": sarja_id,
            "kaava": "ss",
            "nimi": "",
            "lyhenne": "",
            "maksimipisteet": "",
            "jarjestysnro": suurin_jarjestysnro + 1,
            "osa_tehtavat": {},
        }

    data["valid"] = True
    if not posti:
        data["valid"] = False

    # Tehdaan kaikista tehtavista formi:
    for k, v in data.items():
        if not k == "valid":
            ot_formit = []

            # Osatehtavien maara kentta:
            osatehtavia = len(list(v["osa_tehtavat"].keys()))
            errors = ""
            if posti and prefix + str(k) + "_osatehtavia" in posti.keys():
                # Ja validiointi:
                if not is_number(posti[prefix + str(k) + "_osatehtavia"]):
                    errors = "Anna numero! "
                    data["valid"] = False
                elif int(posti[prefix + str(k) + "_osatehtavia"]) < 1:
                    errors = "Tehtävässä täytyy olla vähintään 1 osatehtävä!"
                    data["valid"] = False

                else:
                    osatehtavia = int(posti[prefix + str(k) + "_osatehtavia"])
            elif osatehtavia == 0:
                osatehtavia = 1

            formidata.append(
                (
                    "osatehtavia",
                    {
                        "id": prefix + str(k) + "_osatehtavia",
                        "name": prefix + str(k) + "_osatehtavia",
                        "value": osatehtavia,
                        "errors": errors,
                    },
                )
            )

            # Osatehtavien formien lisays, vanhojen poisto:
            osatehtava_id = 0
            osatehtavat = []
            for tk, tv in v["osa_tehtavat"].items():
                osatehtavat.append((tv["nimi"], tk))

            for ot in sorted(osatehtavat, key=operator.itemgetter(0)):
                tk = ot[1]
                tv = v["osa_tehtavat"][tk]
                if osatehtava_id < osatehtavia:
                    ot_formit.append(
                        osaTehtavaForm(posti, tv, prefix + str(k) + "_" + str(tk))
                    )
                    if "valid" in tv.keys() and tv["valid"] == False:
                        del tv["valid"]
                        data["valid"] = False
                    osatehtava_id = osatehtava_id + 1
                else:
                    v["osa_tehtavat"][-tk] = tv
                    del v["osa_tehtavat"][tk]

            # Uusien osatehtavien lisays:
            while osatehtava_id < osatehtavia:
                # lisataan uusi
                uusi_id = "#" + str(osatehtava_id)
                tId = k
                if k == "#1":
                    tId = None

                v["osa_tehtavat"][uusi_id] = {
                    "nimi": string.ascii_letters[osatehtava_id],
                    "tyyppi": "",
                    "kaava": "",
                    "tehtava": tId,
                }

                ot_formit.append(
                    osaTehtavaForm(
                        posti,
                        v["osa_tehtavat"][uusi_id],
                        prefix + str(k) + "_" + str(uusi_id),
                    )
                )
                if (
                    "valid" in v["osa_tehtavat"][uusi_id].keys()
                    and not v["osa_tehtavat"][uusi_id]["valid"]
                ):
                    del v["osa_tehtavat"][uusi_id]["valid"]
                    data["valid"] = False
                osatehtava_id = osatehtava_id + 1

            # Tehtavan kentat:
            for fk, fv in v.items():
                value = fv
                errors = ""
                id = prefix + str(k) + "_" + fk
                # post
                if posti and id in posti.keys():
                    value = posti[id]
                    # Numeroiden validiointi:
                    if fk == "jarjestysnro":
                        if not is_number(value):
                            errors = "Anna numero!"
                            data["valid"] = False
                    # Merkkijonojen validiointi:
                    if fk == "nimi":
                        if not is_string(value):
                            errors = "Anna merkkijono [a-zA-Za0-9_ ]!"
                            data["valid"] = False
                        else:
                            value = value.replace(
                                " ", "_"
                            )  # Korvataan väli alaviivalla.

                    if fk == "maksimipisteet":
                        if value and not is_number(value):
                            errors = "Anna numero!"
                            data["valid"] = False
                    if fk == "lyhenne":
                        if value and not is_unicode_string(value):
                            errors = "Anna merkkijono!"
                            data["valid"] = False
                    if (
                        fk == "rastikasky"
                    ):  # Estetään muiden kuin validien osotteiden syöttö
                        if value and not (
                            value.startswith("http://") or value.startswith("https://")
                        ):
                            errors = "Osoitteen alettava 'http://' tai 'https://'"
                            data["valid"] = False

                    # Kaavan validiointi:
                    if fk == "kaava":
                        if not is_kaava(value):
                            errors = "Kaava ei toimi!"
                            data["valid"] = False

                if not fk == "osa_tehtavat":
                    formidata.append(
                        (fk, {"id": id, "name": id, "value": value, "errors": errors})
                    )
                data[k][fk] = value
            formidata.append(("osa_tehtavat", ot_formit))
            # formidata.append( ('tehtava_id',k) )
            # formidata.append( ('kisa_nimi',) )
            tags.update(formidata)
    return render_to_string("tupa/forms/tehtava.html", tags)


########################
# Tietokannan muokkaus #
########################
def luoTehtavaData(tehtavat):
    """
    Luo sanakirjan tehtavista, niiden osatehtavista ,parametreista seka syotteiden maaritteista.
    """
    data = []
    objektit = []
    serialized = serializers.serialize("python", tehtavat)
    objektit.extend(tehtavat)
    for s in serialized:
        data.append([s["pk"], s["fields"]])
        osaTehtavat = OsaTehtava.objects.filter(tehtava__id=s["pk"])
        ots = serializers.serialize("python", osaTehtavat)
        ot_data = []
        objektit.extend(osaTehtavat)
        for ot in ots:
            # osa_tehtava
            ot_data.append([ot["pk"], ot["fields"]])
            # parametrit

            parametrit = Parametri.objects.filter(osa_tehtava__id=ot["pk"])
            objektit.extend(parametrit)
            pser = serializers.serialize("python", parametrit)
            p_data = []
            for p in pser:
                p_data.append([p["pk"], p["fields"]])
            ot_data[-1][1]["parametrit"] = dict(p_data)
            # maaritteet
            maaritteet = SyoteMaarite.objects.filter(osa_tehtava__id=ot["pk"])
            objektit.extend(maaritteet)
            mser = serializers.serialize("python", maaritteet)
            m_data = []
            for m in mser:
                m_data.append([m["pk"], m["fields"]])
            ot_data[-1][1]["maaritteet"] = dict(m_data)
        data[-1][1]["osa_tehtavat"] = dict(ot_data)
    return dict(data)


def tallennaTehtavaData(data):
    ser = []
    tehtava_id = None
    if "valid" in data.keys() and data["valid"] == True:
        del data["valid"]
        for k, v in data.items():
            # jokainen tehtava:
            teht = v.copy()
            del teht["osa_tehtavat"]
            teht["sarja_id"] = teht["sarja"]
            del teht["sarja"]
            tehtava = Tehtava(**teht)
            if not type(k) == str:
                tehtava.id = k
            tehtava.save()
            tehtava_id = tehtava.id

            for ot_k, ot_v in v["osa_tehtavat"].items():
                # jokainen osatehtava:
                osateht = ot_v.copy()
                if "parametrit" in osateht.keys():
                    del osateht["parametrit"]
                if "maaritteet" in osateht.keys():
                    del osateht["maaritteet"]
                if "tehtava" in osateht.keys():
                    del osateht["tehtava"]
                osa_tehtava = OsaTehtava(**osateht)
                if not type(ot_k) == str:
                    osa_tehtava.id = ot_k
                osa_tehtava.tehtava = tehtava

                if osa_tehtava.id > 0 or osa_tehtava.id == None:
                    osa_tehtava.save()
                    if "parametrit" in ot_v.keys():
                        for p_k, p_v in ot_v["parametrit"].items():
                            # jokainen parametri:
                            if "osa_tehtava" in p_v.keys():
                                del p_v["osa_tehtava"]
                            parametri = Parametri(**p_v)
                            if not type(p_k) == str:
                                parametri.id = p_k
                            parametri.osa_tehtava = osa_tehtava
                            if parametri.id > 0 or parametri.id == None:

                                parametri.save()
                            else:
                                parametri.id = -parametri.id
                                parametri.delete()

                    if "maaritteet" in ot_v.keys():
                        for m_k, m_v in ot_v["maaritteet"].items():
                            # jokainen maarite:
                            if "osa_tehtava" in m_v.keys():
                                del m_v["osa_tehtava"]
                            maarite = SyoteMaarite(**m_v)
                            if not type(m_k) == str:
                                maarite.id = m_k
                            maarite.osa_tehtava = osa_tehtava
                            if maarite.id > 0 or maarite.id == None:
                                maarite.save()
                            else:
                                maarite.id = -maarite.id
                                maarite.delete()
                else:
                    osa_tehtava.id = -osa_tehtava.id
                    osa_tehtava.delete()
        data["valid"] = True
    return tehtava_id

from django.core import serializers


def kisa_xml(kisa):
    """
    Apufunktio -> Luo xml merkkijonon kaikista kisan objekteista.
    Jättää henkilöt ja allergiat luomatta.
    """

    objects = [
        kisa,
    ]
    for s in kisa.sarja_set.all():
        objects.append(s)
        for v in s.vartio_set.all():
            objects.append(v)
        for t in s.tehtava_set.all():
            objects.append(t)
            for te in t.testaustulos_set.all():
                objects.append(te)
            for tt in t.tuomarineuvostulos_set.all():
                objects.append(tt)
            for ot in t.osatehtava_set.all():
                for sm in ot.syotemaarite_set.all():
                    objects.append(sm)
                    for s in sm.syote_set.all():
                        objects.append(s)
                for p in ot.parametri_set.all():
                    objects.append(p)
                objects.append(ot)
    return serializers.serialize("xml", objects, indent=4)


def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name)) for f in obj._meta.fields])
    return obj.__class__(**initial)


def kopioiTehtava(teht, sarjaan, uusiNimi=None):
    """
    Kopioi maaritellyn tehtavan haluttuun sarjaan.
    """
    # Kopioi itse tehtava:
    tNimi = teht.nimi
    if uusiNimi:
        tNimi = uusiNimi
    uusiTehtava = copy_model_instance(teht)
    uusiTehtava.id = None  # Luodaan uusi seuraavalla savella.
    uusiTehtava.nimi = tNimi
    uusiTehtava.sarja = sarjaan
    uusiTehtava.save()
    # Kopioi osatehtavat:

    osatehtavat = teht.osatehtava_set.all()
    for ot in osatehtavat:
        uusiot = copy_model_instance(ot)
        uusiot.tehtava_id = uusiTehtava.id
        uusiot.id = None  # Luodaan uusi seuraavalla savella.
        uusiot.save()
        # Kopioi parametrit
        parametrit = ot.parametri_set.all()
        for p in parametrit:
            uusip = copy_model_instance(p)
            uusip.osa_tehtava_id = uusiot.id
            uusip.id = None  # Luodaan uusi seuraavalla savella.
            uusip.save()

        # Kopioi maaritteet:
        maaritteet = ot.syotemaarite_set.all()
        for m in maaritteet:
            uusim = copy_model_instance(m)
            uusim.osa_tehtava_id = uusiot.id
            uusim.id = None
            uusim.save()

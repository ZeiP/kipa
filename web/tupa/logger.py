# encoding: utf-8
# KiPa(KisaPalvelu), tuloslaskentajärjestelmä partiotaitokilpailuihin
#    Copyright (C) 2010  Espoon Partiotuki ry. ept@partio.fi

from __future__ import absolute_import
from __future__ import print_function
from xml.dom.minidom import getDOMImplementation
import os.path
import re

from django.conf import settings

from .duplicate import kisa_xml
from .models import Kisa


impl = getDOMImplementation()

record_base = '<?xml version="1.0" encoding="utf-8"?>\n<django-objects version="1.0">\n</django-objects>'


# recorder middleware:
class PostDataRecorder:
    """
    Nauhoittaa post requestit record.xml tietokanta tiedoston loppuun mikali se on olemassa ja settings.RECORDING==True
    """

    def process_request(self, request):
        if settings.RECORDING == True:
            if request.method == "POST":
                posti = request.POST
                address = request.path

                kisa_haku = re.search("^/kipa/(.*?)/.*$", address)
                if not kisa_haku:
                    return None
                kisa_nimi = kisa_haku.group(1)

                if kisa_nimi == "uusiKisa":
                    kisa_nimi = posti["nimi"]
                record_name = "record/" + kisa_nimi + ".xml"

                data = impl.createDocument(None, "uusi_lisa", None)

                post_test = data.createElement("post_request")
                post_test.setAttribute("address", address)

                for n, v in posti.iteritems():
                    elem = data.createElement("input")
                    elem.setAttribute("name", n)
                    elem.setAttribute("value", v)
                    post_test.appendChild(elem)
                    data.childNodes[0].appendChild(post_test)

                if not os.path.isfile(record_name):
                    uusi = open(record_name, "w")
                    if not kisa_haku.group(1) == "uusiKisa":
                        kisa = Kisa.objects.get(nimi=kisa_haku.group(1))
                        vanha = kisa_xml(kisa)
                        print(vanha)
                        uusi.write(kisa_xml(kisa))  # talletetaan kisan kanta pohjaksi
                    else:
                        uusi.write(
                            record_base
                        )  # uusi kisa -> ei olemassaolevaa tietokantaa.
                    uusi.close()

                pos = next = 0
                filuu = open(record_name, "r")
                for line in filuu.readlines():
                    pos = next  # position of beginning of this line
                    next += len(line)  # compute position of beginning of next line
                filuu.close()

                FILE = open(record_name, "r+")
                FILE.seek(pos, 0)

                uusi = data.toprettyxml(encoding="utf-8", indent="    ", newl="\n")
                for line in uusi.splitlines()[2:-1]:
                    FILE.write(line + "\n")
                FILE.write("</django-objects>")
                FILE.close()
                return None

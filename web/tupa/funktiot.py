"""
Tässä tiedostossa on määritelty kaikki funktiot joita voi käyttää laskennan kaavoissa.
"""

from __future__ import absolute_import

from decimal import ROUND_FLOOR, ROUND_CEILING, getcontext

from .laskentatyypit import DictDecimal, suorita_lista


def pienin(*lista):
    if len(lista) == 1:
        return min(lista)
    return min(*lista)


def suurin(*lista):
    if len(lista) == 1:
        return max(lista)
    return max(*lista)


def mediaani(*lista):
    """
    Palauttaa mediaanin arvon joukon lukuarvoista:
    joukko voi olla sanakirja tai lista
    Mikäli lukujoukon pituus on parillinen, palauttaa kahden keskimmaisen luvun keskiarvon.
    """
    values = sorted(lista)
    if len(values) % 2 == 1:
        return DictDecimal(values[(len(values) + 1) // 2 - 1])
    else:
        lower = DictDecimal(values[len(values) // 2 - 1])
        upper = DictDecimal(values[len(values) // 2])
        return (DictDecimal(lower + upper)) / 2


def keskiarvo(*lista):
    """
    Palauttaa joukon lukuarvojen keskiarvon.
    Joukko voi olla sanakirja tai lista.
    """
    # if not len(lista): return None
    total = DictDecimal(0)
    for x in lista:
        total = total + x
    avg = total / len(lista)
    return avg


def summa(*lista):
    """
    Palauttaa joukon lukuarvojen summan.
    Joukko voi olla sanakirja tai lista.
    """
    s = DictDecimal(0)
    for v in lista:
        if v and type(v) is not str:
            s = s + v
    return s


def interpoloi(x, x1, y1, x2, y2=0):
    """
    Palauttaa f(x)=y koordinaatin pisteiden (x1,y1) (x2,y2) määrittämältä suoralta.
    Mikäli f(x)>y1 f(x)=y1
    """
    return suorita_lista(
        suurin,
        DictDecimal(0),
        suorita_lista(pienin, y1, (y1 - y2) / (x1 - x2) * (x - x2)),
    )


def aikavali(a, b):
    tulos = b - a
    if tulos < DictDecimal("0"):
        tulos = tulos + DictDecimal("86400")  # lisataan 24h sekuntteina
    return tulos


def jos(ehto, a, b):
    if ehto:
        return a
    else:
        return b


def floor(x):
    return x.quantize(DictDecimal("1."), rounding=ROUND_FLOOR)


def ceil(x):
    return x.quantize(DictDecimal("1."), rounding=ROUND_CEILING)


"""
Funktiot joiden parametrit ovat toisistaan riippumattomia
"""
perusfunktiot = {
    "interpoloi": interpoloi,
    "abs": abs,
    "aikavali": aikavali,  # Alkuaika ja loppuaika
    "floor": floor,
    "ceil": ceil,
    "sqrt": getcontext().sqrt,
    "exp": getcontext().exp,
    "mod": getcontext().remainder,  # Jakojäännös
    "pow": getcontext().power,
    "power": getcontext().power,
    "log": getcontext().log10,
    "ln": getcontext().ln,
    "if": jos,
}  # Valintalause

"""
Funktiot joiden kaikki parametrit ovat samanarvoisia, ja parametrejä voi olla liukuva määrä.
"""
listafunktiot = {
    "pienin": pienin,
    "min": pienin,
    "suurin": suurin,
    "max": suurin,
    "sum": summa,
    "med": mediaani,
    "kesk": keskiarvo,
    "mean": keskiarvo,
}

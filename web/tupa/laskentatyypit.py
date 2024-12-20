from __future__ import absolute_import
from decimal import Decimal, ROUND_HALF_UP

from . import log


def decimal_uni(self):
    return str(self.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def decimal_repr(self):
    return str(self.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


class SequenceOperations:
    def __add__(self, other):
        return self.operate_to_all(lambda a, b: a + b, other)

    def __radd__(self, other):
        return self.operate_to_all(lambda a, b: a + b, other)

    def __sub__(self, other):
        return self.operate_to_all(lambda a, b: a - b, other)

    def __rsub__(self, other):
        return self.operate_to_all(lambda a, b: b - a, other)

    def __mul__(self, other):
        return self.operate_to_all(lambda a, b: a * b, other)

    def __rmul__(self, other):
        return self.operate_to_all(lambda a, b: a * b, other)

    def __truediv__(self, other):
        return self.operate_to_all(lambda a, b: a / b, other)

    def __rtruediv__(self, other):
        return self.operate_to_all(lambda a, b: b / a, other)

    def __lt__(self, other):
        return self.operate_to_all(lambda a, b: a < b, other)

    def __le__(self, other):
        return self.operate_to_all(lambda a, b: a <= b, other)

    def __eq__(self, other):
        return self.operate_to_all(lambda a, b: a == b, other)

    def __ne__(self, other):
        return self.operate_to_all(lambda a, b: a != b, other)

    def __gt__(self, other):
        return self.operate_to_all(lambda a, b: a > b, other)

    def __ge__(self, other):
        return self.operate_to_all(lambda a, b: a >= b, other)


class MathDict(SequenceOperations, dict):
    """
    Sanakirja jonka alkioille voi tehda massoittain
    laskutoimituksia toisten sanakirjan vastaavien alkioiden kesken.
    """

    def operate_to_all(self, function2, other):
        if type(other) == MathDict:
            oper = MathDict({})
            for k in self.keys():
                try:
                    oper[k] = function2(self[k], other[k])
                except KeyError:
                    pass
                except TypeError:
                    pass
        elif type(other) == MathList:
            oper = MathListDict({})
            for k in self.keys():
                try:
                    oper[k] = [(function2(self[k], x) for x in other)]
                except KeyError:
                    pass
                except TypeError:
                    pass
        else:
            oper = MathDict({})
            for k in self.keys():
                try:
                    oper[k] = function2(self[k], other)

                except KeyError:
                    pass
                except TypeError:
                    pass
        return oper

    def listaksi(self):
        """
        Palauttaa kaikki alkiot yhdessä listasa
        """
        lista = []
        for k, v in self.items():
            lista.append(v)
        return lista

    def __str__(self):
        stringi = "{"
        for k, v in self.items():
            if v:
                stringi += str(k) + ": " + str(v) + ", "
        stringi = stringi[:-2]
        stringi += "}"
        return stringi


class MathList(SequenceOperations, list):
    """
    Lista jonka alkioille voi tehda massoittain
    laskutoimituksia toisten listojen vastaavien alkioiden kesken.
    """

    def operate_to_all(self, function2, other, *args):
        oper = None
        if type(other) == MathList:
            oper = MathList(
                [function2(self[i], other[i], *args) for i in range(len(self))]
            )
        elif type(other) == MathDict:
            oper = MathListDict({})
            for k, v in other.items():
                oper[k] = []
                for x in self:
                    try:
                        oper[k].append(function2(x, v, *args))

                    except KeyError:
                        pass
                    except TypeError:
                        pass
        else:
            oper = MathList([function2(v, other, *args) for v in self])
        return oper

    def listaksi(self):
        return list(self)

    def __str__(self):
        stringi = "["
        for x in self:
            if x:
                stringi += str(x) + ", "
        stringi = stringi[:-2]
        stringi += "]"
        return stringi


class MathListDict(SequenceOperations, dict):
    """
    Lista jonka alkioina on sanakirjoja, sekä sanakirja jonka alkioina on listoja.
    Operoida voi kummalla vaan, tai vaikka toisella MathListDictionarylla.
    """

    def operate_to_all(self, function2, other, *args):
        oper = {}
        if type(other) == MathListDict:
            for k, v in self.items():
                for i in range(len(v)):
                    oper[k] = []
                    try:
                        oper[k].append(function2(v[i], other[k][i], *args))
                    except KeyError:
                        pass
                    except IndexError:
                        pass
                    except TypeError:
                        pass
        elif type(other) == MathList:
            for k, v in self.items():
                try:
                    oper[k] = MathList(
                        [
                            function2(self[k][i], other[i], *args)
                            for i in range(len(self[k]))
                        ]
                    )
                except KeyError:
                    pass
                except TypeError:
                    pass

        elif type(other) == MathDict:
            for k, v in other.items():
                if k in self.keys():  # ainoastaan alkiot jotka löytyvät
                    oper[k] = []
                    for x in self[k]:
                        try:
                            oper[k].append(function2(x, v, *args))
                        except KeyError:
                            pass
                        except TypeError:
                            pass

        else:  # muu (oletetaan skalaariksi)
            for k, v in self.items():
                oper[k] = []
                for x in v:
                    try:
                        oper[k].append(function2(x, other, *args))
                    except KeyError:
                        pass
                    except TypeError:
                        pass
        return oper

    def listaksi(self):
        """
        Palauttaa kaikki alkiot yhdessä listassa
        """
        lista = []
        for k, v in self.items():
            lista.extend(v)
        return lista


class DictDecimal(SequenceOperations, Decimal):
    """
    Desimaali luokka , johon on toteutettu operoiminen MathDict sekä MathList instansseilla.
    """

    def operate_to_all(self, function2, other):
        oper = DictDecimal()
        if type(other) == MathDict:
            oper = MathDict(other)
            for k in other.keys():
                try:
                    oper[k] = function2(self, other[k])
                except KeyError:
                    pass
                except TypeError:
                    pass
        elif type(other) == MathList:
            oper = MathList([])
            for v in other:
                try:
                    oper.append(function2(self, v))
                except KeyError:
                    pass
                except TypeError:
                    pass
        else:
            try:
                oper = DictDecimal(function2(Decimal(self), other))
            except KeyError:
                pass
            except TypeError:
                pass
        return oper

    __repr__ = decimal_repr

    def listaksi(self):
        return [self]


def karsi(lista, lfunktio):
    """
    Yhdistää listan alkiot keskenään ajamalla listafunktiota vastinalkioiden kesken
    """
    karsittu = []
    index = 0
    tavaraa = 1
    while tavaraa:
        varvi = []
        tavaraa = 0
        for x in lista:
            if hasattr(x, "keys"):  # on sanakirja
                pass  # Tähän täytyisi tehdä rekursiivinen sanakirjojen operointi

            elif hasattr(x, "__contains__"):  # on lista
                if len(x) > index and not type(x) == str:
                    tavaraa = 1
                    varvi.append(x[index])
            else:
                varvi.append(x)
        if tavaraa == 0 and index > 0:
            break
        index += 1
        if len(varvi):
            karsittu.append(lfunktio(*varvi))
    if len(karsittu) == 1:
        return karsittu[0]
    else:
        return karsittu


def listaksi(a, *opt):
    """
    Muuttaa sanakirjan tai desimaalin listaksi jos syote on joukkio, muuten palauttaa muuttujan itsessaan.
    """
    if type(a) == MathList:
        a = list(a)

    if len(opt):
        joukkio = [a]
        joukkio += opt
    else:
        joukkio = a

    if type(joukkio) == DictDecimal or type(joukkio) == bool:
        joukkio = [joukkio]
    if type(joukkio) == Decimal:
        joukkio = [DictDecimal(joukkio)]
    elif type(joukkio) == str:
        return joukkio
    if type(joukkio) == list:
        lista = []
        for v in joukkio:
            if type(v) == DictDecimal or type(v) == Decimal:
                lista.append(DictDecimal(v))
            else:
                lista.append(v)
        return lista
    try:
        lista = []
        for k in joukkio.keys():
            if type(joukkio[k]) == DictDecimal or type(joukkio[k]) == Decimal:
                lista.append(DictDecimal(joukkio[k]))
        return lista
    except Exception:
        # TODO: stricter type
        return None


def run_dict(lista, funktio, *param):
    mdict = None
    params = []
    for p in param:
        if type(p) == list:
            params.append(MathList(p))
        else:
            params.append(p)
        if type(p) == MathDict and not mdict:
            mdict = p
    if not mdict:
        if not lista:
            return funktio(*params)
        else:
            return karsi(params, funktio)

    rValue = MathDict({})
    for k in mdict.keys():
        parametrit = []

        for p in params:
            if type(p) == MathDict and k in p.keys():
                parametrit.append(p[k])
            else:
                parametrit.append(p)

        if lista:
            rValue[k] = karsi(listaksi(*parametrit), funktio)
        else:
            try:
                rValue[k] = funktio(*parametrit)
            except Exception:
                pass  # Pass all elemets that could not be calculated.
    return rValue


def suorita(funktio, *param):
    tulos = None
    log.muteLogging()
    try:
        tulos = run_dict(0, funktio, *param)
    except Exception:
        tulos = Decimal(0)
    log.unmuteLogging()
    log.logFunction(funktio, param, tulos)
    return tulos


def suorita_lista(funktio, a, *param):
    tulos = None
    if len(param) == 0:
        if (
            not type(a) == bool
            and not type(a) == Decimal
            and not type(a) == DictDecimal
            and len(a) == 0
        ):
            raise KeyError
        elif type(a) == str:
            tulos = None
        elif type(a) == Decimal or type(a) == bool:
            tulos = karsi(listaksi(a), funktio)
        elif type(a) == list:
            tulos = karsi(a, funktio)
        else:
            tulos = karsi(listaksi(a.listaksi()), funktio)

        parametrit = [a]
        log.logFunction(funktio, parametrit, tulos)
    else:
        tulos = run_dict(1, funktio, a, *param)
        parametrit = [a]
        for p in param:
            parametrit.append(p)
        log.logFunction(funktio, parametrit, tulos)
    return tulos

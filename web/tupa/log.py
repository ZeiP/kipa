import settings

laskentaloki = ""
try:
    stack
except:
    stack = []


def __noLogString(string):
    return None


def __logString(string):
    string = string.replace("\n", "<br>")
    string = string.replace(" ", "&nbsp;")
    global laskentaloki
    laskentaloki += string + "<br>"


def __noLogFunction(function, params, result):
    return None


def __logFunction(function, params, result):
    global laskentaloki
    if params:

        laskentaloki += "<br>"
        laskentaloki += unicode(function.__name__) + "("
        try:
            for p in params:
                laskentaloki += unicode(p) + ", "
        except:
            pass
        laskentaloki = laskentaloki[:-2]
        laskentaloki += ")=<br><b> " + unicode(result)
        laskentaloki += "</b>"
        laskentaloki += "<br>"


def enableLogging():
    global logString
    global logFunction
    logString = __logString
    logFunction = __logFunction


def disableLogging():
    global logString
    global logFunction
    logString = __noLogString
    logFunction = __noLogFunction


def muteLogging():
    global stack
    global logString
    global logFunction
    stack.append(logString)
    stack.append(logFunction)
    disableLogging()


def unmuteLogging():
    global stack
    global logString
    global logFunction
    logFunction = stack.pop()
    logString = stack.pop()


def clearLoki():
    global laskentaloki
    laskentaloki = ""


def palautaLoki():
    global laskentaloki
    return laskentaloki


try:
    logString
except:
    logString = None

try:
    logFunction
except:
    logFunction = None

if not logString or not logFunction:
    enableLogging()

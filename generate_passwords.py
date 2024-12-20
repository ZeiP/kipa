from shutil import copyfile
import string
import random
import crypt
import MySQLdb


def find_check_ids_by_name(checks, cursor):
    # execute SQL query using execute() method.
    cursor.execute(
        "SELECT id FROM kipa_tehtava WHERE sarja_id IN (26, 27, 28, 29, 30) AND nimi IN ('%s')"
        % "', '".join(checks)
    )
    data = cursor.fetchall()

    res = []
    for row in data:
        for val in row:
            res.append(str(val))

    return res


prefix = "llhk19-"
baseurl = "/kipa/Leon_lenkki_ja_Hilkan_kilpa_2019/"
accounts = {
    "hamk": ["Tyoesuhdealias", "RistiNollaKorolla"],
    "liikennepuisto": ["RushHour"],
    "vanaja": ["HPK"],
    "actionfactory": ["Action_Factory"],
    "yo": [
        "Larry",
        "Hexed",
        "Escape_room",
        "Commodore_64",
        "Ruokaralli",
        "Kanaset",
        "Kummitusmetsae",
    ],
    "tekoaltaat": ["Scrabble"],
    "kankaantausta": ["Super_Mario_suunnistusmaassa"],
    "hameensanomat": ["Rubikin_kuutio"],
    "jaahalli": ["Deja_vu"],
    "linna": ["Risk", "Arvaa_kuka"],
    "ahvenisto": ["Afrikan_taehti"],
    "hakovuori": ["Laulava_muistipeli"],
    "verkatehdas": ["Roskaviesti"],
}
templatefile = "/srv/django/kipa/passwords-llhk19"
path = "/srv/django/kipa/auth_files/llhk19/"
letters = string.ascii_letters

access_config = ""

db = MySQLdb.connect(user="kipa", passwd="PWD", host="localhost", db="kipa")
cursor = db.cursor()

print(accounts)
for name, checks in accounts.items():
    username = prefix + name
    pwdfile = path + name
    password = "".join(random.choice(letters) for i in range(10))
    pwhash = crypt.crypt(password)
    copyfile(templatefile, pwdfile)
    f = open(pwdfile, "a")
    print(username + ":" + pwhash, file=f)
    print(username + ";" + password)

    ids = find_check_ids_by_name(checks, cursor)
    for id in ids:
        access_config = (
            access_config
            + """
      location {baseurl}syota/tehtava/{id} {{
          auth_basic "Vain {name}-rastin tulosten syottajille";
          auth_basic_user_file "{pwdfile}";
          include uwsgi_params;
          uwsgi_pass unix:/run/uwsgi/kipa.sock;
      }}

      """.format(
                baseurl=baseurl, name=name.capitalize(), id=id, pwdfile=pwdfile
            )
        )

c = open(path + "access.conf", "w")
print(access_config, file=c)

db.close()

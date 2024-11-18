*** Settings ***
Documentation     Testataan perustoiminnallisuudet
Suite Setup       Kipa Suite Setup
Suite Teardown    Close All Browsers And Stop Selenium Server
Test Setup        Open Competition
Test Teardown     Close Browser
Force Tags        regression    smoke
Library           SeleniumLibrary
Resource          yhteiset_resurssit.resource
Variables         kipa_sivuosoitteet_ja_otsikot.py

*** Test Cases ***
Luodaan uusi kisa
    [Setup]    Open Kipa Main Page
    Create new Competition    ${TESTIKISA}

Tarkista syötä suorituksia
    Open Sub Page Verify Location And Title    syötä suorituksia    ${TULOSTEN_SYOTTO_URL}    ${TULOSTEN_SYOTTO_OTSIKKO}

Tarkista syötä suorituksia - tarkistus
    Open Sub Page Verify Location And Title    syötä suorituksia - tarkistus    ${TULOSTEN_SYOTTO_TARKISTUS_URL}    ${TULOSTEN_SYOTTO_TARKISTUS_OTSIKKO}

Tarkista tulossivu
    Open Sub Page Verify Location And Title    sarjan tulokset    ${TULOSTEN_TARKISTUS_URL}    ${TULOSTEN_TARKISTUS_OTSIKKO}

Tarkista Tuomarineuvosto
    Open Sub Page Verify Location And Title    tuomarineuvoston työkalu    ${TUOMARINEUVOSTO_URL}    ${TUOMARINEUVOSTO_OTSIKKO}
    Page Should Contain Button    Peruuta
    Page Should Contain Button    tallenna

Tarkista laskennan tilanne
    Open Sub Page Verify Location And Title    laskennan tilanne    ${LASKENNAN_TILANNE_URL}    ${LASKENNAN_TILANNE_OTSIKKO}

Tarkista vartioiden määritys
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    Page Should Contain Button    Peruuta
    Page Should Contain Button    tallenna

Tarkista tehtävien määritys
    Open Sub Page Verify Location And Title    määrittele tehtävät    ${TEHTAVAN_MAARITYS_URL}    ${TEHTAVAN_MAARITYS_OTSIKKO}

Tarkista Testituloksien määritys
    Open Sub Page Verify Location And Title    määrittele testituloksia    ${TESTITULOKSIEN_MAARITYS_URL}    ${TESTITULOKSIEN_MAARITYS_OTSIKKO}
    Page Should Contain Button    Peruuta
    Page Should Contain Button    tallenna
    comment    Linkin, luo testitulokset sarjalle, pitäisi viedä samalle sivulle.
    Open Sub Page Verify Location And Title    luo testitulokset sarjalle    ${TESTITULOKSIEN_MAARITYS_URL}    ${TESTITULOKSIEN_MAARITYS_OTSIKKO}
    Page Should Contain Button    Peruuta
    Page Should Contain Button    tallenna

Tarkista palauta kisa
    Open Sub Page Verify Location And Title    palauta kisa    ${KISAN_TUONTI_URL}    ${KISAN_TUONTI_OTSIKKO}
    Page Should Contain Button    Peruuta
    Page Should Contain Button    tallenna
    Page Should Contain Element    file

Tarkista sarjan tulokset
    Open Sub Page Verify Location And Title    sarjan tulokset    ${TULOSTEN_TARKISTUS_URL}    ${TULOSTEN_TARKISTUS_OTSIKKO}

Lisätään sarjoja kisaan
    [Documentation]    sininen, harmaa ja valkoinen
    Click Link    määrittele kisan perustiedot
    Location Should Be    ${KIPA_URL}/${TESTIKISA}/${KISAN_MAARITYS_URL}/
    Title Should Be    Kipa - Määritä kisa
    Input Text    id_sarja_set-0-nimi    sininen
    Input Text    id_sarja_set-1-nimi    harmaa
    Input Text    id_sarja_set-2-nimi    valkoinen
    Click Button    tallenna
    Close Browser
    Open Competition
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    Page Should Contain Link    sininen
    Page Should Contain Link    harmaa
    Page Should Contain Link    valkoinen
    Capture Page Screenshot

Lisätään kaksi vartiota sarjaan
    [Documentation]    harmaa
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    comment    varmistetaan että käpistellään oikeaa sarjaa
    Run Keyword And Ignore Error    Click Link    harmaa
    Input Text    id_harmaa-0-nimi    testivartio1
    Input Text    id_harmaa-0-nro    100
    Input Text    id_harmaa-1-nimi    testivartio2
    Input Text    id_harmaa-1-nro    101
    click button    tallenna
    Close Browser
    Open Competition
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    Run Keyword And Ignore Error    click link    harmaa
    ${first_group}=    get value    id_harmaa-0-nimi
    Should Contain    ${first_group}    testivartio1
    ${second_group}=    get value    id_harmaa-1-nimi
    Should Contain    ${second_group}    testivartio2
    Capture Page Screenshot
    comment     Varmistetaan ettei harmaan vartiot näy muissa sarjoissa
    Run Keyword And Ignore Error    Click Link    sininen
    Element Should not Be Visible    id_harmaa-0-nimi
    Element Should not Be Visible    id_harmaa-1-nimi
    Run Keyword And Ignore Error    Click Link    valkoinen
    Element Should not Be Visible    id_harmaa-0-nimi
    Element Should not Be Visible    id_harmaa-1-nimi

Lisätään tehtäviä tyhjään sarjaan
    Comment    luo kisapistetehtävä    valkoinen

Lisätään tehtäviä vartioita sisältävään sarjaan
    Comment    luo kisapistetehtävä    harmaa

Poistetaan tehtävä sarjasta
    Click Link    määrittele kisan perustiedot
    Location Should Be    ${KIPA_URL}/${TESTIKISA}/${KISAN_MAARITYS_URL}/
    Title Should Be    Kipa - Määritä kisa
    Input Text    id_sarja_set-0-nimi    sininen
    Input Text    id_sarja_set-1-nimi    harmaa
    Input Text    id_sarja_set-2-nimi    valkoinen
    Click Button    tallenna
    Open Competition
    luo kisapistetehtävä    harmaa
    Open Competition
    Open Sub Page Verify Location And Title    määrittele tehtävät    ${TEHTAVAN_MAARITYS_URL}    ${TEHTAVAN_MAARITYS_OTSIKKO}
    Click Link    harmaa
    Select Checkbox    xpath://ul[label[text() = 'Delete:']]/input[@type='checkbox' and not(ancestor::div[contains(@style,'display: none')])]
    Click Button    xpath://button[@type='submit' and contains(., 'Poista valitut') and not(ancestor::div[contains(@style,'display: none')])]
    Wait Until Keyword Succeeds    10 sec    2 sec    Title Should Be    ${TEHTAVAN_MAARITYS_OTSIKKO}

Poistetaan tyhjä sarja kisasta
    [Documentation]    sininen
    Click Link    määrittele kisan perustiedot
    Location Should Be    ${KIPA_URL}/${TESTIKISA}/${KISAN_MAARITYS_URL}/
    comment    Valitaan eka chekboxi, sininen
    Select Checkbox    id_sarja_set-0-DELETE
    Click Button    tallenna
    Close Browser
    Open Competition
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    Page Should Not Contain Link    sininen
    Page Should Contain Link    harmaa
    Page Should Contain Link    valkoinen
    Capture Page Screenshot

Poistetaan vartioita sisältävä sarja kisasta
    [Documentation]    harmaa
    Click Link    määrittele kisan perustiedot
    Location Should Be    ${KIPA_URL}/${TESTIKISA}/${KISAN_MAARITYS_URL}/
    comment    Valitaan eka chekboxi, harmaa
    Select Checkbox    id_sarja_set-0-DELETE
    Click Button    tallenna
    Close Browser
    Open Competition
    Open Sub Page Verify Location And Title    määrittele vartiot    ${VARTIOIDEN_MAARITYS_URL}    ${VARTIOIDEN_MAARITYS_OTSIKKO}
    Page Should Not Contain Link    harmaa
    Page Should Contain Link    valkoinen
    ${first_group}=    Run Keyword And Ignore Error    get value    id_harmaa-0-nimi
    Should not Contain    ${first_group}    testivartio1
    ${second_group}=    Run Keyword And Ignore Error    get value    id_harmaa-1-nimi
    Should not Contain    ${second_group}    testivartio2
    Capture Page Screenshot

Poista Luotu Kisa
    Remove Competition    ${TESTIKISA}
    [Teardown]    close all browsers


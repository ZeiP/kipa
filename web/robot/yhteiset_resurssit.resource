*** Keywords ***
Open KiPa Main Page
    Open Browser And Maximize    ${KIPA_URL}/
    Wait Until Keyword Succeeds    10 sec    2 sec    Title Should Be    ${KIPA_OTSIKKO}

Create New Competition
    [Arguments]    ${competition}
    [Documentation]    Creates new competition and checks that it exist. Expects TESTIKISA to be given as argument.
    Click Link    Luo uusi kisa
    Location Should Be    ${KIPA_URL}/uusiKisa/${KISAN_MAARITYS_URL}/
    Input Text    id_nimi    ${competition}
    Input Text    id_sarja_set-0-nimi    testisarja
    Click Button    tallenna
    Close Browser
    comment    kaikissa ympäristöissä ei näköjään ehditä avamaan selainta aikarajan puitteissa, yritetään 5 sekunnin välein 15 sekunnin ajan ennenkuin luovutetaan
    Wait Until Keyword Succeeds    30 sec    5sec    Open Browser And Maximize    ${KIPA_URL}/
    Click Link    ${competition}
    Location Should Be    ${KIPA_URL}/${competition}/
    Title Should Be    Kipa - ${competition}

Open Browser and Maximize
    [Arguments]    ${page}
    Open Browser    ${page}    ${BROWSER}
    Maximize Browser Window

Kipa Suite Setup
    comment    Uudelleenyritys testiserverin mahdollisen kuormituksen vuoksi.
    Wait Until Keyword Succeeds    3 min    1 min    Open Kipa Main Page
    Comment    Close Browser

Open Sub Page Verify Location And Title
    [Arguments]    ${link_name}    ${link}    ${page_title}
    Click Link    xpath://a[contains(., '${link_name}')]
    Wait Until Keyword Succeeds    10 sec    2 sec    Location Should Be    ${KIPA_URL}/${TESTIKISA}/${link}/
    Wait Until Keyword Succeeds    10 sec    2 sec    Title Should Be    ${page_title}

Open Competition
    Open KiPa Main Page
    comment    ${original timeout}=    Set Selenium Timeout    15 sec
    Click Link    ${TESTIKISA}
    Wait Until Keyword Succeeds    10 sec    2 sec    Title Should Be    Kipa - ${TESTIKISA}
    Capture Page Screenshot

Remove Competition
    [Arguments]    ${competition}
    Open KiPa Main Page
    click link    ${competition}
    title should be    Kipa - ${competition}
    Click Link    xpath://a[contains(., 'poista kisa')]
    Title Should Be    ${KISAN_POISTO_OTSIKKO}
    Click Button    Kyllä
    Wait Until Keyword Succeeds    10 sec    2 sec    Title Should Be    ${KAIKKI_KISAT_OTSIKKO}
    Location Should Be    ${KIPA_URL}/
    Page Should Not Contain Link    ${competition}
    Page Should Not Contain    ${competition}

Close All Browsers And Stop Selenium Server
    Close All Browsers

luo kisapistetehtävä
    [Arguments]    ${sarja}
    Open Sub Page Verify Location And Title    määrittele tehtävät    ${TEHTAVAN_MAARITYS_URL}    ${TEHTAVAN_MAARITYS_OTSIKKO}
    Run Keyword And Ignore Error    Click Link    ${sarja}
    Click Link    xpath://a[contains(., 'Lisää uusi tehtävä') and not(ancestor::div[contains(@style,'display: none')])]
    Input Text    tehtava_#1_nimi    kisapiste_testi_${sarja}
    Element Should Not Be Visible    tehtava_#1_#0_tyyppi_kp_a
    Select Radio Button    tehtava_#1_#0_tyyppi    kp
    Element Should Be Visible    tehtava_#1_#0_tyyppi_kp_a
    Input Text    tehtava_#1_#0_tyyppi_kp_a    testikuvaus
    click button    tallenna
    Wait Until Keyword Succeeds    10 sec    1 sec    Title Should Be    Kipa - kisapiste_testi_${sarja} (${sarja})
    Location Should Contain    talletettu
    Open Competition
    Open Sub Page Verify Location And Title    määrittele tehtävät    ${TEHTAVAN_MAARITYS_URL}    ${TEHTAVAN_MAARITYS_OTSIKKO}
    Run Keyword And Ignore Error    Click Link    ${sarja}
    Wait Until Keyword Succeeds    10 sec    1 sec    Page Should Contain    kisapiste_testi_${sarja}

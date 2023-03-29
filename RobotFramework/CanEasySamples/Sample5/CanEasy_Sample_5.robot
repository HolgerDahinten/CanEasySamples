*** Settings ***
Documentation     Shows how to use caneasy_change_sig_val and manual user input
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           Dialogs
Library           ../../TestLibrary/caneasy.py    # CanEasy interface
Library           OperatingSystem
Library           ../../TestLibrary/window.py
Library           Screenshot

*** Variables ***

*** Test Cases ***
Init CanEasy
    # Prepare CAN Simulation environment
    CanEasy Init
    CanEasy Workspace Load    ${CURDIR}\\..\\CanEasy_Sample.csm
    Sleep    500 ms
    CanEasy Simu Start
    Sleep    500 ms

Test 1 (MANUAL)
    [Documentation]    Show usage of caneasy_change_sig_val and manual user input.
    ...    A Screenshot of a plot is taken at the end of the test.
    [Tags]    manual
    Run Keyword And Continue On Failure    Execute Manual Step    Is Engine Speed 0?
    Caneasy Change Sig Val    ECU1_EngineSpeed    0.0    5000.0    3000    100
    Sleep    1s
    Caneasy Change Sig Val    ECU1_EngineSpeed    5000.0    0.0    3000    100
    Bring Window to Front    EngineSpeedPlot
    Sleep    1s
    Take Screenshot

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample5.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

*** Keywords ***

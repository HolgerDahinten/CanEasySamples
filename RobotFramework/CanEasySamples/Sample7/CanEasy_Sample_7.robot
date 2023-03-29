*** Settings ***
Documentation     Shows how to execute a scheduler table
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           ../../TestLibrary/caneasy.py    # CanEasy interface

*** Test Cases ***
Init CanEasy
    # Prepare CAN Simulation environment
    CanEasy Init
    CanEasy Workspace Load    ${CURDIR}\\..\\CanEasy_Sample.csm
    Sleep    500 ms
    CanEasy Simu Start
    Sleep    500 ms

Test 1
    [Documentation]    Shows how to set a marker and execute a scheduler table
    Sleep    500 ms
    CanEasy Set Value    ECU1_Ignition    0
    CanEasy Is Value Equal    ECU2_EngineRunning    0
    CanEasy Create Marker
    # This Functions set Ignituion to on for 1s
    CanEasy Execute    Tab:SetIgnition
    Sleep    500 ms
    CanEasy Create Marker
    CanEasy Is Value Equal    ECU2_EngineRunning    1
    Sleep    1s
    CanEasy Is Value Equal    ECU2_EngineRunning    0

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample7.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

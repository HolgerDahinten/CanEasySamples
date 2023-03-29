*** Settings ***
Suite Setup
Suite Teardown
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
    [Documentation]    Check general engine functionality
    Check Engine    Stopped
    Set Ignition    On
    Check Engine    Running
    Set Ignition    Off
    Check Engine    Stopped

Test 2
    [Documentation]    Test Ignition with direct calls
    # Set Ignition to 1 by direct CAN Signal
    CanEasy Set Value    ECU1_Ignition    1
    Sleep    100 ms
    # Check Value of CAN Signal
    ${sigval}=    CanEasy Get Value    ECU2_EngineRunning
    Should Be Equal As Numbers    ${sigval}    1
    # Check Signal Value by Valuetable
    ${sigval}=    Caneasy Get Value String    ECU2_EngineRunning
    Should Be Equal    ${sigval}    Running
    # Check by User Keyword
    Check Engine    Running
    # Check with CanEasy Functions
    CanEasy Is Value Equal    ECU2_EngineRunning    1    1000
    CanEasy Is Value Less    ECU2_EngineRunning    2    500
    CanEasy Is Value Greater    ECU2_EngineRunning    0
    CanEasy Is Value Less or Equal    ECU2_EngineRunning    1
    CanEasy Is Value Less or Equal    ECU2_EngineRunning    1.1
    CanEasy Is Value Greater or Equal    ECU2_EngineRunning    1
    CanEasy Is Value Greater or Equal    ECU2_EngineRunning    0.9
    CanEasy is Value in Range    ECU2_EngineRunning    0.9    1.1

Test 3 (FAIL)
    [Documentation]    Test Ignition with direct calls
    [Tags]    noncritical
    # Set Ignition to 0
    CanEasy Set Value String    ECU1_Ignition    Off
    # Check with CanEasy Functions
    Run Keyword And Continue On Failure    CanEasy Is Value Equal    ECU2_EngineRunning    1    50
    Run Keyword And Continue On Failure    CanEasy Is Value Less    ECU2_EngineRunning    0    50
    Run Keyword And Continue On Failure    CanEasy Is Value Greater    ECU2_EngineRunning    0    50
    Run Keyword And Continue On Failure    CanEasy Is Value Less or Equal    ECU2_EngineRunning    -1    50
    Run Keyword And Continue On Failure    CanEasy Is Value Less or Equal    ECU2_EngineRunning    -0.1    50
    Run Keyword And Continue On Failure    CanEasy Is Value Greater or Equal    ECU2_EngineRunning    1    50
    Run Keyword And Continue On Failure    CanEasy Is Value Greater or Equal    ECU2_EngineRunning    0.9    50
    Run Keyword And Continue On Failure    CanEasy is Value in Range    ECU2_EngineRunning    0.9    1.1    50

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample1.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

*** Keywords ***
Check Engine
    [Arguments]    ${Value}
    ${CurrVal}=    CanEasy Get Value String    ECU2_EngineRunning
    Should Be Equal    ${CurrVal}    ${Value}

Set Ignition
    [Arguments]    ${IgnState}
    CanEasy Set Value String    ECU1_Ignition    ${IgnState}


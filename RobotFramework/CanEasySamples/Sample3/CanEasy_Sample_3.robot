*** Settings ***
Documentation     shows how to do tests based on value tables
Suite Setup
Suite Teardown
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           ../../TestLibrary/caneasy.py    # CanEasy interface

*** Variables ***

*** Test Cases ***
Init CanEasy
    # Prepare CAN Simulation environment
    CanEasy Init
    CanEasy Workspace Load    ${CURDIR}\\..\\CanEasy_Sample.csm
    Sleep    500 ms
    CanEasy Simu Start
    Sleep    500 ms

Test 1
    [Documentation]    Engine Speed check data driven
    CheckSpeed    1    500    25
    CheckSpeed    2    100    10
    CheckSpeed    3    500    75
    CheckSpeed    4    4500    900
    CheckSpeed    5    2100    525
    CheckSpeed    6    3400    1020

Test 2 (FAIL)
    [Documentation]    Engine Speed check data driven
    ...    Test in Line 3 will fail
    [Tags]    noncritical
    CheckSpeed    1    500    25
    CheckSpeed    2    100    10
    CheckSpeed    3    500    0
    CheckSpeed    4    4500    900
    CheckSpeed    5    2100    525
    CheckSpeed    6    3400    1020

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample3.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

*** Keywords ***
CheckSpeed
    [Arguments]    ${gear}    ${engspd}    ${expected}
    CanEasy Set Value    ECU1_EngineSpeed    ${engspd}
    CanEasy Set Value    ECU1_Gear    ${gear}
    CanEasy Is Value Equal    ECU2_VehicleSpeed    ${expected}

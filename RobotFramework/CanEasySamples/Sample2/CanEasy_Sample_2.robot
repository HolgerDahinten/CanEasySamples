*** Settings ***
Documentation     shows how to use loops
Suite Setup
Suite Teardown
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           ../../TestLibrary/caneasy.py    # CanEasy interface

*** Variables ***
@{testspeeds}     17    27    37    47    57
@{testgears}      1    3    5

*** Test Cases ***
Init CanEasy
    # Prepare CAN Simulation environment
    CanEasy Init
    CanEasy Workspace Load    ${CURDIR}\\..\\CanEasy_Sample.csm
    Sleep    500 ms
    CanEasy Simu Start
    Sleep    500 ms

Test 1
    [Documentation]    Change Engine Speed from 50 to 150 in a for loop.
    ...    Result is checked by formula.
    ${gear}=    set variable    1
    CanEasy Set Value    ECU1_Gear    ${gear}
    FOR    ${enginespeed}    IN RANGE    50    150
        CanEasy Set Value    ECU1_EngineSpeed    ${enginespeed}
        ${vehiclespeed}=    evaluate    int(${enginespeed} * ${gear} * 0.05)
        CanEasy Is Value Equal    ECU2_VehicleSpeed    ${vehiclespeed}
    END

Test 2
    [Documentation]    Change Engine Speed to a list of values
    ${gear}=    set variable    ${2}
    CanEasy Set Value    ECU1_Gear    ${gear}
    FOR    ${enginespeed}    IN    @{testspeeds}
        CanEasy Set Value    ECU1_EngineSpeed    ${enginespeed}
        ${vehiclespeed}=    evaluate    int(${enginespeed} * ${gear} * 0.05)
        CanEasy Is Value Equal    ECU2_VehicleSpeed    ${vehiclespeed}
    END

Test 3
    [Documentation]    Nested Loops
    FOR    ${enginespeed}    IN    @{testspeeds}
        test all gears    ${enginespeed}
    END

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample2.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

*** Keywords ***
test all gears
    [Arguments]    ${engspeed}
    CanEasy Set Value    ECU1_EngineSpeed    ${engspeed}
    FOR    ${gear}    IN    @{testgears}
        CanEasy Set Value    ECU1_Gear    ${gear}
        ${vehiclespeed}=    evaluate    int(${engspeed} * ${gear} * 0.05)
        CanEasy Is Value Equal    ECU2_VehicleSpeed    ${vehiclespeed}
    END

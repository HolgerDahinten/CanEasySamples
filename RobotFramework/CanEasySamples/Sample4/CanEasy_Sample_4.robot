*** Settings ***
Documentation     Test with Values from JSON File
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           ../../TestLibrary/caneasy.py    # CanEasy interface
Library           OperatingSystem

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
    ${FILECONTENT}=    Get File    ${CURDIR}\\Test_Values_1.json
    ${JSON}=    evaluate    json.loads($FILECONTENT)    json
    FOR    ${ELEMENT}    IN    @{JSON}
        CheckSpeed    ${ELEMENT['gear']}    ${ELEMENT['rpm']}    ${ELEMENT['speed']}
    END

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample4.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

*** Keywords ***
CheckSpeed
    [Arguments]    ${gear}    ${engspd}    ${expected}
    CanEasy Set Value    ECU1_EngineSpeed    ${engspd}
    CanEasy Set Value    ECU1_Gear    ${gear}
    CanEasy Is Value Equal    ECU2_VehicleSpeed    ${expected}

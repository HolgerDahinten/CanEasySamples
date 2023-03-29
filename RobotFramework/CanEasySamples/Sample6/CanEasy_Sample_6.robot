*** Settings ***
Documentation     Shows the useage of external variable files for keyword expansion
Library           ../../python/Lib/site-packages/robot/libraries/BuiltIn.py    # An always available standard library with often needed keywords.
Library           ../../TestLibrary/caneasy.py    # CanEasy interface
Variables         CanEasy_Sample_6_variables.py

*** Test Cases ***
Init CanEasy
    # Prepare CAN Simulation environment
    CanEasy Init
    CanEasy Workspace Load    ${CURDIR}\\..\\CanEasy_Sample.csm
    Sleep    500 ms
    CanEasy Simu Start
    Sleep    500 ms

Test 1
    [Documentation]    Test Ignition with use of external variables
    # Set Ignition to 1
    CanEasy Set Value    ${CanSig_Ignition}    1
    Sleep    500 ms
    # Check Signal Value
    ${sigval}=    CanEasy Get Value    ${CanSig_EngineRunning}
    Should Be Equal As Numbers    ${sigval}    1

Deinit CanEasy
    # Cleanup after Tests have been performed
    Sleep    500 ms
    CanEasy Save Record As    ${OUTPUT_DIR}\\sample6.celog
    CanEasy Simu Stop
    CanEasy Workspace Close

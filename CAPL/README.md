# CAPL Test

Povides a CANoe Project including a test module which can be used to test 
CAPL converter features of CanEasy.

* Use File->Import->CFG to import the Test.cfg file into CanEasy.
-> Database, environment variables, system-variables, panels are imported
* Convert the CAPL Code via the opened CAPL-Converter window (See context menu of Applications->CAPL->Compile)
-> Two CAN files are compiled as MultiStudio applications.
* Save the workspace of CanEasy in the same folder like CFG file
* Start the simulation
* Start the test via context menu of Applications->Test
-> XML and HTML report is generated in same folder
-> In report window you see "Test passed"
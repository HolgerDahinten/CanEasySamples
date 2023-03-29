"""
filename: caneasy.py
Description: Creates access to CanEasy functions using the win32com interface

All methods can be found within CanEasy directory under "ComHelp.hhc"
"""
__version__ = '0.2'

import msvcrt
import time
import win32com.client
from robot.api import logger


CanEasyProcess = None
CanEasyApp = None
CanEasyDiagStack = None

def caneasy_init():
    """The function initializes CanEasy.

    Examples:
    | CanEasy Init |
    """
    global CanEasyProcess
    global CanEasyApp

    logger.info("CanEasy RF Lib: " + __version__)

    if CanEasyProcess == None:
        CanEasyProcess = win32com.client.Dispatch("CanEasyATL.CanEasyProcess")
        CanEasyProcess.KeepAlive()
    else:
        logger.info("CanEasyProcess already initialized")

    if CanEasyApp == None:
        CanEasyApp = CanEasyProcess.GetApplication()
    else:
        logger.info("CanEasyApp already initialized")

    logger.info('CanEasy Version: %s' % CanEasyApp.version)

"""
****************************************************************
***** Diagnosis Stack Function
****************************************************************
"""
def caneasy_diag_init(path: str):
    """The function initializes the CanEasy Stack.

    Examples:
    | Caneasy Diagstack Init | //DB/Channel:Channel 1/Node:diag/Stack:Diag-Config |
    """
    global CanEasyDiagStack
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyDiagStack = CanEasyApp.Database.GetObjectByStringRef(path)
    if CanEasyDiagStack == None:
        raise AssertionError("Failed to get diag stack")

def caneasy_diag_send(data: str):
    """Send given Message over the Diag Stack.

    Examples:
    | ${diagresp}= | Caneasy Diagstack Send | 3E 00 |
    | Should be equal | ${diagresp} | 7E 00 |
    """
    if CanEasyDiagStack == None:
        raise AssertionError("CanEasyDiagStack is not initialized")

    bytedata = bytearray.fromhex(data)

    if not CanEasyDiagStack.TransmitDataAndWait(bytedata, -1):
        return "TIMEOUT"
    
    response = CanEasyDiagStack.LastResponse.Value
    
    stringdata = ""
    for bytedata in response:
        stringdata += '%02X ' % bytedata

    return stringdata.removesuffix(' ')

def caneasy_send_free_can_msg(bus: int, id: int, data: str):
    """Send a free CAN Message over the given busnumber

    Examples:
    | Caneasy Send Free Can Msg | 1 | ${0x700} | 02 10 83 55 55 55 55 55 |
    """
    bytedata = bytearray.fromhex(data)
    CanEasyApp.Database.Busses(bus).SendFreeCanMsg(id, bytedata, len(bytedata))

"""
****************************************************************
***** Common Functions
****************************************************************
"""
def caneasy_simu_start():
    """The function starts simulation on the CAN bus.
    
    Comment 
    The function can also be called if simulation is already started on the CAN bus. 

    Examples:
    | CanEasy Simu Start |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.StartSimulation()


def caneasy_simu_stop():
    """The function pauses simulation on the CAN bus.
    
    Comment 
    The "Stop Simulation" function can be called even if simulation is already paused. 

    Examples:
    | CanEasy Simu Stop |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.StopSimulation()


def caneasy_workspace_load(path: str):
    """The function loads the desired workspace.

    ``path`` Path and name of the csm file to be loaded.
    
    Comment:
    The file name must include the file extension; otherwise, a debugging error will occur. 

    Examples:
    | CanEasy Workspace Load | "c:\\\\temp\\\\workspace.csm" |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.LoadWorkspace(path)

    
def caneasy_workspace_close():
    """This method terminates the CanEasy process and closes the CanEasy application.
    
    Comment: 
    This method must be called to stop the CanEasy application if the method 
    'KeepAlive' has been used. Otherwise, the CanEasy application is closed 
    automatically after the CanEasy process object has been terminated. 
    
    Examples:
    | Can Workspace Close |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyProcess.KillApplication()
    
"""
****************************************************************
***** Functions to Set and Get Values
****************************************************************
"""
def caneasy_get_value(path: str):
    """
    This method returns the value of the given object
    
    Examples:
    | ${sig}= | CanEasy Get Value | SignalName
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    value = CanEasyApp.Database.GetValue(path)
    return float(value)

def caneasy_set_value(path: str, value: float):
    """
    This method changes the referenced object to a specific value
    
    Examples:
    | CanEasy Set Value | SignalName | 1 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.Database.SetValue(path, value)


def caneasy_get_value_string(path: str):
    """
    This method returns the value of the given object as string.
    Used for value tables.
    
    Examples:
    | ${sig}= | CanEasy Get Value String | SignalName
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    value = CanEasyApp.Database.GetValueString(path)
    return str(value)

def caneasy_set_value_string(path: str, value: str):
    """
    This method changes the referenced object to a specific value.
    
    Examples:
    | CanEasy Set Value String | SignalName | 1 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.Database.SetValue(path, value)


"""
****************************************************************
***** Functions to Check Values
****************************************************************
"""
# 
# HRESULT IsValueEqual([in] BSTR sRef, [in] double dVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_equal(path: str, value: float, timeout: int = 1000):
    """
    This method checks if the value is greater or equal then the given object
    
    Examples:
    | CanEasy is Value Equal | SignalName | 1 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueEqual(path, value, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not equal to %s' % (path, currentvalue, value))



# HRESULT IsValueLess([in] BSTR sRef, [in] double dVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_less(path: str, value: float, timeout: int = 1000):
    """
    This method checks if the value is less then the given object
    
    Examples:
    | CanEasy is Value Less | SignalName | 1 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueLess(path, value, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not less than %s' % (path, currentvalue, value))


# HRESULT IsValueGreater([in] BSTR sRef, [in] double dVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_greater(path: str, value: float, timeout: int = 1000):
    """
    This method checks if the value is greater then the given object
    
    Examples:
    | CanEasy is Value Greater | SignalName | 1 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueGreater(path, value, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not greater than %s' % (path, currentvalue, value))



# HRESULT IsValueLessOrEqual([in] BSTR sRef, [in] double dVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_less_or_equal(path: str, value: float, timeout: int = 1000):
    """
    This method checks if the value is less or equal then the given object
    
    Examples:
    | CanEasy is Value Less or Equal | SignalName | 1 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueLessOrEqual(path, value, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not less or equal to %s' % (path, currentvalue, value))


# HRESULT IsValueGreaterOrEqual([in] BSTR sRef, [in] double dVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_greater_or_equal(path: str, value: float, timeout: int = 1000):
    """
    This method checks if the value is greater or equal then the given object
    
    Examples:
    | CanEasy is value Greater or Equal | SignalName | 1 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueGreaterOrEqual(path, value, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not greater or equal to %s' % (path, currentvalue, value))




# HRESULT IsValueInRange([in] BSTR sRef, [in] double dMinVal, [in] double dMaxVal, [in] long timeout, [out, retval] VARIANT_BOOL* boValid);
def caneasy_is_value_in_range(path: str, value_min: float, value_max: float, timeout: int = 1000):
    """
    This method checks if the value is in the given range.
    
    Examples:
    | CanEasy is Value in Range | SignalName | 5 | 10 | 250 |
    """
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    result = CanEasyApp.Database.IsValueInRange(path, value_min, value_max, timeout)
    if result == False:
        currentvalue = CanEasyApp.Database.GetValue(path)
        raise AssertionError('%s: %s is not in range from %s to %s' % (path, currentvalue, value_min, value_max))


"""
****************************************************************
***** Record 
****************************************************************
"""

def caneasy_save_record_as(filename: str):
    """
    This method saves the current record under the given filename
    
    Examples:
    | CanEasy Save Record As | c:\\\\temp\\\\record.celog |
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.Record.Save(filename)



"""
****************************************************************
***** Executer
****************************************************************
"""
def caneasy_execute(path: str):
    """
    This method executes a scheduler table or send a message.
    
    Examples:
    | CanEasy Execute | Tab:ScheduleTable |
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.Database.Execute(path)


def caneasy_create_marker():
    """
    Creates a marker
    
    Examples:
    | CanEasy Create Marker |
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    CanEasyApp.Record.CreateMarker()




"""
****************************************************************
***** Complex value changers
****************************************************************
"""

def caneasy_change_sig_val(signame: str, startval: float, stopval: float, timerange: float, timediff: float):
    """
    This method changes the give signal from startval to stopval
    in the given timerange. Value is changed each timediff.
    """
    
    if CanEasyApp == None:
        raise AssertionError("CanEasy is not initialized")

    stepcount = timerange / timediff
    # print("We need " + str(stepcount) + " steps")
    
    stepsize = ( (stopval - startval) / stepcount )
    # print("We change in " + str(stepsize) + " value steps")
    
    signal = CanEasyApp.Database.GetObjectByStringRef("Sig:" + signame)
    if not signal:
        raise LookupError("CanSignal " + signame + " not found")
    
    currval = startval
    while True:
        if startval < stopval:
            signal.value = min(currval, stopval)
            # print("Value:  " + str(min(currval, stopval)))
        else:
            signal.value = max(currval, stopval)
            # print("Value:  " + str(max(currval, stopval)))
        
        if stepsize > 0 and currval >= stopval:
            break
        elif stepsize < 0 and currval <= stopval:
            break
        currval = currval + stepsize
        time.sleep(timediff / 1000.0)

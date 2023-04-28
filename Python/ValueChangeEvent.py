from caneasylib import *
import win32com.client as win32com

# Get CanEasyApplication instance
caneasy:ICanEasyApplication = getCanEasy()

class ChangeEvent:
    def OnValueChanged(self, _arg):
        arg = IChangeArg(_arg)
        valItem = IValue(arg.Item.DBItem)
        caneasy.MakeReport(f"{valItem.Name} = {valItem.Value}", constants.ReportTypeInformation)
 
@entry
class Application(BaseApplication):
    def OnStarting(self):        
        print("Example to handle value change events from database")

        # Create database item and assign reference
        sig = caneasy.CreateDatabaseItem()
        sig.StringRef = "//DB/Channel:Channel/Node:ECU/Msg:Message/Sig:Signal"
        
        # Activate change events
        recursive = False
        multithread = True
        sig.ActivateChangeEvents(recursive, multithread)
        win32com.WithEvents(sig, ChangeEvent)


from caneasylib import *
import win32com.client as win32com

# Get CanEasyApplication instance
caneasy:ICanEasyApplication = getCanEasy()

class TrsEvent:
    def OnTransmission(self, _trs):
        trs = ITransmissionData(_trs)
        caneasy.MakeReport(f"Message Id={hex(trs.MsgID.Plain)}, Rx={trs.Received}, Data={bytes(trs.Data.Array).hex()}" , constants.ReportTypeInformation);

@entry
class Application(BaseApplication):
    def OnStarting(self):
        msg = caneasy.CreateDatabaseItem()
        msg.StringRef = "Msg:Message"
        win32com.WithEvents(msg, TrsEvent)
        msg.TransmissionEvent.Active = True

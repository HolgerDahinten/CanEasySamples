from caneasylib import *
import win32com.client as win32com

@entry
class Application(BaseApplication):
    def OnStarting(self):
        # Get CanEasyApplication instance
        caneasy:ICanEasyApplication = getCanEasy()
        
        # Create filter to process message record entries
        filter = caneasy.Record.CreateFilter(constants.MsgRecordEntry) 
        # Create iterator to and walk over the record
        iter = caneasy.Record.CreateIterator(filter)
        while iter.Next():
            # Write information about the record entry
            entry = win32com.CastTo(iter.RecordEntry, "IMsgRecordEntry")
            caneasy.MakeReport("TS={:-010.4f}, Bus={}, Id=0x{:x}, Rx={}, Data={}".format(entry.Timestamp*3600, entry.Bus.Name, entry.Id.Plain, entry.Rx, bytes(entry.Data).hex()), constants.ReportTypeInformation)

        # Stop application
        exit()


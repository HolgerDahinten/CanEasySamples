from caneasylib import *

@entry
class Application(BaseApplication):
    def OnStarting(self):
    
        # This example creates a database.
        caneasy:ICanEasyApplication = getCanEasy()
        
        # Create a bus/channel and assign the hardware.
        bus = caneasy.Database.Busses.AddBus(constants.BUSTYPE_CAN, "MyBus")
        bus.SelectHardware("Schleissheimer Virtual", 0, 0)

        # Add ecu.         
        ecu = bus.ControlUnits.AddControlUnit("MyECU")

        # Add message with id 0x12A and DLC 8.
        msg = ecu.Messages.AddMessage("MyMsg", 0x12A, 8)

        # Add signal with starbit 0 and bitlength 8
        sig = msg.Signals.AddSignal("MySig", 0, 8, constants.BYTEORDER_INTEL)

        # Init signal value to 1.
        sig.Value = 1;

        # Create a value table and assign it to the signal.
        table = caneasy.Database.ValueTables.AddValueTable("MyTable")
        table.TableEntries.AddValueTableEntry("off", 0, 0)
        table.TableEntries.AddValueTableEntry("on", 1, 1)
        sig.ValueTable = table

        # Application finished.
        exit()

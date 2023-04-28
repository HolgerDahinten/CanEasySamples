using CanEasy;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        protected override void OnStarting()
        {
            // This example creates a database.

            // Create a bus/channel and assign the hardware.
            var bus = CanEasy.Database.Busses.AddBus(BusType.BUSTYPE_CAN, "MyBus");            
            bus.SelectHardware("Schleissheimer Virtual", 0, 0);

            // Add ecu.
            var ecu = bus.ControlUnits.AddControlUnit("MyECU");

            // Add message with id 0x12A and DLC 8.
            var msg = ecu.Messages.AddMessage("MyMsg", 0x12A, 8);

            // Add signal with starbit 0 and bitlength 8.
            var sig = msg.Signals.AddSignal("MySig", 0, 8, ByteOrder.BYTEORDER_INTEL);

            // Init signal value to 1.
            sig.Value = 1;

            // Create a value table and assign it to the signal.
            var table = CanEasy.Database.ValueTables.AddValueTable("MyTable");
            table.TableEntries.AddValueTableEntry("off", 0, 0);
            table.TableEntries.AddValueTableEntry("on", 1, 1);
            sig.ValueTable = table;

            // Application finished.
            Exit();
        }
    }
}

using CanEasy;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        protected override void OnStarting()
        {
            System.Console.WriteLine("Example to handle value change events from database");

            // Create database item and assign reference
            var sig = CanEasy.CreateDatabaseItem();
            sig.StringRef = "//DB/Channel:Channel/Node:ECU/Msg:Message/Sig:Signal";

            // Activate change events
            sig.ActivateChangeEvents(recursive:true, multithread:true);

            sig.OnValueChanged += (arg) =>
            {
                var item = (IValue)arg.Item.DBItem;
                CanEasy.MakeReport($"{item.Name} = {item.Value}", ReportType.ReportTypeInformation);
            };
        }
    }
}

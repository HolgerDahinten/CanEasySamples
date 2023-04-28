using CanEasy;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        protected override void OnStarting()
        {
            var msg = new CanEasy.DatabaseItem();
            msg.StringRef = "Msg:Message";
            msg.OnTransmission += (trs) =>
            {
                var sData = System.BitConverter.ToString((byte[])trs.Data.Array);
                CanEasy.MakeReport($"Message Id=0x{trs.MsgID.Plain.ToString("x2")}, Rx={trs.Received}, Data={sData}" , ReportType.ReportTypeInformation);
            };
            msg.TransmissionEvent.Active = true;
        }
    }
}

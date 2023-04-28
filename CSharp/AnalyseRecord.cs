using CanEasy;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        protected override void OnStarting()
        {
			// Create filter to process message record entries
            var filter = CanEasy.Record.CreateFilter(RecordEntryType.MsgRecordEntry);
			// Create iterator to and walk over the record
            var iter = CanEasy.Record.CreateIterator(filter);
            while(iter.Next())
            {
				// Write information about the record entry
                var entry = (MsgRecordEntry)iter.RecordEntry;
                var sData = System.BitConverter.ToString((byte[])entry.Data);
                CanEasy.MakeReport($"TS={(entry.Timestamp*3600).ToString("000.0000")}, Bus={entry.Bus.Name}, Id=0x{entry.Id.Plain.ToString("x")}, Rx={entry.Rx}, Data={sData}", ReportType.ReportTypeInformation);
            }

			// Stop application
            Exit();
        }
    }
}

using CanEasy;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        private Stack oStack;
        private byte[] gBuffer;

        public Application()
        {
            CanEasy.MakeReport("UDS Simulation is running", ReportType.ReportTypeInformation);
        }

        public static uint CalculateChecksum(ulong length, byte[] data)
        {
            uint num = 0u;
            for (ulong num2 = 0uL; num2 < length; num2++)
            {
                num ^= data[num2];
                for (byte b = 0; b < 8; b = (byte)(b + 1))
                {
                    num = (((num & 0x80000000u) != 2147483648u) ? (num << 1) : ((num << 1) ^ 0x4C11DB7u));
                    num &= 0xFFFFFFFFu;
                }
            }

            return num;
        }

        protected override void OnStarting()
        {
            gBuffer = new byte[99];
            for(int i=0; i < gBuffer.Length; ++i)
                gBuffer[i] = (byte)i;

            if(oStack == null)
            {
                oStack = (Stack)CanEasy.Database.GetObjectByStringRef("Diag-Simu");
                if(oStack == null)
                {
                    CanEasy.MakeReport("Stack not found", ReportType.ReportTypeError);
                    return;
                }
                oStack.TransmissionEvent.Active = true;
                oStack.OnTransmission += OnTransmission;
            }
        }

        protected void OnTransmission(CanEasy.TransmissionData t)
        {
            if(t.Timeout)
                return;

            byte[] txBuffer = null;
            byte posRes;
            byte[] data = null;

            data = (byte[])t.Data.Array;

            // Is Response?
            if((data[0] & 0x40) != 0)
                return;

            posRes = (byte)(data[0] | 0x40);

            // Session Control
            if(data[0] == 0x10)
            {
                txBuffer = new byte[6];
                txBuffer[0] = posRes;
                txBuffer[1] = data[1];
                txBuffer[2] = 0x00;
                txBuffer[3] = 0x32;
                txBuffer[4] = 0x01;
                txBuffer[5] = 0xF4;
            }
            else if(data[0] == 0x11)
            {
                txBuffer = new byte[2];
                txBuffer[0] = posRes;
                txBuffer[1] = data[1];
            }
            // Tester Present
            else if( data[0] == 0x3e)
            {
                txBuffer = new byte[2];
                txBuffer[0] = posRes;
                txBuffer[1] = data[1];
            }
            // Security access
            else if(data[0] == 0x27)
            {
                if(data[1] == 0x11)
                {
                    txBuffer = new byte[6];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = 0xaa;
                    txBuffer[3] = 0xaa;
                    txBuffer[4] = 0xaa;
                    txBuffer[5] = 0xaa;
                }
                else
                {
                    txBuffer = new byte[2];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                }
            }
            // Write Data by ID
            else if(data[0] == 0x2e)
            {
                txBuffer = new byte[3];
                txBuffer[0] = posRes;
                txBuffer[1] = data[1];
                txBuffer[2] = data[2];
            }	
            // Routine Control
            else if(data[0] == 0x31)
            {
                if(data[2] == 0x02 && data[3] == 0x03)
                {
                    txBuffer = new byte[4];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                    txBuffer[3] = data[3];
                }
                else if(data[2] == 0xff && data[3] == 0x00 ||
                        data[2] == 0x02 && data[3] == 0x02 ||
                        data[2] == 0xff && data[3] == 0x01)
                {
                    txBuffer = new byte[5];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                    txBuffer[3] = data[3];
                    txBuffer[4] = 0x00;
                }
            }
            // Request Download
            else if(data[0] == 0x34)
            {
                txBuffer = new byte[4];
                txBuffer[0] = posRes;
                txBuffer[1] = 0x20;
                txBuffer[2] = 0x0f;
                txBuffer[3] = 0xf2;
            }
            // Transfer Download (76 01 b0 0c eb 84)
            else if(data[0] == 0x36)
            {
                txBuffer = new byte[2];
                txBuffer[0] = posRes;
                txBuffer[1] = data[1];
            }            
            else if(data[0] == 0x37)
            {
                txBuffer = new byte[1];
                txBuffer[0] = posRes;
            }
            else if(data[0] == 0x22)
            {
                if(data[1] == 0xf1 && data[2] == 0x87) // VW Spare Part Number
                {
                    string sSerial = "0Z1915184AG";
                    var tmp = System.Text.Encoding.ASCII.GetBytes(sSerial);
                    txBuffer = new byte[tmp.Length+3];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                    for(var i = 0; i < tmp.Length; ++i)
                        txBuffer[i+3] = tmp[i];
                }
                else if(data[1] == 0xf1 && data[2] == 0x89) // VW Software Version Number
                {
                    string sSerial = "1122";
                    var tmp = System.Text.Encoding.ASCII.GetBytes(sSerial);
                    txBuffer = new byte[tmp.Length+3];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                    for(var i = 0; i < tmp.Length; ++i)
                        txBuffer[i+3] = tmp[i];
                }
                else if(data[1] == 0xf1 && data[2] == 0xd5) // FDS Project Data
                {
                    txBuffer = new byte[9];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                    txBuffer[3] = 0x01;
                    txBuffer[4] = 0xa2;
                    txBuffer[5] = 0xa3;
                    txBuffer[6] = 0xa4;
                    txBuffer[7] = 0xa5;
                    txBuffer[8] = 0xa6;
                }
                else if(data[1] == 0xf1 && data[2] == 0xdf) // ECUProgrammingInformation
                {
                    txBuffer = new byte[3];
                    txBuffer[0] = posRes;
                    txBuffer[1] = data[1];
                    txBuffer[2] = data[2];
                } 
            }
            else
            {
                CanEasy.MakeReport(string.Format("No Response for Request 0x{0:X} defined", data[1]), ReportType.ReportTypeWarning);
            }
            if(txBuffer != null)
            {
                oStack.TransmitData(txBuffer);
            }
        }
    }
}

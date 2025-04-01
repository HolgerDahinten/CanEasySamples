using System;
using System.Diagnostics;
using CanEasy;

namespace MyApplication
{
    class TestReportHelper
    {
        private TestReport _testReport;
        private ICanEasyApplication _ce;
        private string _curTest;
        private bool _testOK = true;

        public TestReportHelper(ICanEasyApplication app, string title)
        {
            _ce = app;
            _testReport = new TestReport();
            _testReport.Title = title;
            _testReport.StartTestReport(_ce.WorkspacePath, title);
        }

        ~TestReportHelper()
        {
            CloseTestReport();
        }        

        private void DoReport(string sMsg)
        {
            _ce.MakeReport(sMsg, ReportType.ReportTypeInformation);
        }
        
        public void TestStep(string sMsg)
        {
            DoReport(sMsg);
            _testReport.Step(_curTest, sMsg);
        }

        public void TestWarning(string sMsg)
        {
            DoReport(sMsg);
            _testReport.StepWarning(_curTest, sMsg);
        }

        public void TestPass(string sMsg)
        {
            DoReport(sMsg);
            _testReport.StepPass(_curTest, sMsg);
        }

        public void TestFail(string sMsg)
        {
            DoReport(sMsg);
            _testReport.StepFail(_curTest, sMsg);
            _testOK = false;
        }

        public void OpenTestcase(string sName, string sDesc, string sId)
        {
            _curTest = sName;
            _testReport.OpenTestcase(sName, sDesc, sId);
        }

        public void CloseTestReport()
        {
            if(_testReport == null)
                return;
                
             _testReport.CloseTestReport();
            

            try
            {
                string fileName = _ce.WorkspacePath + _testReport.Title + ".html";
                Process.Start(new ProcessStartInfo
                {
                    FileName = fileName,
                    UseShellExecute = true
                });            
            }
            catch(Exception)
            {
                
            }

            _testReport = null;

            if(_testOK)
                _ce.MakeReport("Test OK", ReportType.ReportTypeInformation);
            else
                _ce.MakeReport("Test Failed", ReportType.ReportTypeError);
       }

    }
}
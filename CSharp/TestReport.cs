using CanEasy;
//using System.IO;

namespace MyApplication
{
    public class Application : BaseApplication
    {
        private bool CheckResult(bool boResult, string function, TestReport test)
        {
            if(boResult)
                test.StepPass("", function + " within 50 ms, passed", 1);
            else
                test.StepFail("", function + " within 50 ms, failed", 1);
            return boResult;
        }

        private void TestSignals(Signal signal, TestReport test, double dValue)
        {
            var sig = signal.StringRef;
            CheckResult(CanEasy.Database.IsValueEqual(sig, dValue, 50), $"IsValueEqual {dValue}", test);
            CheckResult(CanEasy.Database.IsValueGreater(sig, dValue-1, 50), $"IsValueGreater {dValue-1}", test);
            CheckResult(CanEasy.Database.IsValueLess(sig, dValue+1, 50), $"IsValueLess {dValue+1}", test);
            CheckResult(CanEasy.Database.IsValueLessOrEqual(sig, dValue, 50), $"IsValueLessOrEqual {dValue}", test);
            CheckResult(CanEasy.Database.IsValueGreaterOrEqual(sig, dValue, 50), $"IsValueGreaterOrEqual {dValue}", test);
            CheckResult(CanEasy.Database.IsValueInRange(sig, dValue-1, dValue+1, 50), $"IsValueInRange {dValue-1}-{dValue+1}", test);
        }

        protected override void OnStarting()
        {
            // This example is used test functions of CanEasy.
			// It generates a html report which is opened at the end of the test run.
			
            // Create a test report file.
            var test = new TestReport();
            test.StartTestReport(System.IO.Path.GetTempPath(), "MyReport");

            try
            {
                test.OpenTestcase("Init signal", "", "");

                // Get signal from database.
                var sig = (Signal)CanEasy.Database.GetObjectByStringRef("Sig:MySig");
                if(sig == null)
                {
                    test.StepInconclusive("Missing signal", "No signal with name MySig found", 1);
                    return;
                }                

                test.OpenGroup("Test valid signal values", "", "");

                    test.OpenTestcase("Test signal values 5", "", "");
                    test.Step("", "Setting MySig to 5", 1);
                    sig.Value = 5;
                    TestSignals(sig, test, 5);

                    test.OpenTestcase("Test signal values 8", "", "");
                    test.Step("", "Setting MySig to 8", 1);
                    sig.Value = 8;
                    TestSignals(sig, test, 8);

                test.CloseGroup();

                test.OpenGroup("Test invalid signal values", "", "");

                    test.OpenTestcase("Test invalid signal values 5", "", "");
                        test.Step("", "Setting MySig to 5", 1);
                        sig.Value = 5;
                        TestSignals(sig, test, 8);

                test.CloseGroup();
            }
            finally
            {
                test.CloseTestReport();
                System.Diagnostics.Process.Start(System.IO.Path.GetTempPath() + "MyReport.html");
                Exit();
            }

        }
    }
}

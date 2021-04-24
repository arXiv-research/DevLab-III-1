from __future__ import division
from datetime import datetime
from jinja2 import Environment

testsuitename = "FIX_Test_Suite"

testcaseInfo = {'123': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 123"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {'EcnReqID': "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "PASS",
                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '234': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 234"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "FAIL",
                                 "Actual CAMM Message": "Hello this the CAMM Message",
                                 "Actual FIX Message": "Hello this is the FIX Message."}},
                '345': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 345"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                        "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                        "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                        {
                        "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                        "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                        },
                        "Result": {"OverallResult": "PASS",
                                   "Actual CAMM Message": "Hello this the CAMM Message",
                                   "Actual FIX Message": "Hello this is the FIX Message."}},
                '456': {"Inputs": {"Description": "Description1", "SecurityID": "TestCase 456"},
                        "Expected Outputs": {"CAMM Message1": "Message Output1", "CAMM Message2":  "Message output2"},
                        "CAMM Responses": {
                            "Actual CAMM Response1": {"EcnReqID": "234", "Quantity": "2"},
                            "Actual CAMM Response2": {"EcnReqID2": "123", "Quantity2": "2", "Time": "XX:XX"}
                        },
                        "FIX Responses":
                            {
                                "Actual FIX Response1": {"ReqID2": "123123", "orderID2": "2", "Quantity": "40"},
                                "Actual FIX Response2": {"ReqID2": "123123", "orderID2": "2"}
                            },
                        "Result": {"OverallResult": "PASS",
                                  "Actual CAMM Message": "Hello this the CAMM Message",
                                  "Actual FIX Message": "Hello this is the FIX Message."}}
                }

# using the route decorator to tell the Flask what URL should trigger our function
def template_test():
    test_case_result = {}
    for testcase in testcaseInfo:
        test_case_result[testcase] = testcaseInfo[testcase]["Result"]["OverallResult"]
    input_length = 0
    camm_responses_length = 0
    fix_message_length = 0
    output_camm_messages_length = 0
    for elem in testcaseInfo:
        input_length=len(testcaseInfo[elem]["Inputs"])
        camm_responses_length=len(testcaseInfo[elem]["CAMM Responses"])
        fix_responses_length=len(testcaseInfo[elem]["FIX Responses"])
        output_camm_messages_length=len(testcaseInfo[elem]["Expected Outputs"])

    if (camm_responses_length == fix_responses_length == output_camm_messages_length):
        pass
    else:
        raise ValueError("We dont have the proper inputs for the Report")

    input_fields = []
    camm_message_fields = []
    fix_message_fields = []
    output_camm_messages = []
    for elem in testcaseInfo:
        for elem1 in testcaseInfo[elem]:
            if elem1 == "Inputs":
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in input_fields:
                        input_fields.append(input_value)
            elif elem1 == "Expected Outputs":
                for output_value in testcaseInfo[elem][elem1]:
                    if output_value not in output_camm_messages:
                        output_camm_messages.append(output_value)
            elif "CAMM Responses" == elem1:
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in camm_message_fields:
                        camm_message_fields.append(input_value)
            elif "FIX Responses" == elem1:
               for input_value in testcaseInfo[elem][elem1]:
                   if input_value not in fix_message_fields:
                        fix_message_fields.append(input_value)


    print(input_fields)
    print(fix_message_fields)
    print(camm_message_fields)
    print(output_camm_messages)

    testcasedetails = test_case_result
    count = 0
    for dv in testcasedetails.values():
        if dv == "PASS":
            count = count + 1

    total = len(testcasedetails)
    teststatus = [testsuitename, total, count, total - count, str(round((count / total) * 100, 1))]
    try:
        with open("./templates/template.html", 'r') as temp1:
            htmlval = temp1.read()
            jinja_env = Environment().from_string(htmlval).render(title="Test Execution Report: {}".format(testsuitename),
                                                                  testsuite=testsuitename,
                                                                  statusdet=teststatus,
                                                                  td=testcaseInfo,
                                                                  input_length=input_length,
                                                                  camm_responses_length=camm_responses_length,
                                                                  fix_message_length=fix_message_length,
                                                                  output_camm_messages_length=output_camm_messages_length,
                                                                  input_fields=input_fields,
                                                                  output_fields= zip(camm_message_fields,fix_message_fields),
                                                                  camm_message_fields=camm_message_fields,
                                                                  fix_message_fields=fix_message_fields,
                                                                  output_camm_messages=output_camm_messages)

            timestamp = datetime.timestamp(datetime.now())
            report_filename = "./reports/report_{}_{}.html".format(testsuitename, timestamp)
            with open(report_filename, 'w') as report:
                report.write(jinja_env)
        return "Success"
    except FileNotFoundError:
        print("File not found")
        return "Failed"

if __name__ == '__main__':
    template_test()

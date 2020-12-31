from main import Tool

tool = Tool()

tool.exist_code_number = [1, 2, 3]
tool.javasource_path = "/home/mass/selkit/Research/project/temp/tempa"
tool.testcase_coverage = {
    "test0": {
        "line1": 1,
        "line2": 1,
        "line3": 0
    },
    "test1": {
        "line1": 1,
        "line2": 0,
        "line3": 1
    },
    "test2": {
        "line1": 1,
        "line2": 1,
        "line3": 1
    },
}
tool.testcase_passfail = {
    "test0": True,
    "test1": False,
    "test2": True
}

tool.calculateOchiai()
tool.makeSuspiciousValueHtml()

print(tool.ochiai)
import sys, os
from codeBlock import CodeBlock
from pyJVM import JavaInterpreter
from utility import Util

class Debugger:

    def __init__(self, testCodeFilePath):
        self.codeBlocks = []
        with open(testCodeFilePath) as fp:
            self.test_code = fp.read().splitlines()
    
    def assignSourceCode(self, sourcecode_filepath):
        with open(sourcecode_filepath) as fp:
            raw_sourcecode = fp.read().splitlines()
            line_count = 1
            sourcecode = []
            for source_line in raw_sourcecode:
                if source_line.strip():
                    sourcecode.append((source_line.strip(), line_count))
                line_count += 1
            self.codeBlocks.append((os.path.basename(sourcecode_filepath), self._splitCodeBlock(sourcecode)))

    def testDecode(self):
        for test_code_line in self.test_code:
            command = test_code_line.split(":")[0].strip()
            argument = test_code_line.split(":")[1].strip()
            self.buggy_valiable = {}
            if command == "BuggyPoint":
                next = ""
                for token in argument.split():
                    if token == "var":
                        next = "varname"
                        continue
                    elif token == "in_line":
                        next = "linenum"
                        continue
                    elif token == "of":
                        next = "sourcepath"
                        continue
                    
                    if next == "varname":
                        self.buggy_valiable["name"] = token
                        print("varname: " + self.buggy_valiable["name"])
                    elif next == "linenum":
                        self.buggy_line = int(token)
                        print("line: " + str(self.buggy_line))
                    elif next == "sourcepath":
                        self.buggy_file = token
                        print("source: " + self.buggy_file)
    
    def _splitCodeBlock(self, sourceCode:list):
        buf = ""
        read_mode = "normal"
        escape = False
        for_allow_semicolon_count = 0
        root_codeblock = CodeBlock()
        for source_line in sourceCode:
            for_line_first = True
            for character in source_line[0]:
                if read_mode == "normal": #normal code
                    if character == ";":
                        if buf.strip():
                            if Util.splitToken(buf.strip())[0] == "for" and for_line_first:
                                for_allow_semicolon_count = 2
                                for_line_first = False
                        if for_allow_semicolon_count:
                            for_allow_semicolon_count -= 1
                            buf += character
                        else:
                            if buf:
                                root_codeblock.assign((buf.strip(), source_line[1]))
                                buf = ""
                    elif character == "{":
                        root_codeblock.diveInner()
                        if buf:
                            root_codeblock.assign((buf.strip(), source_line[1]))
                            buf = ""
                    elif character == "}":
                        root_codeblock.floatInner()
                        if buf:
                            root_codeblock.assign((buf.strip(), source_line[1]))
                            buf = ""
                    elif character == "\"" and not escape:
                        read_mode = "string"
                        buf += character
                    else:
                        buf += character
                elif read_mode == "string": #on string token
                    if character == "\"" and not escape:
                        read_mode = "normal"
                        escape = False
                    elif character == "\\":
                        escape = True
                    else:
                        escape = False
                    buf += character
        return root_codeblock
    
    def findBuggyPoint(self):

        #Detecting Buggy Point in Source Code
        for i, (filename, codeblock) in enumerate(self.codeBlocks):
            if filename == self.buggy_file:
                buggy_codeblock_index = i
                for j, (sentence, code_linenum) in enumerate(codeblock.allSentence()):
                    # print("code: %s" % str(codeblock.allSentence()[j]))
                    if not j > len(codeblock.allSentence()) - 2:
                        condition = code_linenum <= self.buggy_line and codeblock.allSentence()[j + 1][1] > self.buggy_line
                    else:
                        condition = code_linenum <= self.buggy_line
                    if condition:
                        self.buggy_index = j
                        # print(codeblock.allSentence()[j])
                        # print(self.buggy_index)
                break
        
        #Reverse Viewing on Source Code
        _, buggy_codeblock = self.codeBlocks[buggy_codeblock_index]
        buggy_block, absolute_index = buggy_codeblock.allIndexToAbsoluteIndex(self.buggy_index)
        print(buggy_block.elements)
        print(absolute_index)
        for i in reversed(range(absolute_index)):
            if isinstance(buggy_block.elements[i], tuple):
                

        
    
    def preprocessing(self):
        self.all_type = Util.all_class + ["void", "short", "int", "long", "float", "double", "char", "boolean"]
        for name, code in self.codeBlocks:
            public_class = code.extractPublicClass()
            self.all_type = self.all_type + public_class
        self.public_attr = []
        for name, code in self.codeBlocks:
            self.public_attr += code.extractPublicAttr(self.all_type)
        for var in self.public_attr:
            print(var.toString())


if __name__ == "__main__":
    dbg = Debugger("testcode/test.tc")
    dbg.assignSourceCode("java-sourcecode/Calc.java")
    dbg.assignSourceCode("java-sourcecode/Form.java")
    Util.getAllClass()
    dbg.testDecode()
    dbg.preprocessing()
    dbg.findBuggyPoint()
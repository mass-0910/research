from codeBlock import CodeBlock
from collections import deque

class JavaInterpreter:
    
    def __init__(self):
        self.codeList = []
        self.executingCodeNumber = 0
        self.pc = 0
        self.stdoutQueue = deque([])
        pass

    def assignCode(self, codeBlock: CodeBlock):
        self.codeList.append(codeBlock)
    
    def setup(self):
        index = 0
        for code in self.codeList:
            self.pc = code.mainFunc()
            if self.pc != None:
                self.executingCodeNumber = index
                break
            index += 1
        print("file: %d" % self.executingCodeNumber)
        print("line: %d" % self.pc)

    def step(self):
        code = self.codeList[self.executingCodeNumber].getSentence(self.pc)
        
        
    def _stdout(self, str):
        self.stdoutQueue.append(str)
    
    def end(self):
        for str in self.stdoutQueue:
            print(str, end = "")

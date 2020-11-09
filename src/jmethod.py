from jvar import JVar
from utility import Util

class JMethod:

    def __init__(self, codeBlock):
        
        self.name = ""
        self.type = ""
        self.arguments = []
        self.local_vars = []
        self.is_public = False

        self.codeblock = codeBlock
        self._extractNameAndArgs()
    
    def getName(self):
        return self.name

    def getArgs(self):
        retval = []
        for arg in self.arguments:
            retval.append(arg.toString())
        return retval
    
    def getBlock(self):
        return self.codeblock

    def _extractNameAndArgs(self):
        sentence, _ = self.codeblock.elements[0]
        type_, name, template, is_array = JVar(sentence).getVarInfo()
        self.name = name
        self.type = "%s%s%s" % (type_, "<%s>" % template if template else "", "[]" if is_array else "")
        
        tokenised_sentence = Util.splitToken(sentence)
        if "public" in tokenised_sentence: self.is_public = True
        
        argument_tokens = tokenised_sentence[tokenised_sentence.index("(") + 1:len(tokenised_sentence) - 1]
        # print(argument_tokens)

        buf = ""
        for token in argument_tokens:
            if token == ",":
                # print(buf)
                self.arguments.append(JVar(buf))
                buf = ""
            else:
                buf += token + " "
        if buf:
            print(buf)
            self.arguments.append(JVar(buf))
        
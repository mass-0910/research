from jvar import JVar
from utility import Util

class JMethod:

    def __init__(self, class_, codeBlock):
        
        self.name = ""
        self.type = ""
        self.arguments = []
        self.local_vars = []
        self.is_public = False
        self.using_attr = []
        self.class_ = class_

        self.codeblock = codeBlock
        self._extractNameAndArgs()
        self._extractLocalVar()
    
    def getName(self):
        return self.name
    
    def getReturnType(self):
        return self.type

    def getArgs(self):
        retval = []
        for arg in self.arguments:
            retval.append(arg.toString())
        return retval
    
    def getBlock(self):
        return self.codeblock
    
    def getLocalVar(self):
        return self.local_vars
    
    def getUsingAttr(self):
        return self.using_attr
    
    def extractUsingAttr(self):
        self.using_attr = []
        local_vars_name = []
        for var in self.local_vars:
            local_vars_name.append(var.getName())
        for var in self.arguments:
            local_vars_name.append(var.getName())
        for sentence, linenum in self.codeblock.allSentence()[1:]:
            tokenized_sentence = Util.splitToken(sentence)
            next_is_method_or_other_attr = False
            for token in tokenized_sentence:
                if next_is_method_or_other_attr:
                    next_is_method_or_other_attr = False
                    continue
                if token == ".":
                    next_is_method_or_other_attr = True
                    continue
                if token[0] == "\"" and token[-1] == "\"":
                    continue
                if token.isdigit():
                    continue
                if not token in Util.keywords and not token in Util.all_type and not token in Util.symbol:
                    if not token in local_vars_name:
                        if token in [attr.getName() for attr in self.class_.public_attrs + self.class_.private_attrs]:
                             if not token in self.using_attr: self.using_attr.append(token)

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
            # print(buf)
            self.arguments.append(JVar(buf))
    
    def _extractLocalVar(self):
        for sentence, linenum in self.codeblock.allSentence()[1:]:
            tokenized_sentence = Util.splitToken(sentence)
            next_is_not_token_def = False
            for token in tokenized_sentence:
                if next_is_not_token_def:
                    next_is_not_token_def = False
                    continue
                if token == "new":
                    next_is_not_token_def = True
                if token in Util.all_type and not next_is_not_token_def:
                    var = JVar(sentence)
                    if var.getName() != ".":
                        self.local_vars.append(var)
        
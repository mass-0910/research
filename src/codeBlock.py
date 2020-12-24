from utility import Util
from enum import Enum
from jclass import JClass
from jvar import JVar

class CodeBlock:

    global_class = []

    def __init__(self):
        self.inner_block = None
        self.inner = False
        self.elements = []
        self.block_type = None
        self.variables = []
        self.methods = []
        self.types = []
        self.all_sentence = None
        self.class_name = ""
        self.method_name = ""

    def assign(self, sentence):
        if self.inner:
            self.inner_block.assign(sentence)
        else:
            self.elements.append(sentence)
    
    def diveInner(self):
        if self.inner:
            self.inner_block.diveInner()
        else:
            self.inner_block = CodeBlock()
            self.inner = True
    
    def floatInner(self):
        if self.inner:
            if self.inner_block.floatInner():
                self.elements.append(self.inner_block)
                self.inner = False
            return False
        else:
            return True #verify
    
    def mainFunc(self, init_line_number = 0):
        codenum = init_line_number
        for elm in self.elements:
            if isinstance(elm, tuple):
                source = elm[0]
                if(Util.splitToken(source)[0:4] == ["public", "static", "void", "main"]):
                    return codenum
                codenum += 1
            else:
                child = elm.mainFunc(codenum)
                if child != None:
                    return child
                else:
                    codenum += elm._count()
        return None
    
    def getSentence(self, codenum, init_line_number = 0):
        index = init_line_number
        for elm in self.elements:
            if(isinstance(elm, tuple)):
                if index == codenum:
                    return elm[0]
                index += 1
            else:
                child = elm.getSentence(codenum, index)
                if child != None:
                    return child
                else:
                    index += elm._count()
        return None
    
    def getElements(self, elmnum):
        return self.elements[elmnum]

    def getBlockType(self):
        if self.block_type == None:
            sentence, _ = self.elements[0] #First sentence of this code block
            tokenized_sentence = Util.splitToken(sentence)
            if "class" in tokenized_sentence:
                self.block_type = BlockType.class_def
            elif "interface" in tokenized_sentence:
                self.block_type = BlockType.interface
            elif "for" in tokenized_sentence:
                self.block_type = BlockType.for_loop
            elif "while" in tokenized_sentence:
                self.block_type = BlockType.while_loop
            elif "if" in tokenized_sentence:
                self.block_type = BlockType.if_branch
            elif "else" in tokenized_sentence:
                self.block_type = BlockType.else_branch
            elif "switch" in tokenized_sentence:
                self.block_type = BlockType.switch_branch
            else:
                self.block_type = BlockType.method
                # token_list = []
                # for i, token in enumerate(tokenized_sentence):
                #     if token in ["public", "private", "protected"]: #Access Modifier
                #         token_list.append("MODIFIER")
                #     elif token in ["final", "static", "transient", "volatile"] and detecting_token == 1: #Field
                #         token_list.append("FIELD")
                #     elif token == "(" or token == ")":
                #         token_list.append(token)
                #     else:
                #         token_list.append("OTHER")
        return self.block_type

    def extractClass(self):
        public_class = []
        for elm in self.elements:
            if not isinstance(elm, tuple):
                if elm.getBlockType() == BlockType.class_def:
                    public_class.append(JClass(elm))
        return public_class

    def extractUsedVar(self):
        self.used_var = []
        for elm in self.elements:
            if isinstance(elm, tuple):
                sentence, _ = elm
                tokenized_sentence = Util.splitToken(sentence)
                buf = ""
                for token in tokenized_sentence:
                    if token == '=':
                        if buf:
                            self.used_var.append(buf)
                    buf = token
        # print(self.used_var)
    
    def isPublicClass(self):
        if isinstance(self.elements[0], tuple):
            sentence, _ = self.elements[0]
            tokenized_sentence = Util.splitToken(sentence)
            if "public" in tokenized_sentence and "class" in tokenized_sentence:
                return tokenized_sentence[tokenized_sentence.index("class") + 1]
        return False
    
    @staticmethod
    def isSentence(element):
        return isinstance(element, tuple)
            
    
    def _count(self):
        count = 0
        for elm in self.elements:
            if isinstance(elm, tuple):
                count += 1
            else:
                count += elm._count()
        return count

    def allSentence(self):
        if self.all_sentence == None:
            self.all_sentence = self._allSentence()
        return self.all_sentence

    def _allSentence(self):
        retval = []
        for elm in self.elements:
            if isinstance(elm, tuple):
                retval.append(elm)
            else:
                retval += elm.allSentence()
        return retval
    
    def allIndexToAbsoluteIndex(self, all_index, init_index = 0) -> int:
        index = init_index
        for i, elm in enumerate(self.elements):
            # print("%s: %s" % (str(self.elements[0]), str(elm)))
            # print("%d" % index)
            if isinstance(elm, tuple):
                if index == all_index:
                    return (self, i)
                index += 1
            else:
                retval = elm.allIndexToAbsoluteIndex(all_index, index)
                if not isinstance(retval, int):
                    return retval
                else:
                    index += retval
        return index - init_index

    #debug
    def printBlock(self):
        print("++++++++++++++++++++CODE BLOCK++++++++++++++++++++")
        print("type: " + str(self.getBlockType()))
        for elm in self.elements:
            if isinstance(elm, tuple):
                print("%d: %s" % (elm[1], elm[0]))
            else:
                elm.printBlock()
        print("--------------------------------------------------")



class BlockType(Enum):
    class_def       = 0
    method          = 1
    interface       = 2
    for_loop        = 3
    while_loop      = 4
    if_branch       = 5
    else_branch     = 6
    switch_branch   = 7
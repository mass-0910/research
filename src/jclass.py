from jvar import JVar
from jmethod import JMethod
from utility import Util

class JClass:

    def __init__(self, codeBlock):
        self.name = ""
        self.public_attrs = []
        self.private_attrs = []
        self.public_methods = []
        self.private_methods = []
        self.is_public = False

        # extract class name
        self.name = self._extractName(codeBlock)
        codeBlock.class_name = self.name

        # extract class attributes
        self.public_attrs, self.private_attrs = self._extractAttrs(codeBlock)

        # extract class methods
        self.public_methods, self.private_methods = self._extractMethods(codeBlock)
    
    def getName(self):
        return self.name
    
    def getPublicAttrNames(self):
        retval = []
        for attr in self.public_attrs:
            type_, name, _, _ = attr.getVarInfo()
            retval.append(name)
        return retval
    
    def getMethodNames(self):
        retval = []
        for method in self.methods:
            name, block = method
            retval.append(name)
        return retval
    
    def printClassInfo(self):
        print("====ClassInfo====")
        print("name: %s" % self.name)
        print("scope: %s" % "public" if self.is_public else "private")
        print("public attributes:")
        for attr in self.public_attrs:
            print("\t%s" % attr.toString())
        print("private attributes:")
        for attr in self.private_attrs:
            print("\t%s" % attr.toString())
        print("public methods:")
        for method in self.public_methods:
            name, block = method.getName(), method.getBlock()
            print("\tmethod name: %s" % name)
            print("\tmethod arguments:")
            for arg in method.getArgs():
                print("\t\t%s" % arg)
            print("\tmethod sentence: ")
            for elm in block.allSentence():
                print("\t\t" + str(elm))
        print("private methods:")
        for method in self.private_methods:
            name, block = method.getName(), method.getBlock()
            print("\tmethod name: %s" % name)
            print("\tmethod arguments:")
            for arg in method.getArgs():
                print("\t\t%s" % arg)
            print("\tmethod sentence: ")
            for elm in block.allSentence():
                print("\t\t" + str(elm))
        print("====END====")
        
    
    def _extractName(self, codeBlock):
        sentence, _ = codeBlock.elements[0]
        tokenized_sentence = Util.splitToken(sentence)
        next = False
        self.is_public = "public" in tokenized_sentence
        for token in tokenized_sentence:
            if next : return token
            if token == "class":
                next = True
        return ""
    
    def _extractAttrs(self, codeBlock):
        public = []
        private = []
        for elm in codeBlock.elements:
            if isinstance(elm, tuple):
                sentence, _ = elm
                tokenized_sentence = Util.splitToken(sentence)
                for token in tokenized_sentence:
                    if token in Util.all_type and not "class" in tokenized_sentence:
                        if "public" in tokenized_sentence:
                            public.append(JVar(sentence))
                        else:
                            private.append(JVar(sentence))
                        break
                    elif token in Util.keywords:
                        continue
                    else:
                        break
        return (public, private)
    
    def _extractMethods(self, codeBlock):
        public = []
        private = []
        for elm in codeBlock.elements:
            if not isinstance(elm, tuple):
                sentence, _ = elm.elements[0]
                tokenized_sentence = Util.splitToken(sentence)
                next = False
                for token in tokenized_sentence:
                    if next:
                        if "public" in tokenized_sentence:
                            public.append(JMethod(elm))
                        else:
                            private.append(JMethod(elm))
                        break
                        next = False
                    if token in Util.all_type:
                        next = True
        return (public, private)
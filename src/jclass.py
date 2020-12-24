from jvar import JVar
from jmethod import JMethod
from utility import Util
import os.path as path
from os import makedirs

class JClass:

    def __init__(self, codeBlock):
        self.name = ""
        self.filename = ""
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
        for method in self.public_methods:
            method.extractUsingAttr()
        for method in self.private_methods:
            method.extractUsingAttr()
    
    def setFilename(self, name):
        self.filename = name
    
    def getName(self):
        return self.name
    
    def getFilename(self):
        return self.filename

    def getScope(self):
        if self.is_public:
            return "public"
        else:
            return "private"
    
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
        if not path.exists("class_info"):
            makedirs("class_info")
        with open("class_info/" + self.name, mode="w") as fp:
            print("====ClassInfo====", file=fp)
            print("name: %s" % self.name, file=fp)
            print("written in: %s" % self.filename, file=fp)
            print("scope: %s" % ("public" if self.is_public else "private"), file=fp)
            print("public attributes:", file=fp)
            for attr in self.public_attrs:
                print("\t%s" % attr.toString(), file=fp)
            print("private attributes:", file=fp)
            for attr in self.private_attrs:
                print("\t%s" % attr.toString(), file=fp)
            print("public methods:", file=fp)
            for method in self.public_methods:
                name, type_, block = method.getName(), method.getReturnType(), method.getBlock()
                print("\tmethod name: %s" % name, file=fp)
                print("\tmethod return type: %s" % type_, file=fp)
                print("\tmethod arguments:", file=fp)
                for arg in method.getArgs():
                    print("\t\t%s" % arg, file=fp)
                print("\tmethod local var: %s" % str([var.getName() for var in method.getLocalVar()]), file=fp)
                print("\tmethod using attributes: %s" % str(method.getUsingAttr()), file=fp)
                print("\tmethod sentence: ", file=fp)
                for elm in block.allSentence():
                    print("\t\t" + str(elm), file=fp)
            print("private methods:", file=fp)
            for method in self.private_methods:
                name, block = method.getName(), method.getBlock()
                print("\tmethod name: %s" % name, file=fp)
                print("\tmethod arguments:", file=fp)
                for arg in method.getArgs():
                    print("\t\t%s" % arg, file=fp)
                print("\tmethod local var: %s" % str([var.getName() for var in method.getLocalVar()]), file=fp)
                print("\tmethod using attributes: %s" % str(method.getUsingAttr()), file=fp)
                print("\tmethod sentence: ", file=fp)
                for elm in block.allSentence():
                    print("\t\t" + str(elm), file=fp)
            print("====END====", file=fp)
            
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
                            public.append(JMethod(self, elm))
                        else:
                            private.append(JMethod(self, elm))
                        break
                        next = False
                    if token in Util.all_type:
                        next = True
        return (public, private)
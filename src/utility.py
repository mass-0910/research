import os

class Util:

    symbol = [',', '.', '+', '-', '*', '/', '%', '{', '}', '[', ']', '(', ')', ';', ':', '=', '>', '<', '!']
    space = [' ', '\t', '\n', '\r']
    keywords = [   
                    "abstract", "assert", "break", "byte", "case", "catch", "class", "const", \
                    "continue", "default", "do", "else", "enum", "extends", "final", "finally", \
                    "for", "goto", "if", "implements", "import", "instanceof", "interface", "native", \
                    "new", "package", "private", "protected", "public", "return", "static", "strictfp", "super", \
                    "switch", "synchrnized", "this", "throw", "throws", "transient", "try", "volatile", "while"\
                ]
    class_modifier = ["abstract", "final", "strictfp"]
    all_class = []

    @staticmethod
    def getAllClass():
        with open(os.path.dirname(__file__) + "/java-classname.txt") as fp:
            Util.all_class = fp.readlines()
        for i, classname in enumerate(Util.all_class):
            Util.all_class[i] = classname.strip()

    @staticmethod
    def splitToken(sentence):
        retval = []
        buf = ""
        mode = 0 #normal
        escape = False
        for character in sentence:
            if mode == 0: #normal
                if character in Util.symbol:
                    if buf:
                        retval.append(buf)
                    retval.append(character)
                    buf = ""
                elif character in Util.space:
                    if buf:
                        retval.append(buf)
                        buf = ""
                elif character == "\"":
                    if buf:
                        retval.append(buf)
                    buf = "\""
                    mode = 1 #string
                else:
                    buf += character
            elif mode == 1: #string
                buf += character
                if character == "\"" and not escape:
                    retval.append(buf)
                    buf = ""
                    mode = 0
                elif character == "\\":
                    escape = True
                elif escape:
                    escape = False

        if buf:
            retval.append(buf)
            buf = ""
        return retval
    
    @staticmethod
    def isString(token):
        if token[0] == "\"" and token[-1] == "\"":
            return True
        else:
            return False
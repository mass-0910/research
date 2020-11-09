from utility import Util

class JVar:
    def __init__(self, def_sentence):

        # print("JVar accept: " + def_sentence)

        tokenized_sentence = Util.splitToken(def_sentence)
        # print(tokenized_sentence)

        next_vartoken = False
        next_tempratetoken = False
        next_arraytoken = False
        attr_type = ""
        template = ""
        is_array = False

        for token in tokenized_sentence:
            if not token in Util.keywords:
                if next_vartoken:
                    if token == "<":
                        next_vartoken = False
                        next_tempratetoken = True
                    elif token == "[":
                        is_array = True
                        next_vartoken = False
                        next_arraytoken = True
                    else:
                        self.name = token
                        self.type = attr_type
                        self.template = template
                        self.is_array = is_array
                        break
                elif next_tempratetoken:
                    if token == ">":
                        next_tempratetoken = False
                        next_vartoken = True
                    else:
                        template += token
                elif next_arraytoken:
                    if token == "]":
                        next_arraytoken = False
                        next_vartoken = True
                else:
                    if token in Util.all_type:
                        attr_type = token
                        next_vartoken = True
    
    def getVarInfo(self):
        return (self.type, self.name, self.template, self.is_array)
    
    def toString(self):
        array_str = "[]" if self.is_array else ""
        template_str = "<%s>" % self.template if self.template else ""
        return "`%s%s%s %s`" % (self.type, template_str, array_str, self.name)
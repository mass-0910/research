class Var:
    def __init__(self, type_, template, is_array, name):
        self.type = type_
        self.template = template
        self.is_array = is_array
        self.name = name
    
    def toString(self):
        array_str = "[]" if self.is_array else ""
        template_str = "<%s>" % self.template if self.template else ""
        return "`%s%s%s %s`" % (self.type, template_str, array_str, self.name)
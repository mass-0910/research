from jvar import JVar
from utility import Util

if __name__ == "__main__":
    Util.getAllClass()
    Util.all_type = Util.all_type + ["void", "short", "int", "long", "float", "double", "char", "boolean"]
    a = JVar("ArrayList<int>[] a = new ArrayList<int>[10]")
    print(a.toString())
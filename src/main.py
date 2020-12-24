import sys
import os.path as path
import os
import glob
import time
import subprocess
import traceback
import argparse
import json
from utility import Util
from javaparser import JavaParser

# /media/mass/0612390E12390469/eval/jsoup /media/mass/0612390E12390469/eval/jsoup/src/main/java/org/jsoup/parser/TokenQueue.java

class ArgumentError(Exception):
    pass

class SubProcessError(Exception):
    pass

class Tool:

    def __init__(self):
        self.mavenproject_path = ""
        self.javasource_path = ""
        self.javaclass_path = ""
        self.exist_code_number = []
        self.exist_test_number = []
        self.testcase_coverage = {}
    
    def setPath(self, mavenproject_path, javasource_path, expectedvaluefile_path=None):
        self.mavenproject_path = mavenproject_path
        self.javasource_path = javasource_path
    
    def phase1(self):
        try:
            self.compileMavenProject()
            self.source2ClassPath()
            print(self.javaclass_path)
            print(self.javaclass_name)
            self.makeEvosuiteTest()
        except:
            raise
    
    def phase2(self):
        try:
            self.source2ClassPath()
            self.addLineNum()
            self.compileMavenProject()
            self.compileEvosuiteTest()
            self.execEvosuiteTest()
            self.collectCoverage()
            self.collectObjectXML()
            self.makeCoverageCsv()
            self.undoAddLineNum()
        except:
            self.undoAddLineNum()
            raise

    def source2ClassPath(self):
        classnames = getClassname(self.javasource_path)
        packagename = getPackagename(self.javasource_path)
        print(classnames)
        print(packagename)
        if not classnames:
            print("%s has no class" % self.javasource_path)
            return
        for classname in classnames:
            parent = path.dirname(self.javasource_path)
            end = False
            before_dir = ""
            while parent != path.dirname(self.mavenproject_path):
                glob_list = []
                for dir_ in os.listdir(parent):
                    if path.isdir(path.join(parent, dir_)) and dir_ != before_dir:
                        glob_list.append(path.join(parent, dir_))
                classfile_pathes = []
                for globdir in glob_list:
                    classfile_pathes += glob.glob(path.join(globdir, "**/*.class"), recursive=True)
                # print(classfile_pathes)
                for classfile in classfile_pathes:
                    # print(classfile)
                    if path.basename(classfile) == classname + ".class" and packagename.replace('.', path.sep) in classfile:
                        classfile_packagename = packagename.replace('.', path.sep) + path.sep + classname + ".class"
                        self.javaclass_path = classfile.replace(classfile_packagename, "")
                        # print("a = " + packagename)
                        self.javaclass_name = packagename + "." + classname
                        end = True
                        break
                if end: break
                before_dir = path.basename(parent)
                parent = path.dirname(parent)
    
    def addLineNum(self):
        print("addLineNum start")
        self._copy(self.javasource_path, path.join(path.dirname(path.abspath(__file__)), "temp", "temp.java"))
        inserter = JavaParser(self.javasource_path)
        inserter.startInsert()

    def _fileCopyAndMakeLineList(self, filepath, temppath):
        with open(filepath, mode="r+") as f:
            with open(temppath, mode="w") as tmpf:
                tmpf.write(f.read())
            f.seek(0, 0)
            source_lines = [line.rstrip(os.linesep) for line in f.readlines()]
        return source_lines
    
    def _removeComment(self, source_lines):
        in_comment = False
        for i, line in enumerate(source_lines):
            buf = ""
            next = False
            for character in line:
                if not in_comment:
                    if character == "/" and not next:
                        next = True
                        continue
                    if next:
                        next = False
                        if character == "*":
                            in_comment = True
                            continue
                        elif character == "/":
                            break
                        else:
                            buf += "/"
                            continue

                if in_comment:
                    if character == "*" and not next:
                        next = True
                        continue
                    if next:
                        next = False
                        if character == "/":
                            in_comment = False
                    continue
                
                buf += character

            # print(buf)
            source_lines[i] = buf
        return source_lines
    
    def undoAddLineNum(self):
        self._undoCopy(self.javasource_path, path.join(path.dirname(path.abspath(__file__)), "temp", "temp.java"))
    
    def _copy(self, src_path, copy_path):
        with open(src_path, mode="r") as rf, open(copy_path, mode="w") as wf:
            wf.write(rf.read())

    def _undoCopy(self, src_path, copy_path):
        with open(copy_path, mode="r") as rf, open(src_path, mode="w") as wf:
            wf.write(rf.read())

    def compileMavenProject(self):
        result = subprocess.run(["mvn", "compile"], cwd=self.mavenproject_path)
        if result.returncode != 0:
            raise SubProcessError("Maven Compile finished with Error!")
    
    def getThisProjectPath(self):
        return path.dirname(path.dirname(path.abspath(__file__)))
    
    def makeEvosuiteTest(self):
        evosuite_command = ["java", "-jar", path.join(self.getThisProjectPath(), "ext_modules", "evosuite-1.1.0.jar"), "-class", self.javaclass_name, "-projectCP", self.javaclass_path]
        result = subprocess.run(evosuite_command, cwd=self.mavenproject_path)
        if result.returncode != 0:
            raise SubProcessError("Some exception has occured in Making EvoSuite Test!")

    def _getJavaEnvironment(self):
        print("path = " + self.getThisProjectPath())
        evosuite_compile_classpath = ':'.join([
            self.javaclass_path,
            path.join(self.getThisProjectPath(), "ext_modules", "evosuite-standalone-runtime-1.1.0.jar"),
            "evosuite-tests",
            path.join(self.getThisProjectPath(), "ext_modules", "junit-4.12.jar"),
            path.join(self.getThisProjectPath(), "ext_modules", "hamcrest-core-1.3.jar"),
            path.join(self.getThisProjectPath(), "ext_modules", "xstream", "xstream-1.4.15.jar"),
            path.join(self.getThisProjectPath(), "ext_modules", "xstream", "xstream", "*")
        ])
        java_environ = os.environ
        java_environ["CLASSPATH"] = evosuite_compile_classpath
        return java_environ
    
    def _getEvosuiteTestPath(self):
        javafiles = glob.glob(path.join(self.mavenproject_path, "evosuite-tests/**/*.java"), recursive=True)
        for esfile in javafiles:
            if getClassname(self.javasource_path)[0] + "_ESTest.java" in esfile:
                testcase_file = esfile
                break
        return testcase_file
    
    def compileEvosuiteTest(self):
        print("compileEvosuiteTest start")
        javafiles = glob.glob(path.join(self.mavenproject_path, "evosuite-tests/**/*.java"), recursive=True)
        testcase_file = self._getEvosuiteTestPath()
        try:
            self._addTestNumber(testcase_file)
        except:
            self._undoCopy(testcase_file, path.join(path.dirname(path.abspath(__file__)), "temp", "temp2.java"))
            raise
        command = ["javac", "-g"] + javafiles
        result = subprocess.run(command, env=self._getJavaEnvironment(), cwd=self.mavenproject_path)
        if result.returncode != 0:
            raise SubProcessError("Some exception has occured in Compiling EvoSuite Test!")
        self._undoCopy(testcase_file, path.join(path.dirname(path.abspath(__file__)), "temp", "temp2.java"))
    
    def _addTestNumber(self, ESTest_path):
        print("_addTestNumber start")
        try:
            source_lines = self._fileCopyAndMakeLineList(ESTest_path, path.join(path.dirname(path.abspath(__file__)), "temp", "temp2.java"))
            # source_lines = self._removeComment(source_lines)
            # print(source_lines)
            with open(ESTest_path, mode='w') as f:
                func_dive = 0
                in_func = False
                objectname = []
                imported = False
                for line in source_lines:
                    tokenized_line = Util.splitToken(line)
                    if len(tokenized_line) >= 3:
                        if tokenized_line[0] == "public" and tokenized_line[1] == "void" and "test" in tokenized_line[2]:
                            test_number = tokenized_line[2].replace("test", "")
                            print(line, file=f)
                            print("System.out.println(\"ESTest_test[" + test_number + "]\");", file=f)
                            func_dive = 1
                            in_func = True
                            continue
                    if in_func:
                        func_dive += tokenized_line.count('{')
                        func_dive -= tokenized_line.count('}')
                        if len(tokenized_line) >= 2:
                            if getClassname(self.javasource_path)[0] == tokenized_line[0] and Util.isIdentifier(tokenized_line[1]):
                                objectname.append(tokenized_line[1])
                        if func_dive == 0:
                            in_func = False
                            for o in objectname:
                                print("System.out.println(\"FilallyObjectAttributes_start[" + o + "]\");", file=f)
                                print("try{System.out.println(new XStream().toXML(" + o + "));}catch(Exception e){e.printStackTrace();}", file=f)
                                print("System.out.println(\"FilallyObjectAttributes_end[" + o + "]\");", file=f)
                            objectname = []
                            print(line, file=f)
                            continue
                    if not imported and "import" in tokenized_line:
                        print("import com.thoughtworks.xstream.XStream;", file=f)
                        imported = True
                    print(line.replace("mockJVMNonDeterminism = true", "mockJVMNonDeterminism = false").replace("(timeout = 4000)", ""), file=f)
        except:
            raise
    
    def execEvosuiteTest(self):
        print("execEvosuiteTest start")
        command = ["java", "org.junit.runner.JUnitCore", getPackagename(self.javasource_path) + "." + getClassname(self.javasource_path)[0] + "_ESTest"]
        result = subprocess.run(command, env=self._getJavaEnvironment(), cwd=self.mavenproject_path, stdout=subprocess.PIPE)
        self.output_list = result.stdout.decode("utf-8").split("\n")
        with open("out2", mode='w') as f:
            for l in self.output_list:
                print(l, file=f)
    
    def collectCoverage(self):
        print("collectCoverage start")
        testnum_str = "ESTest_test["
        linenum_str = "line["
        for line in self.output_list:
            if linenum_str in line:
                linenumber = 0
                i = line.find(linenum_str) + len(linenum_str)
                while i < len(line) and line[i].isdigit() and line[i] != ']':
                    linenumber = int(line[i]) + linenumber * 10
                    i += 1
                if not linenumber in self.exist_code_number:
                    self.exist_code_number.append(linenumber)
        self.exist_code_number.sort()
        for line in self.output_list:
            # print(line)
            if testnum_str in line:
                testnumber = 0
                i = line.find(testnum_str) + len(testnum_str)
                while i < len(line) and line[i].isdigit() and line[i] != ']':
                    testnumber = int(line[i]) + testnumber * 10
                    i += 1
                self.testcase_coverage["test" + str(testnumber)] = {}
                self.exist_test_number.append(testnumber)
                for exist_code_number in self.exist_code_number:
                    self.testcase_coverage["test" + str(testnumber)]["line" + str(exist_code_number)] = 0
                continue
            if linenum_str in line:
                linenumber = 0
                i = line.find(linenum_str) + len(linenum_str)
                while i < len(line) and line[i].isdigit() and line[i] != ']':
                    linenumber = int(line[i]) + linenumber * 10
                    i += 1
                self.testcase_coverage["test" + str(testnumber)]["line" + str(linenumber)] += 1
                continue
        print(self.testcase_coverage)
    
    def collectObjectXML(self):
        self.testcase_finalstate = {}
        testnum_str = "ESTest_test["
        XMLstart_str = "FilallyObjectAttributes_start["
        XMLend_str = "FilallyObjectAttributes_end["
        in_XML = False
        for line in self.output_list:
            if testnum_str in line:
                testnumber = 0
                i = line.find(testnum_str) + len(testnum_str)
                while i < len(line) and line[i].isdigit() and line[i] != ']':
                    testnumber = int(line[i]) + testnumber * 10
                    i += 1
                self.testcase_finalstate["test" + str(testnumber)] = {}
                continue
            if XMLstart_str in line:
                i = line.find(XMLstart_str) + len(XMLstart_str)
                buf = ""
                while i < len(line) and line[i].isalnum() and line[i] != ']':
                    buf += line[i]
                    i += 1
                xmlobject_name = buf
                self.testcase_finalstate["test" + str(testnumber)][xmlobject_name] = ""
                in_XML = True
                continue
            if XMLend_str in line:
                # i = line.find(XMLend_str) + len(XMLend_str)
                # buf = ""
                # while i < len(line) and line[i].isalnum() and line[i] != ']':
                #     buf += int(line[i])
                #     i += 1
                # xmlobject_name = buf
                in_XML = False
                continue
            if in_XML:
                self.testcase_finalstate["test" + str(testnumber)][xmlobject_name] += line + "\n"
        with open("out_attrs.json", mode='w') as f:
            json.dump(self.testcase_finalstate, fp=f, indent=4)
                
    
    def makeCoverageCsv(self):
        print("makeCoverageCsv start")
        with open(path.join(path.dirname(path.abspath(__file__)), "output.csv"), mode="w") as f:
            print(",", file=f, end="")
            for linenum in self.exist_code_number:
                print("line-" + str(linenum) + ",", file=f, end="")
            print("", file=f)
            self.exist_test_number.sort()
            # for testname, val in self.testcase_coverage.items():
            for testnumber in self.exist_test_number:
                print("test" + str(testnumber) + ",", file=f, end="")
                for linenum in self.exist_code_number:
                    print(str(self.testcase_coverage["test" + str(testnumber)]["line" + str(linenum)]) + ",", file=f, end="")
                print("", file=f)

def getClassname(filename:str):
    retval = []
    with open(filename) as f:
        in_comment = False
        for line in f.readlines():
            tokenized = Util.splitToken(line)
            if tokenized:
                if tokenized[0] == "//": continue
                for i, token in enumerate(tokenized):
                    if token == "//" and not in_comment: break
                    if token == "/*" and not in_comment:
                        in_comment = True
                        continue
                    elif token == "*/" and in_comment:
                        in_comment = False
                        continue
                    if token == "class" and not in_comment:
                        try:
                            if not tokenized[i + 1] in Util.symbol:
                                retval.append(tokenized[i + 1])
                        except IndexError as e:
                            print("Error line: " + line.rstrip(os.linesep))
    return retval

def getPackagename(filename:str):
    retval = ""
    with open(filename) as f:
        in_comment = False
        for line in f.readlines():
            if retval: break
            tokenized = Util.splitToken(line)
            if tokenized:
                for i, token in enumerate(tokenized):
                    if token == "//" and not in_comment: break
                    if token == "/*" and not in_comment:
                        in_comment = True
                        continue
                    elif token == "*/" and in_comment:
                        in_comment = False
                        continue
                    if token == "package" and not in_comment:
                        try:
                            buf = ""
                            token_ = tokenized[i+1]
                            j = i + 1
                            while token_ != ";":
                                buf += token_
                                j += 1
                                token_ = tokenized[j]
                            retval = buf
                            break
                        except IndexError as e:
                            print("Error line: " + line.rstrip(os.linesep))
    return retval

class Argument(argparse.ArgumentParser):

    def __init__(self, phase1_func, phase2_func):
        super().__init__(description="Auto SBFL debugging tool")
        self.sub_parser = self.add_subparsers(parser_class=argparse.ArgumentParser)
        phase1_parser = self.sub_parser.add_parser("phase1", help="Execute EvoSuite and create a test suite.")
        phase1_parser.add_argument("mavenproject_path", help="Root path of Maven project containing javasource_path")
        phase1_parser.add_argument("javasource_path", help="The java source path you want to debug")
        phase1_parser.set_defaults(handler=phase1_func)
        phase2_parser = self.sub_parser.add_parser("phase2", help="Calculate suspicious score")
        phase2_parser.add_argument("mavenproject_path", help="Root path of Maven project containing javasource_path")
        phase2_parser.add_argument("javasource_path", help="The java source path you want to debug")
        # phase2_parser.add_argument("expectedvaluefile_path", help="The path of the file that describes the final state of the object in each test of the displayed test case")
        phase2_parser.set_defaults(handler=phase2_func)
        help_parser = self.sub_parser.add_parser("help", help="See 'help -h'")
        help_parser.add_argument("command", help="Command name which help is shown")
        help_parser.set_defaults(handler=self._showHelp)
        
    def _showHelp(self, args):
        self.parse_args([args.command, '--help'])

if __name__ == "__main__":
    tool = Tool()

    argument = Argument(tool.phase1, tool.phase2)
    args = argument.parse_args()
    if hasattr(args, 'handler'):
        if not hasattr(args, 'command'):
            if hasattr(args, 'expectedvaluefile_path'):
                tool.setPath(args.mavenproject_path, args.javasource_path, args.expectedvaluefile_path)
            else:
                tool.setPath(args.mavenproject_path, args.javasource_path)
            try:
                args.handler()
            except:
                print(traceback.format_exc())
        else:
            args.handler(args)
    else:
        argument.print_help()
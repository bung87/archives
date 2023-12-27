# -*- coding:utf8 -*-
import ast
import sys
from io import StringIO
import astpretty
from enum import Enum

indent = "  "


class IfKind(Enum):
    IF = 'if'
    ELIF = 'elif'
    ELSE = 'else'


class SelfRenamer(ast.NodeTransformer):

    def visit_Attribute(self, node):
        if node.value.id == "self":
            node.value.id = "result"
        return node


class Visitor(ast.NodeVisitor):

    def __init__(self):
        self.stream = StringIO()
        self.indentLevel = 0
        self.classDefNode = None
        self.ifKind = None
        self.isAugAssign = False

    def enterClassDef(self, node):
        self.classDefNode = node

    def leaveClassDef(self, node):
        self.classDefNode = None

    def incIndent(self):
        self.indentLevel += 1

    def decIndent(self):
        self.indentLevel -= 1

    def writeIndent(self):
        self.stream.write(indent * self.indentLevel)

    def generic_visit(self, node):
        astpretty.pprint(node)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        self.stream.write(node.id)

    def visit_Assign(self, node):
        tl = len(node.targets)
        self.writeIndent()
        for i, c in enumerate(node.targets):
            self.visit(c)
            if i != tl - 1:
                self.stream.write(", ")
        self.stream.write(" = ")
        self.visit(node.value)
        self.stream.write("\n")

    def visit_AugAssign(self, node):
        self.writeIndent()
        self.visit(node.target)
        self.stream.write(" ")
        self.isAugAssign = True
        self.visit(node.op)
        self.isAugAssign = False
        self.stream.write("=")
        self.stream.write(" ")
        self.visit(node.value)

    def visit_Attribute(self, node):
        self.stream.write("{value}.{attr}".format(value=node.value.id, attr=node.attr))

    def visit_Num(self, node):
        self.stream.write(str(node.n))

    def visit_Str(self, node):
        self.stream.write('"{str}"'.format(str=node.s))

    def visit_Add(self, node):
        if self.isAugAssign:
            self.stream.write("+")
        else:
            self.stream.write(" + ")

    def visit_Sub(self, node):
        if self.isAugAssign:
            self.stream.write("-")
        else:
            self.stream.write(" - ")

    def visit_Mult(self, node):
        if self.isAugAssign:
            self.stream.write("*")
        else:
            self.stream.write(" * ")

    def visit_Div(self, node):
        if self.isAugAssign:
            self.stream.write("/")
        else:
            self.stream.write(" / ")

    def visit_FloorDiv(self, node):
        if self.isAugAssign:
            self.stream.write("div")
        else:
            self.stream.write(" div ")

    def visit_Pow(self, node):
        if self.isAugAssign:
            self.stream.write("^")
        else:
            self.stream.write(" ^ ")

    def visit_Gt(self, node):
        self.stream.write(" > ")

    def visit_Lt(self, node):
        self.stream.write(" < ")

    def visit_Mod(self, node):
        self.stream.write(" mod ")

    def visit_Eq(self, node):
        self.stream.write(" == ")

    def visit_NotEq(self, node):
        self.stream.write(" != ")

    def visit_ClassDef(self, node):
        self.enterClassDef(node)
        self.stream.write("type {typ}* = ref object\n".format(typ=node.name))
        self.incIndent()
        props = list(filter(lambda x: x.__class__ != ast.FunctionDef, node.body))

        funcs = list(filter(lambda x: x.__class__ == ast.FunctionDef, node.body))
        for c in props:
            self.visit(c)
        self.decIndent()
        self.stream.write("\n")

        for c in funcs:
            self.visit(c)
        self.leaveClassDef(node)

    def visit_Subscript(self, node):
        self.visit(node.value)
        if node.slice.__class__ == ast.Index:
            self.stream.write("[")
            self.visit(node.slice.value)
            self.stream.write("]")

    def visit_Dict(self, node):
        self.stream.write("{")
        ziped = list(zip(node.keys, node.values))
        zipedLen = len(ziped)
        for i, t in enumerate(ziped):
            self.visit(t[0])
            self.stream.write(": ")
            self.visit(t[1])
            if i != zipedLen - 1:
                self.stream.write(", ")

        self.stream.write("}")

    def visit_List(self, node):
        self.stream.write("@[")
        eltsLen = len(node.elts)
        for i, t in enumerate(node.elts):
            self.visit(t)
            if i != eltsLen - 1:
                self.stream.write(", ")

        self.stream.write("]")

    def visit_Call(self, node):
        self.writeIndent()
        if node.func.__class__ == ast.Name and node.func.id == "print":
            node.func.id = "echo"
        if node.func.__class__ == ast.Name:
            self.stream.write("{call}(".format(call=node.func.id))
        elif node.func.__class__ == ast.Attribute:
            self.stream.write("{o}.{p}(".format(o=node.func.value.id, p=node.func.attr))
        argsLen = len(node.args)
        for i, c in enumerate(node.args):
            self.visit(c)
            if i != argsLen - 1:
                self.stream.write(", ")
        self.stream.write(")")

    def visit_arg(self, node):
        if node.annotation:
            self.stream.write("{}: {}".format(node.arg, node.annotation.id))
        else:
            self.stream.write(node.arg)

    def visit_FunctionDef(self, node):
        isClassInit = node.name == '__init__'
        if isClassInit:
            # astpretty.pprint(node)
            cls = self.classDefNode.name
            node.name = "new{cls}".format(cls=cls)
            node.args.args.pop(0)
            node.returns = ast.Return(cls)
        returns = node.returns
        self.writeIndent()
        if node.name.startswith("_"):
            self.stream.write("proc {name}(".format(name=node.name))
        else:
            self.stream.write("proc {name}*(".format(name=node.name))
        argsLen = len(node.args.args)
        if self.classDefNode and not isClassInit:
            node.args.args[0].annotation = ast.Name(id=self.classDefNode.name)
        for i, c in enumerate(node.args.args):
            self.visit(c)
            if i != argsLen - 1:
                self.stream.write(", ")
        if returns:
            self.stream.write("): {typ} = \n".format(typ=returns.value))
        else:
            self.stream.write(") = \n")
        self.incIndent()
        renamer = SelfRenamer()
        for c in node.body:
            if isClassInit:
                self.visit(renamer.visit(c))
            else:
                self.visit(c)
        self.decIndent()
        self.stream.write("\n\n")

    def visit_Compare(self, node):
        self.visit(node.left)
        for op in node.ops:
            self.visit(op)
        for c in node.comparators:
            self.visit(c)

    def visit_If(self, node):
        self.writeIndent()
        if self.ifKind is None:
            self.stream.write("if ")
        else:
            self.stream.write(self.ifKind.value + " ")
        self.visit(node.test)
        self.stream.write(":\n")
        self.incIndent()
        for c in node.body:
            self.visit(c)
        self.decIndent()

        for o in node.orelse:
            if o.__class__ == ast.If:
                self.ifKind = IfKind.ELIF
            else:
                self.stream.write("else:\n")
                self.ifKind = IfKind.ELSE
            if self.ifKind == IfKind.ELSE:
                self.incIndent()
            self.visit(o)
            if self.ifKind == IfKind.ELSE:
                self.decIndent()

    def visit_For(self, node):
        self.stream.write("for ")
        target = node.target
        if target.__class__ == ast.Tuple:
            eltsLen = len(target.elts)
            for i, c in enumerate(target.elts):
                self.visit(c)
                if i != eltsLen - 1:
                    self.stream.write(", ")
        elif target.__class__ == ast.Name:
            self.visit(target)
        self.stream.write(" in ")
        self.visit(node.iter)
        self.stream.write(":\n")
        self.incIndent()
        for c in node.body:
            self.visit(c)
            self.stream.write("\n")
        self.decIndent()

    def visit_AnnAssign(self, node):
        self.stream.write("{name}:{typ} = ".format(name=node.target.id, typ=node.annotation.id))
        self.visit(node.value)

    def visit_Expr(self, node):
        self.visit(node.value)
        self.stream.write("\n")

    def run(self, code):
        n = ast.parse(code)
        self.visit(n)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as file:
            source = file.read()
            v = Visitor()
            v.run(source)

            # with open(sys.argv[1].replace(".py", ".nim"), "w") as file:
            #     file.write(convert_source)

from typed_ast import ast3
import os
import io
from typed_ast.ast3 import *
# from stdlib_list import stdlib_list


class Transformer(ast3.NodeTransformer):
    def visit(self, node):
        """Visit a node."""
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    # def visit_Module(self, node):
    #     return node

    # def visit_Import(self, node):
    #     return node

# class Transpiler(ast3.NodeVisitor):
#     def __init__(self, output):
#         self.output = output

#     def visit_Module(self, node):
#         return node


class Writer():
    def __init__(self, output):
        self.output = output
        # self.libraries = set(stdlib_list("3.6"))


if __name__ == "__main__":
    d = os.path.dirname(__file__)
    with open(os.path.join(d, "repo.py"))as f:
        c = f.read()
        root = ast3.parse(c)
        transed = Transformer().visit(root)
        output = io.StringIO()
        writer = Write(output)
        for x in ast3.walk(transed):
            if isinstance(x, Import):
                for y in x.names:
                    print(y.name, y.asname)

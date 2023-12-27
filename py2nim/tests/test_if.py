

from py2nim import Visitor


class TestIf:
    def test_one(self, loadFixture):
        v = Visitor()
        v.run(loadFixture("if.py"))
        print(v.stream.getvalue())
        v.stream.close()

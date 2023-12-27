from py2nim import Visitor


class TestClass:
    def test_one(self, loadFixture):
        v = Visitor()
        v.run(loadFixture("class.py"))
        print(v.stream.getvalue())
        v.stream.close()

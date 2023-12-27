from py2nim import Visitor


class TestNum:
    def test_one(self, loadFixture):
        v = Visitor()
        v.run(loadFixture("num.py"))
        print(v.stream.getvalue())
        v.stream.close()

from py2nim import Visitor


class TestFor:
    def test_one(self, loadFixture):
        v = Visitor()
        v.run(loadFixture("for.py"))
        print(v.stream.getvalue())
        v.stream.close()

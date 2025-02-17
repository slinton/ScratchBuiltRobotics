from tester import Tester

def test1(num):
    print(num)

if __name__ == '__main__':
    tester = Tester()
    tester.add("test1(5)")
    tester.run_tests()
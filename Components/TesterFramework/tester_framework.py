
def test1(num):
    print(num)

class Tester():
    def __init__(self) -> None:
        self.func_strings = []
        
    def add(self, func_string: str) -> None:
        self.func_strings.append(func_string)
        
    def print_tests(self) -> None:
        print('Test Options')

        for i in range(len(self.func_strings)):
            print(f'{i}:\t{self.func_strings[i]}')
        print(f'>={len(self.func_strings)}:\tQuit\n')
        
    def test_loop(self) -> None:
        while True:
            self.print_tests()
            try:
                index = int(input('Input selection: '))
                if index > len(self.func_strings):
                    return
                else:
                    print()
                    exec(self.func_strings[index])
                    print()
                    
            except Exception as e:
                print(f'Exception: {e}')
                
        
    def execute_all(self) -> None:
        for func_string in self.func_strings:
            try:
                exec(func_string)
            except Exception as e:
                print(f'Exception: {e}')
            
            
tester = Tester()
tester.add("test1(5)")

tester.test_loop()
print(i)
    
    
        
        
        

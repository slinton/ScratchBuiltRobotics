
def test1(num):
    print(num)

class Tester():
    
    def __init__(self) -> None:
        self.func_strings = []
        
    def add(self, func_string: str) -> None:
        self.func_strings.append(func_string)
        
    def execute(self) -> None:
        for func_string in self.func_strings:
            try:
                exec(func_string)
            except Exception as e:
                print(f'Exception: {e}')
            
            
tester = Tester()
tester.add("test1(5)")

tester.execute()
    
    
        
        
        

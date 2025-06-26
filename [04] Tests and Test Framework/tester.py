def test1(num):
    print(num)

class Tester():
    """Class to facilitate testing of devices and components.
    """
    
    def __init__(self) -> None:
        self.func_strings = []
        
    def add(self, func_string: str) -> None:
        self.func_strings.append(func_string)

    def execute(self, index: int = None) -> None:
        # Execute the specified test
        if index is not None:
            try:
                print()
                print(f'Executing: {self.func_strings[index]}')
                exec(self.func_strings[index])
            except Exception as e:
                print(f'Failed to execute {self.func_strings[index]} with Exception: {e}')

        # Execute all tests
        else:
            for i in range(len(self.func_strings)):
                self.execute(i)

    def display_menu(self) -> None:
        print()
        print('Test Menu:')
        for i, func_string in enumerate(self.func_strings):
            print(f'{i}: {func_string}')
        print('a: all')
        print('q: quit')

    def _is_valid_answer(answer: str) -> bool:
        return answer in ['a', 'q'] or answer.isdigit()

    def run_tests(self) -> None:
        answer = ''
        while answer != 'q':
            self.display_menu()
            answer = input('Enter selection: ')

            # Quit
            if answer == 'q':
                return
            
            # Execute all tests
            elif answer == 'a':
                self.execute()

            # Select one of the enumerated tests
            elif answer.isdigit():
                num = int(answer)
                if num >= 0 and num < len(self.func_strings):
                    self.execute(int(answer))
                else:
                    print(f'\nInvalid input. Must be between 0 and {len(self.func_strings) - 1}.')

            # Invalid input
            else:
                print('\nInvalid input. Must be a number or q.')
            

if __name__ == '__main__':
    tester = Tester()
    tester.add("test1(5)")
    tester.add("test1(8)")
    tester.run_tests()


    
    
        
        
        

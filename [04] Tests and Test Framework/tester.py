from functools import partial

class Tester:
    """Class to facilitate testing of devices and components."""

    def __init__(self) -> None:
        self.tests: list[tuple[str, callable]] = []

    def add(self, name: str, func: callable, *args, **kwargs) -> None:
        """Register a test with optional positional and keyword arguments."""
        bound = partial(func, *args, **kwargs)
        self.tests.append((name, bound))

    def execute(self, index: int | None = None) -> None:
        if index is not None:
            name, func = self.tests[index]
            try:
                print(f"\nExecuting: {name}")
                func()   # arguments already bound
            except Exception as e:
                print(f"Failed to execute {name} with Exception: {e}")
            return

        # Execute all tests
        for i in range(len(self.tests)):
            self.execute(i)

    def display_menu(self) -> None:
        print("\nTest Menu:")
        for i, (name, _) in enumerate(self.tests):
            print(f"{i}: {name}")
        print("a: all")
        print("q: quit")

    def run_tests(self) -> None:
        while True:
            self.display_menu()
            answer = input('Enter selection: ')

            if answer == 'q':
                return
            elif answer == 'a':
                self.execute()
            elif answer.isdigit():
                num = int(answer)
                if 0 <= num < len(self.tests):
                    self.execute(num)
                else:
                    print(f'\nInvalid input. Must be between 0 and {len(self.tests) - 1}.')
            else:
                print('\nInvalid input. Must be a number or q.')

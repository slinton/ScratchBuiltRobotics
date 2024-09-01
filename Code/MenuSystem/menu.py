#
# Menu
#
# TODO: add display object to display
#
from re import L
from typing import DefaultDict, List, Callable, Optional
from menu_item import MenuItem

class Menu:
    """Menu class for displaying a menu and getting user choice.
    """
    def __init__(self, menu_items: List[MenuItem]) -> None:
        """Initialize a new Menu object.

        Args:
            menu_items (List[MenuItem]): list of menu items.
        """
        self.menu_items: List[MenuItem] = menu_items # May not be needed
        self.menu_stack: List[List[MenuItem]] = []
        self.current_menu_items: List[MenuItem] = self.menu_items
        self.selected_index: int = 0
        if len(menu_items) > 0:
            self.selected = menu_items[0]
            
    def next(self)-> None:
        """Select the next menu item."""
        self.selected_index = (self.selected_index + 1) % len(self.current_menu_items)
        
    def previous(self)-> None:
        """Select the previous menu item."""
        self.selected_index = (self.selected_index - 1) % len(self.current_menu_items)
        
    def up(self)-> None:
        """Go back to the previous menu."""
        if len(self.menu_stack) > 0:
            self.current_menu_items = self.menu_stack.pop()
            self.selected_index = 0
        
    def act(self)-> None:
        """Call the action on the selected menu item. If the selected item has subitems, move to the subitems.
        Otherwise, call the action associated with the selected item."""
        selected_item = self.current_menu_items[self.selected_index]
        
        if selected_item.sub_items:
            self.menu_stack.append(self.current_menu_items) # Push the current menu onto the stack
            self.current_menu_items = selected_item.sub_items
            self.selected_index = 0
        else:
            selected_item()

    def print_all(self)-> None:
        """Print the menu items."""
        for item in self.menu_items:
            item.print()
            
    def print_current(self)-> None:
        """Print the menu items."""
        for i in range(len(self.current_menu_items)):
            if i == self.selected_index:
                print(f"> {self.current_menu_items[i]}")
            else:
                print(f"  {self.current_menu_items[i]}")
            
    def __call__(self)-> None:
        """This method is called when the Menu is 'called' as a function. """
        self.act()


if __name__ == "__main__":
    menu = Menu(menu_items = [
        MenuItem("Option 1", action=lambda: print("Option 1 called")),
        MenuItem("Option 2", sub_items=[
            MenuItem("Back", action=lambda: menu.up()),
            MenuItem("Option 2.1"), 
            MenuItem("Option 2.2")]),
        MenuItem("Option 3"),
    ])
    
    print('Full Menu:')
    menu.print_all()
    print('')
    
    print('Initial Menu')
    menu.print_current()
    
    print('Next')
    menu.next()
    menu.print_current()
    
    print('Next')
    menu.next()
    menu.print_current()
    
    print('Previous')
    menu.previous()
    menu.print_current()
    
    print('Call Menu')
    menu()
    menu.print_current()
    
    print('Call Menu')
    menu()
    menu.print_current()
    
    # print('Up')
    # menu.up()
    # menu.print_current()
    
    print('Call Menu')
    menu()
    menu.print_current()
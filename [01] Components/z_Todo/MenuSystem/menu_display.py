#
# MenuDisplay
#
# Version 24_07_31_04
#
# Todo: Add WindowedMenuItems
#
from screen import Screen
from rotary_encoder import RotaryEncoder
from menu_item import MenuItem
from menu import Menu
import uasyncio as asyncio

class MenuDisplay:
    def __init__(self)-> None:
        self.menu = Menu(
            menu_items = [ MenuItem("Option 1", action=lambda: print("Option 1 called")),
                           MenuItem("Option 2", sub_items=[
                               MenuItem("Back", action=lambda: self.menu.up()),
                               MenuItem("Option 2.1"),
                               MenuItem("Option 2.2")]),
                           MenuItem("Option 3"),
                           ])
        self.screen = Screen()
        self.encoder = RotaryEncoder(
            on_right_func=self.menu_next,
            on_left_func=self.menu_previous,
            on_button_down_func=self.menu_action)

    def menu_next(self)-> None:
        self.menu.next()
        self.display_current_menu()
        
    def menu_previous(self)-> None:
        self.menu.previous()
        self.display_current_menu()
        
    def menu_action(self)-> None:
        print('action')
        self.menu.act()
        self.display_current_menu()
        
    def display_current_menu(self)-> None:
        self.menu.print_current()
        self.screen.fill()
        for i in range(len(self.menu.current_menu_items)):
            message = '> ' if self.menu.selected_index == i else '  '
            message += self.menu.current_menu_items[i].name
            print(f'{i}: {message}')
            self.screen.display(message=message, position=(10, 10 + 25*i), fontsize=2)
        
    async def run_loop(self)-> None:
        """Loop to run all the elements
        """
        self.display_current_menu()
        await self.encoder.run_loop()
        
        
    def start(self)-> None:
        """Syncronous method to start the rotary encoder and button functions."""
        asyncio.run(self.run_loop())
    
    
if __name__ == '__main__':
    menu_display = MenuDisplay()
    menu_display.start()
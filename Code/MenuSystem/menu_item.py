#
# MenuItem
#
from __future__ import annotations
from typing import List, Callable, Optional, Union


class MenuItem:
    """Represents a menu item in a menu system. A MenuItem can have an action associated with it, or can have subitems.
    """
    def __init__(self, 
                 name: str, 
                 action: Optional[Callable]=None, 
                 sub_items: Optional[List[MenuItem]]=None)-> None:
        """Initialize a new MenuItem object. 

        Args:
            name (str): _description_
            action (Callable, optional): function to call if this item is selected. Defaults to None.
            sub_items (List[MenuItem], optional): list of subitems. Defaults to None.
        """
        self.name: str = name
        self.parent_item: Union[MenuItem, None] = None
        self.action: Optional[Callable] = action
        self.sub_items: Optional[List[MenuItem]] = sub_items
        self.selected: Optional[MenuItem] = None
         
        if self.sub_items:           
            for item in self.sub_items:
                item.parent_item = self
            self.selected = self.sub_items[0]

    def __str__(self)-> str:
        """Return the name of the MenuItem."""
        return self.name
    
    def print(self, prefix: str = "")-> None:
        """Print the MenuItem and any subitems. 

        Args:
            prefix (str, optional): prefix to print before the MenuItem. Defaults to "".
        """
        print(f"{prefix}{self.name}")
        if self.sub_items:
            for item in self.sub_items:
                item.print(prefix + "\t")

    def __call__(self)-> None:
        """This method is called when the MenuItem is 'called' as a function. """
        if self.action:
            self.action()
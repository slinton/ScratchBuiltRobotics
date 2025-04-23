#
# StatusPanel
#
# V 2025_04_22_01
from machine import Pin

class StatusPanel:
    def __init__(self, ble_pin_id: int=6, auto_pin_id:int=7): 
        self._ble_status: bool = False  
        self._auto_status: bool = False  
        self._ble_pin: Pin = Pin(ble_pin_id, Pin.OUT)
        self._auto_pin: Pin = Pin(auto_pin_id, Pin.OUT)
        self.ble_status = False
        self.auto_status = False

    @property
    def ble_status(self) -> bool:
        return self._ble_status
    
    @ble_status.setter
    def ble_status(self, status: bool) -> None:
        self._ble_status = status
        self._ble_pin.value(status)

    @property
    def auto_status(self) -> bool:
        return self._auto_status
    
    @auto_status.setter
    def auto_status(self, status: bool) -> None:
        self._auto_status = status
        self._auto_pin.value(status)
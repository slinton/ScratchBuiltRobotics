#
# StatusPanel
#
# Version: 1.00
# Date: 2025-05-31
# Author: Sam Linton
# Description: A status panel class for Raspberry Pi Pico that manages BLE, power and autonomous status indicators.
#
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


if __name__ == "__main__":
    try:
        from time import sleep

        status_panel = StatusPanel()
        print("Status Panel Test")

        for ble_status in [True, False]:
            status_panel.ble_status = ble_status
            print(f'BLE Status: {status_panel.ble_status}')
            for auto_status in [True, False]:
                status_panel.auto_status = auto_status
                print(f'Auto Status: {status_panel.auto_status}')
                sleep(1)
            sleep(1)
        print("Status panel test completed.")

    except KeyboardInterrupt
        print("Exiting status panel test.")

    except Exception as e:
        print(f"An error occurred: {e}")


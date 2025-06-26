from status_panel import StatusPanel
from time import sleep

# from machine import Pin
status_panel = StatusPanel(ble_pin_id=6, auto_pin_id=7)

status_panel.ble_status = True
print(f"Setting BLE Status to {status_panel.ble_status}")
status_panel.auto_status = True
print(f"Setting Auto Status to {status_panel.auto_status}")
sleep(2)
status_panel.ble_status = False
print(f"Setting BLE Status to {status_panel.ble_status}")
status_panel.auto_status = False
print(f"Setting Auto Status to {status_panel.auto_status}")
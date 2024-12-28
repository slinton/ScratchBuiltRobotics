#
# BLEServer
#
# Version 24_07_31_04
#
# 
import aioble
import bluetooth
from micropython import const
import uasyncio as asyncio

_GENERIC_SERVICE_UUID = bluetooth.UUID(0x1848)
_GENERIC_CHAR_UUID = bluetooth.UUID(0x2A6E)
_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL = const(384)

class BLEServer:
    """Class to create a BLE server that advertises a service and characteristic.
    This class can be instantiated and provided with a function that creates a message
    to be sent by the server. The message is sent at a regular interval.
    """
    
    def __init__(self,
                 name:str,
                 create_message_func=None,
                 on_connected_func=None,
                 on_disconnected_func=None,
                 send_interval_ms:int=1000,
                 service_uuid:bluetooth.UUID=_GENERIC_SERVICE_UUID,
                 char_uuid:bluetooth.UUID=_GENERIC_CHAR_UUID)->None:
        """Initialize the BLEServer object.

        Args:
            name (str): Name of the BLE server. This is used by the client to recognize the server.
            create_message_func (function, optional): User-provided function that provides a string to 
                be sent by the server. Defaults to None.
            on_connected_func: (function, optional): Called when the server connects to a client
            on_disconnected_func: (function, optional): Called when the server disconnect from a client
            send_interval_ms (int, optional): Interval between sends, in ms. Defaults to 1000.
            service_uuid (UUID, optional): Service UUID. Defaults to _GENERIC_SERVICE_UUID.
            char_uuid (UUID, optional): Characteristic UUID. Defaults to _GENERIC_CHAR_UUID.
        """
        self.name = name
        self.create_message_func = create_message_func
        self.on_connected_func = on_connected_func
        self.on_disconnected_func = on_disconnected_func
        self.send_interval_ms = send_interval_ms
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.connection = None
        self.characteristic = None
        self.createService()
        
    def start(self)-> None:
        """Non-synchronous method to start the main loop"""
        asyncio.run(self.run_loop())
        
    async def run_loop(self)-> None:
        """Run the main loop to connect and send messages"""
        while True:
            try:
                if self.is_connected():
                    self.show_connected(True)
                    await self.send_message()
                    await asyncio.sleep_ms(self.send_interval_ms)
                else:
                    if self.connection and self.on_disconnected_func:
                        self.on_disconnected()
                    await self.connect_to_client()
                    if self.on_connected_func:
                        self.on_connected_func()
            except Exception as e:
                print(f'Exception: {e}')
                self.connection = None
                
    def is_connected(self)->bool:
        return not self.connection == None and self.connection.is_connected() 
             
        
    async def send_message(self)->None:
        message_str = 'x'
        if not self.create_message_func == None:
            message_str = self.create_message_func()
        message = bytearray(message_str, 'utf-8')
        self.characteristic.write(message)
        self.characteristic.notify(self.connection, message)
        
    async def connect_to_client(self)->None:
        print('Advertising...',end='')
        self.connection = await aioble.advertise(
                1000, 
                name=self.name, 
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[self.service_uuid]
        )
        print("connected to:", self.connection.device)
        print(f'Is connected: {self.connection.is_connected()}')
        
    def createService(self)-> None:
        """Create the service and characteristic for the BLE server and registers
        the service. This function is called during initialization.
        """
        print('createService')
        service = aioble.Service(self.service_uuid)
        self.characteristic = aioble.Characteristic(
            service,
            self.char_uuid,
            read = True,
            notify = True
        )
        aioble.register_services(service)
    
    
if __name__ == "__main__":
    try:
        bleServer = BLEServer('JoystickController')
        bleServer.start()
    
    except KeyboardInterrupt:
        print('Program terminated')
        
        
    

#
# BLEServer
#
# Version: 1.00
# Date: 2025-05-30
# Author: Sam Linton
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
            create_message_func (_type_, optional): User-proviced function that provides a string to 
                be sent by the server. Defaults to None.
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
        
    def start(self)->None:
        """Start the BLE server loop."""
        asyncio.run(self.run_loop())
        
    async def run_loop(self)->None:
        """Run the main loop of the BLE server.
        This loop will continuously check for connection, send messages, and handle disconnections.
        """
        while True:
            try:
                if self.is_connected():
                    await self.send_message()
                    await asyncio.sleep_ms(self.send_interval_ms)
                else:
                    if self.connection and self.on_disconnected_func:
                        self.on_disconnected_func()
                    await self.connect_to_client()
                    if self.on_connected_func:
                        self.on_connected_func()
            except Exception as e:
                print(f'Exception: {e}')
                self.connection = None          
                
    def is_connected(self)->bool:
        """Check if the BLE server is connected to a client.
        Returns: 
            bool: True if connected, False otherwise.
        """
        return not self.connection == None and self.connection.is_connected() 
        
    async def send_message(self)->None:
        """Send a message to the connected client.
        If a user-provided function is defined, it will be called to create the message.
        If no function is provided, a default message 'x' will be sent.
        """
        message_str = 'x'
        if not self.create_message_func == None:
            message_str = self.create_message_func()
        message = bytearray(message_str, 'utf-8')
        self.characteristic.write(message)
        self.characteristic.notify(self.connection, message)
        
    async def connect_to_client(self)->None:
        """Connect to a client that is advertising the service.
        This function will advertise the service and wait for a client to connect.
        If a client connects, it will set the connection attribute and print the device information.
        """
        print('Advertising...', end='')
        self.connection = await aioble.advertise(
                1000, 
                name=self.name, 
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[self.service_uuid]
        )
        print("connected to:", self.connection.device)
        print(f'Is connected: {self.connection.is_connected()}')
        
    def createService(self):
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
        
        
    

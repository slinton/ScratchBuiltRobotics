#
# BLEServer
#
# TODO: should there be an additional non async function inside send_message for subclass
# to override?

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
                 send_message_func=None,
                 send_interval_ms:int=1000,
                 service_uuid:bluetooth.UUID=_GENERIC_SERVICE_UUID,
                 char_uuid:bluetooth.UUID=_GENERIC_CHAR_UUID)->None:
        """Initialize the BLEServer object.

        Args:
            name (str): Name of the BLE server. This is used by the client to recognize the server.
            send_message_func (_type_, optional): User-proviced function that provides a string to 
                be sent by the server. Defaults to None.
            send_interval_ms (int, optional): Interval between sends, in ms. Defaults to 1000.
            service_uuid (UUID, optional): Service UUID. Defaults to _GENERIC_SERVICE_UUID.
            char_uuid (UUID, optional): Characteristic UUID. Defaults to _GENERIC_CHAR_UUID.
        """
        self.name = name
        self.send_message_func = send_message_func
        self.send_interval_ms = send_interval_ms
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.connected = False
        self.connection = None
        self.characteristic = None
        self.createService()
        
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
    
    async def advertise(self, interval_ms:int=250_000)->None:
        """Advertise the BLE server. This function is called by the start function.
        If the server is disconnected, it will resume advertising.

        Args:
            interval_ms (int, optional): Interval of advertising, ms. Defaults to 250_000.
        """
        print('advertise')
        while True:
            print('start advertising')
            async with await aioble.advertise(
                interval_ms, 
                name=self.name, 
                appearance=_BLE_APPEARANCE_GENERIC_REMOTE_CONTROL, 
                services=[self.service_uuid]
            ) as self.connection:
                print("connection from", self.connection.device)
                self.connected = True
                await self.connection.disconnected()
                self.connected = False
                print(f'disconnected')
    
    async def send_message(self)->None:
        """Send a message at regular intervals. The message is created by the send_message_func
        """
        while True:
            if self.connected:
                print('send_message')
                message_str = ''
                if not self.send_message_func == None:
                    print('calling update_func')
                    message_str = self.send_message_func()
                message = bytearray(message_str, 'utf-8')
                self.characteristic.write(message)
                self.characteristic.notify(self.connection, message)
            await asyncio.sleep_ms(self.send_interval_ms)
    
            
    async def start(self)->None:
        """Start the BLE server. This function creates two tasks: advertise and send_message.
        """
        print('start')
        tasks = [
            asyncio.create_task(self.advertise()),
            asyncio.create_task(self.send_message()),
        ]
        await asyncio.gather(*tasks)
    
    
    
async def main()->None:
    """Test Method
    """
    bleServer = BLEServer('BLE Test')
    await bleServer.start()
    
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print(f'End')
        
        
    
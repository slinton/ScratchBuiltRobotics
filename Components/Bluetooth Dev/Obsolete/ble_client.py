#
# BLEClient
#
import aioble
import bluetooth
import uasyncio as asyncio
from typing import Callable

_GENERIC_SERVICE_UUID = bluetooth.UUID(0x1848) # data service UUID
_GENERIC_CHAR_UUID = bluetooth.UUID(0x2A6E) # char

_REMOTE_CHARACTERISTICS_UUID = bluetooth.UUID(0x2A6E)

class BLEClient:
    """Class to create a BLE client that connects to a server and receives messages.
    """
    
    def __init__(self,
                 server_name:str,
                 receive_message_func = None,
                 receive_interval_ms:int = 1000,
                 service_uuid:bluetooth.UUID = _GENERIC_SERVICE_UUID,
                 char_uuid:bluetooth.UUID = _GENERIC_CHAR_UUID)->None:
        """Initialize the BLEClient object.

        Args:
            server_name (str): Name of server to connect to.
            receive_message_func (_type_, optional): User provided function called when the client receives a message. 
                Defaults to None.
            receive_interval_ms (int, optional): Interval between receives, ms. Defaults to 1000.
            service_uuid (UUID, optional): Service UUID. Defaults to _GENERIC_SERVICE_UUID.
            char_uuid (UUID, optional): Characteristic UUID. Defaults to _GENERIC_CHAR_UUID.
        """
        self.server_name = server_name
        self.receive_message_func = receive_message_func
        self.receive_interval_ms = receive_interval_ms
        self.service_uuid = service_uuid
        self.char_uuid = char_uuid
        self.characteristic = None
        self.ready = False
        
    async def receive_message(self)->None:
        """Receive a message from the server. This function is callled periodically
        """
        print('receive message')
        while True:
            if self.ready:
                try:
                    command = await self.characteristic.read()
                    command_str = command.decode('utf-8')
                    print(command_str)
                    if self.receive_message_func:
                        self.receive_message_func(command_str)
                except TypeError:
                    print(f'something went wrong; server disconnected?')
                    self.ready = False
                except asyncio.TimeoutError:
                    print(f'something went wrong; timeout error?')
                    self.ready = False
                except asyncio.GattError:
                    print(f'something went wrong; Gatt error - did the server die?')
                    self.ready = False
                except Exception as e:
                    print(f'receive_message exception: {e}')
                    self.ready = False
            await asyncio.sleep_ms(self.receive_interval_ms)
        
    async def start_ble(self)->None:
        """Start the BLE client and attempt connect to a server if it is not already connected.
        """
        print('start_ble')
        while True:
            if not self.ready:
                print('attempting to start ble')
                try:
                    device = await self.find_server()
                    print(device)
                    connection = await device.connect()
                    print(connection)
                    service = await connection.service(self.service_uuid)
                    print(service)
                    self.characteristic = await service.characteristic(self.char_uuid)
                    print(self.characteristic)
                    if not self.characteristic == None:
                        self.ready = True
                        print(f'self.ready = {self.ready}')
                except asyncio.TimeoutError:
                    print("Timeout during connection")
                except Exception as e:
                    print(f'start_ble exception: {e}')
            await asyncio.sleep_ms(1000)
                
        
    async def find_server(self):
        """Find the server with the name server_name and service_uuid.

        Returns:
            device: server
        """
        while True:
            async with aioble.scan(5000, interval_us=30_000, window_us=30_000, active=True) as scanner:
                async for result in scanner:
                    if result.name() == self.server_name and self.service_uuid in result.services():
                        return result.device
    
    async def start(self)->None:
        """Start the BLE client. This function creates two tasks: start_ble and receive_message.
        """
        print('start')
        tasks = [
            asyncio.create_task(self.start_ble()),
            asyncio.create_task(self.receive_message())
        ]
        await asyncio.gather(*tasks)



async def main():
    client = BLEClient("BLE Test")
    await client.start()
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print('End')
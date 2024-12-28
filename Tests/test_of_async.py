#
# Test of async
#
from time import sleep
import uasyncio as asyncio


async def beep():
    for i in range(5):
        print(f'beep')
        await asyncio.sleep(1)
   
async def boop():
    for i in range(5):
        print('boop')
        await asyncio.sleep(1)
        
    

async def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(beep())
    print('end of main')
    
    await asyncio.gather(beep(), boop())
    
    
if __name__ == '__main__':
    asyncio.run(main())
    
# Adding to a running loop:
# import asyncio
# 
# async def cor1():
#     ...
# 
# async def cor2():
#     ...
# 
# async def main(loop):
#     await asyncio.sleep(0)
#     t1 = loop.create_task(cor1())
#     await cor2()
#     await t1
# 
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))
# loop.close()
    
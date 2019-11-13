import aiohttp
import asyncio


f = open('CREATEFILE', 'rb')
data = f.read()


async def main():
    async with aiohttp.ClientSession() as session:
        try:
            result = await session.post('http://127.0.0.1:20003/file/CREATEFILE', data=data)
            print(result.status)
        except Exception as e:
            print(e)


asyncio.run(main())
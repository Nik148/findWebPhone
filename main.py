from aiohttp import ClientSession
import re
import asyncio
from typing import List


urls = ['https://repetitors.info/', "https://hands.ru/company/about"]

async def find_phone(client: ClientSession, url: str):
    async with client.get(url) as resp:
        assert resp.status == 200
        html = await resp.text()
        
    matches = re.findall(r"(?:(?:8|\+7)[\- ]?)?(?:\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}", html)
    phones = []
    r = re.compile('^\+7|8\D*\d{3}\D*\d{3}\D*\d{2}\D*\d{2}')
    for match in matches:
        if r.search(match):
            phones.append(match)
    return phones


async def get_phone_from_web(urls: List):
    phones = []
    async with ClientSession() as session:
        phones = await asyncio.gather(*(find_phone(session, url) for url in urls))
    print(phones)
    return phones

if __name__ == "__main__":
    asyncio.run(get_phone_from_web(urls))




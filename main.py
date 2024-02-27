import time
import json
import pprint

import asyncio
import aiohttp
from bs4 import BeautifulSoup

url = "https://kwork.ru/projects?a=1&fc=37&prices-filters%5B%5D=4&prices-filters%5B%5D=3&view=0&page=3"


async def main():

    text = None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            print(response.status)
            text = await response.text()

    soup = BeautifulSoup(text, 'html.parser')
    result = None

    for sc in soup.find_all('script'):
        if "window.stateData" in str(sc):
            result = str(sc)
            break

    # print(result)
    index = result.find("window.stateData=") + len("window.stateData=")
    print(index)
    crob_text = result[index:]
    index = crob_text.find(";</script>")
    crob_text = crob_text[:index]
    data = json.loads(crob_text)
    dict_data = dict(data)

    orders = dict_data["wantsListData"]['pagination']['data']
    page = dict_data['wantsListData']['pagination']['current_page']

    print("current page = ", page)

    for ord in orders:
        name = ord.get("name")
        with open(f'{name}.json', 'w') as file:
            json.dump(ord, file, ensure_ascii=False, indent=True)


if __name__ == "__main__":
    asyncio.run(main())



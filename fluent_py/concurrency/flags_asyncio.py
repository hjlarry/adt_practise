import asyncio
import aiohttp
from flags import BASE_URL, save_flag, show, main


async def get_flag(cc):
    resp = await aiohttp.request("GET", f"{BASE_URL}/{cc.lower()}/{cc.lower()}.gif")
    image = await resp.read()
    return image


async def download_one(cc):
    image = await get_flag(cc)
    show(cc)
    save_flag(image, cc.lower() + ".gif")
    return cc


def download_many(cc_list):
    loop = asyncio.get_event_loop()
    to_dos = [download_one(cc) for cc in sorted(cc_list)]
    wait_coro = asyncio.wait(to_dos)
    res, _ = loop.run_until_complete(wait_coro)
    loop.close()
    return len(res)


if __name__ == "__main__":
    main(download_many)

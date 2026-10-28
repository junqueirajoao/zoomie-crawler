import asyncio

import httpx


async def fetch_url(url):
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        response = await client.get(url)
        return response.status_code, len(response.text)

async def main():
    urls = [
        "https://www.google.com",
        "https://www.python.org",
        "https://www.github.com"
    ]
    
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, (status_code, html_length) in zip(urls, results):
        print(f"URL: {url}, Status Code: {status_code}, HTML Length: {html_length}")


if __name__ == "__main__":
    asyncio.run(main())
import httpx


class HttpxClient:

    @staticmethod()
    async def get(*args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.get(*args, **kwargs)

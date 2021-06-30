import httpx


class HttpxClient:

    @staticmethod
    async def get(*args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.get(*args, **kwargs)

    @staticmethod
    async def post(*args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.post(*args, **kwargs)

    @staticmethod
    async def put(*args, **kwargs):
        async with httpx.AsyncClient() as client:
            return await client.put(*args, **kwargs)

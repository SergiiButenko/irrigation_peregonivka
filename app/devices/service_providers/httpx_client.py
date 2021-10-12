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

    @staticmethod
    async def put_with_raise(*args, **kwargs):
        res = HttpxClient.put(*args, **kwargs)
        res.raise_for_status()
        return res

    @staticmethod
    async def post_with_raise(*args, **kwargs):
        res = HttpxClient.post(*args, **kwargs)
        res.raise_for_status()
        return res

    @staticmethod
    async def get_with_raise(*args, **kwargs):
        res = HttpxClient.get(*args, **kwargs)
        res.raise_for_status()
        return res

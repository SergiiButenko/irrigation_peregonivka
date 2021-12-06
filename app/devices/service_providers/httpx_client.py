import httpx


class HttpxClient:
    TIMEOUT = httpx.Timeout(10.0, connect=60.0)
    # transport = httpx.HTTPTransport(retries=1)

    @staticmethod
    async def get(*args, **kwargs):
        async with httpx.AsyncClient(timeout=HttpxClient.TIMEOUT) as client:
            return await client.get(*args, **kwargs)

    @staticmethod
    async def post(*args, **kwargs):
        async with httpx.AsyncClient(timeout=HttpxClient.TIMEOUT) as client:
            return await client.post(*args, **kwargs)

    @staticmethod
    async def put(*args, **kwargs):
        async with httpx.AsyncClient(timeout=HttpxClient.TIMEOUT) as client:
            return await client.put(*args, **kwargs)

    @staticmethod
    async def put_with_raise(*args, **kwargs):
        res = await HttpxClient.put(*args, **kwargs)
        res.raise_for_status()
        return res

    @staticmethod
    async def post_with_raise(*args, **kwargs):
        res = await HttpxClient.post(*args, **kwargs)
        res.raise_for_status()
        return res

    @staticmethod
    async def get_with_raise(*args, **kwargs):
        res = await HttpxClient.get(*args, **kwargs)
        res.raise_for_status()
        return res

import asyncio
import json
import random
from pathlib import Path

import httpx
from django.http import JsonResponse
from django.shortcuts import render

from concurrent.futures import ThreadPoolExecutor
from django_sync_or_async.utils import timeit

current_dir = Path(__file__).resolve().parent
exampledata = json.load(open(f"{current_dir}/assets/countries.json"))

API_ENDPOINT = "http://localhost:5000"


async def api(request, ms=300):
    await asyncio.sleep(delay=ms / 1000)
    return JsonResponse(random.choice(exampledata))


def sync_view(request, ms=300):
    api_urls = (
        f"{API_ENDPOINT}/{ms}/",
        f"{API_ENDPOINT}/{ms*2}/",
        f"{API_ENDPOINT}/{int(ms/2)}/",
    )

    with timeit() as t:
        client = httpx.Client()

        with ThreadPoolExecutor() as executor:
            futures = executor.map(lambda url: client.get(url), api_urls)
        client.close()

        country = next(futures).json()

    return render(
        request,
        "django_sync_or_async/index.html",
        dict(country=country, time=t),
    )


async def async_view(request, ms=300):
    api_urls = (
        f"{API_ENDPOINT}/{ms}/",
        f"{API_ENDPOINT}/{ms*2}/",
        f"{API_ENDPOINT}/{int(ms/2)}/",
    )

    with timeit() as t:
        client = httpx.AsyncClient()

        results = await asyncio.gather(*[client.get(url) for url in api_urls])
        await client.aclose()

        country = results[0].json()

    return render(
        request,
        "django_sync_or_async/index.html",
        dict(country=country, time=t),
    )

import sys
import os

# Add parent project folder to Python path
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import pytest
import httpx

from main import check_url


# Test successful URL
@pytest.mark.asyncio
async def test_valid_url():

    async with httpx.AsyncClient() as client:

        result = await check_url(
            client,
            "https://google.com"
        )

        assert result["status"] == 200
        assert result["response_time_ms"] is not None


# Test invalid URL
@pytest.mark.asyncio
async def test_invalid_url():

    async with httpx.AsyncClient() as client:

        result = await check_url(
            client,
            "https://invalid-url-test-123.com"
        )

        assert result["status"] == "ERROR"


# Test timeout handling
@pytest.mark.asyncio
async def test_timeout():

    async with httpx.AsyncClient() as client:

        result = await check_url(
            client,
            "https://httpstat.us/200?sleep=10000"
        )

        assert result["status"] in [
            "TIMEOUT",
            "ERROR"
        ]
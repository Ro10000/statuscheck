import asyncio
import argparse
import json
import time

import httpx
from tabulate import tabulate


# Check one URL
async def check_url(client, url):

    start = time.perf_counter()

    try:

        response = await client.get(
            url,
            timeout=5,
            follow_redirects=True
        )

        end = time.perf_counter()

        return {
            "url": url,
            "status": response.status_code,
            "response_time_ms": round(
                (end - start) * 1000,
                2
            )
        }

    except httpx.TimeoutException:

        return {
            "url": url,
            "status": "TIMEOUT",
            "response_time_ms": None
        }

    except Exception:

        return {
            "url": url,
            "status": "ERROR",
            "response_time_ms": None
        }


# Run all URLs concurrently
async def check_all_urls(urls):

    async with httpx.AsyncClient() as client:

        tasks = [
            check_url(client, url)
            for url in urls
        ]

        results = await asyncio.gather(*tasks)

        return results


# Load URLs from file
def load_urls(file_name):

    with open(file_name, "r") as file:

        return [
            line.strip()
            for line in file
            if line.strip()
        ]


# Print table output
def print_table(results):

    rows = []

    for result in results:

        rows.append([
            result["url"],
            result["status"],
            result["response_time_ms"]
        ])

    print(
        tabulate(
            rows,
            headers=[
                "URL",
                "STATUS",
                "TIME (ms)"
            ],
            tablefmt="grid"
        )
    )


# Main function
def main():

    parser = argparse.ArgumentParser(
        description="Async URL Status Checker"
    )

    parser.add_argument(
        "--urls",
        nargs="+",
        help="URLs to check"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON"
    )

    parser.add_argument(
        "--file",
        default="urls.txt",
        help="File containing URLs"
    )

    args = parser.parse_args()

    # Get URLs
    if args.urls:
        urls = args.urls
    else:
        urls = load_urls(args.file)

    # Run async checker
    results = asyncio.run(
        check_all_urls(urls)
    )

    # JSON output
    if args.json:

        print(
            json.dumps(
                results,
                indent=4
            )
        )

    # Table output
    else:

        print_table(results)


if __name__ == "__main__":
    main()
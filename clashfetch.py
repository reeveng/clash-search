import asyncio
import json

import httpx


async def get_clash(session: httpx.AsyncClient, clash_handle: str):
    url = "https://www.codingame.com/services/Contribution/findContribution"
    response = await session.request("POST", url, json=[clash_handle, True])
    if response.status_code == 200:
        with open(f"clashes/{clash_handle}.json", "w") as f:
            f.write(response.text)
    else:
        print(f"\nProblem fetching clash {clash_handle}\n\t{response.reason_phrase}")


async def amain(handles: list[str], n: int = 10):
    async with httpx.AsyncClient() as session:
        i = 0
        while i + n < len(handles):
            print(end=".", flush=True)
            coroutines = [get_clash(session, handle) for handle in handles[i:i+n]]
            await asyncio.gather(*coroutines)
            i += n


def read_clash_list(fname: str):
    with open(fname, "r") as f:
        clash_json = json.load(f)
    return [clash["publicHandle"] for clash in clash_json]


# If you got a list of clashes from https://www.codingame.com/services/Contribution/getAcceptedContributions
# you can save the json to file and use this:
# all_handles = read_clash_list("list_of_clashes.json")

test_handles = [
    "52980368bdbd05abdd789a04173b57b0fdea",
    "682102420fbce0fce95e0ee56095ea2b9924",
]

asyncio.run(amain(test_handles))
